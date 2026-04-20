#!/usr/bin/env python3
"""热度评分 v2 - 多源聚合，不再只看 HuggingFace"""

import os
import json
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def compute_trending():
    hot_items = []

    # 1. GitHub 热度飙升 (权重最高 - 真实开源项目)
    trending_path = os.path.join(DATA_DIR, "trending.json")
    if os.path.exists(trending_path):
        with open(trending_path) as f:
            trending = json.load(f)
        for item in trending.get("top_risers", []):
            v = item.get("velocity_per_day", 0)
            if v > 0:
                hot_items.append({
                    "name": item.get("display_name") or item.get("name", ""),
                    "url": item.get("url", ""),
                    "type": "project",
                    "source": "GitHub",
                    "score": min(v / 5, 50),
                    "detail": f"⭐ {item.get('stars', 0)} (+{v:.0f}/天)",
                    "description": item.get("description", ""),
                })

    # 2. GitHub 项目 stars 排名 (补充)
    projects_path = os.path.join(DATA_DIR, "projects.json")
    if os.path.exists(projects_path):
        with open(projects_path) as f:
            projects = json.load(f)
        for p in projects[:30]:
            s = p.get("stars", 0)
            if s > 1000:
                hot_items.append({
                    "name": p.get("display_name") or p.get("name", ""),
                    "url": p.get("url", ""),
                    "type": "project",
                    "source": "GitHub",
                    "score": min(s / 2000, 30),
                    "detail": f"⭐ {s}",
                    "description": p.get("description", ""),
                })

    # 3. HuggingFace 热门模型 (有上限，不喧宾夺主)
    models_path = os.path.join(DATA_DIR, "models.json")
    if os.path.exists(models_path):
        with open(models_path) as f:
            models = json.load(f)
        models.sort(key=lambda x: x.get("likes", 0), reverse=True)
        for m in models[:10]:
            hot_items.append({
                "name": m.get("display_name") or m.get("name", ""),
                "url": m.get("url", ""),
                "type": "model",
                "source": "HuggingFace",
                "score": min(m.get("likes", 0) / 100, 20),
                "detail": f"❤️ {m.get('likes', 0)}",
                "description": m.get("pipeline_tag", ""),
            })

    # 4. 新闻热度 (来源加权)
    news_path = os.path.join(DATA_DIR, "news.json")
    if os.path.exists(news_path):
        with open(news_path) as f:
            news = json.load(f)
        # 每个来源只取前3条最热的，避免同一来源霸榜
        source_counts = {}
        for n in news:
            src = n.get("source", "other")
            source_counts[src] = source_counts.get(src, 0) + 1
            if source_counts[src] > 3:
                continue
            weight = {"Hacker News": 12, "机器之心": 10, "36氪": 8,
                      "TechCrunch AI": 10, "The Verge AI": 8,
                      "r/MachineLearning": 8, "r/LocalLLaMA": 7,
                      "V2EX": 6, "IT之家": 5}.get(src, 3)
            points = n.get("points", 0)
            score = weight + min(points / 50, 10)
            hot_items.append({
                "name": n.get("title", ""),
                "url": n.get("url", ""),
                "type": "news",
                "source": src,
                "score": score,
                "detail": f"{src}" + (f" · {points}分" if points else ""),
                "description": "",
            })

    # 5. 工具精选 (把热门工具也加进来)
    tools_path = os.path.join(DATA_DIR, "tools.json")
    if os.path.exists(tools_path):
        with open(tools_path) as f:
            tools = json.load(f)
        for t in tools:
            if t.get("trending"):
                hot_items.append({
                    "name": t["name"],
                    "url": t.get("url", ""),
                    "type": "tool",
                    "source": "精选",
                    "score": 15,
                    "detail": t.get("pricing", ""),
                    "description": t.get("description", ""),
                })

    # 去重 (同名只保留最高分)
    seen = {}
    for item in hot_items:
        key = item["name"][:30]
        if key not in seen or item["score"] > seen[key]["score"]:
            seen[key] = item

    # 综合排序
    ranked = sorted(seen.values(), key=lambda x: x["score"], reverse=True)

    output = {
        "updated_at": datetime.now().isoformat(),
        "total": len(ranked),
        "hot_list": ranked[:50],
        "top_10": ranked[:10],
    }

    hot_path = os.path.join(DATA_DIR, "hot.json")
    with open(hot_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    # 统计来源分布
    sources = {}
    for item in ranked[:20]:
        s = item["source"]
        sources[s] = sources.get(s, 0) + 1

    return f"计算 {len(ranked)} 条热度, Top 10 来源分布: {sources}"
