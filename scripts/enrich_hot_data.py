#!/usr/bin/env python3
import json
import re
from pathlib import Path

ROOT = Path('/root/ai-hot')
DATA_DIR = ROOT / 'data'
HOT_PATH = DATA_DIR / 'hot.json'
NEWS_PATH = DATA_DIR / 'news.json'


def norm(text: str) -> str:
    text = str(text or '').lower().strip()
    text = re.sub(r'^[^\w\u4e00-\u9fff]+', '', text)
    text = text.replace('一夜断供', '').replace('完整界面', 'ui').replace('深度伪造检测', 'likeness detection')
    text = text.replace('原生互动故事创作平台', '').replace('政治应用', '选举').replace('负责人', '')
    text = re.sub(r'[\W_]+', '', text)
    return text


def token_overlap(a: str, b: str) -> int:
    a_tokens = [x for x in re.split(r'[^a-z0-9\u4e00-\u9fff]+', a.lower()) if len(x) >= 2]
    b_tokens = [x for x in re.split(r'[^a-z0-9\u4e00-\u9fff]+', b.lower()) if len(x) >= 2]
    return len(set(a_tokens) & set(b_tokens))


def enrich_hot_data():
    if not HOT_PATH.exists() or not NEWS_PATH.exists():
        return '缺少 hot.json 或 news.json'

    hot = json.loads(HOT_PATH.read_text(encoding='utf-8'))
    news = json.loads(NEWS_PATH.read_text(encoding='utf-8'))

    by_url = {str(n.get('url', '')).rstrip('/'): n for n in news if n.get('id')}
    items = hot.get('items') or hot.get('top_20') or hot.get('hot_list') or []
    matched = 0

    special_rules = [
        (lambda title: 'claude design' in title.lower(), 'd5c19f9f7a21'),
        (lambda title: 'youtube' in title.lower() and ('伪造' in title or 'likeness' in title.lower()), '2d537bc7c412'),
        (lambda title: '选举' in title or 'election' in title.lower() or '政治应用' in title, '314fefba7e73'),
        (lambda title: 'john ternus' in title.lower(), '7faac906f243'),
    ]
    news_by_id = {n.get('id'): n for n in news if n.get('id')}

    for item in items:
        if item.get('type') != 'news':
            continue
        candidate = None
        raw_title = str(item.get('title') or '')
        for matcher, forced_id in special_rules:
            if matcher(raw_title) and forced_id in news_by_id:
                candidate = news_by_id[forced_id]
                break
        url = str(item.get('url', '')).rstrip('/')
        if url and not candidate:
            candidate = by_url.get(url)
        if not candidate:
            item_title = norm(item.get('title'))
            raw_item_title = str(item.get('title') or '')
            best = None
            best_score = 0
            for n in news:
                raw_title = str(n.get('title') or '')
                raw_title_zh = str(n.get('title_zh') or '')
                t1 = norm(raw_title)
                t2 = norm(raw_title_zh)
                if item_title and ((t1 and (item_title in t1 or t1 in item_title)) or (t2 and (item_title in t2 or t2 in item_title))):
                    candidate = n
                    break
                score = max(token_overlap(raw_item_title, raw_title), token_overlap(raw_item_title, raw_title_zh))
                if score > best_score:
                    best = n
                    best_score = score
            if not candidate and best_score >= 3:
                candidate = best
        if candidate:
            item['news_id'] = candidate.get('id')
            item['internal_url'] = f"https://aihot.bt199.com/news/{candidate.get('id')}/"
            item['ai_summary'] = candidate.get('ai_summary') or candidate.get('summary_zh') or candidate.get('summary') or item.get('subtitle', '')
            item['title_zh'] = candidate.get('title_zh') or candidate.get('title') or item.get('title', '')
            matched += 1

    hot['items'] = items
    if 'top_20' in hot:
        hot['top_20'] = items[:20]
    HOT_PATH.write_text(json.dumps(hot, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return f'热点新闻站内化补全 {matched} 条'


if __name__ == '__main__':
    print(enrich_hot_data())
