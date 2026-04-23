#!/usr/bin/env python3
import argparse
import hashlib
import json
import os
import random
import re
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path('/root/ai-hot')
DATA_NEWS = ROOT / 'data' / 'news.json'
CONTENT_DIR = ROOT / 'site' / 'content' / 'news'
STATIC_IMG_DIR = ROOT / 'site' / 'static' / 'news-images'
CHATGPT_SCRIPT = ROOT / 'scripts' / 'chatgpt_gen.js'
CHATGPT_COOKIES = Path('/tmp/chatgpt_cookies.json')
RECENT_HOURS = 6
MAX_CONCURRENCY = 3
FRONT_PAGE_LIMIT = 8
MUST_READ_SOURCES = {
    '机器之心', '量子位', '新智元', 'TechCrunch AI', 'The Verge AI', 'MIT Tech Review', 'VentureBeat AI', 'InfoQ AI'
}
NOISE_KEYWORDS = {
    '大会', '开幕', '峰会', '论坛', '研讨会', '直播', '视频', '课程', '招聘', '发布会', '白皮书下载', '点击查看原文>', 'newsletter', 'the download'
}
MIN_CONTENT_CHARS = 900
MIN_SUMMARY_CHARS = 24


def clean_text(text: str) -> str:
    text = re.sub(r'\s+', ' ', str(text or '').strip())
    return text


def is_cover_worthy(item):
    title = clean_text(item.get('title_zh') or item.get('title') or '')
    summary = clean_text(item.get('ai_summary') or item.get('summary_zh') or item.get('summary') or '')
    content = clean_text(item.get('content_text') or item.get('content_excerpt') or '')
    source = item.get('source', '')
    low = (title + ' ' + summary + ' ' + content[:300]).lower()

    if source not in MUST_READ_SOURCES:
        return False
    if any(x.lower() in low for x in NOISE_KEYWORDS):
        return False
    if len(content) < MIN_CONTENT_CHARS:
        return False
    if len(summary) < MIN_SUMMARY_CHARS:
        return False
    return True


def parse_published(value):
    value = clean_text(value)
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace('Z', '+00:00')).replace(tzinfo=None)
    except Exception:
        return None


def select_recent_cover_candidates(news, now=None, hours=RECENT_HOURS):
    now = now or datetime.utcnow()
    cutoff = now - timedelta(hours=hours)
    picked = []
    for item in news:
        published = parse_published(item.get('published'))
        if not published or published < cutoff:
            continue
        if is_cover_worthy(item):
            picked.append(item)
    return picked


def select_front_page_news_ids(news):
    ids = []
    for item in news:
        if is_cover_worthy(item):
            ids.append(item.get('id'))
        if len(ids) >= FRONT_PAGE_LIMIT:
            break
    return [x for x in ids if x]


def choose_insert_position(body: str, seed: str):
    rng = random.Random(seed)
    parts = [p for p in re.split(r'\n\n+', body or '') if p.strip()]
    if len(parts) <= 2:
        return 'tail'
    return rng.choice(['head', 'mid', 'tail'])


