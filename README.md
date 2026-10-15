# 特种机器人产业技术雷达

这是一个部署在 GitHub Pages 的自动更新资料网站，**收集对象是特种机器人行业技术发展**，而不是所有人工智能、机器人或机电论文。

适用仓库：<https://github.com/754wu/special-robot-radar>

## 网站监测范围

**行业应用**：防爆石化、危险环境、消防救援、矿山/井下、工业与能源巡检、排爆与高风险作业、野外复杂地形。

**技术体系**：

| 分类 | 关注内容 |
|---|---|
| 硬件与防爆 | 关节电机、驱动器、减速器、传感器、机器人本体、防爆结构及防护 |
| 基础软件与系统 | ROS2、实时通信、仿真、端侧计算、机器人软件框架、系统集成 |
| 小脑与运动控制 | 四足/轮足运动控制、RL、MPC、WBC、步态、Sim-to-Real |
| 大脑与具身智能 | VLM、VLA、Agentic VLN、技能/工具调用、长期规划、世界模型 |
| 感知建图与导航 | SLAM、定位、激光雷达、RGB-D、语义地图、自主探索与导航 |
| 特种应用与产品 | 特种机器人整机、工业巡检与救援任务、现场应用 |

网页用 **两个维度** 检索：技术分类 + 关联方式，并可按特种场景、来源类型和关键词筛选。

“特种场景直接相关”表示论文或仓库简介中确有特种任务/场景线索以及机器人或硬件线索；“可迁移的机器人关键技术”表示其机器人技术可能可用于特种机器人，但**未必已经在该场景验证**。

## 数据源和时间限制

- 论文：arXiv API、OpenAlex、Crossref、arXiv RSS。
- 代码：GitHub 仓库搜索。
- 行业软件动态：ROS Discourse RSS。
- 技术资料只使用公开的标题、摘要和仓库简介做**关键词初筛**；未阅读全文，没有鉴定认证证书。
- OpenAlex、Crossref 是学术索引，不代表文章在这些网站发表。
- `industry_watchlist` 只显示厂商人工关注链接；**暂不自动抓取厂商新闻、新品或标准公告**。

`config.json` 默认设置：

```json
"history_months": 60,
"display_limit": 15000,
"max_history_items": 20000,
"arxiv_limit": 100,
"openalex_limit": 70,
"crossref_limit": 30
```

含义：回溯、展示、保留近 **60 个自然月**的资料；网页一次最多展示 **5000 条**；数据库最多保留 **2500 条**。由于日期过滤、关键词筛选、去重、返回数量限制和源站限流，**不保证采满 5000 条，也不保证这五年每一篇论文都被找出**。GitHub 的日期是仓库最近推送日期，不是创建日期。

## 修改研究范围

大多数时候只需要修改 `config.json`：

- `focus.special_scenarios`：你关注的特种行业场景及关键词；
- `focus.robot_terms`、`focus.platform_terms`：机器人平台线索；
- `focus.native_robot_technologies`：机器人专属的算法或系统线索；
- `focus.robot_component_terms`：机器人硬件线索；
- `focus.min_relevance_score`：筛选门槛（默认 55）；提高门槛会减少误收录，也可能漏检；
- `arxiv_queries` / `openalex_queries` / `crossref_queries` / `github_queries`：采集阶段使用的检索语句。

`main.py` 中的 `KEYWORDS` 是六大技术分类所用词库。如果增加新的技术板块需要修改这里。当前不会直接采集普通网页形式的 IEEE / OpenReview / 企业官网数据，不能将这些普通 URL 当成 RSS 填入配置。

## 更新现有仓库：推荐覆盖包

只用 **`robot_radar_special_industry_update.zip`**，它包含从你 GitHub 现有早期版本直接升级到“半年 + 500 条 + 特种机器人行业筛选”的全部必要文件，**不含 `docs/` 目录**。

将压缩包下载到 `~/Downloads` 后，在 Ubuntu 执行：

```bash
cd ~/project/robot_radar_github_pages_v2
unzip -o ~/Downloads/robot_radar_special_industry_update.zip -d .

git status
git add main.py config.json requirements.txt README.md .env.example .github/workflows/update-radar.yml tests/test_radar.py
git commit -m "Focus radar on special robotics industry and six-month papers"
git push origin main
```

程序升级时不覆盖 `docs/items.json`。下一次 GitHub Actions 运行会**根据新的规则重新筛选现有资料**，自动清理不相关旧记录。如果已经手动修改过程序，请先用 `git diff` 检查再覆盖。

Pages 的 Source 继续保持 **GitHub Actions**；工作流会在 `main` 分支 push 或定时触发。

网站地址：<https://754wu.github.io/special-robot-radar/>

