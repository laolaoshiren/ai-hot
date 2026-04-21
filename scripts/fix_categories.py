#!/usr/bin/env python3
"""
修复工具分类错误
"""

import json

DATA_DIR = "/root/ai-hot/data"

# 需要修正的工具和正确分类
CATEGORY_FIXES = {
    "Jasper": "营销",
    "Copy.ai": "营销",
    "Adobe Firefly": "设计",
    "Runway ML": "设计",
    "DALL-E 3": "绘画",  # 保持绘画分类
    "Midjourney": "绘画",  # 保持绘画分类
    "Stable Diffusion": "绘画",  # 保持绘画分类
}

def fix_categories():
    with open(f"{DATA_DIR}/tools.json", "r") as f:
        tools = json.load(f)
    
    print(f"工具总数: {len(tools)}")
    
    fixed_count = 0
    for tool in tools:
        name = tool.get('name', '')
        if name in CATEGORY_FIXES:
            old_category = tool.get('category', '')
            new_category = CATEGORY_FIXES[name]
            if old_category != new_category:
                tool['category'] = new_category
                fixed_count += 1
                print(f"  ✅ {name}: '{old_category}' → '{new_category}'")
    
    # 保存修改
    with open(f"{DATA_DIR}/tools.json", "w") as f:
        json.dump(tools, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 修复了 {fixed_count} 个工具的分类")
    
    # 统计修复后的分类分布
    from collections import Counter
    categories = Counter([t.get('category', '未分类') for t in tools])
    
    print("\n📊 修复后工具分类分布:")
    for cat, count in categories.most_common():
        print(f"  {cat}: {count}")

if __name__ == "__main__":
    fix_categories()