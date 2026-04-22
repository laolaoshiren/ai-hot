#!/usr/bin/env python3
"""RSS 新闻采集器 v3 - AI 专用过滤，中文优先"""

import os
import json
import re
import hashlib
from datetime import datetime, timedelta

try:
    import feedparser
except ImportError:
    os.system("pip install feedparser -q")
    import feedparser

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

# AI 专用 RSS 源
RSS_SOURCES = [
    # 中文 AI 专用源 (Priority 1)
    {"name": "机器之心", "url": "https://www.jiqizhixin.com/feed", "lang": "zh", "priority": 1, "ai_only": True},
    {"name": "量子位", "url": "https://www.qbitai.com/feed", "lang": "zh", "priority": 1, "ai_only": True},
    {"name": "新智元", "url": "https://www.xinzhiyuan.com/feed", "lang": "zh", "priority": 1, "ai_only": True},
    
    # 英文 AI 专用源 (Priority 1)
    {"name": "TechCrunch AI", "url": "https://techcrunch.com/category/artificial-intelligence/feed/", "lang": "en", "priority": 1, "ai_only": True},
    {"name": "The Verge AI", "url": "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml", "lang": "en", "priority": 1, "ai_only": True},
    
    # 综合科技源 (Priority 2, 需 AI 关键词过滤)
    {"name": "MIT Tech Review", "url": "https://www.technologyreview.com/feed/", "lang": "en", "priority": 2, "ai_only": False},
    {"name": "Ars Technica AI", "url": "https://feeds.arstechnica.com/arstechnica/technology-lab", "lang": "en", "priority": 2, "ai_only": False},
    {"name": "VentureBeat AI", "url": "https://venturebeat.com/category/ai/feed/", "lang": "en", "priority": 2, "ai_only": True},
    {"name": "Hacker News AI", "url": "https://hnrss.org/newest?q=AI+OR+LLM+OR+GPT+OR+%22artificial+intelligence%22+OR+%22machine+learning%22&points=100", "lang": "en", "priority": 2, "ai_only": True},
    
    # 中文综合源 (Priority 3, 需 AI 关键词过滤)
    {"name": "36氪", "url": "https://36kr.com/feed", "lang": "zh", "priority": 4, "ai_only": False},
    {"name": "InfoQ AI", "url": "https://www.infoq.cn/feed", "lang": "zh", "priority": 3, "ai_only": True},
]

# AI 关键词白名单（用于过滤非 AI 专用源）
# 非AI关键词黑名单（用于过滤明显无关内容）
NON_AI_KEYWORDS = [
    "护发", "美妆", "护肤", "彩妆", "美容", "美甲", "美发",
    "汽车大灯", "车灯", "轮胎", "发动机", "变速箱",
    "美食", "菜谱", "烹饪", "餐厅", "外卖",
    "旅游", "酒店", "机票", "签证", "景点",
    "游戏攻略", "游戏评测", "手游", "网游", "电竞",
    "健康养生", "药品", "保健品", "中医",
    "房产", "装修", "家具", "家电",
    "股票", "基金", "理财", "保险",
    "体育", "足球", "篮球", "网球", "奥运",
    "娱乐", "明星", "八卦", "综艺", "电影",
    "时尚", "服装", "穿搭", "潮流",
    "感染", "肠胃", "胃肠", "蛋白质", "肿瘤", "癌症", "细胞治疗", "疫苗",
    "约会", "Tinder", "Airbnb", "诗歌相机", "Poetry Camera", "鞋公司", "Allbirds", "OkCupid",
    # 财经新闻
    "A股", "B股", "港股", "美股", "股市", "涨跌", "涨幅", "跌幅",
    "沪指", "深成指", "创业板指", "三大指数", "集体收涨", "集体收跌",
    "中国移动", "中国联通", "中国电信", "工商银行", "建设银行",
    "兖矿能源", "岳阳兴长", "英维克", "寒武纪", "翠微股份",
    # 汽车新闻（非AI相关）
    "理想汽车", "蔚来", "小鹏", "比亚迪", "特斯拉", "华为汽车",
    "问界", "极氪", "岚图", "零跑", "哪吒",
]

AI_KEYWORDS_ZH = [
    "AI", "人工智能", "大模型", "LLM", "GPT", "ChatGPT", "Claude", "Gemini", "Llama",
    "深度学习", "机器学习", "神经网络", "自然语言", "NLP", "计算机视觉", "CV",
    "生成式", "AIGC", "AGI", "智能体", "Agent", "Transformer", "扩散模型",
    "Stable Diffusion", "Midjourney", "DALL-E", "Sora", "可灵", "通义", "文心",
    "豆包", "Kimi", "DeepSeek", "智谱", "百川", "MiniMax", "零一万物",
    "机器人", "具身智能", "自动驾驶", "语音识别", "TTS", "ASR",
    "英伟达", "NVIDIA", "GPU", "算力", "芯片", "H100", "A100",
    "OpenAI", "Anthropic", "Google AI", "Meta AI", "微软 AI", "百度 AI", "阿里 AI",
    "腾讯 AI", "字节 AI", "华为 AI", "科大讯飞", "商汤", "旷视",
]

