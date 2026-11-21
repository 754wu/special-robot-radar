# 免费大模型辅助分类审核

分类冲突时暂用模型类别并进入二次复核；分类一致则记录已审核、不再重复抽查。

- 规则分类资源：2376
- 具有当前分类版本模型建议：1152
- 本次新增建议：20
- 当日新增待复核候选：5
- 历史待复核候选：0
- 本次应用审核建议：20
- 本次新增独立审核事件：20
- 累计历史审核事件（去重）：2349
- 累计涉及不同资源：1488
- 本次实际改变主分类：7
- 本次API调用次数：8
- 今日累计API调用次数（北京时间）：8/40
- 今日P4抽查API调用次数（北京时间）：6/20
- 本次理论最大审核数：24
- 本次有效输出率：83.3%
- 固定免费模型：openrouter/free
- 规则与模型主分类不一致：84

## 失败原因统计

- output_truncated: 1

## 安全诊断（不含模型原文）

- {"error": "output_truncated", "shape": "empty", "length": 0, "finish_reason": "length", "served_model": "liquid/lfm-3-1.7b:free"}

## 本次分类修改

- Mobile ROS: an open-source ROS 2 app for your phone: 基础软件与系统 -> 基础软件与系统
- A survey of natural language interaction and environmental perception in intelligent robotics: 感知建图与导航 -> 基础软件与系统
- From Temperature-Limited to Battery-Limited Legged Locomotion: 小脑与运动控制 -> 小脑与运动控制
- Learning Latent Volumetric Dynamics for Multimodal Goal-Conditioned Robot Manipulation of Hair: 小脑与运动控制 -> 小脑与运动控制
- Alloy: A Multi-Material Physics Engine for Robot Learning: 小脑与运动控制 -> 基础软件与系统
- RUMI: A Robotiq-Matched Universal Manipulation Interface for Robot Learning with Augmented Reality and Haptic Feedback: 小脑与运动控制 -> 硬件与防爆
- A ROS-based Simulation Framework for Industrial Robotics Pick-and-Place Application: Integration of Vision-based Pose Estimation and 3-DOF Inverse Kinematics: 基础软件与系统 -> 基础软件与系统
- Design of Mecanum Wheel-Leg Coupled Multi-Terrain Quadruped Robot: 小脑与运动控制 -> 硬件与防爆
- Not What You Asked For: Typographic Attacks in Household Robot Manipulation: 小脑与运动控制 -> 感知建图与导航
- Research on IMU-LiDAR collaborative positioning method for unmanned mine truck under weak GNSS conditions: 感知建图与导航 -> 感知建图与导航
- MoDeSuite: Robot Learning Task Suite for Benchmarking Mobile Manipulation With Deformable Objects: 小脑与运动控制 -> 基础软件与系统
- Multi-session perception-aware coverage path planning for active semantic SLAM and automatic change detection: 感知建图与导航 -> 感知建图与导航
- DESIGN AND EXPERIMENT OF MULTI-PUROSE AND MODULAR SENSOR ROBOTIC PLATFORM FOR REAL-TIME ASSESSING AND MONITORING OF CEA FARMS USING POINT CLOUD, LIDAR, RGB AND THERMAL IMAGING: 感知建图与导航 -> 特种应用与产品
- Surrogate compliance modeling enables reinforcement learned locomotion gaits for soft robots: 小脑与运动控制 -> 小脑与运动控制
- A review of mobile robot navigation algorithms: 感知建图与导航 -> 感知建图与导航
- End-to-end Generative Spatial-Temporal Ultrasonic Odometry and Mapping Framework: 感知建图与导航 -> 感知建图与导航
- Robust Walking and Sim-to-Real Optimization for Quadruped Robots via Reinforcement Learning: 小脑与运动控制 -> 小脑与运动控制
- Underwater Pose SLAM using GMM scan matching for a mechanical profiling sonar: 感知建图与导航 -> 感知建图与导航
- Vision-Based Quadruped Pose Estimation and Gait Parameter Extraction Method: 小脑与运动控制 -> 小脑与运动控制
- Whole-Body Control with Motion/Force Transmissibility for Parallel-Legged Robot: 小脑与运动控制 -> 小脑与运动控制

## 分类冲突（前80条）

