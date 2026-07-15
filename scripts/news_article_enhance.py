#!/usr/bin/env python3
"""新闻文章增强：英文新闻中文化 + 正文清洗 + 摘录控制。"""

import hashlib
import json
import re
import time
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NEWS_PATH = ROOT / 'data' / 'news.json'
TRANSLATE_CHUNK_CHARS = 3800
TRANSLATION_RETRY_HOURS = 12
MAX_CONSECUTIVE_FAILURES = 5

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
    """调用现有的 Google 翻译端点。

    正文改用 POST 传参，避免较长文本被拼进 URL 后超过长度限制。
    """
    text = (text or '').strip()
    if not text:
        return ''
    payload = urllib.parse.urlencode({
        'client': 'gtx',
        'sl': source,
        'tl': target,
        'dt': 't',
        'q': text,
    }).encode('utf-8')
    request = urllib.request.Request(
        'https://translate.googleapis.com/translate_a/single',
        data=payload,
        headers={'User-Agent': 'Mozilla/5.0'},
    )
    with urllib.request.urlopen(request, timeout=20) as resp:
        data = json.loads(resp.read().decode('utf-8'))
    return ''.join(part[0] for part in data[0] if part and part[0]).strip()


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


def content_fingerprint(text: str) -> str:
    normalized = clean_content_text(text)
    return hashlib.sha256(normalized.encode('utf-8')).hexdigest()[:16]


def retry_is_deferred(item: dict, now=None) -> bool:
    raw = str(item.get('translation_retry_after') or '').strip()
    if not raw:
        return False
    try:
        retry_after = datetime.fromisoformat(raw.replace('Z', '+00:00'))
    except ValueError:
        return False
    if retry_after.tzinfo is None:
        retry_after = retry_after.replace(tzinfo=timezone.utc)
    now = now or datetime.now(timezone.utc)
    return retry_after > now


