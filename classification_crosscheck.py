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
    # A prior cross-check may itself have set needs_review=True. Recompute
    # that same conflict rather than silently erasing it on the second pass.
    if item.get("rule_confidence")!="high" or (item.get("needs_review") and not item.get("crosscheck_pending")):
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
    # Conservative cross-domain warning patterns: a model acronym or platform
    # alone is not sufficient; explicit task output must be present in the title.
    if category==BRAIN and has(r"(?:vla|vision.language.action)") and has(
        r"action.policy|manipulation.policy|policy.adaptation|action.generation|robot.manipulation|motion.generation") and not has(
        r"tool.calling|skill.orchestration|task.reasoning|long.horizon.task.planning"):
        flag("vla_action_vs_agent",CONTROL,"题名以动作策略或机器人操作为目标，VLA模型名称不能直接证明高层推理贡献")
    if category==CONTROL and has(r"mechanical.design|mechanism.design|semi.modular|independently.actuated.leg.joints|robot.structural.design") and not has(
        r"control.algorithm|gait.policy|reinforcement.learning.control"):
        flag("hardware_vs_motion",HARDWARE,"主要研究对象是机械结构或机器人实体平台设计，非单纯运动控制")
    if category==SOFTWARE and has(r"using.ros|based.on.ros|with.ros") and has(
        r"object.detection|visual.recognition|navigation.algorithm|path.planning.algorithm") and not has(
        r"middleware|framework|software.architecture|benchmark|dataset"):
        flag("tool_vs_deliverable",NAV,"ROS只是算法运行环境，主要成果可能是感知或导航方法")
    if category==CONTROL and has(r"token.compression|geometric.inductive.bias|human.video.guided.adaptation") and has(r"vla|vision.language.action"):
        flag("foundation_model_vs_policy",BRAIN,"主要研究VLA模型架构、表示或推理效率，而非直接优化动作控制器")
    if category==NAV and has(r"simulation.worlds|gazebo.worlds|simulation.scenarios"):
        flag("simulation_deliverable_vs_navigation",SOFTWARE,"主要交付仿真环境资源，导航是其测试用途")
    if category==SOFTWARE and has(r"pure.pursuit.algorithm|lidar.sensor.for.mobile.robot.delivery"):
        flag("ros_tool_vs_navigation",NAV,"ROS只是实现平台，主要贡献为导航或激光感知")
    return flags[:2]

def apply_crosschecks(items):
    """Recompute conflict state on every refresh; do not override manual or model labels."""
    for item in items:
        # Pending model decisions must not be reset by rule crosschecks.
        if item.get("model_reviewed_uncertain"):
            item["crosscheck_conflicts"]=[]
            item["crosscheck_pending"]=False
            continue
        old_flags=list(item.get("crosscheck_conflicts") or [])
        was_pending=bool(item.get("crosscheck_pending"))
        conflicts=crosscheck_high_confidence(item)
        if was_pending and not conflicts:
            # Keep the unresolved finding even if updated rules stop matching.
            item["crosscheck_conflicts"]=old_flags
            item["crosscheck_pending"]=True
            item["needs_review"]=True
            item["classification_confidence"]="规则分类（交叉检查待复核）"
            continue
        item["crosscheck_conflicts"]=conflicts
        if conflicts:
            item["needs_review"]=True
            item["crosscheck_pending"]=True
            item["classification_confidence"]="规则分类（交叉检查待复核）"
        else:
            item["crosscheck_pending"]=False
            if item.get("classification_confidence")=="规则分类（交叉检查待复核）":
                item["classification_confidence"]="高"
                item["needs_review"]=False
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
