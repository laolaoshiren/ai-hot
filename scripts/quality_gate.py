#!/usr/bin/env python3
import json, sys
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
SITE_CONTENT = ROOT / 'site' / 'content'

def zh_ratio(text):
    text = str(text or '').strip()
    letters = sum(c.isalpha() or ('\u4e00' <= c <= '\u9fff') for c in text)
    zh = sum('\u4e00' <= c <= '\u9fff' for c in text)
    return zh / max(letters, 1)

def fail(msg):
    print('❌', msg)
    return 1

def main():
    errors=[]
    agents=json.loads((DATA/'agents.json').read_text(encoding='utf-8'))
    missing=[a.get('name') for a in agents if not (a.get('icon') or a.get('logo') or a.get('emoji'))]
    if missing:
        errors.append(f'agents missing icons: {missing[:10]}')

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

    briefing=json.loads((DATA/'briefing.json').read_text(encoding='utf-8'))
    today=datetime.now(ZoneInfo('Asia/Shanghai')).strftime('%Y-%m-%d')
    if briefing.get('date') != today:
        errors.append(f'briefing date stale: {briefing.get("date")} != {today}')

    if errors:
        for e in errors:
            print('❌', e)
        return 1
    print('✅ quality gate passed')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