def insert_image_into_body(body: str, image_rel: str, alt_text: str, seed: str):
    marker = f'![{alt_text}]({image_rel})'
    parts = [p for p in re.split(r'\n\n+', body or '') if p.strip()]
    if not parts:
        return marker
    pos = choose_insert_position(body, seed)
    if pos == 'head':
        parts.insert(1 if len(parts) > 1 else 0, marker)
    elif pos == 'mid':
        parts.insert(max(1, len(parts) // 2), marker)
    else:
        parts.append(marker)
    return '\n\n'.join(parts)


def is_image_acceptable(analysis_text: str, article_hint: str):
    text = clean_text(analysis_text).lower()
    if not text:
        return False
    reject_keywords = [
        '不可用', '机器人头像', '机械人脸', '未来城市', '泛ai海报', '宣传海报',
        '跑题', '主题不对焦', '文字错误', '错别字', '乱码', '大标题写着通用人工智能加速到来'
    ]
    if any(x in text for x in reject_keywords):
        return False
    if '勉强可用' in text:
        return False
    return '可用' in text or ('实验室' in text and '质谱' in text) or ('芯片' in text and '主题明确' in text)


def build_image_prompt(article):
    title = clean_text(article.get('title_zh') or article.get('title') or '')
    intro = clean_text(article.get('ai_summary') or article.get('summary_zh') or article.get('summary') or '')
    content = clean_text(article.get('content_text') or article.get('content_excerpt') or '')[:900]
    return f'''为 AI 新闻文章生成一张网站头图，16:9 横版，中文科技媒体封面风格，精致、克制、专业。

文章标题：{title}
文章摘要：{intro}
文章关键信息：{content}

必须遵守：
1. 这是一张“文章头图”，不是宣传海报，不是品牌广告，不是招商图。
2. 不要机器人头像、机械人脸、数字地球、蓝色光束城市、悬浮大芯片、通用 AI 海报模板。
3. 不要大段文字，不要口号，不要“AI赋能千行百业”“未来已来”“通用人工智能加速到来”这类空话。
4. 只允许极少量中文文字，最好 0 到 8 个字；如果加字，只能是围绕文章主题的简短中文标签，必须自然、清晰、无错别字。
5. 画面必须围绕文章真实主题选元素：
   - 药物发现 / 分子 / 质谱 / 生物医药：实验室、分子结构、质谱峰图、分析界面、样本瓶
   - AI 芯片 / 算力：芯片实物感、主板、电路、数据面板，但不要夸张海报
   - 模型 / Agent / 编程：代码界面、工作流、开发者桌面、推理结构图
   - 企业产品 / 融资 / 平台：产品界面、团队协作、业务场景，避免空洞概念图
6. 风格参考：严肃科技媒体专题配图、商业杂志头图、现代编辑插画。不要廉价宣传海报感。
7. 构图干净，信息密度中等，适合放在新闻正文顶部。
8. 中文必须正确、清晰、可读；如果做不到，就不要放文字。
9. 重点是“主题准确”，宁可少字，也不要跑题。'''


def patch_frontmatter_cover_image(path: Path, rel_image: str):
    text = path.read_text(encoding='utf-8')
    if 'cover_image = ' in text:
        text = re.sub(r'^cover_image = ".*?"$', f'cover_image = "{rel_image}"', text, flags=re.M)
    else:
        text = text.replace('type = "news"\n', f'type = "news"\ncover_image = "{rel_image}"\n', 1)
    path.write_text(text, encoding='utf-8')


def patch_markdown_inline_image(path: Path, rel_image: str, title: str, seed: str):
    text = path.read_text(encoding='utf-8')
    marker = '<!-- AUTO-GENERATED: news page -->\n'
    if rel_image in text:
        return
    parts = text.split(marker, 1)
    if len(parts) != 2:
        return
    head, rest = parts
    source_marker = '\n## 🔗 原始来源'
    if source_marker in rest:
        body, tail = rest.split(source_marker, 1)
        body = body.strip()
        updated_body = insert_image_into_body(body, rel_image, f'{title} 配图', seed)
        new_text = head + marker + '\n' + updated_body.strip() + '\n\n## 🔗 原始来源' + tail
    else:
        updated_body = insert_image_into_body(rest.strip(), rel_image, f'{title} 配图', seed)
        new_text = head + marker + '\n' + updated_body.strip() + '\n'
    path.write_text(new_text, encoding='utf-8')


def build_output_paths(item_id: str):
    digest = hashlib.md5(item_id.encode('utf-8')).hexdigest()[:8]
    return (
        Path(f'/tmp/chatgpt_image_{item_id}_{digest}.png'),
        Path(f'/tmp/chatgpt_debug_{item_id}_{digest}.png'),
        Path(f'/tmp/news_cover_prompt_{item_id}_{digest}.txt'),
    )


def generate_one_image(item):
    item_id = item.get('id')
    output_path, debug_path, prompt_path = build_output_paths(item_id)
    prompt = build_image_prompt(item)
    prompt_path.write_text(prompt, encoding='utf-8')
    if output_path.exists():
        output_path.unlink()
    env = os.environ.copy()
    env['CHATGPT_OUT'] = str(output_path)
    env['CHATGPT_DEBUG_OUT'] = str(debug_path)
    cmd = f'node {CHATGPT_SCRIPT} "$(cat {prompt_path})"'
    result = subprocess.run(cmd, shell=True, cwd='/tmp', capture_output=True, text=True, timeout=240, env=env)
    return result, output_path, debug_path, prompt_path


def process_article_without_qa(item):
    item_id = item.get('id')
    md_path = CONTENT_DIR / f'{item_id}.md'
    if not md_path.exists():
        return {'id': item_id, 'status': 'skipped', 'reason': 'markdown_missing'}
    md_text = md_path.read_text(encoding='utf-8')
    if f'/news-images/{item_id}.png' in md_text:
        return {'id': item_id, 'status': 'skipped', 'reason': 'already_inserted'}

    last_error = ''
    for attempt in range(2):
        result, output_path, _debug_path, _prompt_path = generate_one_image(item)
        if result.returncode != 0 or not output_path.exists():
            last_error = f'returncode={result.returncode}'
            continue
        return {
            'id': item_id,
            'status': 'generated_raw',
            'raw_image_path': str(output_path),
            'attempt': attempt + 1,
            'title': clean_text(item.get('title_zh') or item.get('title') or 'AI新闻'),
        }
    return {'id': item_id, 'status': 'failed', 'reason': last_error or 'image_not_generated'}


def apply_article_image(item_id: str, raw_image_path: str, title: str):
    md_path = CONTENT_DIR / f'{item_id}.md'
    target = STATIC_IMG_DIR / f'{item_id}.png'
    shutil.copy2(raw_image_path, target)
    rel_image = f'/news-images/{item_id}.png'
    patch_frontmatter_cover_image(md_path, rel_image)
    patch_markdown_inline_image(md_path, rel_image, title, seed=item_id)
    return str(target)


def load_news_map():
    news = json.loads(DATA_NEWS.read_text(encoding='utf-8'))
    return {item.get('id'): item for item in news if item.get('id')}


def retry_one_image(item_id: str):
    item = load_news_map().get(item_id)
    if not item:
        raise SystemExit(f'news id not found: {item_id}')
    result = process_article_without_qa(item)
    print(json.dumps(result, ensure_ascii=False))
    return result


def generate_news_cover_images(limit: int = FRONT_PAGE_LIMIT, hours: int = RECENT_HOURS, concurrency: int = 1):
    if not DATA_NEWS.exists():
        return 'news.json 不存在'
    if not CHATGPT_SCRIPT.exists() or not CHATGPT_COOKIES.exists():
        return '缺少 ChatGPT 生图依赖'

    news = json.loads(DATA_NEWS.read_text(encoding='utf-8'))
    candidates = select_recent_cover_candidates(news, hours=hours)[:limit]
    STATIC_IMG_DIR.mkdir(parents=True, exist_ok=True)

    concurrency = max(1, min(int(concurrency or 1), MAX_CONCURRENCY))
    results = []
    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = [executor.submit(process_article_without_qa, item) for item in candidates]
        for future in as_completed(futures):
            results.append(future.result())

    generated = sum(1 for r in results if r.get('status') == 'generated_raw')
    skipped = sum(1 for r in results if r.get('status') != 'generated_raw')
    return {'candidates': candidates, 'results': results, 'summary': f'最近{hours}小时候选 {len(candidates)} 篇，raw 生成 {generated} 篇，跳过 {skipped} 篇'}


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest='command', required=False)

    raw = sub.add_parser('raw')
    raw.add_argument('--hours', type=int, default=RECENT_HOURS)
    raw.add_argument('--limit', type=int, default=FRONT_PAGE_LIMIT)
    raw.add_argument('--concurrency', type=int, default=1)
    raw.add_argument('--output', type=str, default='')

    apply = sub.add_parser('apply')
    apply.add_argument('--id', required=True)
    apply.add_argument('--raw-image', required=True)
    apply.add_argument('--title', required=True)

    retry = sub.add_parser('retry')
    retry.add_argument('--id', required=True)

    args = parser.parse_args()
    command = args.command or 'raw'

    if command == 'raw':
        result = generate_news_cover_images(limit=args.limit, hours=args.hours, concurrency=args.concurrency)
        if args.output:
            Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if command == 'apply':
        applied = apply_article_image(args.id, args.raw_image, args.title)
        print(json.dumps({'id': args.id, 'applied_image': applied}, ensure_ascii=False))
        return

    if command == 'retry':
        retry_one_image(args.id)
        return


if __name__ == '__main__':
    main()
