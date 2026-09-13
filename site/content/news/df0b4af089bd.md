+++
title = "深度解读：AMD 发布锐龙AI Max PRO 400 系列，端侧智能体走向多模型协同"
description = "深度解读：AMD 发布锐龙AI Max PRO 400 系列，端侧智能体走向多模型协同。来源：InfoQ AI。"
seo_title = "深度解读：AMD 发布锐龙AI Max PRO 400 系列，端侧智能体走向多模型协同｜AI资讯解读 - AI热榜"
seo_description = "深度解读：AMD 发布锐龙AI Max PRO 400 系列，端侧智能体走向多模型协同。来源：InfoQ AI。"
seo_keywords = "深度解读：AMD 发布锐龙AI Max PRO 400 系列，端侧智能体走向多模型协同, InfoQ AI, AI新闻, AI资讯, AI热榜"
slug = "df0b4af089bd"
type = "news"

[params]
id = "df0b4af089bd"
name = "深度解读：AMD 发布锐龙AI Max PRO 400 系列，端侧智能体走向多模型协同"
title_en = "深度解读：AMD 发布锐龙AI Max PRO 400 系列，端侧智能体走向多模型协同"
original_url = "https://www.infoq.cn/article/NizuOkFpcOPgbeClC4uL?utm_source=rss&utm_medium=article"
source = "InfoQ AI"
published = "2026-09-11T12:30:38"
lang = "zh"
intro = "深度解读：AMD 发布锐龙AI Max PRO 400 系列，端侧智能体走向多模型协同。来源：InfoQ AI。"
ai_summary = ""
summary = ""
summary_zh = ""
tags = []
list_page = 6
+++

<!-- AUTO-GENERATED: news page -->

9 月 10 日，AMD 在北京举办媒体沙龙，发布锐龙 AI Max PRO 400 系列处理器，并展示基于该平台打造的 Mini PC、紧凑型工作站、笔记本、平板、一体机和 AI NAS 等产品。

与单纯强调 AI 算力不同，AMD 此次展示的重点，是如何利用大容量统一内存和 CPU、GPU、NPU 异构计算能力，让大模型、知识库和智能体工作流更多地运行在本地设备上，覆盖开发、科研、金融、影视、公共服务和企业投标等场景。

大容量统一内存成为核心
从技术路径看，锐龙 AI Max 系列试图解决端侧 AI 面临的一个直接问题：模型和上下文对内存、显存容量的需求持续增加，而传统 PC 的独立显存容量相对有限。

以锐龙 AI Max+ 395 为例，该平台最高配备 128GB 统一内存，其中最高 96GB 可分配为显存。

由于 CPU 和 GPU 能够访问同一内存池，系统不必在彼此隔离的内存与显存之间频繁搬运数据，也能够为本地大模型、多模态应用、长上下文 RAG 和多智能体并发提供更大的可用空间。

这一设计的意义主要体现在“能否装下模型”，而不只是单次推理速度。

对于参数量较大或者需要同时加载多个模型的智能体应用，内存容量往往会先于算力成为限制因素。

统一内存允许系统根据任务动态调整 CPU 与 GPU 的内存占用，但实际能够运行多大规模的模型，仍取决于模型量化精度、上下文长度、KV Cache 占用和推理框架优化程度。

平台还集成 CPU、GPU 和 NPU 三类计算单元。

面向具体应用，可以由 GPU 承担大模型或多模态模型的批量推理，NPU 处理低功耗、持续运行的轻量任务，CPU 负责智能体编排、工具调用以及传统软件逻辑。

不过，要充分利用三类计算单元，还需要操作系统、推理框架和应用层完成相应的任务拆分与调度。

从运行模型转向承载智能体系统
当本地 AI 从单个聊天助手发展为多个智能体协作，PC 承担的任务也发生了变化。

模型之外，设备还需要同时运行向量数据库、RAG 系统、工具服务、权限管理和任务调度模块，部分智能体还需要持续驻留后台。

星漪科技展示的 Flowy AI PC 尝试以 Agentic PC 架构统一管理大模型调度、智能体服务、工具调用和硬件资源，避免不同应用分别安装模型和运行环境。

锐龙 AI Max 平台的大容量统一内存，则被用于支持多智能体并发、长上下文检索和多模态生成。

## 🔗 原始来源

如果你要核对细节，可以再看原文：
[InfoQ AI原文链接](https://www.infoq.cn/article/NizuOkFpcOPgbeClC4uL?utm_source=rss&utm_medium=article)

