"""Primary-contribution taxonomy and source-quality gate.

Rules use the title as evidence of the RESEARCH QUESTION, and the abstract to
disambiguate. A platform, method or application mentioned in passing should
not become the primary category. This is a transparent metadata classifier;
ambiguous cases are flagged for manual review rather than treated as verified.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

HARDWARE = "硬件与防爆"
SOFTWARE = "基础软件与系统"
CONTROL = "小脑与运动控制"
BRAIN = "大脑与具身智能"
NAV = "感知建图与导航"
APPLICATION = "特种应用与产品"
CATEGORIES = (HARDWARE, SOFTWARE, CONTROL, BRAIN, NAV, APPLICATION)

# Phrases anchored to actual design contributions, not background components.
HARDWARE_CORE = (
    r"\b(?:mechanism|mechanical|structural|structure|chassis|drivetrain|linkage|"
    r"gearbox|gear.reducer|harmonic.drive|transmission|actuator.system|"
    r"joint.actuator|electric.actuator|tendon.driven|continuum.spine|"
    r"robotic.spine|adaptive.foot|foot.mechanism|metamorphic.mechanism|"
    r"robot.morphology|cable.management|battery.pack|pcb|circuit.board|"
    r"servo.motor|sensor.hardware|sensor.design|tactile.sensor|"
    r"flameproof|explosion.proof.cavity|explosion.proof.enclosure|"
    r"explosion.proof.equipment|explosion.proof.electric|"
    r"positive.pressure.explosion.proof|intrinsically.safe|"
    r"explosion.protection|purge.ventilation|motor.design)\b|"
    r"隔爆|防爆外壳|正压防爆|关节执行器|结构设计|机构设计|减速器|机械传动"
)
HARDWARE_DESIGN = (
    r"\b(?:design|fabricat(?:ion|e)|prototype|development|synthesis|"
    r"optimization|manufactur(?:e|ing)|experiment|analysis|"
    r"low.backlash|structural)\b|设计|研制|结构|机构"
)
HARDWARE_ROBOT = (
    r"\b(?:quadruped|hexapod|biped|legged|robot(?:ic)?s?|inspection.robot|"
    r"mechanical|servo|sensor|actuator)\b|四足|轮足|机器人"
)
HARDWARE_EXPLICIT = (
    r"\b(?:explosion.proof|flameproof|intrinsic.safety|intrinsically.safe|"
    r"pressurized.enclosure|explosion.vibration|explosion.protection)\b|"
    r"隔爆|本安|正压防爆|防爆腔体|防爆外壳"
)

# High-level policy selection, reasoning, tools, memory and task planning.
# Ordinary VLM perception, learned navigation policies and locomotion RL
# must not automatically be filed as embodied agents.
AGENT_EXPLICIT = (
    r"\b(?:agentic|embodied.agent|robot(?:ic)?.agent|self.evolv(?:ing)? agents?|"
    r"agent.harness|behavior.tree.agents?|task.planning.agent|"
    r"agent.?based.reasoning|llm.driven|llm.powered|"
    r"multi.llm.coordination|tool.calling|tool.use|skill.calling|"
    r"skill.library|skill.selection|memory.runtime|reasoning.and.planning|"
    r"high.level.reasoning|long.horizon.world.model.planning|"
    r"world.model.planning|"
    r"multimodal.language.model|large.language.model.for.robot|"
    r"robot.foundation.model|vision.language.action|vision.language.models?.for.robot)\b|"
    r"具身智能体|机器人智能体|工具调用|技能调用|任务推理|任务规划|具身大脑"
)
BRAIN_TASK_HINT = (
    r"\b(?:reasoning|task.planning|skill|tool|language.model|llm|vlm|vla|"
    r"world.model|self.reflection|memory|code.generation|"
    r"program.execut(?:ion|e)|planner|multi.agent)\b|具身|智能体|任务规划"
)
NAV_TASK = (
    r"\b(?:navigation|path.planning|route.planning|slam|mapping|"
    r"localiz(?:ation|ing)|odometry|obstacle.avoidance|"
    r"collision.avoidance|mapless.navigation|"
    r"autonomous.exploration|explor(?:ation|ing)|traversability|"
    r"topological.navigation|visual.navigation|"
    r"target.track(?:ing|er)|pedestrian.track(?:ing|er)|"
    r"object.detect(?:ion|or)|line.segment.detection|"
    r"image.enhance(?:ment)?|image.segment(?:ation)?|"
    r"defect.detect(?:ion|or)|crack.segment(?:ation)?|"
    r"sensor.fusion|point.cloud.registration|"
    r"visual.perception|perception|terrain.classification|"
    r"contact.state.detection|scene.understanding|"
    r"foot.contact.state.detection|pose.estimation|"
    r"viewpoint.(?:sampling|optimization)|"
    r"cost.map|lidar.inertial|infrared.thermal.sensor.fusion)\b|"
    r"自主导航|路径规划|感知建图|视觉跟踪|目标检测|里程计|点云|定位|图像增强"
)
CONTROL_TASK = (
    r"\b(?:locomotion|gait|whole.body.control|"
    r"model.predictive.control|torque.control|motion.control|"
    r"balance.control|impedance.control|compliance|"
    r"contact.rich.manipulation|force.modulat(?:ion|ed)|"
    r"robot.learning|policy.learning|locomotion.policy|"
    r"robotic.manipulation|dexterous.robot.learning|"
    r"dexterous.manipulation|robot.learning.from.demonstrations|"
    r"footstep.planning|foothold.control|"
    r"locomotor|trajectory.tracking|motion.tracking|"
    r"predictive.control|cent(?:er|re).of.mass.motion|"
    r"cpg|inverse.dynamics|reinforcement.learning|"
    r"joint.torque|posture.control|stable.walking)\b|"
    r"步态|运动控制|全身控制|强化学习|力矩控制|轨迹跟踪|灵巧操作"
)
CONTROL_SPECIFIC = (
    r"\b(?:locomotion|gait|whole.body.control|torque.control|"
    r"motion.control|balance.control|impedance.control|"
    r"contact.rich.manipulation|force.modulat(?:ion|ed)|"
    r"dexterous.manipulation|robot.learning.from.demonstrations|"
    r"footstep.planning|foothold|trajectory.tracking|"
    r"center.of.mass.motion|cpg)\b|步态|运动控制|力矩控制|全身控制"
)
SOFTWARE_TASK = (
    r"\b(?:ros.?2|robot.operating.system|middleware|"
    r"software.architecture|software.stack|simulation.platform|"
    r"simulator|gazebo|mujoco|isaac.sim|"
    r"digital.twin|benchmark|dataset|"
    r"communication.protocol|cybersecurity|"
    r"qos.polic(?:y|ies)|robot.software|real.time.system|"
    r"software.infrastructure|robotics.framework|"
    r"sensor.network|robot.interface)\b|"
    r"软件架构|仿真平台|机器人操作系统|中间件|数据集|数字孪生"
)
SOFTWARE_FOCUS = (
    r"\b(?:software|system.architecture|middleware|platform|"
    r"simulation|simulator|dataset|benchmark|digital.twin|"
    r"qos|communication|cybersecurity|ros.?2|framework)\b|软件|系统架构|仿真|数据集"
)
APPLICATION_TASK = (
    r"\b(?:firefight(?:ing|er)|rescue|industrial.inspection|"
    r"inspection.robot|pipeline.inspection|"
    r"tunnel.inspection|mine.inspection|"
    r"field.deployment|field.demonstration|"
    r"prototype.evaluation|industrial.application|"
    r"nuclear.inspection|safety.system|explosion.proof.legged.robot|"
    r"eod.robot|substation.inspection|emergency.response)\b|"
    r"消防机器人|巡检机器人|矿山巡检|应急救援|特种机器人|工业巡检"
)
APPLICATION_SYSTEM = (
    r"\b(?:system|platform|prototype|development|deploy(?:ment|ed)|"
    r"application|integration|field.test|"
    r"real.world|inspection.robot|rescue.robot|"
    r"firefighting.robot|robotic.intervention)\b|整机|现场应用|系统集成|机器人原型"
)

# Nontechnical posts may discuss RL etc in the description. Filter on
# *document intent*, i.e. job ad / meeting announcement, not topic words.
JOBS = re.compile(
    r"\b(?:internship|intern.position|intern(?:ship)?\s*@|"
    r"prototyping.intern|job.opening|job.posting|"
    r"we.are.hiring|now.hiring|hiring\b|career.opportunit(?:y|ies)|"
    r"recruiting|vacan(?:cy|cies)|"
    r"looking.for.an?.(?:intern|engineer|researcher)|apply.for.the.role)\b|"
    r"招聘(?:信息|岗位|启事)?|实习生招聘|岗位招聘",
    re.I,
)
EVENTS = re.compile(
    r"\b(?:hackers?.meeting|community.meeting|monthly.meeting|"
    r"meetup|join.us.for.the.meeting|"
    r"meeting.(?:oct|nov|dec|jan|feb|mar|apr|may|jun|jul|aug|sep|\d)|"
    r"webinar.registration|event.registration|"
    r"conference.registration|training.session|"
    r"call.for.speakers|save.the.date|"
    r"newsletter|ros.news.for.the.week)\b|"
    r"活动通知|会议通知|报名通知|招聘会",
    re.I,
)
SOCIAL = re.compile(
    r"\b(?:social.gathering|happy.hour|community.hangout|"
    r"looking.for.volunteers|weekly.community.call)\b", re.I
)


def has(text: str, pattern: str) -> bool:
    return re.search(pattern, text, re.I) is not None


def is_non_technical(item: dict) -> tuple[bool, str]:
    """Remove jobs/events using their headline and source context.

    Do not reject academic papers describing meetings or robot scheduling,
    or technical projects with an abstract mentioning a job/meeting in passing.
    """
    title = str(item.get("title") or "").strip()
    source = str(item.get("source") or "")
    kind = str(item.get("type") or "")
    nonpaper = kind == "社区动态" or source in ("ROS Discourse",)
    if JOBS.search(title):
        return True, "招聘或实习岗位通知"
    if nonpaper and (EVENTS.search(title) or SOCIAL.search(title)):
        return True, "会议活动或非技术公告"
    if source == "GitHub" and re.search(r"/(?:job-board|jobs|hiring|internships)$", title, re.I):
        return True, "招聘目录非技术仓库"
    return False, ""


@dataclass(frozen=True)
class TopicDecision:
    category: str
    related: tuple[str, ...] = ()
    review: bool = False
    reason: str = ""
    confidence: str = "高"


def classify_contribution(title: str, description: str = "", source: str = "") -> TopicDecision:
    """Hierarchical primary-contribution classification, with review flags.

    Priority: explicit physical design -> actual agent/reasoning architecture
    -> target task (navigation/perception vs gait/control) -> software
    -> applied integrated system -> topic-specific abstract -> review.
    """
    t = re.sub(r"\s+", " ", str(title or "")).lower()
    d = re.sub(r"\s+", " ", str(description or "")).lower()
    def decision(category: str, related=(), reason: str = "", review=False):
        related = tuple(dict.fromkeys(x for x in related if x != category))
        return TopicDecision(category, related[:2], bool(review), reason,
                             "待复核" if review else "高")

    physical_focus = has(t, HARDWARE_CORE)
    title_design = has(t, HARDWARE_DESIGN)
    explicit_ex = has(t, HARDWARE_EXPLICIT)
    robot_context = has(t + " " + d, HARDWARE_ROBOT)
    nav_focus = has(t, NAV_TASK)
    control_focus = has(t, CONTROL_TASK)
    gait_focus = has(t, CONTROL_SPECIFIC)
    agent_focus = has(t, AGENT_EXPLICIT)
    software_focus = has(t, SOFTWARE_TASK)
    application_focus = has(t, APPLICATION_TASK)

    # Robot mechanism / enclosure / actuator innovation, not a paper that
    # merely constrains actuator commands or uses a LiDAR sensor.
    if ((physical_focus and (title_design or explicit_ex or has(t, r"\b(?:gearbox|drive.?train|robotic.spine|adaptive.foot|actuator.system|mechanism)\b")))
        or (explicit_ex and has(t, r"\b(?:cavity|housing|enclosure|ventilation|equipment|actuator|motor|protection)\b"))
        or (title_design and has(t, r"\b(?:robot|quadruped|hexapod|biped|legged)\b")
            and has(d, r"\b(?:mechanical.chassis|pcb|printed.circuit.board|fabrication|linkage.mechanism|"
                       r"transmission.mechanism|robot.structure|servo.motors)\b"))
        or has(t, r"\b3d.printed.drivetrain\b")):
        related = (CONTROL,) if gait_focus else ()
        return decision(HARDWARE, related, "核心贡献为硬件、结构或防爆设计")

    # Hardware-themed surveys across structural design AND intelligence should
    # stay in Hardware but be transparently marked as cross-disciplinary.
    if physical_focus and has(t, r"\b(?:survey|review)\b") and robot_context:
        return decision(HARDWARE, (CONTROL,), "跨结构设计与控制的综述", review=True)

    # A world-model *planning* agent is different from model-based RL dynamics.
    strong_agent = (
        agent_focus and
        (has(t, r"\b(?:agent(?:s|ic)?|world.model.planning|skill|tool|llm|"
                r"large.language.model|vision.language.action|"
                r"long.horizon|task.planning|memory|self.evolv)\b")
         or has(d, r"\b(?:tool.calling|write.and.execute.programs|"
                r"reasoning|task.planning|skill.library|reflection|"
                r"memory.runtime|world.model.planning)\b"))
    )
    if strong_agent:
        related = (NAV,) if nav_focus else (CONTROL,) if control_focus else ()
        return decision(BRAIN, related, "主要研究 Agent、世界模型高层规划或语言模型决策")

    # The *objective* beats the chosen algorithm. RL navigation is navigation;
    # raw LiDAR input to a locomotion policy is still locomotion.
    if nav_focus and not gait_focus:
        related = (BRAIN,) if agent_focus else (CONTROL,) if control_focus else ()
        return decision(NAV, related, "主要任务为感知、定位、导航或路径规划")
    if gait_focus:
        related = (NAV,) if nav_focus else (HARDWARE,) if physical_focus else ()
        return decision(CONTROL, related, "主要任务为运动、步态、操作或力控制",
                        review=nav_focus)
    if nav_focus:
        return decision(NAV, (CONTROL,) if control_focus else (),
                        "主要任务为感知、定位、导航或路径规划")
    if control_focus:
        return decision(CONTROL, (), "主要研究动作策略、强化学习或控制算法")
    if software_focus:
        # Technology implemented in ROS2 is not necessarily software research:
        # navigation / locomotion have been handled above.
        related = (BRAIN,) if agent_focus else ()
        return decision(SOFTWARE, related, "主要研究软件平台、系统、仿真或数据集")

    if agent_focus:
        return decision(BRAIN, (), "疑似具身决策研究", review=True)
    if application_focus and has(t, APPLICATION_SYSTEM):
        return decision(APPLICATION, (), "主要研究特种机器人产品、系统集成或现场应用")

    # Titles are sometimes vague, especially Crossref items without abstracts.
    # Match relatively specific phrases in title first, then summary as support.
    if has(t, r"\b(?:vision.language|foundation.model|embodied.intelligence|"
              r"language.guided|multimodal.language|llm|vla)\b"):
        return decision(BRAIN, (NAV,) if has(t, NAV_TASK) else (),
                        "基于题名识别具身模型，缺少高层决策证据", review=True)
    if has(t, r"\b(?:manipulation|robot.learning|motion|mobility|"
              r"robot.polic(?:y|ies)|learning.from.demonstrations)\b"):
        return decision(CONTROL, (), "基于题名判断为机器人运动或操作技术", review=True)
    if has(t, r"\b(?:vision|camera|lidar|depth|image|sensor|"
              r"line.segment|infrared)\b"):
        return decision(NAV, (), "基于题名判断为感知技术", review=True)
    if has(t, r"\b(?:structural|mechanical|actuator|gearbox|hardware)\b") and robot_context:
        return decision(HARDWARE, (), "硬件类线索较弱，需人工确认", review=True)
    if application_focus:
        return decision(APPLICATION, (), "特种场景类研究，技术核心暂不明确", review=True)
    if has(d, AGENT_EXPLICIT):
        return decision(BRAIN, (), "仅摘要提到高层智能决策，待复核", review=True)
    if has(d, NAV_TASK):
        return decision(NAV, (), "仅摘要提示感知导航方向，待复核", review=True)
    if has(d, CONTROL_TASK):
        return decision(CONTROL, (), "仅摘要提示运动策略方向，待复核", review=True)
    if has(d, SOFTWARE_TASK):
        return decision(SOFTWARE, (), "仅摘要提示机器人软件系统方向，待复核", review=True)
    return decision(APPLICATION, (), "元数据不足以确定研究主贡献", review=True)
