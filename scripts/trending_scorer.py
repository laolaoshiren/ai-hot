#!/usr/bin/env python3
"""热度评分 - 多维度综合计算"""

import os
import json
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def compute_trending():
    trending_path = os.path.join(DATA_DIR, "trending.json")
    news_path = os.path.join(DATA_DIR, "news.json")
    projects_path = os.path.join(DATA_DIR, "projects.json")
    models_path = os.path.join(DATA_DIR, "models.json")

    hot_items = []

    # 1. GitHub 热度飙升
    if os.path.exists(trending_path):
        with open(trending_path) as f:
            trending = json.load(f)
        for item in trending.get("top_risers", []):
            hot_items.append({
                "name": item.get("display_name") or item.get("name", ""),
                "url": item.get("url", ""),
                "type": "project",
                "source": "github",
                "score": min(item.get("velocity_per_day", 0) / 10, 40),
                "stars": item.get("stars", 0),
                "velocity": item.get("velocity_per_day", 0),
                "description": item.get("description", ""),
            })

    # 2. HuggingFace 热门模型
    if os.path.exists(models_path):
        with open(models_path) as f:
            models = json.load(f)
        # 按 likes 排序取 top 20
        models.sort(key=lambda x: x.get("likes", 0), reverse=True)
        for m in models[:20]:
            hot_items.append({
                "name": m.get("name", ""),
                "url": m.get("url", ""),
                "type": "model",
                "source": "huggingface",
                "score": min(m.get("likes", 0) / 50, 30),
                "likes": m.get("likes", 0),
                "description": m.get("pipeline_tag", ""),
            })

    # 3. 新闻热度（按来源权重）
    if os.path.exists(news_path):
        with open(news_path) as f:
            news = json.load(f)
        source_weight = {
            "Hacker News": 10, "机器之心": 8, "36氪": 7,
            "TechCrunch AI": 8, "The Verge AI": 7,
            "r/MachineLearning": 6, "r/LocalLLaMA": 6,
            "V2EX": 5, "IT之家": 5,
        }
        for n in news[:50]:
            weight = source_weight.get(n.get("source", ""), 3)
            hot_items.append({
                "name": n.get("title", ""),
                "url": n.get("url", ""),
                "type": "news",
                "source": n.get("source", ""),
                "score": weight,
                "published": n.get("published", ""),
            })

    # 综合排序
    hot_items.sort(key=lambda x: x.get("score", 0), reverse=True)

    output = {
        "updated_at": datetime.now().isoformat(),
        "total": len(hot_items),
        "hot_list": hot_items[:50],
        "top_10": hot_items[:10],
    }

    hot_path = os.path.join(DATA_DIR, "hot.json")
    with open(hot_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    return f"计算 {len(hot_items)} 条热度, Top 10 已生成"
