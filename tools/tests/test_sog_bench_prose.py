"""Human-scoring workflow tests; fixture scores are not model measurements."""
from copy import deepcopy
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

    def test_preselected_run_binds_exact_conditions_and_missing_denominator(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            selection, run = root/'selection', root/'scoring'
            metadata = self.metadata()
            digest = prose.freeze_selection(self.cores, metadata, selection)
            self.assertEqual({p.name for p in selection.iterdir()}, {'selection.json', 'prompts.jsonl'})
            prompts = (selection/'prompts.jsonl').read_bytes()
            rows = [json.loads(line) for line in prompts.splitlines()]
            self.assertEqual([row['id'] for row in rows], metadata['task_ids'])
            self.assertTrue(all(row['track'] == 'natural-language' and
                                not {'rubric', 'steps', 'lean_reference', 'source_file'} & row.keys()
                                for row in rows))
            receipt = json.loads((selection/'selection.json').read_bytes())
            self.assertEqual(receipt['run_metadata'], metadata)
            self.assertEqual(receipt['prompts_sha256'], bench.sha(prompts))
            prose.prepare(self.cores, self.responses(), None, run,
                          selection=selection, selection_sha256=digest)
            self.assertEqual((run/'prompts.jsonl').read_bytes(), prompts)
            self.assertEqual((run/'selection.json').read_bytes(), (selection/'selection.json').read_bytes())
            manifest, _ = prose.load_packet(run)
            self.assertEqual(manifest['schema_version'], 2)
            with patch.object(bench, 'materialize', side_effect=AssertionError('Use archived inputs only')):
                report = prose.adjudicate(run, self.judgment(run), selection_sha256=digest)
            self.assertEqual(report['max_points'], 8)
            self.assertEqual(report['missing_or_empty_count'], 1)
            self.assertEqual(report['selection_receipt_sha256'], digest)
            self.assertTrue(report['selection_external_digest_checked'])
            self.assertFalse(report['selection_timing_verified'])
            self.assertFalse(report['execution_verified'])
            self.assertFalse(prose.adjudicate(run, self.judgment(run))['selection_external_digest_checked'])

    def test_preselection_requires_anchor_and_current_admission_without_replacing_prompt(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            selection, run = root/'selection', root/'scoring'
            metadata = self.metadata()
            digest = prose.freeze_selection(self.cores, metadata, selection)
            with self.assertRaises(FileExistsError):
                prose.freeze_selection(self.cores, metadata, selection)
            for value in ('0'*64, None):
                with self.assertRaisesRegex(ValueError, 'separately recorded'):
                    prose.prepare(self.cores, [], None, run, selection=selection, selection_sha256=value)
            with self.assertRaisesRegex(ValueError, 'never both'):
                prose.prepare(self.cores, [], metadata, run, selection=selection, selection_sha256=digest)
            with patch.object(bench, 'editorial_review', return_value={'items': {}}):
                with self.assertRaisesRegex(ValueError, 'current editorial admission'):
                    prose.freeze_selection(self.cores, metadata, root/'unreviewed')
                with self.assertRaisesRegex(ValueError, 'current editorial admission'):
                    prose.prepare(self.cores, [], None, run, selection=selection, selection_sha256=digest)
            prompts = selection/'prompts.jsonl'
            prompts.write_bytes(prompts.read_bytes() + b'\n')
            with self.assertRaisesRegex(ValueError, 'prompt bytes'):
                prose.prepare(self.cores, [], None, run, selection=selection, selection_sha256=digest)
            self.assertFalse(run.exists())

    def test_preselection_rejects_resigned_conditions_or_rubric(self):
        for change in ('operator-conditions', 'frozen-rubric', 'run-order'):
            with self.subTest(change=change), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                selection, run = root/'selection', root/'scoring'
                digest = prose.freeze_selection(self.cores, self.metadata(), selection)
                if change == 'operator-conditions':
                    receipt = json.loads((selection/'selection.json').read_bytes())
                    receipt['run_metadata']['retrieval_profile'] = 'closed-book'
                    (selection/'selection.json').write_bytes(bench.encoded(receipt))
                    with self.assertRaisesRegex(ValueError, 'separately recorded'):
                        prose.prepare(self.cores, [], None, run, selection=selection, selection_sha256=digest)
                    self.assertFalse(run.exists())
                    continue
                prose.prepare(self.cores, self.responses(), None, run,
                              selection=selection, selection_sha256=digest)
                packet_path, manifest_path = run/'rubric-packet.json', run/'manifest.json'
                packet, manifest = json.loads(packet_path.read_bytes()), json.loads(manifest_path.read_bytes())
                if change == 'frozen-rubric':
                    packet['reference_cores'][0]['rubric'][0]['criterion'] = 'An easier grading target.'
                else:
                    packet['reference_cores'].reverse()
                    packet['run_metadata']['task_ids'].reverse()
                    manifest['task_ids'].reverse()
                    raw = bench.encoded(packet['run_metadata'])
                    (run/'run-metadata.json').write_bytes(raw)
                    manifest['files']['run-metadata.json'] = bench.sha(raw)
                    raw = prose.prose_prompts(packet['reference_cores'])
                    (run/'prompts.jsonl').write_bytes(raw)
                    manifest['files']['prompts.jsonl'] = bench.sha(raw)
                raw = bench.encoded(packet)
                packet_path.write_bytes(raw)
                manifest['files']['rubric-packet.json'] = bench.sha(raw)
                manifest_path.write_bytes(bench.encoded(manifest))
                with self.assertRaisesRegex(ValueError, 'exact public reference core|does not match the scored tasks'):
                    prose.load_packet(run)

    def test_score_rejects_wrong_anchor_or_retroactive_anchor(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            digest = prose.freeze_selection(self.cores, self.metadata(), root/'selection')
            prose.prepare(self.cores, [], None, root/'preselected',
                          selection=root/'selection', selection_sha256=digest)
            prose.prepare(self.cores, [], self.metadata(), root/'legacy')
            for lane, anchor in (('preselected', '0'*64), ('legacy', digest)):
                run = root/lane
                with self.assertRaises(ValueError):
                    prose.adjudicate(run, self.judgment(run), selection_sha256=anchor)
            legacy = prose.adjudicate(root/'legacy', self.judgment(root/'legacy'))
            self.assertIsNone(legacy['selection_receipt_sha256'])
            self.assertFalse(legacy['selection_external_digest_checked'])

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


if __name__=='__main__':
    unittest.main()
