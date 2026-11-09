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

    def test_public_draft_views_use_the_exact_public_hash_contract(self):
        base = {'id': 'draft-core', 'family': 'draft-family', 'library_domains': ['mcmc'],
                'skills': ['proof'], 'title': 'Public fixture', 'split': 'public-dev',
                'binding_sha256': '3'*64, 'level': 'L2', 'domain': 'sampling',
                'assumptions': ['finite measure'], 'question': 'Give a bound'}
        template = 'example : True := by\n  -- Replace this comment with your proof.\n'
        nl = {**base, 'track': 'natural-language'}
        lean = {**base, 'track': 'lean', 'question': exposure.LEAN_PROMPT_PREFIX + template}
        anchors = {base['id']: ['lean:AutoSamplingTheory.Measure.finite_bound']}
        built = exposure.build_published_drafts([nl, lean], anchors)
        catalog = exposure.build_public([{**base, 'declaration': 'AutoSamplingTheory.Measure.finite_bound',
                                          'lean_task': template}], [])
        self.assertEqual(built, catalog)
        for changed in ({**nl, 'answer': 'not a prompt'}, {**lean, 'question': 'unrecognized formatter'},
                        {**lean, 'split': 'private-test'}, {**lean, 'family': 'elsewhere'}):
            with self.assertRaises(ValueError):
                exposure.build_published_drafts([nl, changed], anchors)
        with self.assertRaises(ValueError):
            exposure.build_published_drafts([lean], {})

    def test_shipped_public_exposures_block_relabelled_views_and_source_anchors(self):
        drafts, provenance = exposure.known_published_drafts()
        entries = exposure.public_records(drafts)
        self.assertEqual(exposure.draft_sources(provenance)['snapshot_sha256'], exposure.digest(drafts))
        self.assertTrue({'sogb-031', 'draft-exercise-1-7-compact-pi', 'draft-exercise-1-7-actual-kl',
                         'draft-random-scan-public-paths'} <= {r['id'] for r in entries})
        self.assertEqual(set().union(*(r['views'].keys() for r in entries)), exposure.TRACKS)
        for entry in entries:
            for track, sha in entry['views'].items():
                with self.subTest(track=track, identity=entry['id']):
                    disguised = {**self.private, 'views': {track: sha}}
                    self.assertEqual(exposure.audit_private(self.live, [],
                        inventory([self.live], disguised))['status'], 'no-exact-overlap')
                    with self.assertRaisesRegex(ValueError, 'prompt=1$'):
                        exposure.audit_private(self.live, [drafts], inventory([self.live, drafts], disguised))
            disguised = {**self.private, 'anchors': entry['anchors']}
            with self.assertRaisesRegex(ValueError, 'anchor='):
                exposure.audit_private(self.live, [drafts], inventory([self.live, drafts], disguised))
        with self.assertRaisesRegex(ValueError, 'bound to exactly'):
            exposure.audit_private(self.live, [drafts], inventory([self.live], self.private))

    def test_public_draft_provenance_requires_exact_artifacts_and_anchor_coverage(self):
        graph = {'id': 'graph-draft', 'family': 'graph-family', 'library_domains': ['mcmc'],
                 'skills': ['graph-reading'], 'title': 'Public fixture', 'split': 'public-dev',
                 'binding_sha256': '3'*64, 'level': 'L2', 'track': 'graph-json',
                 'question': 'Which nodes reach the interface?', 'context': {'nodes': ['a']},
                 'targets': ['a'], 'remove': 'b'}
        anchors = {'graph-draft': ['original:graph-fixture']}
        raw = exposure.encoded(graph)
        data = exposure.build_published_drafts([graph], anchors)
        source = exposure.encoded({'schema_version': 1, 'snapshot_sha256': exposure.digest(data),
            'inputs': {'graph-source': {'ref': 'refs/heads/codex/graph-draft', 'commit': 'a'*40,
                'format': 'json', 'sha256': exposure.digest(raw), 'anchors': anchors}}})
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            file, snap, prov = (folder / name for name in ('artifact.json', 'snapshot.json', 'source.json'))
            file.write_bytes(raw)
            snap.write_bytes(data)
            prov.write_bytes(source)
            exposure.replay_published_drafts({'graph-source': file}, data, source)
            with self.assertRaisesRegex(ValueError, 'each exact recorded'):
                exposure.replay_published_drafts({}, data, source)
            file.write_bytes(raw + b'\n')
            with self.assertRaisesRegex(ValueError, 'digest changed'):
                exposure.replay_published_drafts({'graph-source': file}, data, source)
            with patch.object(exposure, 'PUBLIC_DRAFTS', snap), patch.object(exposure, 'PUBLIC_DRAFT_SOURCES', prov):
                self.assertEqual(exposure.known_published_drafts(), (data, source))
                snap.write_bytes(data + b'\n')
                with self.assertRaisesRegex(ValueError, 'recorded provenance'):
                    exposure.known_published_drafts()


