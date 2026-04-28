+++
title = "DeepSeek V4 预览版开源：百万上下文和低成本推理成为主战场"
description = "DeepSeek V4 把百万上下文、MoE 架构和开源模型性能再次推到行业前排。"
seo_title = "DeepSeek V4 预览版开源：百万上下文和低成本推理成为主战场｜AI资讯解读 - AI热榜"
seo_description = "DeepSeek V4 把百万上下文、MoE 架构和开源模型性能再次推到行业前排。"
seo_keywords = "DeepSeek V4 预览版开源：百万上下文和低成本推理成为主战场, Hacker News AI, AI新闻, AI资讯, AI热榜"
slug = "dcc82d6d0a9e"
type = "news"

[params]
id = "dcc82d6d0a9e"
name = "DeepSeek V4 预览版开源：百万上下文和低成本推理成为主战场"
title_en = "DeepSeek-V4: Towards Highly Efficient Million-Token Context Intelligence"
original_url = "https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro"
source = "Hacker News AI"
published = "2026-04-24T03:07:54"
lang = "zh"
intro = "DeepSeek V4 把百万上下文、MoE 架构和开源模型性能再次推到行业前排。"
ai_summary = "DeepSeek V4 把百万上下文、MoE 架构和开源模型性能再次推到行业前排。"
summary = "Article URL: https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro Comments URL: https://news.ycombinator.com/item?id=47885014 Points: 149 # Comments: 14"
summary_zh = "DeepSeek 在 Hugging Face 发布 V4 Pro 与 V4 Flash 预览版，主打百万 token 上下文、更低 KV cache 占用和更强 Agent、编程与推理能力。它的看点不只是跑分，而是用 MoE、混合注意力和新训练流程，把开源模型竞争推进到长上下文与推理成本效率的新阶段。"
tags = []
list_page = 18
+++

<!-- AUTO-GENERATED: news page -->

DeepSeek 在 Hugging Face 上放出了 DeepSeek-V4 系列预览版，包括 V4-Pro 和 V4-Flash 两个 MoE 模型。官方给出的定位很明确：这不是一次只追求参数规模的更新，而是面向百万 token 上下文、复杂 Agent 任务和高效率推理的一代模型。

从技术路线看，V4 系列把重点押在长上下文效率上。DeepSeek 引入了结合压缩稀疏注意力和高度压缩注意力的混合注意力架构，官方称在 1M token 场景下，V4-Pro 相比上一代可把单 token 推理 FLOPs 降到 27%，KV cache 降到 10%。这意味着长文档、代码仓库和多轮 Agent 任务的成本压力会明显下降。

模型训练也不再是简单堆数据。DeepSeek 表示 V4 系列预训练使用超过 32T token，后训练阶段先分别培养领域专家，再通过在线策略蒸馏整合到统一模型中。这个流程说明开源模型正在吸收更多闭源前沿模型常用的系统化后训练方法。

值得看的地方在于，DeepSeek 把“开源可用”继续往“开源高性能且低成本”推进。如果 V4 在真实开发、知识工作和 Agent 场景里能兑现官方指标，它会给闭源模型的定价和企业部署方案带来更大压力。对于开发者和企业来说，真正的变量不是又多了一个模型，而是长上下文和复杂工作流是否开始变得更便宜。

## 🔗 原始来源

如果你要核对细节，可以再看原文：
[Hacker News AI原文链接](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro)

