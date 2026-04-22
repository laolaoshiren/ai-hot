#!/usr/bin/env python3
"""API 新闻采集 (HN / Reddit / V2EX)"""

import os
import json
from datetime import datetime

from news_rss import strip_html, is_ai_related

try:
    import requests
except ImportError:
    os.system("pip install requests -q")
    import requests

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def collect_hn():
    items = []
    try:
        url = "https://hn.algolia.com/api/v1/search"
        params = {"query": "AI", "tags": "story", "hitsPerPage": 30}
        resp = requests.get(url, params=params, timeout=15)
        data = resp.json()
        source_conf = {"name": "Hacker News", "ai_only": False}
        for hit in data.get("hits", []):
            title = strip_html(hit.get("title", ""))
            summary = strip_html(hit.get("story_text", "") or hit.get("comment_text", "") or "")
            if not is_ai_related(title, summary, source_conf):
                continue
            items.append({
                "id": f"hn-{hit['objectID']}",
                "title": title,
                "url": hit.get("url") or f"https://news.ycombinator.com/item?id={hit['objectID']}",
                "source": "Hacker News",
                "lang": "en",
                "published": hit.get("created_at", ""),
                "summary": summary,
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
            source_conf = {"name": f"r/{sub}", "ai_only": False}
            for post in data.get("data", {}).get("children", []):
                d = post["data"]
                title = strip_html(d.get("title", ""))
                summary = strip_html(d.get("selftext", "") or "")
                if not is_ai_related(title, summary, source_conf):
                    continue
                items.append({
                    "id": f"reddit-{d['id']}",
                    "title": title,
                    "url": f"https://reddit.com{d.get('permalink', '')}",
                    "source": f"r/{sub}",
                    "lang": "en",
                    "published": datetime.fromtimestamp(d.get("created_utc", 0)).isoformat(),
                    "summary": summary,
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
        source_conf = {"name": "V2EX", "ai_only": False}
        for topic in resp.json():
            title = strip_html(topic.get("title", ""))
            summary = strip_html(topic.get("content", "") or "")
            if is_ai_related(title, summary, source_conf):
                items.append({
                    "id": f"v2ex-{topic['id']}",
                    "title": title,
                    "url": topic.get("url", ""),
                    "source": "V2EX",
                    "lang": "zh",
                    "published": topic.get("created", ""),
                    "summary": summary,
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

    combined = []
    seen_ids = set()
    for item in existing + new_items:
        item_id = item.get("id")
        if not item_id or item_id in seen_ids:
            continue
        title = strip_html(item.get("title", ""))
        summary = strip_html(item.get("summary", "") or item.get("ai_summary", ""))
        source_conf = {"name": item.get("source", "API"), "ai_only": False}
        if not is_ai_related(title, summary, source_conf):
            continue
        item["title"] = title
        item["summary"] = summary
        combined.append(item)
        seen_ids.add(item_id)

    combined.sort(key=lambda x: x.get("published") or "", reverse=True)
    combined = combined[:500]

    with open(news_path, "w", encoding="utf-8") as f:
        json.dump(combined, f, ensure_ascii=False, indent=2)

    return f"{len(new_items)} 条新新闻 (总计 {len(combined)})"
