# 免费大模型辅助分类审核

确定结果可用于改类；不确定则保留规则分类并继续待复核。

- 规则分类资源：1636
- 具有当前分类版本模型建议：28
- 本次新增建议：6
- 当日新增待复核候选：0
- 历史待复核候选：96
- 本次应用审核建议：6
- 本次新增独立审核事件：6
- 累计历史审核事件（去重）：152
- 累计涉及不同资源：142
- 本次实际改变主分类：3
- 本次API调用次数：4
- 本次理论最大审核数：12
- 本次有效输出率：50.0%
- 固定免费模型：openrouter/free
- 规则与模型主分类不一致：4

## 失败原因统计

- TypeError: 1
- quota_auth_or_unavailable_model: 1

## 安全诊断（不含模型原文）

- {"error": "TypeError", "shape": "empty", "length": 0, "finish_reason": "None", "served_model": "None"}

## 本次分类修改

- DeCoNav: Dialog enhanced Long-Horizon Collaborative Vision-Language Navigation: 大脑与具身智能 -> 大脑与具身智能
- Advances in Robotic Welding for Metallic Materials: Application of Inspection, Modeling, Monitoring and Automation Techniques: 特种应用与产品 -> 小脑与运动控制
- Design and Simulation of a Mobile Robot for Pipeline Inspection: 基础软件与系统 -> 硬件与防爆
- Machine learning techniques for robotic and autonomous inspection of mechanical systems and civil infrastructure: 感知建图与导航 -> 感知建图与导航
- An Aerial/Ground Robot Team for Autonomous Firefighting in Urban GNSS-Denied Scenarios: 特种应用与产品 -> 特种应用与产品
- Design and Implementation of Intelligent EOD System Based on Six-Rotor UAV: 感知建图与导航 -> 特种应用与产品

## 分类冲突（前80条）

- Efficient Ripeness Monitoring in Open-Facility Environments Using a Quadruped Robot and Panoramic AI Recognition | 规则：感知建图与导航 | 模型：特种应用与产品 | 理由：交付自主巡检型轮腿四足番茄成熟度监测系统，并完成商业温室部署验证 | https://doi.org/10.20944/preprints202608.0999.v1
- Advances in Robotic Welding for Metallic Materials: Application of Inspection, Modeling, Monitoring and Automation Techniques | 规则：小脑与运动控制 | 模型：小脑与运动控制 | 理由：主要产出为焊接技术综述，未给出新的控制方法 | https://doi.org/10.3390/met13040711
- Design and Simulation of a Mobile Robot for Pipeline Inspection | 规则：硬件与防爆 | 模型：硬件与防爆 | 理由：仅题名可确认移动机器人设计与仿真，缺少具体硬件创新 | https://doi.org/10.1109/conescapan56456.2022.9959592
- Design and Implementation of Intelligent EOD System Based on Six-Rotor UAV | 规则：特种应用与产品 | 模型：特种应用与产品 | 理由：完成排爆整机集成，并设计绞盘夹持器执行机构 | https://doi.org/10.3390/drones5040146
