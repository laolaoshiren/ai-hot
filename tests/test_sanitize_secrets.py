import tempfile
import unittest
from pathlib import Path

from scripts.sanitize_secrets import sanitize_files, sanitize_text

# Built by concatenation so this source file never contains a full
# token-shaped literal -- otherwise GitHub Push Protection blocks pushes.
HF_TOKEN = "hf_" + "oCfFIJsV" + "dYHmydnCHMExjTYiNVD" + "CzMtqKF"
GHP_TOKEN = "ghp_" + "aBcDeFgHiJkLmNoPqRsTuVwXyZ0123456789"


class SanitizeSecretsTests(unittest.TestCase):
    def test_sanitize_text_redacts_huggingface_token(self):
        clean, counts = sanitize_text("token: " + HF_TOKEN)
        self.assertNotIn("hf_", clean)
        self.assertIn("[REDACTED]", clean)
        self.assertEqual(counts, {"huggingface_token": 1})

    def test_sanitize_text_redacts_github_and_aws_tokens(self):
        text = GHP_TOKEN + " and AKIA" + "1234567890123456"
        clean, counts = sanitize_text(text)
        self.assertNotIn("ghp_", clean)
        self.assertNotIn("AKIA", clean)
        self.assertEqual(counts["github_token"], 1)
        self.assertEqual(counts["aws_access_key"], 1)

    def test_sanitize_text_keeps_normal_urls_and_words(self):
        text = "see https://huggingface.co/blog and the sk-learn pipeline docs"
        clean, counts = sanitize_text(text)
        self.assertEqual(clean, text)
        self.assertEqual(counts, {})

    def test_sanitize_files_rewrites_only_dirty_files_in_temp_tree(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            dirty = root / "data" / "news.json"
            dirty.parent.mkdir(parents=True)
            dirty.write_text('{"text": "' + HF_TOKEN + '"}', encoding="utf-8")
            clean_file = root / "site" / "content" / "news" / "ok.md"
            clean_file.parent.mkdir(parents=True)
            clean_file.write_text("normal content, no secrets", encoding="utf-8")

            changed, totals = sanitize_files(fix=True, root=root)

            self.assertEqual([dirty], changed)
            self.assertEqual(totals, {"huggingface_token": 1})
            self.assertNotIn("hf_", dirty.read_text(encoding="utf-8"))
            self.assertEqual(clean_file.read_text(encoding="utf-8"), "normal content, no secrets")

            changed_again, totals_again = sanitize_files(fix=False, root=root)
            self.assertEqual(changed_again, [])
            self.assertEqual(totals_again, {})

    def test_sanitize_files_check_mode_does_not_modify(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            dirty = root / "data" / "x.json"
            dirty.parent.mkdir(parents=True)
            original = '{"k": "' + GHP_TOKEN + '"}'
            dirty.write_text(original, encoding="utf-8")

            changed, totals = sanitize_files(fix=False, root=root)

            self.assertEqual(len(changed), 1)
            self.assertEqual(dirty.read_text(encoding="utf-8"), original)
            self.assertEqual(totals, {"github_token": 1})


if __name__ == "__main__":
    unittest.main()
