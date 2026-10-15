#!/usr/bin/env python3
"""Incremental five-year historical recovery for Special Robotics Radar.

This is NOT a second pass over the most recent API results. Each job is a
specific publication-half-year + topic + provider, with an on-disk checkpoint.
The job is idempotent, rate-limited, and resumable across daily deployments.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

from dateutil.relativedelta import relativedelta

import main as radar

STATE = radar.DOCS / "backfill_progress.json"
REPORT = radar.DOCS / "backfill_report.md"
UTC = timezone.utc


def historical_windows(now: datetime, months: int = 60) -> list[tuple[datetime, datetime]]:
    """Half-year slices of archived years, respecting the rolling cutoff.

    Current-year discovery stays with the existing daily collector. Split
    archived years into H1/H2 so top-70 results do not always hide January.
    """
    cutoff = (now - relativedelta(months=months)).date()
    current_year = now.year
    result = []
    for year in range(cutoff.year, current_year):
        for first_month, last_month, last_day in ((1, 6, 30), (7, 12, 31)):
            first = datetime(year, first_month, 1, tzinfo=UTC)
            last = datetime(year, last_month, last_day, 23, 59, 59, tzinfo=UTC)
            first = max(first, datetime(cutoff.year, cutoff.month, cutoff.day, tzinfo=UTC))
            if first <= last:
                result.append((first, last))
    # Interleave years rather than consuming all halves of the oldest year.
    return sorted(result, key=lambda x: (x[0].month >= 7, x[0].year))


def backfill_queue(config: dict, now: datetime, done: dict,
                   provider: str) -> list[tuple[str, str, datetime, datetime]]:
    if provider == "OpenAlex":
        topics = config.get("archive_openalex_queries", [])
    elif provider == "Crossref":
        topics = config.get("archive_crossref_queries", [])
    else:
        raise ValueError(provider)
    windows = historical_windows(now, int(config.get("history_months", 60)))
    tasks = []
    # Every topic reaches every old year; alternate providers independently.
    for q in topics:
        for start, end in windows:
            ident = f"{provider}|{q}|{start:%Y-%m-%d}|{end:%Y-%m-%d}"
            if ident not in done:
                tasks.append((ident, q, start, end))
    return tasks


def load_state() -> dict:
    if not STATE.exists():
        return {"completed": {}}
    try:
        raw = json.loads(STATE.read_text(encoding="utf-8"))
        if isinstance(raw, dict) and isinstance(raw.get("completed"), dict):
            return raw
    except (OSError, ValueError):
        pass
    print("[WARN] backfill state invalid; restarting queries safely", file=sys.stderr)
    return {"completed": {}}


def save_state(state: dict) -> None:
    STATE.parent.mkdir(parents=True, exist_ok=True)
    tmp = STATE.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(STATE)


def apply_batches(history: dict[str, dict], incoming: list[dict], config: dict,
                  start: datetime, now: datetime) -> set[str]:
    added = set()
    for raw in incoming:
        if not radar.date_in_window(raw.get("published"), start, now):
            continue
        previous = history.get(raw["id"])
        if previous:
            raw["first_seen"] = previous.get("first_seen", raw["first_seen"])
        item = radar.rule_enrich(raw, config)
        if item is None:
            continue
        if raw["id"] not in history:
            added.add(raw["id"])
        history[raw["id"]] = item
    return added


def report_text(items: list[dict], state: dict, total_jobs: int,
                this_run: list[str], errors: list[str]) -> str:
    years = Counter(str(x.get("published", ""))[:4] for x in items)
    lines = [
        "# 近五年历史补录进度", "",
        "此处显示实际成功完成的“数据源 × 查询词 × 半年度”任务。",
        "该进度不代表检索到了该年度全部论文，也不代表各年份应有相同数量。", "",
        f"最近运行：{radar.utc_now().isoformat()}",
        f"已完成查询：**{len(state.get('completed', {}))} / {total_jobs}**；"
        f"本次成功：**{len(this_run)}**；本次失败：**{len(errors)}**。", "",
        "## 已收录资源年份统计", ""
    ]
    for year in sorted(years):
        lines.append(f"- {year}: {years[year]} 条")
    lines.extend(["", "## 本次已完成查询（最多显示 30 条）", ""])
    lines += [f"- {x}" for x in this_run[-30:]] or ["- 本轮没有新增完成任务"]
    if errors:
        lines.extend(["", "## 本次未完成查询", ""])
        lines += [f"- {x}" for x in errors[-20:]]
    return "\n".join(lines) + "\n"


def run_backfill(config: dict, max_openalex: int = 24, max_crossref: int = 8,
                 max_seconds: int = 520) -> dict:
    state = load_state()
    done = state["completed"]
    now = radar.utc_now()
    cutoff = radar.months_ago(int(config.get("history_months", 60)))
    queue_oa = backfill_queue(config, now, done, "OpenAlex")
    queue_cr = backfill_queue(config, now, done, "Crossref")
    # Explicit year/task coverage is available in JSON even if API access fails.
    total_jobs = len(queue_oa) + len(queue_cr) + len(done)
    history = radar.load_history()
    before = len(history)
    recent_added: set[str] = set()
    finished = []
    errors = []
    started = time.monotonic()
    exhausted = set()
    for provider, queue, budget in (
        ("OpenAlex", queue_oa, max_openalex),
        ("Crossref", queue_cr, max_crossref),
    ):
        for ident, query, start, end in queue[:max(0, int(budget))]:
            if time.monotonic() - started >= max_seconds:
                print("[INFO] reached historical recovery time budget")
                break
            if provider in exhausted:
                break
            try:
                if provider == "OpenAlex":
                    batch = radar.fetch_openalex(
                        query, start, end, int(config.get("openalex_limit", 70))
                    )
                else:
                    batch = radar.fetch_crossref(
                        query, start, end, int(config.get("crossref_limit", 30))
                    )
                new = apply_batches(history, batch, config, cutoff, now)
                recent_added.update(new)
                # Even an empty result is a successfully queried window.
                done[ident] = now.isoformat()
                finished.append(ident)
                print(f"[BACKFILL] {ident}: {len(batch)} fetched, {len(new)} newly accepted")
                save_state(state)
            except Exception as ex:
                message = f"{ident}: {type(ex).__name__} {str(ex)[:180]}"
                errors.append(message)
                print("[WARN] historical lookup failed:", message, file=sys.stderr)
                if "429" in str(ex):
                    exhausted.add(provider)  # respect server rate limits
            if provider == "OpenAlex":
                time.sleep(1.0)
            else:
                time.sleep(5.0)
    kept = radar.sort_items(radar.deduplicate_items(list(history.values())))
    kept = [i for i in kept if radar.date_in_window(i.get("published"), cutoff, now)]
    kept = kept[:max(1, int(config.get("max_history_items", 20000)))]
    radar.DB.write_text(json.dumps(kept, ensure_ascii=False, indent=2), encoding="utf-8")
    REPORT.write_text(report_text(kept, state, total_jobs, finished, errors), encoding="utf-8")
    # Re-render immediately so the release contains the recovered old items,
    # rather than waiting for the next daily task.
    radar.DOCS.joinpath("index.html").write_text(
        radar.render_html(kept, errors, config), encoding="utf-8"
    )
    digest = radar.render_digest(kept, recent_added, errors)
    digest += ("\n\n## 五年历史补录进度\n\n"
               f"已完成 {len(done)} / {total_jobs} 项年度/主题定向查询，"
               f"详见 [backfill_report.md](backfill_report.md)。\n")
    radar.DOCS.joinpath("weekly.md").write_text(digest, encoding="utf-8")
    print(f"Historical backfill finished: {before} -> {len(kept)} items, "
          f"{len(done)}/{total_jobs} query-windows completed, "
          f"{len(errors)} failed; progress saved in {STATE}")
    return {"before": before, "after": len(kept), "completed": len(done),
            "total": total_jobs, "errors": errors, "new_ids": len(recent_added)}


def main() -> None:
    parser = argparse.ArgumentParser(description="Resume bounded 5-year research backfill")
    parser.add_argument("--openalex-budget", type=int, default=24)
    parser.add_argument("--crossref-budget", type=int, default=8)
    parser.add_argument("--max-seconds", type=int, default=520)
    args = parser.parse_args()
    config = json.loads(radar.CONFIG.read_text(encoding="utf-8"))
    run_backfill(config, max_openalex=args.openalex_budget,
                 max_crossref=args.crossref_budget, max_seconds=args.max_seconds)


if __name__ == "__main__":
    main()
