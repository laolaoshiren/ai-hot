#!/usr/bin/env python3
"""生成精选模型榜单：最前沿 / 最热门 / 最实用，而不是模型垃圾堆。"""

import json
import os
import urllib.request
from datetime import datetime, timezone

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
MODELS_PATH = os.path.join(DATA_DIR, 'models.json')
OUTPUT_PATH = os.path.join(DATA_DIR, 'models_curated.json')
OPENROUTER_URL = 'https://openrouter.ai/api/v1/models'

CATEGORY_ORDER = [
    ('top', '🔥 顶级通用大模型', '现在最值得关注、综合能力最强的一线模型'),
    ('coding', '💻 编程最强模型', '写代码、改代码、做 Agent 开发最常用的一批模型'),
    ('multimodal', '👁️ 多模态主力模型', '图文理解、视觉问答、复杂输入处理的主力模型'),
    ('image', '🎨 图像生成主力', '当前最常用、效果最稳的一线生图模型'),
    ('video', '🎬 视频生成主力', '当下最值得关注的视频生成模型与工作流主力'),
    ('open', '🌍 开源旗舰模型', '社区采用度高、真正有人用的开源主力模型'),
    ('watch', '🧪 值得关注的新锐模型', '还在快速爬升、值得盯着看的新一代模型'),
]

