# 高置信度规则分类交叉检查

仅对当前规则高置信度且未由人工/模型确认的条目检查；疑点不等于确证错分。

- 参与范围：1144
- 发现冲突资源：3

## 分类冲突分布
- 大脑与具身智能: 1
- 小脑与运动控制: 1
- 感知建图与导航: 1

## 具体疑点
### Simultaneous Localization and Mapping Methods for Snake-like Robots Based on Gait Adjustment
- 地址：https://doi.org/10.3390/biomimetics9110710
- 规则主分类：小脑与运动控制
- 模型审核状态：待复核
- 可能类别：感知建图与导航；冲突：research_goal_vs_method；理由：论文明确以定位建图为研究目标，运动方式可能只是辅助手段

### Benchmark Analysis of Sampling Methods for RRT Path Planning
- 地址：https://doi.org/10.59247/csol.v2i2.132
- 规则主分类：感知建图与导航
- 模型审核状态：待复核
- 可能类别：基础软件与系统；冲突：deliverable_vs_task；理由：题名显示交付数据集、基准或软件框架

### Can an Embodied Agent Find Your “Cat-shaped Mug”? LLM-Based Zero-Shot Object Navigation
- 地址：https://doi.org/10.1109/lra.2023.3346800
- 规则主分类：大脑与具身智能
- 模型审核状态：待复核
- 可能类别：感知建图与导航；冲突：model_name_vs_research_task；理由：研究目标是目标导航或视觉语言导航，不应仅凭Agent/LLM归入大脑

