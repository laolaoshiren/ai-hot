#!/usr/bin/env python3
"""
工具数据扩充脚本
添加教育、健康、法律、金融等垂直领域 AI 工具
"""

import json
import hashlib

DATA_DIR = "/root/ai-hot/data"

# 新增工具数据
NEW_TOOLS = [
    # 教育类
    {"name": "Duolingo Max", "url": "https://duolingo.com", "description": "AI驱动的语言学习平台，提供个性化课程和实时对话练习", "category": "教育", "pricing": "免费 + Super $7/月", "free_quota": "基础课程免费", "difficulty": 1, "tags": ["#education", "#language", "#learning"], "use_cases": "语言学习、口语练习、语法纠正"},
    {"name": "Khan Academy AI", "url": "https://khanacademy.org", "description": "AI导师提供个性化数学、科学学习路径", "category": "教育", "pricing": "免费", "free_quota": "完全免费", "difficulty": 1, "tags": ["#education", "#math", "#science"], "use_cases": "数学学习、科学教育、个性化辅导"},
    {"name": "Socratic by Google", "url": "https://socratic.org", "description": "拍照搜题AI，支持数学、科学、文学等学科", "category": "教育", "pricing": "免费", "free_quota": "完全免费", "difficulty": 1, "tags": ["#education", "#homework", "#tutor"], "use_cases": "作业辅导、概念解释、学习辅助"},
    {"name": "Quizlet AI", "url": "https://quizlet.com", "description": "AI生成闪卡和学习材料，智能复习系统", "category": "教育", "pricing": "免费 + Plus $8/月", "free_quota": "基础功能免费", "difficulty": 1, "tags": ["#education", "#flashcards", "#study"], "use_cases": "记忆训练、考试准备、知识巩固"},
    {"name": "Photomath", "url": "https://photomath.com", "description": "拍照解数学题，提供详细解题步骤", "category": "教育", "pricing": "免费 + Plus $10/月", "free_quota": "基础解题免费", "difficulty": 1, "tags": ["#education", "#math", "#solver"], "use_cases": "数学解题、步骤学习、作业帮助"},
    {"name": "Elsa Speak", "url": "https://elsaspeak.com", "description": "AI英语口语教练，实时发音纠正", "category": "教育", "pricing": "免费 + Pro $12/月", "free_quota": "每日基础练习", "difficulty": 1, "tags": ["#education", "#english", "#speaking"], "use_cases": "英语口语、发音纠正、流利度提升"},
    {"name": "Century Tech", "url": "https://century.tech", "description": "AI个性化学习平台，为学校和企业提供定制课程", "category": "教育", "pricing": "企业定价", "free_quota": "学校免费试用", "difficulty": 2, "tags": ["#education", "#enterprise", "#adaptive"], "use_cases": "企业培训、学校教育、个性化学习"},
    {"name": "Gradescope", "url": "https://gradescope.com", "description": "AI辅助作业批改和评分系统", "category": "教育", "pricing": "学校定价", "free_quota": "教师免费", "difficulty": 2, "tags": ["#education", "#grading", "#assessment"], "use_cases": "作业批改、考试评分、教学反馈"},
    
    # 健康类
    {"name": "Ada Health", "url": "https://ada.com", "description": "AI症状检查器，提供健康评估和建议", "category": "健康", "pricing": "免费", "free_quota": "完全免费", "difficulty": 1, "tags": ["#health", "#symptom", "#diagnosis"], "use_cases": "症状检查、健康评估、医疗建议"},
    {"name": "Babylon Health", "url": "https://babylonhealth.com", "description": "AI医生咨询，24/7在线健康服务", "category": "健康", "pricing": "订阅制", "free_quota": "基础咨询免费", "difficulty": 1, "tags": ["#health", "#telemedicine", "#consultation"], "use_cases": "在线问诊、健康监测、医疗咨询"},
    {"name": "Woebot", "url": "https://woebot.io", "description": "AI心理健康聊天机器人，提供CBT疗法", "category": "健康", "pricing": "免费", "free_quota": "完全免费", "difficulty": 1, "tags": ["#health", "#mental", "#therapy"], "use_cases": "心理健康、情绪管理、压力缓解"},
    {"name": "Your.MD", "url": "https://your.md", "description": "AI健康助手，提供个性化健康信息", "category": "健康", "pricing": "免费", "free_quota": "完全免费", "difficulty": 1, "tags": ["#health", "#information", "#wellness"], "use_cases": "健康信息、疾病预防、生活方式建议"},
    {"name": "Fitbit AI", "url": "https://fitbit.com", "description": "AI健康数据分析，睡眠和运动建议", "category": "健康", "pricing": "设备+订阅", "free_quota": "基础功能免费", "difficulty": 1, "tags": ["#health", "#fitness", "#wearable"], "use_cases": "运动监测、睡眠分析、健康数据"},
    {"name": "Tempus", "url": "https://tempus.com", "description": "AI驱动的精准医疗和癌症治疗分析", "category": "健康", "pricing": "企业定价", "free_quota": "研究机构合作", "difficulty": 3, "tags": ["#health", "#precision", "#oncology"], "use_cases": "癌症治疗、精准医疗、基因分析"},
    
    # 法律类
    {"name": "DoNotPay", "url": "https://donotpay.com", "description": "AI律师，自动处理罚单、取消订阅等法律事务", "category": "法律", "pricing": "订阅制", "free_quota": "首次免费", "difficulty": 1, "tags": ["#legal", "#consumer", "#automation"], "use_cases": "罚单申诉、订阅取消、消费者权益"},
    {"name": "LawGeex", "url": "https://lawgeex.com", "description": "AI合同审查平台，自动识别风险条款", "category": "法律", "pricing": "企业定价", "free_quota": "企业试用", "difficulty": 2, "tags": ["#legal", "#contract", "#review"], "use_cases": "合同审查、风险识别、法律合规"},
    {"name": "Kira Systems", "url": "https://kirasystems.com", "description": "AI合同分析，提取关键条款和义务", "category": "法律", "pricing": "企业定价", "free_quota": "企业试用", "difficulty": 2, "tags": ["#legal", "#analysis", "#extraction"], "use_cases": "合同分析、条款提取、尽职调查"},
    {"name": "CaseText", "url": "https://casetext.com", "description": "AI法律研究助手，快速找到相关案例", "category": "法律", "pricing": "订阅制", "free_quota": "免费试用", "difficulty": 2, "tags": ["#legal", "#research", "#cases"], "use_cases": "法律研究、案例查找、判例分析"},
    {"name": "Juro", "url": "https://juro.com", "description": "AI合同管理平台，自动化合同生命周期", "category": "法律", "pricing": "企业定价", "free_quota": "企业试用", "difficulty": 2, "tags": ["#legal", "#management", "#lifecycle"], "use_cases": "合同管理、审批流程、电子签名"},
    {"name": "Luminance", "url": "https://luminance.com", "description": "AI法律文档分析，识别异常和风险", "category": "法律", "pricing": "企业定价", "free_quota": "企业试用", "difficulty": 2, "tags": ["#legal", "#document", "#risk"], "use_cases": "文档审查、风险识别、合规检查"},
    
    # 金融类
    {"name": "Wealthfront", "url": "https://wealthfront.com", "description": "AI理财顾问，自动化投资组合管理", "category": "金融", "pricing": "0.25%管理费", "free_quota": "首$5000免费", "difficulty": 1, "tags": ["#finance", "#investment", "#robo-advisor"], "use_cases": "投资管理、理财规划、资产配置"},
    {"name": "Betterment", "url": "https://betterment.com", "description": "AI驱动的投资平台，个性化投资建议", "category": "金融", "pricing": "0.25%管理费", "free_quota": "基础账户免费", "difficulty": 1, "tags": ["#finance", "#investment", "#automation"], "use_cases": "自动化投资、退休规划、税务优化"},
    {"name": "Kavout", "url": "https://kavout.com", "description": "AI股票评分系统，Kai Score量化分析", "category": "金融", "pricing": "订阅制", "free_quota": "基础评分免费", "difficulty": 2, "tags": ["#finance", "#stocks", "#analysis"], "use_cases": "股票分析、量化投资、市场预测"},
    {"name": "Upstart", "url": "https://upstart.com", "description": "AI贷款平台，使用AI评估信用风险", "category": "金融", "pricing": "贷款利率", "free_quota": "免费评估", "difficulty": 1, "tags": ["#finance", "#lending", "#credit"], "use_cases": "个人贷款、信用评估、风险定价"},
    {"name": "AlphaSense", "url": "https://alpha-sense.com", "description": "AI市场情报平台，分析财报和新闻", "category": "金融", "pricing": "企业定价", "free_quota": "企业试用", "difficulty": 2, "tags": ["#finance", "#intelligence", "#research"], "use_cases": "市场研究、财报分析、投资决策"},
    {"name": "Sentieo", "url": "https://sentieo.com", "description": "AI金融研究平台，文档搜索和分析", "category": "金融", "pricing": "企业定价", "free_quota": "企业试用", "difficulty": 2, "tags": ["#finance", "#research", "#document"], "use_cases": "金融研究、文档分析、信息提取"},
    {"name": "Kensho", "url": "https://kensho.com", "description": "AI金融数据分析，为机构投资者提供洞察", "category": "金融", "pricing": "企业定价", "free_quota": "企业合作", "difficulty": 3, "tags": ["#finance", "#analytics", "#institutional"], "use_cases": "金融分析、风险建模、市场预测"},
    {"name": "Zest AI", "url": "https://zest.ai", "description": "AI信用风险建模，公平透明的贷款决策", "category": "金融", "pricing": "企业定价", "free_quota": "企业合作", "difficulty": 2, "tags": ["#finance", "#credit", "#fairness"], "use_cases": "信用评分、风险建模、公平借贷"},
    
    # 设计类
    {"name": "Midjourney", "url": "https://midjourney.com", "description": "AI图像生成器，创建高质量艺术作品", "category": "绘画", "pricing": "订阅制 $10-60/月", "free_quota": "有限免费试用", "difficulty": 2, "tags": ["#design", "#art", "#generation"], "use_cases": "艺术创作、概念设计、视觉内容"},
    {"name": "Canva AI", "url": "https://canva.com", "description": "AI设计助手，模板和智能设计建议", "category": "设计", "pricing": "免费 + Pro $13/月", "free_quota": "基础功能免费", "difficulty": 1, "tags": ["#design", "#template", "#graphics"], "use_cases": "平面设计、社交媒体、演示文稿"},
    {"name": "Figma AI", "url": "https://figma.com", "description": "AI设计工具，智能布局和设计系统", "category": "设计", "pricing": "免费 + Professional $15/月", "free_quota": "3个项目免费", "difficulty": 2, "tags": ["#design", "#ui", "#prototyping"], "use_cases": "UI设计、原型制作、设计协作"},
    {"name": "Adobe Firefly", "url": "https://firefly.adobe.com", "description": "Adobe的AI图像生成，与Creative Cloud集成", "category": "绘画", "pricing": "订阅制", "free_quota": "每月25积分", "difficulty": 2, "tags": ["#design", "#adobe", "#generation"], "use_cases": "图像生成、创意设计、内容创作"},
    {"name": "DALL-E 3", "url": "https://openai.com/dall-e-3", "description": "OpenAI的图像生成模型，高质量创意图像", "category": "绘画", "pricing": "按使用量计费", "free_quota": "ChatGPT Plus包含", "difficulty": 1, "tags": ["#design", "#openai", "#generation"], "use_cases": "图像生成、创意可视化、内容创作"},
    {"name": "Stable Diffusion", "url": "https://stability.ai", "description": "开源图像生成模型，可本地部署", "category": "绘画", "pricing": "开源免费", "free_quota": "完全免费", "difficulty": 3, "tags": ["#design", "#open-source", "#local"], "use_cases": "本地图像生成、模型定制、研究开发"},
    {"name": "Runway ML", "url": "https://runwayml.com", "description": "AI创意工具套件，视频和图像编辑", "category": "视频", "pricing": "订阅制 $15-35/月", "free_quota": "有限免费试用", "difficulty": 2, "tags": ["#design", "#video", "#editing"], "use_cases": "视频编辑、特效制作、创意内容"},
    {"name": "Looka", "url": "https://looka.com", "description": "AI标志设计，几分钟创建专业品牌", "category": "设计", "pricing": "一次性 $20-65", "free_quota": "免费预览", "difficulty": 1, "tags": ["#design", "#logo", "#branding"], "use_cases": "标志设计、品牌创建、视觉识别"},
    
    # 营销类
    {"name": "Jasper", "url": "https://jasper.ai", "description": "AI营销文案生成，博客、广告、社交媒体", "category": "营销", "pricing": "订阅制 $49-125/月", "free_quota": "免费试用5天", "difficulty": 1, "tags": ["#marketing", "#copywriting", "#content"], "use_cases": "营销文案、内容创作、广告文案"},
    {"name": "Copy.ai", "url": "https://copy.ai", "description": "AI文案工具，生成营销内容和文案", "category": "营销", "pricing": "免费 + Pro $49/月", "free_quota": "每月2000字", "difficulty": 1, "tags": ["#marketing", "#copywriting", "#automation"], "use_cases": "文案创作、营销内容、社交媒体"},
    {"name": "MarketMuse", "url": "https://marketmuse.com", "description": "AI内容策略平台，优化SEO和内容规划", "category": "营销", "pricing": "订阅制 $149+/月", "free_quota": "有限免费分析", "difficulty": 2, "tags": ["#marketing", "#seo", "#content-strategy"], "use_cases": "SEO优化、内容规划、竞争分析"},
    {"name": "Persado", "url": "https://persado.com", "description": "AI营销语言优化，生成高转化文案", "category": "营销", "pricing": "企业定价", "free_quota": "企业试用", "difficulty": 2, "tags": ["#marketing", "#language", "#conversion"], "use_cases": "文案优化、转化提升、情感分析"},
    {"name": "Phrasee", "url": "https://phrasee.co", "description": "AI邮件营销优化，提升打开率和点击率", "category": "营销", "pricing": "企业定价", "free_quota": "企业试用", "difficulty": 2, "tags": ["#marketing", "#email", "#optimization"], "use_cases": "邮件营销、标题优化、A/B测试"},
    {"name": "Albert AI", "url": "https://albert.ai", "description": "AI数字营销平台，自动化广告投放", "category": "营销", "pricing": "企业定价", "free_quota": "企业试用", "difficulty": 2, "tags": ["#marketing", "#advertising", "#automation"], "use_cases": "广告投放、营销自动化、预算优化"},
    
    # 客服类
    {"name": "Intercom AI", "url": "https://intercom.com", "description": "AI客服机器人，自动回答常见问题", "category": "客服", "pricing": "订阅制 $74+/月", "free_quota": "14天免费试用", "difficulty": 2, "tags": ["#customer-service", "#chatbot", "#support"], "use_cases": "客户支持、问题解答、工单管理"},
    {"name": "Zendesk AI", "url": "https://zendesk.com", "description": "AI客服解决方案，智能路由和回复", "category": "客服", "pricing": "订阅制 $49+/月", "free_quota": "14天免费试用", "difficulty": 2, "tags": ["#customer-service", "#automation", "#routing"], "use_cases": "客服自动化、工单分类、智能回复"},
    {"name": "Drift", "url": "https://drift.com", "description": "AI对话营销，实时聊天和销售自动化", "category": "客服", "pricing": "企业定价", "free_quota": "基础聊天免费", "difficulty": 2, "tags": ["#customer-service", "#sales", "#chat"], "use_cases": "销售支持、实时聊天、潜在客户开发"},
    {"name": "Ada", "url": "https://ada.cx", "description": "AI客服平台，无需编码的聊天机器人", "category": "客服", "pricing": "企业定价", "free_quota": "企业试用", "difficulty": 2, "tags": ["#customer-service", "#no-code", "#automation"], "use_cases": "客服自动化、多渠道支持、问题解决"},
    {"name": "Freshdesk AI", "url": "https://freshdesk.com", "description": "AI帮助台软件，智能工单管理", "category": "客服", "pricing": "免费 + 订阅制", "free_quota": "基础功能免费", "difficulty": 1, "tags": ["#customer-service", "#helpdesk", "#tickets"], "use_cases": "工单管理、客户支持、团队协作"},
    {"name": "Kustomer", "url": "https://kustomer.com", "description": "AI驱动的CRM和客服平台", "category": "客服", "pricing": "企业定价", "free_quota": "企业试用", "difficulty": 2, "tags": ["#customer-service", "#crm", "#omnichannel"], "use_cases": "客户关系、全渠道支持、数据分析"},
    
    # 数据分析类
    {"name": "Tableau AI", "url": "https://tableau.com", "description": "AI增强的数据可视化，自然语言查询", "category": "数据分析", "pricing": "订阅制 $70+/月", "free_quota": "Tableau Public免费", "difficulty": 2, "tags": ["#data", "#visualization", "#analytics"], "use_cases": "数据可视化、商业智能、报表分析"},
    {"name": "Power BI AI", "url": "https://powerbi.microsoft.com", "description": "微软的AI商业分析工具，智能洞察", "category": "数据分析", "pricing": "免费 + Pro $10/月", "free_quota": "基础功能免费", "difficulty": 2, "tags": ["#data", "#microsoft", "#business-intelligence"], "use_cases": "数据分析、商业智能、报表制作"},
    {"name": "Alteryx", "url": "https://alteryx.com", "description": "AI数据分析平台，自动化数据准备和分析", "category": "数据分析", "pricing": "订阅制 $5000+/年", "free_quota": "免费试用", "difficulty": 3, "tags": ["#data", "#automation", "#preparation"], "use_cases": "数据准备、分析自动化、工作流优化"},
    {"name": "DataRobot", "url": "https://datarobot.com", "description": "AI机器学习平台，自动化模型构建", "category": "数据分析", "pricing": "企业定价", "free_qty": "企业试用", "difficulty": 3, "tags": ["#data", "#machine-learning", "#autoML"], "use_cases": "机器学习、预测建模、自动化分析"},
    {"name": "H2O.ai", "url": "https://h2o.ai", "description": "开源AI平台，自动化机器学习", "category": "数据分析", "pricing": "开源 + 企业版", "free_quota": "开源免费", "difficulty": 3, "tags": ["#data", "#open-source", "#machine-learning"], "use_cases": "机器学习、预测分析、开源AI"},
    {"name": "Sisense", "url": "https://sisense.com", "description": "AI驱动的商业分析平台，嵌入式分析", "category": "数据分析", "pricing": "企业定价", "free_quota": "企业试用", "difficulty": 2, "tags": ["#data", "#embedded", "#analytics"], "use_cases": "嵌入式分析、商业智能、数据产品"},
    {"name": "Qlik Sense", "url": "https://qlik.com", "description": "AI增强的数据发现和可视化", "category": "数据分析", "pricing": "订阅制 $30+/月", "free_quota": "免费个人版", "difficulty": 2, "tags": ["#data", "#discovery", "#visualization"], "use_cases": "数据发现、可视化分析、关联分析"},
    {"name": "ThoughtSpot", "url": "https://thoughtspot.com", "description": "AI搜索驱动的分析，自然语言查询", "category": "数据分析", "pricing": "企业定价", "free_quota": "企业试用", "difficulty": 2, "tags": ["#data", "#search", "#natural-language"], "use_cases": "搜索分析、自然语言查询、自助分析"},
    
    # 翻译类
    {"name": "DeepL", "url": "https://deepl.com", "description": "高质量AI翻译，支持30+语言", "category": "翻译", "pricing": "免费 + Pro $7/月", "free_quota": "每月50万字符", "difficulty": 1, "tags": ["#translation", "#language", "#quality"], "use_cases": "文档翻译、网页翻译、专业翻译"},
    {"name": "Google Translate", "url": "https://translate.google.com", "description": "谷歌AI翻译，支持100+语言", "category": "翻译", "pricing": "免费", "free_quota": "完全免费", "difficulty": 1, "tags": ["#translation", "#google", "#multilingual"], "use_cases": "实时翻译、网页翻译、多语言交流"},
    {"name": "Microsoft Translator", "url": "https://translator.microsoft.com", "description": "微软AI翻译，集成Office和Edge", "category": "翻译", "pricing": "免费 + API计费", "free_quota": "每月200万字符", "difficulty": 1, "tags": ["#translation", "#microsoft", "#integration"], "use_cases": "文档翻译、API集成、实时翻译"},
    {"name": "Smartling", "url": "https://smartling.com", "description": "AI本地化平台，自动化翻译管理", "category": "翻译", "pricing": "企业定价", "free_quota": "企业试用", "difficulty": 2, "tags": ["#translation", "#localization", "#management"], "use_cases": "网站本地化、内容翻译、多语言管理"},
    {"name": "Lilt", "url": "https://lilt.com", "description": "AI辅助翻译，人机协作提高效率", "category": "翻译", "pricing": "企业定价", "free_quota": "企业试用", "difficulty": 2, "tags": ["#translation", "#human-ai", "#collaboration"], "use_cases": "专业翻译、人机协作、翻译记忆"},
    {"name": "Unbabel", "url": "https://unbabel.com", "description": "AI翻译+人工校对，客服翻译解决方案", "category": "翻译", "pricing": "企业定价", "free_quota": "企业试用", "difficulty": 2, "tags": ["#translation", "#customer-service", "#hybrid"], "use_cases": "客服翻译、多语言支持、质量保证"},
    
    # 会议类
    {"name": "Otter.ai", "url": "https://otter.ai", "description": "AI会议记录，实时转录和摘要", "category": "会议", "pricing": "免费 + Pro $17/月", "free_quota": "每月600分钟", "difficulty": 1, "tags": ["#meeting", "#transcription", "#notes"], "use_cases": "会议记录、访谈转录、笔记整理"},
    {"name": "Fireflies.ai", "url": "https://fireflies.ai", "description": "AI会议助手，自动记录和分析对话", "category": "会议", "pricing": "免费 + Pro $10/月", "free_quota": "有限免费存储", "difficulty": 1, "tags": ["#meeting", "#recording", "#analysis"], "use_cases": "会议分析、销售通话、团队协作"},
    {"name": "Grain", "url": "https://grain.com", "description": "AI视频会议工具，自动剪辑和分享亮点", "category": "会议", "pricing": "免费 + Pro $15/月", "free_quota": "基础功能免费", "difficulty": 1, "tags": ["#meeting", "#video", "#highlights"], "use_cases": "会议剪辑、亮点分享、知识管理"},
    {"name": "Fathom", "url": "https://fathom.video", "description": "AI会议记录，自动总结行动项", "category": "会议", "pricing": "免费", "free_quota": "完全免费", "difficulty": 1, "tags": ["#meeting", "#action-items", "#summary"], "use_cases": "会议总结、行动项跟踪、团队同步"},
    {"name": "Avoma", "url": "https://avoma.com", "description": "AI会议助手，销售通话分析和辅导", "category": "会议", "pricing": "订阅制 $17+/月", "free_quota": "14天免费试用", "difficulty": 2, "tags": ["#meeting", "#sales", "#coaching"], "use_cases": "销售分析、通话辅导、客户洞察"},
    {"name": "Chorus.ai", "url": "https://chorus.ai", "description": "AI对话智能平台，销售团队优化", "category": "会议", "pricing": "企业定价", "free_quota": "企业试用", "difficulty": 2, "tags": ["#meeting", "#conversation-intelligence", "#sales"], "use_cases": "销售优化、对话分析、团队培训"},
    
    # 简历类
    {"name": "Resume.io", "url": "https://resume.io", "description": "AI简历构建器，专业模板和优化建议", "category": "简历", "pricing": "免费 + Pro $3/月", "free_quota": "基础模板免费", "difficulty": 1, "tags": ["#resume", "#cv", "#templates"], "use_cases": "简历制作、求职申请、职业发展"},
    {"name": "Kickresume", "url": "https://kickresume.com", "description": "AI简历和求职信生成，个性化建议", "category": "简历", "pricing": "免费 + Pro $5/月", "free_quota": "基础功能免费", "difficulty": 1, "tags": ["#resume", "#cover-letter", "#ai"], "use_cases": "简历优化、求职信撰写、面试准备"},
    {"name": "Jobscan", "url": "https://jobscan.co", "description": "AI简历优化，匹配职位描述关键词", "category": "简历", "pricing": "免费 + Pro $50/月", "free_quota": "每月5次扫描", "difficulty": 1, "tags": ["#resume", "#optimization", "#keywords"], "use_cases": "简历优化、ATS兼容、关键词匹配"},
    {"name": "Teal", "url": "https://tealhq.com", "description": "AI职业发展平台，简历和求职跟踪", "category": "简历", "pricing": "免费 + Pro $9/周", "free_quota": "基础功能免费", "difficulty": 1, "tags": ["#resume", "#career", "#tracking"], "use_cases": "求职跟踪、简历管理、职业规划"},
    {"name": "Rezi", "url": "https://rezi.ai", "description": "AI简历构建器，ATS优化和内容建议", "category": "简历", "pricing": "免费 + Pro $3/月", "free_quota": "基础功能免费", "difficulty": 1, "tags": ["#resume", "#ats", "#optimization"], "use_cases": "ATS优化、内容建议、简历评分"},
    {"name": "Zety", "url": "https://zety.com", "description": "AI简历制作工具，专家建议和模板", "category": "简历", "pricing": "免费 + Pro $6/月", "free_quota": "创建免费", "difficulty": 1, "tags": ["#resume", "#builder", "#expert"], "use_cases": "简历创建、专家建议、模板选择"},
    
    # 电商类
    {"name": "Shopify AI", "url": "https://shopify.com", "description": "AI电商助手，产品描述和营销文案", "category": "电商", "pricing": "订阅制 $29+/月", "free_quota": "14天免费试用", "difficulty": 1, "tags": ["#ecommerce", "#store", "#marketing"], "use_cases": "电商建站、产品描述、营销自动化"},
    {"name": "Klaviyo", "url": "https://klaviyo.com", "description": "AI邮件营销平台，电商自动化", "category": "电商", "pricing": "免费 + 按联系人计费", "free_quota": "250联系人免费", "difficulty": 2, "tags": ["#ecommerce", "#email", "#automation"], "use_cases": "邮件营销、客户分群、销售自动化"},
    {"name": "Dynamic Yield", "url": "https://dynamicyield.com", "description": "AI个性化平台，电商体验优化", "category": "电商", "pricing": "企业定价", "free_quota": "企业试用", "difficulty": 3, "tags": ["#ecommerce", "#personalization", "#optimization"], "use_cases": "个性化推荐、A/B测试、用户体验"},
    {"name": "Bloomreach", "url": "https://bloomreach.com", "description": "AI电商搜索和 merchandising", "category": "电商", "pricing": "企业定价", "free_quota": "企业试用", "difficulty": 2, "tags": ["#ecommerce", "#search", "#merchandising"], "use_cases": "商品搜索、产品发现、 merchandising"},
    {"name": "Nosto", "url": "https://nosto.com", "description": "AI电商个性化，产品推荐和营销", "category": "电商", "pricing": "企业定价", "free_quota": "企业试用", "difficulty": 2, "tags": ["#ecommerce", "#recommendation", "#personalization"], "use_cases": "产品推荐、个性化营销、购物车优化"},
    {"name": "Clerk.io", "url": "https://clerk.io", "description": "AI电商搜索和推荐引擎", "category": "电商", "pricing": "按使用量计费", "free_quota": "每月1000次免费", "difficulty": 2, "tags": ["#ecommerce", "#search", "#recommendations"], "use_cases": "商品搜索、产品推荐、个性化展示"},
]