CURATED_ITEMS = [
    # 顶级通用
    {'category': 'top', 'source': 'openrouter-latest', 'provider_prefix': 'openai', 'family': 'gpt', 'variant': 'base', 'label': '综合王者', 'why': 'OpenAI 最新一线通用主力，推理、写作、执行力都很强'},
    {'category': 'top', 'source': 'openrouter', 'id': 'anthropic/claude-opus-4.7', 'label': '长文与复杂任务', 'why': '复杂任务稳定性强，长上下文和专业写作很能打'},
    {'category': 'top', 'source': 'openrouter', 'id': 'x-ai/grok-4.20', 'label': '热点与推理', 'why': '新一代旗舰之一，热度高、讨论度强'},
    {'category': 'top', 'source': 'openrouter', 'id': 'z-ai/glm-5.1', 'label': '国产主力', 'why': '国产新一代通用模型代表，更新积极'},
    {'category': 'top', 'source': 'openrouter', 'id': 'deepseek/deepseek-v3.2', 'label': '高性价比', 'why': '推理/代码/成本平衡优秀，采用度高'},

    # 编程
    {'category': 'coding', 'source': 'openrouter-latest', 'provider_prefix': 'openai', 'family': 'gpt', 'variant': 'pro', 'label': '重度编码', 'why': 'OpenAI 最新 Pro 线，适合复杂工程任务和严肃编程场景'},
    {'category': 'coding', 'source': 'openrouter', 'id': 'anthropic/claude-sonnet-4.6', 'label': '开发者高频', 'why': 'Claude Code 生态热门底座，真实开发采用广'},
    {'category': 'coding', 'source': 'openrouter', 'id': 'qwen/qwen3.6-plus', 'label': '国产编码主力', 'why': '代码与通用兼顾，近期更新快'},
    {'category': 'coding', 'source': 'huggingface', 'url': 'https://huggingface.co/Qwen/Qwen3-Coder-Next', 'label': '开源代码旗舰', 'why': '开源阵营里实用度高，开发者关注度高'},
    {'category': 'coding', 'source': 'huggingface', 'url': 'https://huggingface.co/moonshotai/Kimi-K2.6', 'label': '中文代码协作', 'why': '中文理解、长上下文协作和最近热度都很强'},

    # 多模态
    {'category': 'multimodal', 'source': 'openrouter-latest', 'provider_prefix': 'openai', 'family': 'gpt', 'variant': 'image', 'label': '图文一体', 'why': 'OpenAI 最新图像/多模态模型，适合复杂多模态工作流'},
    {'category': 'multimodal', 'source': 'openrouter', 'id': 'z-ai/glm-5v-turbo', 'label': '视觉国产主力', 'why': '国产视觉多模态里很值得关注'},
    {'category': 'multimodal', 'source': 'huggingface', 'url': 'https://huggingface.co/google/gemma-4-31B-it', 'label': '开源多模态热门', 'why': 'Google 阵营近期开源关注度很高'},
    {'category': 'multimodal', 'source': 'huggingface', 'url': 'https://huggingface.co/tencent/HY-Embodied-0.5', 'label': '具身方向', 'why': '具身智能方向里值得盯的代表模型'},

    # 图像生成
    {'category': 'image', 'source': 'openrouter-latest', 'provider_prefix': 'openai', 'family': 'gpt', 'variant': 'image', 'label': '最新 GPT 图像', 'why': 'OpenAI 最新图像生成模型，文字渲染和综合生成能力都很强'},
    {'category': 'image', 'source': 'huggingface', 'url': 'https://huggingface.co/black-forest-labs/FLUX.1-dev', 'label': '开源生图旗舰', 'why': 'FLUX.1-dev 仍是国内用户最熟、最常用的一线开源生图主力'},
    {'category': 'image', 'source': 'huggingface', 'url': 'https://huggingface.co/black-forest-labs/FLUX.1-Kontext-dev', 'label': '编辑工作流主力', 'why': 'Kontext 系列更贴近当前图像编辑与工作流场景，实用性高'},
    {'category': 'image', 'source': 'manual', 'name': 'Gemini 3 Pro Image', 'provider': 'Google', 'url': 'https://openrouter.ai/google/gemini-3-pro-image-preview', 'freshness': '2026-04-22', 'badge': '谷歌图像新主力', 'why': 'Google 最新图像生成方向主力，国内用户视角不能缺这条线', 'meta': 'OpenRouter 预览模型', 'tags': ['图像生成']},
    {'category': 'image', 'source': 'manual', 'name': 'Gemini 3.1 Flash Image', 'provider': 'Google', 'url': 'https://openrouter.ai/google/gemini-3.1-flash-image-preview', 'freshness': '2026-04-22', 'badge': '轻量图像快模', 'why': '适合轻量快速出图与产品化场景，是当前值得关注的新线', 'meta': 'OpenRouter 预览模型', 'tags': ['图像生成']},

    # 视频生成
    {'category': 'video', 'source': 'manual', 'name': 'Seedance 2.0', 'provider': 'ByteDance Seed', 'url': 'https://seed.bytedance.com/en/seedance2_0', 'freshness': '2026-04-22', 'badge': '最新视频王炸', 'why': '字节最新视频模型，当前就该放进视频主榜', 'meta': '官方发布', 'tags': ['视频生成', '原生音频']},
    {'category': 'video', 'source': 'manual', 'name': 'Kling AI', 'provider': '快手可灵', 'url': 'https://app.klingai.com/global/', 'freshness': '2026-04-22', 'badge': '国内视频主力', 'why': '国内用户实际使用面很大，视频生成主榜必须有可灵', 'meta': '官网可用', 'tags': ['视频生成']},
    {'category': 'video', 'source': 'manual', 'name': 'Runway Gen-4', 'provider': 'Runway', 'url': 'https://runwayml.com/research/introducing-gen-4/', 'freshness': '2026-04-22', 'badge': '国际视频主力', 'why': '国际视频生成标杆之一，行业心智很强', 'meta': '官方发布', 'tags': ['视频生成']},
    {'category': 'video', 'source': 'huggingface', 'url': 'https://huggingface.co/Lightricks/LTX-2.3', 'label': '视频生成新锐', 'why': '视频方向里热度较高，值得盯着看'},

    # 开源旗舰

    # 开源旗舰
    {'category': 'open', 'source': 'huggingface', 'url': 'https://huggingface.co/Qwen/Qwen2.5-72B-Instruct', 'label': '开源通用王者', 'why': '采用广、能力稳、社区影响力大'},
    {'category': 'open', 'source': 'huggingface', 'url': 'https://huggingface.co/deepseek-ai/DeepSeek-V3', 'label': '开源推理主力', 'why': '开源通用模型里非常有代表性'},
    {'category': 'open', 'source': 'huggingface', 'url': 'https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct', 'label': '生态基座', 'why': 'Llama 生态广，真实使用面极大'},
    {'category': 'open', 'source': 'huggingface', 'url': 'https://huggingface.co/openai/whisper-large-v3', 'label': '语音识别标杆', 'why': 'ASR 领域真正长期被广泛采用的主力'},
    {'category': 'open', 'source': 'huggingface', 'url': 'https://huggingface.co/moonshotai/Kimi-K2.6', 'label': '开源新热门', 'why': '近期讨论度与关注度都很高'},

    # 新锐关注
    {'category': 'watch', 'source': 'openrouter', 'id': 'deepseek/deepseek-v4-pro', 'label': 'DeepSeek V4', 'why': '今天最重要的国产模型发布之一，应该进入模型页重点关注位'},
    {'category': 'watch', 'source': 'openrouter', 'id': 'minimax/minimax-m2.7', 'label': '新锐国产', 'why': '近期迭代积极，值得持续跟踪'},
    {'category': 'watch', 'source': 'openrouter', 'id': 'xiaomi/mimo-32b', 'label': '小米 MiMo', 'why': 'OpenRouter 上热度和实力都不该缺席，国产新锐里必须补上'},
    {'category': 'watch', 'source': 'openrouter', 'id': 'mistralai/mistral-small-2603', 'label': '轻量强者', 'why': '轻量级模型里很能打'},
    {'category': 'watch', 'source': 'openrouter', 'id': 'nvidia/nemotron-3-super-120b-a12b', 'label': 'NVIDIA 新动向', 'why': '大厂新模型线，值得长期观察'},
    {'category': 'watch', 'source': 'huggingface', 'url': 'https://huggingface.co/Qwen/Qwen3.6-35B-A3B', 'label': 'Qwen 新代际', 'why': 'Qwen 新代际开源模型，热度上升中'},
    {'category': 'watch', 'source': 'huggingface', 'url': 'https://huggingface.co/Lightricks/LTX-2.3', 'label': '视频生成新锐', 'why': '视频方向里热度较高，值得盯着看'},
]

