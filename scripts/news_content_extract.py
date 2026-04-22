#!/usr/bin/env python3
"""为 news.json 提取正文，给站内文章页提供真实内容基础。"""

import json
import os
import re
from pathlib import Path

import requests
import trafilatura
from readability import Document
from bs4 import BeautifulSoup

ROOT = Path('/root/ai-hot')
DATA_DIR = ROOT / 'data'
NEWS_PATH = DATA_DIR / 'news.json'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

TEXT_MIN_LEN = 280


def clean_text(text: str) -> str:
    text = '' if text is None else str(text)
    text = text.replace('\r', ' ')
    text = re.sub(r'\n\s*\n+', '\n\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    return text.strip()


def strip_text(text: str) -> str:
    text = clean_text(text)
    return re.sub(r'\s+', ' ', text).strip()


def readability_extract(html: str) -> str:
    try:
        doc = Document(html)
        summary_html = doc.summary()
        text = BeautifulSoup(summary_html, 'html.parser').get_text('\n', strip=True)
        return clean_text(text)
    except Exception:
        return ''


def trafilatura_extract(html: str) -> str:
    try:
        text = trafilatura.extract(
            html,
            include_comments=False,
            include_tables=False,
            favor_precision=True,
        ) or ''
        return clean_text(text)
    except Exception:
        return ''


def choose_best_text(a: str, b: str) -> str:
    a = clean_text(a)
    b = clean_text(b)
    if len(b) >= len(a):
        return b
    return a


def extract_article(url: str):
    resp = requests.get(url, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    html = resp.text
    read_text = readability_extract(html)
    traf_text = trafilatura_extract(html)
    best = choose_best_text(read_text, traf_text)
    return {
        'content_text': best,
        'content_source': 'trafilatura' if len(traf_text) >= len(read_text) else 'readability',
        'content_chars': len(best),
    }


def should_extract(item: dict) -> bool:
    url = item.get('url') or ''
    if not url.startswith('http'):
        return False
    existing = strip_text(item.get('content_text') or '')
    if len(existing) >= TEXT_MIN_LEN:
        return False
    return True


def extract_news_content(limit: int = 24):
    if not NEWS_PATH.exists():
        return 'news.json 不存在'

    news = json.loads(NEWS_PATH.read_text(encoding='utf-8'))
    changed = 0
    attempted = 0
    failed = 0

    for item in news:
        if attempted >= limit:
            break
        if not should_extract(item):
            continue
        attempted += 1
        try:
            result = extract_article(item['url'])
            if result['content_chars'] >= TEXT_MIN_LEN:
                item['content_text'] = result['content_text']
                item['content_source'] = result['content_source']
                item['content_chars'] = result['content_chars']
                changed += 1
        except Exception as e:
            item['extract_error'] = str(e)[:180]
            failed += 1

    NEWS_PATH.write_text(json.dumps(news, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return f'尝试 {attempted} 条，成功提取 {changed} 条正文，失败 {failed} 条'


if __name__ == '__main__':
    print(extract_news_content())
