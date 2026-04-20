#!/usr/bin/env python3
"""新闻穿插排序 - 按时间排序，同来源不连续"""

import os
import json
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def interleave_news():
    """将新闻按时间排序，确保同来源不连续出现"""
    news_path = os.path.join(DATA_DIR, "news.json")
    if not os.path.exists(news_path):
        return "无新闻数据"

    with open(news_path, encoding="utf-8") as f:
        news = json.load(f)

    # 按发布时间排序（最新的在前）
    news.sort(key=lambda x: x.get("published") or "", reverse=True)

    # 穿插：同来源的新闻不连续出现
    result = []
    remaining = list(news)

    while remaining:
        # 找到和上一条不同来源的新闻
        last_source = result[-1].get("source", "") if result else ""
        found = False

        for i, item in enumerate(remaining):
            if item.get("source", "") != last_source:
                result.append(remaining.pop(i))
                found = True
                break

        if not found:
            # 如果全部同来源，直接追加
            result.append(remaining.pop(0))

    with open(news_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    # 统计来源分布
    sources = {}
    for n in result[:20]:
        s = n.get("source", "?")
        sources[s] = sources.get(s, 0) + 1

    return f"穿插完成: {len(result)} 条, Top20 来源分布: {sources}"


if __name__ == "__main__":
    print(interleave_news())
