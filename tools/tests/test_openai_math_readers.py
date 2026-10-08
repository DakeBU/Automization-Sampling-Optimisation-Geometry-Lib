"""A source reader must never masquerade as local Lean admission."""
import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "website" / "scripts"))
import openai_math_intake as intake


class OpenAIMathReaderTests(unittest.TestCase):
    def setUp(self):
        self.model = intake._load()
        self.item = next(item for item in self.model["items"] if item["id"] == "oai-logconcave")

    def test_reuses_existing_mapping(self):
        self.assertEqual(len(self.model["libraries"]), 7)
        self.assertEqual(len(self.model["items"]), 32)
        self.assertEqual(self.item["reader"]["status"], "source-reading-draft")
        self.assertEqual(self.item["declarations"], ["OAI.LogConcaveSampling.exact_source_main"])

    def test_hierarchy_and_adjacent_closed_lean(self):
        html = intake._reader_page(self.item, self.model)
        for marker in ('id="result"', 'id="contribution"', 'id="proof-route"', 'id="verification"'):
            self.assertIn(marker, html)
        self.assertIn('data-local-proof-status="external-reference"', html)
        self.assertNotIn('data-status="compiled"', html)
        self.assertNotIn('<details open', html)
        self.assertLess(html.index('Read the upstream Lean statement'), html.index('id="contribution"'))
        self.assertIn('Read the upstream assembly proof', html)
        self.assertIn('\\[', html)
        self.assertNotIn('D:\\', html)

    def test_no_local_status_promotion(self):
        item = copy.deepcopy(self.item)
        item["reader"]["status"] = "compiled"
        with self.assertRaisesRegex(RuntimeError, "cannot certify"):
            intake._validate_reader(item)

    def test_review_scope_and_tex_blob_links(self):
        item = copy.deepcopy(self.item)
        item["reader"]["review"] = {}
        with self.assertRaisesRegex(RuntimeError, "bounded evidence"):
            intake._validate_reader(item)
        source = self.item["reader"]["source_path"]
        self.assertIn("/blob/", intake._upstream_url(self.model["upstream"]["commit"], source))
        self.assertIn("/tree/", intake._upstream_url(self.model["upstream"]["commit"], self.item["upstream_paths"][0]))

    def test_unsafe_path_and_unpinned_source_rejected(self):
        for key, value in (("path", "../escape.html"), ("source_blob_sha", "main")):
            item = copy.deepcopy(self.item)
            item["reader"][key] = value
            with self.assertRaises(RuntimeError):
                intake._validate_reader(item)

    def test_unique_steps_and_real_boundaries(self):
        item = copy.deepcopy(self.item)
        item["reader"]["steps"][1]["id"] = item["reader"]["steps"][0]["id"]
        with self.assertRaisesRegex(RuntimeError, "unique"):
            intake._validate_reader(item)
        item = copy.deepcopy(self.item)
        item["reader"]["steps"][0]["boundary"] = ""
        with self.assertRaisesRegex(RuntimeError, "incomplete"):
            intake._validate_reader(item)


if __name__ == "__main__":
    unittest.main()
