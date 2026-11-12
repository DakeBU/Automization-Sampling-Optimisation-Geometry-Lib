"""Frozen graph editorial evidence and exact difficulty-only repair contracts."""
from copy import deepcopy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'tools'))
import sog_bench as bench
import sog_bench_graph_review as review


class GraphReviewTests(unittest.TestCase):
    def setUp(self):
        self.items = bench.curriculum.graph_items()

    def frozen_round(self, directory, source):
        for name in ('input.json','source-review.json'):
            (directory/name).write_bytes((source/name).read_bytes())

    def test_original_decisions_are_not_rewritten_by_current_label(self):
        before = {p:p.read_bytes() for p in review.ROUND.glob('*.json')}
        rows = review.statuses(self.items)
        # The old reports stay immutable; new policy/context bindings require
        # an explicit fresh whole-scope review, not silent historical rebinding.
        self.assertEqual(rows['sogb-g001']['editorial'],'stale')
        self.assertEqual(rows['sogb-g002']['editorial'],'stale')
        self.assertEqual(rows['sogb-g003']['editorial'],'stale')
        original = json.loads((review.ROUND/'source-review.json').read_text(encoding='utf-8'))
        self.assertEqual(original['items']['sogb-g003']['verdict'],'repair-required')
        self.assertEqual(before,{p:p.read_bytes() for p in before})

    def test_current_summary_keeps_structural_and_empirical_truth_separate(self):
        summary = review.summary(self.items)
        self.assertEqual(summary['total_tasks'],len(self.items))
        self.assertEqual(summary['accepted_tasks'],len(self.items))
        self.assertEqual(summary['items']['sogb-g003']['editorial'],'accepted')
        self.assertEqual(summary['admission_round'],'graph-7')
        self.assertFalse(summary['difficulty_calibrated'])
        self.assertFalse(summary['model_performance_measured'])
        self.assertEqual(self.items[2]['level'],'L1')
        self.assertTrue(all(not row.get('mathematical_necessity_certified',False) for row in summary['items'].values()))

    def test_disjoint_extension_keeps_base_verdicts_and_cannot_rebind_an_old_item(self):
        by_id = review.summary(self.items)['items']
        self.assertEqual(by_id['sogb-g008']['editorial'], 'accepted')
        self.assertEqual(by_id['sogb-g008']['review_round'], 'graph-extension-exercise17')
        base = review.apply_repair(self.items, review.statuses(self.items, review.CURRENT_ROUND),
                                   review.CURRENT_REPAIR_ROUND, review.CURRENT_ROUND)
        bound_ids = {row['id'] for row in json.loads(
            (review.CURRENT_ROUND / 'input.json').read_bytes())['items']}
        self.assertEqual({key: by_id[key] for key in bound_ids},
                         {key: base[key] for key in bound_ids})
        with self.assertRaisesRegex(ValueError, 'cannot supersede or overlap'):
            review.extension_statuses(self.items, review.ROUND.parent, {'sogb-g008'})
        changed = deepcopy(self.items)
        next(x for x in changed if x['id'] == 'sogb-g008')['question'] += ' Changed.'
        self.assertEqual(review.summary(changed)['items']['sogb-g008']['editorial'], 'stale')

    def test_content_or_source_changes_stale_only_affected_item(self):
        for key,value in (('question','Different question'), ('level','L5'), ('answer',{'nodes':[]})):
            changed = deepcopy(self.items)
            changed[0][key]=value
            rows=review.statuses(changed,review.CURRENT_ROUND)
            self.assertEqual(rows['sogb-g001']['editorial'],'stale')
            self.assertEqual(rows['sogb-g003']['editorial'],'accepted')
        changed=deepcopy(self.items)
        changed[0]['context']['source_sha256_lf']['changed']='source'
        self.assertEqual(review.statuses(changed,review.CURRENT_ROUND)['sogb-g001']['editorial'],'stale')

    def test_random_scan_extension_pins_the_safe_visible_projection(self):
        path = review.ROUND.parent / 'graph-extension-random-scan'
        old = path / 'preflight-answer-binding'
        identity = 'sogb-g009'
        graph = next(item for item in self.items if item['id'] == identity)
        accepted = review.summary(self.items)['items'][identity]
        self.assertEqual((accepted['editorial'], accepted['review_round']), ('accepted', path.name))
        self.assertEqual(review.statuses(self.items, old)[identity]['editorial'], 'repair-required')
        self.assertEqual(graph['family'], 'random-scan-null-atoms')
        self.assertEqual((len(graph['context']['nodes']), len(graph['context']['edges'])), (8, 5))
        self.assertEqual({name.rsplit('.', 1)[-1] for name in graph['answer']['nodes']},
                         {'randomScan_apply_singleton', 'heatBath_ae_apply_eq'})
        packet = json.loads((path / 'input.json').read_bytes())
        self.assertEqual(bench.text_hash(path / 'PrivateBalanceTrace.lean'),
                         packet['proof_occurrence_witness']['probe_sha256_lf'])
        self.assertEqual(graph['context']['snapshot_sha256'],
                         packet['proof_occurrence_witness']['public_snapshot_sha256'])
        actual = bench.curriculum.graph_prompt
        with patch.object(bench.curriculum, 'graph_prompt',
                          side_effect=lambda item: {**actual(item), 'changed_projection': True}):
            self.assertEqual(review.statuses(self.items, path)[identity]['editorial'], 'stale')

    def test_lower_bounds_extension_binds_first_answer_and_visible_prompt(self):
        directory = review.ROUND.parent / 'graph-extension-lower-bounds'
        identity = 'sogb-g010'
        graph = next(item for item in self.items if item['id'] == identity)
        packet = json.loads((directory / 'input.json').read_bytes())
        public = (directory / 'public-prompt.json').read_bytes()
        blind = (directory / 'blind-answer.json').read_bytes()
        self.assertEqual(public, bench.encoded(bench.curriculum.graph_prompt(graph)))
        self.assertEqual(bench.sha(public), packet['public_projection_sha256'][identity])
        self.assertEqual(bench.sha(blind),
                         'b0565ac0819d11d4ec2246451297a7c0626376add939b702d319cf8923ccf787')
        self.assertEqual(json.loads(blind), graph['answer'])
        status = review.summary(self.items)['items'][identity]
        self.assertEqual((status['editorial'], status['review_round'], status['mathematical_necessity_certified']),
                         ('accepted', directory.name, False))

    def test_feature_law_extension_distinguishes_direct_and_transitive_reuse(self):
        import sog_bench_graph_slices as slices

        identity = 'sogb-g011'
        item = next(row for row in self.items if row['id'] == identity)
        directory = review.ROUND.parent / 'graph-extension-feature-law'
        self.assertEqual((item['core_id'], item['family'], item['split'], item['level']),
                         ('sogb-032', 'sphere-feature-law-angular-transport', 'public-dev', 'L2'))
        paths, _ = slices.reference_paths(item)
        self.assertEqual({tuple(node.rsplit('.', 1)[-1] for node in path) for path in paths}, {
            ('quadratic_feature_law_gradient_angular_transport_control',
             'bounded_bochner_mean_quadratic_transport_control',
             'isProbabilityMeasure_of_isCoupling_left'),
            ('expectation_sub_le_linearCost_and_le_wassersteinDistance',
             'isProbabilityMeasure_of_isCoupling_left'),
        })
        public = (directory / 'public-prompt.json').read_bytes()
        self.assertEqual(public, bench.encoded(bench.curriculum.graph_prompt(item)))
        self.assertNotIn('answer', json.loads(public))
        self.assertEqual(json.loads((directory / 'blind-answer.json').read_bytes()), item['answer'])
        self.assertEqual(slices.artifact_for(identity), 'compiled-feature-law-graph.json')
        row = review.summary(self.items)['items'][identity]
        self.assertEqual((row['editorial'], row['review_round'], row['mathematical_necessity_certified']),
                         ('accepted', directory.name, False))

    def test_policy_or_scorer_changes_stale_every_original_decision(self):
        actual=review.payload
        originals = {row['id'] for row in json.loads(
            (review.CURRENT_ROUND / 'input.json').read_bytes())['items']}
        for key in ('policy_sha256_lf','scorer_source'):
            def changed(items):
                result=actual(items)
                result[key]='changed'
                return result
            with patch.object(review,'payload',side_effect=changed):
                rows = review.statuses(self.items, review.CURRENT_ROUND)
                self.assertTrue(all(row['editorial'] == ('stale' if identity in originals else 'pending')
                                    for identity, row in rows.items()))

    def test_only_exact_lower_bounds_addition_preserves_older_domain_policy(self):
        path = bench.curriculum.BASE / 'curriculum.json'
        active = path.read_text(encoding='utf-8')
        self.assertEqual(active.count(review.LOWER_BOUNDS_ADDITION), 1)
        previous = active.replace(review.LOWER_BOUNDS_ADDITION, '', 1)
        archived = json.loads((review.CURRENT_ROUND / 'input.json').read_bytes())['policy_sha256_lf']
        self.assertEqual(bench.sha(previous.encode()), archived)
        domains = review.reviewed_policy_domains(archived, bench.text_hash(path))
        self.assertEqual(domains, set(json.loads(previous)['domains']))
        self.assertNotIn('lower-bounds', domains)
        with tempfile.TemporaryDirectory() as tmp, patch.object(bench.curriculum, 'BASE', Path(tmp)):
            target = Path(tmp) / 'curriculum.json'
            for altered in (active.replace('Lower Bounds', 'Lower Bounds and Oracles'),
                            active.replace('Log-Concave Sampling', 'Sampling'),
                            active.replace('Author-assigned', 'Empirically assigned'),
                            active.replace(review.LOWER_BOUNDS_ADDITION,
                                           review.LOWER_BOUNDS_ADDITION + '    "extra": "Extra",\n')):
                with self.subTest(policy=bench.sha(altered.encode())):
                    target.write_bytes(altered.encode())
                    self.assertFalse(review.reviewed_policy_domains(archived, bench.text_hash(target)))

    def test_author_input_hash_necessity_and_open_repairs_cannot_self_admit(self):
        for case in ('actor','hash','necessity','repair','evidence'):
            with tempfile.TemporaryDirectory() as tmp:
                directory=Path(tmp)
                self.frozen_round(directory,review.ROUND)
                path=directory/'source-review.json'
                report=json.loads(path.read_text(encoding='utf-8'))
                if case=='actor':
                    report['actor_identity']=review.review.AUTHOR
                elif case=='hash':
                    report['input_packet_sha256']='wrong'
                elif case=='necessity':
                    report['items']['sogb-g001']['mathematical_necessity_certified']=True
                elif case=='repair':
                    report['items']['sogb-g001']['repair_requests']=['Unresolved']
                else:
                    report['items']['sogb-g001']['scoring_checks']=[]
                path.write_bytes(bench.encoded(report))
                with self.assertRaises(ValueError):
                    review.statuses(self.items,directory)

    def test_difficulty_repair_requires_distinct_actor_exact_input_and_no_extra_edit(self):
        for case in ('actor','hash','binding','necessity','extra-edit','repair','evidence'):
            with tempfile.TemporaryDirectory() as tmp:
                directory=Path(tmp)
                self.frozen_round(directory,review.REPAIR_ROUND)
                path=directory/'source-review.json'
                report=json.loads(path.read_text(encoding='utf-8'))
                if case=='actor':
                    report['actor_identity']=json.loads((review.ROUND/'source-review.json').read_text(encoding='utf-8'))['actor_identity']
                elif case=='hash':
                    report['input_packet_sha256']='wrong'
                elif case=='binding':
                    report['proposed_binding_sha256']='wrong'
                elif case=='necessity':
                    report['mathematical_necessity_certified']=True
                elif case=='extra-edit':
                    input_path=directory/'input.json'
                    proposal=json.loads(input_path.read_text(encoding='utf-8'))
                    proposal['proposed_after']['question']='A different task'
                    input_path.write_bytes(bench.encoded(proposal))
                    report['input_packet_sha256']=bench.sha(input_path.read_bytes())
                elif case=='repair':
                    report['verdict']='accept'
                    report['repair_requests']=['Unresolved']
                else:
                    report['minimality_checks']=[]
                path.write_bytes(bench.encoded(report))
                with self.assertRaises(ValueError):
                    review.apply_repair(self.items,review.statuses(self.items),directory)

    def test_repair_cannot_be_replayed_after_another_content_change(self):
        changed=deepcopy(self.items)
        changed[2]['answer']['nodes']=[]
        rows=review.apply_repair(changed,review.statuses(changed))
        self.assertEqual(rows['sogb-g003']['editorial'],'stale')

    def test_preparation_does_not_create_or_overwrite_a_verdict(self):
        with tempfile.TemporaryDirectory() as tmp:
            output=Path(tmp)/'input.json'
            review.prepare(output)
            self.assertFalse((output.parent/'source-review.json').exists())
            with self.assertRaises(ValueError):
                review.prepare(output)

    def test_new_policy_cannot_silently_supersede_history_without_actual_review(self):
        for field in ('input','report'):
            with tempfile.TemporaryDirectory() as tmp:
                directory=Path(tmp)
                self.frozen_round(directory,review.CURRENT_ROUND)
                target=directory/('input.json' if field=='input' else 'source-review.json')
                data=json.loads(target.read_text(encoding='utf-8'));data['supersedes_rounds']=[]
                target.write_bytes(bench.encoded(data))
                with patch.object(review,'CURRENT_ROUND',directory):
                    with self.assertRaises(ValueError):
                        review.summary(self.items)

    def test_historical_level_repair_is_preserved_but_not_replayed_under_new_policy(self):
        summary=review.summary(self.items)
        self.assertIsNone(summary['repair_round'])
        self.assertEqual(summary['items']['sogb-g002']['editorial'],'accepted')
        self.assertEqual(next(i for i in self.items if i['id']=='sogb-g002')['level'],'L1')
        old_base=review.ROUND.parent/'graph-4'
        old_repair=review.ROUND.parent/'graph-5'
        base=json.loads((old_base/'source-review.json').read_text(encoding='utf-8'))
        self.assertEqual(base['items']['sogb-g002']['verdict'],'repair-required')
        self.assertEqual(json.loads((old_repair/'source-review.json').read_text(encoding='utf-8'))['verdict'],'accept')
        self.assertEqual(review.apply_repair(self.items,review.statuses(self.items,old_base),old_repair,old_base)['sogb-g002']['editorial'],'stale')
        changed=deepcopy(self.items)
        changed[1]['question']+=' Unreviewed extra task.'
        self.assertEqual(review.summary(changed)['items']['sogb-g002']['editorial'],'stale')
        for key,value in (('actor_identity',base['actor_identity']),('base_round','graph-1'),
                          ('input_packet_sha256','wrong'),('proposed_binding_sha256','wrong'),
                          ('mathematical_necessity_certified',True),('repair_requests',['Unresolved'])):
            with tempfile.TemporaryDirectory() as tmp:
                directory=Path(tmp);self.frozen_round(directory,old_repair)
                path=directory/'source-review.json'
                report=json.loads(path.read_text(encoding='utf-8'));report[key]=value
                path.write_bytes(bench.encoded(report))
                with self.assertRaises(ValueError):
                    review.apply_repair(self.items,review.statuses(self.items,old_base),directory,old_base)

    def test_union_closure_gap_and_pre_repair_compiler_evidence_remain_auditable(self):
        before=review.ROUND.parent/'graph-6'
        report=json.loads((before/'source-review.json').read_text(encoding='utf-8'))
        self.assertEqual(report['items']['sogb-g006']['verdict'],'repair-required')
        self.assertEqual(report['items']['sogb-g007']['verdict'],'repair-required')
        snapshot=json.loads((before/'compiled-flow-before.json').read_text(encoding='utf-8'))
        self.assertNotIn('local_import_closure_sha256_lf',snapshot['provenance'])
        self.assertEqual(bench.text_hash(before/'compiler-before.py'),snapshot['provenance']['generator_sha256_lf'])
        old=json.loads((before/'input.json').read_text(encoding='utf-8'))
        item=next(i for i in old['items'] if i['id']=='sogb-g006')
        self.assertEqual(bench.sha((before/'compiled-flow-before.json').read_bytes()),item['context']['snapshot_sha256'])


if __name__=='__main__':
    unittest.main()
