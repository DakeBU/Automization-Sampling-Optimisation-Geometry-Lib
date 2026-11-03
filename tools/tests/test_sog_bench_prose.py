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
