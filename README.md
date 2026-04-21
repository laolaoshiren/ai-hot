# 🔥 AI热榜

> 中文AI世界实时热榜，每6小时自动更新

[![网站](https://img.shields.io/badge/网站-AI热榜-brightgreen)](https://aihot.bt199.com/)
[![更新频率](https://img.shields.io/badge/更新频率-每6小时-blue)](#)
[![工具](https://img.shields.io/badge/工具-176+-orange)](#)
[![模型](https://img.shields.io/badge/模型-62+-lightgrey)](#)
[![Agent](https://img.shields.io/badge/Agent-13+-purple)](#)
[![License](https://img.shields.io/badge/License-MIT-lightgrey)](LICENSE)

🌐 **网站**: https://aihot.bt199.com/

---

## 🛠️ 收录工具（精选 45+）

### 编程
| 工具 | 说明 | 价格 |
|------|------|------|
| [Cursor](https://cursor.sh) | AI-first 代码编辑器 | 免费 + Pro $20/月 |
| [GitHub Copilot](https://github.com/features/copilot) | GitHub 官方 AI 编程助手 | $10/月 |
| [Claude Code](https://docs.anthropic.com/en/docs/claude-code) | Anthropic CLI 编程助手 | API 按量 |
| [Codex CLI](https://github.com/openai/codex) | OpenAI 终端编程助手 | API 按量 |
| [Codeium](https://codeium.com) | 免费 AI 代码补全 | 个人免费 |
| [Continue](https://continue.dev) | 开源 AI 编程助手 | 开源免费 |
| [Windsurf](https://codeium.com/windsurf) | Codeium 出品 AI IDE | 免费 + Pro $15/月 |
| [Trae](https://trae.ai) | 字节跳动 AI IDE | 免费 |

### 对话
| 工具 | 说明 | 价格 |
|------|------|------|
| [ChatGPT](https://chat.openai.com) | 最流行的 AI 对话 | 免费 + $20/月 |
| [Claude](https://claude.ai) | 长文本能力强 | 免费 + $20/月 |
| [Gemini](https://gemini.google.com) | Google 多模态 | 免费 + $20/月 |
| [DeepSeek](https://chat.deepseek.com) | 国产最强开源 | 免费 |
| [Kimi](https://kimi.moonshot.cn) | 超长上下文 | 免费 |
| [豆包](https://www.doubao.com) | 字节跳动，完全免费 | 免费 |
| [通义千问](https://tongyi.aliyun.com) | 阿里巴巴 | 免费 |
| [文心一言](https://yiyan.baidu.com) | 百度 | 免费 |

### 绘画 / 视频 / 搜索 / 更多...
完整列表请访问 [网站](https://laolaoshiren.github.io/ai-hot/tools/)

---

## 🤖 Agent 专区

| Agent | 类型 | 价格 |
|-------|------|------|
| [Devin](https://devin.ai) | 编程 Agent | $500/月 |
| [Codex (ChatGPT)](https://chatgpt.com) | 编程 Agent | Pro $200/月 |
| [Claude Code](https://docs.anthropic.com/en/docs/claude-code) | 编程 Agent | API 按量 |
| [Dify](https://dify.ai) | Agent 平台 | 开源 |
| [Coze](https://www.coze.com) | Bot 搭建 | 免费 |
| [LangChain](https://langchain.com) | 开发框架 | 开源 |
| [AutoGen](https://github.com/microsoft/autogen) | 多 Agent | 开源 |
| [CrewAI](https://crewai.com) | 多 Agent | 开源 |

---

## 🏢 AI 提供商（国内可用标注）

| 提供商 | 代表模型 | 国内访问 |
|--------|----------|----------|
| [DeepSeek](https://deepseek.com) | DeepSeek-V3, R1 | ✅ 直接访问 |
| [月之暗面](https://moonshot.cn) | Kimi | ✅ 直接访问 |
| [智谱 AI](https://zhipuai.cn) | GLM-4 | ✅ 直接访问 |
| [字节跳动](https://www.doubao.com) | 豆包 | ✅ 直接访问 |
| [阿里云](https://tongyi.aliyun.com) | 通义千问 | ✅ 直接访问 |
| [百度](https://yiyan.baidu.com) | 文心一言 | ✅ 直接访问 |
| [百川智能](https://baichuan-ai.com) | Baichuan 4 | ✅ 直接访问 |
| [OpenAI](https://openai.com) | GPT-4o | ❌ 需代理 |
| [Anthropic](https://anthropic.com) | Claude | ❌ 需代理 |
| [Google](https://ai.google.dev) | Gemini | ❌ 需代理 |

---

## 📊 数据来源

| 类型 | 来源 | 更新频率 |
|------|------|----------|
| 新闻 | 机器之心 / 36氪 / IT之家 / TechCrunch / The Verge / MIT Tech Review | 每6h |
| 社区 | Hacker News / Reddit (ML, LocalLLaMA) / V2EX | 每6h |
| 项目 | GitHub Search API / GitHub Trending | 每6h |
| 模型 | HuggingFace API | 每6h |
| 关键词 | 百度下拉词 / 微博热搜 / 知乎热榜 | 每6h |

## 🔧 技术架构

```
GitHub Actions (每6h定时) → Python 采集脚本 → JSON 数据
        ↓
    Hugo 静态生成 → GitHub Pages 部署
```

## 📝 贡献

通过 [Issues](https://github.com/laolaoshiren/ai-hot/issues) 提交新工具！

## 📄 许可证

[MIT](LICENSE)