AI_KEYWORDS_EN = [
    "AI", "artificial intelligence", "machine learning", "deep learning", "LLM",
    "GPT", "ChatGPT", "Claude", "Gemini", "Llama", "transformer", "diffusion",
    "generative", "AIGC", "AGI", "agent", "neural network", "NLP",
    "OpenAI", "Anthropic", "Google AI", "Meta AI", "Microsoft AI",
    "NVIDIA", "GPU", "inference", "training", "fine-tuning", "RLHF",
    "Stable Diffusion", "Midjourney", "DALL-E", "Sora", "Whisper",
]

def is_ai_related(title, summary, source_config):
    """检查新闻是否与 AI 相关"""
    text = (title + " " + summary).upper()

    # 1. 黑名单优先，任何来源都先过滤明显无关内容
    for keyword in NON_AI_KEYWORDS:
        if keyword.upper() in text:
            return False

    # 2. AI 专用源仍需最基本AI关键词确认，避免漏进奇怪周边新闻
    if source_config.get("ai_only", False):
        return any(kw.upper() in text for kw in AI_KEYWORDS_ZH + AI_KEYWORDS_EN)

    # 3. 非 AI 专用源需要关键词匹配
    for kw in AI_KEYWORDS_ZH:
        if kw.upper() in text:
            return True

    for kw in AI_KEYWORDS_EN:
        if kw.upper() in text:
            return True

    return False


def strip_html(text):
    """去除 HTML 标签，保留纯文本"""
    if not text:
        return ""
    # 去除 HTML 标签
    text = re.sub(r'<[^>]+>', '', text)
    # 去除多余空白
    text = re.sub(r'\s+', ' ', text).strip()
    # 去除 HTML 实体
    text = text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    text = text.replace('&quot;', '"').replace('&#39;', "'").replace('&nbsp;', ' ')
    return text[:300]  # 截断过长


def collect_rss_news():
    all_news = []
    cutoff = datetime.now() - timedelta(days=3)  # 只保留3天内的
    filtered_count = 0

    for source in RSS_SOURCES:
        try:
            feed = feedparser.parse(source["url"])
            count = 0
            for entry in feed.entries[:20]:  # 增加到20条，因为要过滤
                published = None
                if hasattr(entry, "published_parsed") and entry.published_parsed:
                    published = datetime(*entry.published_parsed[:6])

                if published and published < cutoff:
                    continue

                title = strip_html(entry.get("title", ""))
                if not title:
                    continue

                # 清理 summary
                summary = strip_html(entry.get("summary", "") or entry.get("description", ""))

                # AI 相关性过滤
                if not is_ai_related(title, summary, source):
                    filtered_count += 1
                    continue

                news_id = hashlib.md5(entry.link.encode()).hexdigest()[:12]
                all_news.append({
                    "id": news_id,
                    "title": title,
                    "url": entry.link,
                    "source": source["name"],
                    "lang": source["lang"],
                    "priority": source["priority"],
                    "published": published.isoformat() if published else None,
                    "summary": summary,
                    "collected_at": datetime.now().isoformat(),
                })
                count += 1
            print(f"  ✓ {source['name']}: {count} 条 AI 新闻")
        except Exception as e:
            print(f"  ⚠️ {source['name']} 失败: {e}")

    if filtered_count > 0:
        print(f"  🔍 过滤掉 {filtered_count} 条非 AI 相关新闻")

    # 合并已有数据
    existing = []
    news_path = os.path.join(DATA_DIR, "news.json")
    if os.path.exists(news_path):
        with open(news_path) as f:
            existing = json.load(f)

    # 去重
    existing_ids = {n["id"] for n in existing}
    new_items = [n for n in all_news if n["id"] not in existing_ids]

    # 合并后重新按最新规则清洗一次，避免旧脏数据残留
    combined = []
    seen_ids = set()
    source_map = {s["name"]: s for s in RSS_SOURCES}
    recleaned_count = 0

    for item in existing + new_items:
        if item.get("id") in seen_ids:
            continue
        title = strip_html(item.get("title", ""))
        summary = strip_html(item.get("summary", ""))
        source_conf = source_map.get(item.get("source"), {"ai_only": False})
        if not is_ai_related(title, summary, source_conf):
            recleaned_count += 1
            continue
        item["title"] = title
        item["summary"] = summary
        combined.append(item)
        seen_ids.add(item.get("id"))

    # 按发布时间排序，中文优先
    combined.sort(key=lambda x: (
        0 if x.get("lang") == "zh" else 1,
        x.get("published") or ""
    ), reverse=False)
    combined.sort(key=lambda x: x.get("published") or "", reverse=True)

    # 保留最近3天的
    combined = combined[:300]

    if recleaned_count > 0:
        print(f"  🧹 依据新规则额外清理 {recleaned_count} 条旧脏新闻")

    with open(news_path, "w", encoding="utf-8") as f:
        json.dump(combined, f, ensure_ascii=False, indent=2)

    return f"{len(new_items)} 条新新闻 (总计 {len(combined)})"


if __name__ == "__main__":
    print(collect_rss_news())
