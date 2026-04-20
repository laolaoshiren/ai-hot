#!/usr/bin/env python3
"""每日精选 - 自动选择今日推荐"""

import os
import json
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def select_daily_spotlight():
    projects_path = os.path.join(DATA_DIR, "projects.json")
    models_path = os.path.join(DATA_DIR, "models.json")

    candidates = []

    # 从项目中选
    if os.path.exists(projects_path):
        with open(projects_path) as f:
            projects = json.load(f)
        for p in projects[:50]:
            if p.get("description"):
                candidates.append({
                    "name": p.get("display_name") or p.get("name", ""),
                    "url": p.get("url", ""),
                    "type": "project",
                    "description": p.get("description", ""),
                    "stars": p.get("stars", 0),
                    "language": p.get("language", ""),
                })

    # 从模型中选
    if os.path.exists(models_path):
        with open(models_path) as f:
            models = json.load(f)
        for m in models[:30]:
            candidates.append({
                "name": m.get("name", ""),
                "url": m.get("url", ""),
                "type": "model",
                "description": f"Pipeline: {m.get('pipeline_tag', 'N/A')}",
                "likes": m.get("likes", 0),
            })

    if not candidates:
        return "无候选数据"

    # 用日期作为种子，每天固定选同一个
    day_seed = datetime.now().timetuple().tm_yday
    idx = day_seed % len(candidates)
    selected = candidates[idx]

    # 同时选 3 个备选
    alternates = []
    for i in range(1, 4):
        alt_idx = (day_seed + i * 37) % len(candidates)
        alternates.append(candidates[alt_idx])

    output = {
        "updated_at": datetime.now().isoformat(),
        "date": datetime.now().strftime("%Y-%m-%d"),
        "spotlight": selected,
        "alternates": alternates,
    }

    spotlight_path = os.path.join(DATA_DIR, "daily.json")
    with open(spotlight_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    return f"今日精选: {selected['name']}"
