#!/usr/bin/env python3
"""链接健康检查"""

import os
import json
from datetime import datetime

try:
    import requests
except ImportError:
    os.system("pip install requests -q")
    import requests

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def check_url(url, timeout=10):
    try:
        resp = requests.head(url, timeout=timeout, allow_redirects=True,
                             headers={"User-Agent": "Mozilla/5.0"})
        return resp.status_code
    except:
        return 0


def quick_check():
    """快速检查 - 只检查最近新增的条目"""
    files_to_check = ["projects.json", "models.json", "tools.json"]
    broken = []

    for fname in files_to_check:
        fpath = os.path.join(DATA_DIR, fname)
        if not os.path.exists(fpath):
            continue
        with open(fpath) as f:
            items = json.load(f)

        # 只检查最近添加的 20 个
        recent = items[:20]
        for item in recent:
            url = item.get("url", "")
            if not url:
                continue
            status = check_url(url)
            if status >= 400 or status == 0:
                broken.append({
                    "id": item.get("id", ""),
                    "name": item.get("name", ""),
                    "url": url,
                    "status": status,
                    "file": fname,
                })

    # 记录坏链
    if broken:
        broken_path = os.path.join(DATA_DIR, "broken_links.json")
        existing_broken = []
        if os.path.exists(broken_path):
            with open(broken_path) as f:
                existing_broken = json.load(f)
        existing_broken.extend(broken)
        # 只保留最近 200 条
        existing_broken = existing_broken[-200:]
        with open(broken_path, "w", encoding="utf-8") as f:
            json.dump(existing_broken, f, ensure_ascii=False, indent=2)

    return f"检查完成, {len(broken)} 个坏链"
