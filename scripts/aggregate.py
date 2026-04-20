#!/usr/bin/env python3
"""
AI热榜 - 主聚合器
每6小时运行一次，采集全网AI数据
"""

import os
import sys
import json
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))

from news_rss import collect_rss_news
from news_api import collect_api_news
from github_discover import discover_github_projects
from github_trending import track_github_trending
from huggingface_discover import discover_hf_models
from keyword_collector import collect_keywords
from trending_scorer import compute_trending
from daily_spotlight import select_daily_spotlight
from link_checker import quick_check

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def main():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"🚀 AI热榜数据采集开始 - {now}")
    print("=" * 50)

    steps = [
        ("📰 RSS新闻采集", collect_rss_news),
        ("📰 API新闻采集", collect_api_news),
        ("🔍 GitHub项目发现", discover_github_projects),
        ("📈 GitHub热度追踪", track_github_trending),
        ("🤗 HuggingFace模型发现", discover_hf_models),
        ("🔑 关键词采集", collect_keywords),
        ("🔥 热点评分", compute_trending),
        ("⭐ 每日精选", select_daily_spotlight),
        ("🔗 快速链接检查", quick_check),
    ]

    results = {}
    for name, func in steps:
        try:
            print(f"\n{name}...")
            result = func()
            results[name] = "✅"
            print(f"  完成: {result}")
        except Exception as e:
            results[name] = f"❌ {e}"
            print(f"  失败: {e}")

    print("\n" + "=" * 50)
    print("📊 采集结果汇总:")
    for name, status in results.items():
        print(f"  {name}: {status}")

    # 写入更新时间戳
    meta = {
        "last_update": now,
        "results": results
    }
    with open(os.path.join(DATA_DIR, "meta.json"), "w") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 采集流程结束 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()
