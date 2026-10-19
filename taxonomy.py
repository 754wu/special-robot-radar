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
    # Reject unrelated industrial equipment and social-psychology studies that
    # contain incidental robot/inspection/emergency words in abstracts.
    if REJECTION_TITLE.search(title):
        return True, "非机器人核心技术或社会心理研究"
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


# Intent-focused phrases: mechanism/exploration/system alone do not imply a
# mechanical component, environmental exploration, or a software contribution.
PHYSICAL_DESIGN = (
    r"\b(?:mechanical|mechanical.design|mechanical.structure|structural.design|"
    r"structural.analysis|structure.design|chassis.design|chassis.structure|"
    r"kinematic.design|dimensional.synthesis|linkage|parallel.mechanism|"
    r"metamorphic.mechanism|spatial.mechanism|leg.mechanism|"
    r"passive.mechanism|compliant.mechanism|gearbox|drivetrain|"
    r"reducer|transmission.mechanism|motor.design|servo.motor|"
    r"joint.actuator|actuator.design|actuation.platform|actuator.system|"
    r"electric.actuator|piezoelectric|ultrasonic.actuating|"
    r"continuum.robot.actuation|tendon.driven|robotic.spine|"
    r"continuum.spine|adaptive.foot|foot.mechanism|"
    r"robot.morphology|cable.management|"
    r"foot.leg.trunk.integrated.structure|"
    r"reconfigurable.2r.joints|2r.joints|"
    r"robot.fabrication|3d.printed.drivetrain|"
    r"sensor.hardware|sensor.design|visuo.tactile.sensor|"
    r"tactile.sensor|flameproof|explosion.proof|intrinsically.safe|"
    r"pressurized.enclosure|purge.ventilation)\b|"
    r"机械设计|结构设计|机械机构|连杆机构|电机设计|减速器|"
    r"隔爆|防爆腔体|本安电路|关节执行器"
)
REAL_PHYSICAL_NOUN = (
    r"\b(?:mechanical|chassis|linkage|gearbox|drivetrain|"
    r"actuator|actuation|transmission|motor|"
    r"spine|foot.mechanism|adaptive.foot|"
    r"morphology|reconfigurable.joint|robot.structure|"
    r"robotic.hardware|robot.body|sensor.hardware|"
    r"piezoelectric|haptic.device|cable.management|"
    r"parallel.mechanism|passive.mechanism|metamorphic.mechanism)\b"
)
REAL_HARDWARE_EVIDENCE = (
    r"\b(?:mechanical.design|mechanical.structure|chassis.design|"
    r"leg.mechanism|linkage|robot.fabrication|"
    r"gearbox|gear.reducer|joint.actuator|"
    r"hardware.platform|actuation.platform|"
    r"actuator.system|structural.design|"
    r"tendon.driven|printed.circuit.board|mechanical.transmission|"
    r"modular.actuation|physical.prototype|3d.printing)\b"
)
ABSTRACT_MECHANISMS = (
    r"\b(?:exploration|switching|fusion|safety|reflex|"
    r"attention|reinforcement.learning|reward|policy|"
    r"algorithm|multi.scale.structured.exploration|"
    r"decision|control|task.level|stochastic|learning|"
    r"navigation|information|behavioral)\s+mechanisms?\b"
)
PHYSICAL_HARDWARE_DIRECT = (
    r"\b(?:flameproof|explosion.proof.(?:cavity|housing|enclosure|"
    r"motor|electric.actuator|equipment)|"
    r"positive.pressure.explosion.proof|"
    r"pressurized.enclosure|intrinsically.safe|"
    r"mechanical.design|structural.design|"
    r"chassis.design|mechanism.design|"
    r"kinematic.design|dimensional.synthesis|"
    r"3d.printed.drivetrain|"
    r"gearbox|gear.reducer|joint.actuator|"
    r"actuation.platform|continuum.robot.actuation|"
    r"visuo.tactile.sensor|tactile.sensor)\b|"
    r"隔爆外壳|防爆电机|关节机构设计|机械结构设计"
)
SOFTWARE_DELIVERABLE = (
    r"\b(?:benchmark(?:ing)?|dataset|data.set|"
    r"simulation.framework|simulation.platform|"
    r"software.platform|digital.twin.framework|"
    r"robot.software|ros.2.qos|qos.policies|"
    r"software.architecture|middleware|simulator|"
    r"virtual.robotic.laboratory|"
    r"robot.operating.system|robotic.software)\b|数据集|"
    r"仿真平台|通信中间件"
)
HIGH_LEVEL_AGENT = (
    r"\b(?:agentic.robot|agentic|embodied.agent|"
    r"agent(?:s)?\.for.embodied|self.evolving.agents|"
    r"quadruped.agent|robot.agent|robotic.agent|"
    r"robot.brain|agent.harness|"
    r"tool.calling|tool.use|skill.calling|skill.library|"
    r"behavior.tree.agents?|"
    r"llm.driven|llm.powered|multi.llm|"
    r"interacting.trusted.llms|"
    r"world.model.planning|"
    r"long.horizon.world.model.planning|"
    r"vision.language.action|"
    r"vision.language.models?.for.robot|"
    r"robot.foundation.model|"
    r"task.reasoning|task.planning)\b|"
    r"具身智能体|技能调用|机器人智能体|工具调用|高层任务规划"
)
AGENT_SKILL_LANGUAGE = (
    r"\b(?:multimodal.commands|multimodal.observations|"
    r"language.instructions|llms|"
    r"reasoning.and.planning|task.planning|"
    r"self.reflection|skills.and.tools|"
    r"code.execution|executable.skills|"
    r"world.model.planning|tool.using|agentic.task)\b"
)
ENVIRONMENT_TASK = (
    r"\b(?:slam|simultaneous.localization|odometry|"
    r"localization|localising|localizing|"
    r"autonomous.navigation|robot.navigation|"
    r"mobile.robot.navigation|visual.navigation|"
    r"navigation|mapless.navigation|path.planning|"
    r"route.planning|obstacle.avoidance|"
    r"frontier.exploration|autonomous.exploration|"
    r"spatial.exploration|subterranean.exploration|"
    r"unknown.environment.exploration|"
    r"mapping|occupancy.map|cost.map|"
    r"viewpoint.optimization|viewpoint.sampling|"
    r"visual.odometry|"
    r"pedestrian.tracking|target.tracking|"
    r"object.detection|line.segment.detection|"
    r"terrain.classification|crack.segmentation|"
    r"vision.based.guidance|fire.detection|"
    r"lidar.inertial|scene.reconstruction|"
    r"defect.localization|sensor.fusion|"
    r"object.tracking|point.cloud.registration|"
    r"visual.perception|image.segmentation|"
    r"visual.anomaly.detection|contact.state.detection|"
    r"infrared.sensor.fusion|"
    r"rapidly.exploring.random.tree|rrt)\b|"
    r"自主导航|定位建图|路径规划|里程计|环境感知|目标跟踪|视觉检测"
)
CONTROL_DELIVERABLE = (
    r"\b(?:reinforcement.learning|robot.learning|"
    r"imitation.learning|"
    r"locomotion|locomotor|"
    r"gait|whole.body.control|"
    r"motion.control|balance.control|"
    r"impedance.control|robot.control|"
    r"optimal.control|"
    r"predictive.control|mpc|nmpc|"
    r"torque.control|"
    r"quadruped.skills|robot.dog.new.tricks|"
    r"actuation.control|"
    r"footstep.planning|footsteps|foothold|"
    r"trajectory.tracking|"
    r"force.modulated|"
    r"contact.rich.manipulation|"
    r"dexterous.manipulation|"
    r"robot.manipulation|policy.learning|"
    r"model.based.reinforcement.learning|"
    r"body.oscillations|"
    r"motion.skill.learning|"
    r"center.of.mass.motion|"
    r"body.motion|"
    r"control.strategy|"
    r"cpg|qp.optimization.control|"
    r"gait.transition|"
    r"robotic.manipulation|"
    r"walking|body.dynamics)\b|"
    r"运动控制|步态控制|强化学习|力矩控制|全身控制|落脚点规划"
)
CONTROL_OBJECTIVE = (
    r"\b(?:locomotion|gait|body.oscillations|"
    r"quadruped.skills|motor.skill|"
    r"motion.control|whole.body.control|"
    r"torque.control|impedance.control|"
    r"manipulation|"
    r"footsteps|footstep.planning|"
    r"model.predictive.control|"
    r"trajectory.tracking|walking|"
    r"center.of.mass|body.motion|"
    r"reflex|qp.optimization.control|"
    r"robot.control|locomotor)\b"
)
SYSTEM_DELIVERABLE = (
    r"\b(?:robotic.platform|"
    r"firefighting.robot.system|inspection.robot.system|"
    r"field.demonstration|"
    r"real.world.deployment|"
    r"robotic.prototype|integrated.inspection.robot|"
    r"robot.prototype|"
    r"industrial.robot.application|"
    r"field.validation|"
    r"integrated.rescue.robot)\b"
)
# Research *deliverables* take precedence over incidental terminology. In
# particular, Mechanical Systems as an ML application domain is not a
# mechanical design contribution; describing a robot in a ROS2 simulator is
# not equivalent to designing a new physical mechanism.
SOFTWARE_SIMULATION_CONTRIBUTION = (
    r"\b(?:simulation|simulator|simulation.framework|"
    r"modeling|modelling|real2sim|digital.twin)\b"
)
SOFTWARE_ROBOTICS_FRAMEWORK = (
    r"\b(?:ros.2|ros2|gazebo|mujoco|isaac.sim|"
    r"robot.operating.system|simulation.framework|"
    r"simulation.platform|robot.simulator)\b"
)
ML_INSPECTION_STUDY = (
    r"\b(?:machine.learning|deep.learning|learning.techniques|"
    r"artificial.intelligence|ai.based)\b"
)
ML_APPLICATION_EVIDENCE = (
    r"\b(?:robotic.inspection|autonomous.inspection|"
    r"condition.monitoring|fault.diagnosis|machine.vision|"
    r"defect.detection|visual.inspection|"
    r"inspection.of.mechanical.systems|inspection)\b"
)
PHYSICAL_DELIVERABLE_TITLE = (
    r"\b(?:mechanical.design|mechanism.design|structural.design|"
    r"chassis.design|kinematic.design|linkage.design|"
    r"gearbox.design|actuator.design|joint.actuator|"
    r"motor.design|drivetrain.design|"
    r"flameproof|explosion.proof|"
    r"hardware.design|physical.prototype|"
    r"mechanical.transmission)\b"
)
CONTROL_SYSTEM_CONTRIBUTION = (
    r"\b(?:intelligent.control.system|adaptive.control.system|"
    r"novel.controller|fuzzy.(?:adaptive.)?pid|"
    r"optimized.pid|pid.control|robot.control.strategy|"
    r"motion.control.system)\b"
)
ROBOT_DEPLOYMENT_CONTEXT = (
    r"\b(?:warehouse.management|logistics.management|"
    r"warehouse.operations|industrial.deployment|"
    r"robot.integration|existing.robot.platform)\b"
)


