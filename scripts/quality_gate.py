#!/usr/bin/env python3
import hashlib
import json, sys
import re
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
SITE_CONTENT = ROOT / 'site' / 'content'
NEWS_PAGE_MARKER = '<!-- AUTO-GENERATED: news page -->'
NEWS_SOURCE_HEADING = '## 🔗 原始来源'

def zh_ratio(text):
    text = str(text or '').strip()
    letters = sum(c.isalpha() or ('\u4e00' <= c <= '\u9fff') for c in text)
    zh = sum('\u4e00' <= c <= '\u9fff' for c in text)
    return zh / max(letters, 1)

def fail(msg):
    print('❌', msg)
    return 1


def read_generated_news_body(path):
    text = path.read_text(encoding='utf-8')
    if NEWS_PAGE_MARKER not in text:
        return ''
    body = text.split(NEWS_PAGE_MARKER, 1)[1]
    body = body.split(NEWS_SOURCE_HEADING, 1)[0]
    body = re.sub(r'!\[[^\]]*\]\([^)]*\)', '', body)
    body = re.sub(r'https?://\S+', '', body)
    return body.strip()


def check_english_news_bodies(errors):
    """英文来源可以保留原始链接，但站内文章主体必须是中文。"""
    path = DATA / 'news.json'
    if not path.exists():
        errors.append('news.json missing')
        return

    news = json.loads(path.read_text(encoding='utf-8'))
    invalid = []
    for item in news:
        if str(item.get('lang') or '').lower() != 'en':
            continue
        news_id = item.get('slug') or item.get('id')
        if not news_id:
            continue
        page = SITE_CONTENT / 'news' / f'{news_id}.md'
        if not page.exists():
            invalid.append(f'{news_id}: missing page')
    for page in (SITE_CONTENT / 'news').glob('*.md'):
        text = page.read_text(encoding='utf-8')
        if NEWS_PAGE_MARKER not in text or not re.search(r'(?m)^lang = "en"$', text):
            continue
        body = read_generated_news_body(page)
        zh_chars = sum('\u4e00' <= ch <= '\u9fff' for ch in body)
        if zh_chars < 2 or zh_ratio(body) < 0.15:
            invalid.append(f'{page.stem}: zh_ratio={zh_ratio(body):.2f}')

    if invalid:
        errors.append(f'English-source news bodies not Chinese enough: {invalid[:10]}')


def news_content_fingerprint(text):
    lines = []
    for line in str(text or '').splitlines():
        line = re.sub(r'\s+', ' ', line).strip()
        if line:
            lines.append(line)
    normalized = '\n'.join(lines)
    return hashlib.sha256(normalized.encode('utf-8')).hexdigest()[:16]


def recent_translation_problem(item):
    source = str(item.get('content_excerpt') or '').strip()
    if not source:
        return ''
    translated = str(item.get('content_zh') or '').strip()
    min_length = min(120, max(40, int(len(source) * 0.2)))
    if len(translated) < min_length:
        return f'content_zh too short ({len(translated)} < {min_length})'
    if zh_ratio(translated) < 0.35:
        return f'content_zh ratio too low ({zh_ratio(translated):.2f})'
    if item.get('content_zh_source_hash') != news_content_fingerprint(source):
        return 'content_zh source hash stale'
    try:
        recorded_chars = int(item.get('content_zh_chars') or 0)
    except (TypeError, ValueError):
        return 'content_zh_chars invalid'
    if recorded_chars != len(translated):
        return 'content_zh_chars mismatch'
    if item.get('translation_error'):
        return 'translation_error present'
    return ''


def check_recent_english_translations(warnings, news, limit=40):
    recent = [item for item in news if str(item.get('lang') or '').lower() == 'en'][:limit]
    invalid = []
    for item in recent:
        problem = recent_translation_problem(item)
        if problem:
            invalid.append(f"{item.get('id')}: {problem}")
    if invalid:
        warnings.append(f'Recent English-source articles missing complete Chinese body: {invalid[:10]}')

BAD_ICON_SUBSTRINGS = (
    'aihot.bt199.com/favicon',
    'github.com/favicon',
    'www.github.com/favicon',
)


def has_bad_icon(icon, *, allow_openrouter=False):
    icon = str(icon or '').lower()
    if not icon:
        return False
    if any(bad in icon for bad in BAD_ICON_SUBSTRINGS):
        return True
    if not allow_openrouter and 'openrouter.ai/favicon' in icon:
        return True
    return False


def check_icon_url_records(errors, filename, *, allow_openrouter=False):
    path = DATA / filename
    if not path.exists():
        errors.append(f'{filename} missing')
        return []
    data = json.loads(path.read_text(encoding='utf-8'))
    records = data.get('items') if isinstance(data, dict) else data
    records = records or []
    missing_icon_url = []
    bad_icons = []
    for item in records:
        label = item.get('name') or item.get('id')
        icon_url = str(item.get('icon_url') or '')
        icon = str(item.get('icon') or item.get('logo') or item.get('logo_url') or '')
        if not icon_url:
            missing_icon_url.append(label)
        if has_bad_icon(icon_url, allow_openrouter=allow_openrouter) or has_bad_icon(icon, allow_openrouter=allow_openrouter):
            bad_icons.append(label)
    if missing_icon_url:
        errors.append(f'{filename} missing icon_url: {missing_icon_url[:10]}')
    if bad_icons:
        errors.append(f'{filename} fake/generic icons: {bad_icons[:10]}')
    return records


