#!/usr/bin/env python3
"""
AI 能力模块 v3.0
用大模型给冰冷的数据注入智能感

能力:
1. 新闻智能摘要 - 每条新闻生成一句话中文摘要
2. 每日 AI 快报 - 综合当日新闻生成一段总结
3. 工具质量评分 - AI 评估工具好坏
4. 关联推荐 - 根据工具特性推荐相关工具
"""

import os
import json
import re
from datetime import datetime

try:
    import requests
except ImportError:
    os.system("pip install requests -q")
    import requests

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

# 从环境变量或 auth.json 读取 API key
def get_api_key():
    """读取 Nous API key"""
    auth_path = os.path.join(os.path.expanduser("~"), ".hermes", "auth.json")
    try:
        with open(auth_path) as f:
            auth = json.load(f)
        return auth["providers"]["nous"]["agent_key"]
    except Exception:
        return os.environ.get("NOUS_API_KEY", "")


def llm_call(prompt, max_tokens=500, system="你是一个专业的AI领域分析师。"):
    """调用 Nous Research API"""
    api_key = get_api_key()
    if not api_key:
        return None

    try:
        resp = requests.post(
            "https://inference-api.nousresearch.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "nousresearch/hermes-4-405b",
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": max_tokens,
                "temperature": 0.7,
            },
            timeout=60
        )
        if resp.status_code == 200:
            return resp.json()["choices"][0]["message"]["content"]
        else:
            print(f"  ⚠️ API 返回 {resp.status_code}: {resp.text[:100]}")
            return None
    except Exception as e:
        print(f"  ⚠️ API 调用失败: {e}")
        return None


def summarize_news():
    """为没有摘要的新闻生成 AI 摘要"""
    news_path = os.path.join(DATA_DIR, "news.json")
    if not os.path.exists(news_path):
        return "无新闻数据"

    with open(news_path, encoding="utf-8") as f:
        news = json.load(f)

    summarized = 0
    for item in news[:30]:  # 只处理最新的30条
        if item.get("ai_summary"):
            continue

        title = item.get("title", "")
        summary = item.get("summary", "")

        # 用 AI 生成一句话摘要
        prompt = f"请用一句话（不超过50字）总结这条AI新闻的核心要点，用中文回答，不要加引号：\n\n标题：{title}\n内容：{summary[:300]}"

        result = llm_call(prompt, max_tokens=100)
        if result:
            item["ai_summary"] = result.strip().strip('"').strip("'")
            summarized += 1
            print(f"  ✓ {title[:30]}: {item['ai_summary'][:40]}...")

    with open(news_path, "w", encoding="utf-8") as f:
        json.dump(news, f, ensure_ascii=False, indent=2)

    return f"AI 摘要完成: {summarized} 条"


def generate_daily_briefing():
    """生成每日 AI 快报"""
    news_path = os.path.join(DATA_DIR, "news.json")
    if not os.path.exists(news_path):
        return "无新闻数据"

    with open(news_path, encoding="utf-8") as f:
        news = json.load(f)

    # 取今天和昨天的新闻
    today = datetime.now().strftime("%Y-%m-%d")
    recent_news = [n for n in news if (n.get("published") or "").startswith(today)]

    if not recent_news:
        # 如果今天没有，取最新的20条
        recent_news = news[:20]

    # 拼接新闻标题
    titles = "\n".join([f"- {n['title']}" for n in recent_news[:20]])

    prompt = f"""请根据以下今日AI新闻标题，写一段200字以内的中文日报总结。格式要求：
1. 开头用一句话概括今天AI领域最重要的事
2. 然后分2-3个要点展开
3. 语言简洁专业，像科技媒体编辑写的
4. 不要用markdown格式，纯文本

今日AI新闻：
{titles}"""

    result = llm_call(prompt, max_tokens=600)
    if result:
        briefing = {
            "date": today,
            "content": result.strip(),
            "news_count": len(recent_news),
            "generated_at": datetime.now().isoformat(),
        }

        briefing_path = os.path.join(DATA_DIR, "briefing.json")
        with open(briefing_path, "w", encoding="utf-8") as f:
            json.dump(briefing, f, ensure_ascii=False, indent=2)

        return f"每日快报生成: {len(recent_news)} 条新闻 → 200字总结"

    return "AI 快报生成失败"


def score_tools():
    """AI 评估工具质量"""
    tools_path = os.path.join(DATA_DIR, "tools.json")
    if not os.path.exists(tools_path):
        return "无工具数据"

    with open(tools_path, encoding="utf-8") as f:
        tools = json.load(f)

    scored = 0
    for tool in tools[:10]:  # 每次处理10个
        if tool.get("ai_score"):
            continue

        name = tool.get("name", "")
        desc = tool.get("description", "")
        pricing = tool.get("pricing", "")
        category = tool.get("category", "")

        prompt = f"""请对这个AI工具进行简短评价（1-2句话），然后给出1-10分的评分。

工具：{name}
类别：{category}
描述：{desc}
价格：{pricing}

请用以下格式回答：
评价：（你的评价）
评分：（数字）"""

        result = llm_call(prompt, max_tokens=150)
        if result:
            # 解析评分
            score_match = re.search(r'评分[：:]\s*(\d+(?:\.\d+)?)', result)
            if score_match:
                tool["ai_score"] = float(score_match.group(1))
            # 解析评价
            eval_match = re.search(r'评价[：:]\s*(.+?)(?:\n|$)', result)
            if eval_match:
                tool["ai_review"] = eval_match.group(1).strip()
            scored += 1
            print(f"  ✓ {name}: {tool.get('ai_score', '?')}分")

    with open(tools_path, "w", encoding="utf-8") as f:
        json.dump(tools, f, ensure_ascii=False, indent=2)

    return f"工具评分完成: {scored} 个"


def suggest_related():
    """AI 推荐相关工具"""
    tools_path = os.path.join(DATA_DIR, "tools.json")
    if not os.path.exists(tools_path):
        return "无工具数据"

    with open(tools_path, encoding="utf-8") as f:
        tools = json.load(f)

    # 取前5个没有 related 的工具
    todo = [t for t in tools if not t.get("ai_related")][:5]

    # 构建工具列表
    tool_list = "\n".join([f"- {t['name']}: {t.get('description', '')}" for t in tools])

    for tool in todo:
        prompt = f"""从以下工具列表中，为「{tool['name']}」推荐3个最相关的工具（只返回工具名，用逗号分隔）：

{tool_list}"""

        result = llm_call(prompt, max_tokens=100)
        if result:
            tool["ai_related"] = [n.strip() for n in result.strip().split(",")[:3]]
            print(f"  ✓ {tool['name']}: 关联 {tool['ai_related']}")

    with open(tools_path, "w", encoding="utf-8") as f:
        json.dump(tools, f, ensure_ascii=False, indent=2)

    return f"关联推荐完成: {len(todo)} 个工具"


if __name__ == "__main__":
    print("=== AI 能力模块测试 ===")
    print(f"API Key: {'已配置' if get_api_key() else '未配置'}")
    print(f"1. 新闻摘要: {summarize_news()}")
    print(f"2. 每日快报: {generate_daily_briefing()}")
    print(f"3. 工具评分: {score_tools()}")
    print(f"4. 关联推荐: {suggest_related()}")
