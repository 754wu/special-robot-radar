"""Manual classification corrections after secondary abstract-level evidence audit.
Only cases whose main physical or model deliverable is explicit in stored metadata.
"""
BATCH_DECISIONS = {
    "condensevla: learnable history condensation for efficient multi-frame vla": ("大脑与具身智能", "摘要提出VLA解码端可学习的历史视觉Token凝缩模块，通过查询和交叉注意力压缩多帧上下文；主要创新为基础模型的多帧表征与推理结构，并非运动控制器。"),
    "causal analysis of robot foundation models enables efficiency gains": ("大脑与具身智能", "摘要采用激活修补分析π0.5等VLA的视觉语言信息到动作专家的因果通路，主要贡献为具身基础模型机制解释与计算效率。"),
    "fast-vla: you only think once for robot manipulation": ("大脑与具身智能", "摘要提出VLM每回合仅编码一次任务上下文、利用固定多层KV记忆供在线Actor查询，主要贡献为VLA模型推理架构与效率优化。"),
    "improving the energy efficiency of quadruped robots on uneven terrains through bio-inspired elastic design": ("硬件与防爆", "摘要提出可调刚度弹性腿结构与样机并验证不同地形下能效提升；创新集中在仿生弹性物理腿设计。"),
    "mors: bldc based small sized quadruped robot": ("硬件与防爆", "摘要明确交付MORS小型四足机器人整机的机械设计、无刷驱动电子与模块化结构；运动控制算法属于集成组成部分。"),
    "magnetically driven quadruped soft robot with multimodal motion for targeted drug delivery": ("硬件与防爆", "摘要明确提出具有特定磁化角度、磁性顶盖和多模态运动能力的磁驱四足软体机器人新结构，主要技术交付为机器人本体与驱动机制。"),
    "a pipeline inspection robot for navigating tubular environments in the sub-centimeter scale": ("硬件与防爆", "摘要提出2.2克、直径小于10毫米的介电弹性体驱动微型管道机器人及锚定结构，主要创新为微型机器人驱动硬件与实体构型。"),
}