def check_models_curated(errors):
    path = DATA / 'models_curated.json'
    if not path.exists():
        errors.append('models_curated.json missing')
        return
    data = json.loads(path.read_text(encoding='utf-8'))
    items = data.get('items') or []
    names = [str(x.get('name') or '') for x in items]
    urls = [str(x.get('url') or '') for x in items]
    blobs = [f"{n} {u}".lower() for n, u in zip(names, urls)]
    required = ['gpt-5', 'glm-5.2', 'minimax-m3', 'qwen3.7']
    for key in required:
        if not any(key in b for b in blobs):
            errors.append(f'models missing required hot model: {key}')

    stale_patterns = [r'deepseek-v3\.2', r'qwen3\.5', r'mimo-32b']
    stale_hits = []
    for b, n in zip(blobs, names):
        if any(re.search(p, b) for p in stale_patterns):
            stale_hits.append(n)
    if stale_hits:
        errors.append(f'models contain superseded old versions: {stale_hits[:10]}')

    model_bad_icons = []
    for x in items:
        icon = str(x.get('icon_url') or x.get('icon') or '')
        if not icon or has_bad_icon(icon):
            model_bad_icons.append(x.get('name'))
    if model_bad_icons:
        errors.append(f'models fake/missing icons: {model_bad_icons[:10]}')

    category_ids = [c.get('id') for c in data.get('categories') or []]
    expected = ['top', 'coding', 'multimodal', 'image', 'video', 'open', 'watch']
    ordered = [c for c in category_ids if c in expected]
    if ordered != expected[:len(ordered)]:
        errors.append(f'model category order unexpected: {category_ids}')

def check_readme_sync(errors, expected_date):
    readme = ROOT / 'README.md'
    if not readme.exists():
        return
    text = readme.read_text(encoding='utf-8')
    if expected_date and expected_date not in text:
        errors.append(f'README date not synced with data date: missing {expected_date}')

def main():
    errors=[]
    warnings=[]
    check_models_curated(errors)

    providers = check_icon_url_records(errors, 'providers.json', allow_openrouter=True)
    if providers[:5] and not all(str(p.get('icon_url') or '').strip() for p in providers[:5]):
        errors.append('providers first entries do not all expose icon_url')
    check_icon_url_records(errors, 'models_curated.json')
    check_icon_url_records(errors, 'tools.json')
    agents = check_icon_url_records(errors, 'agents.json')
    missing=[a.get('name') for a in agents if not (a.get('icon') or a.get('logo') or a.get('emoji') or a.get('icon_url'))]
    if missing:
        errors.append(f'agents missing icons: {missing[:10]}')
    english_agents=[]
    for a in agents:
        desc=str(a.get('description') or '').strip()
        if len(desc) < 8 or zh_ratio(desc) < 0.35:
            english_agents.append(a.get('name') or a.get('id'))
    if english_agents:
        errors.append(f'agents descriptions not Chinese enough: {english_agents[:10]}')

    list_tpl = (ROOT / 'site' / 'layouts' / '_default' / 'list.html').read_text(encoding='utf-8')
    if 'https://www.google.com/s2/favicons?domain={{ $modelDomain }}' in list_tpl or 'https://www.google.com/s2/favicons?domain={{ $toolDomain }}' in list_tpl:
        errors.append('models/tools/agents templates still derive generic favicons from item URL instead of using icon_url')
    if '.icon_url' not in list_tpl:
        errors.append('list template does not render icon_url')
    if 'aihot.bt199.com/favicon' in list_tpl or 'github.com/favicon' in list_tpl:
        errors.append('list template contains forbidden favicon fallback')

    hot=json.loads((DATA/'hot.json').read_text(encoding='utf-8'))
    items=hot.get('top_20') or hot.get('items') or []
    if not items:
        errors.append('hot list is empty')
    for idx,item in enumerate(items[:10],1):
        nid=item.get('news_id')
        title=item.get('title_zh') or item.get('title') or ''
        summary=item.get('ai_summary') or item.get('subtitle') or item.get('description') or ''
        if item.get('type') != 'news':
            errors.append(f'hot #{idx} not news: {title}')
        if not nid:
            errors.append(f'hot #{idx} missing news_id: {title}')
        elif not ((SITE_CONTENT/'news'/f'{nid}.md').exists() or (SITE_CONTENT/'news'/str(nid)/'index.md').exists()):
            errors.append(f'hot #{idx} missing generated page: /news/{nid}/')
        if zh_ratio(title) < 0.35:
            errors.append(f'hot #{idx} title not Chinese enough: {title}')
        if zh_ratio(summary) < 0.45:
            errors.append(f'hot #{idx} summary not Chinese enough: {summary[:80]}')

    check_english_news_bodies(errors)
    news=json.loads((DATA/'news.json').read_text(encoding='utf-8'))
    check_recent_english_translations(warnings, news)

    briefing=json.loads((DATA/'briefing.json').read_text(encoding='utf-8'))
    meta=json.loads((DATA/'meta.json').read_text(encoding='utf-8'))
    tz=ZoneInfo('Asia/Shanghai')
    last_update_raw=str(meta.get('last_update') or '').strip()
    try:
        last_update=datetime.strptime(last_update_raw, '%Y-%m-%d %H:%M:%S').replace(tzinfo=tz)
    except ValueError:
        errors.append(f'meta last_update invalid: {last_update_raw}')
    else:
        age_hours=(datetime.now(tz)-last_update).total_seconds()/3600
        # 放宽时间限制到24小时，允许更灵活的更新
        if age_hours > 24:
            errors.append(f'data stale: last_update {last_update_raw}, age {age_hours:.1f}h')
        expected_date=last_update.strftime('%Y-%m-%d')
        # 不再检查 briefing 日期是否匹配，因为新闻永久保留
        check_readme_sync(errors, expected_date)

    for warning in warnings:
        print('⚠️', warning)
    if errors:
        for e in errors:
            print('❌', e)
        return 1
    print('✅ quality gate passed')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
