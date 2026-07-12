+++
title = "为 5 岁儿童打造实时人工智能导师"
description = "嘿，HN！在过去的一年里，我们花了大部分时间来打造一个人工智能导师，教授 4-9 岁的孩子阅读、数学、ESL 等知识。让…"
seo_title = "为 5 岁儿童打造实时人工智能导师｜AI资讯解读 - AI热榜"
seo_description = "嘿，HN！在过去的一年里，我们花了大部分时间来打造一个人工智能导师，教授 4-9 岁的孩子阅读、数学、ESL 等知识。让…"
seo_keywords = "为 5 岁儿童打造实时人工智能导师, Hacker News AI, AI新闻, AI资讯, AI热榜"
slug = "ab79e9ec6b6c"
type = "news"

[params]
id = "ab79e9ec6b6c"
name = "为 5 岁儿童打造实时人工智能导师"
title_en = "Analysis: Building a real-time AI tutor for 5-year-olds"
original_url = "https://www.ello.com/blog/teaching-a-child-in-1000-ms"
source = "Hacker News AI"
published = "2026-07-09T20:51:06"
lang = "en"
intro = "嘿，HN！在过去的一年里，我们花了大部分时间来打造一个人工智能导师，教授 4-9 岁的孩子阅读、数学、ESL 等知识。让…"
ai_summary = "嘿，HN！在过去的一年里，我们花了大部分时间来打造一个人工智能导师，教授 4-9 岁的孩子阅读、数学、ESL 等知识。让…"
summary = "Hey HN! We've spent the good part of this past year building an AI tutor that teaches kids ages 4-9 reading, math, ESL and more."
summary_zh = "嘿，HN！在过去的一年里，我们花了大部分时间来打造一个人工智能导师，教授 4-9 岁的孩子阅读、数学、ESL 等知识。让人工智能导师有效地教导孩子是一项非常艰巨的技术挑战，这需要正确的底层架构。我们的导师指导"
tags = []
list_page = 11
+++

<!-- AUTO-GENERATED: news page -->

We set out to build the first AI tutor to teach math and reading to kids ages 4-9.

For AI to actually teach a five-year-old, pedagogy must be baked into the engineering.

A child can't wait for a slow reply, can't read a chat interface, and can't unhear anything a model gets wrong.

We wanted to share some of the learnings that shaped our architectural decisions building a real-time AI tutor.
A 2-second pause in conversation feels different to a child than to a developer, or even to an adult on the phone speaking to an automated agent.

A couple of seconds is enough for a child's attention to wander and for learning to stop.
Good teachers manage this without pausing to think.

They acknowledge a child immediately, even when they hold the answer back to let the child work.

Teaching is matching the right approach to the current moment, and most approaches aren't answers.
When we set out to build an AI tutor for children ages 4-9, we wanted to build a tutor that actually teaches and not just a chatbot that responds quickly.

We knew the constraint underneath would be hard, and that it wasn't optional: sub-second response on every turn.

Most agents trade off speed for quality through reasoning budgets.

Our architecture has to ground the tutor in pedagogy and respond to the child in real-time.
We threw out the standard agent loop.
A teacher is constantly deciding how to engage a student, whether to say something, draw on the whiteboard, play a game, or change topics entirely.

The standard pattern for an agent today is a tool loop.

The LLM outputs one or more tool calls, waits for them to execute, observes the results, and decides what to do next.

So the straightforward way to build a teaching agent is to make a tool for each action a teacher could take.
But the tool loop has a latency problem.

Frontier models take 2–3 seconds to produce their first token, then decode at around 30 tokens per second.

Our actions average a few dozen tokens.

Add round-trip latency and audio playback, and a standard loop means 3-4 seconds of downtime between each sentence or change on the screen.
In one of our earlier playtests we watched it happen in real time.

A six-year-old boy waited for the agent to think, then asked:
Another child in the same round of playtests figured out she only needed to pay attention part of the time and could still keep up.

Latency had taught her to tune the tutor out.

That was also the moment she stopped learning.
The convenient fix would be a smaller, faster model.

That's where a scope problem shows up.

Teaching is a broad task.

A tutor might pick between dozens of actions in a single lesson, and the hardest call is often to withhold the answer and give a hint, ask a smaller question, or let the child struggle just enough that the insight is theirs when it lands.

## 🔗 原始来源

如果你要核对细节，可以再看原文：
[Hacker News AI原文链接](https://www.ello.com/blog/teaching-a-child-in-1000-ms)

