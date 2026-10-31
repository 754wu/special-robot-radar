# 免费大模型辅助分类审核

分类冲突时暂用模型类别并进入二次复核；分类一致则记录已审核、不再重复抽查。

- 规则分类资源：1921
- 具有当前分类版本模型建议：318
- 本次新增建议：62
- 当日新增待复核候选：12
- 历史待复核候选：27
- 本次应用审核建议：62
- 本次新增独立审核事件：62
- 累计历史审核事件（去重）：712
- 累计涉及不同资源：487
- 本次实际改变主分类：23
- 本次API调用次数：28
- 今日累计API调用次数（北京时间）：28/40
- 今日P4抽查API调用次数（北京时间）：14/20
- 本次理论最大审核数：84
- 本次有效输出率：73.8%
- 固定免费模型：openrouter/free
- 规则与模型主分类不一致：42

## 失败原因统计

- invalid_fields: 6
- invalid_review_flag: 2
- missing_or_invalid_batch_items: 6
- output_truncated: 1

## 安全诊断（不含模型原文）

- {"error": "output_truncated", "shape": "empty", "length": 0, "finish_reason": "length", "served_model": "poolside/laguna-xs-2.1:free"}

## 本次分类修改

- Survey: where does your time go between laptop and robot? (3 min, results shared back): 特种应用与产品 -> 基础软件与系统
- Huzaifa-Rahim-Malik/12-DOF-Quadrupled-Dog: 小脑与运动控制 -> 小脑与运动控制
- Modeling and simulation of obstacle detection for a mobile robot: 基础软件与系统 -> 感知建图与导航
- Head of Engineering (robotics, controls, hardware) at Arculus Solutions, Alexandria VA, on-site: 特种应用与产品 -> 特种应用与产品
- ROS 2 GUI Installer – Making ROS 2 Setup Easier for Beginners: 基础软件与系统 -> 基础软件与系统
- yuzhen-song/hand_locomotion: 小脑与运动控制 -> 小脑与运动控制
- ohho-robotics/ohho-os: 特种应用与产品 -> 基础软件与系统
- Remember Where You Walk: Learning Spatial Memory for End-to-End Legged Robot Exploration: 感知建图与导航 -> 感知建图与导航
- RoboSTD: Zero-Shot Single-to-Dual Transfer via Sagittal Mirroring for Bimanual Learning: 小脑与运动控制 -> 小脑与运动控制
- Ego-CEVR: Learning Cross-Embodiment Visual Representations from Human Egocentric Videos: 小脑与运动控制 -> 大脑与具身智能
- Which Hand Was Late? Diagnosis for Robot Failure Recovery in Bimanual Tool Use: 大脑与具身智能 -> 感知建图与导航
- CLEAR-IR: Clarity-Enhanced Active Reconstruction of Infrared Imagery: 感知建图与导航 -> 感知建图与导航
- RobotAgentBench: Towards Open-world Robot Autonomy: 小脑与运动控制 -> 基础软件与系统
- PushAround: Collaborative Path Clearing via Physics-Informed Hybrid Search: 感知建图与导航 -> 小脑与运动控制
- Continuous-Time Safe Planning and Control for Agile Quadrupeds: 感知建图与导航 -> 小脑与运动控制
- Testing the slam_toolbox multi-robot node with Nav2 on three TurtleBot3 Burgers (Jazzy): 感知建图与导航 -> 感知建图与导航
- Founding Robotics Engineer - Subsea: 感知建图与导航 -> 感知建图与导航
- We made a new ROS robot: Mini Pupper 4: 特种应用与产品 -> 硬件与防爆
- batchplan: batched motion planning for ROS 2, with a MoveIt plugin: 基础软件与系统 -> 小脑与运动控制
- From Tabletop to Walking Bot: Deploying a VLA Model on a Legged Manipulator Robot: 大脑与具身智能 -> 大脑与具身智能
- An untethered sub-gram flapping-wing flight system achieves sustained self-stabilizing and altitude-controlled flight: 特种应用与产品 -> 硬件与防爆
- Belief-Overlap Partial Inversion: Object-Centric Flow Replanning for Humanoid Loco-Manipulation: 小脑与运动控制 -> 小脑与运动控制
- Velocity-scaled safe artificial potential field for mobile robot navigation in dynamic environments: 感知建图与导航 -> 感知建图与导航
- Unlocking fast robotic locomotor propulsion through dynamic spine-leg synergy: 小脑与运动控制 -> 小脑与运动控制
- MimicAgent: Quadruped Skills via Prompt-to-Trajectory Generation: 小脑与运动控制 -> 大脑与具身智能
- Exploring Nonlinear Body Oscillations for Natural Quadruped Gaits: 小脑与运动控制 -> 小脑与运动控制
- A Novel Paddling Propulsion Gait for a Wheel-Legged Robot on Sand Terrain: 小脑与运动控制 -> 小脑与运动控制
- DeCoNav: Dialog enhanced Long-Horizon Collaborative Vision-Language Navigation: 大脑与具身智能 -> 感知建图与导航
- SmoothTurn: Learning to Turn Smoothly for Agile Navigation with Quadrupedal Robots: 感知建图与导航 -> 小脑与运动控制
- Discovering Self-Protective Falling Policy for Humanoid Robot via Deep Reinforcement Learning: 小脑与运动控制 -> 小脑与运动控制
- Inspection Robot Path Planning Optimization Algorithm: 感知建图与导航 -> 感知建图与导航
- Motion Control Methods for Dual Wheel-Legged Robot: 小脑与运动控制 -> 小脑与运动控制
- Benchmarking Large Language Model Reasoning in Indoor Robot Navigation: 感知建图与导航 -> 基础软件与系统
- Uni-NaVid: A Video-based Vision-Language-Action Model for Unifying Embodied Navigation Tasks: 大脑与具身智能 -> 感知建图与导航
- Wheel-Legged SLAM: Indoor LiDAR-Inertial SLAM Integrating Kinematic Model of Wheel-Legged Robots: 感知建图与导航 -> 感知建图与导航
- Motion control study of omnidirectional mobile robot for substation inspection: 小脑与运动控制 -> 小脑与运动控制
- Mobile crawler robot for seed sowing and route planning through neuro-diffuse control: 感知建图与导航 -> 小脑与运动控制
- Design of ROS Robot Tracing Navigation Control System Based on Virtual Navigation Paths: 感知建图与导航 -> 感知建图与导航
- Benchmarking SLAM Algorithms in the Cloud: The SLAM Hive Benchmarking Suite: 感知建图与导航 -> 基础软件与系统
- The integration of GPS and visual navigation for autonomous navigation of an Ackerman steering mobile robot in cotton fields: 感知建图与导航 -> 感知建图与导航
- Development and Evaluation of a Computer Vision System for Robot Navigation and Object Recognition in Real-World Environments: 感知建图与导航 -> 感知建图与导航
- Kinematic Analysis and Application to Control Logic Development for RHex Robot Locomotion: 小脑与运动控制 -> 小脑与运动控制
- Autonomous Robotics with Vision-Language AI for Industrial Inspection and Maintenance: 感知建图与导航 -> 基础软件与系统
- LiDAR-Based Object Recognition for Robotic Inspection of Power Lines: 感知建图与导航 -> 感知建图与导航
- Design and Development of swarm AGV’s alliance for Search and Rescue operations: 特种应用与产品 -> 特种应用与产品
- Fast Lidar Inertial Odometry and Mapping for Mobile Robot SE(2) Navigation: 感知建图与导航 -> 感知建图与导航
- Deep Learning Vision System for Quadruped Robot Gait Pattern Regulation: 小脑与运动控制 -> 小脑与运动控制
- ACCURACY AND PRECISION OF AN INDOOR AUTONOMOUS MOBILE ROBOT LOCALIZATION UTILIZING A RFID READER MFRC522: 感知建图与导航 -> 感知建图与导航
- Elements needed to implement the Obstacle-Avoidance Robots: 感知建图与导航 -> 感知建图与导航
- Advances in Robotic Welding for Metallic Materials: Application of Inspection, Modeling, Monitoring and Automation Techniques: 小脑与运动控制 -> 特种应用与产品
- A General Relationship Between Optimality Criteria and Connectivity Indices for Active Graph-SLAM: 感知建图与导航 -> 感知建图与导航
- Development of a Low-Cost Stationary Laser Scanning System for Generation of Building Information Models: 基础软件与系统 -> 硬件与防爆
- G-ROBOT: An Intelligent Greenhouse Seedling Height Inspection Robot: 特种应用与产品 -> 特种应用与产品
- Convolutional Auto-Encoder and Independent Component Analysis Based Automatic Place Recognition for Moving Robot in Invariant Season Condition: 感知建图与导航 -> 感知建图与导航
- Frictional Anisotropic Locomotion and Adaptive Neural Control for a Soft Crawling Robot: 小脑与运动控制 -> 小脑与运动控制
- Design and Simulation of a Mobile Robot for Pipeline Inspection: 硬件与防爆 -> 硬件与防爆
- Intelligent control method of underwater inspection robot in netcage: 特种应用与产品 -> 小脑与运动控制
- Efficient and Safe Robotic Autonomous Environment Exploration Using Integrated Frontier Detection and Multiple Path Evaluation: 感知建图与导航 -> 感知建图与导航
- The Effects of Over-Ground Robot-Assisted Gait Training for Children with Ataxic Cerebral Palsy: A Case Report: 小脑与运动控制 -> 特种应用与产品
- Leg Centroidal Dynamics Based New Locomotion Principle of a Quadruped Robot with On-line Legged Motion Generation: 小脑与运动控制 -> 小脑与运动控制
- Inspection Robotic UGV Platform and the Procedure for an Acoustic Signal-Based Fault Detection in Belt Conveyor Idler: 特种应用与产品 -> 特种应用与产品
- Structural Design, Simulation and Experiment of Quadruped Robot: 硬件与防爆 -> 硬件与防爆

