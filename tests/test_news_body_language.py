import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import news_article_enhance
from scripts.generate_news_pages import GENERATED_MARKER, build_page, sanitize_legacy_english_page
from scripts.quality_gate import news_content_fingerprint, recent_translation_problem


def generated_body(page: str) -> str:
    return page.split(GENERATED_MARKER.strip(), 1)[1].split('## 🔗 原始来源', 1)[0].strip()


class NewsBodyLanguageTests(unittest.TestCase):
    def test_english_source_never_falls_back_to_english_excerpt(self):
        english_excerpt = 'OpenAI released a new model with a longer context window and lower latency.'
        page = build_page({
            'id': 'english-fallback',
            'title': 'OpenAI releases a new model',
            'title_zh': 'OpenAI 发布新模型',
            'source': 'Example News',
            'lang': 'en',
            'ai_summary': '新模型拥有更长的上下文窗口，并降低了响应延迟。',
            'summary_zh': '新模型拥有更长的上下文窗口，并降低了响应延迟。',
            'content_excerpt': english_excerpt,
        })

        body = generated_body(page)
        self.assertNotIn(english_excerpt, body)
        self.assertIn('新模型拥有更长的上下文窗口', body)

    def test_translation_failure_uses_chinese_fallback(self):
        english_excerpt = 'This English article body must stay out of the generated page.'
        english_summary = 'This summary also remained English because translation failed.'
        page = build_page({
            'id': 'translation-failed',
            'title': 'An English source title',
            'title_zh': '英文来源文章的中文标题',
            'source': 'Example News',
            'lang': 'en',
            'ai_summary': english_summary,
            'summary_zh': english_summary,
            'content_excerpt': english_excerpt,
        })

        body = generated_body(page)
        self.assertNotIn(english_excerpt, body)
        self.assertNotIn(english_summary, body)
        self.assertIn('英文来源文章的中文标题', body)

    def test_english_source_prefers_translated_body(self):
        english_excerpt = 'The original article body must not be rendered.'
        chinese_body = '这是一段已经翻译完成的中文正文。\n它保留了文章的主要事实和上下文。'
        page = build_page({
            'id': 'translated-body',
            'title': 'An English title',
            'title_zh': '一个中文标题',
            'source': 'Example News',
            'lang': 'en',
            'summary_zh': '这是一条中文摘要。',
            'rewrite_body': english_excerpt,
            'content_zh': chinese_body,
            'content_excerpt': english_excerpt,
        })

        body = generated_body(page)
        self.assertIn('这是一段已经翻译完成的中文正文。', body)
        self.assertIn('它保留了文章的主要事实和上下文。', body)
        self.assertNotIn(english_excerpt, body)

    def test_enhancer_skips_completed_item_and_translates_next_pending_body(self):
        completed_source = 'The completed English article already has a translated body.'
        pending_source = 'The pending English article needs its body translated into Chinese.'
        items = [
            {
                'id': 'complete',
                'lang': 'en',
                'title': 'Complete',
                'title_zh': '已完成标题',
                'summary': 'Complete summary',
                'summary_zh': '已完成摘要',
                'ai_summary': '这是一条已完成的中文摘要',
                'content_text': completed_source,
                'content_zh': '这是一段已经完成翻译的中文正文。',
                'content_zh_source_hash': news_article_enhance.content_fingerprint(completed_source),
            },
            {
                'id': 'pending',
                'lang': 'en',
                'title': 'Pending',
                'title_zh': '待处理标题',
                'summary': 'Pending summary',
                'summary_zh': '待处理摘要',
                'ai_summary': '这是一条待处理的中文摘要',
                'content_text': pending_source,
            },
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            news_path = Path(tmpdir) / 'news.json'
            news_path.write_text(json.dumps(items, ensure_ascii=False), encoding='utf-8')
            with patch.object(news_article_enhance, 'NEWS_PATH', news_path), patch.object(
                news_article_enhance,
                'translate',
                return_value='这是翻译后的中文正文，包含文章的主要信息。',
            ) as translate_mock:
                result = news_article_enhance.enhance_news(limit=1)

            updated = json.loads(news_path.read_text(encoding='utf-8'))

        self.assertEqual(updated[0]['content_zh'], '这是一段已经完成翻译的中文正文。')
        self.assertEqual(updated[1]['content_zh'], '这是翻译后的中文正文，包含文章的主要信息。')
        self.assertEqual(translate_mock.call_count, 1)
        self.assertIn('翻译正文 1 条', result)

    def test_enhancer_skips_failed_item_during_retry_cooldown(self):
        items = []
        for item_id in ('deferred', 'ready'):
            items.append({
                'id': item_id,
                'lang': 'en',
                'title': item_id.title(),
                'title_zh': f'{item_id} 的中文标题',
                'summary': 'English summary',
                'summary_zh': '这是一条中文摘要',
                'ai_summary': '这是一条可用的中文摘要',
                'content_text': f'The {item_id} article needs a Chinese body.',
            })
        items[0]['translation_error'] = '正文: timeout'
        items[0]['translation_retry_after'] = '2999-01-01T00:00:00+00:00'

        with tempfile.TemporaryDirectory() as tmpdir:
            news_path = Path(tmpdir) / 'news.json'
            news_path.write_text(json.dumps(items, ensure_ascii=False), encoding='utf-8')
            with patch.object(news_article_enhance, 'NEWS_PATH', news_path), patch.object(
                news_article_enhance,
                'translate',
                return_value='这是翻译后的中文正文，包含文章的完整信息。',
            ) as translate_mock:
                news_article_enhance.enhance_news(limit=1)
            updated = json.loads(news_path.read_text(encoding='utf-8'))

        self.assertNotIn('content_zh', updated[0])
        self.assertIn('content_zh', updated[1])
        self.assertEqual(translate_mock.call_count, 1)

    def test_enhancer_persists_cooldown_before_reporting_failure(self):
        item = {
            'id': 'failed',
            'lang': 'en',
            'title': 'Failed article',
            'title_zh': '翻译失败的文章',
            'summary': 'English summary',
            'summary_zh': '这是一条中文摘要',
            'ai_summary': '这是一条可用的中文摘要',
            'content_text': 'The translation service keeps returning the original English article body.',
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            news_path = Path(tmpdir) / 'news.json'
            news_path.write_text(json.dumps([item], ensure_ascii=False), encoding='utf-8')
            with patch.object(news_article_enhance, 'NEWS_PATH', news_path), patch.object(
                news_article_enhance,
                'translate',
                return_value='The untranslated English response.',
            ), patch.object(news_article_enhance.time, 'sleep'):
                with self.assertRaises(RuntimeError):
                    news_article_enhance.enhance_news(limit=1)
            updated = json.loads(news_path.read_text(encoding='utf-8'))[0]

        self.assertIn('translation_retry_after', updated)
        self.assertIn('正文翻译失败', updated['translation_error'])
        self.assertNotIn('content_zh', updated)

    def test_long_body_translation_is_chunked(self):
        source = ('This sentence contains enough text to require another translation chunk. ' * 8).strip()
        calls = []

        def fake_translate(chunk):
            calls.append(chunk)
            return '这是对应分块的中文翻译结果。'

        with patch.object(news_article_enhance, 'translate', side_effect=fake_translate):
            result = news_article_enhance.translate_content(source, max_chars=120, retries=1)

        self.assertGreater(len(calls), 1)
        self.assertTrue(all(len(chunk) <= 120 for chunk in calls))
        self.assertIn('中文翻译结果', result)

    def test_non_chinese_translation_result_is_retried(self):
        with patch.object(
            news_article_enhance,
            'translate',
            side_effect=['The service returned the source text.', '这是第二次请求返回的中文正文。'],
        ) as translate_mock:
            result = news_article_enhance.translate_content(
                'The source article needs translation.',
                max_chars=120,
                retries=2,
            )

        self.assertEqual(translate_mock.call_count, 2)
        self.assertIn('第二次请求返回的中文正文', result)

    def test_recent_translation_guard_rejects_stale_or_short_body(self):
        source = 'The source article contains enough original text for a translated article body.'
        translated = '这是完整的中文翻译正文，包含来源文章中的主要事实和上下文。' * 6
        item = {
            'content_excerpt': source,
            'content_zh': translated,
            'content_zh_chars': len(translated),
            'content_zh_source_hash': news_content_fingerprint(source),
        }
        self.assertEqual(recent_translation_problem(item), '')

        item['content_zh_source_hash'] = 'stale'
        self.assertIn('hash stale', recent_translation_problem(item))

        item['content_zh_source_hash'] = news_content_fingerprint(source)
        item['content_zh'] = '中文太短'
        self.assertIn('too short', recent_translation_problem(item))

    def test_orphaned_legacy_english_page_is_sanitized(self):
        english_body = 'This orphaned generated page still contains its old English article body.'
        page = build_page({
            'id': 'legacy-orphan',
            'title': 'Legacy English title',
            'title_zh': '历史文章的中文标题',
            'source': 'Example News',
            'lang': 'en',
            'summary_zh': '这是一条历史文章的中文摘要。',
        })
        before, after = page.split(GENERATED_MARKER.strip(), 1)
        _, source_section = after.split('## 🔗 原始来源', 1)
        legacy_page = (
            f'{before}{GENERATED_MARKER.strip()}\n\n{english_body}\n\n'
            f'## 🔗 原始来源{source_section}'
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / 'legacy-orphan.md'
            path.write_text(legacy_page, encoding='utf-8')
            changed = sanitize_legacy_english_page(path)
            updated = path.read_text(encoding='utf-8')

        self.assertTrue(changed)
        self.assertNotIn(english_body, generated_body(updated))
        self.assertIn('历史文章的中文摘要', generated_body(updated))


if __name__ == '__main__':
    unittest.main()
