#!/usr/bin/env python3
"""API 新闻采集 (HN / Reddit / V2EX)"""

import os
import json
import hashlib
from datetime import datetime, timedelta

try:
    import requests
except ImportError:
    os.system("pip install requests -q")
    import requests

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
AI_KEYWORDS = ["ai", "gpt", "llm", "claude", "openai", "anthropic", "deepseek",
               "machine learning", "neural", "transformer", "diffusion", "agent",
               "人工智能", "大模型", "智能体"]


def is_ai_related(text):
    text_lower = text.lower()
    return any(kw in text_lower for kw in AI_KEYWORDS)


def collect_hn():
    items = []
    try:
        url = "https://hn.algolia.com/api/v1/search"
        params = {"query": "AI", "tags": "story", "hitsPerPage": 30}
        resp = requests.get(url, params=params, timeout=15)
        data = resp.json()
        for hit in data.get("hits", []):
            if not is_ai_related(hit.get("title", "")):
                continue
            items.append({
                "id": f"hn-{hit['objectID']}",
                "title": hit.get("title", ""),
                "url": hit.get("url") or f"https://news.ycombinator.com/item?id={hit['objectID']}",
                "source": "Hacker News",
                "lang": "en",
                "published": hit.get("created_at", ""),
                "points": hit.get("points", 0),
                "collected_at": datetime.now().isoformat(),
            })
    except Exception as e:
        print(f"  ⚠️ HN 失败: {e}")
    return items


def collect_reddit():
    items = []
    subreddits = ["MachineLearning", "LocalLLaMA", "artificial"]
    headers = {"User-Agent": "AI-Hot-Bot/1.0"}
    for sub in subreddits:
        try:
            url = f"https://www.reddit.com/r/{sub}/hot.json?limit=15"
            resp = requests.get(url, headers=headers, timeout=15)
            data = resp.json()
            for post in data.get("data", {}).get("children", []):
                d = post["data"]
                items.append({
                    "id": f"reddit-{d['id']}",
                    "title": d.get("title", ""),
                    "url": f"https://reddit.com{d.get('permalink', '')}",
                    "source": f"r/{sub}",
                    "lang": "en",
                    "published": datetime.fromtimestamp(d.get("created_utc", 0)).isoformat(),
                    "points": d.get("score", 0),
                    "collected_at": datetime.now().isoformat(),
                })
        except Exception as e:
            print(f"  ⚠️ Reddit r/{sub} 失败: {e}")
    return items


def collect_v2ex():
    items = []
    try:
        url = "https://www.v2ex.com/api/topics/hot.json"
        resp = requests.get(url, timeout=15)
        for topic in resp.json():
            if is_ai_related(topic.get("title", "")):
                items.append({
                    "id": f"v2ex-{topic['id']}",
                    "title": topic.get("title", ""),
                    "url": topic.get("url", ""),
                    "source": "V2EX",
                    "lang": "zh",
                    "published": topic.get("created", ""),
                    "collected_at": datetime.now().isoformat(),
                })
    except Exception as e:
        print(f"  ⚠️ V2EX 失败: {e}")
    return items


def collect_api_news():
    all_news = []
    all_news.extend(collect_hn())
    all_news.extend(collect_reddit())
    all_news.extend(collect_v2ex())

    # 合并去重
    existing = []
    news_path = os.path.join(DATA_DIR, "news.json")
    if os.path.exists(news_path):
        with open(news_path) as f:
            existing = json.load(f)

    existing_ids = {n["id"] for n in existing}
    new_items = [n for n in all_news if n["id"] not in existing_ids]

    combined = existing + new_items
    combined.sort(key=lambda x: x.get("published") or "", reverse=True)
    combined = combined[:500]

    with open(news_path, "w", encoding="utf-8") as f:
        json.dump(combined, f, ensure_ascii=False, indent=2)

    return f"{len(new_items)} 条新新闻 (总计 {len(combined)})"