## 分类冲突（前80条）

- Survey: where does your time go between laptop and robot? (3 min, results shared back) | 规则：基础软件与系统 | 模型：基础软件与系统 | 理由：调查工具用于量化软件迁移至机器人中的时间消耗。 | https://discourse.openrobotics.org/t/survey-where-does-your-time-go-between-laptop-and-robot-3-min-results-shared-back/59366
- Modeling and simulation of obstacle detection for a mobile robot | 规则：感知建图与导航 | 模型：感知建图与导航 | 理由：提出了一种混合导航架构，结合PID跟踪与虚拟传感器避障，实现机器人安全导航。属于感知导航。 | https://doi.org/10.3389/fcteg.2026.1928428
- ohho-robotics/ohho-os | 规则：基础软件与系统 | 模型：基础软件与系统 | 理由：提供Python SDK和CLI，实现机器人仿真、遥操控及ROS2接口 | https://github.com/ohho-robotics/ohho-os
- Ego-CEVR: Learning Cross-Embodiment Visual Representations from Human Egocentric Videos | 规则：大脑与具身智能 | 模型：大脑与具身智能 | 理由：提出跨本体视觉表征学习框架，从自我中心视频学习分层视觉表示 | https://arxiv.org/abs/2610.37509
- Which Hand Was Late? Diagnosis for Robot Failure Recovery in Bimanual Tool Use | 规则：感知建图与导航 | 模型：感知建图与导航 | 理由：基于感知通道的双臂故障诊断可辨识性，不属导航检测，证据不足 | https://arxiv.org/abs/2610.37533
- RobotAgentBench: Towards Open-world Robot Autonomy | 规则：基础软件与系统 | 模型：基础软件与系统 | 理由：提供开放世界机器人自主性评测基准及真实-模拟数据集 | https://arxiv.org/abs/2610.34649
- PushAround: Collaborative Path Clearing via Physics-Informed Hybrid Search | 规则：小脑与运动控制 | 模型：小脑与运动控制 | 理由：提出机器人协作清障的有效物理信息混合搜索算法 | https://arxiv.org/abs/2610.35062
- Continuous-Time Safe Planning and Control for Agile Quadrupeds | 规则：小脑与运动控制 | 模型：小脑与运动控制 | 理由：提出四足机器人连续时间安全规划控制框架方法 | https://arxiv.org/abs/2610.35670
- We made a new ROS robot: Mini Pupper 4 | 规则：硬件与防爆 | 模型：硬件与防爆 | 理由：摘要极简，仅提及制作了Mini Pupper 4机器人，无具体科研创新或技术贡献。 | https://discourse.openrobotics.org/t/we-made-a-new-ros-robot-mini-pupper-4/59197
- batchplan: batched motion planning for ROS 2, with a MoveIt plugin | 规则：小脑与运动控制 | 模型：小脑与运动控制 | 理由：提出批量运动规划算法及ROS2插件，实现多姿态IK与路径生成 | https://discourse.openrobotics.org/t/batchplan-batched-motion-planning-for-ros-2-with-a-moveit-plugin/59144
- October CWG Meeting - Deep Venture and ResQ ROV: From COTS to Capability | 规则：特种应用与产品 | 模型：硬件与防爆 | 理由：仅为会议通知，未明确提出新算法、硬件或软件交付物，证据不足。 | https://discourse.openrobotics.org/t/october-cwg-meeting-deep-venture-and-resq-rov-from-cots-to-capability/59056
- An untethered sub-gram flapping-wing flight system achieves sustained self-stabilizing and altitude-controlled flight | 规则：硬件与防爆 | 模型：硬件与防爆 | 理由：设计了一种微重力级别的振动式翼结构，实现高升力与自稳定，属于硬件创新。 | https://doi.org/10.1038/s41467-026-78914-x
- Upcoming ROS 2 Workshop: Building AI Robots with Vision-Language Models and ROS 2 | 规则：基础软件与系统 | 模型：大脑与具身智能 | 理由：研讨会通知，未展示具体的研究输出、算法或系统设计，仅为主题活动预告。 | https://discourse.openrobotics.org/t/upcoming-ros-2-workshop-building-ai-robots-with-vision-language-models-and-ros-2/59032
- MimicAgent: Quadruped Skills via Prompt-to-Trajectory Generation | 规则：大脑与具身智能 | 模型：大脑与具身智能 | 理由：提示到轨迹生成框架实现四足机器人动态技能学习。 | https://doi.org/10.48550/arxiv.2609.24145
- Efficient Ripeness Monitoring in Open-Facility Environments Using a Quadruped Robot and Panoramic AI Recognition | 规则：感知建图与导航 | 模型：特种应用与产品 | 理由：交付自主巡检型轮腿四足番茄成熟度监测系统，并完成商业温室部署验证 | https://doi.org/10.20944/preprints202608.0999.v1
- Vision-Language-Action and Vision Language Models for Robot Manipulation: A Comprehensive Review Towards Real-World Applications | 规则：大脑与具身智能 | 模型：基础软件与系统 | 理由：综述论文仅提供分类分析，无新模型或系统交付 | https://doi.org/10.20944/preprints202606.0400.v1
- DeCoNav: Dialog enhanced Long-Horizon Collaborative Vision-Language Navigation | 规则：感知建图与导航 | 模型：感知建图与导航 | 理由：提出协作长时VLN基准与对话驱动分散框架 | https://doi.org/10.48550/arxiv.2604.12486
- SmoothTurn: Learning to Turn Smoothly for Agile Navigation with Quadrupedal Robots | 规则：小脑与运动控制 | 模型：小脑与运动控制 | 理由：提出平滑转向学习框架，实现四足机器人敏捷导航中的连续目标切换和动量保持 | https://doi.org/10.48550/arxiv.2603.12842
- Prototypes of intelligent robots for first aid in natural disasters: A bibliometric analysis | 规则：特种应用与产品 | 模型：基础软件与系统 | 理由：本文为灾难机器人研究的文献综述，未提出新算法或系统 | https://doi.org/10.31893/multirev.2026304
- Comparative analysis of localization methods for autonomous mobile robots using Robot Operating System 2 | 规则：感知建图与导航 | 模型：小脑与运动控制 | 理由：本文对现有定位方法进行了比较分析但未提出新架构或方法，属于算法评估而非核心贡献 | https://doi.org/10.21439/jme.v8i.122
- The Smallest Impulse-based Firefighting Drone for Rapid Response: Making every second count! | 规则：特种应用与产品 | 模型：硬件与防爆 | 理由：题名指向超小型脉冲消防无人机设计，但摘要未说明结构创新 | https://doi.org/10.1109/ssrr68451.2025.11391279
- Smart Wireless Power Transfer: A Review of Integrating AI and Sensing for Next-Generation Robotic and IoT Systems | 规则：特种应用与产品 | 模型：硬件与防爆 | 理由：论文综述融合AI与传感的智能无线充电系统，核心在于线圈结构设计与硬件能量传输优化。 | https://doi.org/10.20944/preprints202506.2021.v1
- Benchmarking Large Language Model Reasoning in Indoor Robot Navigation | 规则：基础软件与系统 | 模型：基础软件与系统 | 理由：构建室内导航LLM推理基准测试套件，评估推理能力 | https://doi.org/10.1109/siu66497.2025.11111749
- Uni-NaVid: A Video-based Vision-Language-Action Model for Unifying Embodied Navigation Tasks | 规则：感知建图与导航 | 模型：感知建图与导航 | 理由：提出视频基础视觉-语言-动作模型（Uni-NaVid），统一多种具身导航任务的端到端策略学习。 | https://doi.org/10.15607/rss.2025.xxi.013
- Automated system of scaffold point cloud data acquisition using a robot dog | 规则：特种应用与产品 | 模型：基础软件与系统 | 理由：系统实现自动化点云获取，属于软件工具交付，证据充分 | https://doi.org/10.1016/j.autcon.2024.105944
- Review of Self-Learning Systems Based on End-to-End Deep Learning in Bionic Robots | 规则：小脑与运动控制 | 模型：大脑与具身智能 | 理由：综述自学系统在仿生机器人中的应用，未提出新方法，仅回顾现有工作 | https://doi.org/10.54254/2755-2721/97/20241337
- Mobile crawler robot for seed sowing and route planning through neuro-diffuse control | 规则：小脑与运动控制 | 模型：小脑与运动控制 | 理由：基于ANFIS神经模糊控制实现轨迹跟踪纠偏 | https://doi.org/10.22201/icat.24486736e.2024.22.5.2445
- Benchmarking SLAM Algorithms in the Cloud: The SLAM Hive Benchmarking Suite | 规则：基础软件与系统 | 模型：基础软件与系统 | 理由：开源SLAM Hive云端基准测试套件，支持大规模评测 | https://doi.org/10.48550/arxiv.2406.17586
- Advanced Pipeline Inspection Robot Development Utilizing Non-Destructive Evaluation and Simulated with Verilog | 规则：特种应用与产品 | 模型：硬件与防爆 | 理由：管道检查机器人设计创新，结合非破坏性评估实现硬件实现 | https://doi.org/10.2139/ssrn.4894242
- Autonomous Robotics with Vision-Language AI for Industrial Inspection and Maintenance | 规则：基础软件与系统 | 模型：基础软件与系统 | 理由：提出工业巡检维护的自主框架，集成多模态视觉语言人工智能 | https://doi.org/10.67228/30716357/ijmrse-2024pii8t1v
- Distribution Station Inspection Robot with Modular Manipulator | 规则：特种应用与产品 | 模型：硬件与防爆 | 理由：模块化操作臂提升检查灵活性，体现硬件机制创新 | https://doi.org/10.2139/ssrn.4873574
- Advances in Robotic Welding for Metallic Materials: Application of Inspection, Modeling, Monitoring and Automation Techniques | 规则：特种应用与产品 | 模型：特种应用与产品 | 理由：综述焊接机器人检测建模监控自动化进展技术 | https://doi.org/10.3390/met13040711
- Rescue and Firefighting Operations During Incidents Involving Vehicles with Alternative Propulsion. Electric Vehicles | 规则：特种应用与产品 | 模型：感知建图与导航 | 理由：仅是对电动车辆救援风险的综述，未提出新方法或具体成果 | https://doi.org/10.12845/sft.60.2.2022.1
- Development of a Low-Cost Stationary Laser Scanning System for Generation of Building Information Models | 规则：硬件与防爆 | 模型：硬件与防爆 | 理由：开发了一种低成本固定式激光扫描系统，实现3D点云与BIM生成，属于硬件设计。 | https://doi.org/10.5755/j02.eie.31374
- Offline Reinforcement Learning for Visual Navigation | 规则：感知建图与导航 | 模型：小脑与运动控制 | 理由：提出ReViND离线RL系统，实现视觉导航任务的奖励函数优化。 | https://doi.org/10.48550/arxiv.2212.08244
- Design and Motion Planning of a Metamorphic Flipping Robot | 规则：小脑与运动控制 | 模型：硬件与防爆 | 理由：提出柔性腰部可重构腿足机器人设计并规划翻转恢复步态 | https://doi.org/10.3390/act11120344
- Design and Development of Internal Pipe Inspection Robot | 规则：特种应用与产品 | 模型：硬件与防爆 | 理由：仅凭标题无法区分是硬件机构设计还是完整检测系统，两类均可能。 | https://doi.org/10.24321/2454.8650.202202
- Inspection Robot Design for Underwater Structure in Complex Flow Environment | 规则：特种应用与产品 | 模型：硬件与防爆 | 理由：针对复杂水流环境设计了一种新型水下巡检机器人 | https://doi.org/10.1109/icosr57188.2022.00043
- Design and Development of Tank Cleaning and Inspection Robot | 规则：特种应用与产品 | 模型：硬件与防爆 | 理由：开发了适用于化工储罐清洗巡检的机器人整机设计与控制策略。 | https://doi.org/10.47750/pnr.2022.13.s03.156
- Intelligent control method of underwater inspection robot in netcage | 规则：小脑与运动控制 | 模型：小脑与运动控制 | 理由：提供网箱环境下水下巡检机器人的智能控制方法 | https://doi.org/10.1111/are.15721
- The Effects of Over-Ground Robot-Assisted Gait Training for Children with Ataxic Cerebral Palsy: A Case Report | 规则：特种应用与产品 | 模型：特种应用与产品 | 理由：报告RAGT在儿童共济失调CP中的临床疗效，证明其改善运动功能 | https://doi.org/10.3390/s21237875
- A bio-inspired robotic climbing robot to understand kinematic and morphological determinants for an optimal climbing gait | 规则：小脑与运动控制 | 模型：硬件与防爆 | 理由：设计了具有活动脊椎、肩部和爪部的仿生攀爬机器人X4，研究其形态与步态优化。 | https://doi.org/10.1088/1748-3190/ac370f