- A survey of natural language interaction and environmental perception in intelligent robotics | 规则：基础软件与系统 | 模型：基础软件与系统 | 理由：论文为综述，无新方法或系统交付物属于文献综述类 | https://doi.org/10.1007/s42452-026-09890-6
- Hal1lZtrk/Firefighter-Spider-Robot | 规则：特种应用与产品 | 模型：小脑与运动控制 | 理由：六足消防仿真含卡尔曼滤波楼梯平衡控制并实现避障灭火 | https://github.com/Hal1lZtrk/Firefighter-Spider-Robot
- Alloy: A Multi-Material Physics Engine for Robot Learning | 规则：基础软件与系统 | 模型：基础软件与系统 | 理由：提出多材质物理引擎Alloy实现软硬体统一仿真 | https://arxiv.org/abs/2611.16312
- RUMI: A Robotiq-Matched Universal Manipulation Interface for Robot Learning with Augmented Reality and Haptic Feedback | 规则：硬件与防爆 | 模型：硬件与防爆 | 理由：设计匹配二指夹爪的手持力反馈采集接口与增强现实提示 | https://arxiv.org/abs/2611.15802
- Quadruped Agile Locomotion: Sparsely Gated Mixture of Experts with Visual Input | 规则：小脑与运动控制 | 模型：大脑与具身智能 | 理由：提出稀疏门控混合专家视觉敏捷运动策略提升 | https://arxiv.org/abs/2604.19344
- Q-OIL: Optimistic Exploration in Learning from Human Interventions | 规则：小脑与运动控制 | 模型：基础软件与系统 | 理由：基于人类干预进度模型的机器人学习基准测试，类别界定需谨慎 | https://arxiv.org/abs/2611.08576
- GigaBrain-WBC-0.5: A Behavior World Model for Robust Humanoid Whole-Body Tracking with Environment Interaction | 规则：大脑与具身智能 | 模型：小脑与运动控制 | 理由：行为世界模型联合预测动作状态与行为分布，用于人形全身复杂地形跟踪控制。 | https://arxiv.org/abs/2608.18234
- WayTrace: A Map-to-Language-to-Trace Hierarchy for Embodied Urban Navigation | 规则：感知建图与导航 | 模型：大脑与具身智能 | 理由：整合地图指令、语言理解与轨迹预测，实现城市环境中的语言指令导航与执行 | https://arxiv.org/abs/2611.05129
- Semantically Adaptive Control Barrier Functions with Vision-Language Models for Real-Time Robot Navigation | 规则：感知建图与导航 | 模型：小脑与运动控制 | 理由：提出基于视觉语言模型语义自适应控制约束实时导航安全 | https://arxiv.org/abs/2603.21142
- Keeping the Franka Emika Panda alive: a ROS 2 stack with a reliable position interface | 规则：基础软件与系统 | 模型：小脑与运动控制 | 理由：异步硬件接口解决位置控制抖动，属低层执行创新 | https://arxiv.org/abs/2608.19740
- Design of Mecanum Wheel-Leg Coupled Multi-Terrain Quadruped Robot | 规则：硬件与防爆 | 模型：硬件与防爆 | 理由：设计新型麦克纳姆轮腿耦合四足机器人结构及运动学分析 | https://doi.org/10.1016/j.rineng.2026.114284
- Information-Driven Collaborative Autonomy for Heterogeneous UAV/UGV Teams | 规则：感知建图与导航 | 模型：大脑与具身智能 | 理由：基于ergodic control和贝叶斯多伯努利近似的协同自主框架. | https://arxiv.org/abs/2610.39379
- lightBot: rebuilt a ROSOrin Pro from a blank drive after apt update broke it (ROS 2 Humble, Orin NX, 37-chapter guide) | 规则：基础软件与系统 | 模型：感知建图与导航 | 理由：仅描述机器人重建维护步骤，未提出新研究输出或方法 | https://discourse.openrobotics.org/t/lightbot-rebuilt-a-rosorin-pro-from-a-blank-drive-after-apt-update-broke-it-ros-2-humble-orin-nx-37-chapter-guide/59328
- Which Hand Was Late? Diagnosis for Robot Failure Recovery in Bimanual Tool Use | 规则：大脑与具身智能 | 模型：感知建图与导航 | 理由：基于感知通道的双臂故障诊断可辨识性，不属导航检测，证据不足 | https://arxiv.org/abs/2610.37533
- Autonomous Pallet Jack Project – An Ongoing Robotics Project | 规则：感知建图与导航 | 模型：特种应用与产品 | 理由：项目介绍为主，缺乏明确研究创新点，难以判断类别 | https://discourse.openrobotics.org/t/autonomous-pallet-jack-project-an-ongoing-robotics-project/59254
- New course: Agentic Robotics with ROS 2, from AI agents to VLA models (code on GitHub) | 规则：大脑与具身智能 | 模型：基础软件与系统 | 理由：主要交付为可复用课程、代码、数据集与技能服务器工具，非新模型或智能体 | https://discourse.openrobotics.org/t/new-course-agentic-robotics-with-ros-2-from-ai-agents-to-vla-models-code-on-github/59239
- VisGeo-PipeTrack: A Visual Geometric Servo Control Framework with MPC-RCAPID Control for UAV-Based Dynamic Pipes Tracking | 规则：小脑与运动控制 | 模型：感知建图与导航 | 理由：提出了利用视觉几何约束和MPC-RCAPID控制的UAV动态管道跟踪框架，实现管道运动下的精确跟踪 | https://arxiv.org/abs/2610.35342
- RetroNav: Scene-Grounded Retrospection and Retry for Self-Evolving Lifelong Navigation | 规则：感知建图与导航 | 模型：大脑与具身智能 | 理由：提出训练免自我进化导航记忆与失败反思机制 | https://arxiv.org/abs/2610.35172
- October CWG Meeting - Deep Venture and ResQ ROV: From COTS to Capability | 规则：特种应用与产品 | 模型：硬件与防爆 | 理由：仅为会议通知，未明确提出新算法、硬件或软件交付物，证据不足。 | https://discourse.openrobotics.org/t/october-cwg-meeting-deep-venture-and-resq-rov-from-cots-to-capability/59056
- Training in Deployment: Human-in-the-loop Online Post-Training for Robot Manipulation | 规则：小脑与运动控制 | 模型：大脑与具身智能 | 理由：具身基础模型在线人在回合后训练框架TIDE，通过证明条件监督学习实现适配 | https://arxiv.org/abs/2610.29264
- Upcoming ROS 2 Workshop: Building AI Robots with Vision-Language Models and ROS 2 | 规则：基础软件与系统 | 模型：大脑与具身智能 | 理由：研讨会通知，未展示具体的研究输出、算法或系统设计，仅为主题活动预告。 | https://discourse.openrobotics.org/t/upcoming-ros-2-workshop-building-ai-robots-with-vision-language-models-and-ros-2/59032
- SOMA: Stack-of-Objects Manipulation using a Quadruped Robot | 规则：小脑与运动控制 | 模型：大脑与具身智能 | 理由：提出全身非手取堆叠强化学习框架与三维推进策略 | https://arxiv.org/abs/2610.20968
- Cross-Embodiment Causal Transfer from Human Videos to Robot Manipulation | 规则：小脑与运动控制 | 模型：大脑与具身智能 | 理由：提出CBST方法，实现人类视频到机器人操作的跨形态因果知识迁移并分析了子任务转移中的因果依赖关系 | https://arxiv.org/abs/2610.21798
- System design of the Ultra Mobility Vehicle: A driving, balancing, and jumping bicycle robot | 规则：硬件与防爆 | 模型：小脑与运动控制 | 理由：通过模拟驱动优化设计空间链路，结合深度RL实现多样运动行为的零-shot转移 | https://doi.org/10.1126/scirobotics.aed3627
- TRACE: Efficient Transfer Learning for Neural Whole-Body Control Across Humanoid Embodiments | 规则：小脑与运动控制 | 模型：大脑与具身智能 | 理由：利用编码器蒸馏与低秩强化学习实现预训练运动模型的跨具身高效适应 | https://doi.org/10.48550/arxiv.2610.17999
- JitterVLA: A Replay Benchmark for Motion Quality in VLA-Driven Human-Robot Manipulation | 规则：基础软件与系统 | 模型：小脑与运动控制 | 理由：提出VLA人机操作运动质量重放基准，评估并改进轨迹平滑与低层执行控制方法。 | https://arxiv.org/abs/2610.13628
- Acting from Belief, Looking When Needed: A Bayesian Spatial World Model for Navigation under Intermittent Perception | 规则：感知建图与导航 | 模型：大脑与具身智能 | 理由：提出贝叶斯空间世界模型，实现间歇感知下的导航推理与信念更新 | https://doi.org/10.48550/arxiv.2610.11591
- RegenHarness: A Robot Agent Harness with Evidence-Gated Recursive Self-Improvement | 规则：大脑与具身智能 | 模型：基础软件与系统 | 理由：提出证据门控递归自我改进的机器人代理框架，实现任务规划到技能执行的闭环 | http://arxiv.org/abs/2609.27612v1
- MimicAgent: Quadruped Skills via Prompt-to-Trajectory Generation | 规则：小脑与运动控制 | 模型：大脑与具身智能 | 理由：提示到轨迹生成框架实现四足机器人动态技能学习。 | https://doi.org/10.48550/arxiv.2609.24145
- Vision‐Language‐Action Models for Embodied Artificial Intelligence: A Comprehensive Survey | 规则：大脑与具身智能 | 模型：基础软件与系统 | 理由：论文核心贡献为VLA模型综述，属文献综述而非技术创新 | https://doi.org/10.1002/rob.70340
- Hexapod Locomotion Across Structured and Unstructured Terrains: A Data‐Driven Review of Modeling, Control, and Validation | 规则：小脑与运动控制 | 模型：基础软件与系统 | 理由：题目提出基于五十八研究的六足运动图层架构与分类体系作为新研究输出 | https://doi.org/10.1002/rob.70325
- Efficient Ripeness Monitoring in Open-Facility Environments Using a Quadruped Robot and Panoramic AI Recognition | 规则：感知建图与导航 | 模型：特种应用与产品 | 理由：交付自主巡检型轮腿四足番茄成熟度监测系统，并完成商业温室部署验证 | https://doi.org/10.20944/preprints202608.0999.v1
- Vision-Language-Action and Vision Language Models for Robot Manipulation: A Comprehensive Review Towards Real-World Applications | 规则：大脑与具身智能 | 模型：基础软件与系统 | 理由：综述论文仅提供分类分析，无新模型或系统交付 | https://doi.org/10.20944/preprints202606.0400.v1
- Not What You Asked For: Typographic Attacks in Household Robot Manipulation | 规则：感知建图与导航 | 模型：感知建图与导航 | 理由：提出解耦感知架构维持几何定位并评估文字攻击，主贡献为视觉感知鲁棒性 | https://doi.org/10.48550/arxiv.2605.18593
- Deep Reinforcement Learning for Mobile Robot Navigation in Indoor Environments | 规则：感知建图与导航 | 模型：小脑与运动控制 | 理由：深度强化学习用于室内移动机器人导航，提出了深度强化学习方法实现室内环境下的自主导航决策 | https://doi.org/10.1109/raiie70320.2026.11566902
- Dynamic Legged Ball Manipulation on Rugged Terrains With Hierarchical Reinforcement Learning | 规则：小脑与运动控制 | 模型：大脑与具身智能 | 理由：提出分层强化学习框架并优化高低层技能切换 | https://doi.org/10.1109/lra.2026.3682979
- MoDeSuite: Robot Learning Task Suite for Benchmarking Mobile Manipulation With Deformable Objects | 规则：基础软件与系统 | 模型：基础软件与系统 | 理由：提出可变形物体移动操作的首个标准化基准任务套件，属数据集与基准软件交付物 | https://doi.org/10.1109/lra.2026.3683316
- Collision Prediction and Social-Norm-Fusion-Based Social-Navigation Method for Quadruped Robots | 规则：感知建图与导航 | 模型：大脑与具身智能 | 理由：论文提出基于碰撞预测和社会规范的社会导航模型，属于具身智能领域的任务推理贡献 | https://doi.org/10.3390/biomimetics11040228
- A Review of Fire-Fighting Robots | 规则：感知建图与导航 | 模型：特种应用与产品 | 理由：综述论文没有新算法也没有系统硬件交付物 | https://doi.org/10.56726/irjmets90479
- Comparison of ROS 2 QoS Policies for Real-Time Quadruped Robot Control | 规则：基础软件与系统 | 模型：小脑与运动控制 | 理由：仅对现有质量服务策略进行比较，未提出新控制算法或系统 | https://doi.org/10.1109/infoteh68759.2026.11477650
- Review Paper on Fire Fighting Robot Using Arduino | 规则：感知建图与导航 | 模型：特种应用与产品 | 理由：集成传感器与物联网的自主灭火机器人系统 | https://doi.org/10.55041/ijsrem57649
- SmoothTurn: Learning to Turn Smoothly for Agile Navigation with Quadrupedal Robots | 规则：感知建图与导航 | 模型：小脑与运动控制 | 理由：提出平滑转向学习框架，实现四足机器人敏捷导航中的连续目标切换和动量保持 | https://doi.org/10.48550/arxiv.2603.12842
- Language-Guided Grasping under Partial Observation for Mobile Manipulation in Field Inspection and Maintenance | 规则：小脑与运动控制 | 模型：大脑与具身智能 | 理由：提出部分观测下语言引导机械臂完整抓取流程 | https://doi.org/10.48550/arxiv.2603.07866
- Leveraging Edge Impulse for Multi-Class Error-Related Potentials: Edge AI Brain-Robot Interface for Correcting Navigation Errors in Assistive Mobile Robot Wheelchairs | 规则：感知建图与导航 | 模型：大脑与具身智能 | 理由：提出基于边缘AI的多类错误电位脑机接口，用于校正助行轮椅的导航错误 | https://doi.org/10.1109/icara69401.2026.11480283
- DESIGN AND EXPERIMENT OF MULTI-PUROSE AND MODULAR SENSOR ROBOTIC PLATFORM FOR REAL-TIME ASSESSING AND MONITORING OF CEA FARMS USING POINT CLOUD, LIDAR, RGB AND THERMAL IMAGING | 规则：特种应用与产品 | 模型：特种应用与产品 | 理由：平台设计与CEA农场监测应用混杂，难以确定是硬件机构创新还是集成系统。 | https://doi.org/10.35633/inmateh-77-01
- Prototypes of intelligent robots for first aid in natural disasters: A bibliometric analysis | 规则：特种应用与产品 | 模型：基础软件与系统 | 理由：本文为灾难机器人研究的文献综述，未提出新算法或系统 | https://doi.org/10.31893/multirev.2026304
- Comparative analysis of localization methods for autonomous mobile robots using Robot Operating System 2 | 规则：感知建图与导航 | 模型：小脑与运动控制 | 理由：本文对现有定位方法进行了比较分析但未提出新架构或方法，属于算法评估而非核心贡献 | https://doi.org/10.21439/jme.v8i.122
- The Smallest Impulse-based Firefighting Drone for Rapid Response: Making every second count! | 规则：特种应用与产品 | 模型：硬件与防爆 | 理由：题名指向超小型脉冲消防无人机设计，但摘要未说明结构创新 | https://doi.org/10.1109/ssrr68451.2025.11391279
- SDA-LLM: Spatial DisAmbiguation via Multi-turn Vision-Language Dialogues for Robot Navigation | 规则：感知建图与导航 | 模型：大脑与具身智能 | 理由：提出多轮VLM空间消歧对话提升导航理解能力 | https://doi.org/10.1109/iros60139.2025.11246115
- Uncertainty-Aware Autonomous Robotic Inspection Based on Active Vision and Deep Reinforcement Learning | 规则：小脑与运动控制 | 模型：感知建图与导航 | 理由：提出不确定性引导动态视角选择并融合多时刻预测，属视觉感知方法。 | https://doi.org/10.12783/shm2025/37531
- Multi-layer robotic controller for enhancing the safety of mobile robot navigation in human-centered indoor environments | 规则：感知建图与导航 | 模型：小脑与运动控制 | 理由：提出多层次导航系统，室内机器人安全导航核心贡献，属于动作-政策学习。 | https://doi.org/10.3389/frobt.2025.1629931
- Development and Testing of an Autonomous Mobile Robot for Material Handling Using SLAM and Nav2 | 规则：感知建图与导航 | 模型：特种应用与产品 | 理由：开发集成SLAM和Nav2的物料搬运自主移动机器人系统并进行测试验证 | https://doi.org/10.30880/jamea.2025.06.01.003
- Smart Wireless Power Transfer: A Review of Integrating AI and Sensing for Next-Generation Robotic and IoT Systems | 规则：特种应用与产品 | 模型：硬件与防爆 | 理由：论文综述融合AI与传感的智能无线充电系统，核心在于线圈结构设计与硬件能量传输优化。 | https://doi.org/10.20944/preprints202506.2021.v1
- NaVILA: Legged Robot Vision-Language-Action Model for Navigation | 规则：大脑与具身智能 | 模型：感知建图与导航 | 理由：仅有标题和会议来源，缺少摘要，无法判断是新模型架构还是导航应用。 | https://doi.org/10.15607/rss.2025.xxi.018
- M2CS: A Multimodal and Campus‐Scapes Dataset for Dynamic SLAM and Moving Object Perception | 规则：基础软件与系统 | 模型：感知建图与导航 | 理由：该论文提出M2CS多模态数据集，包含动态SLAM与移动物体感知，属于感知建图与导航创新。 | https://doi.org/10.1002/rob.22468
- Automated system of scaffold point cloud data acquisition using a robot dog | 规则：特种应用与产品 | 模型：基础软件与系统 | 理由：系统实现自动化点云获取，属于软件工具交付，证据充分 | https://doi.org/10.1016/j.autcon.2024.105944
- Review of Self-Learning Systems Based on End-to-End Deep Learning in Bionic Robots | 规则：小脑与运动控制 | 模型：大脑与具身智能 | 理由：综述自学系统在仿生机器人中的应用，未提出新方法，仅回顾现有工作 | https://doi.org/10.54254/2755-2721/97/20241337
- Integration of Various ROS Packages for Autonomous Navigation and Mapping of Mobile Robot | 规则：感知建图与导航 | 模型：基础软件与系统 | 理由：主要交付为ROS包集成导航建图系统，非新算法 | https://doi.org/10.1109/tensymp61132.2024.10752146
- A low-cost robotic system for simultaneous localization and mapping | 规则：感知建图与导航 | 模型：特种应用与产品 | 理由：设计制造低成本移动机器人平台，集成Kinect和树莓派实现室内SLAM | https://doi.org/10.1186/s44147-024-00486-8
- Recent advances in Rapidly-exploring random tree: A review | 规则：感知建图与导航 | 模型：大脑与具身智能 | 理由：对快速探索随机树(RRT)算法进行系统性综述，涵盖理论改进与应用场景 | https://doi.org/10.1016/j.heliyon.2024.e32451
- Color-Based Image Processing for Autonomous Human Following Trolley Robot Navigation with Camera Vision | 规则：感知建图与导航 | 模型：特种应用与产品 | 理由：描述一种基于颜色识别的自主跟随人推车机器人系统，具备完整集成的应用成果 | https://doi.org/10.36596/jcse.v5i1.727
- Research on the Intelligent System Architecture and Control Strategy of Mining Robot Crowds | 规则：小脑与运动控制 | 模型：感知建图与导航 | 理由：元数据仅描述智能系统架构和控制策略，未明确具体感知或导航输出，需审查 | https://doi.org/10.3390/en17081834
- Advanced Pipeline Inspection Robot Development Utilizing Non-Destructive Evaluation and Simulated with Verilog | 规则：特种应用与产品 | 模型：硬件与防爆 | 理由：管道检查机器人设计创新，结合非破坏性评估实现硬件实现 | https://doi.org/10.2139/ssrn.4894242
- Distribution Station Inspection Robot with Modular Manipulator | 规则：特种应用与产品 | 模型：硬件与防爆 | 理由：模块化操作臂提升检查灵活性，体现硬件机制创新 | https://doi.org/10.2139/ssrn.4873574
- Improved Fault Diagnosis of Legged Robot Actuators Based on Feature Interaction-Aware LightGBM | 规则：小脑与运动控制 | 模型：硬件与防爆 | 理由：提出特征交互感知LightGBM方法用于机器人执行器故障诊断，属于硬件诊断技术。 | https://doi.org/10.64972/jaat.2023v1.306p20e:269-280
- Automated assessment for grinding spots on aircraft landing gear components using robotic white light interferometry | 规则：特种应用与产品 | 模型：感知建图与导航 | 理由：标题提出使用白光干涉评估磨削点未公开新感知算法细节 | https://doi.org/10.1117/12.2673757
- Cable management design for Inspection Robot | 规则：硬件与防爆 | 模型：特种应用与产品 | 理由：摘要仅含标题，未描述具体技术贡献，无法确定研究输出 | https://doi.org/10.2172/1997106
- Advances in Robotic Welding for Metallic Materials: Application of Inspection, Modeling, Monitoring and Automation Techniques | 规则：特种应用与产品 | 模型：小脑与运动控制 | 理由：主要产出为焊接技术综述，未给出新的控制方法 | https://doi.org/10.3390/met13040711
- Rescue and Firefighting Operations During Incidents Involving Vehicles with Alternative Propulsion. Electric Vehicles | 规则：特种应用与产品 | 模型：感知建图与导航 | 理由：仅是对电动车辆救援风险的综述，未提出新方法或具体成果 | https://doi.org/10.12845/sft.60.2.2022.1
- Offline Reinforcement Learning for Visual Navigation | 规则：感知建图与导航 | 模型：小脑与运动控制 | 理由：提出ReViND离线RL系统，实现视觉导航任务的奖励函数优化。 | https://doi.org/10.48550/arxiv.2212.08244
- Design and Motion Planning of a Metamorphic Flipping Robot | 规则：小脑与运动控制 | 模型：硬件与防爆 | 理由：提出柔性腰部可重构腿足机器人设计并规划翻转恢复步态 | https://doi.org/10.3390/act11120344
- Overhead transmission line inspection robot control system reliability design | 规则：小脑与运动控制 | 模型：特种应用与产品 | 理由：针对输电线路检测机器人提出控制系统可靠性设计，属特种应用产品 | https://doi.org/10.1109/iccasit55263.2022.9986844
- Navigation System of Coal Mine Rescue Robot Based on Virtual Reality Technology | 规则：感知建图与导航 | 模型：特种应用与产品 | 理由：基于虚拟现实技术的煤矿救援机器人导航系统方案 | https://doi.org/10.23919/wac55640.2022.9934676
- Design and Development of Internal Pipe Inspection Robot | 规则：特种应用与产品 | 模型：硬件与防爆 | 理由：仅凭标题无法区分是硬件机构设计还是完整检测系统，两类均可能。 | https://doi.org/10.24321/2454.8650.202202
- Bio-Inspired Autonomous Learning Algorithm With Application to Mobile Robot Obstacle Avoidance | 规则：感知建图与导航 | 模型：小脑与运动控制 | 理由：提出新的奖励生成机制和基于SNN的自主学习算法，用于移动机器人障碍避免 | https://doi.org/10.3389/fnins.2022.905596
- Path Planning and Obstacle Avoidance using ROS | 规则：感知建图与导航 | 模型：小脑与运动控制 | 理由：实现了基于ROS的路径规划与障碍物规避原型系统，属于动作-政策学习与导航控制核心贡献。 | https://doi.org/10.5281/zenodo.6716576
- Inspection Robot Design for Underwater Structure in Complex Flow Environment | 规则：特种应用与产品 | 模型：硬件与防爆 | 理由：针对复杂水流环境设计了一种新型水下巡检机器人 | https://doi.org/10.1109/icosr57188.2022.00043
- A Massively Parallel Implementation of Gaussian Process Regression for Real Time Bathymetric Modeling and Simultaneous Localization and Mapping | 规则：感知建图与导航 | 模型：基础软件与系统 | 理由：大规模并行高斯过程回归实现实时水深建图与SLAM | https://doi.org/10.55417/fr.2022031
- Design and Development of Tank Cleaning and Inspection Robot | 规则：特种应用与产品 | 模型：硬件与防爆 | 理由：开发了适用于化工储罐清洗巡检的机器人整机设计与控制策略。 | https://doi.org/10.47750/pnr.2022.13.s03.156
- A Mobile Sensing System for Future Gas Mapping in Confined Space Using an Olfactory Quadruped Robot | 规则：感知建图与导航 | 模型：特种应用与产品 | 理由：提出四足机器人气体预测与建图系统，属于特定场景集成移动感知。 | https://doi.org/10.2139/ssrn.4197688
