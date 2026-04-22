#!/usr/bin/env python3
import json
import os
import urllib.request
from datetime import datetime, timezone

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
PROVIDERS_PATH = os.path.join(DATA_DIR, 'providers.json')
OPENROUTER_MODELS_URL = 'https://openrouter.ai/api/v1/models'

PROVIDER_PREFIX_MAP = {
    'openai': ['openai'],
    'anthropic': ['anthropic'],
    'google': ['google'],
    'deepseek': ['deepseek'],
    'alibaba': ['qwen', 'alibaba'],
    'baidu': ['baidu'],
    'bytedance': ['bytedance-seed', 'bytedance'],
    'tencent': ['tencent'],
    'moonshot': ['moonshotai'],
    'zhipu': ['z-ai'],
    'minimax': ['minimax'],
    'mistral': ['mistralai'],
    'meta': ['meta-llama'],
    'xai': ['x-ai'],
    'nvidia': ['nvidia'],
    'aws-bedrock': [],
    'azure-openai': [],
    'openrouter': ['openrouter'],
    'together': [],
    'groq': [],
    'siliconflow': [],
    'volcengine': [],
}

PLATFORM_IDS = {'aws-bedrock', 'azure-openai', 'together', 'groq', 'siliconflow', 'volcengine', 'openrouter'}
MODEL_AUTHOR_IDS = {
    'openai', 'anthropic', 'google', 'deepseek', 'alibaba', 'baidu', 'bytedance',
    'tencent', 'moonshot', 'zhipu', 'minimax', 'mistral', 'meta', 'xai', 'nvidia'
}


def fetch_openrouter_models():
    req = urllib.request.Request(OPENROUTER_MODELS_URL, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp).get('data', [])


def ts_to_date(ts):
    if not ts:
        return ''
    return datetime.fromtimestamp(ts, tz=timezone.utc).strftime('%Y-%m-%d')


def clean_model_name(name):
    if not name:
        return ''
    out = name
    prefixes = [
        'OpenAI: ', 'Anthropic: ', 'Google: ', 'DeepSeek: ', 'Qwen: ', 'Baidu: ',
        'ByteDance Seed: ', 'MoonshotAI: ', 'Z.ai: ', 'MiniMax: ', 'Mistral: ',
        'Meta: ', 'xAI: ', 'NVIDIA: ', 'Amazon: ', 'Tencent: '
    ]
    for p in prefixes:
        if out.startswith(p):
            out = out[len(p):]
            break
    return out.replace('  ', ' ').strip()


def derive_modalities(models):
    labels = []
    seen = set()
    for m in models[:8]:
        arch = m.get('architecture') or {}
        inputs = arch.get('input_modalities') or []
        outputs = arch.get('output_modalities') or []
        merged = set(inputs) | set(outputs)
        if 'video' in merged:
            label = '视频'
        elif 'audio' in merged:
            label = '音频'
        elif 'image' in merged and 'text' in merged:
            label = '多模态'
        elif 'image' in merged:
            label = '图像'
        elif 'text' in merged:
            label = '文本'
        else:
            continue
        if label not in seen:
            seen.add(label)
            labels.append(label)
    return labels[:4]


def classify_provider(provider):
    pid = provider.get('id')
    if pid in PLATFORM_IDS:
        return 'platform'
    if pid in MODEL_AUTHOR_IDS:
        return 'model_author'
    return 'manual'


def summarize_provider(provider, matched_models):
    provider_kind = classify_provider(provider)
    provider['provider_kind'] = provider_kind

    if provider_kind == 'platform':
        provider['source'] = 'manual'
        provider['latest_models'] = provider.get('models', [])[:3]
        provider['model_count'] = 0
        provider['last_updated'] = ''
        provider['modalities'] = []
        provider['live_summary'] = '平台型提供商，展示的是接入能力与生态，不直接等同于某个模型作者'
        return provider

    if not matched_models:
        provider['source'] = 'manual'
        provider['latest_models'] = provider.get('models', [])[:3]
        provider['model_count'] = 0
        provider['last_updated'] = ''
        provider['modalities'] = []
        provider['live_summary'] = '站内手工维护，待补充实时模型索引'
        return provider

    matched_models = sorted(matched_models, key=lambda x: x.get('created', 0), reverse=True)
    latest = matched_models[:3]
    latest_names = [clean_model_name(m.get('name') or m.get('id')) for m in latest]

    provider['source'] = 'openrouter'
    provider['latest_models'] = latest_names
    provider['model_count'] = len(matched_models)
    provider['last_updated'] = ts_to_date(latest[0].get('created'))
    provider['modalities'] = derive_modalities(matched_models)
    provider['live_summary'] = f"OpenRouter 已收录 {len(matched_models)} 个该作者/厂商相关模型，最近更新为 {latest_names[0]}"
    return provider


def update_providers():
    with open(PROVIDERS_PATH, 'r', encoding='utf-8') as f:
        providers = json.load(f)

    models = fetch_openrouter_models()
    by_prefix = {}
    for model in models:
        model_id = model.get('id', '')
        prefix = model_id.split('/')[0] if '/' in model_id else model_id
        by_prefix.setdefault(prefix, []).append(model)

    updated = []
    live_count = 0
    for provider in providers:
        prefixes = PROVIDER_PREFIX_MAP.get(provider.get('id'), [])
        matched = []
        for prefix in prefixes:
            matched.extend(by_prefix.get(prefix, []))
        summarize_provider(provider, matched)
        if matched and provider.get('source') == 'openrouter':
            live_count += 1
        updated.append(provider)

    with open(PROVIDERS_PATH, 'w', encoding='utf-8') as f:
        json.dump(updated, f, ensure_ascii=False, indent=2)

    return f'更新 {len(updated)} 家提供商，其中 {live_count} 家为模型作者型实时索引'


if __name__ == '__main__':
    print(update_providers())
