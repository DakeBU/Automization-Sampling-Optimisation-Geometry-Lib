"""Human-scoring workflow tests; fixture scores are not model measurements."""
from copy import deepcopy
from contextlib import redirect_stdout
from io import StringIO
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT/'tools'), str(ROOT/'website/scripts')]
import sog_bench as bench
import sog_bench_prose as prose


class ProseRunTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source_patch = patch.object(bench.astis_site, '_SOURCE_BY_NAME',
            {d.full_name:d for d in bench.astis_site.scan_project_sources()[1]})
        cls.source_patch.start()
        cls.addClassCleanup(cls.source_patch.stop)
        cls.cores = bench.materialize()
        cls.by_id = {c['id']:c for c in cls.cores}

    def metadata(self):
        return {'run_id':'software-test-fixture', 'model':'not-an-evaluated-model', 'model_version':'fixture',
                'created_at':'2026-11-03T10:00:00+08:00', 'track':'natural-language',
                'prompt_profile':'catalog-question', 'attempt_policy':'first-attempt',
                'retrieval_profile':'open-library', 'tools':[], 'seed':None, 'decoding':{},
                'task_ids':['sogb-015','sogb-017']}

    def responses(self, text='A serialization fixture, not a real model answer.'):
        return [{'id':'sogb-015','binding_sha256':self.by_id['sogb-015']['binding_sha256'],
                 'track':'natural-language','attempt':1,'response':text}]

    def judgment(self, directory):
        data = json.loads((directory/'adjudication-template.json').read_text(encoding='utf-8'))
        data.update(grader_id='software-fixture-not-a-human-evaluation',
                    adjudicated_at='2026-11-03T10:30:00+08:00')
        for row in data['items'].values():
            for i, criterion in enumerate(row['criteria']):
                criterion.update(score=i%2, rationale='Software fixture only; no mathematical judgment measured.')
        return data

    def test_packet_separates_prompts_from_gold_and_preserves_missing_denominator(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            prose.prepare(self.cores, self.responses(), self.metadata(), directory)
            prompts = [json.loads(line) for line in (directory/'prompts.jsonl').read_text(encoding='utf-8').splitlines()]
            self.assertEqual(len(prompts), 2)
            self.assertTrue(all('steps' not in row and 'rubric' not in row and 'lean_reference' not in row for row in prompts))
            report = prose.adjudicate(directory, self.judgment(directory))
            self.assertEqual((report['points'],report['max_points']), (2,8))
            self.assertEqual(report['missing_or_empty_count'],1)
            self.assertFalse(report['execution_verified'])
            self.assertFalse(report['judgments_automatically_verified'])
            self.assertFalse(report['unseen_generalization_claim'])
            self.assertIsNone(report['registered_plan_sha256'])

    def test_pre_response_plan_cli_seals_ordered_prompts_and_keeps_misses(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            metadata, responses = root/'metadata.json', root/'responses.jsonl'
            metadata.write_bytes(bench.encoded(self.metadata()))
            responses.write_bytes(prose.jsonl(self.responses()))
            planned, run = root/'planned', root/'run'
            args = ['sog_bench_prose.py', 'plan', '--run-metadata', str(metadata), '--output', str(planned)]
            with patch.object(sys, 'argv', args), patch.object(bench, 'materialize', return_value=self.cores), redirect_stdout(StringIO()) as out:
                self.assertEqual(prose.main(), 0)
            self.assertEqual({p.name for p in planned.iterdir()}, {'plan.json', 'prompts.jsonl'})
            raw = (planned/'plan.json').read_bytes()
            digest = bench.sha(raw)
            self.assertIn(digest, out.getvalue())
            prompts = (planned/'prompts.jsonl').read_bytes()
            plan = json.loads(raw)
            self.assertEqual(plan['prompt_sha256'], bench.sha(prompts))
            self.assertEqual([r['id'] for r in plan['task_bindings']], self.metadata()['task_ids'])
            self.assertNotIn(b'"rubric"', prompts)
            self.assertNotIn(b'"response"', prompts)
            with self.assertRaises(ValueError):
                prose.register_plan(self.cores, self.metadata(), planned)
            args = ['sog_bench_prose.py', 'prepare', '--plan', str(planned/'plan.json'), '--plan-sha256', digest,
                    '--submissions', str(responses), '--output', str(run)]
            with patch.object(sys, 'argv', args), patch.object(bench, 'materialize', return_value=self.cores), redirect_stdout(StringIO()):
                self.assertEqual(prose.main(), 0)
            self.assertEqual((run/prose.PLAN_FILE).read_bytes(), raw)
            self.assertEqual((run/'prompts.jsonl').read_bytes(), prompts)
            manifest, _ = prose.load_packet(run)
            self.assertEqual(manifest['schema_version'], 2)
            self.assertEqual(manifest['files'][prose.PLAN_FILE], digest)
            first = {**self.judgment(run), 'grader_id': 'fixture-A', 'independent_initial_grade_attested': True}
            second = {**first, 'grader_id': 'fixture-B'}
            for report in (prose.adjudicate(run, first), prose.adjudicate_panel(run, first, second)):
                self.assertEqual(report['registered_plan_sha256'], digest)
                self.assertEqual(report['missing_or_empty_count'], 1)
                self.assertFalse(report['selection_timing_verified'])

    def test_plan_rejects_reordered_tasks_changed_conditions_and_wrong_receipt(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            digest = prose.register_plan(self.cores, self.metadata(), root/'plan')
            raw = (root/'plan'/'plan.json').read_bytes()
            changed = [{**self.metadata(), 'task_ids': ['sogb-017', 'sogb-015']},
                       {**self.metadata(), 'model_version': 'another'},
                       {**self.metadata(), 'retrieval_profile': 'closed-book'}]
            for metadata in changed:
                with self.assertRaises(ValueError):
                    prose.prepare(self.cores, self.responses(), metadata, root/'run',
                                  plan_bytes=raw, expected_plan_sha256=digest)
            for offered in (None, 'f' * 64):
                with self.assertRaises(ValueError):
                    prose.prepare(self.cores, self.responses(), self.metadata(), root/'run',
                                  plan_bytes=raw, expected_plan_sha256=offered)
            with patch.object(bench, 'load', return_value={**bench.load(), 'version': 'unrelated-fixture-version'}):
                with self.assertRaises(ValueError):
                    prose.prepare(self.cores, self.responses(), self.metadata(), root/'run',
                                  plan_bytes=raw, expected_plan_sha256=digest)
            self.assertFalse((root/'run').exists())

    def test_archived_plan_cannot_disagree_with_frozen_run_even_if_rehashed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            planned, run = root/'plan', root/'run'
            digest = prose.register_plan(self.cores, self.metadata(), planned)
            raw = (planned/'plan.json').read_bytes()
            prose.prepare(self.cores, self.responses(), self.metadata(), run,
                          plan_bytes=raw, expected_plan_sha256=digest)
            changed = json.loads(raw)
            changed['task_bindings'].reverse()
            changed_bytes = bench.encoded(changed)
            (run/prose.PLAN_FILE).write_bytes(changed_bytes)
            packet_path, manifest_path = run/'rubric-packet.json', run/'manifest.json'
            packet, manifest = (json.loads(p.read_bytes()) for p in (packet_path, manifest_path))
            packet['registered_plan_sha256'] = bench.sha(changed_bytes)
            packet_path.write_bytes(bench.encoded(packet))
            manifest['files'][prose.PLAN_FILE] = bench.sha(changed_bytes)
            manifest['files']['rubric-packet.json'] = bench.sha(packet_path.read_bytes())
            manifest_path.write_bytes(bench.encoded(manifest))
            with self.assertRaises(ValueError):
                prose.load_packet(run)

    def test_empty_or_missing_outputs_get_zero_without_fake_human_grades(self):
        for responses in ([], self.responses('   ')):
            with tempfile.TemporaryDirectory() as tmp:
                directory = Path(tmp)
                prose.prepare(self.cores, responses, self.metadata(), directory)
                judgment = self.judgment(directory)
                self.assertEqual(judgment['items'], {})
                report = prose.adjudicate(directory, judgment)
                self.assertEqual((report['points'],report['max_points']), (0,8))
                self.assertEqual(report['missing_or_empty_count'],2)

    def test_rejects_unknown_duplicate_stale_attempt_and_track_records(self):
        base = self.responses()[0]
        for rows in ([base,base], [{**base,'id':'unknown'}], [{**base,'binding_sha256':'stale'}],
                     [{**base,'attempt':True}], [{**base,'attempt':2}], [{**base,'track':'lean'}],
                     [{**base,'response':None}]):
            with tempfile.TemporaryDirectory() as tmp:
                with self.assertRaises(ValueError):
                    prose.prepare(self.cores, rows, self.metadata(), Path(tmp))

    def test_metadata_declares_selection_profile_model_and_timezone(self):
        for key,value in (('model_version',''), ('created_at','2026-11-03'),
                          ('attempt_policy','best-of-10'), ('task_ids',[]),
                          ('task_ids',['sogb-015','sogb-015']), ('task_ids',['unknown']),
                          ('tools','none'), ('decoding',None), ('seed',True),
                          ('retrieval_profile','verified-private')):
            with self.assertRaises(ValueError):
                prose.validate_metadata({**self.metadata(),key:value}, self.cores)

    def test_sealed_bytes_or_frozen_selection_cannot_change(self):
        for name in prose.SEALED_FILES:
            with tempfile.TemporaryDirectory() as tmp:
                directory = Path(tmp)
                prose.prepare(self.cores,self.responses(),self.metadata(),directory)
                path = directory/name
                path.write_bytes(path.read_bytes()+b'\n')
                with self.assertRaises(ValueError):
                    prose.load_packet(directory)

    def test_incomplete_boolean_or_rewritten_rubric_grades_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            prose.prepare(self.cores,self.responses(),self.metadata(),directory)
            original = self.judgment(directory)
            cases = []
            for key,value in (('grader_kind','unvalidated-ai'), ('grader_id',''),
                              ('adjudicated_at','2026-11-02T10:00:00+08:00'), ('packet_sha256','wrong'),
                              ('items',{})):
                cases.append({**deepcopy(original),key:value})
            for key,value in (('score',True), ('score',2), ('rationale',''), ('criterion_text','different rubric')):
                changed = deepcopy(original)
                changed['items']['sogb-015']['criteria'][0][key] = value
                cases.append(changed)
            duplicate = deepcopy(original)
            duplicate['items']['sogb-015']['criteria'][1]['criterion']=1
            cases.append(duplicate)
            response = deepcopy(original)
            response['items']['sogb-015']['response_sha256']='different response'
            cases.append(response)
            malformed = deepcopy(original)
            malformed['items']['sogb-015']['criteria'][0] = 'not a criterion'
            cases.append(malformed)
            for judgment in cases:
                with self.assertRaises(ValueError):
                    prose.adjudicate(directory,judgment)

    def test_packet_can_be_scored_as_frozen_archive_without_current_catalog(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            prose.prepare(self.cores,self.responses(),self.metadata(),directory)
            with patch.object(bench,'materialize',side_effect=AssertionError('Do not reinterpret historical responses')):
                report = prose.adjudicate(directory,self.judgment(directory))
            self.assertEqual(report['catalog_version'],bench.load()['version'])

    def test_archived_responses_still_require_unique_exact_question_bindings(self):
        for case in ('duplicate','binding','selection'):
            with tempfile.TemporaryDirectory() as tmp:
                directory=Path(tmp)
                prose.prepare(self.cores,self.responses(),self.metadata(),directory)
                packet_path=directory/'rubric-packet.json'
                packet=json.loads(packet_path.read_text(encoding='utf-8'))
                if case=='duplicate':
                    packet['responses']*=2
                elif case=='binding':
                    packet['responses'][0]['binding_sha256']='wrong'
                else:
                    packet['responses'][0]['id']='unselected'
                responses=prose.jsonl(packet['responses'])
                packet_path.write_bytes(bench.encoded(packet))
                (directory/'responses.jsonl').write_bytes(responses)
                manifest_path=directory/'manifest.json'
                manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
                manifest['files']['rubric-packet.json']=bench.sha(packet_path.read_bytes())
                manifest['files']['responses.jsonl']=bench.sha(responses)
                manifest_path.write_bytes(bench.encoded(manifest))
                with self.assertRaises(ValueError):
                    prose.load_packet(directory)

    def test_model_text_is_never_executed_and_existing_run_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory=Path(tmp)
            text='import os; os.system("this is inert answer text, never executed")'
            prose.prepare(self.cores,self.responses(text),self.metadata(),directory)
            with patch('subprocess.run',side_effect=AssertionError('Never execute model answers')):
                report=prose.adjudicate(directory,self.judgment(directory))
            self.assertEqual(report['max_points'],8)
            with self.assertRaises(ValueError):
                prose.prepare(self.cores,self.responses(),self.metadata(),directory)

    def panel_fixture(self, directory, *, disagree=True, missing_all=False):
        prose.prepare(self.cores, [] if missing_all else self.responses(), self.metadata(), directory)
        first = self.judgment(directory)
        first.update(grader_id='fixture-grader-A', independent_initial_grade_attested=True)
        second = deepcopy(first)
        second.update(grader_id='fixture-grader-B', adjudicated_at='2026-11-03T10:45:00+08:00')
        if disagree:
            second['items']['sogb-015']['criteria'][0]['score'] = 1
        return first, second

    def test_panel_preserves_both_grades_and_resolves_only_disputes(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            a, b = self.panel_fixture(directory)
            worksheet = prose.panel_template(directory, a, b)
            self.assertEqual(set(worksheet['items']), {'sogb-015'})
            self.assertEqual(set(worksheet['items']['sogb-015']), {'1'})
            self.assertEqual(worksheet['items']['sogb-015']['1']['initial_scores'], [0, 1])
            self.assertIsNone(worksheet['items']['sogb-015']['1']['score'])
            with self.assertRaises(ValueError):
                prose.adjudicate_panel(directory, a, b)
            resolution = deepcopy(worksheet)
            resolution.update(resolver_id='fixture-resolver', resolved_at='2026-11-03T11:00:00+08:00')
            resolution['items']['sogb-015']['1'].update(score=1, rationale='Fixture resolution only')
            report = prose.adjudicate_panel(directory, a, b, resolution)
            self.assertEqual((report['points'], report['max_points'], report['missing_or_empty_count']), (3, 8, 1))
            self.assertEqual(report['initial_adjudication_sha256'], [bench.sha(bench.encoded(s)) for s in (a, b)])
            self.assertEqual(report['resolution_sha256'], bench.sha(bench.encoded(resolution)))
            self.assertEqual([report['criterion_agreement'][k] for k in ('agreed', 'disputed', 'compared')], [3, 1, 4])
            self.assertEqual([g['score'] for g in report['results'][0]['criteria'][0]['initial_grades']], [0, 1])
            self.assertEqual(report['results'][0]['criteria'][0]['resolution']['rationale'], 'Fixture resolution only')
            self.assertIsNone(report['results'][0]['criteria'][1]['resolution'])
            self.assertEqual(report['results'][1]['criteria'], [])
            self.assertFalse(report['grader_identity_authenticated'])
            self.assertFalse(report['unseen_generalization_claim'])

    def test_panel_rejects_grade_and_resolution_substitution(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            a, b = self.panel_fixture(directory)
            for key, value in (('grader_id', ' Fixture-Grader-a '), ('independent_initial_grade_attested', False),
                               ('independent_initial_grade_attested', 1), ('packet_sha256', 'wrong')):
                with self.assertRaises(ValueError):
                    prose.panel_template(directory, a, {**b, key: value})
            resolution = prose.panel_template(directory, a, b)
            resolution.update(resolver_id='fixture-resolver', resolved_at='2026-11-03T11:00:00+08:00')
            resolution['items']['sogb-015']['1'].update(score=1, rationale='Fixture resolution only')
            for key, value in (('resolver_id', 'FIXTURE-grader-b'), ('resolver_kind', 'ai'),
                               ('resolved_at', '2026-11-03T10:35:00+08:00'), ('items', {}),
                               ('packet_sha256', 'wrong')):
                with self.assertRaises(ValueError):
                    prose.adjudicate_panel(directory, a, b, {**resolution, key: value})
            for key, value in (('score', True), ('rationale', ''), ('initial_scores', [False, True]),
                               ('criterion_text', 'changed rubric')):
                changed = deepcopy(resolution)
                changed['items']['sogb-015']['1'][key] = value
                with self.assertRaises(ValueError):
                    prose.adjudicate_panel(directory, a, b, changed)
            override = deepcopy(resolution)
            override['items']['sogb-015']['2'] = override['items']['sogb-015']['1']
            with self.assertRaises(ValueError):
                prose.adjudicate_panel(directory, a, b, override)
            with self.assertRaises(ValueError):
                prose.adjudicate_panel(directory, b, a, resolution)

    def test_unanimous_panel_never_requires_or_permits_an_extra_grade(self):
        for empty in (False, True):
            with tempfile.TemporaryDirectory() as tmp:
                directory = Path(tmp)
                a, b = self.panel_fixture(directory, disagree=False, missing_all=empty)
                worksheet = prose.panel_template(directory, a, b)
                self.assertEqual(worksheet['items'], {})
                report = prose.adjudicate_panel(directory, a, b)
                self.assertEqual(report['criterion_agreement']['compared'], 0 if empty else 4)
                self.assertEqual(report['missing_or_empty_count'], 2 if empty else 1)
                self.assertIsNone(report['resolver'])
                with self.assertRaises(ValueError):
                    prose.adjudicate_panel(directory, a, b, worksheet)

    def test_panel_cli_uses_the_frozen_packet_and_does_not_overwrite_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            run = directory/'run'
            a, b = self.panel_fixture(run)
            first, second = directory/'grader-a.json', directory/'grader-b.json'
            first.write_bytes(bench.encoded(a))
            second.write_bytes(bench.encoded(b))
            flags = ['--packet', str(run), '--adjudication', str(first), '--second-adjudication', str(second)]
            worksheet = directory/'disputes.json'
            with patch.object(sys, 'argv', ['sog_bench_prose.py', 'panel-template', *flags, '--output', str(worksheet)]), redirect_stdout(StringIO()):
                self.assertEqual(prose.main(), 0)
            resolved = json.loads(worksheet.read_bytes())
            resolved.update(resolver_id='fixture-resolver', resolved_at='2026-11-03T11:00:00+08:00')
            resolved['items']['sogb-015']['1'].update(score=0, rationale='Fixture resolution only')
            completed = directory/'resolved.json'
            completed.write_bytes(bench.encoded(resolved))
            output = directory/'result.json'
            args = ['sog_bench_prose.py', 'score-panel', *flags, '--resolution', str(completed), '--output', str(output)]
            with patch.object(sys, 'argv', args), redirect_stdout(StringIO()):
                self.assertEqual(prose.main(), 0)
                saved = output.read_bytes()
                with self.assertRaises(ValueError):
                    prose.main()
            self.assertEqual(output.read_bytes(), saved)
            self.assertEqual(json.loads(saved)['points'], 2)

    def test_family_macro_is_not_duplicated_task_weight_and_uses_selected_denominators(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            task_ids = ['sogb-007', 'sogb-009', 'sogb-015']
            submissions = [{**self.responses()[0], 'id': i, 'binding_sha256': self.by_id[i]['binding_sha256']}
                           for i in ('sogb-007', 'sogb-015')]
            prose.prepare(self.cores, submissions, {**self.metadata(), 'task_ids': task_ids}, directory)
            scores = self.judgment(directory)
            for i, row in scores['items'].items():
                for c in row['criteria']:
                    c['score'] = int(i == 'sogb-007')
            report = prose.adjudicate(directory, scores)
            self.assertEqual((report['points'], report['max_points'], report['selected_families']), (4, 12, 2))
            self.assertEqual(report['breakdown']['family_macro_rate'], {'numerator': 1, 'denominator': 4})
            shared = report['breakdown']['by_family'][self.by_id['sogb-007']['family']]
            self.assertEqual((shared['selected_cores'], shared['max_points'], shared['missing_or_empty_count']), (2, 8, 1))
            level = self.by_id['sogb-009']['track_levels']['natural-language']
            self.assertEqual(report['breakdown']['by_level'][level]['missing_or_empty_count'], 1)
            path = directory/'result.json'
            prose.write_new_report(path, report)
            before = path.read_bytes()
            with self.assertRaises(ValueError):
                prose.write_new_report(path, {})
            self.assertEqual(path.read_bytes(), before)


if __name__=='__main__':
    unittest.main()
