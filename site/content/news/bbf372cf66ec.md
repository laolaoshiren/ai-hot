+++
title = "重磅！GitHub AI Agent 翻车：攻击者不用黑客技术，只写一句话就能窃取数据"
description = "重磅！GitHub AI Agent 翻车：攻击者不用黑客技术，只写一句话就能窃取数据。来源：InfoQ AI。"
seo_title = "重磅！GitHub AI Agent 翻车：攻击者不用黑客技术，只写一句话就能窃取数据｜AI资讯解读 - AI热榜"
seo_description = "重磅！GitHub AI Agent 翻车：攻击者不用黑客技术，只写一句话就能窃取数据。来源：InfoQ AI。"
seo_keywords = "重磅！GitHub AI Agent 翻车：攻击者不用黑客技术，只写一句话就能窃取数据, InfoQ AI, AI新闻, AI资讯, AI热榜"
slug = "bbf372cf66ec"
type = "news"

[params]
id = "bbf372cf66ec"
name = "重磅！GitHub AI Agent 翻车：攻击者不用黑客技术，只写一句话就能窃取数据"
title_en = "重磅！GitHub AI Agent 翻车：攻击者不用黑客技术，只写一句话就能窃取数据"
original_url = "https://www.infoq.cn/article/u4rDqep8zVWUJsqVoQ23?utm_source=rss&utm_medium=article"
source = "InfoQ AI"
published = "2026-07-31T12:00:00"
lang = "zh"
intro = "重磅！GitHub AI Agent 翻车：攻击者不用黑客技术，只写一句话就能窃取数据。来源：InfoQ AI。"
ai_summary = ""
summary = ""
summary_zh = ""
tags = []
list_page = 117
+++

<!-- AUTO-GENERATED: news page -->

GitLost
是由 Noma Security 发现的一种提示注入漏洞利用方式，它能够诱骗 GitHub 新推出的
Agentic Workflows
泄露私有数据。

攻击者只需在公开 GitHub Issue 中嵌入隐藏指令，就可以绕过安全防护措施，诱导 AI Agent 在公开评论中泄露机密信息。

Noma Labs 发现的这一存在漏洞的 GitHub Agentic Workflow，被配置为在
issues.assigned
事件触发时运行，读取 Issue 标题和正文，通过
add-comment
工具发布回复评论，并且拥有读取组织内其他仓库（包括公开仓库和私有仓库）的权限。

为了利用这一漏洞，攻击者不需要任何编程技能、访问权限或凭据。

攻击者只需要在一个使用 GitHub Agentic Workflow 配置的组织所属公开仓库中创建一个 Issue，然后等待即可。

## 🔗 原始来源

如果你要核对细节，可以再看原文：
[InfoQ AI原文链接](https://www.infoq.cn/article/u4rDqep8zVWUJsqVoQ23?utm_source=rss&utm_medium=article)

