#!/usr/bin/env python3
"""
AI热榜 - 主聚合器 v3.1
每6小时运行一次，采集+AI增强
"""

import os
import sys
import json
import shutil
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))

from news_rss import collect_rss_news
from news_api import collect_api_news
from news_interleave import interleave_news
from github_discover import discover_github_projects
from github_trending import track_github_trending
from huggingface_discover import discover_hf_models
from keyword_collector import collect_keywords
from agent_discover import discover_agents
# from trending_scorer import compute_trending  # 已由Hermes定时任务接管
from daily_spotlight import select_daily_spotlight
from link_checker import quick_check
from ai_enhance import summarize_news, generate_daily_briefing, score_tools
from generate_sitemap import generate_sitemap
from openrouter_providers import update_providers

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
SITE_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "site", "data")


def sync_to_site():
    """同步数据到 Hugo site/data 目录"""
    if not os.path.exists(SITE_DATA_DIR):
        os.makedirs(SITE_DATA_DIR)
    
    count = 0
    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".json"):
            src = os.path.join(DATA_DIR, filename)
            dst = os.path.join(SITE_DATA_DIR, filename)
            shutil.copy2(src, dst)
            count += 1
    
    return f"同步 {count} 个文件到 site/data/"


def main():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"🚀 AI热榜数据采集 v3.0 - {now}")
    print("=" * 50)

    # Phase 1: 数据采集
    print("\n📡 Phase 1: 数据采集")
    steps_collect = [
        ("📰 RSS新闻", collect_rss_news),
        ("📰 API新闻", collect_api_news),
        ("🔀 新闻穿插", interleave_news),
        ("🔍 GitHub项目", discover_github_projects),
        ("📈 GitHub热度", track_github_trending),
        ("🤗 HF模型", discover_hf_models),
        ("🔑 关键词", collect_keywords),
        ("🤖 Agent发现", discover_agents),
    ]

    # Phase 2: 数据处理
    print("\n⚙️ Phase 2: 数据处理")
    steps_process = [
        ("🔥 保留热点", lambda: "由Hermes定时任务生成"),
        ("🏢 提供商更新", update_providers),
        ("⭐ 每日精选", select_daily_spotlight),
        ("🔗 链接检查", quick_check),
    ]

    # Phase 3: AI 增强
    print("\n🤖 Phase 3: AI 增强")
    steps_ai = [
        ("📝 新闻摘要", summarize_news),
        ("📰 每日快报", generate_daily_briefing),
        ("⭐ 工具评分", score_tools),
    ]

    # Phase 4: 同步部署
    print("\n🚀 Phase 4: 同步部署")
    steps_deploy = [
        ("📦 同步数据", sync_to_site),
        ("🗺️ 生成Sitemap", generate_sitemap),
    ]

    all_steps = [
        ("📡 数据采集", steps_collect),
        ("⚙️ 数据处理", steps_process),
        ("🤖 AI 增强", steps_ai),
        ("🚀 同步部署", steps_deploy),
    ]

    results = {}
    for phase_name, phase_steps in all_steps:
        for name, func in phase_steps:
            try:
                print(f"  {name}...")
                result = func()
                results[name] = f"✅ {result}"
                print(f"    → {result}")
            except Exception as e:
                results[name] = f"❌ {e}"
                print(f"    → ❌ {e}")

    # 汇总
    print("\n" + "=" * 50)
    success = sum(1 for v in results.values() if v.startswith("✅"))
    fail = sum(1 for v in results.values() if v.startswith("❌"))
    print(f"📊 结果: {success} 成功 / {fail} 失败 / {len(results)} 总计")

    # 写入元数据
    meta = {
        "last_update": now,
        "version": "3.0",
        "results": results,
    }
    with open(os.path.join(DATA_DIR, "meta.json"), "w") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 采集流程结束 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()
