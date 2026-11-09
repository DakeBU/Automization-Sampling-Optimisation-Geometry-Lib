"""The topic reader reuses canonical nodes and never admits a pending proof."""
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "tools"), str(ROOT / "website/scripts")]
import lower_bounds as reader


class LowerBoundsTests(unittest.TestCase):
    def setUp(self):
        self.name = "Samplinglib.Existing.result"
        self.node = "decl:" + self.name
        self.lesson = reader.declaration_lessons.lesson_path(self.name)
        self.binding = {"declaration": self.name, "audit_id": "review", "role": "proof-edge"}
        self.items = {"result": {"title": "Component", "bindings": [self.binding],
                                 "source": {"url": "https://example.test/source"}}}
        self.data = {"audits": {"review": {"state": "source-reviewed",
                    "source_review": {"state": "accepted"}, "lean": {"compiled": True},
                    "publication_binding_sha256": "current"}}}
        self.nodes = {self.node: {"url": self.lesson}}
        for name, result in (("verified_binding", True), ("binding_digest", "current")):
            fake = patch.object(reader.publication, name, return_value=result)
            fake.start()
            self.addCleanup(fake.stop)

    def test_reuse_existing_identity_and_authored_reader(self):
        rows = reader.reviewed_readings(("result", "result"), self.items, self.data, self.nodes)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["node"], self.node)
        self.assertEqual(rows[0]["lesson"], self.lesson)
        query = parse_qs(urlparse(reader.graph_path(self.node)).query)
        self.assertEqual(query, {"view": ["lean"], "focus": [self.node], "q": [self.name]})

    def test_pending_stale_and_absent_publications_receive_no_credit(self):
        self.assertEqual(reader.reviewed_readings(("not-merged",), self.items, self.data, self.nodes), [])
        audit = self.data["audits"]["review"]
        audit["publication_binding_sha256"] = "stale"
        self.assertEqual(reader.reviewed_readings(("result",), self.items, self.data, self.nodes), [])
        audit["publication_binding_sha256"] = "current"
        audit["source_review"]["state"] = "pending"
        self.assertEqual(reader.reviewed_readings(("result",), self.items, self.data, self.nodes), [])

    def test_missing_graph_identity_is_an_error(self):
        with self.assertRaisesRegex(ValueError, "canonical graph-to-lesson"):
            reader.reviewed_readings(("result",), self.items, self.data, {})

    def test_reader_uses_source_cases_and_separates_scopes(self):
        text = reader.render(reader.samplewiki_companions.load(), {}, {"audits": {}}, {})
        self.assertIn("companions/midpoint-langevin.html", text)
        self.assertIn("companions/gaussian-sampling-complexity.html", text)
        self.assertIn("chapter-04.html", text)
        self.assertIn("not a lower bound over all randomized oracles", text)
        self.assertIn("not a proved reduction", text)
        self.assertIn(r"\varepsilon", text)

    def test_algorithm_and_oracle_questions_have_distinct_hierarchies(self):
        text = reader.render(reader.samplewiki_companions.load(), {}, {"audits": {}}, {})
        method = text.split('<section id="algorithm-specific">', 1)[1].split('<section id="general">', 1)[0]
        general = text.split('<section id="general">', 1)[1].split('<section id="connections">', 1)[0]
        for anchor in ('mala', 'hmc', 'midpoint', 'method-sharpness'):
            self.assertIn(f'<details id="{anchor}">', method)
            self.assertNotIn(f'id="{anchor}"', general)
        for anchor in ('optimisation', 'gaussian', 'nonlinear'):
            self.assertIn(f'<details id="{anchor}">', general)
        self.assertIn('not every possible computational model', general)
        self.assertNotIn('<details open', text)

    def test_cross_subject_links_do_not_claim_new_lean_edges(self):
        text = reader.render(reader.samplewiki_companions.load(), {}, {"audits": {}}, {})
        for node in ('method:mala', 'method:hmc'):
            self.assertIn(reader.graph_path(node, 'perspectives').replace('&', '&amp;'), text)
        self.assertIn('proofs/random-scan-reversibility.html', text)
        self.assertIn('not certified reductions or new Functor edges', text)
        self.assertIn('no formal proof edges or completion credit', text)
        self.assertIn(reader.METROPOLIZED_SOURCE, text)
        self.assertIn(reader.WARM_MALA_SOURCE, text)
        self.assertEqual(reader.METHOD_CONTEXTS['textbook/chapter-07/section-7-6.html'][0], 'mala')


if __name__ == "__main__":
    unittest.main()
