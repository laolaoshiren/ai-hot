import unittest
from pathlib import Path

ROOT = Path('/root/ai-hot')
LIST_TMPL = ROOT / 'site' / 'layouts' / '_default' / 'list.html'
SINGLE_TMPL = ROOT / 'site' / 'layouts' / 'news' / 'single.html'


class NewsPageRegressionTests(unittest.TestCase):
    def test_news_single_does_not_depend_on_site_data_lookup(self):
        text = SINGLE_TMPL.read_text(encoding='utf-8')
        self.assertNotIn('index (where $articles "id" $articleId) 0', text)
        self.assertNotIn('if not $article', text)

    def test_news_list_persists_page_number_in_url(self):
        text = LIST_TMPL.read_text(encoding='utf-8')
        self.assertIn('params.set(\'p\'', text)
        self.assertIn('history.replaceState', text)
        self.assertIn('/?p={{ add (div $index 10) 1 }}', text)


if __name__ == '__main__':
    unittest.main()
