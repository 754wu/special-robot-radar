"""Verified high-confidence rule classification corrections from stored abstracts.
Only evidence-supported clear mismatches; not full-text peer review.
"""
BATCH_DECISIONS = {
    "robot learning with vision-language-action models for agricultural manipulation": ("小脑与运动控制", "摘要研究农业场景抓取与到达的VLA动作策略适配和仿真到现实迁移，核心交付为操作策略。"),
    "fastvla: task-conditioned and temporally adaptive visual token compression for efficient vision-language-action models": ("小脑与运动控制", "摘要以闭环VLA操作控制的逐步视觉Token压缩与推理加速为主，未涉及高层任务规划。"),
    "one-shot human video-guided adaptation for vision-language-action models": ("小脑与运动控制", "摘要提出以单段人类视频适配新操作任务的VLA动作策略，主要成果为操作策略迁移。"),
    "g$^3$vla: geometric inductive bias for vision-language-action models": ("小脑与运动控制", "摘要提出相机标定几何增强VLA操作策略的视觉表征，明确保留原有动作学习目标。"),
    "42 gazebo harmonic simulation worlds for navigation, exploration and slam workflows": ("基础软件与系统", "直接交付42个Gazebo及Blender生成的仿真世界和转换工具，用于测试导航SLAM而非提出导航算法。"),
    "implementation of pure pursuit algorithm for nonholonomic mobile robot using robot operating system": ("感知建图与导航", "主要实施并验证基于Pure Pursuit的移动机器人路径跟随算法，ROS和Gazebo只是试验环境。"),
    "implementation of lidar sensor for mobile robot delivery based on robot operating system": ("感知建图与导航", "摘要围绕配送机器人激光雷达感知与导航性能验证，没有通用ROS软件交付。"),
    "make {\\pi}0.5 learn to call astra for reliable robot manipulation": ("大脑与具身智能", "摘要明确提出机器人策略在关键恢复事件自动调用外部推理模型的CALL模块，核心贡献为推理工具调用决策。"),
}