class PrivateSealTests(unittest.TestCase):
    def setUp(self):
        self.live = snapshot(row('pub', 'public-family', 'original:public-anchor', 'public prompt'))
        self.old = snapshot(row('retired', 'old-family', 'original:retired-anchor', 'retired prompt'))
        self.views = {'natural-language': {'assumptions': ['fixture assumption'], 'question': 'fixture question'},
                      'lean': 'fixture template'}
        self.row = {'id': 'opaque-item', 'family': 'opaque-family', 'anchors': ['original:opaque-anchor'],
                    'views': {k: exposure.prompt_sha256(k, v) for k, v in self.views.items()}}
        self.inventory = inventory([self.live, self.old], self.row)
        self.prompts = self.pack(exposure.PROMPT_KIND, self.views)
        self.references = self.pack(exposure.REFERENCE_KIND, {k: {
            'solution': 'fixture solution', 'rubric': 'fixture rubric'} for k in self.views})

    def pack(self, kind, views, **extra):
        return exposure.encoded({'schema_version': 1, 'kind': kind, 'records': [
            {'id': self.row['id'], 'views': views, **extra}]})

    def receipt(self, **changes):
        return exposure.encoded({'schema_version': 1, 'kind': exposure.REVIEW_KIND,
            'inventory_sha256': exposure.digest(self.inventory), 'prompts_sha256': exposure.digest(self.prompts),
            'references_sha256': exposure.digest(self.references), 'author': 'author-a', 'reviewer': 'reviewer-b',
            'families': [{'id': self.row['family'], 'decision': 'accept', 'checks': sorted(exposure.REVIEW_CHECKS)}],
            **changes})

    def audit(self, *, review=None, pin=None):
        review = self.receipt() if review is None else review
        return exposure.audit_private_seal(self.live, [self.old], self.inventory,
            self.prompts, self.references, review, exposure.digest(review) if pin is None else pin)

    def test_valid_seal_reports_counts_not_private_data_or_acceptance(self):
        result = self.audit()
        self.assertEqual(result['status'], 'matches-pinned-private-review')
        self.assertEqual(result['private_views'], 2)
        self.assertEqual(result['review_bound_families'], 1)
        for key in ('admitted', 'model_measurement', 'receipt_identity_authenticated',
                    'semantic_independence_verified'):
            self.assertIs(result[key], False)
        for secret in ('opaque-item', 'opaque-family', 'fixture question', 'fixture solution', 'reviewer-b'):
            self.assertNotIn(secret, json.dumps(result))

    def test_pinned_receipt_binds_every_exact_file(self):
        receipt = self.receipt()
        with self.assertRaisesRegex(ValueError, 'pinned SHA-256'):
            self.audit(review=receipt + b'\n', pin=exposure.digest(receipt))
        for member in ('inventory', 'prompts', 'references'):
            with self.subTest(member=member), patch.object(self, member, getattr(self, member) + b'\n'):
                with self.assertRaisesRegex(ValueError, 'does not bind'):
                    self.audit(review=receipt)

    def test_even_repinned_receipt_cannot_change_screened_prompt_or_tracks(self):
        for views, error in (
            ({**self.views, 'lean': 'different exact template'}, 'screened inventory'),
            ({'lean': self.views['lean']}, 'inventory IDs or tracks'),
        ):
            with self.subTest(error=error), patch.object(self, 'prompts', self.pack(exposure.PROMPT_KIND, views)):
                with self.assertRaisesRegex(ValueError, error):
                    self.audit()
        with patch.object(self, 'prompts', self.pack(exposure.PROMPT_KIND, self.views, solution='leak')):
            with self.assertRaisesRegex(ValueError, 'inventory IDs or tracks'):
                self.audit()

    def test_missing_or_invalid_grader_data_is_not_a_sealed_task(self):
        for views in ({}, {k: {'solution': ' ', 'rubric': 'fixture'} for k in self.views}):
            with self.subTest(views=len(views)), patch.object(self, 'references',
                    self.pack(exposure.REFERENCE_KIND, views)):
                with self.assertRaises(ValueError):
                    self.audit()

    def test_receipt_refuses_same_label_or_incomplete_family_checklist(self):
        family = {'id': self.row['family'], 'decision': 'accept', 'checks': sorted(exposure.REVIEW_CHECKS)}
        for fields in ({'reviewer': 'author-a'}, {'families': []}, {'families': [family, family]},
                       {'families': [{**family, 'decision': 'reject'}]},
                       {'families': [{**family, 'checks': ['family-independence'] * 4}]}):
            with self.subTest(fields=fields), self.assertRaises(ValueError):
                self.audit(review=self.receipt(**fields))

    def test_seal_does_not_override_history_screen(self):
        family = exposure.strict_json(self.old)['records'][0]['family']
        exposed = inventory([self.live, self.old], {**self.row, 'family': family})
        with patch.object(self, 'inventory', exposed), self.assertRaisesRegex(ValueError, 'family=1'):
            self.audit()
