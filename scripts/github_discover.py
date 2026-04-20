#!/usr/bin/env python3
"""GitHub AI 项目发现"""

import os
import json
from datetime import datetime, timedelta

try:
    import requests
except ImportError:
    os.system("pip install requests -q")
    import requests

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
TOKEN = os.environ.get("GITHUB_TOKEN", "")

SEARCH_QUERIES = [
    "topic:artificial-intelligence created:>{}",
    "topic:machine-learning stars:>100 pushed:>{}",
    "topic:llm stars:>50",
    "topic:ai-agent stars:>50",
    "topic:large-language-models stars:>50",
]


def search_repos(query, per_page=30):
    headers = {"Accept": "application/vnd.github.v3+json"}
    if TOKEN:
        headers["Authorization"] = f"token {TOKEN}"
    url = "https://api.github.com/search/repositories"
    params = {"q": query, "sort": "stars", "order": "desc", "per_page": per_page}
    try:
        resp = requests.get(url, headers=headers, params=params, timeout=20)
        if resp.status_code == 200:
            return resp.json().get("items", [])
        else:
            print(f"  ⚠️ GitHub API {resp.status_code}")
            return []
    except Exception as e:
        print(f"  ⚠️ GitHub搜索失败: {e}")
        return []


def discover_github_projects():
    existing = []
    projects_path = os.path.join(DATA_DIR, "projects.json")
    if os.path.exists(projects_path):
        with open(projects_path) as f:
            existing = json.load(f)

    existing_ids = {p["id"] for p in existing}
    thirty_days_ago = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    new_projects = []

    for query_tpl in SEARCH_QUERIES:
        query = query_tpl.format(thirty_days_ago)
        repos = search_repos(query)
        for repo in repos:
            repo_id = f"github-{repo['id']}"
            if repo_id in existing_ids:
                continue

            topics = repo.get("topics", [])
            # 只收 AI 相关
            ai_topics = {"ai", "artificial-intelligence", "machine-learning", "llm",
                         "deep-learning", "nlp", "computer-vision", "generative-ai",
                         "ai-agent", "chatgpt", "gpt", "transformer"}
            if not (set(topics) & ai_topics) and "ai" not in repo.get("description", "").lower():
                continue

            new_projects.append({
                "id": repo_id,
                "name": repo["full_name"],
                "display_name": repo["name"],
                "url": repo["html_url"],
                "description": repo.get("description", ""),
                "stars": repo.get("stargazers_count", 0),
                "forks": repo.get("forks_count", 0),
                "language": repo.get("language", ""),
                "topics": topics,
                "created_at": repo.get("created_at", ""),
                "updated_at": repo.get("updated_at", ""),
                "license": (repo.get("license") or {}).get("spdx_id", ""),
                "source": "github-search",
                "collected_at": datetime.now().isoformat(),
            })
            existing_ids.add(repo_id)

    combined = existing + new_projects
    combined.sort(key=lambda x: x.get("stars", 0), reverse=True)
    combined = combined[:2000]

    with open(projects_path, "w", encoding="utf-8") as f:
        json.dump(combined, f, ensure_ascii=False, indent=2)

    return f"{len(new_projects)} 个新项目 (总计 {len(combined)})"