## 本地校验（可选）

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m unittest discover -s tests -v
python main.py --offline  # 仅用已有 docs/items.json 重新筛选和生成网页，不联网
python main.py            # 在线采集，受网络和接口限流影响
python -m http.server 8000 --directory docs
```

访问 <http://localhost:8000>。**在本地跑 `--offline` 会改写本地 `docs/`，如果只想对比代码，最好先备份这些文件。**

## 数据源限流与降级运行

- arXiv 的历史检索 API 经常对 GitHub Actions 共享出口 IP 返回 HTTP 429。
  为避免每天连续发起 10 次不可成功的请求，默认关闭这一路历史回填（`arxiv_queries_per_run: 0`），
  **但保留 arXiv Robotics/CV RSS、OpenAlex、Crossref、ROS Discourse 和 GitHub 的每日采集**。
- 需要主动补充某段时间的 arXiv 历史数据时，可把 `config.json` 的
  `arxiv_queries_per_run` 改为 `1`，每天轮换一个查询；遇到 429 则停止后续 arXiv 历史请求。
- OpenAlex 的 5xx 网关故障和短暂网络错误会进行有限次数重试，遇到不可安全重试的
  429 / 长时间 Retry-After 则尊重限流，不进行密集重试。
- 第三方接口**无法保证 100% 永不超时或限流**。一次采集部分失败时仍会保留
  `docs/items.json` 中的历史资料；网站使用可折叠提示，明细保存在 `docs/weekly.md`，
  而非用红色警告遮挡页面。

## API 和安全性

- 无需大模型 API Key，即可实现自动采集、关键词分类和发布。
- OpenAlex 可选密钥 `OPENALEX_API_KEY`；Crossref 可选联系邮箱 `RADAR_CONTACT_EMAIL`。参见 `.env.example`。某些 API 可能需要凭据或因限流报错，程序会把失败来源写入 `docs/weekly.md`。
- 大模型分析是可选功能，默认不会因为没有密钥而执行。
- **不要上传真正的 `.env`、API Key、密码或单位内部信息到公开 GitHub 仓库。**
- 自动筛选结果只是行业信息线索，不代表论文实验已验证、产品可用或防爆认证有效。


## 近五年查询与新版网页

- `history_months=24`：自动查询并保留近 60 个月资源。数据源接口每次最多返回部分结果，并非五年内所有论文都能立即全部抓取。
- `display_limit=5000`、`max_history_items=7500`：防止网页仍被旧的 500 条上限截断。
- 页面具有技术领域标签、研究关联方式、类型、场景、搜索词，以及开始/结束日期（包含两端）的组合筛选。
- “近 30 天 / 近 6 个月 / 近 1 年 / 全部五年”快捷筛选只是前端选择已采集数据的时间范围，不会让浏览器实时调用外部学术 API。
- 历史补录：每天额外发起少量 OpenAlex 和 Crossref 的分季度查询（对应 `openalex_backfill_per_run` 和 `crossref_backfill_per_run`），逐步补足因每次请求返回上限造成的早期空白。
- 默认仍不会密集访问 arXiv 历史 API（避免曾出现的 HTTP 429）；arXiv RSS 保持启用。


## 分类准确性更新

采用标题优先、摘要辅助的研究主贡献分类；仅提及 LiDAR、sensor、actuator、joint 不足以进入“硬件与防爆”；必须有防爆结构、机械机构、电机或执行器设计的明确技术证据。所有既有库存每日重新分类；LLM 提议仅供参考，不得覆盖主分类。关键词初筛仍不能代替全文人工核验。


## 硬件与防爆召回率专项修复

数据库存在少量硬件论文被归入软件、运动控制或特种应用的情况；仅 5 条不代表五年内只有 5 篇。新增真实样本回归测试，加强隔爆腔体、正压通风、关节执行器、电机与机械结构分类；同时保持 RL/SLAM 等算法论文不被“sensor/actuator”背景用词误导。添加 OpenAlex/Crossref 的硬件定向检索，并按日轮换与分季度补录，以控制请求数量。下一轮发布会重新分类既有记录，五年历史文章需逐步补齐。


## 年份覆盖核验与分页

网页公布各年份真实入库量（按发表或仓库更新日期），不能把近五年检索窗口误解为已完全覆盖五年。历史补录改为按日轮换的年份分层查询，优先修复以往最新结果截断导致的旧论文缺失。每页 10 条，支持首页/上一页/下一页/尾页及指定页码（回车或点击前往），筛选后自动回到第 1 页。


## 历史资料恢复机制（2021—2025）

历史查询已独立为 `backfill.py`，默认每天在 `Recover Five-Year Archive` 工作流中执行。按照检索词 × 半年度窗口分别采集，成功后将检查点持久化到 `docs/backfill_progress.json`，报告保存至 `docs/backfill_report.md`。源站报限流则跳过该源剩余查询，并在下一次运行后恢复。不同年份的资源数量并不意味着每年发文量相同；只有成功的查询会标记完成。可在 Actions 中手动触发此工作流加快初次回填，但不应频繁运行，以免被 API 限流。
