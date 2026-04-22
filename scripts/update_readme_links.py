#!/usr/bin/env python3
import json
import re
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

ROOT = Path('/root/ai-hot')
README = ROOT / 'README.md'
HOT = ROOT / 'data' / 'hot.json'
BRIEFING = ROOT / 'data' / 'briefing.json'
RISING = ROOT / 'data' / 'rising.json'


def update_readme_links():
    if not README.exists() or not HOT.exists():
        return '缺少 README.md 或 hot.json'

    text = README.read_text(encoding='utf-8')
    hot = json.loads(HOT.read_text(encoding='utf-8'))
    briefing = json.loads(BRIEFING.read_text(encoding='utf-8')) if BRIEFING.exists() else {}
    rising = json.loads(RISING.read_text(encoding='utf-8')) if RISING.exists() else {}
    items = hot.get('items') or hot.get('top_20') or hot.get('hot_list') or []

    text = re.sub(r'🕐 \*\*最近更新\*\*：.*', f'🕐 **最近更新**：{datetime.now(ZoneInfo("Asia/Shanghai")).strftime("%Y-%m-%d %H:%M:%S")}', text)

    lines = text.splitlines()
    for idx, line in enumerate(lines):
        m = re.match(r'^(\d+)\. \[(.*?)\]\((.*?)\)$', line)
        if not m:
            continue
        rank = int(m.group(1))
        if rank < 1 or rank > len(items):
            continue
        item = items[rank - 1]
        target = item.get('internal_url') if item.get('type') == 'news' and item.get('internal_url') else item.get('url')
        lines[idx] = f'{rank}. [{m.group(2)}]({target})'

    text = "\n".join(lines)

    summary = briefing.get('content', '').strip()
    emoji = briefing.get('emoji', '⚡')
    date = briefing.get('date', '')
    news_count = briefing.get('news_count', '')
    briefing_block = f'''## 🤖 AI 简报\n\n> {emoji} {summary}\n\n`基于 {news_count} 条新闻 · {date}`\n\n👉 [去网站看完整 AI 新闻与站内文章 →](https://aihot.bt199.com/news/)'''

    text = re.sub(r'## 🤖 每日 AI 快报[\s\S]*?👉 \[去网站看完整 AI 日报与更多快报 →\]\(https://aihot.bt199.com/news/\)', briefing_block, text)

    rising_items = rising.get('items') or []
    rising_lines = []
    for item in rising_items[:5]:
        rising_lines.append(f"- [{item.get('name','未命名')}]({item.get('url','https://aihot.bt199.com/')})：{item.get('reason','最近值得关注')}")
    rising_window = rising.get('window_days', 7)
    rising_block = f"## 📈 热度飙升\n\n" + "\n".join(rising_lines) + f"\n\n👉 [去网站看完整热度飙升榜单 →](https://aihot.bt199.com/)"
    text = re.sub(r'## 📈 热度飙升[\s\S]*?👉 \[去网站看完整热度飙升榜单 →\]\(https://aihot.bt199.com/tools/\)', rising_block, text)

    README.write_text(text + "\n", encoding='utf-8')
    return 'README 热点链接、AI 简报与热度飙升已刷新'


if __name__ == '__main__':
    print(update_readme_links())
