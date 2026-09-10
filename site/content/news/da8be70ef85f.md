+++
title = "Qwen 3.8 遵循 GPT-5.5 Pro 推理预填充"
description = "文章网址： 评论网址： 积分：178 # 评论：73"
seo_title = "Qwen 3.8 遵循 GPT-5.5 Pro 推理预填充｜AI资讯解读 - AI热榜"
seo_description = "文章网址： 评论网址： 积分：178 # 评论：73"
seo_keywords = "Qwen 3.8 遵循 GPT-5.5 Pro 推理预填充, Hacker News AI, AI新闻, AI资讯, AI热榜"
slug = "da8be70ef85f"
type = "news"

[params]
id = "da8be70ef85f"
name = "Qwen 3.8 遵循 GPT-5.5 Pro 推理预填充"
title_en = "In depth: Qwen 3.8 follows GPT-5.5 Pro reasoning prefills"
original_url = "https://gist.github.com/wsxiaoys/e0286dc6bb624ff5fdf49e7f4c528ba3"
source = "Hacker News AI"
published = "2026-09-09T17:24:28"
lang = "en"
intro = "文章网址： 评论网址： 积分：178 # 评论：73"
ai_summary = "文章网址： 评论网址： 积分：178 # 评论：73"
summary = "Article URL: https://gist.github.com/wsxiaoys/e0286dc6bb624ff5fdf49e7f4c528ba3 Comments URL: https://news."
summary_zh = "文章网址： 评论网址： 积分：178 # 评论：73"
tags = []
list_page = 6
+++

<!-- AUTO-GENERATED: news page -->

一些开放模型的推理预填充，v1.1
后续行动
在一些开放模型上进行推理预填充
和
被盗的想法
此 v1.1 以 GPT-5.5 Pro 作为教师重新运行推理预填充实验。

对于每个问题，我从每个目标模型生成两个响应：
普通的、未预先填充的响应；和
从 GPT-5.5 Pro 推理的前 1% 开始的响应，插入到目标模型的推理通道中。

可见的答案仍然是自由生成的。

然后，我测量了老师的可见答案中有多少出现在目标模型答案的前 100 个标记中。

与上一篇文章一样，每个分数都是一元词、二元词和三元词源回忆的平均值。

增量是绝对百分比变化。

## 🔗 原始来源

如果你要核对细节，可以再看原文：
[Hacker News AI原文链接](https://gist.github.com/wsxiaoys/e0286dc6bb624ff5fdf49e7f4c528ba3)

