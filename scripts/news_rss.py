#!/usr/bin/env python3
"""RSS 新闻采集器 v2 - 清理 HTML，中文优先"""

import os
import json
import re
import hashlib
from datetime import datetime, timedelta

try:
    import feedparser
except ImportError:
    os.system("pip install feedparser -q")
    import feedparser

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

RSS_SOURCES = [
    {"name": "机器之心", "url": "https://www.jiqizhixin.com/feed", "lang": "zh", "priority": 1},
    {"name": "36氪", "url": "https://36kr.com/feed", "lang": "zh", "priority": 2},
    {"name": "IT之家", "url": "https://www.ithome.com/rss/", "lang": "zh", "priority": 3},
    {"name": "TechCrunch AI", "url": "https://techcrunch.com/category/artificial-intelligence/feed/", "lang": "en", "priority": 1},
    {"name": "The Verge AI", "url": "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml", "lang": "en", "priority": 2},
    {"name": "MIT Tech Review", "url": "https://www.technologyreview.com/feed/", "lang": "en", "priority": 2},
]


def strip_html(text):
    """去除 HTML 标签，保留纯文本"""
    if not text:
        return ""
    # 去除 HTML 标签
    text = re.sub(r'<[^>]+>', '', text)
    # 去除多余空白
    text = re.sub(r'\s+', ' ', text).strip()
    # 去除 HTML 实体
    text = text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    text = text.replace('&quot;', '"').replace('&#39;', "'").replace('&nbsp;', ' ')
    return text[:300]  # 截断过长


def collect_rss_news():
    all_news = []
    cutoff = datetime.now() - timedelta(days=3)  # 只保留3天内的

    for source in RSS_SOURCES:
        try:
            feed = feedparser.parse(source["url"])
            count = 0
            for entry in feed.entries[:15]:
                published = None
                if hasattr(entry, "published_parsed") and entry.published_parsed:
                    published = datetime(*entry.published_parsed[:6])

                if published and published < cutoff:
                    continue

                title = strip_html(entry.get("title", ""))
                if not title:
                    continue

                # 清理 summary
                summary = strip_html(entry.get("summary", "") or entry.get("description", ""))

                news_id = hashlib.md5(entry.link.encode()).hexdigest()[:12]
                all_news.append({
                    "id": news_id,
                    "title": title,
                    "url": entry.link,
                    "source": source["name"],
                    "lang": source["lang"],
                    "priority": source["priority"],
                    "published": published.isoformat() if published else None,
                    "summary": summary,
                    "collected_at": datetime.now().isoformat(),
                })
                count += 1
            print(f"  ✓ {source['name']}: {count} 条")
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

    # 合并
    combined = existing + new_items

    # 按发布时间排序，中文优先
    combined.sort(key=lambda x: (
        0 if x.get("lang") == "zh" else 1,  # 中文优先
        x.get("published") or ""  # 时间倒序
    ), reverse=False)
    combined.sort(key=lambda x: x.get("published") or "", reverse=True)

    # 保留最近3天的
    combined = combined[:300]

    with open(news_path, "w", encoding="utf-8") as f:
        json.dump(combined, f, ensure_ascii=False, indent=2)

    return f"{len(new_items)} 条新新闻 (总计 {len(combined)})"
