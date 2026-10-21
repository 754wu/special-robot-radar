"""Verified high-confidence rule classification corrections from stored abstracts.
Only evidence-supported clear mismatches; not full-text peer review.
"""
BATCH_DECISIONS = {
    "robot learning with vision-language-action models for agricultural manipulation": ("小脑与运动控制", "摘要研究农业场景抓取与到达的VLA动作策略适配和仿真到现实迁移，核心交付为操作策略。"),
    "fastvla: task-conditioned and temporally adaptive visual token compression for efficient vision-language-action models": ("大脑与具身智能", "研究任务感知的视觉Token压缩与动态预算分配以优化VLA基础模型推理效率，核心贡献是具身基础模型推理机制而非底层控制器。"),
    "one-shot human video-guided adaptation for vision-language-action models": ("大脑与具身智能", "提出由单段人类视频进行跨任务表征提取和预训练VLA基础模型适配，主要研究基础模型泛化与任务适配机制。"),
    "g$^3$vla: geometric inductive bias for vision-language-action models": ("大脑与具身智能", "利用相机标定、投影位置编码和跨视角融合增强VLA基础模型的空间几何表示，并未改变原动作学习目标。"),
    "42 gazebo harmonic simulation worlds for navigation, exploration and slam workflows": ("基础软件与系统", "直接交付42个Gazebo及Blender生成的仿真世界和转换工具，用于测试导航SLAM而非提出导航算法。"),
    "implementation of pure pursuit algorithm for nonholonomic mobile robot using robot operating system": ("感知建图与导航", "主要实施并验证基于Pure Pursuit的移动机器人路径跟随算法，ROS和Gazebo只是试验环境。"),
    "implementation of lidar sensor for mobile robot delivery based on robot operating system": ("感知建图与导航", "摘要围绕配送机器人激光雷达感知与导航性能验证，没有通用ROS软件交付。"),
    "make {\\pi}0.5 learn to call astra for reliable robot manipulation": ("大脑与具身智能", "摘要明确提出机器人策略在关键恢复事件自动调用外部推理模型的CALL模块，核心贡献为推理工具调用决策。"),
}
