#!/usr/bin/env python3
"""
AI Agent 自动发现器
从 GitHub 搜索热门 AI Agent 项目，自动更新 agents.json
"""

import os
import json
import subprocess
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
AGENTS_FILE = os.path.join(DATA_DIR, "agents.json")

SEARCH_QUERIES = [
    "autonomous AI agent",
    "AI coding agent",
    "multi-agent framework",
    "AI assistant agent",
    "openclaw",
    "browser use agent",
    "research agent LLM",
]

TYPE_KEYWORDS = {
    "编程": ["coding", "code", "program", "swe", "dev", "copilot", "aider", "opencode"],
    "研究": ["research", "search", "analysis", "report", "storm"],
    "自动化": ["automation", "autonomous", "auto", "orchestrat"],
    "助手": ["assistant", "chat", "personal", "openclaw", "hermes"],
    "浏览器": ["browser", "web", "scrape", "navigate", "computer use"],
    "多Agent": ["multi-agent", "crew", "swarm", "team", "autogen", "langgraph"],
    "平台": ["platform", "dify", "coze", "n8n", "build"],
}

def classify_agent(name, description):
    text = f"{name} {description}".lower()
    for agent_type, keywords in TYPE_KEYWORDS.items():
        if any(kw in text for kw in keywords):
            return f"{agent_type} Agent"
    return "AI Agent"

def run_gh_search(query, limit=5):
    try:
        result = subprocess.run(
            ["gh", "search", "repos", query, "--sort", "stars", "--limit", str(limit)],
            capture_output=True, text=True, timeout=30
        )
        repos = []
        for line in result.stdout.strip().split("\n"):
            if not line.strip():
                continue
            parts = line.split("\t")
            if len(parts) >= 2:
                repos.append({
                    "full_name": parts[0].strip(),
                    "description": parts[1].strip() if len(parts) > 1 else "",
                })
        return repos
    except Exception as e:
        return []

def load_existing():
    if os.path.exists(AGENTS_FILE):
        with open(AGENTS_FILE, "r") as f:
            return json.load(f)
    return []

def discover_agents():
    """主入口函数，供 aggregate.py 调用"""
    existing = load_existing()
    existing_ids = {a["id"] for a in existing}
    
    agent_keywords = ["agent", "assistant", "copilot", "autonomous", "openclaw", 
                      "hermes", "autogpt", "crew", "swarm", "browser use"]
    
    new_agents = []
    seen = set()
    
    for query in SEARCH_QUERIES:
        repos = run_gh_search(query, limit=5)
        for repo in repos:
            repo_name = repo["full_name"].split("/")[-1].lower()
            if repo_name in seen:
                continue
            seen.add(repo_name)
            
            if repo_name in existing_ids:
                continue
            
            desc = repo.get("description", "").lower()
            if not any(kw in repo_name or kw in desc for kw in agent_keywords):
                continue
            
            display_name = repo_name.replace("-", " ").replace("_", " ").title()
            agent = {
                "id": repo_name,
                "name": display_name,
                "url": f"https://github.com/{repo['full_name']}",
                "description": repo.get("description", "")[:100],
                "type": classify_agent(repo_name, repo.get("description", "")),
                "pricing": "开源免费",
                "difficulty": 2,
                "source": "github",
                "last_seen": datetime.now().isoformat(),
            }
            new_agents.append(agent)
    
    if new_agents:
        all_agents = existing + new_agents
        with open(AGENTS_FILE, "w") as f:
            json.dump(all_agents, f, ensure_ascii=False, indent=2)
        return f"发现 {len(new_agents)} 个新Agent，总计 {len(all_agents)} 个"
    
    return f"无新发现，当前 {len(existing)} 个Agent"

if __name__ == "__main__":
    print(discover_agents())
