# 特种机器人技术雷达｜每天自动更新的论文 & 项目网站

这是一个可部署到 GitHub Pages 的 **免费、无需服务器、无需大模型 API** 的小型网站。

它每天自动：

1. 从 arXiv（机器人 / 人工智能）、ROS 社区 RSS 采集新内容；
2. 从 GitHub 搜索四足、轮足、运控、SLAM、VLM、Agentic VLN 等开源项目；
3. 自动去重、关键词初筛，按 **硬件 / 小脑 / 导航 / 大脑 / 应用** 分类；
4. 生成 `docs/index.html` 网页、`docs/items.json` 历史记录和 `docs/weekly.md` 七日简报；
5. GitHub Actions 自动提交更新，并发布到 GitHub Pages。

> 注意：本项目当前采集**标题、摘要、代码仓库简介**，没有阅读全文、验证实验或检查防爆认证。源站偶有访问失败、RSS 漏项、GitHub API 限流；不等同于完整的行业数据库。`GitHub pushed_at` 是仓库最近推送时间，不是最早发布日。初版不自动抓取厂商新闻，`industry_watchlist` 仅作为人工链接收藏。

## 0. 只想上线？不用在电脑里运行 Python

你可以**直接按下面第 1–3 节操作**。采集脚本完全交给 GitHub Actions 在云端运行。建议使用 **公开仓库**，GitHub Free 可以发布 GitHub Pages 网站。

## 1. 在 GitHub 新建空仓库

1. 登录 GitHub，打开 https://github.com/new
2. 仓库名称（Repository name）输入：`special-robot-radar`
3. 选 **Public**（公开）。
4. **不要勾选** `Add a README file`、`.gitignore`、License（这些文件已在压缩包中）。
5. 点击 **Create repository**。创建后保留页面，不必复制页面里的示例代码。

## 2. 上传项目代码（Ubuntu 22.04）

在文件管理器中解压项目 zip。打开终端，进入**包含 `main.py` 的那个目录**，例如：

```bash
cd ~/Downloads/special_robot_radar
```

然后执行以下命令：

```bash
git init -b main
git add .
git commit -m "Initial robotics radar website"
git remote add origin https://github.com/你的GitHub用户名/special-robot-radar.git
git push -u origin main
```

请将命令里的 **`你的GitHub用户名`** 换成自己的真实用户名。`git add .` 会把隐藏目录 `.github/workflows/` 一并提交，这是自动更新的关键。

GitHub 不支持直接用账号密码完成 HTTPS Git 推送。如果要求认证，按 Git Credential Manager、GitHub CLI (`gh auth login`) 或个人访问令牌等官方支持方式登录。若提示 `Author identity unknown`，先设置 Git 提交信息：

```bash
git config --global user.name "你的GitHub用户名"
git config --global user.email "你用于GitHub提交的邮箱"
```

重新执行 `git commit` 和 `git push`。

**上传后检查：** GitHub 仓库的 Code 页面中应该能找到 `.github/workflows/update-radar.yml` 文件。如果没有，该仓库就无法自动更新。

## 3. 开启 GitHub Pages，运行首次采集

1. 在仓库页面进入 **Settings → Pages**。
2. 找到 **Build and deployment → Source**，选 **GitHub Actions**（不是 `Deploy from a branch`）。
3. 返回仓库 **Actions**，找到 **Update Special Robot Radar**。
4. 点击 **Run workflow → Run workflow** 手动运行一次；上传到 `main` 也会自动触发一次，如第一次在 Pages 启用前失败，手动再运行即可。
5. 工作流显示绿色 ✅ 且有 `Deploy GitHub Pages` 成功记录后，在 **Settings → Pages** 找到站点网址，通常为：

   `https://你的GitHub用户名.github.io/special-robot-radar/`

6. 打开网址，网页上可以按五大技术方向筛选、按论文/项目筛选，或在搜索框搜索关键词。

### 自动更新时间

- 每天 `01:15 UTC` 运行一次（**北京时间 09:15 / 东京时间 10:15**）；可在 `.github/workflows/update-radar.yml` 修改 `cron`。
- 修改代码并推送到 `main` 也会运行；仅由 Actions 自动推送的 `docs/` 更新不会形成循环运行。
- GitHub 的定时运行不是严格定点，有可能延迟或个别执行被跳过。公开仓库如果 60 天没有活动，定时工作流可能被 GitHub 自动禁用，需要到 Actions 页面重新启用。

### 如果 Actions 报权限不足

