+++
title = "最新动态：边端AI不只缺算力：安谋科技重做CPU、NPU、VPU与AI操作系统"
description = "最新动态：边端AI不只缺算力：安谋科技重做CPU、NPU、VPU与AI操作系统。来源：InfoQ AI。"
seo_title = "最新动态：边端AI不只缺算力：安谋科技重做CPU、NPU、VPU与AI操作系统｜AI资讯解读 - AI热榜"
seo_description = "最新动态：边端AI不只缺算力：安谋科技重做CPU、NPU、VPU与AI操作系统。来源：InfoQ AI。"
seo_keywords = "最新动态：边端AI不只缺算力：安谋科技重做CPU、NPU、VPU与AI操作系统, InfoQ AI, AI新闻, AI资讯, AI热榜"
slug = "d4ccf84ee66f"
type = "news"

[params]
id = "d4ccf84ee66f"
name = "最新动态：边端AI不只缺算力：安谋科技重做CPU、NPU、VPU与AI操作系统"
title_en = "最新动态：边端AI不只缺算力：安谋科技重做CPU、NPU、VPU与AI操作系统"
original_url = "https://www.infoq.cn/article/iIoJ2qhXbXCH2ozGqCJ6?utm_source=rss&utm_medium=article"
source = "InfoQ AI"
published = "2026-07-19T11:09:02"
lang = "zh"
intro = "最新动态：边端AI不只缺算力：安谋科技重做CPU、NPU、VPU与AI操作系统。来源：InfoQ AI。"
ai_summary = ""
summary = ""
summary_zh = ""
tags = []
list_page = 16
+++

<!-- AUTO-GENERATED: news page -->

7 月 18 日，WAIC 2026 期间，安谋科技在上海世博展览馆举行 AI 前瞻发布会。

与展馆中大量围绕超节点、万卡集群和云端大模型的讨论不同，这场发布会把重点放在了另一端：当 AI 进入嵌入式设备、摄像头、机器人、工业网关和边缘计算节点，有限功耗、有限内存和复杂负载将如何改变芯片与系统设计。

发布会涉及四条技术线：面向嵌入式设备的“星辰”CPU 与 Arm Helium 指令集，面向边端推理的“周易”X3-Pro NPU 架构，面向机器视觉的“玲珑”VPU，以及安谋科技牵头发起的开源 AIOS 联盟。

把这些内容放在一起看，安谋科技这次在 WAIC 上试图回答的是一个更具体的工程问题：在功耗、温度、内存带宽和软件生态都受到约束的情况下，如何让计算、视频和系统软件形成一套可以部署的本地 AI 基础设施。

端侧 AI 的矛盾，不只是模型太大
过去几年，端侧 AI 通常被理解为把云端模型缩小后放进终端。

但这种理解忽略了两类计算环境之间的差异。

云端服务器通常可以通过增加 GPU 数量、显存容量和网络带宽扩展计算资源，而嵌入式设备首先受到电池、散热、芯片面积和成本限制。

摄像头、门锁、可穿戴设备和工业控制器也很难为了运行一个模型，持续占用全部 CPU 资源。

与此同时，端侧任务又对实时性提出了更严格的要求。

云端应用可以等待模型完成数秒推理，但语音唤醒、人脸检测、机器人避障和工业控制往往需要立即响应。

大量视频、音频和传感器数据如果全部上传云端，也会带来网络依赖、带宽成本和数据管理问题。

这意味着，端侧 AI 面对的不是单纯的算力不足，而是性能、功耗、响应时间、带宽和可靠性之间的多重约束。

安谋科技 CPU 产品总监朱晓鸣在现场将端侧计算划分为三类需求：始终在线的低功耗感知、由 CPU 承担的逻辑控制，以及相对复杂的 AI 计算。

在这种架构中，CPU 仍然负责系统控制、实时任务和通用逻辑，向量计算单元和 NPU 则分别承接适合并行处理和矩阵计算的负载。

其目标是让嵌入式设备在有限的功耗和算力下尽可能多的释放 AI 计算潜力。

## 🔗 原始来源

如果你要核对细节，可以再看原文：
[InfoQ AI原文链接](https://www.infoq.cn/article/iIoJ2qhXbXCH2ozGqCJ6?utm_source=rss&utm_medium=article)

