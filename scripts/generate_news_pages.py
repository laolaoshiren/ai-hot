#!/usr/bin/env python3
"""根据 data/news.json 生成站内可收录的新闻文章页。"""

from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
NEWS_JSON = ROOT / 'data' / 'news.json'
CONTENT_DIR = ROOT / 'site' / 'content' / 'news'
GENERATED_MARKER = '<!-- AUTO-GENERATED: news page -->\n'


def esc(value: str) -> str:
    value = '' if value is None else str(value)
    return value.replace('\\', '\\\\').replace('"', '\\"')


def slugify(value: str) -> str:
    value = (value or '').strip().lower()
    value = re.sub(r'[^a-z0-9\u4e00-\u9fff]+', '-', value)
    value = re.sub(r'-+', '-', value).strip('-')
    return value or 'news'


def toml_array(items):
    if not items:
        return '[]'
    return '[' + ', '.join(f'"{esc(x)}"' for x in items) + ']'


def build_keywords(item):
    parts = [
        item.get('title_zh') or item.get('title', ''),
        item.get('source', ''),
        'AI新闻',
        'AI资讯',
        'AI热榜',
    ]
    parts.extend((item.get('tags') or [])[:6])
    seen = []
    for part in parts:
        part = (part or '').strip()
        if part and part not in seen:
            seen.append(part)
    return ', '.join(seen)


def single_line(text: str) -> str:
    text = '' if text is None else str(text)
    text = text.replace('\r', ' ').replace('\n', ' ')
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def clean_summary(text: str) -> str:
    text = single_line(text)
    if text in {'点击查看原文>', '点击查看原文', '阅读全文', 'Read more'}:
        return ''
    return text


def mostly_ascii(text: str) -> bool:
    text = text or ''
    if not text:
        return False
    ascii_chars = sum(1 for ch in text if ord(ch) < 128)
    return ascii_chars / max(len(text), 1) > 0.8


def looks_bad_en_summary(text: str) -> bool:
    text = clean_summary(text)
    if not text:
        return True
    low = text.lower()
    if text.startswith('AI领域最新动态：') or text.startswith('AI最新动态：'):
        return True
    if 'click to read' in low or 'click to view' in low:
        return True
    if mostly_ascii(text) and len(text) < 40:
        return True
    if mostly_ascii(text) and text.endswith('。'):
        return True
    return False


def zh_fast_read_fallback(title_zh, source):
    if source:
        return f'{title_zh}。这条新闻来自 {source}，站内页优先帮你快速抓住核心变化与影响。'
    return f'{title_zh}。这条新闻的站内页优先帮你快速抓住核心变化与影响。'


def build_intro(item, title_zh, source):
    ai_summary = clean_summary(item.get('ai_summary') or '')
    summary_zh = clean_summary(item.get('summary_zh') or '')
    summary = clean_summary(item.get('summary') or '')
    lang = (item.get('lang') or '').lower()
    if lang == 'en' and looks_bad_en_summary(ai_summary):
        ai_summary = ''
    if ai_summary:
        return ai_summary
    if summary_zh:
        return summary_zh
    if lang == 'en':
        return zh_fast_read_fallback(title_zh, source)
    if summary:
        return summary
    return zh_fast_read_fallback(title_zh, source)


def build_page(item, list_page=1):
    news_id = item.get('id') or slugify(item.get('title_zh') or item.get('title') or 'news')
    slug = item.get('slug') or news_id
    title = item.get('title') or slug
    title_zh = item.get('title_zh') or title
    source = item.get('source', '')
    published = item.get('published', '')
    url = item.get('url', '')
    ai_summary = clean_summary(item.get('ai_summary') or '')
    summary_zh = clean_summary(item.get('summary_zh') or '')
    summary = clean_summary(item.get('summary') or '')
    lang = item.get('lang', '')
    if str(lang).lower() == 'en' and looks_bad_en_summary(ai_summary):
        ai_summary = ''
    tags = item.get('tags') or []
    intro = single_line(build_intro(item, title_zh, source))
    seo_title = single_line(f'{title_zh}｜AI资讯解读 - AI热榜')
    seo_description = single_line(intro[:120] if intro else f'{title_zh}：AI热榜整理的中文快读版，帮你快速了解这条 AI 新闻的重点。')

    raw_body = item.get('rewrite_body') or item.get('article_body') or item.get('content_rewrite') or item.get('content_excerpt') or item.get('content_text') or ''
    raw_body = str(raw_body or '').replace('\r', '\n')
    raw_body = re.sub(r'\n{3,}', '\n\n', raw_body).strip()
    if not raw_body:
        raw_body = intro

    if '\n\n' not in raw_body:
        raw_body = raw_body.replace('。', '。\n\n').replace('！', '！\n\n').replace('？', '？\n\n').replace('. ', '.\n\n')
        raw_body = re.sub(r'\n{3,}', '\n\n', raw_body).strip()

    lines = [
        '+++',
        f'title = "{esc(title_zh)}"',
        f'description = "{esc(seo_description)}"',
        f'seo_title = "{esc(seo_title)}"',
        f'seo_description = "{esc(seo_description)}"',
        f'seo_keywords = "{esc(build_keywords(item))}"',
        f'slug = "{esc(slug)}"',
        'type = "news"',
        '',
        '[params]',
        f'id = "{esc(news_id)}"',
        f'name = "{esc(title_zh)}"',
        f'title_en = "{esc(title)}"',
        f'original_url = "{esc(url)}"',
        f'source = "{esc(source)}"',
        f'published = "{esc(published)}"',
        f'lang = "{esc(lang)}"',
        f'intro = "{esc(intro)}"',
        f'ai_summary = "{esc(ai_summary)}"',
        f'summary = "{esc(summary)}"',
        f'summary_zh = "{esc(summary_zh)}"',
        f'tags = {toml_array(tags)}',
        f'list_page = {int(list_page)}',
        '+++',
        '',
        GENERATED_MARKER.rstrip(),
        '',
        raw_body,
        '',
        '## 🔗 原始来源',
        '',
        '如果你要核对细节，可以再看原文：',
        f'[{source or "原文链接"}原文链接]({url})' if url else '原文链接暂不可用。',
        '',
    ]
    return '\n'.join(lines) + '\n'


def generate_news_pages():
    news = json.loads(NEWS_JSON.read_text(encoding='utf-8'))
    CONTENT_DIR.mkdir(parents=True, exist_ok=True)

    keep = {'_index.md'}
    generated = 0
    for index, item in enumerate(news):
        news_id = item.get('id') or slugify(item.get('title_zh') or item.get('title') or 'news')
        slug = item.get('slug') or news_id
        path = CONTENT_DIR / f'{slug}.md'
        path.write_text(build_page({**item, 'slug': slug}, list_page=(index // 10) + 1), encoding='utf-8')
        keep.add(path.name)
        generated += 1

    for path in CONTENT_DIR.glob('*.md'):
        if path.name not in keep:
            text = path.read_text(encoding='utf-8', errors='ignore')
            if GENERATED_MARKER in text:
                path.unlink()

    return f'生成 {generated} 个站内新闻页'


if __name__ == '__main__':
    print(generate_news_pages())
