"""Reader structure and source boundaries; not mathematical proof credit."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / 'tools'), str(ROOT / 'website/scripts')]
import subject_readers as readers
import samplewiki_companions as papers
import samplewiki_navigation as navigation


class SubjectReaderTests(unittest.TestCase):
    def test_sampling_separates_books_research_and_methods(self):
        body = readers.sampling_body()
        for path in ('textbook/index.html', 'example-cases/samplewiki.html', readers.DISCRETE,
                     'libraries/mcmc/index.html', 'lower-bounds/index.html'):
            self.assertIn(path, body)
        self.assertNotIn('completed paper', body)
        self.assertIn('progress/index.html#samplewiki', body)
        self.assertNotIn('progress/index.html#samplewiki-route', body)

    def test_existing_discrete_proofs_not_duplicated_or_promoted(self):
        fake = [{'id':'random-scan-law','title':'Law','purpose':'Existing statement',
                 'evidence':{'compiled':False,'cell_status':'claimed','source_review':'pending'}}]
        html = readers.discrete_proofs(fake)
        self.assertIn('proofs/random-scan-law.html', html)
        self.assertIn('Compilation not certified', html)
        self.assertIn('pending', html)
        self.assertNotIn('Verified', html)
        self.assertNotIn('<code', html)

    def test_discrete_not_called_fast_mixing(self):
        body = readers.discrete_body([], '<h2>Canonical section inventory</h2>')
        self.assertIn('What is still needed for fast mixing?', body)
        self.assertIn('Reversibility alone', body)
        self.assertIn('Null conditioning fibers', body)
        self.assertIn('rate 1 per site', body)
        self.assertIn('Canonical section inventory', body)
        self.assertEqual(body.count('<h1'), 1)

    def test_new_paper_pin_and_no_scheduling_takeover(self):
        model = papers.load()
        papers.validate_data(model)
        source = model['sources']['slc-lsi-complexity-2026']
        self.assertEqual(source['version'], '2611.05813v1')
        self.assertEqual(source['sha256'], '05520f2a491fedc6ceecc7eb0f3d0c1b23275faceb9da1d9cfa6db421aab4f0e')
        self.assertEqual(len(navigation.priority_cases(model)), 4)
        case = next(c for c in model['cases'] if c['id']=='ASTIS-SW-SLC-LSI-COMPLEXITY-2026')
        self.assertEqual([t['id'] for t in case['theorems']], ['slc-cold-main','slc-warm-main','lsi-main'])
        self.assertEqual(case['status'],'planned')
        text = papers.comparison_html(case)
        self.assertIn('source-conditioning', text)
        self.assertNotIn('Residual Haar', text)
        for node in case['source_graph']['nodes']:
            self.assertEqual(node['status'], 'open')
        for t in case['theorems']:
            html = papers.theorem_html(model, case, t)
            self.assertIn('data-proof-status="planned"', html)
            self.assertIn('local proof open', html)


if __name__ == '__main__':
    unittest.main()
