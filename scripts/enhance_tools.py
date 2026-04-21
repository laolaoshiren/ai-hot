#!/usr/bin/env python3
"""
为工具数据添加优缺点等新字段
"""

import json

DATA_DIR = "/root/ai-hot/data"

# 为热门工具添加优缺点数据
TOOL_ENHANCEMENTS = {
    "cursor": {
        "pros": ["AI代码补全智能", "基于VS Code，生态丰富", "支持多模型切换", "中文友好"],
        "cons": ["高级功能需付费", "偶有延迟", "隐私顾虑"],
        "best_for": ["个人开发者", "小团队", "全栈工程师"],
        "alternatives": ["copilot", "codeium", "tabnine"]
    },
    "chatgpt": {
        "pros": ["对话能力强大", "支持多模态", "插件生态丰富", "中文支持好"],
        "cons": ["需要科学上网", "高级版价格高", "有时会编造信息"],
        "best_for": ["内容创作者", "学生", "企业用户"],
        "alternatives": ["claude", "gemini", "kimi"]
    },
    "claude": {
        "pros": ["长文本处理能力强", "安全性高", "代码能力优秀", "分析能力强"],
        "cons": ["需要科学上网", "免费额度有限", "多模态能力弱于GPT-4V"],
        "best_for": ["开发者", "研究人员", "文档处理"],
        "alternatives": ["chatgpt", "gemini", "deepseek"]
    },
    "midjourney": {
        "pros": ["图像质量极高", "艺术风格多样", "社区活跃", "持续更新"],
        "cons": ["需要Discord使用", "无免费额度", "中文提示词支持弱"],
        "best_for": ["设计师", "艺术家", "内容创作者"],
        "alternatives": ["dalle3", "stable-diffusion", "adobe-firefly"]
    },
    "stable-diffusion": {
        "pros": ["完全开源免费", "可本地部署", "模型生态丰富", "高度可定制"],
        "cons": ["需要GPU", "配置复杂", "出图质量参差不齐"],
        "best_for": ["技术用户", "研究人员", "独立开发者"],
        "alternatives": ["midjourney", "dalle3", "comfyui"]
    },
    "notion-ai": {
        "pros": ["与Notion深度集成", "写作辅助强大", "总结归纳优秀", "操作简单"],
        "cons": ["需订阅Notion", "中文能力一般", "功能相对单一"],
        "best_for": ["知识工作者", "团队协作", "文档管理"],
        "alternatives": ["chatgpt", "claude", "grammarly"]
    },
    "github-copilot": {
        "pros": ["代码补全准确", "支持多语言", "IDE集成好", "学习能力强"],
        "cons": ["需要付费", "隐私问题", "有时生成重复代码"],
        "best_for": ["专业开发者", "企业团队", "开源贡献者"],
        "alternatives": ["cursor", "codeium", "tabnine"]
    },
    "deepseek": {
        "pros": ["中文能力突出", "完全免费", "代码能力强", "开源模型"],
        "cons": ["知名度较低", "插件生态弱", "多模态能力有限"],
        "best_for": ["中文用户", "开发者", "研究人员"],
        "alternatives": ["chatgpt", "claude", "kimi"]
    },
    "kimi": {
        "pros": ["超长文本支持", "中文理解优秀", "搜索能力强", "免费使用"],
        "cons": ["国际知名度低", "代码能力一般", "插件少"],
        "best_for": ["文档处理", "中文用户", "研究人员"],
        "alternatives": ["claude", "chatgpt", "deepseek"]
    },
    "dalle3": {
        "pros": ["与ChatGPT集成", "文字渲染准确", "理解力强", "使用简单"],
        "cons": ["需要ChatGPT Plus", "风格有限", "分辨率受限"],
        "best_for": ["内容创作者", "营销人员", "普通用户"],
        "alternatives": ["midjourney", "stable-diffusion", "adobe-firefly"]
    },
    "grammarly": {
        "pros": ["语法检查精准", "多平台支持", "写作风格建议", "实时反馈"],
        "cons": ["高级功能收费", "中文支持弱", "有时过度纠正"],
        "best_for": ["英文写作者", "学生", "商务人士"],
        "alternatives": ["chatgpt", "notion-ai", "quillbot"]
    },
    "perplexity": {
        "pros": ["实时搜索+AI", "信息来源标注", "研究能力强", "免费版够用"],
        "cons": ["中文内容有限", "深度分析弱于ChatGPT", "偶有错误引用"],
        "best_for": ["研究人员", "学生", "信息检索"],
        "alternatives": ["chatgpt", "claude", "bing-copilot"]
    },
    "ollama": {
        "pros": ["本地运行", "完全隐私", "支持多种模型", "简单易用"],
        "cons": ["需要硬件配置", "模型选择有限", "无云端同步"],
        "best_for": ["隐私敏感用户", "技术爱好者", "离线场景"],
        "alternatives": ["lmstudio", "gpt4all", "jan"]
    },
    "runwayml": {
        "pros": ["视频AI强大", "操作简单", "效果出色", "持续创新"],
        "cons": ["价格较高", "需要学习", "渲染时间长"],
        "best_for": ["视频创作者", "营销团队", "设计师"],
        "alternatives": ["pika", "stable-video", "capcut"]
    },
    "elevenlabs": {
        "pros": ["语音质量极高", "多语言支持", "声音克隆", "API稳定"],
        "cons": ["价格较贵", "中文支持一般", "有使用限制"],
        "best_for": ["播客制作", "有声书", "视频配音"],
        "alternatives": ["azure-tts", "google-tts", "fish-audio"]
    },
    "coze": {
        "pros": ["无需编程", "集成多种模型", "支持知识库", "免费使用"],
        "cons": ["功能有限制", "稳定性一般", "中文文档少"],
        "best_for": ["非技术用户", "快速原型", "小型项目"],
        "alternatives": ["dify", "langchain", "botpress"]
    },
    "dify": {
        "pros": ["开源可控", "功能全面", "RAG支持好", "部署灵活"],
        "cons": ["需要技术基础", "配置复杂", "社区支持有限"],
        "best_for": ["开发者", "企业用户", "技术团队"],
        "alternatives": ["coze", "langchain", "fastgpt"]
    },
    "hailuoai": {
        "pros": ["视频生成质量高", "中文支持好", "操作简单", "更新快速"],
        "cons": ["需要排队", "时长有限", "偶有瑕疵"],
        "best_for": ["短视频创作者", "营销团队", "内容创作者"],
        "alternatives": ["runwayml", "pika", "kling"]
    },
    "kling": {
        "pros": ["视频质量优秀", "物理模拟真实", "中文友好", "持续迭代"],
        "cons": ["需要申请", "生成速度慢", "分辨率受限"],
        "best_for": ["专业创作者", "影视制作", "广告创意"],
        "alternatives": ["hailuoai", "runwayml", "pika"]
    },
    "comfyui": {
        "pros": ["节点式工作流", "高度灵活", "社区活跃", "免费开源"],
        "cons": ["学习曲线陡", "需要技术基础", "界面不直观"],
        "best_for": ["高级用户", "AI艺术家", "研究人员"],
        "alternatives": ["stable-diffusion-webui", "fooocus", "automatic1111"]
    }
}


def enhance_tools():
    with open(f"{DATA_DIR}/tools.json", "r") as f:
        tools = json.load(f)
    
    print(f"工具总数: {len(tools)}")
    
    enhanced_count = 0
    for tool in tools:
        tool_id = tool.get('id', '')
        if tool_id in TOOL_ENHANCEMENTS:
            enhancement = TOOL_ENHANCEMENTS[tool_id]
            tool.update(enhancement)
            enhanced_count += 1
            print(f"  ✅ {tool['name']}: 添加了优缺点信息")
    
    # 保存修改
    with open(f"{DATA_DIR}/tools.json", "w") as f:
        json.dump(tools, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 增强了 {enhanced_count} 个工具的数据")
    
    # 统计有优缺点的工具数量
    with_pros = len([t for t in tools if t.get('pros')])
    with_cons = len([t for t in tools if t.get('cons')])
    with_best_for = len([t for t in tools if t.get('best_for')])
    
    print(f"\n📊 数据质量统计:")
    print(f"  有优点: {with_pros}/{len(tools)}")
    print(f"  有缺点: {with_cons}/{len(tools)}")
    print(f"  有适用场景: {with_best_for}/{len(tools)}")


if __name__ == "__main__":
    enhance_tools()