工作流已经声明 `contents: write`、`pages: write`、`id-token: write`。如果 `git push` 仍返回 403，请检查仓库 **Settings → Actions → General → Workflow permissions**，以及组织策略、`main` 分支保护规则是否阻止 GitHub Actions 写入。如果 `pages` 部署失败，确认 **Settings → Pages → Source = GitHub Actions**。

无需自己创建 `GITHUB_TOKEN`：GitHub Actions 会自动生成临时 token，代码会用它访问 GitHub 搜索 API。

## 4. 改成你自己感兴趣的机器人方向

在 GitHub 仓库 **Code** 页面打开 `config.json`，点铅笔图标修改，保存（Commit changes）即可启动一轮更新。

```json
{
  "rss": [
    {"name": "arXiv Robotics", "url": "https://rss.arxiv.org/rss/cs.RO"},
    {"name": "arXiv Artificial Intelligence", "url": "https://rss.arxiv.org/rss/cs.AI"},
    {"name": "ROS Discourse", "url": "https://discourse.ros.org/latest.rss"}
  ],
  "github_queries": [
    "quadruped locomotion in:name,description,readme",
    "wheel legged robot in:name,description,readme",
    "robot vision language navigation in:name,description,readme",
    "robot reinforcement learning in:name,description,readme",
    "robot slam navigation in:name,description,readme",
    "explosion proof robot in:name,description,readme"
  ],
  "industry_watchlist": []
}
```

**说明**：这是展示结构的示例，并不是要求替换现有配置。现有 `config.json` 已经包含针对特种机器人的查询词和人工观察链接。分类词在 `main.py` 的 `KEYWORDS` 内。

如果只关心论文 / 项目，可从 `config.json` 删除 `ROS Discourse` RSS 数据源；如果只关心 Agentic VLN，可以减少 `github_queries`，多写如 `"robot agent vlm in:name,description,readme"` 等查询。GitHub 搜索针对每条查询默认最多取 25 条近期更新项目，不保证涵盖全部相关仓库。

## 5. 本地测试（可选）

```bash
cd special_robot_radar
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
python -m http.server 8000 --directory docs
```

浏览器访问 `http://127.0.0.1:8000`。不想联网、只查看已有资料时运行：

```bash
python main.py --offline
```

运行测试：

```bash
python -m unittest discover -s tests -v
```

## 6. 可选：以后再加 LLM 中文摘要

**完全可选**，不用配置也能每天自动抓取并按关键词归类。若以后希望大模型根据论文摘要生成更自然的中文解释：

在 GitHub 仓库 **Settings → Secrets and variables → Actions**：

- **Secrets** 新建 `RADAR_MODEL_API_KEY`（私密 API Key）。
- **Variables** 新建 `RADAR_MODEL_NAME`（你已开通的模型名称）；非 OpenAI 官方接口可选 `RADAR_MODEL_BASE_URL`。

启用后仅对每轮最多 48 条新数据尝试 LLM 元数据初筛。API 调用可能产生费用。**绝对不要把 `.env`、密钥或单位内部资料提交到公开仓库。**

## 7. 目录结构

```text
special_robot_radar/
├── .github/workflows/update-radar.yml  # 定时采集、自动发布
├── config.json                         # arXiv/RSS/GitHub 检索词
├── main.py                             # 收集、去重、分类、生成网页
├── requirements.txt                    # Python 依赖
├── tests/test_radar.py                 # 基础测试
├── docs/
│   ├── index.html                      # 网页
│   ├── items.json                      # 累积的公开条目
│   └── weekly.md                       # 每周调研线索
└── README.md                           # 部署教程
```

## 8. 常见问题

**问题：网站显示 0 条？** 第一次尚未成功采集前是空索引。先到 Actions 查看运行日志。GitHub / arXiv 对网络、速率和服务状态有限制；某个源报错时通常继续处理其他源；所有来源均失败时工作流会报错，保留已发布的旧页面。

**问题：`Resource not accessible by integration` 或 push 403？** 看第 3 节权限说明；如果仓库设置不允许 Actions 写入、分支保护禁止机器人提交或组织策略限制，需要调整授权或改成只构建网页、不提交历史记录的模式。

**问题：找不到 Run workflow 按钮？** 先检查 `main` 分支、工作流 YAML 是否存在、仓库是否已启用 GitHub Actions。`workflow_dispatch` 必须位于默认分支才能手动触发。

**问题：如何只保留近一个月？** `main.py` 当前显示近 40 天内容，保存最多约 100 天的历史，改动 `timedelta(days=40)` 等参数即可。

技术限制：更新周期为每日一次；关键词匹配并非专业全文判读；目前并没有自动阅读论文 PDF、对比论文内容或提取 GitHub README 全文。下一阶段可接入 LLM Agent、向量库、企业公告源。
