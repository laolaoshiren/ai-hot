#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

ROOT = Path('/root/ai-hot')
SCRIPT = ROOT / 'scripts' / 'generate_news_cover_images.py'
RAW_JSON = ROOT / 'data' / 'news_cover_raw_results.json'


def main():
    cmd = ['python3.11', str(SCRIPT), 'raw', '--hours', '6', '--limit', '6', '--concurrency', '2', '--output', str(RAW_JSON)]
    result = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
        raise SystemExit(result.returncode)
    print(f'RAW_RESULTS={RAW_JSON}')


if __name__ == '__main__':
    main()
