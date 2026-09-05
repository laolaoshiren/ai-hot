+++
title = "最新动态：Kubernetes 统治了容器时代，谷歌 Agent Substrate 意在拿下下一个十年"
description = "最新动态：Kubernetes 统治了容器时代，谷歌 Agent Substrate 意在拿下下一个十年。来源：InfoQ AI。"
seo_title = "最新动态：Kubernetes 统治了容器时代，谷歌 Agent Substrate 意在拿下下一个十年｜AI资讯解读 - AI热榜"
seo_description = "最新动态：Kubernetes 统治了容器时代，谷歌 Agent Substrate 意在拿下下一个十年。来源：InfoQ AI。"
seo_keywords = "最新动态：Kubernetes 统治了容器时代，谷歌 Agent Substrate 意在拿下下一个十年, InfoQ AI, AI新闻, AI资讯, AI热榜"
slug = "3fdfdecd47eb"
type = "news"

[params]
id = "3fdfdecd47eb"
name = "最新动态：Kubernetes 统治了容器时代，谷歌 Agent Substrate 意在拿下下一个十年"
title_en = "最新动态：Kubernetes 统治了容器时代，谷歌 Agent Substrate 意在拿下下一个十年"
original_url = "https://www.infoq.cn/article/h0WG6p7z3tyTk3hxQIhT?utm_source=rss&utm_medium=article"
source = "InfoQ AI"
published = "2026-07-30T19:50:44"
lang = "zh"
intro = "最新动态：Kubernetes 统治了容器时代，谷歌 Agent Substrate 意在拿下下一个十年。来源：InfoQ AI。"
ai_summary = ""
summary = ""
summary_zh = ""
tags = []
list_page = 129
+++

<!-- AUTO-GENERATED: news page -->

谷歌于 2026 年 5 月份推出 GKE Agent Sandbox，并在公告中介绍了另一个名为 Agent Substrate 的项目。

这两项公告间接承认了一个 Kubernetes 资深人士一直不愿公开点明的事实。

那个曾称霸容器时代的平台并不适合作为 AI 智能体的控制平面。

Agent Sandbox 为智能体提供了一个运行不可信代码的安全环境。

Agent Substrate 则增加了一个调度层，绕过了 Kubernetes 控制平面，因为 API 服务器的设计初衷从未考虑过智能体的行为模式。

如果将智能体比作操作系统中的进程，而不是数据中心里的服务，这种不匹配就显而易见了。

现代操作系统运行着成千上万个进程，它们大部分时间都处于休眠状态。

操作系统会在事件触发时唤醒它们，分配一小片 CPU 时间，然后将它们闲置的内存分页到磁盘，以便为下一个进程腾出空间。

智能体的行为几乎与这些进程完全一致。

Kubernetes 最初是为了管理一组固定的、长期运行的复制服务而设计的。

这种根本性的设计差异解释了为什么现在的智能体基础设施大多是在 Kubernetes 之上运行，而不是像 Deployment 或 StatefulSet 那样作为工作负载被集成到 Kubernetes 中。

智能体作为工作负载的本质
智能体是长期运行、有状态的会话，其生命周期的大部分时间处于空闲状态，被唤醒执行一阵代码后，再次归于沉寂。

它执行的代码是由大模型在运行时生成的。

运行宿主必须默认将其视为不可信的负载。

每个会话都需要一个稳定的身份标识，能够在不丢失内存的情况下暂停和恢复，并且与其他会话实现硬性隔离。

不妨把智能体想象成分时操作系统中的进程。

就像调度器挂起一个休眠进程并在键盘输入到达时立即恢复它一样，智能体运行时环境也必须在会话空闲时将其休眠，并在恢复时保持其工作内存完好无损。

唤醒链路直接决定用户等待时长，因此路径上的每一毫秒延迟都能被感知到。

试想一个开发者在一下午都保持打开状态的编程智能体。

当提示词到达时，它运行 10 秒，然后等待 20 分钟，直到下一个提示词到达。

将这个数字乘以团队中的开发者数量，你就有了成千上万个名义上“活跃”但实际在“沉睡”的会话。

超大规模云厂商已经在朝这个方向布局。

这种具有会话感知能力、隔离的智能体运行时已成为继虚拟机、容器和无服务器计算之后的第四种计算形态。

沉睡数小时的会话
智能体会话的流量突发特性与 Web 服务截然不同。

为每个空闲会话保留一个完整的 Pod 会浪费 Pod 预留的内存和 CPU，这就是为什么新一代运行时会将空闲会话的状态快照从计算资源中剥离。

## 🔗 原始来源

如果你要核对细节，可以再看原文：
[InfoQ AI原文链接](https://www.infoq.cn/article/h0WG6p7z3tyTk3hxQIhT?utm_source=rss&utm_medium=article)

