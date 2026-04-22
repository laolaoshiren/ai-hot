#!/usr/bin/env python3
"""生成首页热度飙升数据。"""

from __future__ import annotations

import json
import math
import os
import re
from datetime import datetime, timedelta
from typing import Any, Dict, Iterable, List, Optional

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
RISING_PATH = os.path.join(DATA_DIR, "rising.json")
PROJECTS_PATH = os.path.join(DATA_DIR, "projects.json")
TOOLS_PATH = os.path.join(DATA_DIR, "tools.json")
AGENTS_PATH = os.path.join(DATA_DIR, "agents.json")
MODELS_PATH = os.path.join(DATA_DIR, "models.json")
DEFAULT_WINDOWS = (7, 14, 30)
NOISY_MODEL_TERMS = (
    "gguf",
    "uncensored",
    "distill",
    "distilled",
    "merged",
    "merge",
    "quant",
    "awq",
    "gptq",
    "4bit",
    "8bit",
    "fp8",
    "nf4",
)
MAINSTREAM_MODEL_AUTHORS = {
    "openai",
    "anthropic",
    "google",
    "meta-llama",
    "mistralai",
    "qwen",
    "deepseek-ai",
    "deepseek",
    "black-forest-labs",
    "stabilityai",
    "runwayml",
    "bytedance-seed",
    "zai-org",
    "z-ai",
    "minimax",
    "baai",
    "microsoft",
}
MAINSTREAM_MODEL_KEYWORDS = (
    "gpt",
    "claude",
    "gemini",
    "deepseek",
    "flux",
    "sdxl",
    "stable-diffusion",
    "runway",
    "seedance",
    "kling",
    "glm",
    "mistral",
    "llama",
)
MIN_GITHUB_STARS = 200
MIN_MODEL_LIKES = 50
MIN_MODEL_DOWNLOADS = 5000
BLOCKED_MODEL_NAME_TERMS = (
    "aggressive",
    "flash",
    "dflash",
    "tq",
    "a3b",
    "uncensored",
    "nsfw",
)


