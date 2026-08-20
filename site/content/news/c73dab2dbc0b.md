+++
title = "面向多模态推理的高效长上下文建模｜AICon深圳，这意味着什么？"
description = "面向多模态推理的高效长上下文建模｜AICon深圳，这意味着什么？。来源：InfoQ AI。"
seo_title = "面向多模态推理的高效长上下文建模｜AICon深圳，这意味着什么？｜AI资讯解读 - AI热榜"
seo_description = "面向多模态推理的高效长上下文建模｜AICon深圳，这意味着什么？。来源：InfoQ AI。"
seo_keywords = "面向多模态推理的高效长上下文建模｜AICon深圳，这意味着什么？, InfoQ AI, AI新闻, AI资讯, AI热榜"
slug = "c73dab2dbc0b"
type = "news"

[params]
id = "c73dab2dbc0b"
name = "面向多模态推理的高效长上下文建模｜AICon深圳，这意味着什么？"
title_en = "面向多模态推理的高效长上下文建模｜AICon深圳，这意味着什么？"
original_url = "https://www.infoq.cn/article/OgbViICigja8tasE0lwi?utm_source=rss&utm_medium=article"
source = "InfoQ AI"
published = "2026-08-15T10:00:00"
lang = "zh"
intro = "面向多模态推理的高效长上下文建模｜AICon深圳，这意味着什么？。来源：InfoQ AI。"
ai_summary = ""
summary = ""
summary_zh = ""
tags = []
list_page = 15
+++

<!-- AUTO-GENERATED: news page -->

大模型能力持续演进，但 AI 的下一阶段竞争正在发生变化。

模型能力之外，如何构建可靠的智能体、完善 AI 工程体系，并让 AI 在复杂业务环境中稳定运行，正在成为产业探索的新重点。

8 月 21 日-22 日，AICon 全球人工智能开发与应用大会将在深圳举办。

大会全日程现已 100%上线，来自产业一线的技术专家将围绕 Agent 工程化、大模型基础设施、AI Native 研发、具身智能等前沿方向，分享 AI 时代的技术探索与工程实践，共同探讨 AI 从能力突破走向系统构建的新路径。

浙江大学百人计划研究员庄博涵已确认出席 “大模型效率工程与 Agent 系统实践” 专题，并发表题为《面向多模态推理的高效长上下文建模》的主题分享。

2026 年，多模态大模型正从“被动感知”走向“主动执行”，而不断增长的上下文长度与生成成本，使“效率”成为其规模化落地的核心瓶颈。

本次分享围绕面向多模态理解与生成的高效推理，介绍团队在大模型“算法—系统协同设计”上的最新进展：高效注意力方面，覆盖支撑长上下文的稀疏 / 线性注意力；高效记忆方面，介绍基于 KV-cache 压缩与缓存管理的显存优化；高效解码方面，分享近期并行解码策略。

在此基础上，串联多模态大模型（Agent）在理解、生成等核心能力上的实践；并进一步简单介绍面向视频生成对齐的高效扩散强化学习，以及在交互式世界模型评测上的探索。

最后分享对高效基础模型未来走向的思考，包括 agentic loop 等。

在本次演讲中，庄博涵将对此展开详细介绍。

庄博涵，浙江大学百人计划研究员、博士生导师，入选国家级高层次青年人才计划。

主要研究高效大模型算法与系统协同优化，致力于打造极致 Token 性价比，并围绕 Agent Loops、World Models 和 Embodied AI 开展前沿研究。

曾任 Monash University 长聘助理教授并创立 ZIP Lab，与多家全球头部科技企业保持深度科研合作。

实验室首批 7 名博士毕业生均进入顶尖企业或高校，包括 DeepSeek、ByteDance Seed 等，多人入选头部人才计划；本科毕业生多赴世界一流高校攻读 PhD，有成员获 UC Berkeley 博士奖学金。

他在本次会议的详细演讲内容如下：
演讲提纲：
Efficient AI：算法与 infra 协同设计
高效注意力：化解注意力随序列长度二次增长的瓶颈，支撑长上下文理解与长视频生成。

高效记忆：通过 KV-cache 压缩与缓存管理，突破长序列推理的显存瓶颈。

高效解码：通过并行解码提升推理吞吐、降低生成时延。

2.

多模态大模型（Agent）的核心能力：理解与生成

## 🔗 原始来源

如果你要核对细节，可以再看原文：
[InfoQ AI原文链接](https://www.infoq.cn/article/OgbViICigja8tasE0lwi?utm_source=rss&utm_medium=article)

