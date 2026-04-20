#!/usr/bin/env python3
"""RSS 新闻采集器"""

import os
import json
import hashlib
from datetime import datetime, timedelta

try:
    import feedparser
except ImportError:
    print("  安装 feedparser...")
    os.system("pip install feedparser -q")
    import feedparser

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
RSS_SOURCES = [
    {"name": "机器之心", "url": "https://www.jiqizhixin.com/feed", "lang": "zh"},
    {"name": "IT之家", "url": "https://www.ithome.com/rss/", "lang": "zh"},
    {"name": "36氪", "url": "https://36kr.com/feed", "lang": "zh"},
    {"name": "TechCrunch AI", "url": "https://techcrunch.com/category/artificial-intelligence/feed/", "lang": "en"},
    {"name": "The Verge AI", "url": "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml", "lang": "en"},
    {"name": "MIT Tech Review", "url": "https://www.technologyreview.com/feed/", "lang": "en"},
]


def collect_rss_news():
    all_news = []
    cutoff = datetime.now() - timedelta(days=7)

    for source in RSS_SOURCES:
        try:
            feed = feedparser.parse(source["url"])
            for entry in feed.entries[:20]:
                published = None
                if hasattr(entry, "published_parsed") and entry.published_parsed:
                    published = datetime(*entry.published_parsed[:6])

                if published and published < cutoff:
                    continue

                news_id = hashlib.md5(entry.link.encode()).hexdigest()[:12]
                all_news.append({
                    "id": news_id,
                    "title": entry.title,
                    "url": entry.link,
                    "source": source["name"],
                    "lang": source["lang"],
                    "published": published.isoformat() if published else None,
                    "summary": entry.get("summary", "")[:200],
                    "collected_at": datetime.now().isoformat(),
                })
        except Exception as e:
            print(f"  ⚠️ {source['name']} 失败: {e}")

    # 合并已有数据
    existing = []
    news_path = os.path.join(DATA_DIR, "news.json")
    if os.path.exists(news_path):
        with open(news_path) as f:
            existing = json.load(f)

    # 去重
    existing_ids = {n["id"] for n in existing}
    new_items = [n for n in all_news if n["id"] not in existing_ids]

    # 只保留最近7天
    combined = existing + new_items
    combined.sort(key=lambda x: x.get("published") or "", reverse=True)
    combined = combined[:500]

    with open(news_path, "w", encoding="utf-8") as f:
        json.dump(combined, f, ensure_ascii=False, indent=2)

    return f"{len(new_items)} 条新新闻 (总计 {len(combined)})"
