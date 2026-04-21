#!/usr/bin/env python3
"""
模型数据精简脚本
过滤 GGUF/GPTQ/AWQ/量化版本，只保留核心模型
"""

import json
import re
from collections import defaultdict

DATA_DIR = "/root/ai-hot/data"

def is_quantized_version(name):
    """判断是否是量化版本"""
    patterns = [
        r'gguf', r'gptq', r'awq', r'exl2', r'q[0-9]', 
        r'[0-9]+bit', r'k_s', r'k_m', r'q[0-9]_',
        r'ggml', r'q[0-9]_[0-9]'
    ]
    name_lower = name.lower()
    return any(re.search(p, name_lower) for p in patterns)

def get_base_model_name(name):
    """获取基础模型名称（去掉量化后缀）"""
    # 去掉常见量化后缀
    suffixes = [
        '-gguf', '-gptq', '-awq', '-exl2',
        '-q[0-9]', '-q[0-9]_[0-9]', '-[0-9]bit',
        '-k_s', '-k_m', '-ggml'
    ]
    for suffix in suffixes:
        name = re.sub(f'{suffix}.*', '', name, flags=re.IGNORECASE)
    return name

def refine_models():
    with open(f"{DATA_DIR}/models.json", "r") as f:
        models = json.load(f)
    
    print(f"原始模型数量: {len(models)}")
    
    # 1. 过滤量化版本
    core_models = []
    quantized_models = []
    
    for m in models:
        name = m.get('name', '')
        if is_quantized_version(name):
            quantized_models.append(m)
        else:
            core_models.append(m)
    
    print(f"过滤量化版本: {len(quantized_models)} 个")
    print(f"剩余核心模型: {len(core_models)} 个")
    
    # 2. 按 pipeline_tag 分组
    by_pipeline = defaultdict(list)
    for m in core_models:
        tag = m.get('pipeline_tag', 'other')
        if not tag:
            tag = 'other'
        by_pipeline[tag].append(m)
    
    # 3. 每个分类保留 Top 15（按likes排序）
    refined = []
    for tag, group in by_pipeline.items():
        # 过滤掉没有likes的模型
        group_with_likes = [m for m in group if m.get('likes')]
        group_without_likes = [m for m in group if not m.get('likes')]
        
        # 按likes排序，取前15
        sorted_models = sorted(group_with_likes, key=lambda x: x.get('likes', 0), reverse=True)
        top_15 = sorted_models[:15]
        
        # 添加到精简列表
        refined.extend(top_15)
        
        print(f"  {tag}: {len(group)} → {len(top_15)} (likes排序)")
    
    # 4. 添加元数据字段
    for i, m in enumerate(refined):
        m['id'] = f"model-{i+1}"
        m['display_priority'] = i + 1
        m['is_core'] = True
        
        # 生成更友好的显示名称
        if not m.get('display_name'):
            name = m.get('name', '')
            # 去掉作者前缀
            if '/' in name:
                name = name.split('/')[-1]
            m['display_name'] = name
    
    # 5. 保存精简后的模型
    with open(f"{DATA_DIR}/models.json", "w") as f:
        json.dump(refined, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 模型精简完成: {len(models)} → {len(refined)}")
    print("已保存到 models.json")
    
    # 6. 统计分布
    by_source = defaultdict(int)
    by_pipeline = defaultdict(int)
    for m in refined:
        url = m.get('url', '')
        if 'huggingface.co' in url:
            by_source['HuggingFace'] += 1
        elif 'github.com' in url:
            by_source['GitHub'] += 1
        else:
            by_source['其他'] += 1
            
        tag = m.get('pipeline_tag', 'other')
        if not tag:
            tag = 'other'
        by_pipeline[tag] += 1
    
    print("\n📊 精简后分布:")
    print("来源统计:")
    for source, count in by_source.items():
        print(f"  {source}: {count}")
    
    print("\n任务类型统计:")
    for tag, count in sorted(by_pipeline.items(), key=lambda x: x[1], reverse=True):
        print(f"  {tag}: {count}")

if __name__ == "__main__":
    refine_models()