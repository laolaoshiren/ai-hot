import unittest

from scripts.generate_rising import (
    build_rising_candidates,
    choose_window_days,
    score_github_candidate,
    score_model_candidate,
)


class GenerateRisingTests(unittest.TestCase):
    def test_choose_window_days_prefers_requested_when_enough_candidates(self):
        candidates = [
            {"name": f"item-{i}", "window_days": 7, "score": 100 - i}
            for i in range(6)
        ] + [
            {"name": "item-older", "window_days": 14, "score": 50}
        ]

        self.assertEqual(choose_window_days(candidates, preferred_days=7, minimum_count=5), 7)

    def test_choose_window_days_falls_back_when_requested_window_too_sparse(self):
        candidates = [
            {"name": "recent-1", "window_days": 7, "score": 100},
            {"name": "recent-2", "window_days": 7, "score": 95},
            {"name": "older-1", "window_days": 14, "score": 90},
            {"name": "older-2", "window_days": 14, "score": 85},
            {"name": "older-3", "window_days": 14, "score": 80},
            {"name": "older-4", "window_days": 14, "score": 75},
        ]

        self.assertEqual(choose_window_days(candidates, preferred_days=7, minimum_count=5), 14)

    def test_score_github_candidate_rewards_recent_high_star_growth(self):
        fast = {
            "stars": 7000,
            "created_at": "2026-04-20T00:00:00Z",
            "window_days": 7,
        }
        slow = {
            "stars": 7000,
            "created_at": "2026-04-01T00:00:00Z",
            "window_days": 21,
        }

        self.assertGreater(score_github_candidate(fast), score_github_candidate(slow))

    def test_score_model_candidate_rewards_fresh_models_with_heat_signals(self):
        stronger = {
            "created_at": "2026-04-21T00:00:00Z",
            "window_days": 7,
            "likes": 3000,
            "downloads": 200000,
            "openrouter_available": True,
        }
        weaker = {
            "created_at": "2026-04-10T00:00:00Z",
            "window_days": 14,
            "likes": 100,
            "downloads": 1000,
            "openrouter_available": False,
        }

        self.assertGreater(score_model_candidate(stronger), score_model_candidate(weaker))

    def test_build_rising_candidates_mixes_types_and_limits_output(self):
        projects = [
            {
                "id": "p1",
                "display_name": "OpenHands",
                "name": "All-Hands-AI/OpenHands",
                "url": "https://github.com/All-Hands-AI/OpenHands",
                "description": "AI dev agent",
                "stars": 52000,
                "created_at": "2026-04-20T00:00:00Z",
                "collected_at": "2026-04-22T12:00:00",
            }
        ]
        tools = [
            {
                "id": "cursor",
                "name": "Cursor",
                "url": "https://cursor.sh",
                "description": "AI-first 代码编辑器",
                "stars": 12000,
                "github_url": "https://github.com/getcursor/cursor",
                "added_at": "2026-04-21T00:00:00Z",
            }
        ]
        agents = [
            {
                "id": "swe-agent",
                "name": "SWE-Agent",
                "url": "https://github.com/princeton-nlp/SWE-agent",
                "description": "软件工程 Agent",
                "stars": 19030,
                "created_at": "2026-03-19T00:00:00Z",
            }
        ]
        models = [
            {
                "id": "m1",
                "display_name": "Gemini 3.1 Pro Image",
                "name": "google/gemini-3.1-pro-image-preview",
                "url": "https://openrouter.ai/google/gemini-3.1-pro-image-preview",
                "created_at": "2026-04-21T00:00:00Z",
                "likes": 300,
                "downloads": 50000,
                "source": "openrouter",
                "provider": "Google"
            },
            {
                "id": "m2",
                "display_name": "FLUX.1 Kontext dev",
                "name": "black-forest-labs/FLUX.1-Kontext-dev",
                "url": "https://huggingface.co/black-forest-labs/FLUX.1-Kontext-dev",
                "created_at": "2026-04-20T00:00:00Z",
                "likes": 5000,
                "downloads": 100000,
                "source": "hf-text-to-image",
            },
        ]

        rising = build_rising_candidates(
            projects=projects,
            tools=tools,
            agents=agents,
            models=models,
            preferred_days=7,
            candidate_limit=10,
            display_limit=5,
            now_iso="2026-04-22T12:00:00+08:00",
        )

        self.assertEqual(rising["window_days"], 7)
        self.assertLessEqual(len(rising["items"]), 5)
        self.assertGreaterEqual(len(rising["items"]), 3)
        item_types = {item["type"] for item in rising["items"]}
        self.assertTrue(item_types.issubset({"project", "tool", "agent", "model"}))
        self.assertTrue({"project", "model", "agent"}.issubset(item_types))
        self.assertTrue(all(item["reason"] for item in rising["items"]))
        self.assertTrue(all("近7天" not in item["reason"] and "近30天" not in item["reason"] for item in rising["items"]))


if __name__ == "__main__":
    unittest.main()
