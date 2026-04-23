#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

ROOT = Path('/root/ai-hot')
RAW_JSON = ROOT / 'data' / 'news_cover_raw_results.json'
SCRIPT = ROOT / 'scripts' / 'generate_news_cover_images.py'


def main():
    if not RAW_JSON.exists():
        print(json.dumps({'error': 'raw results not found', 'path': str(RAW_JSON)}, ensure_ascii=False))
        raise SystemExit(1)
    data = json.loads(RAW_JSON.read_text(encoding='utf-8'))
    results = data.get('results', [])
    raw_items = [r for r in results if r.get('status') == 'generated_raw']
    print(json.dumps({'count': len(raw_items), 'items': raw_items}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
