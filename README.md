# 🔥 AI热榜

> 面向中文用户的 AI 工具 / 模型 / Agent / 新闻导航站。**网站 + GitHub 双向信息流**，每 6 小时自动更新。

[![网站](https://img.shields.io/badge/网站-AI热榜-brightgreen)](https://aihot.bt199.com/)
[![更新频率](https://img.shields.io/badge/更新频率-每6小时-blue)](https://aihot.bt199.com/)
[![工具](https://img.shields.io/badge/工具-171+-orange)](https://aihot.bt199.com/tools/)
[![模型](https://img.shields.io/badge/模型-87+-lightgrey)](https://aihot.bt199.com/models/)
[![Agent](https://img.shields.io/badge/Agent-52+-purple)](https://aihot.bt199.com/agents/)
[![新闻](https://img.shields.io/badge/新闻-151+-red)](https://aihot.bt199.com/news/)
[![License](https://img.shields.io/badge/License-MIT-lightgrey)](LICENSE)

🌐 **在线网站**：https://aihot.bt199.com/  
📦 **GitHub 仓库**：https://github.com/laolaoshiren/ai-hot

---

## 项目定位

AI热榜不是单纯的“静态导航页”，而是一个持续滚动更新的 AI 信息入口：

- **网站端**：给中文用户直接看结果、找工具、看模型、追新闻
- **GitHub 端**：作为公开的数据源、更新源、开发记录、协作入口

也就是说，这个项目从一开始就是：

> **GitHub 负责沉淀与公开，网站负责分发与触达。**

现在两边已经打通：
- GitHub 上的数据和代码更新，会驱动网站更新
- 网站上的重要栏目和内容结构，也会反向推动 GitHub 持续整理与维护

---

## 现在网站上有什么

### 核心栏目
- [🔥 今日热点](https://aihot.bt199.com/)
- [🛠️ AI工具](https://aihot.bt199.com/tools/)
- [🧠 AI模型](https://aihot.bt199.com/models/)
- [🤖 AI Agent](https://aihot.bt199.com/agents/)
- [📰 AI新闻](https://aihot.bt199.com/news/)
- [🏢 AI提供商](https://aihot.bt199.com/providers/)
- [🔍 全站搜索](https://aihot.bt199.com/search/)
- [⚔️ 工具对比](https://aihot.bt199.com/compare/)

### 代表能力
- 工具 / 模型 / Agent / 新闻统一导航
- 面向中文用户的人话筛选与排序
- 工具静态详情页（利于 SEO 与分享）
- 首页热搜关键词可点击直达站内搜索
- Providers / Models 分栏，不再语义混乱
- 首页底部显示中国时间的最近更新时间

---

## 当前数据规模

截至当前仓库版本：

- **工具**：171+
- **模型**：87+
- **精选模型榜**：34+
- **Agent**：52+
- **新闻**：151+
- **提供商**：22+
- **项目**：166+

说明：
- 网站展示内容会持续变化
- GitHub 中的数据是当前版本的公开沉淀
- 线上站点可能因缓存出现几分钟延迟，但 GitHub 提交始终是第一手变更记录

---

## GitHub 和网站的双向信息流怎么运作

### GitHub → 网站
- `data/*.json`：原始/生成数据源
- `site/data/*.json`：Hugo 实际读取的数据
- `site/layouts/`：网站页面模板
- Push 到 `main` 后，GitHub Actions 自动构建并部署到 Pages

### 网站 → GitHub
网站不是“孤立成品”，而是反过来指导 GitHub 更新：
- 首页/栏目页暴露脏数据 → 回到 GitHub 修数据规则
- SEO 表现不够 → 回到 GitHub 补静态详情页 / sitemap / 结构化数据
- 用户体验发现问题 → 回到 GitHub 调整模板与信息结构

所以这个仓库不只是存代码，也是：
- **公开路线图**
- **内容更新源**
- **线上问题修复记录**
- **项目可信背书**

---

## 项目结构

```text
ai-hot/
├── data/                  # 原始/生成数据（Git 跟踪）
├── site/
│   ├── content/           # Hugo 内容页（含静态工具详情页）
│   ├── data/              # Hugo 构建读取的数据
│   ├── layouts/           # 页面模板
│   └── static/            # 静态资源、sitemap、robots 等
├── scripts/               # 数据采集、清洗、生成、SEO、部署脚本
├── .github/workflows/     # GitHub Actions 工作流
└── docs/                  # 阶段性报告与开发文档
```

---

## 自动化更新机制

### GitHub Actions
- **6-Hour AI Data Aggregation**
  - 每 6 小时自动采集/更新数据
- **Deploy to GitHub Pages**
  - push 到 `main` 后自动部署网站

### 主要流程
```text
数据采集/清洗 → 写入 data/*.json → 同步到 site/data/ → Hugo 构建 → GitHub Pages 发布
```

### 当前关键特性
- 首页更新时间强制使用 **中国时间（Asia/Shanghai）**
- 工具详情页已升级为静态路由：
  - `/tools/cursor/`
  - `/tools/claude-code/`
  - `/tools/deepseek/`
- sitemap 已升级为索引模式：
  - `/sitemap.xml`
  - `/sitemap-pages.xml`
  - `/sitemap-tools.xml`

---

## GitHub 侧目前重点维护什么

接下来 GitHub 侧会重点承担这些工作：

1. **README 持续更新**
   - 保持和网站栏目、数据规模、能力一致
2. **数据质量维护**
   - 清理脏新闻、过时模型、错误链接
3. **文档化沉淀**
   - 把重要设计决策、结构演进、SEO 改造沉淀到仓库
4. **对外协作入口**
   - 通过 Issues / PR 接收建议与修正
5. **双向信息流强化**
   - 让 GitHub 不只是代码仓库，而是网站的公开后台与说明书

---

## 关键页面入口

### 网站入口
- [首页](https://aihot.bt199.com/)
- [工具库](https://aihot.bt199.com/tools/)
- [模型榜](https://aihot.bt199.com/models/)
- [Agent](https://aihot.bt199.com/agents/)
- [新闻](https://aihot.bt199.com/news/)
- [提供商](https://aihot.bt199.com/providers/)

### GitHub 文档入口
- [开发文档目录](./docs/)
- [V4 完成报告](./docs/V4_COMPLETE_REPORT.md)
- [V4 开发计划](./docs/V4_DEVELOPMENT_PLAN.md)
- [V3 开发指南](./docs/V3_DEVELOPMENT_GUIDE.md)

---

## 贡献方式

欢迎通过以下方式参与：

- 提交新工具 / 新模型 / 新 Agent 线索
- 报告错误链接、脏数据、过时信息
- 提建议：栏目结构、SEO、GitHub 展示、数据源
- 提交 PR 改进仓库与网站

👉 Issues：
https://github.com/laolaoshiren/ai-hot/issues

---

## 许可证

[MIT](LICENSE)
