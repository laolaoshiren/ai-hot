+++
title = "法学硕士可以通过利用推理引擎来控制其主机"
description = "法学硕士可以通过利用推理引擎来控制其主机。来源：Hacker News AI"
seo_title = "法学硕士可以通过利用推理引擎来控制其主机｜AI资讯解读 - AI热榜"
seo_description = "法学硕士可以通过利用推理引擎来控制其主机。来源：Hacker News AI"
seo_keywords = "法学硕士可以通过利用推理引擎来控制其主机, Hacker News AI, AI新闻, AI资讯, AI热榜"
slug = "dffcb3a91fbb"
type = "news"

[params]
id = "dffcb3a91fbb"
name = "法学硕士可以通过利用推理引擎来控制其主机"
title_en = "In depth: LLMs could control their host machines by exploiting inference engines"
original_url = "https://boydkane.com/essays/llms-could-control-their-host-machines-by-exploiting-inference-engines"
source = "Hacker News AI"
published = "2026-08-24T19:03:06"
lang = "en"
intro = "法学硕士可以通过利用推理引擎来控制其主机。来源：Hacker News AI"
ai_summary = "法学硕士可以通过利用推理引擎来控制其主机。来源：Hacker News AI"
summary = "Article URL: https://boydkane.com/essays/llms-could-control-their-host-machines-by-exploiting-inference-engines Comments URL: https://news."
summary_zh = "法学硕士可以通过利用推理引擎来控制其主机。来源：Hacker News AI"
tags = []
list_page = 31
+++

<!-- AUTO-GENERATED: news page -->

|阅读LessWrong |
大型语言模型通常采取在一台计算机上运行的操作（通过 Claude Code 或 Codex 等代理工具），但法学硕士对提示的响应是在另一台具有 GPU 访问权限的计算机上计算的。

恶意 LLM 能否控制加载其权重的主机？

这样的机器是一个高价值的目标：与互联网上的通用计算机相比，它具有足够的计算能力来运行前沿 LLM，提供对 LLM 权重的轻松访问，并且具有对数据中心中其他计算机的特权访问权限。

本文探讨了恶意 LLM 如何轻松地控制主机。

这里考虑的主要攻击涉及 LLM 发出一个与语义无关的令牌序列，但它利用了将 LLM 加载到 GPU 上的软件中的漏洞，运行 LLM 来生成输出令牌，并将这些令牌解析为响应。

 。

LLM 如何在主机上执行代码？

与任何程序一样，vLLM 或 SGLang 等推理引擎可能包含可利用的错误。

由于 LLM 控制传递给推理引擎的令牌，因此恶意 LLM 可能会发出一系列令牌，而编写不当的推理引擎会将其误认为是要执行的代码或指令，而不是返回给用户的数据。

但肯定所有推理引擎都是强大的软件，这种情况永远不会发生，对吗？

vLLM 之前在工具调用参数上使用了 eval()
CVE-2025-9141 是 vLLM 基于 XML 的工具中的任意代码执行错误
Qwen3 Coder 的解析器。

解析器将几乎所有工具调用参数传递给
eval()，允许LLM在主机上执行任意代码。

## 🔗 原始来源

如果你要核对细节，可以再看原文：
[Hacker News AI原文链接](https://boydkane.com/essays/llms-could-control-their-host-machines-by-exploiting-inference-engines)

