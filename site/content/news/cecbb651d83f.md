+++
title = "GLM 5.2 和即将到来的人工智能利润率崩溃"
description = "文章网址：https://martinalderson.com/posts/the-upcoming-ai-margin…"
seo_title = "GLM 5.2 和即将到来的人工智能利润率崩溃｜AI资讯解读 - AI热榜"
seo_description = "文章网址：https://martinalderson.com/posts/the-upcoming-ai-margin…"
seo_keywords = "GLM 5.2 和即将到来的人工智能利润率崩溃, Hacker News AI, AI新闻, AI资讯, AI热榜"
slug = "cecbb651d83f"
type = "news"

[params]
id = "cecbb651d83f"
name = "GLM 5.2 和即将到来的人工智能利润率崩溃"
title_en = "Report: GLM 5.2 and the coming AI margin collapse"
original_url = "https://martinalderson.com/posts/the-upcoming-ai-margin-collapse-part-1-glm-5-2/"
source = "Hacker News AI"
published = "2026-07-06T20:14:55"
lang = "en"
intro = "文章网址：https://martinalderson.com/posts/the-upcoming-ai-margin…"
ai_summary = "文章网址：https://martinalderson.com/posts/the-upcoming-ai-margin…"
summary = "Article URL: https://martinalderson.com/posts/the-upcoming-ai-margin-collapse-part-1-glm-5-2/ Comments URL: https://news."
summary_zh = "文章网址：https://martinalderson.com/posts/the-upcoming-ai-margin-collapse-part-1-glm-5-2/ 评论网址：https://news.ycombinator.com/…"
tags = []
list_page = 21
+++

<!-- AUTO-GENERATED: news page -->

This is a two part series focusing on what I believe is perhaps the least understood upcoming shift in AI economics.

If you've enjoyed this and want to be notified about the second post, please feel free to sign up for my newsletter.
The real DeepSeek moment is upon us
What feels like decades ago, markets recoiled at DeepSeek's R1 model.

The theory being that given the underlying V3 model reportedly cost under $6m to train, the market therefore thought the huge investment in capex for model training was over, and thus the stock price of Nvidia et al collapsed overnight.
Of course, this was a hugely poor read of where the costs actually lie in AI.

Training - while no doubt capex intensive - is a fixed, up-front cost.

You spend hundreds of millions to train a model, then you are "done".[1]
Inference, on the other hand, scales with your demand.

It has genuine marginal costs.

I've written about this at length over the past year or so.

Again, the mainstream understanding of this - that the API costs the providers charge are their real costs is mistaken.
Indeed, when Anthropic/OpenAI charge $25/MTok for inference, my napkin maths suggests that this is probably something like 90% gross margin on the cost of compute vs the rack rate.

It may be a bit higher, or a bit lower (OpenAI's leaked financials suggest a ~60% gross margin on revenue, but this no doubt includes a lot of other costs like support, payment processing and other services they offer), but the whole business model of frontier AI labs is in short to spend a large amount of money on salaries on compute to train a model, then amortise that cost over a lot of very profitable inference.

If you can amortise that cost over enough inference you turn from profitable on a COGS basis to...

actually profitable.
GLM 5.2
I have been playing around with GLM5.2 from Z.ai for the last couple of weeks.

I believe GLM5.2 is the first model that reaches the "bar" of a genuine open weights competitor to Opus and GPT (at the time of writing, the latest version of GPT was 5.5 - future models no doubt will exceed this).
It's genuinely very good and hard for me to tell the difference between Opus - my daily driver and it.
I've found that it is slow because of the amount of thinking it tends to do.

For non interactive agentic tasks (like reviewing PRs in the background) which aren't time critical this is a non issue, but for interactive use it is definitely a tad too slow to keep my attention.

This also somewhat reduces the cost effectiveness of it (more thinking means more tokens, which increases costs).

## 🔗 原始来源

如果你要核对细节，可以再看原文：
[Hacker News AI原文链接](https://martinalderson.com/posts/the-upcoming-ai-margin-collapse-part-1-glm-5-2/)

