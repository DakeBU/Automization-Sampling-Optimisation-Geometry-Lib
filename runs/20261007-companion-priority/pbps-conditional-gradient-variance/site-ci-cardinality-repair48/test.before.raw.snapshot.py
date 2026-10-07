"""Source contracts and graph separation; these tests do not prove mathematics."""
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT/'tools'), str(ROOT/'website/scripts')]
import samplewiki_companions as companion
import research_workspace
import cross_domain
from underlying_lean_graph_model import GraphBuilder


class CompanionTests(unittest.TestCase):
    def test_valid_model_and_existing_graph(self):
        companion.validate_data()
        cross_domain.validate_data()

    def test_three_sources_keep_the_two_paper_composition_separate(self):
        m=companion.load()
        self.assertEqual(len(m['sources']),3)
        self.assertEqual(len(m['cases']),3)
        self.assertEqual(set(m['composition']['source_ids']),{'sphmc-2026','pbps-2026'})
        cloud=next(row for row in m['cases'] if row['id']=='ASTIS-SW-GAUSSIAN-CLOUD-2026')
        self.assertEqual(cloud['source_ids'],['gaussian-cloud-2026'])
        self.assertIn('bookkeeping',cloud)
        snapshot=json.loads((ROOT/'research-wiki/source-index/SampleWiki_cases.json').read_text(encoding='utf8'))
        self.assertEqual(len(snapshot['cases']),34)
        active=json.loads((ROOT/'website/content/samplewiki_reader.json').read_text(encoding='utf8'))
        self.assertEqual(active['active_case_id'],'ASTIS-SW-SETTING-LOG-CONCAVE-SMOOTH-UPPER-IDEAL-PROXIMAL-CHAIN')

    def test_new_cards_cannot_turn_blue(self):
        m=companion.load(); m['cases'][0]['status']='compiled'
        with self.assertRaisesRegex(ValueError,'remain planned'):
            companion.validate_data(m)

    def test_candidate_modules_must_exist(self):
        m=companion.load(); m['technologies'][0]['search_modules']=['AutoSamplingTheory.DoesNotExist']
        with self.assertRaisesRegex(ValueError,'Invented Lean'):
            companion.validate_data(m)

    def test_unknown_parent_and_cycles_rejected(self):
        m=companion.load(); m['technologies'][0]['parents']=['tech:missing']
        with self.assertRaisesRegex(ValueError,'Unknown technology parent'):
            companion.validate_data(m)
        m=companion.load(); m['technologies'][0]['parents']=['tech:picard-integrator']
        with self.assertRaisesRegex(ValueError,'Cyclic'):
            companion.validate_data(m)

    def test_proxy_and_oracle_distinctions_are_preserved(self):
        m=companion.load()
        w2,proxy=m['cases'][0]['theorems']
        self.assertIn('prox',w2['formula'])
        self.assertIn('dagger',proxy['formula'])
        self.assertIn('Only the proxy',proxy['boundary'])
        self.assertIn('TV proximity alone cannot',m['composition']['theorems'][0]['steps'][-1]['text'])
        pbps=next(row for row in m['cases'] if row['id']=='ASTIS-SW-PBPS-2026')['theorems'][0]
        self.assertIn('discrete augmented',pbps['boundary'])

    def test_every_theorem_has_adjacent_closed_lean_folds(self):
        m=companion.load()
        for row in [*m['cases'],m['composition']]:
            for theorem in row['theorems']:
                text=companion.theorem_html(m,row,theorem)
                self.assertEqual(text.count('<details '),2+len(theorem['steps']))
                self.assertNotIn('<details open',text)
                self.assertLess(text.index('Lean statement'),text.index('Proof architecture and calculations'))
                self.assertLess(text.index('Lean proof'),text.index('Strict boundary'))

    def test_overlay_does_not_create_compiler_edges(self):
        b=GraphBuilder(); counts=companion.add_to_graph(b)
        self.assertEqual(counts,{'source_cases':3,'composition_views':1,'technology_candidates':12})
        self.assertEqual(len(b.nodes),19)
        self.assertFalse(any(n.get('status')=='compiled' for n in b.nodes.values()))
        formal={'imports','declares','depends-on','closes leaf'}
        self.assertFalse(any(e['relation'] in formal for e in b.edges.values()))
        self.assertEqual(sum(n['id']=='tech:rgo-calculus' for n in b.nodes.values()),1)

    def test_lineage_does_not_credit_all_hypocoercivity_to_pbps(self):
        d=json.loads(companion.DELTAS.read_text(encoding='utf8'))
        self.assertEqual(len(d['lineage']),3)
        self.assertIn('Jianfeng Lu',d['lineage'][1]['label'])
        self.assertIn('idealized',d['deltas'][3]['boundary'])
        self.assertIn('centered',d['operator_walkthrough'][2]['text'])

    def test_svg_is_accessible_and_has_no_blue_proof_claim(self):
        m=companion.load(); svg=companion.topology_svg(m)
        self.assertIn('aria-labelledby',svg)
        self.assertIn('not compiler dependency',svg)
        self.assertIn('#ba3535',svg)
        self.assertIn('Picard HMC Part I',svg)
        ledger=companion.gaussian_cloud_ledger_svg()
        self.assertIn('two ledgers',ledger)
        self.assertIn('εcap',ledger)
        d=json.loads(companion.DELTAS.read_text(encoding='utf8'))
        svg=companion.proof_delta_svg(d)
        self.assertIn('Fan–Li–Lu',svg)
        self.assertEqual(svg.count('<g id='),5)

    def test_research_workspace_is_a_projection_not_a_second_status_source(self):
        model = companion.load()
        payload = research_workspace.build_payload(model)
        self.assertEqual(payload['generated_from'], 'website/content/samplewiki_companion_frontiers.json')
        self.assertEqual(
            {row['id'] for row in payload['workspaces']},
            {row['id'] for row in model['cases']},
        )
        cloud = next(
            row for row in payload['workspaces']
            if row['id'] == 'ASTIS-SW-GAUSSIAN-CLOUD-2026'
        )
        self.assertEqual(cloud['status'], 'planned')
        self.assertIn('ledger', cloud)
        tv = next(row for row in cloud['theorems'] if row['id'] == 'gaussian-cloud-tv-ledger')
        suffix = next(row for row in tv['steps'] if 'data processing' in row['title'].lower())
        self.assertEqual(suffix['status'], 'compiled-support-only')
        self.assertTrue(suffix['compiled_support'])
        text = research_workspace.workspace_markdown(cloud)
        self.assertIn('AI explanations and generated Lean are unverified', text)
        self.assertEqual(
            cloud['evidence_contract']['source_fidelity'],
            'independent-review-required',
        )

    def test_news_short_and_oldest_is_foundation(self):
        readme=(ROOT/'README.md').read_text(encoding='utf8')
        news=readme.split('## News\n',1)[1].split('\n## ',1)[0]
        lines=[line for line in news.splitlines() if line.strip()]
        self.assertTrue(all(line.startswith('- **2026-') for line in lines))
        self.assertLessEqual(len(lines),8)
        self.assertIn('Established Auto-Sampling-Theory-In-Sleep.',lines[-1])


if __name__=='__main__':
    unittest.main()
