#!/usr/bin/env python3
"""新闻文章增强：英文新闻中文化 + 正文清洗 + 摘录控制。"""

import json
import re
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path('/root/ai-hot')
NEWS_PATH = ROOT / 'data' / 'news.json'

AD_PATTERNS = [
    r'Meet your next investor.*',
    r'Your next round\.?',
    r'Your next hire\.?',
    r'Your next breakout opportunity\.?',
    r'Find it at TechCrunch Disrupt.*',
    r'Register now to save.*',
]


def clean_line(line: str) -> str:
    line = (line or '').strip()
    line = re.sub(r'\s+', ' ', line)
    return line


def clean_content_text(text: str) -> str:
    text = text or ''
    lines = [clean_line(x) for x in text.splitlines()]
    kept = []
    for line in lines:
        if not line:
            continue
        bad = False
        for pat in AD_PATTERNS:
            if re.search(pat, line, re.I):
                bad = True
                break
        if bad:
            continue
        if line.startswith('< img') or line.startswith('img '):
            continue
        kept.append(line)
    return '\n'.join(kept).strip()


def take_excerpt(text: str, max_paras: int = 12) -> str:
    paras = [clean_line(x) for x in text.splitlines() if clean_line(x)]
    return '\n'.join(paras[:max_paras]).strip()


def translate(text: str, source='en', target='zh-CN') -> str:
    text = (text or '').strip()
    if not text:
        return ''
    url = (
        'https://translate.googleapis.com/translate_a/single'
        f'?client=gtx&sl={source}&tl={target}&dt=t&q={urllib.parse.quote(text)}'
    )
    with urllib.request.urlopen(url, timeout=20) as resp:
        data = json.loads(resp.read().decode('utf-8'))
    return ''.join(part[0] for part in data[0] if part and part[0]).strip()


def shorten_zh(text: str, limit: int = 80) -> str:
    text = clean_line(text)
    return text[:limit].rstrip('，。；： ') + ('…' if len(text) > limit else '')


def enhance_news(limit: int = 40):
    news = json.loads(NEWS_PATH.read_text(encoding='utf-8'))
    done = 0

    for item in news:
        content = clean_content_text(item.get('content_text') or '')
        if content:
            item['content_text'] = content
            item['content_excerpt'] = take_excerpt(content, max_paras=10)

        if (item.get('lang') or '').lower() != 'en':
            continue
        if done >= limit:
            continue

        title = clean_line(item.get('title') or '')
        summary = clean_line(item.get('summary') or '')
        content_excerpt = item.get('content_excerpt') or ''

        current_ai = clean_line(item.get('ai_summary') or '')
        stale_ai = (not current_ai) or current_ai.startswith('AI领域最新动态：') or current_ai.endswith('。') and len(current_ai) < 40

        if (not item.get('title_zh')) and title:
            try:
                item['title_zh'] = translate(title)
            except Exception:
                pass

        zh_base = ''
        if summary:
            try:
                zh_base = translate(summary)
            except Exception:
                zh_base = ''
        elif content_excerpt:
            first_para = content_excerpt.splitlines()[0] if content_excerpt.splitlines() else ''
            try:
                zh_base = translate(first_para)
            except Exception:
                zh_base = ''

        if zh_base and (not item.get('summary_zh')):
            item['summary_zh'] = shorten_zh(zh_base, 120)
        if zh_base and stale_ai:
            item['ai_summary'] = shorten_zh(zh_base, 60)
        done += 1

    NEWS_PATH.write_text(json.dumps(news, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return f'增强 {done} 条英文新闻，清洗正文并生成摘录'


if __name__ == '__main__':
    print(enhance_news())
