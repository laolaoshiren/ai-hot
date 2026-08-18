+++
title = "刚刚，Snowflake CoCo AI 成本优化指南：7 个关键方法 | 技术实践"
description = "刚刚，Snowflake CoCo AI 成本优化指南：7 个关键方法 | 技术实践。来源：InfoQ AI。"
seo_title = "刚刚，Snowflake CoCo AI 成本优化指南：7 个关键方法 | 技术实践｜AI资讯解读 - AI热榜"
seo_description = "刚刚，Snowflake CoCo AI 成本优化指南：7 个关键方法 | 技术实践。来源：InfoQ AI。"
seo_keywords = "刚刚，Snowflake CoCo AI 成本优化指南：7 个关键方法 | 技术实践, InfoQ AI, AI新闻, AI资讯, AI热榜"
slug = "d70ba66d8fed"
type = "news"

[params]
id = "d70ba66d8fed"
name = "刚刚，Snowflake CoCo AI 成本优化指南：7 个关键方法 | 技术实践"
title_en = "刚刚，Snowflake CoCo AI 成本优化指南：7 个关键方法 | 技术实践"
original_url = "https://www.infoq.cn/article/pOfV96f9DHG9Cw1KQAZB?utm_source=rss&utm_medium=article"
source = "InfoQ AI"
published = "2026-08-18T16:29:05"
lang = "zh"
intro = "刚刚，Snowflake CoCo AI 成本优化指南：7 个关键方法 | 技术实践。来源：InfoQ AI。"
ai_summary = ""
summary = ""
summary_zh = ""
tags = []
list_page = 1
+++

<!-- AUTO-GENERATED: news page -->

2026 年，智能体将在企业级应用中取得哪些实质性突破？

点击下载《2026 年 AI 与数据发展预测》白皮书，获悉专家一手前瞻，抢先拥抱新的工作方式！

Snowflake CoCo 可以把自然语言直接转化成真实工作流。

它会运行 SQL、执行多步流程，并且在每一轮交互里调用大语言模型。

它确实很强大，但也随之带来了一个新的成本问题：Agentic 会话会按照处理的 tokens 消耗 credits，如果团队没有治理机制，成本很容易失控。

好消息是，Snowflake 已经提供了一整套 AI 成本治理能力，而且这些能力都可以通过 SQL、Snowsight，甚至直接在 CoCo 里完成管理。

总体思路始终是三步：先看清成本花在哪里，再优化默认运行方式，最后在需要时设置强约束。

下面这 7 个控制手段，覆盖了从轻量监控到强制阻断的完整路径，并附上可直接使用的代码。

1、Usage history views：先知道成本花在哪
你无法治理自己看不见的东西。

设置任何限制之前，先把成本基线搞清楚。

CoCo 会把详细使用遥测写入各个 surface 对应的 ACCOUNT_USAGE 视图：
SNOWFLAKE.ACCOUNT_USAGE.CORTEX_CODE_CLI_USAGE_HISTORYSNOWFLAKE.ACCOUNT_USAGE.CORTEX_CODE_SNOWSIGHT_USAGE_HISTORYSNOWFLAKE.ACCOUNT_USAGE.CORTEX_CODE_DESKTOP_USAGE_HISTORY
每一行代表一次请求，其中包含 TOKEN_CREDITS、总 TOKENS，以及在 TOKENS_GRANULAR 和 CREDITS_GRANULAR 中记录的按模型拆分的 input、output 和 cache tokens 明细。

USER_ID、USER_TAGS 和 METADATA（例如角色名、推理区域）字段则提供了归因和分摊能力。

例如，下面这段查询可以统计过去 30 天里 CLI surface 上每个用户消耗的总 credits：

## 🔗 原始来源

如果你要核对细节，可以再看原文：
[InfoQ AI原文链接](https://www.infoq.cn/article/pOfV96f9DHG9Cw1KQAZB?utm_source=rss&utm_medium=article)