def hardware_boundary_decision(title: str, description: str = "") -> TopicDecision | None:
    """Recognize competing contributions BEFORE broad hardware heuristics.

    Only clear title-level evidence is used for an automatic re-route. Mixed
    hardware/control work remains marked for review rather than deleted.
    """
    t = str(title or "").lower()
    d = str(description or "").lower()

    # The research output is a ROS2/Gazebo/Real2Sim *simulation*, even when
    # a CAD mechanical design must first be imported into that simulator.
    if has(t, SOFTWARE_SIMULATION_CONTRIBUTION) and has(
        t, SOFTWARE_ROBOTICS_FRAMEWORK
    ) and not has(t, r"\b(?:structural.design|mechanical.design|"
                      r"mechanism.design|actuator.design|"
                      r"gearbox.design)\b"):
        return TopicDecision(
            SOFTWARE, (HARDWARE,), False,
            "研究交付成果为 ROS2 等仿真模型/平台，并非新硬件设计", "高"
        )

    # This is an algorithms-for-inspection survey/method, not innovation in
    # the inspected mechanical equipment itself.
    if (has(t, ML_INSPECTION_STUDY) and has(t, ML_APPLICATION_EVIDENCE)
        and not has(t, PHYSICAL_DELIVERABLE_TITLE)):
        return TopicDecision(
            NAV, (APPLICATION,), True,
            "主要研究机器学习在机器人巡检/感知中的应用，非机械硬件创新", "待复核"
        )

    # Ambiguous 'Design of a Robot Based on a Novel Controller' titles:
    # the algorithm may be the primary result even if the robot was built.
    if (has(t, CONTROL_SYSTEM_CONTRIBUTION)
        and has(t, r"\b(?:quadruped|legged|robot)\b")
        and has(t, r"\b(?:design|development|implementation|based.on)\b")
        and not has(t, PHYSICAL_DELIVERABLE_TITLE)
        and has(d, r"\b(?:controller|pid|trajectory|tracking|"
                       r"control.algorithm|fuzzy.control)\b")):
        return TopicDecision(
            CONTROL, (HARDWARE,), True,
            "论文强调控制器和轨迹算法；机械结构作为验证平台，需复核主贡献", "待复核"
        )

    # A commercial mobile robot being integrated into a warehouse platform
    # is an application/system study, not a novel chassis or actuator.
    if (has(t, ROBOT_DEPLOYMENT_CONTEXT)
        and has(t, r"\b(?:robot|mobile.robot|robotic.platform)\b")
        and not has(t, PHYSICAL_DELIVERABLE_TITLE)
        and not has(d, r"\b(?:novel.mechanical.design|new.chassis|"
                       r"new.linkage|new.actuator|novel.transmission)\b")):
        return TopicDecision(
            APPLICATION, (SOFTWARE,), True,
            "现有机器人平台的场景集成应用，未发现硬件设计创新", "待复核"
        )
    return None


