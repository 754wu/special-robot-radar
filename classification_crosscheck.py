"""Independent, conservative high-confidence classification cross-check.

Only flags conflicting *research goals*; never rewrites the primary category.
"""
from __future__ import annotations
import re
from pathlib import Path
import json
from collections import Counter

NAV="感知建图与导航"
CONTROL="小脑与运动控制"
BRAIN="大脑与具身智能"
HARDWARE="硬件与防爆"
SOFTWARE="基础软件与系统"
APPLICATION="特种应用与产品"

def crosscheck_high_confidence(item):
    if item.get("manual_category_override") or item.get("model_applied"):
        return []
    if item.get("rule_confidence")!="high" or item.get("needs_review"):
        return []
    title=str(item.get("title") or "").lower()
    desc=str(item.get("description") or "").lower()
    category=item.get("rule_category") or item.get("category")
    def has(p, src=title):
        return bool(re.search(p,src,re.I))
    flags=[]
    def flag(kind, suggested, reason):
        if category!=suggested:
            flags.append({"type":kind,"suggested_category":suggested,"reason":reason})
    # A narrow, explicitly named research deliverable wins over a method or model-name.
    if category==CONTROL and has(r"simultaneous.localization.and.mapping|\bslam.methods?\b|localization.and.mapping"):
        flag("research_goal_vs_method",NAV,"论文明确以定位建图为研究目标，运动方式可能只是辅助手段")
    if category==BRAIN and has(r"zero.shot.object.navigation|object.goal.navigation|\bvision.language.navigation\b|\bvln\b") and not has(
        r"tool.calling|skill.orchestration|task.decomposition|high.level.task.planning|multi.llm.coordination"):
        flag("model_name_vs_research_task",NAV,"研究目标是目标导航或视觉语言导航，不应仅凭Agent/LLM归入大脑")
    if category==BRAIN and has(r"gait.control|locomotion.policy|robot.action.policy|whole.body.control|torque.control") and not has(r"task.planning|skill.orchestration|tool.calling"):
        flag("model_name_vs_action_policy",CONTROL,"核心任务为动作策略或底层控制")
    if category==APPLICATION and has(r"fuzzy.pid|trajectory.tracking.control|gait.control|force.control|torque.control"):
        flag("application_vs_algorithm",CONTROL,"特种应用是实验场景，主要成果是控制方法")
    if category==APPLICATION and has(r"\bpath.planning.algorithm|\bslam.algorithm|object.detection.algorithm|visual.navigation.algorithm"):
        flag("application_vs_algorithm",NAV,"主要成果是空间规划或环境感知算法")
    if category==APPLICATION and has(r"explosion.proof.{0,65}(?:motor|battery|power.supply|valve|enclosure)") and not has(r"robot|quadruped|legged"):
        flag("application_vs_hardware",HARDWARE,"防爆电气或结构设计并非整机机器人产品")
    if category in (BRAIN,NAV,APPLICATION) and has(r"\b(?:dataset|benchmark|simulation.framework|middleware)\b") and not has(r"using.(?:a|the).(?:dataset|benchmark)"):
        flag("deliverable_vs_task",SOFTWARE,"题名显示交付数据集、基准或软件框架")
    return flags[:2]

def apply_crosschecks(items):
    """Recompute conflict state on every refresh; do not override manual or model labels."""
    for item in items:
        conflicts=crosscheck_high_confidence(item)
        item["crosscheck_conflicts"]=conflicts
        if conflicts:
            item["needs_review"]=True
            item["crosscheck_pending"]=True
            item["classification_confidence"]="规则分类（交叉检查待复核）"
        else:
            item["crosscheck_pending"]=False
    return items

def report(items, path):
    checked=[x for x in items if x.get("rule_confidence")=="high"
             and not x.get("manual_category_override") and not x.get("model_applied")]
    flagged=[x for x in checked if x.get("crosscheck_conflicts")]
    counts=Counter(x.get("rule_category") or x.get("category") for x in flagged)
    lines=["# 高置信度规则分类交叉检查","",
           "仅对当前规则高置信度且未由人工/模型确认的条目检查；疑点不等于确证错分。","",
           f"- 参与范围：{len(checked)}",
           f"- 发现冲突资源：{len(flagged)}","",
           "## 分类冲突分布"]
    for k,n in sorted(counts.items()):
        lines.append(f"- {k}: {n}")
    lines.extend(["","## 具体疑点"])
    for x in flagged:
        lines.extend([f"### {str(x.get('title',''))[:190]}",
                      f"- 地址：{x.get('url','')}",
                      f"- 规则主分类：{x.get('rule_category') or x.get('category')}",
                      f"- 模型审核状态：{'待复核' if x.get('needs_review') else '无需复核'}"])
        for y in x["crosscheck_conflicts"]:
            lines.append(f"- 可能类别：{y['suggested_category']}；冲突：{y['type']}；理由：{y['reason']}")
        lines.append("")
    Path(path).parent.mkdir(parents=True,exist_ok=True)
    Path(path).write_text("\n".join(lines)+"\n",encoding="utf-8")
    return len(flagged)

if __name__=="__main__":
    root=Path(__file__).resolve().parent
    db=root/"docs/items.json"
    if db.exists():
        data=json.loads(db.read_text(encoding="utf-8"))
        apply_crosschecks(data)
        report(data,root/"docs/classification_crosscheck.md")
