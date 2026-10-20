# 免费大模型辅助分类审核

确定结果可用于改类；不确定则保留规则分类并继续待复核。

- 规则分类资源：1668
- 具有当前分类版本模型建议：55
- 本次新增建议：3
- 当日新增待复核候选：19
- 历史待复核候选：433
- 本次处理已有模型建议：27
- 本次实际改变主分类：1
- 本次API调用次数：2
- 本次理论最大审核数：6
- 本次有效输出率：50.0%
- 固定免费模型：openrouter/free
- 规则与模型主分类不一致：11

## 失败原因统计

- quota_auth_or_unavailable_model: 1

## 安全诊断（不含模型原文）


## 本次分类修改

- hu-zlatan/embodied-ai-radar: 大脑与具身智能 -> 大脑与具身智能
- weihairuo/wheel-motion-uncertainty: 小脑与运动控制 -> 感知建图与导航
- CondenseVLA: Learnable History Condensation for Efficient Multi-Frame VLA: 大脑与具身智能 -> 大脑与具身智能
- Time-JEPA: Grounding Video World Models with Physical Time Series: 小脑与运动控制 -> 小脑与运动控制
- Unifying Embodied Foundation Models via a Model-to-Policy Formulation: 大脑与具身智能 -> 大脑与具身智能
- Causal Analysis of Robot Foundation Models Enables Efficiency Gains: 小脑与运动控制 -> 小脑与运动控制
- Fast-VLA: You Only Think Once for Robot Manipulation: 大脑与具身智能 -> 大脑与具身智能
- SAPS: Shared Autonomy for Policy Steering by Blending Teleoperation with a Pretrained VLA: 小脑与运动控制 -> 小脑与运动控制
- MorphAct: Robot Policies Morphing with the Worlds They Act In: 小脑与运动控制 -> 小脑与运动控制
- LIME: Learning Intent-aware Camera Motion from Egocentric Video: 小脑与运动控制 -> 小脑与运动控制
- Modeling and Understanding Neural Weights of Humanoid Policies with Diffusion: 小脑与运动控制 -> 小脑与运动控制
- FACT: A Multimodal Force-Action-Track Foundation Model for Human-to-Robot Dexterity: 大脑与具身智能 -> 大脑与具身智能
- Active Generative Simulation: Meta-Learning What to Simulate for Sim-and-Real Policy Co-Training: 基础软件与系统 -> 基础软件与系统
- ConTrack: Constrained Hand Motion Tracking with Adaptive Trade-off Control: 小脑与运动控制 -> 小脑与运动控制
- Learning Self-Orchestration in Decentralized Agent Swarms: 感知建图与导航 -> 感知建图与导航
- Value-Preserving Action Quantization: 小脑与运动控制 -> 小脑与运动控制
- Noise Space Learning for VLA Adaptation: 大脑与具身智能 -> 大脑与具身智能
- BT-Agent: Deploying Onboard Robot Agents with Behavior Trees and Multi-Fidelity Evaluation: 大脑与具身智能 -> 大脑与具身智能
- Mapless, Stabilizing, and Anti-Stuck Flipper Control for Articulated Tracked Robots: 感知建图与导航 -> 感知建图与导航
- Design and Control of the "QuadBoat": A Quadruped Surface Vehicle for Drowning Rescue: 小脑与运动控制 -> 小脑与运动控制
- Lessons from the Field: A Case Study of Robotic Intervention in an Industrial Emergency: 特种应用与产品 -> 特种应用与产品
- HORIZON: Recoverability-Governed Curriculum for Physical-Domain Scaling: 小脑与运动控制 -> 小脑与运动控制
- Research on Downhole MTATBOT Positioning and Autonomous Driving Strategies Based on Odometer-Assisted Inertial Measurement: 感知建图与导航 -> 感知建图与导航
- Intelligent Firefighting Robot Based on HT32F52352: 特种应用与产品 -> 特种应用与产品
- Meaningful human control and variable autonomy in human-robot teams for firefighting: 特种应用与产品 -> 特种应用与产品
- Implementation and Feedback Controller of Mobile Platform for Hammering Inspection Robot: 特种应用与产品 -> 特种应用与产品
- Explosion-proof lithium-ion battery pack – In-depth investigation and experimental study on the design criteria: 感知建图与导航 -> 感知建图与导航

## 分类冲突（前80条）

- weihairuo/wheel-motion-uncertainty | 规则：感知建图与导航 | 模型：感知建图与导航 | 理由：面向轮足机器人改进激光惯性里程计，重点处理退化与轮速不确定性 | https://github.com/weihairuo/wheel-motion-uncertainty
- Time-JEPA: Grounding Video World Models with Physical Time Series | 规则：小脑与运动控制 | 模型：大脑与具身智能 | 理由：以物理时间序列辅助视频世界模型，保持并学习跨域物理状态演化 | https://arxiv.org/abs/2610.23982
- Causal Analysis of Robot Foundation Models Enables Efficiency Gains | 规则：小脑与运动控制 | 模型：大脑与具身智能 | 理由：机械分析视语言动作跨注意力层的因果条件接口 | https://arxiv.org/abs/2610.20750
- SAPS: Shared Autonomy for Policy Steering by Blending Teleoperation with a Pretrained VLA | 规则：小脑与运动控制 | 模型：大脑与具身智能 | 理由：融合预训练VLA模型与遥操作进行策略引导，属于高层具身智能与自主决策范畴。 | https://arxiv.org/abs/2606.15568
- MorphAct: Robot Policies Morphing with the Worlds They Act In | 规则：小脑与运动控制 | 模型：大脑与具身智能 | 理由：基于交互语境的策略参数动态调整，体现具身智能中的语境感知与自适应能力。 | https://arxiv.org/abs/2610.20019
- LIME: Learning Intent-aware Camera Motion from Egocentric Video | 规则：小脑与运动控制 | 模型：大脑与具身智能 | 理由：语言意识相机运动生成，旨在通过意图感知提升具身代理感知与行动能力。 | https://arxiv.org/abs/2607.02417
- Learning Self-Orchestration in Decentralized Agent Swarms | 规则：感知建图与导航 | 模型：大脑与具身智能 | 理由：研究去中心化智能体群的自组织与高层协同，属于多智能体决策与具身智能。 | https://doi.org/10.48550/arxiv.2610.22322
- Mapless, Stabilizing, and Anti-Stuck Flipper Control for Articulated Tracked Robots | 规则：感知建图与导航 | 模型：小脑与运动控制 | 理由：利用惯性测量和关节角实现无地图翻转控制方法 | https://arxiv.org/abs/2610.13838
- HORIZON: Recoverability-Governed Curriculum for Physical-Domain Scaling | 规则：小脑与运动控制 | 模型：大脑与具身智能 | 理由：提出基于可恢复性的物理域扩展课程，提升具身智能策略泛化。 | http://arxiv.org/abs/2606.05143v1
- Implementation and Feedback Controller of Mobile Platform for Hammering Inspection Robot | 规则：特种应用与产品 | 模型：小脑与运动控制 | 理由：移动平台反馈控制算法的运动控制实现与验证 | https://doi.org/10.1299/jsmeidecon.2023.0_29
- Explosion-proof lithium-ion battery pack – In-depth investigation and experimental study on the design criteria | 规则：感知建图与导航 | 模型：硬件与防爆 | 理由：锂电池包防爆设计与实验研究，属硬件防爆类，非具身智能规划。 | https://doi.org/10.1016/j.energy.2022.123715
