#!/usr/bin/env python3
"""模型数据精简脚本
去重、过滤量化/二创/噪音版本，只保留核心模型
"""

import json
import os
import re
from collections import defaultdict

DATA_DIR = "/root/ai-hot/data"
MODELS_PATH = os.path.join(DATA_DIR, "models.json")

NOISE_PATTERNS = [
    r'gguf', r'gptq', r'awq', r'exl2', r'ggml', r'mlx', r'coreml',
    r'uncensored', r'distill', r'quant', r'int8', r'int4', r'fp8',
    r'mxfp4', r'4bit', r'6bit', r'8bit', r'crack', r'abliterated'
]

PREFERRED_AUTHORS = {
    'openai', 'openai-community', 'meta-llama', 'google', 'qwen', 'zai-org', 'moonshotai',
    'black-forest-labs', 'stabilityai', 'deepseek-ai', 'deepseek', 'mistralai',
    'microsoft', 'tencent', 'baai', 'tiiuae', 'runwayml', 'hunyuan', 'nvidia'
}


def is_noise_model(model):
    text = ' '.join([
        model.get('name', ''),
        model.get('display_name', ''),
        model.get('author', ''),
        ' '.join(model.get('tags', []) or []),
    ]).lower()
    return any(re.search(p, text) for p in NOISE_PATTERNS)


def canonical_key(model):
    name = (model.get('name') or '').strip().lower()
    author = (model.get('author') or '').strip().lower()
    url = (model.get('url') or '').strip().lower()

    if url:
        return url

    base = name.split('/')[-1] if name else (model.get('display_name') or '').strip().lower()
    base = re.sub(r'\s+', '-', base)
    base = re.sub(r'[^a-z0-9.+_-]+', '-', base)
    base = re.sub(r'-+', '-', base).strip('-')

    if author and base:
        return f'{author}/{base}'
    return name or base


def score_model(model):
    score = 0
    author = (model.get('author') or '').lower()
    url = (model.get('url') or '').lower()
    source = (model.get('source') or '').lower()
    likes = model.get('likes', 0) or 0
    downloads = model.get('downloads', 0) or 0

    if author in PREFERRED_AUTHORS:
        score += 100000
    if author and f'/{author}/' in url:
        score += 50000
    if source == 'seed':
        score += 20000
    if source.startswith('hf-'):
        score += 5000

    score += likes * 10
    score += min(downloads // 100, 5000)

    if is_noise_model(model):
        score -= 200000

    return score


def normalize_model(model):
    if not model.get('display_name'):
        name = model.get('name', '')
        if '/' in name:
            name = name.split('/')[-1]
        model['display_name'] = name
    return model


def refine_models():
    with open(MODELS_PATH, 'r', encoding='utf-8') as f:
        models = json.load(f)

    print(f'原始模型数量: {len(models)}')

    normalized = [normalize_model(dict(m)) for m in models]

    deduped = {}
    removed_noise = 0
    replaced_by_better = 0

    for model in normalized:
        key = canonical_key(model)
        current_score = score_model(model)

        if is_noise_model(model):
            removed_noise += 1
            # still allow if no cleaner duplicate exists later? no, drop directly
            continue

        existing = deduped.get(key)
        if not existing:
            deduped[key] = model
            continue

        if current_score > score_model(existing):
            deduped[key] = model
            replaced_by_better += 1

    core_models = list(deduped.values())
    print(f'过滤噪音版本: {removed_noise} 个')
    print(f'去重后核心模型: {len(core_models)} 个')

    by_pipeline = defaultdict(list)
    for m in core_models:
        tag = m.get('pipeline_tag') or 'other'
        by_pipeline[tag].append(m)

    refined = []
    limits = {
        'text-generation': 24,
        'image-text-to-text': 20,
        'text-to-image': 18,
        'automatic-speech-recognition': 10,
        'text-to-speech': 8,
        'image-to-video': 8,
        'video-to-video': 8,
        'any-to-any': 8,
        'image-to-3d': 6,
        'translation': 6,
        'other': 12,
    }

    for tag, group in by_pipeline.items():
        limit = limits.get(tag, 10)
        sorted_group = sorted(group, key=score_model, reverse=True)
        kept = sorted_group[:limit]
        refined.extend(kept)
        print(f'  {tag}: {len(group)} → {len(kept)}')

    refined = sorted(refined, key=score_model, reverse=True)

    for i, m in enumerate(refined, start=1):
        m['display_priority'] = i
        m['is_core'] = True

    with open(MODELS_PATH, 'w', encoding='utf-8') as f:
        json.dump(refined, f, ensure_ascii=False, indent=2)

    print(f'\n✅ 模型精简完成: {len(models)} → {len(refined)}')
    print(f'✅ 去重替换更优版本: {replaced_by_better}')
    print('已保存到 models.json')


if __name__ == '__main__':
    refine_models()
