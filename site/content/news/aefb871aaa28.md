+++
title = "最新动态：GKE 安全蓝图加入云厂商 AI 安全框架阵营"
description = "最新动态：GKE 安全蓝图加入云厂商 AI 安全框架阵营。来源：InfoQ AI。"
seo_title = "最新动态：GKE 安全蓝图加入云厂商 AI 安全框架阵营｜AI资讯解读 - AI热榜"
seo_description = "最新动态：GKE 安全蓝图加入云厂商 AI 安全框架阵营。来源：InfoQ AI。"
seo_keywords = "最新动态：GKE 安全蓝图加入云厂商 AI 安全框架阵营, InfoQ AI, AI新闻, AI资讯, AI热榜"
slug = "aefb871aaa28"
type = "news"

[params]
id = "aefb871aaa28"
name = "最新动态：GKE 安全蓝图加入云厂商 AI 安全框架阵营"
title_en = "最新动态：GKE 安全蓝图加入云厂商 AI 安全框架阵营"
original_url = "https://www.infoq.cn/article/DXKamMhJKJeV7CkeExzo?utm_source=rss&utm_medium=article"
source = "InfoQ AI"
published = "2026-07-24T18:00:00"
lang = "zh"
intro = "最新动态：GKE 安全蓝图加入云厂商 AI 安全框架阵营。来源：InfoQ AI。"
ai_summary = ""
summary = ""
summary_zh = ""
tags = []
list_page = 1
+++

<!-- AUTO-GENERATED: news page -->

谷歌云发布了一份新的安全蓝图，介绍企业应如何保护运行在 Google Kubernetes Engine（GKE） 上的人工智能工作负载。

谷歌认为，AI 应用从原型阶段走向生产环境的速度，已经超过了传统安全模型的适应能力。

这份
文档由 Glen Messenger 和 Shannon Kularathna 撰写
，提出了一套覆盖基础设施安全、模型完整性以及应用安全的三层安全方案，目标读者主要是首席信息安全官（CISO）以及平台工程团队。

GKE 安全团队的群产品经理 Messenger 表示，团队需要“保护专有模型权重，防御 Prompt Injection 等新型应用层威胁，同时满足严格的监管合规要求，而且不能拖慢 AI 开发团队的速度。

”该蓝图认为，实现这些目标不能仅依赖一个运行容器的平台，而需要一个能够“开箱即用地叠加多层安全能力”的平台。

在基础设施层面，蓝图建议使用 Confidential GKE Nodes。

该能力可以将硬件级内存加密扩展到包括英伟达 H100 GPU 和 TPU 在内的计算加速器。

此外，结合 Workload Identity Federation（允许推理 Pod 从 Cloud Storage 获取模型权重，而无需长期保存密钥）以及 VPC Service Controls，管理员可以围绕受监管数据建立安全边界。

你不能在一个不安全的集群上运行安全的 AI 工作负载。

——Google Cloud GKE 团队，《
Securing AI at Enterprise Scale: The Google Kubernetes Engine Blueprint
（大规模企业 AI 安全实践：Google Kubernetes Engine 安全蓝图）》

## 🔗 原始来源

如果你要核对细节，可以再看原文：
[InfoQ AI原文链接](https://www.infoq.cn/article/DXKamMhJKJeV7CkeExzo?utm_source=rss&utm_medium=article)

