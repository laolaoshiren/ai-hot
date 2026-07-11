+++
title = "重磅！AWS 推出开源框架 Blocks，面向 AI 智能体的后端开发工具"
description = "重磅！AWS 推出开源框架 Blocks，面向 AI 智能体的后端开发工具。来源：InfoQ AI。"
seo_title = "重磅！AWS 推出开源框架 Blocks，面向 AI 智能体的后端开发工具｜AI资讯解读 - AI热榜"
seo_description = "重磅！AWS 推出开源框架 Blocks，面向 AI 智能体的后端开发工具。来源：InfoQ AI。"
seo_keywords = "重磅！AWS 推出开源框架 Blocks，面向 AI 智能体的后端开发工具, InfoQ AI, AI新闻, AI资讯, AI热榜"
slug = "e47a7e7be0cd"
type = "news"

[params]
id = "e47a7e7be0cd"
name = "重磅！AWS 推出开源框架 Blocks，面向 AI 智能体的后端开发工具"
title_en = "重磅！AWS 推出开源框架 Blocks，面向 AI 智能体的后端开发工具"
original_url = "https://www.infoq.cn/article/ZdA3CGtWNFGAoalSeiu8?utm_source=rss&utm_medium=article"
source = "InfoQ AI"
published = "2026-06-29T14:00:00"
lang = "zh"
intro = "重磅！AWS 推出开源框架 Blocks，面向 AI 智能体的后端开发工具。来源：InfoQ AI。"
ai_summary = ""
summary = ""
summary_zh = ""
tags = []
list_page = 61
+++

<!-- AUTO-GENERATED: news page -->

亚马逊云科技近期推出
Blocks
公开预览版，这是一款开源 TypeScript 框架，框架中每个 “Block” 都打包了应用程序代码、本地开发实现以及该应用上线生产环境所需的 AWS 基础设施资源。

开发者只需运行
npm run dev
就能在本地获得一个包含 Postgres、身份认证、实时消息和文件存储的应用，且无需使用 AWS 账户。

部署时，同一份代码无需任何修改即可运行在 Lambda、DynamoDB、Aurora、API Gateway 和 Bedrock 上。

官方公告
称，该框架免去了开发者学习各类基础设施工具的门槛。

Blocks 与众多后端框架的区别在于一个根植于 2026 年行业现状的设计理念：AI 智能体编写代码，而框架从一开始就提供规范、标准的代码编写范式。

Blocks 内置了引导文件，无需额外自定义配置就能引导代码智能体输出架构合规的代码。

开发者可以提示智能体“添加身份认证和数据库”，智能体生成的代码既能在本地运行，也能部署到生产级 AWS 服务，因为框架会约束智能体，使其严格遵循标准开发模式。

它的组合模型设计简洁易懂。

每一个 Block 都是独立的 npm 包，分别对应一项后端能力：数据表、用户身份认证、AI 智能体、文件上传、后台任务、定时任务、实时通知以及邮件服务。

开发者按需引入各类 Block 并自由组合，框架便会按照行业最佳实践自动生成对应的 AWS 基础设施。

除此之外，该框架无需额外代码生成步骤即可将类型安全从数据模型贯通至前端；仅依靠一套后端定义，就能适配各类 Web 框架（Next.js、Nuxt、Astro、React、Vue、Svelte、Angular）与原生客户端（Swift、Kotlin、Dart/Flutter）。

## 🔗 原始来源

如果你要核对细节，可以再看原文：
[InfoQ AI原文链接](https://www.infoq.cn/article/ZdA3CGtWNFGAoalSeiu8?utm_source=rss&utm_medium=article)

