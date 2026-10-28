# 全库逐条分类元数据审计

本表对每条已入库资源扫描标题、摘要及现有分类；疑点不等于确证错分。

总资源：1813；出现一项或以上疑点：398。

## 分类数量

- 感知建图与导航: 750
- 小脑与运动控制: 625
- 特种应用与产品: 145
- 硬件与防爆: 122
- 基础软件与系统: 98
- 大脑与具身智能: 73

## 疑点分布

- EXISTING_REVIEW: 226
- THIN_ABSTRACT: 171
- HW_NO_EVIDENCE: 18
- SOFT_ALGORITHM: 3
- NAV_AGENT_REVIEW: 2
- BRAIN_POLICY_REVIEW: 1
- HW_ALGORITHM: 1
- APP_ALGORITHM: 1

## 重点疑点逐篇示例

### EXISTING_REVIEW（226 条）
- ohho-robotics/ohho-os | 当前：特种应用与产品 | 建议：待复核 | https://github.com/ohho-robotics/ohho-os
- yuzhen-song/hand_locomotion | 当前：小脑与运动控制 | 建议：待复核 | https://github.com/yuzhen-song/hand_locomotion
- rokbenko/quackd | 当前：基础软件与系统 | 建议：待复核 | https://github.com/rokbenko/quackd
- Autonomous Pallet Jack Project – An Ongoing Robotics Project | 当前：感知建图与导航 | 建议：待复核 | https://discourse.openrobotics.org/t/autonomous-pallet-jack-project-an-ongoing-robotics-project/59254
- ThinkLocoManip: A Whole-Body Control Agentic Harness for Legged Loco-Manipulation | 当前：大脑与具身智能 | 建议：小脑与运动控制（待复核）；待复核 | https://arxiv.org/abs/2610.34370
- T-ConSG: A LiDAR-Based Real-Time Temporal Construction Scene Graph for Dynamic and Evolving Environments | 当前：感知建图与导航 | 建议：待复核 | https://arxiv.org/abs/2610.34041
- RoboReason: Boosting Robotics-Relevant VLM Reasoning Through Scalable Data Generation | 当前：大脑与具身智能 | 建议：待复核 | https://arxiv.org/abs/2610.33778
- RobotAgentBench: Towards Open-world Robot Autonomy | 当前：小脑与运动控制 | 建议：待复核 | https://arxiv.org/abs/2610.34649
- RoboJev: An Open Vision-Language Judge for Robot Success Detection | 当前：感知建图与导航 | 建议：待复核 | https://arxiv.org/abs/2610.33718
- PushAround: Collaborative Path Clearing via Physics-Informed Hybrid Search | 当前：感知建图与导航 | 建议：待复核 | https://arxiv.org/abs/2610.35062
- Continuous-Time Safe Planning and Control for Agile Quadrupeds | 当前：感知建图与导航 | 建议：待复核 | https://arxiv.org/abs/2610.35670
- A Shared Control Framework for Mobile Robots with Planning-Level Intention Prediction | 当前：小脑与运动控制 | 建议：待复核 | https://arxiv.org/abs/2511.08912
### THIN_ABSTRACT（171 条）
- coverMoon/quadruped_control | 当前：小脑与运动控制 | 建议：待复核 | https://github.com/coverMoon/quadruped_control
- 1ulone/quins_ros2 | 当前：基础软件与系统 | 建议：待复核 | https://github.com/1ulone/quins_ros2
- Gait-Aware Command Timing for Decentralized Quadruped Swarms | 当前：小脑与运动控制 | 建议：待复核 | https://doi.org/10.21203/rs.3.rs-11332226/v1
- bell-ha/visually-impaired-navigation-robot | 当前：感知建图与导航 | 建议：待复核 | https://github.com/bell-ha/visually-impaired-navigation-robot
- HAVEN: A unified monocular RGB vision-and-language navigation framework for wheeled-legged robots | 当前：感知建图与导航 | 建议：待复核 | https://doi.org/10.1016/j.displa.2026.103724
- Design of YOLOv8-SLAM Robot Path Planning Method for Outdoor Complex Environments | 当前：感知建图与导航 | 建议：待复核 | https://doi.org/10.21203/rs.3.rs-10726549/v1
- Terrain-Aware Convex Feasible Region Planning for Robust Wheeled-Legged Locomotion | 当前：小脑与运动控制 | 建议：待复核 | https://doi.org/10.21203/rs.3.rs-10577407/v1
- Deep Reinforcement Learning for Quadruped Locomotion Controlled by Natural Language | 当前：小脑与运动控制 | 建议：待复核 | https://doi.org/10.21203/rs.3.rs-10704583/v1
- H-VLN: hierarchical visual-language adaptive navigation control framework for wheel-legged robots | 当前：感知建图与导航 | 建议：待复核 | https://doi.org/10.1016/j.displa.2026.103512
- Adaptive fuzzy-learning control with multi-objective optimization for robust mobile robot navigation | 当前：感知建图与导航 | 建议：待复核 | https://doi.org/10.1016/j.array.2026.101053
- MAXIMAL X-PROJECTION OF CHUA ATTRACTORS: THEORY AND MOBILE ROBOT NAVIGATION APPLICATIONS | 当前：感知建图与导航 | 建议：待复核 | https://doi.org/10.1007/s10958-026-08613-x
- Constrained-Axis Visual-Inertial Odometry for Mobile Robot Displacement Logging Using Commodity Mobile Devices | 当前：感知建图与导航 | 建议：待复核 | https://doi.org/10.21203/rs.3.rs-10175959/v1
### HW_NO_EVIDENCE（18 条）
- A Soft Worm Robot for Sub-Centimeter Scale Pipeline Inspection | 当前：硬件与防爆 | 建议：待复核 | https://doi.org/10.1109/lra.2026.3699247
- CAD-based Optimization of the Medium-sized Unmanned Ground Vehicle | 当前：硬件与防爆 | 建议：待复核 | https://doi.org/10.18372/1990-5548.88.20978
- Research progress in thermal protection materials and technologies for firefighting robots | 当前：硬件与防爆 | 建议：待复核 | https://doi.org/10.11868/j.issn.1001-4381.2025.000330
- Development of a Leg-Wheel Quadruped Robot | 当前：硬件与防爆 | 建议：待复核 | https://doi.org/10.17587/mau.26.588-593
- Development and Experimental Validation of a Novel Quadruped Robot with a Versatile Robotic Tail | 当前：硬件与防爆 | 建议：待复核 | https://doi.org/10.36227/techrxiv.176127306.69222504/v1
- Design and Dynamic Modeling of a Flying Cable Inspection Robot | 当前：硬件与防爆 | 建议：待复核 | https://doi.org/10.1109/cac67268.2025.11486703
- Lightweight structure of superheater pipe inspection robot | 当前：硬件与防爆 | 建议：待复核 | https://doi.org/10.1117/12.3080460
- Small Modular Magnetic-Wheel-Type Wall- Climbing Inspection Robot | 当前：硬件与防爆 | 建议：待复核 | https://doi.org/10.1109/aeeca65693.2025.00071
- Resonant Inductive Coupling Power Transfer for Mid-Sized Inspection Robot | 当前：硬件与防爆 | 建议：待复核 | https://doi.org/10.32388/j9up4u
- Research on the overturning phenomenon of firefighting and rescue crawler robots when climbing up and down stairs | 当前：硬件与防爆 | 建议：待复核 | https://doi.org/10.1007/s41315-024-00394-3
- PaTS-Wheel: A Passively-Transformable Single-Part Wheel for Mobile Robot Navigation on Unstructured Terrain | 当前：硬件与防爆 | 建议：小脑与运动控制/感知建图与导航；待复核 | https://doi.org/10.1109/lra.2024.3389828
- A Mobile Inspection Robot Design Analysis in ANSYS Simulation for Extreme Weather Conditions | 当前：硬件与防爆 | 建议：待复核 | https://doi.org/10.1109/iccma59762.2023.10375060
### SOFT_ALGORITHM（3 条）
- 42 Gazebo Harmonic Simulation Worlds for Navigation, Exploration and SLAM workflows | 当前：基础软件与系统 | 建议：感知导航/小脑 | https://discourse.openrobotics.org/t/42-gazebo-harmonic-simulation-worlds-for-navigation-exploration-and-slam-workflows/58934
- SLAMs for Quadruped Robot: Mapping Capability-centric Agentic Simulation | 当前：基础软件与系统 | 建议：感知导航/小脑 | https://doi.org/10.21203/rs.3.rs-7367448/v1
- Principles and Guidelines for Evaluating Social Robot Navigation Algorithms | 当前：基础软件与系统 | 建议：感知导航/小脑；待复核 | https://doi.org/10.1145/3700599
### NAV_AGENT_REVIEW（2 条）
- Verifier-Mediated Multi-LLM Coordination for Multi-Robot Path Planning | 当前：感知建图与导航 | 建议：大脑与具身智能（待复核） | https://arxiv.org/abs/2610.12761
- Self-Organizing Memory Based on Adaptive Resonance Theory for Vision and Language Navigation | 当前：感知建图与导航 | 建议：大脑与具身智能（待复核） | https://doi.org/10.3390/math11194192
### BRAIN_POLICY_REVIEW（1 条）
- ThinkLocoManip: A Whole-Body Control Agentic Harness for Legged Loco-Manipulation | 当前：大脑与具身智能 | 建议：小脑与运动控制（待复核）；待复核 | https://arxiv.org/abs/2610.34370
### HW_ALGORITHM（1 条）
- PaTS-Wheel: A Passively-Transformable Single-Part Wheel for Mobile Robot Navigation on Unstructured Terrain | 当前：硬件与防爆 | 建议：小脑与运动控制/感知建图与导航；待复核 | https://doi.org/10.1109/lra.2024.3389828
### APP_ALGORITHM（1 条）
- Inspection Robot of Industrial Park Plant Based on Deep Learning | 当前：特种应用与产品 | 建议：具体算法主类 | https://doi.org/10.25236/ajets.2024.070215
