#!/usr/bin/env python3
"""
热度评分 v5 - 智能混合评分
确保：工具、项目、新闻混合显示，内容饱满，分类清晰
"""

import os
import json
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

# 分类映射
CATEGORY_MAP = {
    "tool": "🛠️ 工具",
    "project": "💻 项目",
    "model": "🧠 模型",
    "news": "📰 新闻",
}

# 来源权重
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
    'i hope they include it', 'deepseek v4 人'
)

BREAKING_MODEL_KEYWORDS = {
    'gpt-5.5': 18,
    'deepseek v4': 18,
    'deepseek-v4': 18,
    'deepseek: deepseek v4': 18,
}

def compute_trending():
    hot_items = []
    
    # 1. AI工具（优先级最高，权重最高）
    tools_path = os.path.join(DATA_DIR, "tools.json")
    if os.path.exists(tools_path):
        with open(tools_path) as f:
            tools = json.load(f)
        
        # 热门工具（trending=true）
        trending_tools = [t for t in tools if t.get("trending")]
        for t in trending_tools[:8]:
            hot_items.append({
                "id": t.get("id", ""),
                "name": t["name"],
                "url": t.get("url", ""),
                "type": "tool",
                "source": "热门工具",
                "score": 50,  # 基础高分
                "detail": t.get("pricing", ""),
                "description": t.get("description", ""),
                "category": t.get("category", ""),
            })
        
        # 精选工具（featured=true）
        featured_tools = [t for t in tools if t.get("featured") and not t.get("trending")]
        for t in featured_tools[:5]:
            hot_items.append({
                "id": t.get("id", ""),
                "name": t["name"],
                "url": t.get("url", ""),
                "type": "tool",
                "source": "精选",
                "score": 35,
                "detail": t.get("pricing", ""),
                "description": t.get("description", ""),
                "category": t.get("category", ""),
            })
    
    # 2. GitHub 热度飙升项目
    trending_path = os.path.join(DATA_DIR, "trending.json")
    if os.path.exists(trending_path):
        with open(trending_path) as f:
            trending = json.load(f)
        
        # 使用rankings字段，取stars最高的项目
        rankings = trending.get("rankings", [])
        if rankings:
            # 按stars排序，取前6个
            top_projects = sorted(rankings, key=lambda x: x.get("stars", 0), reverse=True)[:6]
            for item in top_projects:
                stars = item.get("stars", 0)
                if stars > 10000:  # 只要高star项目
                    hot_items.append({
                        "name": item.get("display_name") or item.get("name", ""),
                        "url": item.get("url", ""),
                        "type": "project",
                        "source": "GitHub",
                        "score": 40 + min(stars / 50000, 20),  # stars越高分数越高
                        "detail": f"⭐ {stars}",
                        "description": item.get("description", ""),
                        "category": "编程",
                    })
    
    # 3. 新闻热度（精选最新的）
    news_path = os.path.join(DATA_DIR, "news.json")
    if os.path.exists(news_path):
        with open(news_path) as f:
            news = json.load(f)
        
        # 按来源分组，每来源取2条最新
        source_counts = {}
        for n in news:
            src = n.get("source", "other")
            if src in NOISY_NEWS_SOURCES or src not in TRUSTED_NEWS_SOURCES:
                continue
            source_counts[src] = source_counts.get(src, 0) + 1
            if source_counts[src] > 2:
                continue

            raw_title = n.get("title_zh") or n.get("title") or ""
            ai_summary = n.get("ai_summary", "") or ""
            summary_zh = n.get("summary_zh", "") or ""
            summary = n.get("summary", "") or ""
            desc = ai_summary or summary_zh or summary
            low_blob = f"{raw_title} {desc}".lower()
            if any(p in low_blob for p in BAD_DESC_PATTERNS):
                continue

            weight = SOURCE_WEIGHTS.get(src, 3)
            title_low = (n.get("title", "") + ' ' + n.get("title_zh", "")).lower()

            if desc and len(desc) > 30:
                weight += 5

            for kw, bonus in BREAKING_MODEL_KEYWORDS.items():
                if kw in title_low:
                    weight += bonus

            hot_items.append({
                "title": raw_title,
                "name": raw_title,
                "title_zh": n.get("title_zh") or n.get("title") or raw_title,
                "url": n.get("url", ""),
                "type": "news",
                "source": src,
                "score": weight,
                "detail": n.get("published", "")[:10],
                "time": n.get("published", "")[:10],
                "description": desc[:120],
                "subtitle": desc[:120],
                "ai_summary": desc[:120],
                "category": "资讯",
                "news_id": n.get("id"),
                "internal_url": f"https://aihot.bt199.com/news/{n.get('id')}/" if n.get("id") else "",
            })
    
    # 4. HuggingFace 热门模型
    models_path = os.path.join(DATA_DIR, "models.json")
    if os.path.exists(models_path):
        with open(models_path) as f:
            models = json.load(f)
        
        # 取likes最高的5个
        top_models = sorted(models, key=lambda x: x.get("likes", 0), reverse=True)[:5]
        for m in top_models:
            hot_items.append({
                "name": m.get("display_name") or m.get("name", ""),
                "url": m.get("url", ""),
                "type": "model",
                "source": "HuggingFace",
                "score": 30 + min(m.get("likes", 0) / 1000, 15),
                "detail": f"❤️ {m.get('likes', 0)}",
                "description": m.get("pipeline_tag", ""),
                "category": "模型",
            })
    
    # 去重 + 排序
    seen = {}
    for item in hot_items:
        key = item["name"][:30]
        if key not in seen or item["score"] > seen[key]["score"]:
            seen[key] = item
    ranked = sorted(seen.values(), key=lambda x: x["score"], reverse=True)

    # 重大模型发布优先置顶，避免被工具类常青内容压住
    breaking = []
    normal = []
    for item in ranked:
        low = (item.get('name', '') + ' ' + item.get('description', '')).lower()
        if any(kw in low for kw in BREAKING_MODEL_KEYWORDS):
            breaking.append(item)
        else:
            normal.append(item)
    ranked = breaking + normal
    
    # 首页今日热点优先展示新闻大事件，工具/项目后置
    final_list = []
    type_counts = {"tool": 0, "project": 0, "news": 0, "model": 0}
    max_per_type = {"tool": 4, "project": 3, "news": 10, "model": 3}

    news_first = [x for x in ranked if x.get('type') == 'news']
    others = [x for x in ranked if x.get('type') != 'news']

    for item in news_first:
        if len(final_list) >= 8:
            break
        final_list.append(item)
        type_counts['news'] += 1

    for item in others + news_first[8:]:
        item_type = item.get("type", "other")
        if type_counts.get(item_type, 0) < max_per_type.get(item_type, 10):
            final_list.append(item)
            type_counts[item_type] = type_counts.get(item_type, 0) + 1

        if len(final_list) >= 20:  # 显示20条
            break
    
    # 添加分类标签
    for item in final_list:
        item["type_label"] = CATEGORY_MAP.get(item.get("type", ""), "其他")
    
    # 输出
    output = {
        "updated_at": datetime.now().isoformat(),
        "total": len(ranked),
        "hot_list": ranked[:50],
        "top_20": final_list[:20],  # 改为top_20
        "type_stats": type_counts,
    }
    
    with open(os.path.join(DATA_DIR, "hot.json"), "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    return f"✅ 生成 {len(final_list)} 条混合热点 (工具:{type_counts['tool']}, 项目:{type_counts['project']}, 新闻:{type_counts['news']}, 模型:{type_counts['model']})"


if __name__ == "__main__":
    print(compute_trending())