REJECTION_TITLE = re.compile(
    r"\b(?:"
    r"electric.drive.automatic.control.system.for.mine.belt.conveyors|"
    r"automatic.control.system.for.mine.belt.conveyors|"
    r"robot.discussions|"
    r"trust.in.robot.discussions|"
    r"exposure.to.changing.opinions.or.reaffirmation.opinions"
    r")\b", re.I
)


def classify_contribution(title: str, description: str = "", source: str = "") -> TopicDecision:
    """Identify primary technical output, then check evidence consistency.

    High-confidence decisions require title evidence aligned to the output.
    Ambiguous records remain available with a 'needs_review' flag.
    """
    t = re.sub(r"\s+", " ", str(title or "")).lower()
    d = re.sub(r"\s+", " ", str(description or "")).lower()

    def result(category, reason, related=(), review=False):
        rel = tuple(dict.fromkeys(x for x in related if x != category))
        return validate_contribution(
            TopicDecision(category, rel[:2], review, reason,
                          "待复核" if review else "高"), t, d
        )

    # Dedicated evidence-based embodied classifier; avoid counting every use of
    # "agent" or "VLM" as high-level embodied reasoning.
    from embodied_topics import embodied_decision
    embodied = embodied_decision(t, d)
    if embodied is not None:
        return result(embodied.category, embodied.reason, embodied.related,
                      review=embodied.review)

    # Resolve ambiguous mechanical/ML/simulation/platform headlines before
    # the physical-design keyword stage. Do not mutate cross-domain evidence.
    boundary = hardware_boundary_decision(t, d)
    if boundary is not None:
        return result(boundary.category, boundary.reason, boundary.related,
                      review=boundary.review)

    # Precise semantic constructions evidenced by prior corpus audits.
    # These describe research outputs rather than matching "mechanism" alone.
    if has(t, r"\b(?:explosion.proof.electric.actuators?|"
              r"limited.rotation.explosion.proof.electric.actuators?)\b"):
        return result(HARDWARE, "防爆执行器及其结构或检测技术")
    if has(t, r"\b(?:metamorphic.mechanism|reconfigurable.2r.joints|"
              r"haptic.devices?.based.on.reconfigurable)\b"):
        return result(HARDWARE, "研究可重构物理机构")
    if has(t, r"\b(?:task.level.fusion.autonomous.switching|"
              r"guide.robot.for.the.visually.impaired)\b"):
        return result(NAV, "面向定位/导航的融合与引导任务", review=True)
    if has(t, r"\binteracting.{0,20}trusted.llms\b"):
        return result(BRAIN, "多个 LLM 交互实现机器人任务/行为")
    if has(t, r"\bslams?.for.quadruped.robot\b") and has(
        t, r"\b(?:agentic.simulation|evaluation|benchmark)\b"):
        return result(SOFTWARE, "四足 SLAM 仿真评估系统")
    if has(t, r"\b(?:mode.reactive.template.based.control)\b"):
        return result(CONTROL, "腿式机器人动力学控制")

    hw_core = has(t, PHYSICAL_DESIGN)
    hw_explicit = has(t, PHYSICAL_HARDWARE_DIRECT)
    hw_from_desc = has(d, REAL_HARDWARE_EVIDENCE)
    material = has(t, REAL_PHYSICAL_NOUN)
    vague_mechanism = has(t, ABSTRACT_MECHANISMS) or has(
        t, r"\b(?:safety.mechanism|biological.reflex.mechanism|"
        r"structured.terrains?|structural.terrains?)\b")
    has_physical_design = (hw_explicit or
        (hw_core and material and has(t, HARDWARE_DESIGN) and not vague_mechanism) or
        (has(t, r"\b(?:design|fabrication|development|implementation)\b")
         and has(t, r"\b(?:quadruped|robot|legged|biped|hexapod)\b")
         and hw_from_desc)
    )

    # Hardware protection devices and physical mechanisms take precedence,
    # but word "mechanism" alone NEVER counts as mechanical engineering.
    if has_physical_design:
        return result(HARDWARE, "论文核心为机械结构、电机、执行器或防爆硬件的设计",
                      (CONTROL,) if has(t, CONTROL_OBJECTIVE) else ())

    software_deliverable = has(t, SOFTWARE_DELIVERABLE)
    nav_title = has(t, ENVIRONMENT_TASK)
    ctrl_title = has(t, CONTROL_DELIVERABLE)
    ctrl_objective = has(t, CONTROL_OBJECTIVE)
    agent_title = has(t, HIGH_LEVEL_AGENT)
    agent_abstract = has(d, AGENT_SKILL_LANGUAGE)

    # Dataset / benchmark / ROS middleware / simulation deliverable is a
    # software product even if domain = SLAM or locomotion.
    if software_deliverable and has(t, r"\b(?:dataset|benchmark|"
       r"simulation.framework|simulation.platform|"
       r"software.architecture|ros.2.qos|"
       r"middleware|digital.twin.framework)\b|数据集|仿真平台"):
        return result(SOFTWARE, "主要交付数据集、基准、仿真平台或软件架构",
                      (NAV,) if nav_title else (CONTROL,) if ctrl_title else ())

    # Agents must involve an agent architecture/reasoning/planning contribution,
    # not merely mention 'agentic simulation' of SLAM.
    is_slam_benchmark = has(t, r"\b(?:slams?.for|slam|mapping.capability)\b") and (
        has(t, r"\b(?:evaluation|simulation|benchmark|mapping)\b"))
    agent_architecture = has(t, r"\b(?:agentic.robot|embodied.agent|"
        r"self.evolving.agents|quadruped.agent|robot.agent|robotic.agent|"
        r"robot.brain|agent.harness|behavior.tree.agents|"
        r"llm|world.model.planning|multi.llm|"
        r"tool.calling|skill.calling|task.planning|"
        r"agentic.skill|quadrupedgpt)\b|机器人智能体|技能调用")
    if agent_title and (agent_architecture or agent_abstract) and not is_slam_benchmark:
        return result(BRAIN, "研究任务推理、Agent、工具技能调用或世界模型高层规划",
                      (NAV,) if nav_title else (CONTROL,) if ctrl_title else ())

    # Robot motion and RL action-space exploration should not be filed as
    # spatial frontier exploration. An RL-based NAVIGATION paper, however,
    # remains NAV because the objective is route finding.
    environmental_nav = nav_title
    if has(t, r"\b(?:motion.mapping|com.motion.mapping|"
             r"motion.response|center.of.mass.motion)\b") and not has(
             t, r"\b(?:slam|navigation|path.planning|odometry)\b"):
        environmental_nav = False
    if has(t, r"\b(?:active.exploration|structured.exploration|"
             r"exploration.mechanism|exploration.in.bayesian)\b") and not has(
             t, r"\b(?:navigation|map|frontier|environment|spatial|route)\b"):
        environmental_nav = False
    if has(t, r"\b(?:body.oscillations|nonlinear.body|"
             r"gait|locomotion|footstep.planning)\b") and not has(
             t, r"\b(?:navigation|slam|mapping|path.planning)\b"):
        environmental_nav = False

    if environmental_nav and not ctrl_objective:
        return result(NAV, "核心任务为环境感知、定位、建图或导航",
                      (CONTROL,) if ctrl_title else (BRAIN,) if agent_title else ())
    if ctrl_objective:
        return result(CONTROL, "核心任务为运动、步态、控制或机器人操作",
                      (NAV,) if environmental_nav else (),
                      review=bool(environmental_nav and has(t, r"\b(?:navigation|path.planning)\b")))
    if environmental_nav:
        return result(NAV, "核心任务为环境感知、定位、建图或导航",
                      (CONTROL,) if ctrl_title else ())
    if ctrl_title:
        return result(CONTROL, "题名显示机器人控制或策略学习研究")

    # LLM-led robotics work without a precise title goal remains reviewable,
    # not hidden under a generic software label.
    if agent_title:
        return result(BRAIN, "涉及具身智能或语言模型决策，需核实主贡献", review=True)

    if software_deliverable or has(t, r"\b(?:ros.?2|gazebo|mujoco|"
       r"software.implementation|middleware|digital.twin|"
       r"simulator|simulation|"
       r"robotic.software|robotics.platform|qos)\b"):
        return result(SOFTWARE, "研究机器人软件、仿真或平台系统",
                      review=not software_deliverable)

    # Distinguish an integrated special-robot product from an algorithm merely
    # demonstrated on an inspection or firefighting robot.
    is_special_robot = has(t, APPLICATION_TASK)
    if is_special_robot and has(t, SYSTEM_DELIVERABLE):
        return result(APPLICATION, "特种机器人整机、现场部署或集成系统")
    if is_special_robot and has(t, APPLICATION_SYSTEM) and not has(
        t, r"\b(?:algorithm|strategy|planning|detection|tracking|control.method)\b"):
        return result(APPLICATION, "特种机器人应用系统，贡献边界待复核",
                      review=True)

    # Secondary title clues (always flagged for review).
    if has(t, r"\b(?:actuation|actuator|haptic.device|mechanical|"
       r"structure|mechanism.design|sensor.design)\b"):
        return result(HARDWARE, "硬件证据不足，需复核是否为物理设计", review=True)
    if has(t, r"\b(?:world.model|foundation.model|vla|vlm|"
       r"language.model|robot.agent|embodied)\b"):
        return result(BRAIN, "基于题名识别具身模型，需复核主贡献",
                      review=True)
    if has(t, r"\b(?:manipulation|robot.learning|"
       r"learning.from.demonstration|"
       r"robot.policies|motion|"
       r"footsteps|trajectory)\b"):
        return result(CONTROL, "根据题名初步判断运动或策略研究", review=True)
    if has(t, r"\b(?:image|lidar|vision|camera|depth|"
       r"infrared|sensor|perception|scene|"
       r"robot.inspection)\b"):
        return result(NAV, "根据题名初步判断感知相关研究", review=True)

    # Abstract fallback only if title has no decisive topic. If multiple
    # strong subjects occur in the abstract, confidence stays low.
    if has(d, AGENT_SKILL_LANGUAGE) and has(d, r"\b(?:robot|agent|skill)\b"):
        return result(BRAIN, "摘要显示 Agent/技能推理，需要人工复核", review=True)
    if has(d, ENVIRONMENT_TASK):
        return result(NAV, "仅摘要含感知导航相关证据", review=True)
    if has(d, CONTROL_DELIVERABLE):
        return result(CONTROL, "仅摘要含运动控制相关证据", review=True)
    if has(d, REAL_HARDWARE_EVIDENCE) and has(t, r"\b(?:robot|quadruped|legged)\b"):
        return result(HARDWARE, "仅摘要含硬件设计相关证据", review=True)
    if has(d, SOFTWARE_DELIVERABLE):
        return result(SOFTWARE, "仅摘要含软件平台相关证据", review=True)

    return result(APPLICATION, "元数据不足，临时标记待复核（不视为应用领域确认）", review=True)


