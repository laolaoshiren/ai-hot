#!/usr/bin/env python3
"""Scrub secret-like strings out of generated site data.

The aggregator scrapes public feeds, and scraped content sometimes embeds
strings that look like real credentials (e.g. hf_/ghp_/sk- tokens inside
benchmark transcripts). When such text gets baked into the Hugo output,
GitHub Push Protection rejects the gh-pages push and the deploy fails.

Usage:
  python scripts/sanitize_secrets.py           # scrub data/ and site/ in place
  python scripts/sanitize_secrets.py --check   # verify only; exit 1 if dirty
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REDACTION = "[REDACTED]"

SECRET_PATTERNS = {
    # NOTE: no \b guards on purpose -- scraped JSON stores tokens next to
    # escaped "\\n" whose literal letter n defeats word-boundary matching,
    # while GitHub's push protection still flags the bare substring.
    "huggingface_token": r"hf_[A-Za-z0-9]{20,}",
    "github_token": r"gh[pousr]_[A-Za-z0-9]{20,}",
    "github_pat": r"github_pat_[A-Za-z0-9_]{20,}",
    "aws_access_key": r"AKIA[0-9A-Z]{16}",
    "openai_key": r"sk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{20,}",
    "google_api_key": r"AIza[0-9A-Za-z_-]{30,}",
    "slack_token": r"xox[baprs]-[A-Za-z0-9-]{10,}",
    "gitlab_token": r"glpat-[A-Za-z0-9_-]{15,}",
}

COMPILED = {name: re.compile(pat) for name, pat in SECRET_PATTERNS.items()}


def iter_target_files(root=None):
    """All candidate text files under <root>/data and <root>/site."""
    root = Path(root) if root else ROOT
    seen = set()
    for base in ("data", "site"):
        for path in (root / base).rglob("*"):
            if path.is_file() and path not in seen:
                seen.add(path)
                yield path


def sanitize_text(text):
    """Return (clean_text, {pattern_name: replacement_count})."""
    counts = {}
    for name, rx in COMPILED.items():
        text, n = rx.subn(REDACTION, text)
        if n:
            counts[name] = counts.get(name, 0) + n
    return text, counts


def sanitize_files(fix=True, root=None):
    """Scan targets; optionally rewrite. Returns (changed_paths, totals)."""
    changed = []
    totals = {}
    for path in iter_target_files(root=root):
        try:
            raw = path.read_bytes()
            text = raw.decode("utf-8")
        except (UnicodeDecodeError, OSError):
            continue  # binary or unreadable -> skip
        clean, counts = sanitize_text(text)
        if not counts:
            continue
        if fix:
            # Bytes round-trip preserves original line endings exactly.
            path.write_bytes(clean.encode("utf-8"))
        changed.append(path)
        for name, n in counts.items():
            totals[name] = totals.get(name, 0) + n
    return changed, totals


def main():
    parser = argparse.ArgumentParser(
        description="Scrub/verify secret-like strings in generated data"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify only: exit 1 if any secret-like string is present",
    )
    args = parser.parse_args()

    changed, totals = sanitize_files(fix=not args.check)

    def rel(p):
        return p.relative_to(ROOT).as_posix()

    if not changed:
        print("OK: no secret-like strings found")
        return 0

    if args.check:
        print("FAIL: secret-like strings detected:")
        for p in changed:
            print("  -", rel(p))
        for name, n in sorted(totals.items()):
            print(f"  [{name}] x{n}")
        return 1

    print("Sanitized files:")
    for p in changed:
        print("  -", rel(p))
    for name, n in sorted(totals.items()):
        print(f"  [{name}] x{n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