BANNED_HF_AUTHORS = {
    'alwaysgood', 'apocalypseparty', 'quixiai', 'mats-10-sprint-cs-jb', 'flwrlabs', 'rta-ailabs', 'z-lab'
}

MIN_HF_LIKES = 300

OPENROUTER_ALLOWED_IDS = {item['id'] for item in CURATED_ITEMS if item['source'] == 'openrouter'}
HF_ALLOWED_URLS = {item['url'] for item in CURATED_ITEMS if item['source'] == 'huggingface'}



def fetch_openrouter_models():
    req = urllib.request.Request(OPENROUTER_URL, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return {m['id']: m for m in json.load(resp)['data']}


def load_local_models():
    with open(MODELS_PATH, 'r', encoding='utf-8') as f:
        items = json.load(f)

    filtered = []
    for m in items:
        author = (m.get('author') or '').lower()
        likes = m.get('likes', 0) or 0
        url = m.get('url')
        if url in HF_ALLOWED_URLS:
            filtered.append(m)
            continue
        if author in BANNED_HF_AUTHORS:
            continue
        if likes < MIN_HF_LIKES:
            continue
        filtered.append(m)

    return {m.get('url'): m for m in filtered}


def fmt_date(ts):
    if not ts:
        return ''
    return datetime.fromtimestamp(ts, tz=timezone.utc).strftime('%Y-%m-%d')


def clean_name(name):
    prefixes = ['OpenAI: ', 'Anthropic: ', 'Google: ', 'DeepSeek: ', 'Qwen: ', 'Baidu: ', 'ByteDance Seed: ', 'MoonshotAI: ', 'Z.ai: ', 'MiniMax: ', 'Xiaomi: ', 'Mistral: ', 'Meta: ', 'xAI: ', 'NVIDIA: ', 'Amazon: ']
    out = name or ''
    for p in prefixes:
        if out.startswith(p):
            out = out[len(p):]
            break
    return out.replace('  ', ' ').strip()


def provider_label_from_model(model):
    name = model.get('name') or ''
    if ':' in name:
        return name.split(':', 1)[0].strip()
    model_id = model.get('id') or ''
    prefix = model_id.split('/')[0] if '/' in model_id else model_id
    return prefix.replace('-', ' ').title()



ARCHIVE_VARIANT_KEYWORDS = {
    'pro': ['pro'],
    'image': ['image'],
    'base': [],
}

STALE_VARIANT_KEYWORDS = ['mini', 'nano', 'chat', 'audio', 'codex']


def openrouter_created(model):
    return model.get('created') or 0


def resolve_latest_openrouter_id(openrouter_map, provider_prefix, family='gpt', variant='base'):
    provider_prefix = provider_prefix.lower().rstrip('/')
    family = family.lower()
    variant = variant.lower()
    wanted = ARCHIVE_VARIANT_KEYWORDS.get(variant, [])
    candidates = []
    for model_id, model in openrouter_map.items():
        low_id = model_id.lower()
        low_name = (model.get('name') or '').lower()
        blob = f"{low_id} {low_name}"
        if not low_id.startswith(provider_prefix + '/'):
            continue
        if family not in blob:
            continue
        if variant == 'base' and any(k in blob for k in STALE_VARIANT_KEYWORDS + ['pro', 'image']):
            continue
        if wanted and not any(k in blob for k in wanted):
            continue
        candidates.append((openrouter_created(model), model_id))
    if not candidates:
        return None
    return max(candidates)[1]


def materialize_latest_specs(specs, openrouter_map):
    out = []
    for spec in specs:
        if spec.get('source') != 'openrouter-latest':
            out.append(spec)
            continue
        model_id = resolve_latest_openrouter_id(
            openrouter_map,
            spec['provider_prefix'],
            spec.get('family', ''),
            spec.get('variant', 'base'),
        )
        if not model_id:
            continue
        resolved = dict(spec)
        resolved['source'] = 'openrouter'
        resolved['id'] = model_id
        resolved['auto_resolved'] = True
        out.append(resolved)
    return out


def archive_superseded_openrouter_specs(specs, openrouter_map):
    latest_by_slot = {}
    for spec in specs:
        if spec.get('source') != 'openrouter':
            continue
        mid = spec.get('id', '')
        provider = mid.split('/')[0] if '/' in mid else ''
        name_blob = f"{mid} {(openrouter_map.get(mid) or {}).get('name', '')}".lower()
        if provider == 'openai' and 'gpt' in name_blob:
            if 'image' in name_blob:
                slot = ('openai', 'gpt', 'image')
            elif 'pro' in name_blob:
                slot = ('openai', 'gpt', 'pro')
            elif any(k in name_blob for k in STALE_VARIANT_KEYWORDS):
                continue
            else:
                slot = ('openai', 'gpt', 'base')
            current = latest_by_slot.get(slot)
            if current is None or openrouter_created(openrouter_map.get(mid, {})) > openrouter_created(openrouter_map.get(current, {})):
                latest_by_slot[slot] = mid
    archived = []
    for spec in specs:
        mid = spec.get('id', '')
        if spec.get('source') != 'openrouter' or not mid.startswith('openai/'):
            archived.append(spec)
            continue
        name_blob = f"{mid} {(openrouter_map.get(mid) or {}).get('name', '')}".lower()
        slot = None
        if 'gpt' in name_blob:
            if 'image' in name_blob:
                slot = ('openai', 'gpt', 'image')
            elif 'pro' in name_blob:
                slot = ('openai', 'gpt', 'pro')
            elif any(k in name_blob for k in STALE_VARIANT_KEYWORDS):
                slot = None
            else:
                slot = ('openai', 'gpt', 'base')
        if slot and latest_by_slot.get(slot) and latest_by_slot[slot] != mid:
            continue
        archived.append(spec)
    return archived

def auto_discovery_series_key(model_id, model):
    low = f"{model_id} {(model.get('name') or '')}".lower()
    prefix = model_id.split('/')[0] if '/' in model_id else model_id
    if prefix == 'xiaomi' or 'mimo' in low:
        return ('xiaomi', 'mimo')
    return (prefix, model_id.split('/')[-1].split('-')[0])


def build_auto_discovery_specs(openrouter_map):
    specs = []
    for model_id, model in openrouter_map.items():
        low = f"{model_id} {(model.get('name') or '')}".lower()
        if 'xiaomi/' in model_id or 'mimo' in low:
            specs.append({
                'category': 'watch',
                'source': 'openrouter',
                'id': model_id,
                'label': '自动发现',
                'why': '从 OpenRouter 自动发现的高关注国产模型，应该进入候选榜单',
            })
    specs.sort(key=lambda x: openrouter_map[x['id']].get('created', 0), reverse=True)
    dedup = []
    seen_ids = set()
    seen_series = set()
    for spec in specs:
        if spec['id'] in seen_ids:
            continue
        seen_ids.add(spec['id'])
        series = auto_discovery_series_key(spec['id'], openrouter_map[spec['id']])
        if series in seen_series:
            continue
        seen_series.add(series)
        dedup.append(spec)
    return dedup


def merge_curated_items(base_items, auto_items):
    merged = list(base_items)
    existing_or_ids = {item.get('id') for item in base_items if item.get('source') == 'openrouter'}
    existing_urls = {item.get('url') for item in base_items if item.get('source') == 'huggingface'}
    for item in auto_items:
        if item.get('source') == 'openrouter' and item.get('id') in existing_or_ids:
            continue
        if item.get('source') == 'huggingface' and item.get('url') in existing_urls:
            continue
        merged.append(item)
    return merged


def modalities_from_or(model):
    arch = model.get('architecture') or {}
    merged = set((arch.get('input_modalities') or []) + (arch.get('output_modalities') or []))
    labels = []
    if 'text' in merged:
        labels.append('文本')
    if 'image' in merged:
        labels.append('图像')
    if 'video' in merged:
        labels.append('视频')
    if 'audio' in merged:
        labels.append('音频')
    if len(merged) >= 2:
        labels.insert(0, '多模态')
    # dedupe keep order
    seen = set()
    out = []
    for x in labels:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out[:4]


def format_context_meta(context_length):
    if not context_length:
        return '商用主力模型'
    if context_length >= 1_000_000:
        m = context_length / 1_000_000
        if abs(m - round(m)) < 1e-9:
            return f"{int(round(m))}M 上下文"
        return f"{m:.1f}M 上下文"
    return f"{context_length // 1000}K 上下文"


def build_item(spec, openrouter_map, hf_map):
    if spec['source'] == 'openrouter':
        model = openrouter_map[spec['id']]
        return {
            'category': spec['category'],
            'source': 'OpenRouter',
            'name': clean_name(model.get('name') or spec['id']),
            'provider': (model.get('name') or spec['id']).split(':')[0],
            'url': f"https://openrouter.ai/{spec['id']}",
            'freshness': fmt_date(model.get('created')),
            'badge': spec['label'],
            'why': spec['why'],
            'meta': format_context_meta(model.get('context_length')),
            'tags': modalities_from_or(model),
        }

    if spec['source'] == 'manual':
        return {
            'category': spec['category'],
            'source': '官方补充',
            'name': spec['name'],
            'provider': spec['provider'],
            'url': spec['url'],
            'freshness': spec.get('freshness', ''),
            'badge': spec['badge'],
            'why': spec['why'],
            'meta': spec.get('meta', '官方发布'),
            'tags': spec.get('tags', []),
        }

    hf = hf_map[spec['url']]
    tags = []
    if hf.get('pipeline_tag') == 'text-generation':
        tags.append('文本')
    elif hf.get('pipeline_tag') == 'text-to-image':
        tags.append('图像生成')
    elif hf.get('pipeline_tag') == 'image-text-to-text':
        tags.append('多模态')
    elif hf.get('pipeline_tag') == 'automatic-speech-recognition':
        tags.append('语音识别')
    elif hf.get('pipeline_tag') == 'image-to-video':
        tags.append('视频生成')
    elif hf.get('pipeline_tag') == 'image-to-3d':
        tags.append('3D')

    return {
        'category': spec['category'],
        'source': 'HuggingFace',
        'name': hf.get('display_name') or hf.get('name', '').split('/')[-1],
        'provider': hf.get('author', ''),
        'url': hf.get('url'),
        'freshness': (hf.get('created_at') or '')[:10],
        'badge': spec['label'],
        'why': spec['why'],
        'meta': f"❤️ {hf.get('likes', 0)}" if hf.get('likes') else '开源热门模型',
        'tags': tags,
    }


def generate_curated_models():
    openrouter_map = fetch_openrouter_models()
    hf_map = load_local_models()

    base_specs = materialize_latest_specs(CURATED_ITEMS, openrouter_map)
    curated_specs = merge_curated_items(base_specs, build_auto_discovery_specs(openrouter_map))
    curated_specs = archive_superseded_openrouter_specs(curated_specs, openrouter_map)

    items = []
    for spec in curated_specs:
        try:
            items.append(build_item(spec, openrouter_map, hf_map))
        except KeyError:
            continue

    out = {
        'updated_at': datetime.now().isoformat(),
        'total': len(items),
        'categories': [
            {
                'id': cid,
                'name': name,
                'subtitle': subtitle,
                'count': sum(1 for x in items if x['category'] == cid),
            }
            for cid, name, subtitle in CATEGORY_ORDER
            if any(x['category'] == cid for x in items)
        ],
        'items': items,
    }

    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    return f'生成精选模型榜单 {len(items)} 条'


if __name__ == '__main__':
    print(generate_curated_models())
