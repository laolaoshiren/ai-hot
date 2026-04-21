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
    
    # 取最近20条新闻
    recent_news = news[:20]
    
    # 简单快报：统计信息
    sources = {}
    for item in recent_news:
        source = item.get("source", "未知")
        sources[source] = sources.get(source, 0) + 1
    
    briefing = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "content": f"今日共收录 {len(recent_news)} 条 AI 新闻，主要来源：{', '.join(sources.keys())}",
        "news_count": len(recent_news),
        "sources": sources
    }
    
    with open(briefing_path, "w", encoding="utf-8") as f:
        json.dump(briefing, f, ensure_ascii=False, indent=2)
    
    return f"生成每日快报（{len(recent_news)} 条新闻）"


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