def add_tools():
    # 读取现有工具
    with open(f"{DATA_DIR}/tools.json", "r") as f:
        existing_tools = json.load(f)
    
    print(f"现有工具数量: {len(existing_tools)}")
    
    # 生成ID和添加元数据
    for tool in NEW_TOOLS:
        # 生成基于名称的ID
        tool_id = tool["name"].lower().replace(" ", "-").replace(".", "-")
        tool["id"] = tool_id
        
        # 添加默认值
        tool.setdefault("stars", None)
        tool.setdefault("trending", False)
        tool.setdefault("featured", False)
    
    # 合并工具（避免重复）
    existing_ids = {t["id"] for t in existing_tools}
    new_tools_added = []
    
    for tool in NEW_TOOLS:
        if tool["id"] not in existing_ids:
            new_tools_added.append(tool)
            existing_ids.add(tool["id"])
    
    # 合并所有工具
    all_tools = existing_tools + new_tools_added
    
    # 保存到文件
    with open(f"{DATA_DIR}/tools.json", "w") as f:
        json.dump(all_tools, f, ensure_ascii=False, indent=2)
    
    print(f"新增工具数量: {len(new_tools_added)}")
    print(f"总工具数量: {len(all_tools)}")
    
    # 统计分类分布
    from collections import Counter
    categories = Counter([t.get("category", "未分类") for t in all_tools])
    
    print("\n📊 更新后工具分类分布:")
    for cat, count in categories.most_common():
        print(f"  {cat}: {count}")
    
    # 显示新增工具示例
    print("\n🆕 新增工具示例:")
    for i, tool in enumerate(new_tools_added[:3]):
        print(f"  {i+1}. {tool['name']} - {tool['category']}")
        print(f"     {tool['description'][:50]}...")


if __name__ == "__main__":
    add_tools()