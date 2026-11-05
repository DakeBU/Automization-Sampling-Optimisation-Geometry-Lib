from __future__ import annotations

import copy
import hashlib
import json
import re
import sys
import unittest
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
sys.path.insert(0, str(ROOT / 'website/scripts'))
import bench_portals
import reader_hierarchy


class BenchReaderHierarchyTests(unittest.TestCase):
    def test_three_collections_cover_seven_domains_without_partitioning_families(self):
        config = bench_portals.configuration()
        self.assertEqual(config['display_name'], 'Sampling-Optimisation-Geometry-Bench')
        self.assertEqual(len(config['collections']), 3)
        core = {'id': 'shared', 'family': 'unchanged-family', 'split': 'public-dev',
                'library_domains': ['riemannian-optimization']}
        original = copy.deepcopy(core)
        hits = [c['id'] for c in config['collections'] if bench_portals.members([core],c)]
        self.assertEqual(hits, ['optimisation','geometry'])
        self.assertEqual(core, original)

    def test_sidebar_has_visible_graph_doors_and_peer_bench_shelf(self):
        source = ('<aside><div class="sidebar-contents"><section class="sidebar-group sidebar-libraries">old</section>'
                  '<section data-context>Keep this source context</section></div>'
                  '<div class="sidebar-utility"><a data-sog-bench-nav href="old">QA Bench</a></div></aside>')
        text = reader_hierarchy.sidebar(source, 'textbook/chapter-01.html')
        self.assertLess(text.index('data-reader-graph-nav'), text.index('sidebar-libraries'))
        self.assertLess(text.index('sidebar-libraries'), text.index('sidebar-benches'))
        self.assertEqual(text.count('data-bench-collection='), 3)
        self.assertIn('Keep this source context', text)
        self.assertNotIn('>QA Bench<', text)
        self.assertIn('Library tools &amp; project', text)
        self.assertNotIn('reader-secondary-nav" open', text)

    def test_home_has_four_visual_doors_not_a_status_wall(self):
        text = reader_hierarchy.home()
        self.assertEqual(text.count('class="sog-portal-card"'), 4)
        self.assertEqual(text.count('<svg '), 4)
        self.assertIn('view=lean', text)
        self.assertIn('view=functor', text)
        self.assertNotIn('<table', text)

    def test_collection_list_preserves_real_task_ids_and_supports_progressive_loading(self):
        core={'id':'sogb-fixture', 'title':'A source-backed task', 'family':'one-family',
              'library_domains':['optimisation'], 'track_levels':{'natural-language':'L3'}}
        collection=bench_portals.configuration()['collections'][1]
        text=bench_portals.collection_page([core], collection)
        self.assertIn('../sogb-fixture.html', text)
        self.assertIn('data-sog-task-list', text)
        self.assertIn('type="search"', text)
        self.assertIn('data-sog-show-more hidden', text)
        self.assertIn('NL L3', text)
        self.assertNotIn('Lean L', text)

    def test_agentic_lean_readiness_is_not_inferred_from_the_graph_runner(self):
        text=bench_portals.evaluation_page()
        self.assertIn('executor pending', text)
        self.assertIn('Experimental Linux CLI', text)
        self.assertIn('native08-independent-review.json', text)
        self.assertIn('lean-runtime/WORKSPACE.md', text)
        self.assertIn('Human-assessed', text)
        self.assertIn('Native Harbor adapter', text)
        self.assertIn('not ready', text)
        self.assertNotIn('leaderboard score', text)
        source_links=re.findall(r'href="(https://github.com/[^\"]+/blob/[^\"]+)"',text)
        self.assertEqual(len(source_links),2)
        git=bench_portals.astis_site.git_context()
        for link in source_links:
            self.assertIsNone(bench_portals.astis_site.source_commit_link_error(link,git.commit,git.web_root))

    def test_collection_download_keeps_original_rows_and_one_core_identity(self):
        core={'id':'sogb-fixture','library_domains':['riemannian-optimization']}
        rows=[{'id':core['id'],'track':t,'family':'same-family','split':'public-dev','binding_sha256':'unchanged'}
              for t in ('natural-language','lean')]
        raw=b''.join((json.dumps(r,sort_keys=True)+'\n').encode() for r in rows)
        with tempfile.TemporaryDirectory() as temporary:
            folder=Path(temporary)
            (folder/'reviewed-questions.jsonl').write_bytes(raw)
            (folder/'manifest.json').write_bytes(b'{"schema_version":1}\n')
            assets=bench_portals.collection_assets(folder,[core],bench_portals.configuration()['collections'][2])
            self.assertEqual(assets['questions.jsonl'],raw)
            manifest=json.loads(assets['manifest.json'])
            self.assertEqual(manifest['core_ids'],[core['id']])
            self.assertEqual(manifest['qa_views'],2)
            self.assertEqual(manifest['files']['questions.jsonl'],hashlib.sha256(raw).hexdigest())
            self.assertFalse(manifest['includes_reference_answers'])
            (folder/'reviewed-questions.jsonl').write_text(json.dumps(dict(rows[0],steps=['not a prompt'])))
            with self.assertRaises(ValueError):
                bench_portals.collection_assets(folder,[core],bench_portals.configuration()['collections'][2])


if __name__ == '__main__':
    unittest.main()
