+++
title = "最新动态：从GPU到Token：英伟达Vera Rubin如何重构下一代AI工厂"
description = "最新动态：从GPU到Token：英伟达Vera Rubin如何重构下一代AI工厂。来源：InfoQ AI。"
seo_title = "最新动态：从GPU到Token：英伟达Vera Rubin如何重构下一代AI工厂｜AI资讯解读 - AI热榜"
seo_description = "最新动态：从GPU到Token：英伟达Vera Rubin如何重构下一代AI工厂。来源：InfoQ AI。"
seo_keywords = "最新动态：从GPU到Token：英伟达Vera Rubin如何重构下一代AI工厂, InfoQ AI, AI新闻, AI资讯, AI热榜"
slug = "6a6a02fcaf8d"
type = "news"

[params]
id = "6a6a02fcaf8d"
name = "最新动态：从GPU到Token：英伟达Vera Rubin如何重构下一代AI工厂"
title_en = "最新动态：从GPU到Token：英伟达Vera Rubin如何重构下一代AI工厂"
original_url = "https://www.infoq.cn/article/s8EpYCpdF3YiSkSbYfGG?utm_source=rss&utm_medium=article"
source = "InfoQ AI"
published = "2026-07-17T10:09:25"
lang = "zh"
intro = "最新动态：从GPU到Token：英伟达Vera Rubin如何重构下一代AI工厂。来源：InfoQ AI。"
ai_summary = ""
summary = ""
summary_zh = ""
tags = []
list_page = 21
+++

<!-- AUTO-GENERATED: news page -->

英伟达正在将下一代 AI 基础设施的竞争，从“谁拥有更快的 GPU”推向“谁能建成效率更高的 Token 工厂”。

之前，企业只需要数百到数千块加速卡组成的集群，但现在 AI 基础设施面对的任务已经不再是完成一次次更大规模训练，还需要支持智能体系统持续运行生成更多 Token、KV cache，并产生大量 CPU 沙盒、网络通信和数据存取等需求。

这意味着，AI 基础设施的衡量标准正在发生根本变化。

单颗芯片的峰值算力仍然重要，但已经不足以决定系统最终能够创造多少价值。

用户更关心的是，在固定电力、机房空间和资本投入下，系统能够持续生成多少 Token；单个用户获得 Token 的速度有多快；每百万 Token 需要多少成本；以及数万乃至更多加速器能否长时间保持稳定运行。

Vera Rubin 正是英伟达面向智能体 AI 下一阶段给出的系统级答案。

它并非单纯升级 GPU，而是将 CPU、GPU、LPU、DPU、网络、上下文存储和软件编排整合为一套异构基础设施，让不同处理器承担各自擅长的任务，共同扩大 AI 工厂的 Token 产能。

核心计算 Vera Rubin：更重持续产出
Vera Rubin NVL72 是这套基础设施中的核心计算引擎。

它集成了 72 颗 Rubin GPU、36 颗 Vera CPU，通过大规模 NVLink 铜质主干相连，可作为一个巨大的 GPU。

对上层软件而言，这 72 颗 GPU 可以像一个拥有超大显存和计算能力的统一加速器运行。

机架内部使用第六代 NVLink 和 NVLink 6 Switch 完成纵向扩展，机架之间则可以通过 Spectrum-X Ethernet 或 Quantum-X800 InfiniBand 进行横向扩展。

与 GB200、GB300 NVL72 类似，Vera Rubin NVL72 将 CPU、GPU、交换系统和网络端点设计为一个统一平台。

区别在于，Rubin 进一步提升了计算密度、显存带宽和 GPU 间通信能力，并针对推理、后训练和智能体工作负载增加了新的 Transformer Engine、全机架机密计算能力以及第二代可靠性、可用性和可维护性引擎。

官方数据显示，单颗 Rubin GPU 提供 288 GB HBM4 显存和 22 TB/s 显存带宽，NVFP4 推理性能达到 50 PFLOPS，NVFP4 训练性能达到 35 PFLOPS。

整个 NVL72 机架可提供 20.7 TB HBM4 显存。

NVLink 6 则为每颗 GPU 提供 3.6 TB/s 的全互联带宽，使 72 颗 GPU 可以在非阻塞互联结构中作为一个统一的大型加速器运行。

这种设计尤其适合预训练、后训练、测试时扩展、智能体扩展、强化学习、长上下文推理以及通信密集型的混合专家模型（MoE）。

在这些场景中，性能瓶颈往往不只来自计算本身，还来自 All-Reduce、专家分发以及跨 GPU 数据同步。

GPU 数量不断增加后，如果互联带宽和通信效率跟不上，更多芯片并不会带来线性的性能提升，反而会让大量 GPU 陷入等待。

## 🔗 原始来源

如果你要核对细节，可以再看原文：
[InfoQ AI原文链接](https://www.infoq.cn/article/s8EpYCpdF3YiSkSbYfGG?utm_source=rss&utm_medium=article)

