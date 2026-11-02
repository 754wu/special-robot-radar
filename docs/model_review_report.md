# 免费大模型辅助分类审核

分类冲突时暂用模型类别并进入二次复核；分类一致则记录已审核、不再重复抽查。

- 规则分类资源：1978
- 具有当前分类版本模型建议：382
- 本次新增建议：52
- 当日新增待复核候选：16
- 历史待复核候选：4
- 本次应用审核建议：52
- 本次新增独立审核事件：52
- 累计历史审核事件（去重）：817
- 累计涉及不同资源：592
- 本次实际改变主分类：20
- 本次API调用次数：22
- 今日累计API调用次数（北京时间）：22/40
- 今日P4抽查API调用次数（北京时间）：14/20
- 本次理论最大审核数：66
- 本次有效输出率：78.8%
- 固定免费模型：openrouter/free
- 规则与模型主分类不一致：40

## 失败原因统计

- invalid_fields: 3
- missing_or_invalid_batch_items: 2
- output_truncated: 1

## 安全诊断（不含模型原文）

- {"error": "output_truncated", "shape": "empty", "length": 0, "finish_reason": "length", "served_model": "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free"}

## 本次分类修改

- 12sqawdwq/FlyHead: 感知建图与导航 -> 大脑与具身智能
- MIHIR-1304/NOBoT: 感知建图与导航 -> 特种应用与产品
- jinyang-ops/go2-sim-test-bench: 小脑与运动控制 -> 基础软件与系统
- CaPtain: A Pipeline for Post-Training Code-as-Policy Robot Agents: 大脑与具身智能 -> 大脑与具身智能
- Sensorium: An Open-Source Multimodal Data Collection and Curation Library for Embodied Surgical AI: 大脑与具身智能 -> 基础软件与系统
- WorldBridge: Bridging Video and Action for Task Generalization in World Action Models: 小脑与运动控制 -> 大脑与具身智能
- $\nabla$Mimic: Ultra-Efficient Humanoid Control with Differentiable Simulation: 基础软件与系统 -> 小脑与运动控制
- Keeping the Franka Emika Panda alive: a ROS 2 stack with a reliable position interface: 基础软件与系统 -> 小脑与运动控制
- How does Nav2 calculate and provide the map -> odom transform? (REP 105): 感知建图与导航 -> 感知建图与导航
- [Open Source] DDS AutoDiag v0.1.0 — ROS 2 DDS Diagnostics with AI-Assisted Troubleshooting: 基础软件与系统 -> 基础软件与系统
- Indirect Optimal Control for Constructing Libraries of Periodic Trajectories: Application to Bipedal Walking: 小脑与运动控制 -> 小脑与运动控制
- Search and Rescue in Tunnels, an Integrated Approach Using Robotic Platforms: 基础软件与系统 -> 基础软件与系统
- Flexible-torso quadruped robots: biomimetic principles, structural designs, and torso-limb coordination – a review: 小脑与运动控制 -> 基础软件与系统
- Training in Deployment: Human-in-the-loop Online Post-Training for Robot Manipulation: 小脑与运动控制 -> 大脑与具身智能
- Agentic World Action Models: 大脑与具身智能 -> 大脑与具身智能
- SharedKV-BT: Node-Local Typed Decisions for Behavior-Tree Agents: 大脑与具身智能 -> 大脑与具身智能
- RegenHarness: A Robot Agent Harness with Evidence-Gated Recursive Self-Improvement: 大脑与具身智能 -> 基础软件与系统
- Static and Dynamic Path Planning Using Enhanced Firefly Algorithm with B-spline for Mobile Robot Navigation: 感知建图与导航 -> 感知建图与导航
- Smooth LiDAR–Inertial–Joint Odometry for perception-driven legged locomotion: 小脑与运动控制 -> 感知建图与导航
- Robust Locomotion Control of Quadrupedal Wheel-Legged Robots via Contrastive History-Aware Reinforcement Learning in Complex Environments: 小脑与运动控制 -> 小脑与运动控制
- Image Segmentation-Guided Visual Tracking on a Bio-Inspired Quadruped Robot: 感知建图与导航 -> 感知建图与导航
- Terrain-based place recognition for LiDAR SLAM of quadruped robots with limited field-of-view measurements: 感知建图与导航 -> 感知建图与导航
- From Prompts to Paths: Large Language Models for Zero-Shot Planning in Unmanned Ground Vehicle Simulation: 基础软件与系统 -> 感知建图与导航
- Research on Lidar-Vision Fusion for Mobile Robot Navigation: Fusion Application of LiDAR and Machine Vision YOLO: 感知建图与导航 -> 感知建图与导航
- A Novel Contact‐Implicit Trajectory Optimization Framework for Quadruped Locomotion without Fixed Contact Sequences: 小脑与运动控制 -> 小脑与运动控制
- Deep Reinforcement Learning with PSO Algorithm in Agile Dodge Actions of Quadruped Robot: 小脑与运动控制 -> 小脑与运动控制
- WITHDRAWN: Industrial Mobile Robot Navigation Based on the LiDAR-IMU-Visual Measurements: 感知建图与导航 -> 感知建图与导航
- Editorial: Vibration-based robot locomotion: 小脑与运动控制 -> 小脑与运动控制
- Simultaneous localization and mapping (SLAM)-based robot localization and navigation algorithm: 感知建图与导航 -> 感知建图与导航
- A Learning-based Motion Control Policy Fusing Multi-Mode Perception for Legged Robot: 小脑与运动控制 -> 小脑与运动控制
- DIGITAL TWIN BASED LIGHTWEIGHTING OF ROBOT UNMANNED GROUND VEHICLES: 基础软件与系统 -> 硬件与防爆
- Research on the autonomous system of the quadruped robot with a manipulator to realize leader‐following, object recognition, navigation and operation: 感知建图与导航 -> 特种应用与产品
- Efficient Reinforcement Learning for 3D LiDAR Navigation of Mobile Robot: 感知建图与导航 -> 感知建图与导航
- Event-Based Line SLAM in Real-Time: 感知建图与导航 -> 感知建图与导航
- Plane-based grid map: A robot-centric mapping algorithm for wheel-legged rover motion planning in unstructured terrain environments: 感知建图与导航 -> 感知建图与导航
- Multi-Agent Autonomy: Advancements and Challenges in Subterranean Exploration: 感知建图与导航 -> 感知建图与导航
- A Massively Parallel Implementation of Gaussian Process Regression for Real Time Bathymetric Modeling and Simultaneous Localization and Mapping: 感知建图与导航 -> 基础软件与系统
- Mobile Robot Navigation Functions Tuned by Sensor Readings in Partially Known Environments: 感知建图与导航 -> 感知建图与导航
- Vision-Only Robot Navigation in a Neural Radiance World: 感知建图与导航 -> 感知建图与导航
- Integration of prioritized impedance controller in improved hierarchical operational-space torque control frameworks for legged locomotion robots: 小脑与运动控制 -> 小脑与运动控制
- Mobile Robot Navigation with Swarm Intelligence using a Decentralized Strategy: 感知建图与导航 -> 感知建图与导航
- Validating observer based on-line slip estimation for improved navigation by a mobile robot: 感知建图与导航 -> 感知建图与导航
- Acquisition of Walking Motion by Deep Reinforcement Learning for Quadruped Robot Using Simulation: 小脑与运动控制 -> 小脑与运动控制
- Robust Walking Based on MPC With Viability Guarantees: 小脑与运动控制 -> 小脑与运动控制
- Efficient Computation for Localization and Navigation System for a Differential Drive Mobile Robot in Indoor and Outdoor Environments: 感知建图与导航 -> 感知建图与导航
- Influences of pitch angle for a quadruped robot in bounding gait: 小脑与运动控制 -> 小脑与运动控制
- Agile Control For Quadruped Robot In Complex Environment Based on Deep Reinforcement Learning Method: 小脑与运动控制 -> 小脑与运动控制
- Robot Navigation with Interaction-based Deep Reinforcement Learning: 感知建图与导航 -> 小脑与运动控制
- Bioinspiration to Robot Locomotion implementing 3D printed Foxtail Grass: 小脑与运动控制 -> 硬件与防爆
- Hand-Eye Calibration of EOD Robot by Solving the AXB = YCZD Problem: 特种应用与产品 -> 小脑与运动控制
- Remote drain inspection framework using the convolutional neural network and re-configurable robot Raptor: 感知建图与导航 -> 基础软件与系统
- Towards Contactless Learning Activities during Pandemics Using Autonomous Service Robots: 感知建图与导航 -> 特种应用与产品

