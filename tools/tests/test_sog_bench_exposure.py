"""Offline fixtures: collisions and path checks, not an authored private test set."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tools import sog_bench_exposure as exposure


def row(identity, family, anchor, prompt, track='natural-language'):
    return {'id': identity, 'family': family, 'anchors': [anchor],
            'views': {track: exposure.digest(prompt.encode())}}


def snapshot(*rows):
    return exposure.encoded({'schema_version': 1, 'kind': exposure.PUBLIC_KIND, 'records': rows})


def inventory(snapshots, *rows):
    return exposure.encoded({'schema_version': 1, 'kind': exposure.PRIVATE_KIND,
        'source_scope': exposure.SOURCE_SCOPE, 'split': 'private-test',
        'public_snapshots': [exposure.digest(s) for s in snapshots], 'records': rows})


class ExposureTests(unittest.TestCase):
    def setUp(self):
        self.live = snapshot(row('public-new', 'new-family', 'original:new-source', 'new prompt'))
        self.old_row = row('public-old', 'retired-family', 'exercise:archived-exercise', 'old prompt')
        self.old = snapshot(self.old_row)
        self.private = row('operator-example', 'operator-family', 'original:operator-problem', 'fixture')

    def test_history_retains_retired_exact_id_family_prompt_and_anchor(self):
        for dimension, mutate in {
            'id': {'id': self.old_row['id']},
            'family': {'family': self.old_row['family']},
            'anchor': {'anchors': self.old_row['anchors']},
            'prompt': {'views': self.old_row['views']},
        }.items():
            with self.subTest(dimension=dimension):
                private = inventory([self.live, self.old], {**self.private, **mutate})
                with self.assertRaisesRegex(ValueError, f'Public exposure overlaps: {dimension}=1$'):
                    exposure.audit_private(self.live, [self.old], private)

    def test_public_snapshot_set_is_exact_not_optional_after_freeze(self):
        declared = inventory([self.live, self.old], self.private)
        for live, historical in ((self.live, []), (self.live, [self.old, self.old]),
                                 (self.live + b'\n', [self.old])):
            with self.subTest(historical=len(historical)):
                with self.assertRaises(ValueError):
                    exposure.audit_private(live, historical, declared)

    def test_clear_exact_preflight_is_nonadmitting_and_never_echoes_private_labels(self):
        result = exposure.audit_private(self.live, [self.old],
                inventory([self.old, self.live], self.private))
        self.assertEqual(result['status'], 'no-exact-overlap')
        self.assertEqual(result['public_snapshot_count'], 2)
        self.assertEqual(result['private_records'], 1)
        for key in ('admitted', 'semantic_independence_verified', 'model_measurement'):
            self.assertIs(result[key], False)
        self.assertNotIn(self.private['id'], json.dumps(result))
        self.assertNotIn(self.private['family'], json.dumps(result))

    def test_alias_family_split_and_exact_duplicate_view_are_rejected(self):
        second = row('second-example', self.private['family'], self.private['anchors'][0], 'other')
        self.assertEqual(exposure.audit_private(self.live, [],
            inventory([self.live], self.private, second))['private_families'], 1)
        for changes, error in (({'family': 'other-family'}, 'split across families'),
                               ({'views': self.private['views']}, 'Duplicate exact prompt')):
            with self.subTest(error=error), self.assertRaisesRegex(ValueError, error):
                exposure.audit_private(self.live, [],
                    inventory([self.live], self.private, {**second, **changes}))

    def test_inventory_rejects_payloads_invalid_types_and_duplicate_keys(self):
        good = inventory([self.live], self.private)
        for raw in (good.replace(b'"schema_version": 1', b'"schema_version": true'),
                    good.replace(b'"split": "private-test"', b'"split": "public-dev"'),
                    good.replace(b'"split": "private-test"', b'"split": "public-dev", "split": "private-test"'),
                    inventory([self.live], {**self.private, 'answer': 'never pass raw payload'}),
                    inventory([self.live], {**self.private, 'anchors': ['atlas:restricted']})):
            with self.assertRaises(ValueError):
                exposure.audit_private(self.live, [], raw)

    def test_private_metadata_path_must_resolve_outside_repo_and_is_bounded(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            repo = folder / 'repo'
            repo.mkdir()
            inside = repo / 'heldout.json'
            outside = folder / 'heldout.json'
            inside.write_bytes(b'inventory fixture')
            outside.write_bytes(b'inventory fixture')
            with self.assertRaisesRegex(ValueError, 'outside the repository'):
                exposure.read_metadata(inside, outside=repo)
            self.assertEqual(exposure.read_metadata(outside, outside=repo), b'inventory fixture')
            with patch.object(exposure, 'MAX_METADATA_BYTES', 1), self.assertRaisesRegex(ValueError, 'byte limit'):
                exposure.read_metadata(outside, outside=repo)

    def test_public_fingerprints_ignore_renamed_ids_but_preserve_assumptions_and_tracks(self):
        core = {'id': 'fixture', 'family': 'fixture-family', 'split': 'public-dev',
                'declaration': 'AutoSamplingTheory.Measure.finite_bound', 'lean_task': 'example : Nat := 0',
                'question': 'Prove the bound', 'assumptions': ['finite measure'],
                'title': 'A public title', 'steps': ['private-shaped proof not emitted']}
        graph = {'id': 'fixture-graph', 'family': core['family'], 'core_id': core['id'],
                 'split': 'public-dev', 'question': 'List the outgoing edges',
                 'targets': ['a'], 'context': {'nodes': ['a']}, 'answer': {'nodes': []}}
        one = json.loads(exposure.build_public([core], [graph]))['records']
        changed = deepcopy(core)
        changed.update(id='renamed', family='other-family', title='New title')
        two = json.loads(exposure.build_public([changed], []))['records']
        self.assertEqual(one[0]['views'], two[0]['views'])
        self.assertEqual(set(one[1]['views']), {'graph-json'})
        self.assertEqual(one[0]['anchors'], one[1]['anchors'])
        changed['assumptions'] = ['not necessarily finite']
        three = json.loads(exposure.build_public([changed], []))['records']
        self.assertNotEqual(one[0]['views']['natural-language'], three[0]['views']['natural-language'])
        self.assertEqual(one[0]['views']['lean'], three[0]['views']['lean'])
        self.assertNotIn(b'private-shaped proof', exposure.build_public([core], [graph]))
        with self.assertRaisesRegex(ValueError, 'source family'):
            exposure.build_public([core], [{**graph, 'family': 'elsewhere'}])