def _split_long_line(line: str, max_chars: int):
    parts = []
    remaining = line.strip()
    while len(remaining) > max_chars:
        window = remaining[:max_chars + 1]
        cut = -1
        for separator in ('. ', '? ', '! ', '; ', ', ', ' '):
            index = window.rfind(separator, max_chars // 2)
            if index > cut:
                cut = index + len(separator)
        if cut <= 0:
            cut = max_chars
        parts.append(remaining[:cut].strip())
        remaining = remaining[cut:].strip()
    if remaining:
        parts.append(remaining)
    return parts


def split_translation_chunks(text: str, max_chars: int = TRANSLATE_CHUNK_CHARS):
    """按段落聚合正文，确保每个翻译请求不超过服务端文本上限。"""
    if max_chars < 100:
        raise ValueError('max_chars 不能小于 100')

    lines = [clean_line(line) for line in clean_content_text(text).splitlines() if clean_line(line)]
    segments = []
    for line in lines:
        if len(line) > max_chars:
            segments.extend(_split_long_line(line, max_chars))
        else:
            segments.append(line)

    chunks = []
    current = []
    current_len = 0
    for segment in segments:
        added_len = len(segment) + (1 if current else 0)
        if current and current_len + added_len > max_chars:
            chunks.append('\n'.join(current))
            current = []
            current_len = 0
        current.append(segment)
        current_len += len(segment) + (1 if len(current) > 1 else 0)
    if current:
        chunks.append('\n'.join(current))
    return chunks


def translate_content(text: str, max_chars: int = TRANSLATE_CHUNK_CHARS, retries: int = 2) -> str:
    """分块翻译正文并保留块之间的段落边界。"""
    translated_chunks = []
    for chunk in split_translation_chunks(text, max_chars=max_chars):
        last_error = None
        translated = ''
        for attempt in range(max(retries, 1)):
            try:
                candidate = clean_content_text(translate(chunk))
                if candidate and looks_chinese_body(candidate):
                    translated = candidate
                    break
                last_error = RuntimeError('翻译结果为空或仍不是中文')
            except Exception as exc:
                last_error = exc
            if attempt + 1 < max(retries, 1):
                time.sleep(0.4 * (attempt + 1))
        if not translated:
            raise RuntimeError(f'正文翻译失败: {last_error}')
        translated_chunks.append(translated)

    result = '\n'.join(translated_chunks).strip()
    if result and not looks_chinese_body(result):
        raise RuntimeError('正文翻译结果未通过中文检测')
    return result


def shorten_zh(text: str, limit: int = 80) -> str:
    text = clean_line(text)
    return text[:limit].rstrip('，。；： ') + ('…' if len(text) > limit else '')


def enhance_news(limit: int = 40):
    news = json.loads(NEWS_PATH.read_text(encoding='utf-8'))
    now = datetime.now(timezone.utc)
    attempted = 0
    changed = 0
    body_done = 0
    failed = 0
    consecutive_failures = 0
    circuit_open = False

    for item in news:
        item_changed = False
        content = clean_content_text(item.get('content_text') or '')
        if content:
            old_content = item.get('content_text') or ''
            old_excerpt = item.get('content_excerpt') or ''
            item['content_text'] = content
            item['content_excerpt'] = take_excerpt(content, max_paras=10)
            item_changed = old_content != item['content_text'] or old_excerpt != item['content_excerpt']

        if (item.get('lang') or '').lower() != 'en':
            if item_changed:
                changed += 1
            continue

        title = clean_line(item.get('title') or '')
        summary = clean_line(item.get('summary') or '')
        content_excerpt = item.get('content_excerpt') or ''
        summary_source = summary or (content_excerpt.splitlines()[0] if content_excerpt.splitlines() else '')
        source_hash = content_fingerprint(content_excerpt) if content_excerpt else ''

        current_ai = clean_line(item.get('ai_summary') or '')
        stale_ai = (
            (not current_ai)
            or current_ai.startswith('AI领域最新动态：')
            or current_ai.startswith('AI最新动态：')
            or not looks_chinese(current_ai)
        )
        needs_title = bool(title) and not clean_line(item.get('title_zh') or '')
        needs_summary = bool(summary_source) and not looks_chinese(item.get('summary_zh') or '')
        needs_ai = bool(summary_source) and stale_ai
        needs_body = bool(content_excerpt) and (
            not looks_chinese_body(item.get('content_zh') or '')
            or item.get('content_zh_source_hash') != source_hash
        )

        if not (needs_title or needs_summary or needs_ai or needs_body):
            for key in ('translation_error', 'translation_retry_after', 'translation_failures'):
                if item.pop(key, None) is not None:
                    item_changed = True
            if item_changed:
                changed += 1
            continue
        if retry_is_deferred(item, now=now) or circuit_open:
            if item_changed:
                changed += 1
            continue
        if attempted >= limit:
            if item_changed:
                changed += 1
            continue
        attempted += 1

        errors = []
        if needs_title:
            try:
                translated_title = clean_line(translate(title))
                if not looks_chinese(translated_title):
                    raise RuntimeError('标题翻译结果仍不是中文')
                item['title_zh'] = translated_title
                item_changed = True
            except Exception as exc:
                errors.append(f'标题: {exc}')

        zh_base = ''
        if needs_summary or needs_ai:
            existing_summary_zh = clean_line(item.get('summary_zh') or '')
            if existing_summary_zh and looks_chinese(existing_summary_zh):
                zh_base = existing_summary_zh
            else:
                try:
                    translated_summary = clean_line(translate(summary_source))
                    if not looks_chinese(translated_summary):
                        raise RuntimeError('摘要翻译结果仍不是中文')
                    zh_base = translated_summary
                except Exception as exc:
                    title_fallback = clean_line(item.get('title_zh') or '')
                    if looks_chinese(title_fallback):
                        source = clean_line(item.get('source') or '')
                        zh_base = f'{title_fallback}。' + (f'来源：{source}。' if source else '')
                    else:
                        zh_base = ''
                        errors.append(f'摘要: {exc}')

        if zh_base and needs_summary:
            item['summary_zh'] = shorten_zh(zh_base, 120)
            item_changed = True
        if zh_base and needs_ai:
            item['ai_summary'] = shorten_zh(zh_base, 60)
            item_changed = True

        if needs_body:
            try:
                if looks_chinese_body(content_excerpt):
                    content_zh = content_excerpt
                else:
                    content_zh = translate_content(content_excerpt)
                item['content_zh'] = content_zh
                item['content_zh_chars'] = len(content_zh)
                item['content_zh_source_hash'] = source_hash
                body_done += 1
                item_changed = True
            except Exception as exc:
                errors.append(f'正文: {exc}')

        if errors:
            item['translation_error'] = '; '.join(errors)[:500]
            item['translation_failures'] = int(item.get('translation_failures') or 0) + 1
            item['translation_retry_after'] = (
                now + timedelta(hours=TRANSLATION_RETRY_HOURS)
            ).isoformat(timespec='seconds')
            failed += 1
            consecutive_failures += 1
            if consecutive_failures >= MAX_CONSECUTIVE_FAILURES:
                circuit_open = True
            item_changed = True
        else:
            consecutive_failures = 0
            for key in ('translation_error', 'translation_retry_after', 'translation_failures'):
                if item.pop(key, None) is not None:
                    item_changed = True

        if item_changed:
            changed += 1

    NEWS_PATH.write_text(json.dumps(news, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    if failed:
        raise RuntimeError(
            f'英文新闻增强存在失败：尝试 {attempted} 条，失败 {failed} 条；已写入冷却状态'
        )
    return f'尝试增强 {attempted} 条英文新闻，更新 {changed} 条，翻译正文 {body_done} 条，失败 {failed} 条'


if __name__ == '__main__':
    print(enhance_news())
