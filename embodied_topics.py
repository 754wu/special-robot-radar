"""Research-contribution signals for robot brains and embodied agents.

This intentionally does not equate every occurrence of "VLM", "agent" or
"navigation" with a high-level agent. Title+abstract evidence must describe
reasoning, planning, model architecture, tool/skill invocation or coordination.
Pure navigation perception remains Navigation, locomotion RL remains Control.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

BRAIN = "大脑与具身智能"
NAV = "感知建图与导航"
CONTROL = "小脑与运动控制"
SOFTWARE = "基础软件与系统"

def hit(text: str, pattern: str) -> bool:
    return bool(re.search(pattern, text, flags=re.I))


@dataclass(frozen=True)
class BrainEvidence:
    category: str
    reason: str
    related: tuple[str, ...] = ()
    review: bool = False
    tags: tuple[str, ...] = ()


ROBOT = (
    r"\b(?:robot(?:ics|ic|s)?|quadruped|legged|humanoid|"
    r"manipulat(?:ion|or)|mobile.robot|vln|vla|"
    r"vision.language.navigation|embodied|"
    r"robotic.task|navigation)\b|机器人|具身|四足|轮足"
)
AGENT_ARCH = (
    r"\b(?:agentic|embodied.agents?|robot(?:ic)?.agents?|"
    r"onboard.robot.agents?|behavior.tree.agents?|"
    r"visual.interface.agent|self.evolving.agents?|"
    r"agent.harness|task.oriented.agent|"
    r"llm.based.conversations?|"
    r"llm.powered.(?:reasoning|planning)|"
    r"foundation.model.agents?|multi.llm.coordination|"
    r"tool.call(?:ing|s)?|tool.use|skill.call(?:ing|s)?|"
    r"skill.library|skill.selection|"
    r"reflection.and.replanning|"
    r"long.horizon.(?:task|world.model).planning|"
    r"world.model.planning)\b|"
    r"技能调用|机器人智能体|任务推理"
)
REASONING = (
    r"\b(?:reason(?:ing|er)|reflect(?:ion|ive)|"
    r"task.plann(?:ing|er)|"
    r"skill(?:s)?.(?:execution|selection|composition|calling)|"
    r"tool.calling|"
    r"failure.feedback|self.correction|"
    r"decision.making|program.execut(?:e|ion)|"
    r"high.level.(?:decision|planning)|"
    r"long.horizon.(?:planning|navigation)|"
    r"episodic.memory|task.memory|"
    r"multi.agent.coordination|"
    r"language.model.agents?|"
    r"multi.robot.collaboration|"
    r"llm.enabled.conversations?|"
    r"collaborative.reasoning)\b|"
    r"高级规划|高层推理|记忆反思|技能决策"
)
VLA = r"\b(?:vla|vision.language.action|vision.and.language.action)\b"
VLM = r"\b(?:vlm|vision.language.models?|vision.and.language.models?)\b"
VLN = r"\b(?:vln|vision.language.navigation|vision.and.language.navigation)\b"
MODEL_CONTRIBUTION = (
    r"\b(?:model|models|architecture|framework|"
    r"representation|training|fine.tuning|"
    r"inference|token.compression|"
    r"tokenization|task.context|"
    r"memory|feature.learning|"
    r"pretraining|foundation.model|"
    r"reasoner|language.encoder)\b"
)
VLA_ACTION_CONTROL = (
    r"\b(?:whole.body.control|"
    r"force.aware.whole.body|"
    r"force.control|motion.compensation|"
    r"teleoperation|"
    r"control.steering|policy.steering|"
    r"torque.control|"
    r"gait.control|locomotion.control)\b"
)
PERCEPTION_OBJECTIVE = (
    r"\b(?:traversability|terrain.estimat(?:ion|e)|"
    r"traversability.navigation|"
    r"cost.map|depth.estimation|"
    r"visual.grounding|"
    r"semantic.segmentation|"
    r"object.detect(?:ion|or)|"
    r"image.enhancement|lidar.odometry|"
    r"slam|scene.reconstruction)\b"
)
NAV_OBJECTIVE = (
    r"\b(?:navigation|traversability|slam|odometry|"
    r"path.planning|localization|mapless.navigation|"
    r"route.planning|frontier.exploration)\b"
)
CONTROL_OBJECTIVE = (
    r"\b(?:locomotion|gait|walking|"
    r"joint.control|whole.body.control|"
    r"ppo.agent|reinforcement.learning|"
    r"robot.manipulation|dexterous.control|"
    r"force.aware|trajectory.tracking)\b"
)
SOFTWARE_PRODUCT = (
    r"\b(?:dataset|benchmark|"
    r"simulation.toolkit|"
    r"real2sim.toolkit|"
    r"robot.simulator|"
    r"ros.2.middleware)\b"
)
AGENT_FALSE_FRIEND = (
    r"\b(?:multi.agent.reinforcement.learning|"
    r"multi.agent.control|"
    r"multi.agent.coevolutionary|"
    r"ppo.agent|"
    r"rl.agent|"
    r"agent.learning.for.(?:walking|locomotion)|"
    r"agentic.simulation.of.slam)\b"
)

def embodied_decision(title: str, abstract: str = "") -> BrainEvidence | None:
    t = re.sub(r"\s+", " ", title or "").lower()
    d = re.sub(r"\s+", " ", abstract or "").lower()
    if not hit(t + " " + d, ROBOT):
        return None

    # Technically named "agents" in RL / multi-agent gait control are not
    # language-based deliberative robot agents.
    if hit(t, AGENT_FALSE_FRIEND) and not hit(t + " " + d, r"\b(?:llm|large.language.model|tool.calling|skill.calling)\b"):
        if hit(t, NAV_OBJECTIVE) and not hit(t, r"\b(?:gait|locomotion|walking|torque.control)\b"):
            return BrainEvidence(NAV, "RL 多智能体用于环境导航，非高层语言 Agent", tags=("Multi-agent RL",))
        return BrainEvidence(CONTROL, "主要贡献是多智能体强化学习或步态控制", tags=("Multi-agent RL",))

    if hit(t, SOFTWARE_PRODUCT):
        return BrainEvidence(SOFTWARE, "主要成果是数据集、仿真工具或基准，而非高层决策系统")

    # VLM + perception is perception, absent an architecture for high-level
    # language reasoning, skill execution or task-level decision-making.
    if hit(t, PERCEPTION_OBJECTIVE) and not hit(t, AGENT_ARCH):
        return BrainEvidence(NAV, "主要任务是环境感知/地形估计而非 Agent 决策",
                             tags=("VLM",) if hit(t, VLM) else ())

    # A robot Agent may use navigation/perception as a skill. When the
    # research contribution is language-driven task decomposition or tool/skill
    # orchestration, keep it in Brain even if the title says "navigation".
    # Require both title-level agent/model evidence and concrete planning
    # evidence in the title or abstract; generic VLN is still Navigation.
    high_level_title = hit(t, r"\\b(?:agentic|embodied.agent|robot(?:ic)?.agent|"
                           r"llm|language.model|vlm|vision.language|"
                           r"skill.calling|tool.calling|task.planning)\\b")
    explicit_skill = hit(t + " " + d, r"\\b(?:tool.call(?:ing|s)?|"
                         r"skill.(?:call(?:ing|s)?|selection|composition|execution)|"
                         r"task.decomposition|task.planning|"
                         r"high.level.(?:decision|planning)|"
                         r"reflection.and.replanning|"
                         r"language.model.planning)\\b")
    explicit_language = hit(t + " " + d, r"\\b(?:llm|large.language.model|"
                            r"vision.language.model|vlm|language.instructions|"
                            r"language.model|agentic)\\b")
    if high_level_title and explicit_skill and explicit_language and not hit(t, AGENT_FALSE_FRIEND):
        return BrainEvidence(
            BRAIN, "研究语言驱动的高层任务分解、技能编排或工具调用",
            related=(NAV,) if hit(t, NAV_OBJECTIVE) else
                    (CONTROL,) if hit(t, CONTROL_OBJECTIVE) else (),
            tags=("Agentic", "Skill/Tool Calling")
        )

    # A deliberately narrow high-level agent rule: requires agent architecture
    # AND actionable decision skills, or a highly distinctive agent name.
    distinctive = hit(t, r"\b(?:bt.agent|visual.interface.agent|"
                      r"agentic.vision.language.navigation|"
                      r"cooperative.agents?.for.multi.object.navigation|"
                      r"self.evolving.agents?.for.embodied.navigation|"
                      r"quadrupedgpt)\b")
    agent_architecture = hit(t, AGENT_ARCH) or (
        hit(t, r"\b(?:robot.agent|embodied.agent|"
                    r"cooperative.agents?|agentic.navigation)\b") and hit(d, REASONING)
    )
    action_reasoning = hit(t + " " + d, REASONING)
    language_model = hit(t + " " + d, r"\b(?:llm|language.model|"
                         r"vision.language|vlm|vla|"
                         r"tool.calling|skill.calling|"
                         r"reasoning|world.model.planning)\b")
    if distinctive or (agent_architecture and action_reasoning and language_model):
        return BrainEvidence(
            BRAIN, "核心创新是具身 Agent、高层任务推理、技能调用或协作决策",
            related=(NAV,) if hit(t, NAV_OBJECTIVE) else (CONTROL,) if hit(t, CONTROL_OBJECTIVE) else (),
            tags=("Agentic", "Skill/Tool Calling") if hit(t+d, r"skill|tool|behavior.tree") else ("Agentic",)
        )

    # Distinguish concrete foundation-model innovations from action policies.
    if hit(t, VLA) and hit(t, r"token.compression|visual.token|geometric.inductive.bias|cross.view.fusion|human.video.guided.adaptation"):
        return BrainEvidence(BRAIN, "VLA基础模型架构、表示或推理机制创新", related=(CONTROL,), tags=("VLA",))
    if hit(t, VLA) and hit(t, r"agricultural.manipulation|grasping.policy|locomotion.policy|whole.body.control"):
        return BrainEvidence(CONTROL, "面向具体任务的VLA动作策略学习", related=(BRAIN,), tags=("VLA",))

    # VLA model research rather than robot's low-level controller: action-
    # oriented policy steering/whole-body control remains in Control.
    if hit(t, VLA):
        if hit(t, VLA_ACTION_CONTROL) and not hit(t, r"\b(?:model|architecture|"
                                                       r"token.compression|task.memory)\b"):
            return BrainEvidence(CONTROL, "VLA 在此作为辅助技术，主要研究实时运动/力控制",
                                 related=(BRAIN,), tags=("VLA",))
        if hit(t, MODEL_CONTRIBUTION) or hit(d, r"\b(?:vision.language.action|"
                                                    r"vla.model|"
                                                    r"task.context.memory|"
                                                    r"vision.language.model)\b"):
            return BrainEvidence(BRAIN, "研究 VLA 模型架构、推理或任务表示",
                                 related=(CONTROL,), tags=("VLA",))
        return BrainEvidence(BRAIN, "VLA 相关研究，主要贡献尚需人工复核",
                             related=(CONTROL,), review=True, tags=("VLA",))

    # Explicit long-horizon language reasoning in VLN is a brain contribution.
    # A plain VLN benchmark/policy, or a VLM used only for grounding, is NAV.
    if hit(t, VLN):
        deliberate = hit(t + " " + d, r"\b(?:reason(?:er|ing)|reflect(?:ion|ive)|"
                         r"dialog(?:ue)?|collaborat(?:ive|ion)|"
                         r"multi.agent.coordination|"
                         r"hierarchical.reasoning|"
                         r"language.model.plann(?:ing|er)|"
                         r"task.decomposition|tool.calling|"
                         r"skill.execution|"
                         r"agentic)\b")
        if deliberate and hit(t, r"\b(?:collaborat(?:ive|ion)|"
                                  r"dialog(?:ue)?|large.small.hierarch|"
                                  r"agentic|"
                                  r"long.horizon)\b"):
            return BrainEvidence(BRAIN, "VLN 主要贡献涉及高层推理、协作/反思机制",
                                 related=(NAV,), tags=("VLN", "Agentic VLN"))
        return BrainEvidence(NAV, "以视觉语言导航算法或视觉落地为主要任务",
                             related=(BRAIN,), tags=("VLN",))

    # VLM-only papers go to Brain ONLY when their main contribution is model
    # reasoning or task planning, never solely from having a VLM in a title.
    if hit(t, VLM):
        if hit(t + " " + d, REASONING) and hit(t, r"\b(?:planning|"
                        r"reasoning|agent|task|memory|"
                        r"tool|skill)\b"):
            return BrainEvidence(BRAIN, "VLM 用于高层任务推理和技能决策",
                                 related=(NAV,) if hit(t, NAV_OBJECTIVE) else (),
                                 tags=("VLM",))
        if hit(t, NAV_OBJECTIVE):
            return BrainEvidence(NAV, "VLM 用于导航/感知；无充分高层 Agent 贡献证据",
                                 related=(BRAIN,), tags=("VLM",))

    return None