## 分类冲突（前80条）

- 12sqawdwq/FlyHead | 规则：大脑与具身智能 | 模型：大脑与具身智能 | 理由：构建果蝇全脑连接组模型驱动机器人，实现脑启发式的具身感知与运动控制。 | https://github.com/12sqawdwq/FlyHead
- MIHIR-1304/NOBoT | 规则：特种应用与产品 | 模型：特种应用与产品 | 理由：集成OpenCV、YOLOv8与传感器融合的四足机器人，属于完整系统集成与产品级工程。 | https://github.com/MIHIR-1304/NOBoT
- jinyang-ops/go2-sim-test-bench | 规则：基础软件与系统 | 模型：基础软件与系统 | 理由：摘要过于简短，无法确定主要贡献是仿真测试工具还是强化学习运动控制策略本身。 | https://github.com/jinyang-ops/go2-sim-test-bench
- Sensorium: An Open-Source Multimodal Data Collection and Curation Library for Embodied Surgical AI | 规则：基础软件与系统 | 模型：基础软件与系统 | 理由：提出开源多模态数据采集与标注库Sensorium，提供数据处理与生成功能，属于基础软件与系统。 | https://arxiv.org/abs/2610.41946
- WorldBridge: Bridging Video and Action for Task Generalization in World Action Models | 规则：大脑与具身智能 | 模型：大脑与具身智能 | 理由：提出WorldBridge视频到动作桥接方法，提升世界动作模型任务泛化能力，属于具身基础模型架构研究。 | https://arxiv.org/abs/2610.40748
- $\nabla$Mimic: Ultra-Efficient Humanoid Control with Differentiable Simulation | 规则：小脑与运动控制 | 模型：小脑与运动控制 | 理由：提出可微仿真人形控制方法$\nabla$Mimic，解决接触动力学梯度与效率问题，属于小脑与运动控制。 | https://arxiv.org/abs/2610.41654
- Keeping the Franka Emika Panda alive: a ROS 2 stack with a reliable position interface | 规则：小脑与运动控制 | 模型：小脑与运动控制 | 理由：异步硬件接口解决位置控制抖动，属低层执行创新 | https://arxiv.org/abs/2608.19740
- Flexible-torso quadruped robots: biomimetic principles, structural designs, and torso-limb coordination – a review | 规则：基础软件与系统 | 模型：基础软件与系统 | 理由：标题表明是综述，未展示新算法或系统，缺乏明确创新贡献 | https://doi.org/10.1080/01691864.2026.2742578
- October CWG Meeting - Deep Venture and ResQ ROV: From COTS to Capability | 规则：特种应用与产品 | 模型：硬件与防爆 | 理由：仅为会议通知，未明确提出新算法、硬件或软件交付物，证据不足。 | https://discourse.openrobotics.org/t/october-cwg-meeting-deep-venture-and-resq-rov-from-cots-to-capability/59056
- Training in Deployment: Human-in-the-loop Online Post-Training for Robot Manipulation | 规则：大脑与具身智能 | 模型：大脑与具身智能 | 理由：具身基础模型在线人在回合后训练框架TIDE，通过证明条件监督学习实现适配 | https://arxiv.org/abs/2610.29264
- Upcoming ROS 2 Workshop: Building AI Robots with Vision-Language Models and ROS 2 | 规则：基础软件与系统 | 模型：大脑与具身智能 | 理由：研讨会通知，未展示具体的研究输出、算法或系统设计，仅为主题活动预告。 | https://discourse.openrobotics.org/t/upcoming-ros-2-workshop-building-ai-robots-with-vision-language-models-and-ros-2/59032
- RegenHarness: A Robot Agent Harness with Evidence-Gated Recursive Self-Improvement | 规则：基础软件与系统 | 模型：基础软件与系统 | 理由：提出证据门控递归自我改进的机器人代理框架，实现任务规划到技能执行的闭环 | http://arxiv.org/abs/2609.27612v1
- Efficient Ripeness Monitoring in Open-Facility Environments Using a Quadruped Robot and Panoramic AI Recognition | 规则：感知建图与导航 | 模型：特种应用与产品 | 理由：交付自主巡检型轮腿四足番茄成熟度监测系统，并完成商业温室部署验证 | https://doi.org/10.20944/preprints202608.0999.v1
- Smooth LiDAR–Inertial–Joint Odometry for perception-driven legged locomotion | 规则：感知建图与导航 | 模型：感知建图与导航 | 理由：提出融合多源感知的四足机器人状态估计方法，属定位导航。 | https://doi.org/10.55092/rl20260024
- Vision-Language-Action and Vision Language Models for Robot Manipulation: A Comprehensive Review Towards Real-World Applications | 规则：大脑与具身智能 | 模型：基础软件与系统 | 理由：综述论文仅提供分类分析，无新模型或系统交付 | https://doi.org/10.20944/preprints202606.0400.v1
- From Prompts to Paths: Large Language Models for Zero-Shot Planning in Unmanned Ground Vehicle Simulation | 规则：感知建图与导航 | 模型：感知建图与导航 | 理由：论文主要贡献为利用大语言模型实现无人车零样本路径规划与导航。 | https://doi.org/10.3390/drones9120875
- Prototypes of intelligent robots for first aid in natural disasters: A bibliometric analysis | 规则：特种应用与产品 | 模型：基础软件与系统 | 理由：本文为灾难机器人研究的文献综述，未提出新算法或系统 | https://doi.org/10.31893/multirev.2026304
- Comparative analysis of localization methods for autonomous mobile robots using Robot Operating System 2 | 规则：感知建图与导航 | 模型：小脑与运动控制 | 理由：本文对现有定位方法进行了比较分析但未提出新架构或方法，属于算法评估而非核心贡献 | https://doi.org/10.21439/jme.v8i.122
- The Smallest Impulse-based Firefighting Drone for Rapid Response: Making every second count! | 规则：特种应用与产品 | 模型：硬件与防爆 | 理由：题名指向超小型脉冲消防无人机设计，但摘要未说明结构创新 | https://doi.org/10.1109/ssrr68451.2025.11391279
- Smart Wireless Power Transfer: A Review of Integrating AI and Sensing for Next-Generation Robotic and IoT Systems | 规则：特种应用与产品 | 模型：硬件与防爆 | 理由：论文综述融合AI与传感的智能无线充电系统，核心在于线圈结构设计与硬件能量传输优化。 | https://doi.org/10.20944/preprints202506.2021.v1
- Automated system of scaffold point cloud data acquisition using a robot dog | 规则：特种应用与产品 | 模型：基础软件与系统 | 理由：系统实现自动化点云获取，属于软件工具交付，证据充分 | https://doi.org/10.1016/j.autcon.2024.105944
- Review of Self-Learning Systems Based on End-to-End Deep Learning in Bionic Robots | 规则：小脑与运动控制 | 模型：大脑与具身智能 | 理由：综述自学系统在仿生机器人中的应用，未提出新方法，仅回顾现有工作 | https://doi.org/10.54254/2755-2721/97/20241337
- Advanced Pipeline Inspection Robot Development Utilizing Non-Destructive Evaluation and Simulated with Verilog | 规则：特种应用与产品 | 模型：硬件与防爆 | 理由：管道检查机器人设计创新，结合非破坏性评估实现硬件实现 | https://doi.org/10.2139/ssrn.4894242
- Distribution Station Inspection Robot with Modular Manipulator | 规则：特种应用与产品 | 模型：硬件与防爆 | 理由：模块化操作臂提升检查灵活性，体现硬件机制创新 | https://doi.org/10.2139/ssrn.4873574
- Advances in Robotic Welding for Metallic Materials: Application of Inspection, Modeling, Monitoring and Automation Techniques | 规则：特种应用与产品 | 模型：小脑与运动控制 | 理由：主要产出为焊接技术综述，未给出新的控制方法 | https://doi.org/10.3390/met13040711
- Rescue and Firefighting Operations During Incidents Involving Vehicles with Alternative Propulsion. Electric Vehicles | 规则：特种应用与产品 | 模型：感知建图与导航 | 理由：仅是对电动车辆救援风险的综述，未提出新方法或具体成果 | https://doi.org/10.12845/sft.60.2.2022.1
- DIGITAL TWIN BASED LIGHTWEIGHTING OF ROBOT UNMANNED GROUND VEHICLES | 规则：硬件与防爆 | 模型：硬件与防爆 | 理由：基于数字孪生数据对机器人底盘进行拓扑优化与轻量化设计，属于硬件结构与CAD工程。 | https://doi.org/10.22190/fuacr221121015b
- Offline Reinforcement Learning for Visual Navigation | 规则：感知建图与导航 | 模型：小脑与运动控制 | 理由：提出ReViND离线RL系统，实现视觉导航任务的奖励函数优化。 | https://doi.org/10.48550/arxiv.2212.08244
- Design and Motion Planning of a Metamorphic Flipping Robot | 规则：小脑与运动控制 | 模型：硬件与防爆 | 理由：提出柔性腰部可重构腿足机器人设计并规划翻转恢复步态 | https://doi.org/10.3390/act11120344
- Research on the autonomous system of the quadruped robot with a manipulator to realize leader‐following, object recognition, navigation and operation | 规则：特种应用与产品 | 模型：特种应用与产品 | 理由：提出了一个具备操纵器的四足机器人自主系统解决方案，包括感知、导航和操作模块 | https://doi.org/10.1049/csy2.12069
- Design and Development of Internal Pipe Inspection Robot | 规则：特种应用与产品 | 模型：硬件与防爆 | 理由：仅凭标题无法区分是硬件机构设计还是完整检测系统，两类均可能。 | https://doi.org/10.24321/2454.8650.202202
- Inspection Robot Design for Underwater Structure in Complex Flow Environment | 规则：特种应用与产品 | 模型：硬件与防爆 | 理由：针对复杂水流环境设计了一种新型水下巡检机器人 | https://doi.org/10.1109/icosr57188.2022.00043
- A Massively Parallel Implementation of Gaussian Process Regression for Real Time Bathymetric Modeling and Simultaneous Localization and Mapping | 规则：基础软件与系统 | 模型：基础软件与系统 | 理由：大规模并行高斯过程回归实现实时水深建图与SLAM | https://doi.org/10.55417/fr.2022031
- Design and Development of Tank Cleaning and Inspection Robot | 规则：特种应用与产品 | 模型：硬件与防爆 | 理由：开发了适用于化工储罐清洗巡检的机器人整机设计与控制策略。 | https://doi.org/10.47750/pnr.2022.13.s03.156
- Robot Navigation with Interaction-based Deep Reinforcement Learning | 规则：小脑与运动控制 | 模型：小脑与运动控制 | 理由：提出了一种基于交互的深度强化学习机器人导航策略方法 | https://doi.org/10.1109/robio54168.2021.9739455
- Bioinspiration to Robot Locomotion implementing 3D printed Foxtail Grass | 规则：硬件与防爆 | 模型：硬件与防爆 | 理由：提出3D打印狗尾草生物灵感运动结构，属物理机构设计而非控制算法。 | https://doi.org/10.1109/robio54168.2021.9739623
- Hand-Eye Calibration of EOD Robot by Solving the AXB = YCZD Problem | 规则：小脑与运动控制 | 模型：小脑与运动控制 | 理由：提出手眼标定新算法，利用克罗内克积闭式求解与凸优化实现双臂协同校准 | https://doi.org/10.1109/access.2021.3136850
- Remote drain inspection framework using the convolutional neural network and re-configurable robot Raptor | 规则：基础软件与系统 | 模型：基础软件与系统 | 理由：提出CNN检测框架和可重构机器人Raptor，提供定制数据集，体现软件创新 | https://doi.org/10.1038/s41598-021-01170-0
- Towards Contactless Learning Activities during Pandemics Using Autonomous Service Robots | 规则：特种应用与产品 | 模型：特种应用与产品 | 理由：提出面向疫情无接触教学的自主服务机器人系统，集成导航与语音交互，属于特种应用与产品。 | https://doi.org/10.3390/app112110449
- A bio-inspired robotic climbing robot to understand kinematic and morphological determinants for an optimal climbing gait | 规则：小脑与运动控制 | 模型：硬件与防爆 | 理由：设计了具有活动脊椎、肩部和爪部的仿生攀爬机器人X4，研究其形态与步态优化。 | https://doi.org/10.1088/1748-3190/ac370f
