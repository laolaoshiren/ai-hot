#!/usr/bin/env python3
"""每日精选 v2 - 从工具+模型+项目中选，不再只看项目"""

import os
import json
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def select_daily_spotlight():
    candidates = []

    # 从精选工具中选
    tools_path = os.path.join(DATA_DIR, "tools.json")
    if os.path.exists(tools_path):
        with open(tools_path) as f:
            tools = json.load(f)
        for t in tools:
            if t.get("featured"):
                candidates.append({
                    "id": t.get("id", ""),
                    "name": t["name"],
                    "url": t.get("url", ""),
                    "type": "tool",
                    "description": t.get("description", ""),
                    "pricing": t.get("pricing", ""),
                    "category": t.get("category", ""),
                })

    # 从 Agent 中选
    agents_path = os.path.join(DATA_DIR, "agents.json")
    if os.path.exists(agents_path):
        with open(agents_path) as f:
            agents = json.load(f)
        for a in agents:
            candidates.append({
                "name": a["name"],
                "url": a.get("url", ""),
                "type": "agent",
                "description": a.get("description", ""),
                "pricing": a.get("pricing", ""),
                "category": a.get("type", ""),
            })

    if not candidates:
        return "无候选数据"

    # 用日期做种子，每天固定
    day_seed = datetime.now().timetuple().tm_yday
    idx = day_seed % len(candidates)
    selected = candidates[idx]

    # 选3个备选
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

    return f"今日精选: {selected['name']} ({selected['type']})"
