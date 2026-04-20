# 🔥 AI热榜 (AI Hot)

> **每天6小时，带你追上AI的速度**

[![更新频率](https://img.shields.io/badge/更新频率-每6小时-brightgreen)](#)
[![工具收录](https://img.shields.io/badge/工具-500+-blue)](#)
[![开源](https://img.shields.io/badge/开源-数据透明-orange)](#)
[![License](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey)](LICENSE)

---

**AI热榜** 是一个每6小时自动更新的中文AI导航站，收录最新最热的AI工具、AI模型、AI Agent、AI新闻。用数据驱动，不用人工维护。

🌐 **网站**: [即将上线]()

---

## ✨ 特色

- 🔥 **每6小时自动更新** — 全网最快AI导航更新频率
- 📊 **热度飙升榜** — GitHub stars加速度排名，发现爆炸性项目
- 📰 **新闻即导航** — 每条新闻关联相关AI工具
- 💰 **价格透明** — 国内大模型API价格实时对比
- 🤖 **Agent图谱** — AI Agent生态全景可视化
- 🎲 **随机发现** — 每次访问都有新惊喜
- 🔍 **中文SEO优化** — 让需要AI工具的人第一时间找到我们

## 📂 数据分类

| 板块 | 内容 | 更新频率 |
|------|------|----------|
| 🔥 今日热榜 | 全网AI热点 | 每6小时 |
| 🧠 AI模型 | 大语言/图像/视频/语音/多模态 | 每6小时 |
| 🛠️ AI工具 | 编程/写作/设计/办公/搜索 | 每6小时 |
| 🤖 AI Agent | Agent框架/平台/工作流 | 每6小时 |
| 📰 AI新闻 | 行业动态/新品发布/论文突破 | 每6小时 |
| 🏢 AI提供商 | 国内外AI公司+价格对比 | 每周 |

## 🔧 技术架构

```
GitHub Actions (6h cron)
    ↓
Python 脚本采集 → JSON 数据
    ↓
Hugo 静态生成
    ↓
GitHub Pages + Cloudflare Pages 部署
```

- **零成本**: 仅域名费用 ~¥50/年
- **全自动化**: 从数据采集到部署全自动
- **开源透明**: 数据源、更新日志、评分算法全部公开

## 📊 数据来源

### 新闻源
机器之心 / IT之家 / 36氪 / TechCrunch / The Verge / Hacker News / Reddit / V2EX

### 项目发现
GitHub Search API / GitHub Trending / HuggingFace API / Papers With Code

### 热点探测
GitHub stars加速度 + HN前页 + V2EX热门 + Reddit hot + 微博热搜 + 百度热搜

### 关键词（实时）
百度下拉词 / 微博热搜 / 知乎热榜 / 抖音热榜（每6h自动采集驱动SEO）

## 🛠️ 本地开发

```bash
# 克隆仓库
git clone https://github.com/laolaoshiren/ai-hot.git
cd ai-hot

# 安装 Python 依赖
pip install -r scripts/requirements.txt

# 手动运行数据采集
python scripts/aggregate.py

# 启动 Hugo 本地预览
cd site && hugo server -D
```

## 📝 贡献

欢迎通过 [Issues](https://github.com/laolaoshiren/ai-hot/issues) 提交新的AI工具！

## 📄 许可证

数据: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)
代码: [MIT](LICENSE)

---

<p align="center">
  <b>⭐ 如果觉得有用，请给个 Star 支持一下！</b>
</p>
