+++
title = "重磅！面向 Agentic 负载的下一代 LLM 推理引擎设计实践｜AICon深圳"
description = "重磅！面向 Agentic 负载的下一代 LLM 推理引擎设计实践｜AICon深圳。来源：InfoQ AI。"
seo_title = "重磅！面向 Agentic 负载的下一代 LLM 推理引擎设计实践｜AICon深圳｜AI资讯解读 - AI热榜"
seo_description = "重磅！面向 Agentic 负载的下一代 LLM 推理引擎设计实践｜AICon深圳。来源：InfoQ AI。"
seo_keywords = "重磅！面向 Agentic 负载的下一代 LLM 推理引擎设计实践｜AICon深圳, InfoQ AI, AI新闻, AI资讯, AI热榜"
slug = "cdd19ecab418"
type = "news"

[params]
id = "cdd19ecab418"
name = "重磅！面向 Agentic 负载的下一代 LLM 推理引擎设计实践｜AICon深圳"
title_en = "重磅！面向 Agentic 负载的下一代 LLM 推理引擎设计实践｜AICon深圳"
original_url = "https://www.infoq.cn/article/fjkG0xhaV42S8sfCayFy?utm_source=rss&utm_medium=article"
source = "InfoQ AI"
published = "2026-07-14T10:00:00"
lang = "zh"
intro = "重磅！面向 Agentic 负载的下一代 LLM 推理引擎设计实践｜AICon深圳。来源：InfoQ AI。"
ai_summary = ""
summary = ""
summary_zh = ""
tags = []
list_page = 44
+++

<!-- AUTO-GENERATED: news page -->

Agent 时代，哪些方向正在成为行业关键变量？

50 + 实战案例揭晓答案！

模型参数规模不断突破，推理成本持续下降，开源生态日益繁荣。

当模型能力逐渐成为行业共识，一个新的问题开始浮现：当人人都能获得强大的模型能力之后，真正的竞争力还剩下什么？

 答案正在从模型能力本身，转向围绕模型构建可规模化的智能系统；从单点能力提升，转向系统工程与组织级落地能力。

在这一背景下，2026 年 AICon 人工智能开发与应用大会 · 深圳站正式启动。

本次大会将于 8 月 21 日—22 日举办，聚焦 AI 基础设施、大模型系统、智能体工程、数据智能、多模态技术与行业落地等关键方向，邀请来自腾讯、阿里、华为、百度、蚂蚁集团等 50 + 头部科技企业技术负责人、科研机构一线专家，系统性分享前沿洞察与实战干货，共同探讨 AI 技术从能力到系统、从实验到生产的真实路径。

阿里云高级开发工程师尚旭春已确认出席 “AI Infra、推理工程与异构计算” 专题，并发表题为《面向 Agentic 负载的下一代 LLM 推理引擎设计实践》的主题分享。

随着 AI Agent 从 Demo 逐步走向生产环境，LLM 推理负载正在发生根本性变化。

相比传统聊天场景，Agentic 工作负载具有高并发、短请求、多轮工具调用、逐 Token 生成等特点，推理引擎的优化目标也从追求极限吞吐，转向在保证低延迟的同时实现更高的 GPU Token 输出效率。

本次分享将结合 TokenSpeed 的研发实践，从 Runtime 与 Kernel 两个层面介绍面向 Agentic 推理场景的新一代推理引擎设计。

尚旭春，阿里云高级开发工程师，长期专注在大模型（LLM）软件栈在新硬件环境下的适配、性能调优与架构优化工作。

在深耕工业界核心算力基础设施的同时，深度参与并活跃于顶尖的大模型开源基础设施（Infra）社区。

作为 Mooncake 社区的 Maintainer，负责维护核心组件 Mooncake Store，该项目目前在 GitHub 上已获得超过 4k star；作为 SGLang 社区的 Committer，贡献了 PD 分离、流水线（PP）并行以及 HiCache 等多个提升长文本与高并发推理性能的核心特性；同时也是 TokenSpeed 社区的 Maintainer，负责 PD 分离、EPLB（弹性流水线负载均衡）以及 KVStore 等多个高吞吐核心子模块的架构与研发工作。

他在本次会议的详细演讲内容如下：
演讲提纲：
一、为什么 Agentic 推理需要新的推理引擎
1.1 Agentic 工作负载带来的新挑战
Agent 与 Chat 的推理模式差异
Token Throughput 与 User Latency 的重新平衡

## 🔗 原始来源

如果你要核对细节，可以再看原文：
[InfoQ AI原文链接](https://www.infoq.cn/article/fjkG0xhaV42S8sfCayFy?utm_source=rss&utm_medium=article)

