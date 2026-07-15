#!/usr/bin/env python3
"""根据 data/news.json 生成站内可收录的新闻文章页。"""

from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
NEWS_JSON = ROOT / 'data' / 'news.json'
CONTENT_DIR = ROOT / 'site' / 'content' / 'news'
GENERATED_MARKER = '<!-- AUTO-GENERATED: news page -->\n'
SOURCE_HEADING = '## 🔗 原始来源'

BAD_DOWNLOAD_TITLE_TRANSLATIONS = {
    '下载：介绍自然问题',
    '下载：介绍目前人工智能中最重要的 10 件事',
}


def clean_title_zh(title_zh: str, title_en: str) -> str:
    title_zh = single_line(title_zh)
    title_en = single_line(title_en)
    if title_en.lower().startswith('the download:') and title_zh in BAD_DOWNLOAD_TITLE_TRANSLATIONS:
        return title_en
    return title_zh or title_en


def esc(value: str) -> str:
    value = '' if value is None else str(value)
    # Filter control chars except CR LF TAB and DEL
    value = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', value)
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


def zh_ratio(text: str) -> float:
    text = str(text or '')
    letters = sum(ch.isalpha() for ch in text)
    zh = sum('\u4e00' <= ch <= '\u9fff' for ch in text)
    return zh / max(letters, 1)


def looks_chinese(text: str) -> bool:
    text = str(text or '').strip()
    zh = sum('\u4e00' <= ch <= '\u9fff' for ch in text)
    return zh >= 2 and zh_ratio(text) >= 0.15


def looks_chinese_body(text: str) -> bool:
    text = str(text or '').strip()
    zh = sum('\u4e00' <= ch <= '\u9fff' for ch in text)
    return zh >= 4 and zh_ratio(text) >= 0.35


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


def zh_fast_read_fallback(title_zh, source, require_chinese_title=False):
    title_is_usable = bool(single_line(title_zh)) and (
        not require_chinese_title or looks_chinese(title_zh)
    )
    if title_is_usable and source:
        return f'{title_zh}。来源：{source}。'
    if title_is_usable:
        return title_zh
    if source:
        return f'这是一条来自 {source} 的 AI 资讯，完整细节请查看下方原始来源。'
    return '这是一条 AI 资讯，完整细节请查看下方原始来源。'


def build_intro(item, title_zh, source):
    ai_summary = clean_summary(item.get('ai_summary') or '')
    summary_zh = clean_summary(item.get('summary_zh') or '')
    summary = clean_summary(item.get('summary') or '')
    lang = (item.get('lang') or '').lower()
    if lang == 'en':
        if ai_summary and looks_chinese(ai_summary) and not looks_bad_en_summary(ai_summary):
            return ai_summary
        if summary_zh and looks_chinese(summary_zh):
            return summary_zh
        return zh_fast_read_fallback(title_zh, source, require_chinese_title=True)
    if ai_summary:
        return ai_summary
    if summary_zh:
        return summary_zh
    if lang == 'en':
        return zh_fast_read_fallback(title_zh, source)
    if summary:
        return summary
    return zh_fast_read_fallback(title_zh, source)


def normalize_body(text: str) -> str:
    text = str(text or '').replace('\r', '\n')
    return re.sub(r'\n{3,}', '\n\n', text).strip()


def select_article_body(item, intro: str) -> str:
    """选择页面正文；英文来源只允许中文候选，禁止回退到英文原文。"""
    lang = str(item.get('lang') or '').lower()
    if lang == 'en':
        candidates = (
            item.get('content_zh'),
            item.get('article_body_zh'),
            item.get('content_excerpt_zh'),
            item.get('rewrite_body'),
            item.get('content_rewrite'),
            item.get('article_body'),
        )
        for candidate in candidates:
            body = normalize_body(candidate)
            if body and looks_chinese_body(body):
                return body
        return normalize_body(intro) or zh_fast_read_fallback('', item.get('source', ''))

    candidates = (
        item.get('rewrite_body'),
        item.get('article_body'),
        item.get('content_rewrite'),
        item.get('content_zh'),
        item.get('content_excerpt'),
        item.get('content_text'),
    )
    for candidate in candidates:
        body = normalize_body(candidate)
        if body:
            return body
    return normalize_body(intro)


def build_page(item, list_page=1):
    news_id = item.get('id') or slugify(item.get('title_zh') or item.get('title') or 'news')
    slug = item.get('slug') or news_id
    title = item.get('title') or slug
    title_zh = clean_title_zh(item.get('title_zh') or title, title)
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

    raw_body = select_article_body(item, intro)
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


def frontmatter_string(text: str, key: str) -> str:
    match = re.search(rf'(?m)^{re.escape(key)} = "(.*)"$', text)
    if not match:
        return ''
    return match.group(1).replace('\\"', '"').replace('\\\\', '\\')


def sanitize_legacy_english_page(path: Path) -> bool:
    """清理已脱离 news.json、但仍永久保留的旧英文正文页。"""
    text = path.read_text(encoding='utf-8')
    marker = GENERATED_MARKER.rstrip()
    if marker not in text or not re.search(r'(?m)^lang = "en"$', text):
        return False

    before, after = text.split(marker, 1)
    if SOURCE_HEADING not in after:
        return False
    body, source_section = after.split(SOURCE_HEADING, 1)
    body_without_images = re.sub(r'(?m)^!\[[^\]]*\]\([^)]*\)\s*$', '', body)
    if looks_chinese(body_without_images):
        return False

    intro = frontmatter_string(text, 'intro')
    if not looks_chinese(intro):
        title = frontmatter_string(text, 'title')
        source = frontmatter_string(text, 'source')
        intro = zh_fast_read_fallback(title, source, require_chinese_title=True)

    images = re.findall(r'(?m)^!\[[^\]]*\]\([^)]*\)\s*$', body)
    replacement_parts = [intro] + images
    replacement = '\n\n'.join(part for part in replacement_parts if part).strip()
    updated = f'{before}{marker}\n\n{replacement}\n\n{SOURCE_HEADING}{source_section}'
    path.write_text(updated, encoding='utf-8')
    return True


def generate_news_pages():
    news = json.loads(NEWS_JSON.read_text(encoding='utf-8'))
    CONTENT_DIR.mkdir(parents=True, exist_ok=True)

    generated = 0
    active_paths = set()
    for index, item in enumerate(news):
        news_id = item.get('id') or slugify(item.get('title_zh') or item.get('title') or 'news')
        slug = item.get('slug') or news_id
        path = CONTENT_DIR / f'{slug}.md'
        path.write_text(build_page({**item, 'slug': slug}, list_page=(index // 10) + 1), encoding='utf-8')
        active_paths.add(path.resolve())
        generated += 1

    # 永久保留所有新闻页面，不再删除
    sanitized = 0
    for path in CONTENT_DIR.glob('*.md'):
        if path.resolve() in active_paths:
            continue
        if sanitize_legacy_english_page(path):
            sanitized += 1

    return f'生成 {generated} 个站内新闻页，修复 {sanitized} 个历史英文页'


if __name__ == '__main__':
    print(generate_news_pages())
