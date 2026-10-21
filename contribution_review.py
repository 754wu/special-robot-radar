"""Conservative contribution consistency and robot-relevance checks.

These checks are guards, not proof of a paper's scientific contribution.
Only high-specificity task phrases may veto an LLM label.
"""
import re

HARDWARE="硬件与防爆"
SOFTWARE="基础软件与系统"
CONTROL="小脑与运动控制"
BRAIN="大脑与具身智能"
NAV="感知建图与导航"
APPLICATION="特种应用与产品"

def contribution_evidence(title, description=""):
    title=str(title or "").lower()
    body=(title+" "+str(description or "").lower())
    def match(pattern, source=title):
        return bool(re.search(pattern,source,re.I))
    if match(r"(?:explosion.proof|flameproof).{0,50}(?:motor|battery|valve|actuator|enclosure)|(?:motor|battery|valve).{0,35}explosion.proof") and match(r"design|performance|optimization|model|current.sharing|relief|electromagnetic|structure"):
        return HARDWARE,"防爆设备物理或电气设计成果"
    # Primary deliverable boundaries, before generic keyword evidence.
    if match(r"simulation.worlds|gazebo.worlds|simulation.scenarios|navigation.dataset"):
        return SOFTWARE,"主要交付仿真场景或数据资源，而非导航算法"
    if match(r"pure.pursuit.algorithm|lidar.sensor.for.mobile.robot.delivery|slam.algorithm.using.ros"):
        return NAV,"ROS是实现平台，贡献为导航、跟踪或激光感知方法"
    if match(r"token.compression|geometric.inductive.bias|human.video.guided.adaptation") and match(r"vla|vision.language.action"):
        return BRAIN,"具身基础模型架构、表示或推理效率创新"
    if match(r"vla.models?.for.agricultural.manipulation"):
        return CONTROL,"特定机器人操作任务的动作策略适配"
    if match(r"\b(?:pid|lqr|mpc)\b.{0,30}control|gait.control|locomotion.policy|trajectory.interpolation|polynomial.interpolation.algorithm|flipper.control|force.control"):
        return CONTROL,"底层运动控制或轨迹生成"
    if match(r"\b(?:slam|odometry|localization|visual.pose.estimation|object.detection|defect.detection|path.planning|path.optimization|vision.language.navigation|zero.shot.navigation)\b"):
        if match(r"multi.llm|verifier.mediated|task.reasoning|tool.calling|skill.orchestration") and match(r"multi.robot|coordination|planning"):
            return None,"高层任务协调和导航混合，保留冲突复核"
        return NAV,"环境感知、定位或空间导航任务"
    if match(r"\b(?:simulation.framework|benchmark|dataset|middleware|software.architecture|ros.2.interface)\b"):
        return SOFTWARE,"可复用机器人软件或评测交付物"
    if match(r"(?:llm|vlm|agent).{0,30}(?:tool.calling|skill.selection|task.decomposition|high.level.task.planning)|(?:skill.orchestration|multi.llm.coordination)"):
        return BRAIN,"具身任务推理或技能编排"
    if match(r"(?:motion.policy|action.policy|imitation.learning|robot.manipulation.policy|whole.body.control|robot.locomotion)"):
        return CONTROL,"动作策略学习与运动执行"
    return None,"研究贡献缺少足够明确的独立校验证据"

def contribution_conflict(item, model_category, main_contribution=""):
    """Return a guard reason when a *clear* research task contradicts the proposed class."""
    expected, evidence=contribution_evidence(item.get("title"),item.get("description"))
    if expected and expected!=model_category:
        return "研究贡献冲突："+evidence+"；任务证据更支持"+expected
    # A proposed contribution has to be grounded in available metadata.
    if main_contribution:
        from llm_review import evidence_supported
        if not evidence_supported(item,main_contribution):
            return "模型所述主要研究贡献无法由题名摘要核验"
    return ""

def relevance_status(title, description, direct, transferable, native, robots):
    """Separate collection eligibility from classification without deleting ambiguous records."""
    text=(str(title or "")+" "+str(description or "")).lower()
    robot_link=bool(robots or re.search(r"\b(robot(?:ic)?s?|quadruped|wheel.legged|legged|humanoid|uav|ugv)\b|机器人|四足|轮足",text))
    bare_device=bool(re.search(r"explosion.proof|flameproof",title,re.I) and
                     re.search(r"battery|valve|motor|fan|power.supply|enclosure",title,re.I))
    if bare_device and not robot_link:
        return "潜在相关（需核实机器人应用）"
    if direct:
        return "直接相关"
    if transferable and robot_link:
        return "可迁移的机器人关键技术"
    return "相关性待核实"
