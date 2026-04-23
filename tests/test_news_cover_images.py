import unittest
from datetime import datetime, timedelta

from scripts.generate_news_cover_images import (
    build_image_prompt,
    choose_insert_position,
    insert_image_into_body,
    is_cover_worthy,
    is_image_acceptable,
    select_front_page_news_ids,
    select_recent_cover_candidates,
)


class NewsCoverImageTests(unittest.TestCase):
    def test_select_front_page_news_ids_limits_to_eight(self):
        news = [
            {
                "id": str(i),
                "source": "TechCrunch AI",
                "title": f"title {i}",
                "summary": "这是一篇适合生成配图的文章摘要，信息完整，主题明确，适合制作新闻头图。",
                "content_text": "x" * 1200,
            }
            for i in range(12)
        ]
        ids = select_front_page_news_ids(news)
        self.assertEqual(len(ids), 8)
        self.assertEqual(ids[0], "0")
        self.assertEqual(ids[-1], "7")

    def test_is_cover_worthy_filters_low_information_or_event_articles(self):
        self.assertFalse(is_cover_worthy({
            "id": "a",
            "source": "InfoQ AI",
            "title": "高能研讨会｜端侧 AI 正在重写实时感知效率上限",
            "summary": "点击查看原文>",
            "content_text": "",
        }))
        self.assertTrue(is_cover_worthy({
            "id": "b",
            "source": "TechCrunch AI",
            "title": "AI 已能批量提出候选药物，10x Science 想先解决怎么筛出真有用的分子",
            "summary": "药物发现的瓶颈正在从生成候选转向验证候选，文章信息充足。",
            "content_text": "10x Science 试图用 AI 和质谱分析帮助研究团队理解复杂分子结构。" * 40,
        }))

    def test_build_image_prompt_includes_article_specific_constraints(self):
        article = {
            "title_zh": "AI 已能批量提出候选药物，10x Science 想先解决怎么筛出真有用的分子",
            "ai_summary": "药物发现的瓶颈正在从生成候选转向验证候选",
            "summary_zh": "10x Science 想把质谱分析、化学生物学算法和 AI 代理结合起来，帮助研究人员更快判断哪些复杂分子值得推进。",
            "rewrite_body": "团队希望把质谱分析这类高门槛实验手段，与化学、生物学规则算法以及 AI 代理结合起来，帮助研究人员更快读懂复杂分子结构。",
            "takeaways": [
                "候选药物越来越多，真正稀缺的是高质量表征与验证流程。",
                "这家公司解决的不是生成更多分子，而是更快筛掉无效候选。"
            ],
            "content_text": "10x Science 试图用 AI 和质谱分析帮助研究团队理解复杂分子结构。" * 20,
        }
        prompt = build_image_prompt(article)
        self.assertIn("质谱", prompt)
        self.assertIn("药物发现", prompt)
        self.assertIn("高门槛实验手段", prompt)
        self.assertIn("高质量表征与验证流程", prompt)
        self.assertIn("不要机器人头像", prompt)
        self.assertIn("不是宣传海报", prompt)
        self.assertIn("默认生成“无文字图片”", prompt)
        self.assertIn("文章正文关键信息", prompt)
        self.assertIn("请一次性完整理解以上全部信息后再出图", prompt)


    def test_select_recent_cover_candidates_only_keeps_recent_and_worthy_articles(self):
        now = datetime(2026, 4, 22, 18, 0, 0)
        recent_good = {
            "id": "recent-good",
            "source": "TechCrunch AI",
            "published": "2026-04-22T16:30:00",
            "title": "AI 已能批量提出候选药物，10x Science 想先解决怎么筛出真有用的分子",
            "summary": "药物发现的瓶颈正在从生成候选转向验证候选，文章信息充足，适合做头图。",
            "content_text": "10x Science 试图用 AI 和质谱分析帮助研究团队理解复杂分子结构。" * 40,
        }
        old_good = dict(recent_good, id="old-good", published="2026-04-22T09:30:00")
        recent_bad = dict(recent_good, id="recent-bad", title="高能研讨会｜端侧 AI 正在重写实时感知效率上限", summary="点击查看原文>", content_text="")
        ids = [x["id"] for x in select_recent_cover_candidates([recent_good, old_good, recent_bad], now=now, hours=6)]
        self.assertEqual(ids, ["recent-good"])

    def test_choose_insert_position_returns_head_mid_or_tail(self):
        body = "第一段。\n\n第二段。\n\n第三段。\n\n第四段。"
        self.assertIn(choose_insert_position(body, seed="a"), {"head", "mid", "tail"})
        self.assertIn(choose_insert_position(body, seed="b"), {"head", "mid", "tail"})

    def test_insert_image_into_body_inserts_markdown_image(self):
        body = "第一段。\n\n第二段。\n\n第三段。\n\n第四段。"
        updated = insert_image_into_body(body, "/news-images/x.png", "测试配图", seed="abc")
        self.assertIn("![测试配图](/news-images/x.png)", updated)

    def test_is_image_acceptable_rejects_generic_ai_poster_text(self):
        bad = "这是一张泛AI海报，主体是机器人头像和未来城市，大标题写着通用人工智能加速到来。"
        good = "这是一张实验室场景配图，包含分子结构、质谱峰图和分析界面，几乎没有多余文字。"
        self.assertFalse(is_image_acceptable(bad, "药物发现 + 质谱分析"))
        self.assertTrue(is_image_acceptable(good, "药物发现 + 质谱分析"))


if __name__ == '__main__':
    unittest.main()
