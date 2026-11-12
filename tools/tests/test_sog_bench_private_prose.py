"""Synthetic local workflow only; no real held-out tasks or measurements."""
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from tools.tests import test_sog_bench_split_guard as fixtures

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
import sog_bench_private_prose as run

guard = run.guard
SYNTHETIC_ADMISSION = {"public_tips": ["a" * 40], **{key: "b" * 64 for key in run.ADMISSION_DIGESTS}}


def fixture():
    reservation, packet = fixtures.synthetic_prose()
    for identity in ('missing-synthetic', 'unselected-synthetic'):
        task = {**packet['tasks'][0], 'id': identity, 'question': f'Synthetic prompt for {identity}'}
        packet['tasks'].append(task)
        reservation['families'][0]['tasks'].append({'id': identity, 'nl_prompt_sha256':
                                                    guard.prompt_digest(task['assumptions'], task['question'])})
    metadata = {'run_id': 'fixture-not-a-run', 'model': 'fixture-not-a-model', 'model_version': 'synthetic',
                'created_at': '2026-11-10T08:50:00+00:00', 'track': 'natural-language',
                'prompt_profile': run.PROFILE, 'attempt_policy': 'first-attempt', 'retrieval_profile': 'open-library',
                'tools': ['library search'], 'seed': None, 'decoding': {},
                'task_ids': ['missing-synthetic', 'candidate-one']}
    return reservation, packet, metadata


def response_object(plan_bytes, task, **changes):
    return {'schema_version': 1, 'plan_sha256': guard.digest(plan_bytes),
            'responses': [{'id': task['id'], 'prompt_sha256': guard.prose_prompt(task)['prompt_sha256'],
                           'track': 'natural-language', 'attempt': 1,
                           'response': 'Synthetic answer, not a model response.', **changes}]}


def judgment(worksheet):
    worksheet.update(grader_id='software-fixture-not-a-grader', adjudicated_at='2026-11-10T09:00:00+00:00')
    for item in worksheet['items'].values():
        for criterion in item['criteria']:
            criterion.update(score=int(criterion['criterion'] != 4), rationale='Synthetic worksheet fixture.')
    return worksheet


class PrivatePlanTests(unittest.TestCase):
    def test_policy_prompt_admission_and_response_drift_fail(self):
        _, packet, metadata = fixture()
        tasks = packet['tasks']
        admission = SYNTHETIC_ADMISSION
        plan, prompts, _ = run.plan_for(tasks, admission, metadata)
        plan_bytes = run.sealed(plan)
        digest = guard.digest(plan_bytes).encode()
        response = response_object(plan_bytes, tasks[0])
        with self.assertRaisesRegex(guard.GuardError, '^private-run-policy-drift$'):
            run.plan_for(tasks, admission, {**metadata, 'tools': []})
        for args, reason in (([tasks, admission, plan_bytes, b'0'*64, prompts, response], 'digest-mismatch'),
                             ([tasks, admission, plan_bytes, digest, prompts+b' ', response], 'plan-or-prompt-drift'),
                             ([tasks, {**admission, 'public_history_sha256': '0'*64}, plan_bytes, digest, prompts, response],
                              'plan-or-prompt-drift'),
                             ([tasks, admission, plan_bytes, digest, prompts, {**response, 'plan_sha256': '0'*64}],
                              'responses-plan-binding')):
            with self.subTest(reason=reason), self.assertRaisesRegex(guard.GuardError, f'^private-run-{reason}$'):
                run.archive_for(*args)
        for obj, reason in ((response_object(plan_bytes, tasks[0], attempt=2), 'response-binding'),
                            (response_object(plan_bytes, tasks[0], prompt_sha256='f'*64), 'response-binding'),
                            (response_object(plan_bytes, tasks[2]), 'unselected-or-duplicate-response'),
                            ({**response, 'responses': response['responses'] * 2}, 'unselected-or-duplicate-response')):
            with self.subTest(reason=reason), self.assertRaisesRegex(guard.GuardError, f'^private-run-{reason}$'):
                run.archive_for(tasks, admission, plan_bytes, digest, prompts, obj)

    def test_empty_first_responses_keep_all_selected_in_denominator(self):
        _, packet, metadata = fixture()
        tasks = packet['tasks']
        plan, prompts, _ = run.plan_for(tasks, SYNTHETIC_ADMISSION, metadata)
        raw = run.sealed(plan)
        sha = guard.digest(raw)
        archive = run.archive_for(tasks, SYNTHETIC_ADMISSION, raw, sha.encode(), prompts,
                                  {'schema_version': 1, 'plan_sha256': sha, 'responses': []})
        archive_sha = guard.digest(run.sealed(archive))
        snapshot = run.score_input(archive, archive_sha)
        template = run.prose.judgment_template(snapshot[1]['reference_cores'], [], archive_sha)
        report = run.prose.grade_snapshot(snapshot, judgment(template))
        self.assertEqual((report['points'], report['max_points'], report['missing_or_empty_count']), (0, 8, 2))
        self.assertEqual(report['split'], 'private-test')


