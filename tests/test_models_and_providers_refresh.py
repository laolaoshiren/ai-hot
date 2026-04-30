import unittest

from scripts.generate_curated_models import (
    archive_superseded_openrouter_specs,
    build_auto_discovery_specs,
    materialize_latest_specs,
    merge_curated_items,
    provider_label_from_model,
    resolve_latest_openrouter_id,
)
from scripts.openrouter_providers import PROVIDER_PREFIX_MAP, infer_provider_candidates, merge_provider_records


class ModelsAndProvidersRefreshTests(unittest.TestCase):
    def test_provider_prefix_map_includes_xiaomi(self):
        self.assertIn('xiaomi', PROVIDER_PREFIX_MAP)
        self.assertIn('xiaomi', PROVIDER_PREFIX_MAP['xiaomi'])

    def test_infer_provider_candidates_detects_xiaomi_mimo(self):
        models = [
            {'id': 'xiaomi/mimo-7b', 'name': 'Xiaomi: MiMo 7B', 'created': 1713744000},
            {'id': 'xiaomi/mimo-32b', 'name': 'Xiaomi: MiMo 32B', 'created': 1713830400},
        ]
        inferred = infer_provider_candidates(models)
        merged = merge_provider_records([], inferred)
        self.assertTrue(any(x['id'] == 'xiaomi' for x in merged))
        xiaomi = next(x for x in merged if x['id'] == 'xiaomi')
        self.assertEqual(xiaomi['latest_models'][0], 'MiMo 32B')
        self.assertGreaterEqual(xiaomi['model_count'], 2)

    def test_build_auto_discovery_specs_adds_hot_xiaomi_model(self):
        openrouter_map = {
            'xiaomi/mimo-7b': {
                'id': 'xiaomi/mimo-7b',
                'name': 'Xiaomi: MiMo 7B',
                'created': 1713744000,
                'context_length': 131072,
                'architecture': {'input_modalities': ['text'], 'output_modalities': ['text']},
                'top_provider': {'is_moderated': True}
            },
            'xiaomi/mimo-32b': {
                'id': 'xiaomi/mimo-32b',
                'name': 'Xiaomi: MiMo 32B',
                'created': 1713830400,
                'context_length': 1048576,
                'architecture': {'input_modalities': ['text'], 'output_modalities': ['text']},
                'top_provider': {'is_moderated': True}
            },
        }
        specs = build_auto_discovery_specs(openrouter_map)
        self.assertTrue(any(x['id'] == 'xiaomi/mimo-32b' for x in specs))
        mimo = next(x for x in specs if x['id'] == 'xiaomi/mimo-32b')
        self.assertIn(mimo['category'], {'top', 'watch', 'coding'})

    def test_merge_curated_items_deduplicates_manual_and_auto_specs(self):
        base = [{'category': 'watch', 'source': 'openrouter', 'id': 'xiaomi/mimo-32b', 'label': '手工补充', 'why': '老描述'}]
        auto = [{'category': 'top', 'source': 'openrouter', 'id': 'xiaomi/mimo-32b', 'label': '自动发现', 'why': '新描述'}]
        merged = merge_curated_items(base, auto)
        items = [x for x in merged if x.get('id') == 'xiaomi/mimo-32b']
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]['label'], '手工补充')

    def test_provider_label_from_model_handles_xiaomi(self):
        model = {'id': 'xiaomi/mimo-32b', 'name': 'Xiaomi: MiMo 32B'}
        self.assertEqual(provider_label_from_model(model), 'Xiaomi')

    def test_openrouter_latest_resolves_newest_gpt_family(self):
        openrouter_map = {
            'openai/gpt-5.4': {'id': 'openai/gpt-5.4', 'name': 'OpenAI: GPT-5.4', 'created': 100},
            'openai/gpt-5.5': {'id': 'openai/gpt-5.5', 'name': 'OpenAI: GPT-5.5', 'created': 200},
            'openai/gpt-5.5-pro': {'id': 'openai/gpt-5.5-pro', 'name': 'OpenAI: GPT-5.5 Pro', 'created': 210},
            'openai/gpt-5.5-mini': {'id': 'openai/gpt-5.5-mini', 'name': 'OpenAI: GPT-5.5 Mini', 'created': 300},
        }
        self.assertEqual(resolve_latest_openrouter_id(openrouter_map, 'openai', 'gpt', 'base'), 'openai/gpt-5.5')
        self.assertEqual(resolve_latest_openrouter_id(openrouter_map, 'openai', 'gpt', 'pro'), 'openai/gpt-5.5-pro')

    def test_archive_superseded_openai_gpt_models(self):
        openrouter_map = {
            'openai/gpt-5.4': {'id': 'openai/gpt-5.4', 'name': 'OpenAI: GPT-5.4', 'created': 100},
            'openai/gpt-5.5': {'id': 'openai/gpt-5.5', 'name': 'OpenAI: GPT-5.5', 'created': 200},
            'openai/gpt-5.4-pro': {'id': 'openai/gpt-5.4-pro', 'name': 'OpenAI: GPT-5.4 Pro', 'created': 110},
            'openai/gpt-5.5-pro': {'id': 'openai/gpt-5.5-pro', 'name': 'OpenAI: GPT-5.5 Pro', 'created': 210},
        }
        specs = [
            {'category': 'top', 'source': 'openrouter', 'id': 'openai/gpt-5.4'},
            {'category': 'top', 'source': 'openrouter', 'id': 'openai/gpt-5.5'},
            {'category': 'coding', 'source': 'openrouter', 'id': 'openai/gpt-5.4-pro'},
            {'category': 'coding', 'source': 'openrouter', 'id': 'openai/gpt-5.5-pro'},
        ]
        kept = archive_superseded_openrouter_specs(specs, openrouter_map)
        kept_ids = {x['id'] for x in kept}
        self.assertIn('openai/gpt-5.5', kept_ids)
        self.assertIn('openai/gpt-5.5-pro', kept_ids)
        self.assertNotIn('openai/gpt-5.4', kept_ids)
        self.assertNotIn('openai/gpt-5.4-pro', kept_ids)

    def test_materialize_latest_specs_replaces_placeholder(self):
        openrouter_map = {
            'openai/gpt-5.4': {'id': 'openai/gpt-5.4', 'name': 'OpenAI: GPT-5.4', 'created': 100},
            'openai/gpt-5.5': {'id': 'openai/gpt-5.5', 'name': 'OpenAI: GPT-5.5', 'created': 200},
        }
        specs = [{'category': 'top', 'source': 'openrouter-latest', 'provider_prefix': 'openai', 'family': 'gpt', 'variant': 'base', 'label': '综合王者', 'why': '最新'}]
        resolved = materialize_latest_specs(specs, openrouter_map)
        self.assertEqual(resolved[0]['source'], 'openrouter')
        self.assertEqual(resolved[0]['id'], 'openai/gpt-5.5')


if __name__ == '__main__':
    unittest.main()
