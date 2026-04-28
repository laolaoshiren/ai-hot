#!/usr/bin/env python3
"""
热度评分 v5 - 首页今日热点只保留高质量新闻，不混入工具/项目/模型。
"""

import os
import json
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

CATEGORY_MAP = {
    "tool": "🛠️ 工具",
    "project": "💻 项目",
    "model": "🧠 模型",
    "news": "📰 新闻",
}

SOURCE_WEIGHTS = {
    "机器之心": 10,
    "36氪": 8,
    "TechCrunch AI": 10,
    "The Verge AI": 8,
    "量子位": 8,
    "InfoQ AI": 7,
    "MIT Tech Review": 8,
    "Ars Technica AI": 6,
    "VentureBeat AI": 7,
    "IT之家": 5,
}

TRUSTED_NEWS_SOURCES = set(SOURCE_WEIGHTS.keys())
NOISY_NEWS_SOURCES = {"Hacker News AI", "r/LocalLLaMA", "r/MachineLearning", "r/artificial", "V2EX"}
BAD_DESC_PATTERNS = (
    '点击查看原文', '文章网址：', '评论网址：', 'reddit.com/', 'v2ex.com/', '![图片', '```',
    'i hope they include it', 'deepseek v4 人', "this is today's edition of the download", 'introducing: the nature issue'
)

BREAKING_MODEL_KEYWORDS = {
    'gpt-5.5': 18,
    'deepseek v4': 18,
    'deepseek-v4': 18,
    'deepseek: deepseek v4': 18,
}


def zh_ratio(text):
    text = str(text or '').strip()
    if not text:
        return 0.0
    zh = sum('\u4e00' <= c <= '\u9fff' for c in text)
    letters = sum(c.isalpha() or ('\u4e00' <= c <= '\u9fff') for c in text)
    return zh / max(letters, 1)


def is_publishable_hot_news(item):
    title_zh = item.get('title_zh') or ''
    ai_summary = item.get('ai_summary') or item.get('summary_zh') or ''
    news_id = item.get('id') or ''
    if not news_id or not title_zh or not ai_summary:
        return False
    if zh_ratio(title_zh) < 0.35 or zh_ratio(ai_summary) < 0.45:
        return False
    blob = f"{title_zh} {ai_summary}".lower()
    if any(p in blob for p in BAD_DESC_PATTERNS):
        return False
    return True


def compute_trending():
    hot_items = []

    news_path = os.path.join(DATA_DIR, 'news.json')
    if os.path.exists(news_path):
        with open(news_path, encoding='utf-8') as f:
            news = json.load(f)

        source_counts = {}
        for n in news:
            src = n.get('source', 'other')
            if src in NOISY_NEWS_SOURCES or src not in TRUSTED_NEWS_SOURCES:
                continue
            source_counts[src] = source_counts.get(src, 0) + 1
            if source_counts[src] > 2:
                continue

            title_en = n.get('title') or ''
            if title_en.lower().startswith('the download:'):
                continue
            if not is_publishable_hot_news(n):
                continue
            raw_title = n.get('title_zh') or n.get('title') or ''
            ai_summary = n.get('ai_summary', '') or ''
            summary_zh = n.get('summary_zh', '') or ''
            summary = n.get('summary', '') or ''
            desc = ai_summary or summary_zh or summary
            low_blob = f"{raw_title} {title_en} {desc}".lower()

            weight = SOURCE_WEIGHTS.get(src, 3)
            title_low = (n.get('title', '') + ' ' + n.get('title_zh', '')).lower()
            if desc and len(desc) > 30:
                weight += 5
            for kw, bonus in BREAKING_MODEL_KEYWORDS.items():
                if kw in title_low:
                    weight += bonus

            hot_items.append({
                'title': raw_title,
                'name': raw_title,
                'title_zh': n.get('title_zh') or n.get('title') or raw_title,
                'url': n.get('url', ''),
                'type': 'news',
                'source': src,
                'score': weight,
                'detail': n.get('published', '')[:10],
                'time': n.get('published', '')[:10],
                'description': desc[:120],
                'subtitle': desc[:120],
                'ai_summary': desc[:120],
                'category': '资讯',
                'news_id': n.get('id'),
                'internal_url': f"https://aihot.bt199.com/news/{n.get('id')}/" if n.get('id') else '',
            })

    seen = {}
    for item in hot_items:
        key = item['name'][:30]
        if key not in seen or item['score'] > seen[key]['score']:
            seen[key] = item
    ranked = sorted(seen.values(), key=lambda x: x['score'], reverse=True)

    breaking = []
    normal = []
    for item in ranked:
        low = (item.get('name', '') + ' ' + item.get('description', '')).lower()
        if any(kw in low for kw in BREAKING_MODEL_KEYWORDS):
            breaking.append(item)
        else:
            normal.append(item)
    ranked = breaking + normal

    final_list = [x for x in ranked if x.get('type') == 'news'][:10]
    type_counts = {"tool": 0, "project": 0, "news": len(final_list), "model": 0}

    for item in final_list:
        item['type_label'] = CATEGORY_MAP.get(item.get('type', ''), '其他')

    output = {
        'updated_at': datetime.now().isoformat(),
        'total': len(ranked),
        'hot_list': ranked[:50],
        'top_20': final_list[:20],
        'type_stats': type_counts,
    }

    with open(os.path.join(DATA_DIR, 'hot.json'), 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    return f"✅ 生成 {len(final_list)} 条新闻热点 (新闻:{type_counts['news']})"


if __name__ == '__main__':
    print(compute_trending())
