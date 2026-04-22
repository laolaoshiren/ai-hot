#!/usr/bin/env python3
"""生成 sitemap.xml（含静态工具详情页）"""

import json
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

ROOT = Path('/root/ai-hot')
DATA_DIR = ROOT / 'data'
SITE_DIR = ROOT / 'site' / 'static'
BASE_URL = 'https://aihot.bt199.com'
SH_TZ = ZoneInfo('Asia/Shanghai')


def today_str():
    return datetime.now(SH_TZ).strftime('%Y-%m-%d')


def build_url(loc: str, priority: str, changefreq: str, lastmod: str):
    return {
        'loc': BASE_URL + loc,
        'lastmod': lastmod,
        'changefreq': changefreq,
        'priority': priority,
    }


def write_sitemap(filename: str, urls):
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url in urls:
        xml += '  <url>\n'
        xml += f'    <loc>{url["loc"]}</loc>\n'
        xml += f'    <lastmod>{url["lastmod"]}</lastmod>\n'
        xml += f'    <changefreq>{url["changefreq"]}</changefreq>\n'
        xml += f'    <priority>{url["priority"]}</priority>\n'
        xml += '  </url>\n'
    xml += '</urlset>'
    out = SITE_DIR / filename
    out.write_text(xml, encoding='utf-8')
    return out


def generate_sitemap():
    today = today_str()
    SITE_DIR.mkdir(parents=True, exist_ok=True)

    page_urls = [
        build_url('/', '1.0', 'daily', today),
        build_url('/search/', '0.8', 'weekly', today),
        build_url('/compare/', '0.8', 'weekly', today),
        build_url('/tools/', '0.9', 'daily', today),
        build_url('/models/', '0.9', 'daily', today),
        build_url('/agents/', '0.8', 'weekly', today),
        build_url('/news/', '0.8', 'daily', today),
        build_url('/providers/', '0.7', 'weekly', today),
    ]

    tool_urls = []
    tools = json.loads((DATA_DIR / 'tools.json').read_text(encoding='utf-8'))
    for tool in tools:
        tool_id = tool.get('id')
        if tool_id:
            tool_urls.append(build_url(f'/tools/{tool_id}/', '0.7', 'weekly', today))

    news_urls = []
    news = json.loads((DATA_DIR / 'news.json').read_text(encoding='utf-8'))
    for item in news:
        news_id = item.get('id')
        if news_id:
            news_urls.append(build_url(f'/news/{news_id}/', '0.7', 'daily', today))

    write_sitemap('sitemap-pages.xml', page_urls)
    write_sitemap('sitemap-tools.xml', tool_urls)
    write_sitemap('sitemap-news.xml', news_urls)

    index_xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    index_xml += '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for name in ['sitemap-pages.xml', 'sitemap-tools.xml', 'sitemap-news.xml']:
        index_xml += '  <sitemap>\n'
        index_xml += f'    <loc>{BASE_URL}/{name}</loc>\n'
        index_xml += f'    <lastmod>{today}</lastmod>\n'
        index_xml += '  </sitemap>\n'
    index_xml += '</sitemapindex>'
    (SITE_DIR / 'sitemap.xml').write_text(index_xml, encoding='utf-8')

    print(f'  ✓ 页面 sitemap: {len(page_urls)} 个URL')
    print(f'  ✓ 工具 sitemap: {len(tool_urls)} 个URL')
    print(f'  ✓ 新闻 sitemap: {len(news_urls)} 个URL')
    print(f'\n✅ 生成 sitemap 索引: {len(page_urls) + len(tool_urls) + len(news_urls)} 个URL')
    return len(page_urls) + len(tool_urls) + len(news_urls)


if __name__ == '__main__':
    print(generate_sitemap())