@unittest.skipUnless(shutil.which('git'), 'Git executable needed for private admission replay')
class PrivateCLI(unittest.TestCase):
    def test_real_local_git_plan_archive_and_replay(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo, private = root / 'git-fixture', root / 'private-fixture'
            repo.mkdir()
            private.mkdir()

            def git(*args):
                return subprocess.check_output(['git', *args], cwd=repo, stderr=subprocess.STDOUT).strip()

            def store(name, data):
                path = private / name
                path.write_bytes(run.sealed(data) if isinstance(data, dict) else data)
                return str(path)

            def command(argv, code):
                out, err = StringIO(), StringIO()
                with patch.object(guard, 'ROOT', repo), redirect_stdout(out), redirect_stderr(err):
                    self.assertEqual(run.main(argv), code, err.getvalue())
                for value in (str(private), 'candidate-one', 'candidate-family', 'Synthetic nonpublic prompt',
                              'Synthetic answer', 'Criterion 0', 'fixture-not-a-model'):
                    self.assertNotIn(value, out.getvalue() + err.getvalue())
                return json.loads(out.getvalue() or err.getvalue())

            git('init', '-q')
            path = repo / guard.CATALOG
            path.parent.mkdir(parents=True)
            path.write_bytes(guard.canonical(fixtures.catalog(fixtures.public_core())))
            git('add', '--', guard.CATALOG)
            git('-c', 'user.name=Synthetic Fixture', '-c', 'user.email=fixture@example.invalid',
                '-c', 'commit.gpgsign=false', 'commit', '-qm', 'Synthetic public history')
            tip = git('rev-parse', 'HEAD').decode()
            _, exposure = guard.inventory(repo, [tip])
            reservation, packet, metadata = fixture()
            bindings, _ = guard.private_prose_packet(reservation, packet)
            review = fixtures.synthetic_review(reservation, exposure['public_history_sha256'], schema_version=2,
                                               prose_packet_sha256=bindings['candidate-family'])
            admission_args = ['--public-tip', tip, '--reservation', store('reservation.json', reservation),
                              '--prose-packet', store('task-packet.json', packet), '--review-file', store('review.json', review)]
            meta = store('metadata.json', metadata)
            self.assertEqual(command(['plan', *admission_args, '--run-metadata', meta, '--output',
                                      str(repo / 'ordinary-output')], 2)['reason'], 'reservation-must-stay-out-of-tracked-paths')
            self.assertFalse((repo / 'ordinary-output').exists())
            planned = private / 'planned'
            command(['plan', *admission_args, '--run-metadata', meta, '--output', str(planned)], 0)
            prompt_path = planned / 'prompts.jsonl'
            prompt_raw = prompt_path.read_bytes()
            self.assertEqual([json.loads(line)['id'] for line in prompt_raw.splitlines()], metadata['task_ids'])
            self.assertNotIn(b'operator-only', prompt_raw)
            self.assertNotIn(b'candidate-family', prompt_raw)
            self.assertNotIn(b'unselected-synthetic', prompt_raw)
            raw_plan = (planned / 'plan.json').read_bytes()
            plan_digest = store('separate-plan.sha256', (planned / 'plan.sha256').read_bytes())
            collected = private / 'collected'
            command(['archive', *admission_args, '--plan', str(planned / 'plan.json'), '--plan-digest', plan_digest,
                     '--prompts', str(prompt_path), '--responses', store('responses.json', response_object(raw_plan, packet['tasks'][0])),
                     '--output', str(collected)], 0)
            self.assertEqual({p.name for p in collected.iterdir()}, {'archive.json', 'archive.sha256', 'adjudication-template.json'})
            frozen = collected / 'archive.json'
            archive_digest = store('separate-archive.sha256', (collected / 'archive.sha256').read_bytes())
            sheet = judgment(json.loads((collected / 'adjudication-template.json').read_bytes()))
            report_path = private / 'score.json'
            grade = ['score', '--archive', str(frozen), '--archive-digest', archive_digest,
                     '--judgment', store('judgment.json', sheet), '--output', str(report_path)]
            raw_archive = frozen.read_bytes()
            frozen.write_bytes(raw_archive + b' ')
            self.assertEqual(command(grade, 2)['reason'], 'private-run-digest-mismatch')
            self.assertFalse(report_path.exists())
            frozen.write_bytes(raw_archive)
            command(grade, 0)
            report = json.loads(report_path.read_bytes())
            self.assertEqual((report['points'], report['max_points'], report['missing_or_empty_count']), (3, 8, 1))
            self.assertEqual(report['split'], 'private-test')
            for name in ('execution_verified', 'unseen_generalization_claim', 'grader_identity_authenticated', 'selection_timing_verified'):
                self.assertIs(report[name], False)
            replay = private / 'score-replay.json'
            command(grade[:-1] + [str(replay)], 0)
            self.assertEqual(report_path.read_bytes(), replay.read_bytes())
            command(grade, 2)  # Existing report cannot be overwritten.


if __name__ == '__main__':
    unittest.main()