def validate_contribution(decision: TopicDecision, title: str,
                          description: str = "") -> TopicDecision:
    """Final evidence validation: demote or reroute indefensible decisions.

    High-confidence category requires task-anchored title evidence.
    If evidence is weak, mark review; do not claim a verified classification.
    """
    t = str(title or "").lower()
    d = str(description or "").lower()
    cat = decision.category
    review = decision.review
    reason = decision.reason
    related = decision.related

    # Defense in depth: no high-confidence Hardware result based solely on
    # an algorithm applied to mechanical equipment or a software simulator.
    if cat == HARDWARE:
        boundary = hardware_boundary_decision(t, d)
        if boundary is not None:
            cat, review, reason = boundary.category, boundary.review, boundary.reason
            related = boundary.related

    if cat == HARDWARE and not (
        has(t, PHYSICAL_HARDWARE_DIRECT) or
        (has(t, PHYSICAL_DESIGN) and has(t, REAL_PHYSICAL_NOUN)
         and has(t, HARDWARE_DESIGN) and not has(t, ABSTRACT_MECHANISMS)) or
        (has(t, r"\b(?:robot|quadruped|legged)\b") and
         has(t, HARDWARE_DESIGN) and has(d, REAL_HARDWARE_EVIDENCE))
    ):
        if has(t, CONTROL_DELIVERABLE):
            cat, review, reason = CONTROL, False, "一致性检查：算法机制不属于机械机构"
        elif has(t, ENVIRONMENT_TASK):
            cat, review, reason = NAV, True, "一致性检查：缺少物理硬件设计证据"
        else:
            review, reason = True, "硬件类别缺少直接设计证据"
    if cat == APPLICATION and not review:
        if not has(t, APPLICATION_TASK):
            review, reason = True, "应用系统缺少标题中的特种机器人场景依据"
        elif has(t, r"\b(?:detection|tracking|"
                       r"planning|algorithm|reinforcement.learning)\b"):
            review, reason = True, "可能以算法而不是产品集成为主要贡献"
    if cat == BRAIN and not (
        has(t, HIGH_LEVEL_AGENT) or has(t, AGENT_SKILL_LANGUAGE)):
        review, reason = True, "Agent 高层决策证据较弱"
    if cat == NAV and not (
        has(t, ENVIRONMENT_TASK) or has(t, r"\b(?:image|vision|lidar|"
                                         r"camera|sensor|depth|perception)\b")):
        review = True
        reason = "导航/感知类别缺少题名中的明确研究任务"
    if cat == CONTROL and not (
        has(t, CONTROL_DELIVERABLE) or has(t, CONTROL_OBJECTIVE) or
        has(t, r"\b(?:manipulation|motion|robot.learning)\b")):
        review, reason = True, "运动控制类别缺少题名中的控制任务证据"
    rel = tuple(k for k in related if k != cat)
    return TopicDecision(cat, rel, review, reason, "待复核" if review else "高")
