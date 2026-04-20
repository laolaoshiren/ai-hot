#!/usr/bin/env python3
"""HuggingFace 模型发现"""

import os
import json
from datetime import datetime

try:
    import requests
except ImportError:
    os.system("pip install requests -q")
    import requests

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

HF_ENDPOINTS = [
    {"name": "trending", "url": "https://huggingface.co/api/models?sort=likes7d&limit=50"},
    {"name": "newest", "url": "https://huggingface.co/api/models?sort=createdAt&direction=-1&limit=50"},
    {"name": "text-gen", "url": "https://huggingface.co/api/models?pipeline_tag=text-generation&sort=likes7d&limit=30"},
    {"name": "text-to-image", "url": "https://huggingface.co/api/models?pipeline_tag=text-to-image&sort=downloads&limit=20"},
]


def discover_hf_models():
    existing = []
    models_path = os.path.join(DATA_DIR, "models.json")
    if os.path.exists(models_path):
        with open(models_path) as f:
            existing = json.load(f)

    existing_ids = {m["id"] for m in existing}
    new_models = []

    for ep in HF_ENDPOINTS:
        try:
            resp = requests.get(ep["url"], timeout=20)
            if resp.status_code != 200:
                print(f"  ⚠️ HF {ep['name']} 返回 {resp.status_code}")
                continue
            for model in resp.json():
                mid = f"hf-{model['id'].replace('/', '--')}"
                if mid in existing_ids:
                    continue

                new_models.append({
                    "id": mid,
                    "name": model["id"],
                    "display_name": model.get("id", "").split("/")[-1],
                    "url": f"https://huggingface.co/{model['id']}",
                    "author": model.get("id", "").split("/")[0] if "/" in model.get("id", "") else "",
                    "pipeline_tag": model.get("pipeline_tag", ""),
                    "likes": model.get("likes", 0),
                    "downloads": model.get("downloads", 0),
                    "tags": model.get("tags", []),
                    "created_at": model.get("createdAt", ""),
                    "source": f"hf-{ep['name']}",
                    "collected_at": datetime.now().isoformat(),
                })
                existing_ids.add(mid)
        except Exception as e:
            print(f"  ⚠️ HF {ep['name']} 失败: {e}")

    combined = existing + new_models
    combined.sort(key=lambda x: x.get("likes", 0), reverse=True)
    combined = combined[:1000]

    with open(models_path, "w", encoding="utf-8") as f:
        json.dump(combined, f, ensure_ascii=False, indent=2)

    return f"{len(new_models)} 个新模型 (总计 {len(combined)})"
