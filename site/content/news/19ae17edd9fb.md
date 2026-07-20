+++
title = "重磅！Google 想为 AI Agent 打造下一个 Kubernetes"
description = "重磅！Google 想为 AI Agent 打造下一个 Kubernetes。来源：InfoQ AI。"
seo_title = "重磅！Google 想为 AI Agent 打造下一个 Kubernetes｜AI资讯解读 - AI热榜"
seo_description = "重磅！Google 想为 AI Agent 打造下一个 Kubernetes。来源：InfoQ AI。"
seo_keywords = "重磅！Google 想为 AI Agent 打造下一个 Kubernetes, InfoQ AI, AI新闻, AI资讯, AI热榜"
slug = "19ae17edd9fb"
type = "news"

[params]
id = "19ae17edd9fb"
name = "重磅！Google 想为 AI Agent 打造下一个 Kubernetes"
title_en = "重磅！Google 想为 AI Agent 打造下一个 Kubernetes"
original_url = "https://www.infoq.cn/article/jNsfjJuAJjDzGYS51jHC?utm_source=rss&utm_medium=article"
source = "InfoQ AI"
published = "2026-06-18T17:27:42"
lang = "zh"
intro = "重磅！Google 想为 AI Agent 打造下一个 Kubernetes。来源：InfoQ AI。"
ai_summary = ""
summary = ""
summary_zh = ""
tags = []
list_page = 182
+++

<!-- AUTO-GENERATED: news page -->

两个新的 Apache 2.0 项目让具有突发性的 Agent 工作负载硬件效率提升了 97%。

Google 表示，面向希望在大规模企业环境中高效运行 Agent 工作负载、又不想重新发明 Kubernetes 的组织，它已经拿出了一个早期方案。

目前，Google 已经开源 Agent Substrate，以及构建在其上的分布式 Agent 运行时 Agent eXecutor，简称 AX。

两个项目均采用较为宽松的 Apache-2.0 许可证。

不过，Agent Substrate 仍处于非常早期的开发阶段，相关能力和接口都可能继续变化。

Agent Substrate 是一种在 Kubernetes 之上构建 Agent 专属控制能力的方式。

它让用户可以借助一个轻量级控制平面来管理 Agent 生命周期。

这个控制平面专门面向 Agent 场景中的高频交互设计，可应对数百万次亚秒级工具调用。

与之配套的 AX，则是一个子系统或运行时，用于协调 Agentic 循环、通过事件日志管理执行，并与本地和远程 Actor 通信……原生支持恢复和执行续跑，即使是在复杂的分布式环境中也是如此。

来自 Kubernetes 的经验？

GKE 工程师 Tim Hockin 和产品经理 Brandon Royal 在谈到为何开放这些早期项目时表示：“在 Kubernetes 早期，来自不同贡献者的反馈和视角至关重要，他们在解决类似挑战的过程中帮助项目走向成功。

我们认为，Agent 基础设施正处在一个类似的拐点。

”
Google 在 5 月下旬发布了这两个项目，版本分别为 v0.0.0 和 v0.1.0。

两者都附带了大量关于破坏性变更和整体不成熟的提示。

Substrate 文档警告称：“在这一阶段，我们不对向后兼容性作出任何保证，本项目中的一切都可能发生变化。

”这也强调了它仍处于非常早期的孕育阶段。

配套的视频演示展示了 AX 和 Substrate 的实际运行效果：对于突发式工作负载的 Agent，它们能够带来巨大的效率提升。

这类场景在 Agent 等待人类交互、外部工具或数据源时很常见。

## 🔗 原始来源

如果你要核对细节，可以再看原文：
[InfoQ AI原文链接](https://www.infoq.cn/article/jNsfjJuAJjDzGYS51jHC?utm_source=rss&utm_medium=article)

