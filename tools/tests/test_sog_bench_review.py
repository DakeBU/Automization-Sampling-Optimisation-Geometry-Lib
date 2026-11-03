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
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            bench.export(target, self.cores)
            questions = [json.loads(line) for line in (target/'reviewed-questions.jsonl').read_text(encoding='utf-8').splitlines()]
            refs = [json.loads(line) for line in (target/'reviewed-reference.jsonl').read_text(encoding='utf-8').splitlines()]
            self.assertEqual(len(questions), 10)
            self.assertEqual(len(refs), 7)
            self.assertEqual({q['id'] for q in questions}, {c['id'] for c in refs})
            self.assertTrue(all('steps' not in q and 'lean_reference' not in q for q in questions))
            self.assertTrue(all(q['id'] not in {f'sogb-{i:03d}' for i in range(8,15)} for q in questions))


if __name__ == '__main__':
    unittest.main()
