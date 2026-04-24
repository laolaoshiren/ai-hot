import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'scripts'
sys.path.insert(0, str(SCRIPTS))

class HotAndNewsGenerationRegressionTests(unittest.TestCase):
    def test_trending_scorer_homepage_is_news_only(self):
        text = (SCRIPTS / 'trending_scorer.py').read_text(encoding='utf-8')
        self.assertIn("final_list = [x for x in ranked if x.get('type') == 'news'][:10]", text)
        self.assertIn("title_en.lower().startswith('the download:')", text)
        self.assertIn("NOISY_NEWS_SOURCES", text)

    def test_generate_news_pages_no_marketing_fallback(self):
        text = (SCRIPTS / 'generate_news_pages.py').read_text(encoding='utf-8')
        self.assertNotIn('站内页优先帮你快速抓住核心变化与影响', text)
        self.assertIn("return f'{title_zh}。来源：{source}。'", text)

    def test_generate_news_pages_filters_bad_download_translation(self):
        text = (SCRIPTS / 'generate_news_pages.py').read_text(encoding='utf-8')
        self.assertIn("'下载：介绍自然问题'", text)
        self.assertIn("'下载：介绍目前人工智能中最重要的 10 件事'", text)
        self.assertIn("title_en.lower().startswith('the download:')", text)

if __name__ == '__main__':
    unittest.main()
