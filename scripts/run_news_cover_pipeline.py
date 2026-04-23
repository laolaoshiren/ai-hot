#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

ROOT = Path('/root/ai-hot')
SCRIPT = ROOT / 'scripts' / 'generate_news_cover_images.py'
RAW_JSON = ROOT / 'data' / 'news_cover_raw_results.json'


def main():
    print(json.dumps({
        'status': 'disabled',
        'reason': 'image generation API temporarily limited; news cover generation paused'
    }, ensure_ascii=False))


if __name__ == '__main__':
    main()
