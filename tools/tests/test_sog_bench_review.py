"""Independent-role evidence, exact inputs, local staleness and reviewed-subset safety."""
from copy import deepcopy
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / 'tools'), str(ROOT / 'website/scripts')]
import sog_bench as bench
import sog_bench_review as review


class EditorialReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source_patch = patch.object(bench.astis_site, '_SOURCE_BY_NAME',
            {d.full_name:d for d in bench.astis_site.scan_project_sources()[1]})
        cls.source_patch.start()
        cls.addClassCleanup(cls.source_patch.stop)
        cls.cores = bench.materialize()

    def test_actual_independent_evidence_admits_only_the_reviewed_seven(self):
        rows = review.statuses(self.cores)
        accepted = {k for k,v in rows.items() if review.accepted(v)}
        self.assertEqual(accepted, {f'sogb-{i:03d}' for i in range(1,8)})
        self.assertEqual(rows['sogb-003']['editorial'], 'accepted-after-repair')
        for core in self.cores[:3]:
            row = rows[core['id']]
            self.assertEqual(row['formal_alignment'], 'conclusion-only')
            self.assertTrue(row['remaining_unformalized'])
        self.assertEqual(review.summary(self.cores)['difficulty_calibrated'], False)

    def test_anonymous_packet_has_no_source_identity_or_gold_and_survives_prose_only_repair(self):
        packet, mapping = review.decoder_packet(self.cores)
        frozen = json.loads((review.ROUND / 'packets/anonymous-input.json').read_text(encoding='utf-8'))
        self.assertEqual(packet, frozen)
        text = json.dumps(packet)
        for core in self.cores:
            for key in ('id','title','source_file','declaration'):
                self.assertNotIn(core[key], text)
        self.assertNotIn('AutoSamplingTheory', text)
        self.assertNotIn('reference_answer', text)
        self.assertEqual(set(mapping['cases']), {'A','B','C'})

    def test_changing_one_question_invalidates_only_its_editorial_binding(self):
        data = deepcopy(bench.load())
        data['cores'][0]['question'] += ' Additional unreviewed clause.'
        changed = bench.materialize(data)
        rows = review.statuses(changed)
        self.assertEqual(rows['sogb-001']['editorial'], 'stale')
        self.assertEqual(rows['sogb-002']['editorial'], 'accepted')
        self.assertEqual(rows['sogb-003']['editorial'], 'accepted-after-repair')

    def test_role_reuse_and_changed_packet_bytes_fail_closed(self):
        for scenario in ('role-reuse','packet-bytes'):
            with tempfile.TemporaryDirectory() as tmp:
                folder = Path(tmp) / 'round'
                shutil.copytree(review.ROUND, folder)
                if scenario == 'role-reuse':
                    path = folder / 'source-review.json'
                    obj = json.loads(path.read_text(encoding='utf-8'))
                    obj['actor_identity'] = review.AUTHOR
                    path.write_bytes(bench.encoded(obj))
                else:
                    path = folder / 'packets/anonymous-input.json'
                    path.write_bytes(path.read_bytes() + b'\n')
                with self.assertRaises(ValueError):
                    review.statuses(self.cores, folder)

    def test_rejected_old_wording_does_not_gain_the_repair_acceptance(self):
        old_packet = json.loads((review.ROUND / 'packets/reviewer-input.json').read_text(encoding='utf-8'))
        old_core = next(c for c in old_packet['mathematical_cores'] if c['id']=='sogb-003')
        mixed = [old_core if c['id']=='sogb-003' else c for c in self.cores]
        self.assertEqual(review.statuses(mixed)['sogb-003']['editorial'], 'repair-required')

    def test_reviewed_exports_cannot_silently_include_new_drafts(self):
        data = deepcopy(bench.load())
        draft = deepcopy(data['cores'][-1])
        draft['id'] = 'sogb-999'
        draft['question'] += ' Unreviewed test-fixture revision.'
        data['cores'].append(draft)
        with_draft = bench.materialize(data)
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            bench.export(target, with_draft)
            questions = [json.loads(line) for line in (target/'reviewed-questions.jsonl').read_text(encoding='utf-8').splitlines()]
            refs = [json.loads(line) for line in (target/'reviewed-reference.jsonl').read_text(encoding='utf-8').splitlines()]
            self.assertEqual(len(questions), 38)
            self.assertEqual(len(refs), 26)
            self.assertEqual({q['id'] for q in questions}, {c['id'] for c in refs})
            self.assertTrue(all('steps' not in q and 'lean_reference' not in q for q in questions))
            self.assertNotIn('sogb-999', {q['id'] for q in questions})

    def test_nl_round_accepts_without_inventing_formal_alignment(self):
        rows = review.prose_statuses(self.cores)
        self.assertEqual(set(rows), {f'sogb-{i:03d}' for i in range(8,15)})
        self.assertTrue(all(review.accepted(row) for row in rows.values()))
        self.assertTrue(all(row['formal_alignment'] == 'no-aligned-view' for row in rows.values()))
        self.assertEqual(review.summary(self.cores)['accepted_cores'], 26)

    def test_uncountable_event_review_is_unpaired_and_separately_content_bound(self):
        directory=review.BASE/'reviews/prose-4'
        rows=review.prose_statuses(self.cores,directory)
        self.assertEqual(set(rows),{'sogb-024'})
        self.assertEqual(rows['sogb-024']['editorial'],'accepted')
        self.assertEqual(rows['sogb-024']['formal_alignment'],'no-aligned-view')
        changed=deepcopy(self.cores)
        next(c for c in changed if c['id']=='sogb-024')['binding_sha256']='changed-quantifier'
        self.assertEqual(review.prose_statuses(changed,directory)['sogb-024']['editorial'],'stale')

    def test_additional_prose_round_is_disjoint_and_content_bound(self):
        directory=review.BASE/'reviews/prose-3'
        rows=review.prose_statuses(self.cores,directory)
        self.assertEqual(set(rows),{'sogb-020'})
        self.assertEqual(rows['sogb-020']['formal_alignment'],'no-aligned-view')
        changed=deepcopy(self.cores)
        next(c for c in changed if c['id']=='sogb-020')['binding_sha256']='changed'
        self.assertEqual(review.prose_statuses(changed,directory)['sogb-020']['editorial'],'stale')
        with patch.object(review,'PROSE_ROUND',directory):
            with self.assertRaisesRegex(ValueError,'Overlapping'):
                review.summary(self.cores)

    def test_new_scoped_repairs_preserve_old_reviews_and_reject_laundered_changes(self):
        import sog_bench_formal_review as formal
        for name,identity,is_formal in (('prose-3','sogb-020',False),('formal-7','sogb-019',True)):
            original=review.BASE/'reviews'/name
            status=formal.round_statuses if is_formal else review.prose_statuses
            self.assertEqual(status(self.cores,original)[identity]['editorial'],'accepted-after-repair')
            actual_context=review.context_binding
            with patch.object(review,'context_binding',side_effect=lambda core: 'changed-source' if core['id']==identity else actual_context(core)):
                self.assertEqual(status(self.cores,original)[identity]['editorial'],'stale')
            for scenario in ('actor-reuse','proposal-bytes','open-repair','source-change'):
                with tempfile.TemporaryDirectory() as tmp:
                    directory=Path(tmp)/name
                    shutil.copytree(original,directory)
                    path=directory/'repair-review.json'
                    obj=json.loads(path.read_text(encoding='utf-8'))
                    if scenario=='actor-reuse':
                        obj['actor_identity']=json.loads((directory/'source-review.json').read_text(encoding='utf-8'))['actor_identity']
                    elif scenario=='proposal-bytes':
                        proposal_path=directory/'packets/repair-input.json'
                        proposal_path.write_bytes(proposal_path.read_bytes()+b'\n')
                    elif scenario=='open-repair':
                        obj['items'][identity]['repair_requests']=['Unresolved scoring change.']
                    else:
                        proposal_path=directory/'packets/repair-input.json'
                        proposal=json.loads(proposal_path.read_text(encoding='utf-8'))
                        after=proposal['cases'][identity]['proposed_after']
                        after['assumptions'].append('An unreviewed extra mathematical assumption.')
                        after['binding_sha256']=bench.sha(bench.encoded({k:v for k,v in after.items() if k!='binding_sha256'}))
                        proposal_path.write_bytes(bench.encoded(proposal))
                        obj['input_packet_sha256']=bench.sha(proposal_path.read_bytes())
                        obj['items'][identity]['proposed_binding_sha256']=after['binding_sha256']
                    path.write_bytes(bench.encoded(obj))
                    with self.assertRaises(ValueError):
                        status(self.cores,directory)

    def test_nl_packet_route_rejects_formal_views_duplicates_unknown_ids_and_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'input.json'
            for identities in ([], ['sogb-001'], ['sogb-008', 'sogb-008'], ['unknown']):
                with self.assertRaises(ValueError):
                    review.prepare_prose(self.cores, identities, path)
            review.prepare_prose(self.cores, ['sogb-008'], path)
            self.assertEqual(json.loads(path.read_text(encoding='utf-8'))['scope'], review.PROSE_SCOPE)
            with self.assertRaises(ValueError):
                review.prepare_prose(self.cores, ['sogb-008'], path)

    def test_nl_review_rejects_role_reuse_changed_bytes_false_alignment_and_open_repairs(self):
        for scenario in ('role-reuse', 'packet-bytes', 'formal-scope', 'open-repair'):
            with tempfile.TemporaryDirectory() as tmp:
                folder = Path(tmp) / 'round'
                shutil.copytree(review.PROSE_ROUND, folder)
                path = folder / 'source-review.json'
                obj = json.loads(path.read_text(encoding='utf-8'))
                if scenario == 'role-reuse':
                    obj['actor_identity'] = review.AUTHOR
                elif scenario == 'formal-scope':
                    obj['items']['sogb-008']['formal_scope'] = 'conclusion-only'
                elif scenario == 'open-repair':
                    obj['items']['sogb-008']['repair_requests'] = ['An unresolved mathematical change.']
                else:
                    packet = folder / 'packets/prose-input.json'
                    packet.write_bytes(packet.read_bytes() + b'\n')
                path.write_bytes(bench.encoded(obj))
                with self.assertRaises(ValueError):
                    review.prose_statuses(self.cores, folder)

    def test_additional_support_modules_and_ancestors_bind_research_audit(self):
        core = next(c for c in self.cores if c['id'] == 'sogb-026')
        actual_hash = bench.text_hash
        baseline = review.context_binding(core)
        self.assertEqual(len(core['supporting_declarations']), 4)
        for support in core['supporting_declarations']:
            target = (bench.ROOT / support['source_file']).resolve()
            self.assertEqual(support['source_sha256_lf'], actual_hash(target))
            with patch.object(bench, 'text_hash', side_effect=lambda path:
                              'changed-extra-source' if path.resolve() == target else actual_hash(path)):
                self.assertNotEqual(review.context_binding(core), baseline)
        # This ancestor is not itself one of the four named support modules.
        target = (bench.ROOT / 'AutoSamplingTheory/ExampleCases/ProximalBPS/GaussianAugmentation.lean').resolve()
        with patch.object(bench, 'text_hash', side_effect=lambda path:
                          'changed-extra-ancestor' if path.resolve() == target else actual_hash(path)):
            self.assertNotEqual(review.context_binding(core), baseline)

    def test_additional_source_metadata_is_resolved_and_not_prompt_leakage(self):
        data = deepcopy(bench.load())
        original = next(c for c in data['cores'] if c['id'] == 'sogb-026')
        for names in ([], ['Unknown.missing'], ['duplicate', 'duplicate'], 'not-a-list'):
            original['additional_source_declarations'] = names
            with self.assertRaises(ValueError):
                bench.materialize(data)
        core = next(c for c in self.cores if c['id'] == 'sogb-026')
        prompt = bench.prompts([core])[0]
        self.assertNotIn('supporting_declarations', prompt)
        self.assertNotIn('support_lean_source', prompt)
        self.assertNotIn('lean', core['track_levels'])

    def test_curvature_prose_repair_preserves_the_actual_math_and_no_formal_alignment(self):
        directory = review.BASE / 'reviews/prose-5'
        packet = json.loads((directory / 'packets/prose-input.json').read_text(encoding='utf-8'))
        proposal = json.loads((directory / 'packets/repair-input.json').read_text(encoding='utf-8'))
        before = packet['mathematical_cores'][0]
        after = proposal['cases']['sogb-026']['proposed_after']
        self.assertEqual(before['track_levels'], {'natural-language': 'L5'})
        self.assertEqual(after['track_levels'], {'natural-language': 'L4'})
        changed = {k for k in before.keys() | after.keys() if before.get(k) != after.get(k)}
        self.assertEqual(changed, {'track_levels', 'difficulty_reason', 'binding_sha256'})
        row = review.prose_statuses(self.cores, directory)['sogb-026']
        self.assertEqual(row['editorial'], 'accepted-after-repair')
        self.assertEqual(row['formal_alignment'], 'no-aligned-view')

    def test_nl_review_is_local_and_stale_when_content_or_support_changes(self):
        data = deepcopy(bench.load())
        data['cores'][7]['question'] += ' Additional unaudited clause.'
        changed = bench.materialize(data)
        rows = review.prose_statuses(changed)
        self.assertEqual(rows['sogb-008']['editorial'], 'stale')
        self.assertEqual(rows['sogb-009']['editorial'], 'accepted')
        actual_binding = review.context_binding
        def changed_context(core):
            return 'changed' if core['id'] == 'sogb-013' else actual_binding(core)
        with patch.object(review, 'context_binding', side_effect=changed_context):
            rows = review.prose_statuses(self.cores)
        self.assertEqual(rows['sogb-013']['editorial'], 'stale')
        self.assertEqual(rows['sogb-012']['editorial'], 'accepted')


if __name__ == '__main__':
    unittest.main()
