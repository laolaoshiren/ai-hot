#!/usr/bin/env python3
"""实时关键词采集器 - 中文为主"""

import os
import json
import re
import time
from datetime import datetime

try:
    import requests
except ImportError:
    os.system("pip install requests -q")
    import requests

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

SEED_KEYWORDS = [
    "AI工具", "AI软件", "AI网站", "AI平台",
    "AI写作", "AI绘画", "AI编程", "AI视频", "AI音乐", "AI翻译",
    "AI办公", "AI设计", "AI搜索", "AI聊天", "AI绘画",
    "ChatGPT", "Claude", "DeepSeek", "大模型",
    "文心一言", "通义千问", "豆包", "Kimi",
    "AI Agent", "AI智能体", "AI助手",
    "免费AI", "AI替代", "AI教程",
    "Claude Code", "Cursor", "Copilot",
]


def get_baidu_suggestions(keyword):
    """百度下拉联想词"""
    try:
        url = "https://suggestion.baidu.com/su"
        params = {"wd": keyword, "action": "opensearch", "cb": ""}
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, params=params, headers=headers, timeout=10)
        # 返回格式: ["keyword", ["sug1", "sug2", ...]]
        match = re.search(r'\[(.*?)\]', resp.text)
        if match:
            items = re.findall(r'"([^"]+)"', match.group(1))
            return items
    except Exception as e:
        print(f"  ⚠️ 百度下拉失败 [{keyword}]: {e}")
    return []


def get_weibo_hot():
    """微博热搜 AI 相关"""
    items = []
    try:
        url = "https://weibo.com/ajax/side/hotSearch"
        resp = requests.get(url, timeout=10)
        data = resp.json().get("data", {}).get("realtime", [])
        ai_kw = ["AI", "人工智能", "GPT", "大模型", "智能", "算法",
                  "ChatGPT", "Claude", "DeepSeek", "机器人", "深度学习"]
        for item in data:
            word = item.get("word", "")
            if any(kw in word for kw in ai_kw):
                items.append(word)
    except Exception as e:
        print(f"  ⚠️ 微博热搜失败: {e}")
    return items


def get_zhihu_hot():
    """知乎热榜 AI 相关"""
    items = []
    try:
        url = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=50"
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=10)
        data = resp.json().get("data", [])
        ai_kw = ["AI", "人工智能", "GPT", "大模型", "智能", "算法",
                  "ChatGPT", "Claude", "DeepSeek", "机器学习"]
        for item in data:
            title = item.get("target", {}).get("title", "")
            if any(kw in title for kw in ai_kw):
                items.append(title)
    except Exception as e:
        print(f"  ⚠️ 知乎热榜失败: {e}")
    return items


def collect_keywords():
    all_keywords = {}
    now = datetime.now().isoformat()

    # 1. 百度下拉词
    print("  🔍 百度下拉词...")
    for seed in SEED_KEYWORDS:
        suggestions = get_baidu_suggestions(seed)
        for sug in suggestions:
            if sug in all_keywords:
                all_keywords[sug]["count"] = all_keywords[sug].get("count", 0) + 1
            else:
                all_keywords[sug] = {
                    "source": "baidu_suggestion",
                    "seed": seed,
                    "first_seen": now,
                    "last_seen": now,
                    "count": 1,
                }
        time.sleep(0.3)

    # 2. 微博热搜
    print("  📱 微博热搜...")
    weibo = get_weibo_hot()
    for item in weibo:
        all_keywords[item] = {
            "source": "weibo_hot",
            "first_seen": now,
            "last_seen": now,
            "hot": True,
        }

    # 3. 知乎热榜
    print("  📖 知乎热榜...")
    zhihu = get_zhihu_hot()
    for item in zhihu:
        all_keywords[item] = {
            "source": "zhihu_hot",
            "first_seen": now,
            "last_seen": now,
            "hot": True,
        }

    # 合并已有关键词
    kw_path = os.path.join(DATA_DIR, "keywords.json")
    existing = {}
    if os.path.exists(kw_path):
        with open(kw_path) as f:
            old = json.load(f)
            existing = old.get("keywords", {})

    # 合并
    for kw, info in all_keywords.items():
        if kw in existing:
            existing[kw]["last_seen"] = now
            existing[kw]["count"] = existing[kw].get("count", 0) + info.get("count", 0)
            if info.get("hot"):
                existing[kw]["hot"] = True
        else:
            existing[kw] = info

    # 输出
    hot_kws = [k for k, v in existing.items() if v.get("hot")]
    top_kws = sorted(
        existing.items(),
        key=lambda x: x[1].get("count", 0),
        reverse=True
    )[:100]

    # 如果微博/知乎没有抓到可用热点，就回退到百度下拉中的高频真实搜索词
    display_hot_kws = hot_kws[:10]
    if not display_hot_kws:
        display_hot_kws = [item[0] for item in top_kws[:10]]

    output = {
        "updated_at": now,
        "total_keywords": len(existing),
        "hot_keywords": display_hot_kws,
        "top_suggestions": top_kws,
        "keywords": existing,
    }

    with open(kw_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    # 同时输出 SEO 数据供 Hugo 使用
    seo_data = {
        "updated_at": now,
        "homepage_keywords": [item[0] for item in top_kws[:20]],
        "hot_keywords": display_hot_kws,
    }
    seo_path = os.path.join(DATA_DIR, "seo.json")
    with open(seo_path, "w", encoding="utf-8") as f:
        json.dump(seo_data, f, ensure_ascii=False, indent=2)

    return f"{len(all_keywords)} 个新关键词 (总计 {len(existing)}, 热点展示 {len(display_hot_kws)})"


if __name__ == "__main__":
    print(collect_keywords())