def parse_dt(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    text = str(value).strip()
    if not text:
        return None
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        return datetime.fromisoformat(text)
    except ValueError:
        for fmt in ("%Y-%m-%d", "%Y-%m-%d %H:%M:%S"):
            try:
                return datetime.strptime(text, fmt)
            except ValueError:
                continue
    return None


def load_json(path: str) -> Any:
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def age_days(created_at: Optional[str], now_dt: datetime) -> Optional[float]:
    dt = parse_dt(created_at)
    if not dt:
        return None
    if dt.tzinfo is not None and now_dt.tzinfo is None:
        now_ref = now_dt.replace(tzinfo=dt.tzinfo)
    elif dt.tzinfo is None and now_dt.tzinfo is not None:
        dt = dt.replace(tzinfo=now_dt.tzinfo)
        now_ref = now_dt
    else:
        now_ref = now_dt
    delta = now_ref - dt
    return max(delta.total_seconds() / 86400, 0.0)


def choose_window_days(candidates: List[Dict[str, Any]], preferred_days: int = 7, minimum_count: int = 5) -> int:
    windows = sorted({int(item.get("window_days", 0)) for item in candidates if item.get("window_days")})
    if not windows:
        return preferred_days

    eligible = [window for window in windows if window >= preferred_days]
    if preferred_days in windows:
        count = sum(1 for item in candidates if int(item.get("window_days", 0)) <= preferred_days)
        if count >= minimum_count:
            return preferred_days

    for window in eligible:
        count = sum(1 for item in candidates if int(item.get("window_days", 0)) <= window)
        if count >= minimum_count:
            return window

    return eligible[-1] if eligible else windows[-1]


def score_github_candidate(item: Dict[str, Any]) -> float:
    stars = max(float(item.get("stars") or 0), 0.0)
    window_days = max(float(item.get("window_days") or 1), 1.0)
    age = age_days(item.get("created_at") or item.get("added_at"), datetime.now())
    age_factor = 1.0
    if age is not None:
        age_factor = max(0.35, min(1.5, window_days / max(age, 1.0)))
    return (math.sqrt(stars + 1) * 12 + (stars / window_days)) * age_factor


def score_model_candidate(item: Dict[str, Any]) -> float:
    likes = max(float(item.get("likes") or 0), 0.0)
    downloads = max(float(item.get("downloads") or 0), 0.0)
    window_days = max(float(item.get("window_days") or 1), 1.0)
    age = age_days(item.get("created_at") or item.get("freshness"), datetime.now())
    age_factor = 1.0
    if age is not None:
        age_factor = max(0.4, min(1.6, window_days / max(age, 1.0)))
    openrouter_bonus = 120.0 if item.get("openrouter_available") else 0.0
    return (likes * 1.5 + math.sqrt(downloads + 1) * 2.5 + openrouter_bonus) * age_factor


def clean_intro(text: str, limit: int = 42) -> str:
    text = re.sub(r"\s+", " ", (text or "").strip())
    text = re.sub(r"^[^\w\u4e00-\u9fff]+", "", text)
    if not text:
        return "最近值得关注的一条新线"
    if len(text) > limit:
        text = text[: limit - 1].rstrip() + "…"
    return text


def localize_intro(name: str, description: str, kind: str, openrouter_available: bool = False) -> str:
    text = clean_intro(description)
    lower = text.lower()

    if any(ch >= '\u4e00' and ch <= '\u9fff' for ch in text):
        return text

    if kind == 'project':
        if 'memory system' in lower:
            return '开源 AI 记忆系统，主打长期记忆与效果验证'
        if 'job search system' in lower:
            return '基于 Claude Code 的求职自动化工作流系统'
        if 'curated list' in lower and 'open-source ai' in lower:
            return '精选开源 AI 项目、模型与工具导航合集'
        if 'agent' in lower:
            return '最近讨论度很高的开源 AI 项目'
        return '最近值得点开的开源 AI 项目'

    if kind == 'agent':
        if 'research' in lower:
            return '面向研究与信息整理的 Agent 代表项目'
        if 'coding' in lower or 'software' in lower:
            return '面向开发任务的 Agent 代表项目'
        return '最近值得关注的 Agent 项目'

    if kind == 'model':
        if openrouter_available:
            return '已进入 OpenRouter 的新模型线，值得直接上手'
        if name.lower().startswith('glm'):
            return '智谱新一代通用模型线，近期关注度明显抬头'
        if 'flux' in name.lower():
            return '近期讨论度很高的图像模型新线'
        return '最近值得关注的新模型线'

    if kind == 'tool':
        if 'code editor' in lower:
            return '面向开发者的 AI 编码工具代表'
        return '最近被频繁提到的工具代表'

    return text if text != '最近值得关注的一条新线' else '最近值得关注的一条新线'


def build_reason(item: Dict[str, Any]) -> str:
    name = item.get("name") or ""
    return localize_intro(
        name=name,
        description=item.get("description") or "",
        kind=item.get("type") or "",
        openrouter_available=bool(item.get("openrouter_available")),
    )


def normalize_project(item: Dict[str, Any], now_dt: datetime, preferred_days: int) -> Optional[Dict[str, Any]]:
    created = item.get("created_at")
    age = age_days(created, now_dt)
    if age is None:
        return None
    window = next((days for days in DEFAULT_WINDOWS if age <= days), None)
    if window is None:
        return None
    if int(item.get("stars") or 0) < MIN_GITHUB_STARS:
        return None
    return {
        "id": item.get("id"),
        "name": item.get("display_name") or item.get("name"),
        "url": item.get("url"),
        "description": item.get("description") or "",
        "type": "project",
        "stars": item.get("stars") or 0,
        "created_at": created,
        "window_days": window,
        "score": 0,
    }


def normalize_tool(item: Dict[str, Any], now_dt: datetime, preferred_days: int) -> Optional[Dict[str, Any]]:
    created = item.get("added_at") or item.get("created_at") or item.get("collected_at")
    age = age_days(created, now_dt)
    if age is None:
        return None
    window = next((days for days in DEFAULT_WINDOWS if age <= days), None)
    if window is None:
        return None
    stars = int(item.get("stars") or 0)
    if not (item.get("github_url") or "github.com" in str(item.get("url", "")) or stars):
        return None
    if stars < MIN_GITHUB_STARS:
        return None
    return {
        "id": item.get("id"),
        "name": item.get("name"),
        "url": item.get("github_url") or item.get("url"),
        "description": item.get("description") or "",
        "type": "tool",
        "stars": item.get("stars") or 0,
        "created_at": created,
        "window_days": window,
        "score": 0,
    }


def normalize_agent(item: Dict[str, Any], now_dt: datetime, preferred_days: int) -> Optional[Dict[str, Any]]:
    created = item.get("created_at") or item.get("collected_at")
    age = age_days(created, now_dt)
    if age is None:
        return None
    window = next((days for days in DEFAULT_WINDOWS if age <= days), None)
    if window is None:
        return None
    stars = int(item.get("stars") or 0)
    if not ("github.com" in str(item.get("url", "")) or stars):
        return None
    if stars < MIN_GITHUB_STARS:
        return None
    return {
        "id": item.get("id"),
        "name": item.get("name"),
        "url": item.get("url"),
        "description": item.get("description") or "",
        "type": "agent",
        "stars": item.get("stars") or 0,
        "created_at": created,
        "window_days": window,
        "score": 0,
    }


def normalize_model(item: Dict[str, Any], now_dt: datetime, preferred_days: int) -> Optional[Dict[str, Any]]:
    created = item.get("created_at") or item.get("freshness")
    age = age_days(created, now_dt)
    if age is None:
        return None
    window = next((days for days in DEFAULT_WINDOWS if age <= days), None)
    if window is None:
        return None
    url = item.get("url") or ""
    name = item.get("display_name") or item.get("name") or ""
    source = (item.get("source") or "").lower()
    author = (item.get("author") or item.get("provider") or "").lower()
    haystack = f"{name} {author} {url}".lower()
    if any(term in haystack for term in NOISY_MODEL_TERMS):
        return None
    if any(term in name.lower() for term in BLOCKED_MODEL_NAME_TERMS):
        return None
    likes = int(item.get("likes") or 0)
    downloads = int(item.get("downloads") or 0)
    if likes < MIN_MODEL_LIKES or downloads < MIN_MODEL_DOWNLOADS:
        return None
    if source.startswith("hf-"):
        if author not in MAINSTREAM_MODEL_AUTHORS:
            return None
        if not any(keyword in haystack for keyword in MAINSTREAM_MODEL_KEYWORDS):
            return None
    return {
        "id": item.get("id"),
        "name": name,
        "url": url,
        "description": item.get("author") or item.get("provider") or item.get("source") or "",
        "type": "model",
        "likes": item.get("likes") or 0,
        "downloads": item.get("downloads") or 0,
        "created_at": created,
        "window_days": window,
        "openrouter_available": "openrouter.ai" in url or item.get("source") == "openrouter",
        "score": 0,
    }


def dedupe_items(items: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    seen = set()
    result = []
    for item in items:
        key = (item.get("type"), item.get("url") or item.get("name"))
        if key in seen:
            continue
        seen.add(key)
        result.append(item)
    return result


def build_rising_candidates(
    projects: List[Dict[str, Any]],
    tools: List[Dict[str, Any]],
    agents: List[Dict[str, Any]],
    models: List[Dict[str, Any]],
    preferred_days: int = 7,
    candidate_limit: int = 10,
    display_limit: int = 5,
    now_iso: Optional[str] = None,
) -> Dict[str, Any]:
    now_dt = parse_dt(now_iso) if now_iso else datetime.now().astimezone()
    if now_dt is None:
        now_dt = datetime.now().astimezone()

    candidates: List[Dict[str, Any]] = []
    for row in projects:
        item = normalize_project(row, now_dt, preferred_days)
        if item:
            item["score"] = score_github_candidate(item)
            candidates.append(item)
    for row in tools:
        item = normalize_tool(row, now_dt, preferred_days)
        if item:
            item["score"] = score_github_candidate(item)
            candidates.append(item)
    for row in agents:
        item = normalize_agent(row, now_dt, preferred_days)
        if item:
            item["score"] = score_github_candidate(item)
            candidates.append(item)
    for row in models:
        item = normalize_model(row, now_dt, preferred_days)
        if item:
            item["score"] = score_model_candidate(item)
            candidates.append(item)

    candidates = dedupe_items(sorted(candidates, key=lambda x: x.get("score", 0), reverse=True))
    active_window = choose_window_days(candidates, preferred_days=preferred_days, minimum_count=display_limit)
    filtered = [item for item in candidates if int(item.get("window_days") or 0) <= active_window]
    filtered = sorted(filtered, key=lambda x: x.get("score", 0), reverse=True)[:candidate_limit]

    def with_reason(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        result = []
        for item in items:
            enriched = dict(item)
            enriched["reason"] = build_reason(enriched)
            result.append(enriched)
        return result

    def pick_fallback(kind: str) -> Optional[Dict[str, Any]]:
        if kind == "agent":
            pool = []
            for row in agents:
                stars = int(row.get("stars") or 0)
                if stars < MIN_GITHUB_STARS:
                    continue
                url = str(row.get("url") or "")
                if "github.com" not in url:
                    continue
                pool.append({
                    "id": row.get("id"),
                    "name": row.get("name"),
                    "url": url,
                    "description": row.get("description") or "",
                    "type": "agent",
                    "stars": stars,
                    "score": stars,
                    "window_days": active_window,
                })
            pool.sort(key=lambda x: x.get("score", 0), reverse=True)
            return pool[0] if pool else None
        if kind == "model":
            pool = []
            for row in models:
                item = normalize_model(row, now_dt, preferred_days)
                if not item:
                    continue
                item["score"] = score_model_candidate(item)
                pool.append(item)
            pool.sort(key=lambda x: x.get("score", 0), reverse=True)
            return pool[0] if pool else None
        if kind == "project":
            pool = []
            for row in projects:
                stars = int(row.get("stars") or 0)
                if stars < MIN_GITHUB_STARS:
                    continue
                pool.append({
                    "id": row.get("id"),
                    "name": row.get("display_name") or row.get("name"),
                    "url": row.get("url"),
                    "description": row.get("description") or "",
                    "type": "project",
                    "stars": stars,
                    "score": stars,
                    "window_days": active_window,
                })
            pool.sort(key=lambda x: x.get("score", 0), reverse=True)
            return pool[0] if pool else None
        return None

    final_items = []
    used_keys = set()
    required_types = ["project", "model", "agent"]
    for required_type in required_types:
        preferred = next((item for item in filtered if item.get("type") == required_type), None)
        if not preferred:
            preferred = pick_fallback(required_type)
        if preferred:
            key = (preferred.get("type"), preferred.get("url") or preferred.get("name"))
            if key not in used_keys:
                used_keys.add(key)
                final_items.append(preferred)

    type_counts = {}
    for item in final_items:
        item_type = item.get("type")
        type_counts[item_type] = type_counts.get(item_type, 0) + 1

    for item in filtered:
        key = (item.get("type"), item.get("url") or item.get("name"))
        if key in used_keys:
            continue
        item_type = item.get("type")
        if type_counts.get(item_type, 0) >= 2:
            continue
        used_keys.add(key)
        type_counts[item_type] = type_counts.get(item_type, 0) + 1
        final_items.append(item)
        if len(final_items) >= display_limit:
            break

    if len(final_items) < display_limit:
        for item in filtered:
            key = (item.get("type"), item.get("url") or item.get("name"))
            if key in used_keys:
                continue
            used_keys.add(key)
            final_items.append(item)
            if len(final_items) >= display_limit:
                break

    final_items = with_reason(final_items[:display_limit])

    return {
        "updated_at": now_dt.isoformat(),
        "window_days": active_window,
        "candidate_count": len(filtered),
        "items": final_items[:display_limit],
    }


def generate_rising(preferred_days: int = 7, candidate_limit: int = 10, display_limit: int = 5) -> str:
    projects = load_json(PROJECTS_PATH)
    tools = load_json(TOOLS_PATH)
    agents = load_json(AGENTS_PATH)
    models = load_json(MODELS_PATH)
    rising = build_rising_candidates(
        projects=projects,
        tools=tools,
        agents=agents,
        models=models,
        preferred_days=preferred_days,
        candidate_limit=candidate_limit,
        display_limit=display_limit,
    )
    with open(RISING_PATH, "w", encoding="utf-8") as f:
        json.dump(rising, f, ensure_ascii=False, indent=2)
    return f"生成热度飙升 {len(rising['items'])} 条（窗口 {rising['window_days']} 天）"


if __name__ == "__main__":
    print(generate_rising())
