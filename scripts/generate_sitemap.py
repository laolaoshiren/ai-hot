#!/usr/bin/env python3
"""
生成 sitemap.xml
"""

import json
import os
from datetime import datetime

DATA_DIR = "/root/ai-hot/data"
SITE_DIR = "/root/ai-hot/site/static"
BASE_URL = "https://laolaoshiren.github.io/ai-hot"

def generate_sitemap():
    urls = []
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 主要页面
    pages = [
        {"loc": "/", "priority": "1.0", "changefreq": "daily"},
        {"loc": "/search/", "priority": "0.8", "changefreq": "weekly"},
        {"loc": "/compare/", "priority": "0.8", "changefreq": "weekly"},
        {"loc": "/tools/", "priority": "0.9", "changefreq": "daily"},
        {"loc": "/models/", "priority": "0.9", "changefreq": "daily"},
        {"loc": "/agents/", "priority": "0.8", "changefreq": "weekly"},
        {"loc": "/news/", "priority": "0.8", "changefreq": "daily"},
        {"loc": "/providers/", "priority": "0.7", "changefreq": "weekly"},
    ]
    
    for page in pages:
        urls.append({
            "loc": BASE_URL + page["loc"],
            "lastmod": today,
            "changefreq": page["changefreq"],
            "priority": page["priority"]
        })
    
    # 工具详情页
    try:
        with open(f"{DATA_DIR}/tools.json", "r") as f:
            tools = json.load(f)
        for tool in tools:
            if tool.get("id"):
                urls.append({
                    "loc": f"{BASE_URL}/tool/?id={tool['id']}",
                    "lastmod": today,
                    "changefreq": "weekly",
                    "priority": "0.7"
                })
        print(f"  ✓ 添加 {len(tools)} 个工具页面")
    except Exception as e:
        print(f"  ⚠️ 读取tools.json失败: {e}")
    
    # 生成XML
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
    
    # 保存
    output_path = f"{SITE_DIR}/sitemap.xml"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(xml)
    
    print(f"\n✅ 生成 sitemap.xml: {len(urls)} 个URL")
    print(f"   保存到: {output_path}")
    
    return len(urls)


if __name__ == "__main__":
    generate_sitemap()