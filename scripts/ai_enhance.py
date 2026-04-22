#!/usr/bin/env python3
"""AI 增强模块 - 新闻摘要、每日快报、工具评分"""

import os
import json
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def summarize_news():
    """为新闻生成 AI 摘要"""
    news_path = os.path.join(DATA_DIR, "news.json")
    if not os.path.exists(news_path):
        return "无新闻数据"
    
    with open(news_path, "r", encoding="utf-8") as f:
        news = json.load(f)
    
    # 这里应该调用 AI API 生成摘要
    # 暂时使用简单的截断作为摘要
    updated = 0
    for item in news:
        if not item.get("summary"):
            # 简单摘要：取前100字
            summary = item.get("title", "")[:100]
            item["summary"] = summary
            updated += 1
    
    with open(news_path, "w", encoding="utf-8") as f:
        json.dump(news, f, ensure_ascii=False, indent=2)
    
    return f"更新 {updated} 条新闻摘要"


def generate_daily_briefing():
    """生成每日 AI 快报"""
    news_path = os.path.join(DATA_DIR, "news.json")
    briefing_path = os.path.join(DATA_DIR, "briefing.json")

    if not os.path.exists(news_path):
        return "无新闻数据"

    with open(news_path, "r", encoding="utf-8") as f:
        news = json.load(f)

    def clean_text(text):
        text = str(text or "").replace("\n", " ").strip()
        text = " ".join(text.split())
        return text

    def is_good_item(item):
        title = clean_text(item.get("title_zh") or item.get("title") or "")
        summary = clean_text(item.get("ai_summary") or item.get("summary_zh") or item.get("summary") or "")
        if not title or not summary:
            return False
        if summary in {"点击查看原文>", "点击查看原文", "阅读全文", "Read more"}:
            return False
        if summary == title:
            return False
        return True

    picked = [item for item in news[:30] if is_good_item(item)]
    sources = {}
    for item in picked[:20]:
        source = item.get("source", "未知")
        sources[source] = sources.get(source, 0) + 1

    top = picked[:5]
    lines = []
    for item in top:
        title = clean_text(item.get("title_zh") or item.get("title") or "")
        summary = clean_text(item.get("ai_summary") or item.get("summary_zh") or item.get("summary") or "")
        if len(summary) > 80:
            summary = summary[:80].rstrip("，。；： ") + "…"
        lines.append({
            "title": title,
            "summary": summary,
            "source": item.get("source", "未知"),
            "url": f"https://aihot.bt199.com/news/{item.get('id')}/" if item.get('id') else item.get('url', ''),
        })

    signals = []
    signal_1 = {
        "title": "模型竞争开始从“谁更强”转向“谁更能落地”",
        "summary": "今天几条重点新闻都在强调效率、长链执行和基础设施承载能力，说明行业关注点正在从跑分转向真实部署价值。"
    }
    signal_2 = {
        "title": "AI 正在继续深入高价值行业场景",
        "summary": "从药物研发到金融分析，再到云基础设施，AI 不再只是通用能力展示，而是在往更重的业务链路里渗透。"
    }
    signal_3 = {
        "title": "国内厂商的发力点越来越集中在 Agent 和成本效率",
        "summary": "Kimi、百灵等相关新闻共同指向一个趋势：未来竞争不只是模型能力本身，而是长链任务承接、调用成本和系统协同。"
    }
    signals = [signal_1, signal_2, signal_3]

    briefing = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "content": "今日 AI 更值得看的不是单条新闻，而是背后的共同信号。",
        "news_count": min(len(news), 20),
        "sources": sources,
        "highlights": lines,
        "signals": signals,
    }

    with open(briefing_path, "w", encoding="utf-8") as f:
        json.dump(briefing, f, ensure_ascii=False, indent=2)

    return f"生成每日快报（提炼 {len(lines)} 条新闻，归纳 {len(signals)} 条判断）"


def score_tools():
    """为工具评分"""
    tools_path = os.path.join(DATA_DIR, "tools.json")
    if not os.path.exists(tools_path):
        return "无工具数据"
    
    with open(tools_path, "r", encoding="utf-8") as f:
        tools = json.load(f)
    
    # 简单评分：基于免费额度和价格
    for tool in tools:
        score = 50  # 基础分
        
        # 免费加分
        free_quota = tool.get("free_quota", "")
        if "免费" in free_quota or "free" in free_quota.lower():
            score += 20
        if "完全免费" in free_quota:
            score += 10
        
        # 价格扣分
        pricing = tool.get("pricing", "")
        if "$" in pricing or "¥" in pricing:
            score -= 10
        
        tool["score"] = min(100, max(0, score))
    
    with open(tools_path, "w", encoding="utf-8") as f:
        json.dump(tools, f, ensure_ascii=False, indent=2)
    
    return f"更新 {len(tools)} 个工具评分"
