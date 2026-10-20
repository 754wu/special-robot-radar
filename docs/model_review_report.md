# 免费大模型辅助分类审核

确定结果可用于改类；不确定则保留规则分类并继续待复核。

- 规则分类资源：1669
- 具有当前分类版本模型建议：23
- 本次新增建议：12
- 当日新增待复核候选：0
- 历史待复核候选：200
- 本次应用审核建议：12
- 本次新增独立审核事件：12
- 累计历史审核事件（去重）：134
- 累计涉及不同资源：124
- 本次实际改变主分类：7
- 本次API调用次数：8
- 本次理论最大审核数：24
- 本次有效输出率：50.0%
- 固定免费模型：openrouter/free
- 规则与模型主分类不一致：8

## 失败原因统计

- TypeError: 1
- invalid_fields: 6
- missing_or_invalid_batch_items: 2
- quota_auth_or_unavailable_model: 1

## 安全诊断（不含模型原文）

- {"error": "TypeError", "shape": "empty", "length": 0, "finish_reason": "None", "served_model": "None"}

## 本次分类修改

- 1ulone/quins_ros2: 特种应用与产品 -> 基础软件与系统
- New packages for Humble Hawksbill 2026-10-12: 特种应用与产品 -> 基础软件与系统
- Autonomous Robotic Systems in Agriculture 5.0: A Review on Technical Architecture, Operational Applications, and Future Perspectives: 特种应用与产品 -> 特种应用与产品
- Path Identification in Multi-Robot Environments Using a Restricted Minimum Spanning Tree Based Motion Strategy: 小脑与运动控制 -> 感知建图与导航
- Design and application of quick-change explosion-proof inspection fire-extinguishing robot: 特种应用与产品 -> 特种应用与产品
- Design and application of intelligent robot for explosion-proof inspection and fire-extinguishing: 特种应用与产品 -> 特种应用与产品
- Edge AI-Based LSTM Voice-Controlled Mobile Robot for Industrial Pipe Inspection: 感知建图与导航 -> 特种应用与产品
- Inchworm-inspired micro-inspection robot: Autonomous design for aero-engine inspection: 特种应用与产品 -> 硬件与防爆
- Tunnel Apparent Disease Inspection Robot Based on Mobile LiDAR: 特种应用与产品 -> 感知建图与导航
- "Wireless Firefighting Robot for Emergency Response: A Critique of its Design, Functionality, and Real-World Application": 特种应用与产品 -> 特种应用与产品
- FireGuardian: A Smart IoT Firefighting Robot for Automated Fire Hazard Mitigation: 特种应用与产品 -> 特种应用与产品
- Design and analysis of AGM explosion proof plug automatic assembly and inspection production line: 特种应用与产品 -> 硬件与防爆

## 分类冲突（前80条）

- 1ulone/quins_ros2 | 规则：基础软件与系统 | 模型：基础软件与系统 | 理由：交付四足机器人ROS源码，属于可复用软件基础设施 | https://github.com/1ulone/quins_ros2
- New packages for Humble Hawksbill 2026-10-12 | 规则：基础软件与系统 | 模型：基础软件与系统 | 理由：发布40个新包及446项更新，形成可复用ROS软件基础设施 | https://discourse.openrobotics.org/t/new-packages-for-humble-hawksbill-2026-10-12/58802
- Efficient Ripeness Monitoring in Open-Facility Environments Using a Quadruped Robot and Panoramic AI Recognition | 规则：感知建图与导航 | 模型：特种应用与产品 | 理由：交付自主巡检型轮腿四足番茄成熟度监测系统，并完成商业温室部署验证 | https://doi.org/10.20944/preprints202608.0999.v1
- Path Identification in Multi-Robot Environments Using a Restricted Minimum Spanning Tree Based Motion Strategy | 规则：感知建图与导航 | 模型：感知建图与导航 | 理由：基于RFID网络提出受限最小生成树运动策略，规划路径并处理机器人碰撞 | https://doi.org/10.15866/ireaco.v19i2.27469
- Edge AI-Based LSTM Voice-Controlled Mobile Robot for Industrial Pipe Inspection | 规则：特种应用与产品 | 模型：特种应用与产品 | 理由：仅见边缘LSTM语音控制工业管道巡检机器人，摘要缺失难以确认主要创新 | https://doi.org/10.1109/icat66432.2025.11189277
- Inchworm-inspired micro-inspection robot: Autonomous design for aero-engine inspection | 规则：硬件与防爆 | 模型：硬件与防爆 | 理由：提出毛毛虫仿生微型巡检机器人本体及自主设计方案 | https://doi.org/10.1016/j.sna.2025.116589
- Tunnel Apparent Disease Inspection Robot Based on Mobile LiDAR | 规则：感知建图与导航 | 模型：感知建图与导航 | 理由：仅表明基于移动激光雷达的隧道病害巡检机器人，具体感知方法与系统贡献不明 | https://doi.org/10.1109/mrai65197.2025.11135693
- Design and analysis of AGM explosion proof plug automatic assembly and inspection production line | 规则：硬件与防爆 | 模型：硬件与防爆 | 理由：提出防爆插塞自动装配检测生产线，并完成产线结构及关键机构设计分析 | https://doi.org/10.1088/1742-6596/2902/1/012002
