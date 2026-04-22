#!/usr/bin/env python3
"""根据 data/news.json 生成站内可收录的新闻文章页。"""

from pathlib import Path
import json
import re

ROOT = Path('/root/ai-hot')
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
    return f'{title_zh}。这篇内容来自 {source}，AI热榜已整理成站内中文快读版，方便先快速抓重点，再按需查看原始来源。'


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


def build_brief(item, title_zh):
    pieces = []
    ai_summary = clean_summary(item.get('ai_summary') or '')
    summary_zh = clean_summary(item.get('summary_zh') or '')
    summary = clean_summary(item.get('summary') or '')
    lang = (item.get('lang') or '').lower()
    if lang == 'en' and looks_bad_en_summary(ai_summary):
        ai_summary = ''

    if ai_summary:
        pieces.append(f'一句话看懂：{ai_summary}')
    if summary_zh and summary_zh != ai_summary:
        pieces.append(f'中文摘要：{summary_zh}')
    elif summary and summary != ai_summary and lang != 'en':
        pieces.append(f'内容摘要：{summary}')

    if lang == 'en' and not pieces:
        pieces.append('中文快读：这是一篇英文来源的 AI 新闻，本站当前先提供中文导读框架与重点提炼，方便快速理解。')
    if not pieces:
        pieces.append(f'{title_zh} 是近期值得关注的一条 AI 动态，建议先看下方重点，再决定是否继续读原文。')
    return '\n\n'.join(pieces)


def build_takeaways(item):
    title_zh = item.get('title_zh') or item.get('title', '')
    source = item.get('source', '原始来源')
    ai_summary = clean_summary(item.get('ai_summary') or '')
    summary_zh = clean_summary(item.get('summary_zh') or '')
    summary = clean_summary(item.get('summary') or '')
    lang = (item.get('lang') or '').lower()
    if lang == 'en' and looks_bad_en_summary(ai_summary):
        ai_summary = ''

    takeaway_1 = ai_summary or summary_zh
    if not takeaway_1 and lang != 'en':
        takeaway_1 = summary
    if not takeaway_1:
        takeaway_1 = f'{title_zh} 是这条新闻的核心信息。'

    takeaway_2 = f'这条内容来自 {source}，适合拿来快速判断它是否值得继续深挖。'
    takeaway_3 = '如果你只想节省时间，可以先看本站整理的中文导读；如果你要核对细节，再去看原文。'
    return [takeaway_1, takeaway_2, takeaway_3]


def build_page(item):
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
    for item in news:
        news_id = item.get('id') or slugify(item.get('title_zh') or item.get('title') or 'news')
        slug = item.get('slug') or news_id
        path = CONTENT_DIR / f'{slug}.md'
        path.write_text(build_page({**item, 'slug': slug}), encoding='utf-8')
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
