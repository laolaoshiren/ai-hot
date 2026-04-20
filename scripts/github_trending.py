#!/usr/bin/env python3
"""GitHub 热度追踪 - 记录 stars 变化计算加速度"""

import os
import json
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def track_github_trending():
    projects_path = os.path.join(DATA_DIR, "projects.json")
    trending_path = os.path.join(DATA_DIR, "trending.json")

    if not os.path.exists(projects_path):
        return "无项目数据，跳过"

    with open(projects_path) as f:
        projects = json.load(f)

    # 加载上次的 stars 记录
    prev_trending = {}
    if os.path.exists(trending_path):
        with open(trending_path) as f:
            prev_trending = {t["id"]: t for t in json.load(f).get("rankings", [])}

    now = datetime.now().isoformat()
    rankings = []

    for proj in projects[:200]:  # 只追踪 top 200
        pid = proj["id"]
        current_stars = proj.get("stars", 0)
        prev = prev_trending.get(pid, {})

        prev_stars = prev.get("stars", current_stars)
        prev_time = prev.get("tracked_at")

        velocity = 0
        if prev_time and prev_stars:
            try:
                hours = max(1, (datetime.fromisoformat(now) - datetime.fromisoformat(prev_time)).total_seconds() / 3600)
                velocity = (current_stars - prev_stars) / hours
            except:
                pass

        rankings.append({
            "id": pid,
            "name": proj["name"],
            "display_name": proj.get("display_name", ""),
            "url": proj["url"],
            "description": proj.get("description", ""),
            "stars": current_stars,
            "prev_stars": prev_stars,
            "velocity_per_hour": round(velocity, 2),
            "velocity_per_day": round(velocity * 24, 1),
            "language": proj.get("language", ""),
            "tracked_at": now,
        })

    # 按速度排序
    rankings.sort(key=lambda x: x["velocity_per_day"], reverse=True)

    trending = {
        "updated_at": now,
        "rankings": rankings[:100],
        "top_risers": [r for r in rankings if r["velocity_per_day"] > 10][:20],
    }

    with open(trending_path, "w", encoding="utf-8") as f:
        json.dump(trending, f, ensure_ascii=False, indent=2)

    hot_count = len(trending["top_risers"])
    return f"追踪 {len(rankings)} 个项目, {hot_count} 个热度飙升"
