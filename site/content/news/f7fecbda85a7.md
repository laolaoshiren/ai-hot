+++
title = "突发：谷歌 Genkit 推出 Agents API：支持分离式任务轮次与人机协同"
description = "突发：谷歌 Genkit 推出 Agents API：支持分离式任务轮次与人机协同。来源：InfoQ AI。"
seo_title = "突发：谷歌 Genkit 推出 Agents API：支持分离式任务轮次与人机协同｜AI资讯解读 - AI热榜"
seo_description = "突发：谷歌 Genkit 推出 Agents API：支持分离式任务轮次与人机协同。来源：InfoQ AI。"
seo_keywords = "突发：谷歌 Genkit 推出 Agents API：支持分离式任务轮次与人机协同, InfoQ AI, AI新闻, AI资讯, AI热榜"
slug = "f7fecbda85a7"
type = "news"

[params]
id = "f7fecbda85a7"
name = "突发：谷歌 Genkit 推出 Agents API：支持分离式任务轮次与人机协同"
title_en = "突发：谷歌 Genkit 推出 Agents API：支持分离式任务轮次与人机协同"
original_url = "https://www.infoq.cn/article/ckLEtt7bN6AAURuEjfFF?utm_source=rss&utm_medium=article"
source = "InfoQ AI"
published = "2026-07-16T16:00:00"
lang = "zh"
intro = "突发：谷歌 Genkit 推出 Agents API：支持分离式任务轮次与人机协同。来源：InfoQ AI。"
ai_summary = ""
summary = ""
summary_zh = ""
tags = []
list_page = 35
+++

<!-- AUTO-GENERATED: news page -->

最近，谷歌
Genkit
（谷歌用于构建全栈式 AI 应用的开源框架）发布预览版 Agents API。

该 API 将消息历史、工具执行循环、流式传输、状态持久化以及前端协议全部封装在一个
chat()
接口背后，无论智能体是在进程内运行还是部署在 HTTP 端点之后，该接口的工作方式完全一致。

预览版现已支持 TypeScript 和 Go，Python 和 Dart 的支持也在计划之中。

其核心设计原则是：一个抽象层即可实现扩容，无需更换底层基础组件。

同一个智能体对象可处理一次性应答、流式多轮对话、等待人工确认的暂停工具调用，以及独立运行的长耗时任务。

当产品功能从简易聊天机器人迭代为多智能体协同工作流时，开发团队无需切换框架内其他组件。

Genkit 对两种大多数框架会混淆的智能体数据进行了区分。

自定义状态：驱动下一轮对话的强类型应用数据，例如工作流状态、任务列表或已选择的实体。

产物（Artifact）：可供用户单独查看、下载或版本管理的生成输出，例如报告、代码补丁或旅行行程。

工具可通过当前会话更新任意一类数据，且 Genkit 会实时将数据变更流式推送至客户端。

状态持久化提供两种实现方案。

服务端管理：配置会话存储后，消息、自定义状态和产物会以快照形式持久化保存，客户端通过会话 ID 重新连接。

Genkit 内置了 Firestore（生产多实例）、内存（开发环境）和文件（本地测试）三种存储，并支持通过可插拔接口实现自定义存储。

客户端管理：未配置存储时，服务端返回完整状态，客户端在每次对话轮次将其回传。

AI 工程师 Ebenezer Don
强调了这一架构选择在合规层面的意义

## 🔗 原始来源

如果你要核对细节，可以再看原文：
[InfoQ AI原文链接](https://www.infoq.cn/article/ckLEtt7bN6AAURuEjfFF?utm_source=rss&utm_medium=article)

