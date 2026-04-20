# 🔥 AI热榜

> 中文AI世界实时热榜，每6小时自动更新

[![网站](https://img.shields.io/badge/网站-AI热榜-brightgreen)](https://laolaoshiren.github.io/ai-hot/)
[![更新频率](https://img.shields.io/badge/更新频率-每6小时-blue)](#)
[![数据源](https://img.shields.io/badge/数据源-10个-orange)](#)
[![License](https://img.shields.io/badge/License-MIT-lightgrey)](LICENSE)

---

🌐 **网站**: https://laolaoshiren.github.io/ai-hot/

---

## ✨ 特色

- 🔥 **每6小时自动更新** — 全网最快AI导航更新频率
- 📊 **热度飙升榜** — GitHub stars加速度排名，发现爆炸性项目
- 📰 **新闻即导航** — 每条新闻关联相关AI工具
- 🔑 **实时关键词** — 百度/微博/知乎热搜自动驱动SEO
- 🤖 **Agent图谱** — AI Agent生态全景
- 🎲 **随机发现** — 每次访问都有新惊喜

## 📂 内容板块

| 板块 | 内容 | 数据源 |
|------|------|--------|
| 🔥 今日热榜 | 全网AI热点 | GitHub/HN/Reddit/V2EX |
| 🧠 AI模型 | 大语言/图像/视频/语音 | HuggingFace API |
| 🛠️ AI工具 | 编程/写作/设计/办公 | 待扩展 |
| 🤖 AI Agent | Agent框架/平台 | GitHub Search |
| 📰 AI新闻 | 行业动态/新品发布 | RSS + API (6源) |
| 🏢 AI提供商 | 国内外AI公司 | 待扩展 |

## 🔧 技术架构

```
GitHub Actions (6h cron)
    ↓
Python 脚本采集 → JSON 数据
    ↓
Hugo 静态生成
    ↓
GitHub Pages 部署
```

- **全自动化**: 从数据采集到部署全自动
- **开源透明**: 数据源、更新日志全部公开

## 📊 数据来源

| 类型 | 来源 |
|------|------|
| 新闻 | 机器之心 / IT之家 / 36氪 / TechCrunch / The Verge / MIT Tech Review |
| 社区 | Hacker News / Reddit (ML, LocalLLaMA) / V2EX |
| 项目 | GitHub Search API / GitHub Trending |
| 模型 | HuggingFace API (trendingScore, 最新, 分类) |
| 关键词 | 百度下拉词 / 微博热搜 / 知乎热榜（每6h自动采集） |

## 🛠️ 本地开发

```bash
git clone https://github.com/laolaoshiren/ai-hot.git
cd ai-hot

# 运行数据采集
pip install -r scripts/requirements.txt
python scripts/aggregate.py

# 启动 Hugo 本地预览
cd site && hugo server -D
```

## 📝 贡献

欢迎通过 [Issues](https://github.com/laolaoshiren/ai-hot/issues) 提交新的AI工具！

## 📄 许可证

[MIT](LICENSE)

---

<p align="center"><b>⭐ 觉得有用请给个 Star 支持一下！</b></p>
