"""Anonymous paired review, exact target bindings and distinct-role admission."""
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
import sog_bench_formal_review as formal

ROUND = formal.REVIEWS / 'formal-3'


class PairedReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source_patch = patch.object(bench.astis_site, '_SOURCE_BY_NAME',
            {d.full_name:d for d in bench.astis_site.scan_project_sources()[1]})
        cls.source_patch.start()
        cls.addClassCleanup(cls.source_patch.stop)
        cls.cores = bench.materialize()
        cls.core = next(c for c in cls.cores if c['id'] == 'sogb-015')

    def test_anonymous_input_is_exact_without_source_identity_or_answer(self):
        packet, mapping = formal.decoder_payload([self.core])
        self.assertEqual((ROUND/'packets/anonymous-input.json').read_bytes(), bench.encoded(packet))
        self.assertEqual((ROUND/'packets/coordinator-map.json').read_bytes(), bench.encoded(mapping))
        text = json.dumps(packet)
        for key in ('id', 'title', 'family', 'source_file', 'declaration'):
            self.assertNotIn(self.core[key], text)
        self.assertNotIn('AutoSamplingTheory', text)
        self.assertNotIn(':= by', text)
        self.assertNotIn('steps', text)
        self.assertNotIn('lean_reference', text)
        self.assertIn('def IsCoupling', text)

    def test_input_generation_rejects_missing_context_source_leaks_unpaired_and_overwrite(self):
        for change in ({'decoder_definitions': []}, {'decoder_definitions': [self.core['declaration']]},
                       {'decoder_definitions': [{'hidden': 'structured context'}]}, {'lean_enabled': False}):
            with self.assertRaises(ValueError):
                formal.decoder_payload([{**self.core, **change}])
        with self.assertRaises(ValueError):
            formal.decoder_payload([self.core, self.core])
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / 'packets'
            formal.prepare_decoder([self.core], target)
            with self.assertRaises(ValueError):
                formal.prepare_decoder([self.core], target)

    def test_actual_distinct_actor_evidence_admits_one_conclusion_only_pair(self):
        rows = formal.statuses(self.cores)
        first_round = {'sogb-001', 'sogb-002', 'sogb-003'}
        self.assertEqual(set(rows), {c['id'] for c in self.cores if bench.has_lean(c)} - first_round)
        self.assertEqual(rows['sogb-015']['editorial'], 'accepted')
        self.assertEqual(rows['sogb-015']['formal_alignment'], 'conclusion-only')
        self.assertTrue(rows['sogb-015']['remaining_unformalized'])
        self.assertEqual(rows['sogb-032']['editorial'], 'accepted')
        self.assertEqual(rows['sogb-032']['formal_alignment'], 'conclusion-only')
        self.assertEqual(rows['sogb-038']['editorial'], 'accepted-after-repair')
        self.assertEqual(rows['sogb-038']['formal_alignment'], 'conclusion-only')
        for identity in ('sogb-039', 'sogb-040', 'sogb-041'):
            self.assertEqual(rows[identity]['editorial'], 'accepted')
            self.assertEqual(rows[identity]['formal_alignment'], 'conclusion-only')
            self.assertTrue(rows[identity]['remaining_unformalized'])
        self.assertEqual(review.summary(self.cores)['accepted_cores'], len(self.cores))

    def test_product_coupling_preserves_the_exact_preflight_and_repaired_review(self):
        directory = formal.REVIEWS / 'formal-16'
        previous = directory / 'preflight-v1'
        packet = json.loads((previous / 'packets/reviewer-input.json').read_text(encoding='utf-8'))
        old = packet['mathematical_cores'][0]
        new = next(c for c in self.cores if c['id'] == 'sogb-041')
        self.assertEqual(formal.round_statuses([old], previous)['sogb-041']['editorial'], 'repair-required')
        self.assertEqual(formal.round_statuses([new], previous)['sogb-041']['editorial'], 'stale')
        self.assertEqual(formal.round_statuses([new], directory)['sogb-041']['editorial'], 'accepted')
        self.assertEqual(old['lean_task'], new['lean_task'])
        self.assertEqual(old['lean_reference'], new['lean_reference'])
        self.assertEqual(old['question'], new['question'])
        self.assertEqual(old['rubric'], new['rubric'])

    def test_common_kernel_review_preserves_rejected_predecessor(self):
        directory = formal.REVIEWS / 'formal-13'
        previous = directory / 'predecessor-repair-required'
        packet = json.loads((previous / 'packets/reviewer-input.json').read_text(encoding='utf-8'))
        self.assertEqual(formal.round_statuses(packet['mathematical_cores'], previous)['sogb-037']['editorial'],
                         'repair-required')
        self.assertEqual(formal.round_statuses(self.cores, previous)['sogb-037']['editorial'], 'stale')
        accepted = formal.round_statuses(self.cores, directory)['sogb-037']
        self.assertEqual(accepted['editorial'], 'accepted')
        self.assertEqual(accepted['formal_alignment'], 'conclusion-only')

    def test_sphere_bound_uses_only_the_reviewed_anonymous_alias(self):
        core = next(c for c in self.cores if c['id'] == 'sogb-032')
        directory = formal.REVIEWS/'formal-12'
        packet, _ = formal.decoder_payload([core])
        self.assertIn('anonymous_constant_1', packet['cases'][0]['statement'])
        self.assertNotIn('AutoSamplingTheory', json.dumps(packet))
        for symbols in ([core['declaration']], core['decoder_symbols'] * 2):
            with self.assertRaises(ValueError):
                formal.decoder_payload([{**core, 'decoder_symbols': symbols}])
        changed = deepcopy(bench.load())
        next(c for c in changed['cores'] if c['id'] == core['id'])['question'] += ' Unreviewed conclusion.'
        self.assertEqual(formal.round_statuses(bench.materialize(changed), directory)[core['id']]['editorial'], 'stale')

    def test_transport_join_has_its_own_blind_reconstruction_and_source_boundaries(self):
        core=next(c for c in self.cores if c['id']=='sogb-018')
        directory=formal.REVIEWS/'formal-6'
        mapping,decoded=formal.decoder_evidence(directory,[core])
        self.assertEqual(set(mapping['cases']),{'case-1'})
        self.assertFalse(decoded['source_text_visible'])
        self.assertNotIn(core['declaration'],json.dumps(formal.decoder_payload([core])[0]))
        row=formal.round_statuses(self.cores,directory)['sogb-018']
        self.assertEqual(row['editorial'],'accepted')
        self.assertEqual(row['formal_alignment'],'conclusion-only')
        self.assertTrue(row['remaining_unformalized'])
        # A later changed proof/question cannot inherit acceptance.
        changed=deepcopy(bench.load())
        next(c for c in changed['cores'] if c['id']=='sogb-018')['question']+=' Claim optimal-plan attainment.'
        self.assertEqual(formal.round_statuses(bench.materialize(changed),directory)['sogb-018']['editorial'],'stale')

    def test_curve_and_flow_audit_has_only_one_exact_proof_prose_repair(self):
        directory=review.BASE/'reviews/formal-8'
        rows=formal.round_statuses(self.cores,directory)
        self.assertEqual(rows['sogb-022']['editorial'],'accepted-after-repair')
        self.assertEqual(rows['sogb-023']['editorial'],'accepted')
        proposal=json.loads((directory/'packets/repair-input.json').read_text(encoding='utf-8'))
        self.assertEqual(proposal['scope'],review.PAIRED_PROSE_REPAIR_SCOPE)
        case=proposal['cases']['sogb-022']
        before,after=case['before'],case['proposed_after']
        self.assertEqual({k for k in before if before[k]!=after[k]},{'steps','binding_sha256'})
        self.assertEqual([i for i,(a,b) in enumerate(zip(before['steps'],after['steps'])) if a!=b],[2])
        self.assertNotIn('weaker midpoint',after['steps'][2])
        for key in ('lean_task','lean_reference','context','assumptions','question','rubric','track_levels'):
            self.assertEqual(before[key],after[key])
        changed=deepcopy(bench.load())
        next(c for c in changed['cores'] if c['id']=='sogb-023')['question']+=' Allow observation time zero.'
        revised=formal.round_statuses(bench.materialize(changed),directory)
        self.assertEqual(revised['sogb-023']['editorial'],'stale')
        self.assertEqual(revised['sogb-022']['editorial'],'accepted-after-repair')

    def test_paired_proof_prose_scope_rejects_resigned_rubric_and_difficulty_changes(self):
        original=review.BASE/'reviews/formal-8'
        for field in ('rubric','track_levels'):
            with tempfile.TemporaryDirectory() as tmp:
                directory=Path(tmp)/'round'
                shutil.copytree(original,directory)
                proposal_path=directory/'packets/repair-input.json'
                proposal=json.loads(proposal_path.read_text(encoding='utf-8'))
                after=proposal['cases']['sogb-022']['proposed_after']
                if field=='rubric':
                    after['rubric'][0]['criterion']='An unreviewed scoring change.'
                else:
                    after['track_levels']['natural-language']='L5'
                after['binding_sha256']=bench.sha(bench.encoded({k:v for k,v in after.items() if k!='binding_sha256'}))
                proposal_path.write_bytes(bench.encoded(proposal))
                report_path=directory/'repair-review.json'
                report=json.loads(report_path.read_text(encoding='utf-8'))
                report['input_packet_sha256']=bench.sha(proposal_path.read_bytes())
                report['items']['sogb-022']['proposed_binding_sha256']=after['binding_sha256']
                report_path.write_bytes(bench.encoded(report))
                with self.assertRaises(ValueError):
                    formal.round_statuses(self.cores,directory)

    def test_altered_packets_role_reuse_slots_and_open_repairs_fail_closed(self):
        for scenario in ('packet', 'source-role', 'decoder-role', 'slots', 'repair'):
            with tempfile.TemporaryDirectory() as tmp:
                directory = Path(tmp) / 'formal-test'
                shutil.copytree(ROUND, directory)
                path = directory / 'source-review.json'
                data = json.loads(path.read_text(encoding='utf-8'))
                if scenario == 'packet':
                    packet = directory / 'packets/anonymous-input.json'
                    packet.write_bytes(packet.read_bytes() + b'\n')
                elif scenario == 'source-role':
                    data['actor_identity'] = review.AUTHOR
                elif scenario == 'decoder-role':
                    data['actor_identity'] = json.loads((directory/'decoder.json').read_text(encoding='utf-8'))['actor_identity']
                elif scenario == 'slots':
                    data['items']['sogb-015']['semantic_slots'].pop('constants')
                else:
                    data['items']['sogb-015']['repair_requests'] = ['Unresolved mathematical repair.']
                path.write_bytes(bench.encoded(data))
                with self.assertRaises(ValueError):
                    formal.round_statuses(self.cores, directory)

    def test_current_revision_becomes_stale_without_invalidating_other_rounds(self):
        data = deepcopy(bench.load())
        next(c for c in data['cores'] if c['id'] == 'sogb-015')['question'] += ' An additional unreviewed conclusion.'
        changed = bench.materialize(data)
        rows = review.summary(changed)['items']
        self.assertEqual(rows['sogb-015']['editorial'], 'stale')
        self.assertEqual(rows['sogb-001']['editorial'], 'accepted')
        self.assertEqual(rows['sogb-012']['editorial'], 'accepted')

    def test_overlapping_formal_rounds_do_not_silently_override_a_decision(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            shutil.copytree(ROUND, target/'formal-a')
            shutil.copytree(ROUND, target/'formal-b')
            with self.assertRaises(ValueError):
                formal.statuses(self.cores, target)

    def test_more_than_nine_aliases_keep_numeric_case_order(self):
        # Synthetic input/reconstruction fixtures exercise serialization only.
        # No source-review verdict is created or admitted.
        cores = [{**self.core, 'id': f'sogb-{100+i:03d}',
                  'binding_sha256': bench.sha(str(i).encode())} for i in range(12)]
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            formal.prepare_decoder(cores, directory/'packets')
            packet = json.loads((directory/'packets/anonymous-input.json').read_text(encoding='utf-8'))
            decoded = {'schema_version': 1, 'actor_identity': 'software-test-fixture-only',
                       'source_text_visible': False,
                       'input_packet_sha256': bench.sha((directory/'packets/anonymous-input.json').read_bytes()),
                       'cases': {c['case']: {slot: 'Serialization fixture, not a mathematical review.'
                                           for slot in review.SLOTS} for c in packet['cases']}}
            (directory/'decoder.json').write_bytes(bench.encoded(decoded))
            formal.prepare_reviewer(cores, directory)
            combined = json.loads((directory/'packets/reviewer-input.json').read_text(encoding='utf-8'))
            self.assertEqual([c['id'] for c in combined['mathematical_cores']], [c['id'] for c in cores])
            self.assertEqual(formal.round_statuses(cores, directory), {})

    def test_bibliography_rebinding_reuses_only_identical_blind_input_and_output(self):
        old = formal.REVIEWS/'formal-4'
        current = formal.REVIEWS/'formal-5'
        self.assertEqual((old/'packets/anonymous-input.json').read_bytes(),
                         (current/'packets/anonymous-input.json').read_bytes())
        self.assertEqual((old/'decoder.json').read_bytes(), (current/'decoder.json').read_bytes())
        self.assertNotEqual((old/'packets/coordinator-map.json').read_bytes(),
                            (current/'packets/coordinator-map.json').read_bytes())
        self.assertEqual(formal.round_statuses(self.cores, old), {})


if __name__ == '__main__':
    unittest.main()
