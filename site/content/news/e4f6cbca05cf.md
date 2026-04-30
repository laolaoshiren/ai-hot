+++
title = "Slack 长时运行多智能体系统的上下文管理方案"
description = "Slack 长时运行多智能体系统的上下文管理方案。来源：InfoQ AI。"
seo_title = "Slack 长时运行多智能体系统的上下文管理方案｜AI资讯解读 - AI热榜"
seo_description = "Slack 长时运行多智能体系统的上下文管理方案。来源：InfoQ AI。"
seo_keywords = "Slack 长时运行多智能体系统的上下文管理方案, InfoQ AI, AI新闻, AI资讯, AI热榜"
slug = "e4f6cbca05cf"
type = "news"

[params]
id = "e4f6cbca05cf"
name = "Slack 长时运行多智能体系统的上下文管理方案"
title_en = "Slack 长时运行多智能体系统的上下文管理方案"
original_url = "https://www.infoq.cn/article/v51PWObFB4xuqM2lkMpg?utm_source=rss&utm_medium=article"
source = "InfoQ AI"
published = "2026-04-30T13:00:00"
lang = "zh"
intro = "Slack 长时运行多智能体系统的上下文管理方案。来源：InfoQ AI。"
ai_summary = ""
summary = ""
summary_zh = ""
tags = []
list_page = 2
+++

<!-- AUTO-GENERATED: news page -->

为了在长时间运行的智能体系统中保持效率，Slack 工程师放弃了累积聊天记录的做法，转而采用
结构化记忆、验证与蒸馏事实
的方式来维持长时间运行智能体系统的连贯性与准确性。

虽然短时间的 LLM 会话通常不需要显式的上下文管理，但在长时间运行的会话中，要保持会话连贯性，上下文管理就变得至关重要——因为随着消息历史不断增加，每次请求都附带完整上下文会变得不切实际：
智能体框架会在 API 调用之间累积消息历史，以此为用户解决状态管理问题。

但这会占用并填满智能体的上下文窗口，而上下文窗口对智能体可处理的信息总量存在硬性上限。

即便只是接近上下文窗口的容量上限，也可能降低响应质量。

正如 Slack 高级软件工程师 Dominic Marks 所介绍的，Slack 的一款多智能体应用可跨越数百次请求，并生成数兆字节的输出。

为应对这类复杂场景，他们采用了由三类互补上下文通道组成的方案：Director 日志（用于存储 Director 的结构化工作记忆）、Critic 评审（用于存储附带可信度评分的注释与结论报告）和 Critic 时间线（用于存储按时间排序、标注可信度评分的关键信息）。

Slack 采用了
协调器/调度器式多智能体设计
，中央协调器作为决策核心，负责接收各类请求，并将任务分派至下游智能体，也就是专家（Expert）与评审员（Critic）。

Critic 会对 Expert 的工作进行评估，因为部分结论“可能存在编造或严重曲解了数据”。

他们接收 Expert 提交的摘要报告并核验报告中的相关依据。

这一个评估工作是创建评分系统的基础，用于筛选出经多方信息交叉验证的结果。

## 🔗 原始来源

如果你要核对细节，可以再看原文：
[InfoQ AI原文链接](https://www.infoq.cn/article/v51PWObFB4xuqM2lkMpg?utm_source=rss&utm_medium=article)

