#!/usr/bin/env python3
"""根据 data/tools.json 生成可收录的静态工具详情页。"""

from pathlib import Path
import json
import re

ROOT = Path('/root/ai-hot')
TOOLS_JSON = ROOT / 'data' / 'tools.json'
CONTENT_DIR = ROOT / 'site' / 'content' / 'tools'
GENERATED_MARKER = '<!-- AUTO-GENERATED: tool page -->\n'


def esc(value: str) -> str:
    value = '' if value is None else str(value)
    return value.replace('\\', '\\\\').replace('"', '\\"')


def slugify(value: str) -> str:
    value = (value or '').strip().lower()
    value = re.sub(r'[^a-z0-9\u4e00-\u9fff]+', '-', value)
    value = re.sub(r'-+', '-', value).strip('-')
    return value or 'tool'


def toml_array(items):
    if not items:
        return '[]'
    return '[' + ', '.join(f'"{esc(x)}"' for x in items) + ']'


def build_keywords(tool):
    parts = [tool.get('name', ''), tool.get('category', ''), 'AI工具', 'AI热榜']
    parts.extend([t.lstrip('#') for t in (tool.get('tags') or [])][:6])
    if tool.get('alternatives'):
        parts.append('替代方案')
    seen = []
    for item in parts:
        item = (item or '').strip()
        if item and item not in seen:
            seen.append(item)
    return ', '.join(seen)


def build_page(tool):
    tool_id = tool.get('id') or slugify(tool.get('name', ''))
    name = tool.get('name', tool_id)
    category = tool.get('category', 'AI工具')
    description = tool.get('description') or f'{name} 的价格、功能、优缺点与替代方案。'
    seo_title = f'{name} 是什么？价格、优缺点、替代方案 - AI热榜'
    seo_description = f'{name}：{description} 这里整理了价格、免费额度、适合人群、优缺点和替代方案，帮助你快速判断它值不值得用。'
    lines = [
        '+++',
        f'title = "{esc(name)}"',
        f'description = "{esc(description)}"',
        f'seo_title = "{esc(seo_title)}"',
        f'seo_description = "{esc(seo_description)}"',
        f'seo_keywords = "{esc(build_keywords(tool))}"',
        f'slug = "{esc(tool_id)}"',
        'type = "tools"',
        '',
        '[params]',
        f'id = "{esc(tool_id)}"',
        f'name = "{esc(name)}"',
        f'url = "{esc(tool.get("url", ""))}"',
        f'category = "{esc(category)}"',
        f'pricing = "{esc(tool.get("pricing", ""))}"',
        f'free_quota = "{esc(tool.get("free_quota", ""))}"',
        f'difficulty = {int(tool.get("difficulty", 0) or 0)}',
        f'trending = {str(bool(tool.get("trending"))).lower()}',
        f'featured = {str(bool(tool.get("featured"))).lower()}',
        f'use_cases = "{esc(tool.get("use_cases", ""))}"',
        f'score = {int(tool.get("score", 0) or 0)}',
        f'tags = {toml_array(tool.get("tags") or [])}',
        f'pros = {toml_array(tool.get("pros") or [])}',
        f'cons = {toml_array(tool.get("cons") or [])}',
        f'best_for = {toml_array(tool.get("best_for") or [])}',
        f'alternatives = {toml_array(tool.get("alternatives") or [])}',
        '+++',
        '',
        GENERATED_MARKER.rstrip(),
        '',
        f'{name} 是一款偏 {category} 场景的 AI 工具。这里整理了它的价格、免费额度、优缺点、适合人群和替代方案，方便直接判断是否值得用。',
        '',
    ]
    return '\n'.join(lines) + '\n'


def generate_tool_pages():
    tools = json.loads(TOOLS_JSON.read_text(encoding='utf-8'))
    CONTENT_DIR.mkdir(parents=True, exist_ok=True)

    keep = {'_index.md'}
    generated = 0
    for tool in tools:
        tool_id = tool.get('id') or slugify(tool.get('name', ''))
        path = CONTENT_DIR / f'{tool_id}.md'
        path.write_text(build_page(tool), encoding='utf-8')
        keep.add(path.name)
        generated += 1

    for path in CONTENT_DIR.glob('*.md'):
        if path.name not in keep:
            text = path.read_text(encoding='utf-8', errors='ignore')
            if GENERATED_MARKER in text:
                path.unlink()

    return f'生成 {generated} 个静态工具详情页'


if __name__ == '__main__':
    print(generate_tool_pages())
