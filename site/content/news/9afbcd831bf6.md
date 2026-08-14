+++
title = "人工智能最重要的协议变得更容易使用"
description = "在新系统下，该协议将在服务器端对会话 ID 采取更宽松的“无状态”方法，类似于大多数普通网站的工作方式"
seo_title = "人工智能最重要的协议变得更容易使用｜AI资讯解读 - AI热榜"
seo_description = "在新系统下，该协议将在服务器端对会话 ID 采取更宽松的“无状态”方法，类似于大多数普通网站的工作方式"
seo_keywords = "人工智能最重要的协议变得更容易使用, TechCrunch AI, AI新闻, AI资讯, AI热榜"
slug = "9afbcd831bf6"
type = "news"

[params]
id = "9afbcd831bf6"
name = "人工智能最重要的协议变得更容易使用"
title_en = "Analysis: AI’s most important protocol is getting a little bit easier to use"
original_url = "https://techcrunch.com/2026/07/20/ais-most-important-protocol-is-getting-a-little-bit-easier-to-use/"
source = "TechCrunch AI"
published = "2026-07-20T20:50:40"
lang = "en"
intro = "在新系统下，该协议将在服务器端对会话 ID 采取更宽松的“无状态”方法，类似于大多数普通网站的工作方式"
ai_summary = "在新系统下，该协议将在服务器端对会话 ID 采取更宽松的“无状态”方法，类似于大多数普通网站的工作方式"
summary = "Under the new system, the protocol will take a looser, \"stateless\" approach to session IDs on the server side, similar to how most ordinary websites already work."
summary_zh = "在新系统下，该协议将在服务器端对会话 ID 采取更宽松的“无状态”方法，类似于大多数普通网站的工作方式"
tags = []
list_page = 110
+++

<!-- AUTO-GENERATED: news page -->

模型上下文协议 (MCP) 是 AI 互操作性的基本构建模块之一，为 AI 模型提供了访问外部数据源和服务的安全方式。

它是让聊天机器人访问您的日历、数据库或内部工具的管道，而不是工程师为每个连​​接构建自定义管道。

下周，该协议将进行重大更新，虽然最终用户可能不会注意到，但它可能会对生态系统的发展产生重大影响。

新版本的官方规范自 5 月份以来就已公开，但周一早上，我们从 Arcade 的工作人员那里得到了对这些变化的异常清晰的解释。

Arcade 是一家成立两年的初创公司，其整个业务都是围绕让人工智能代理在真实公司内部实际运行的工作展开的，让它们安全地连接到 Gmail、Slack 和 Salesforce 等工具并对其进行操作。

Arcade 在 6 月份筹集了 6000 万美元，其理念是大多数 AI 代理不会因为底层模型薄弱而失败，而是因为它们周围的基础设施尚未准备好，而这正是本次更新试图解决的问题。

从本质上讲，MCP 正在改变它处理会话 ID 的方式——服务器用来记住“啊，这与五秒钟前的对话是一样的”的小令牌——这样服务器就可以更轻松地在更大范围内运行。

正如 Arcade 创始人 Nate Barbettini 所说：
[在当前系统下]像Claude这样的MCP客户端第一次连接到服务器时，它会发送一个“hello”：我是Claude，这是我的版本，这是我的功能。

服务器用自己的功能进行回复，并返回一个会话 ID…从那时起，客户端在每个请求上发送该会话 ID，以便服务器知道这是同一个会话。

有时 ID 会过期，因此客户必须注意，请求一个新 ID，然后继续……。

想象一下真实的部署。

您正在为数百万用户运行一台服务器，位于负载均衡器后面，其全部工作是将每个请求路由到场中任何空闲的服务器，有时位于不同的区域。

现在，每台机器都必须知道其他机器分发的会话 ID。

这并非不可能，但这是一个严重的痛苦，它会与负载均衡器对抗而不是与之合作。

换句话说，当前的设置假设一台服务器记住了您，但真正的公司将流量分布在默认情况下不相互通信的数十台服务器上，因此今天的 MCP 服务器必须做额外的工作才能跟踪谁是谁。

对于任何大规模运行 MCP 服务器的人来说，这都是一个令人头疼的问题，这也是我们没有看到更多公司推出大规模第一方 MCP 集成的部分原因，尽管今年围绕代理 AI 进行了大肆宣传。

在新系统下，该协议将在服务器端对会话ID采取更宽松、“无状态”的方法，类似于大多数普通网站已经工作的方式，这应该使整个系统更容易维护，并且理论上大规模运行更便宜。

这些都是相当技术性的，但它重要地提醒我们，并非人工智能开发的每个部分都在以惊人的速度发展。

尽管模型训练进展顺利，但这些模型所需的许多技术基础设施仍然受到标准机构共识缓慢滚动的影响。

这确实正在发生；只是慢了一点！

## 🔗 原始来源

如果你要核对细节，可以再看原文：
[TechCrunch AI原文链接](https://techcrunch.com/2026/07/20/ais-most-important-protocol-is-getting-a-little-bit-easier-to-use/)

