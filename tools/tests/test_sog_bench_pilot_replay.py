"""Offline verification of one actual archived pilot; no model or Lean runs."""
import io
import json
from pathlib import Path
import stat
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
import sog_bench_pilot_replay as replay

b, bridge, local = replay.bench, replay.bridge, replay.local


class RecordedPilotReplayTests(unittest.TestCase):
    def test_real_archive_replays_without_execution_and_matches_current_task(self):
        with (patch.object(local, 'CpuModel', side_effect=AssertionError('no model load')),
              patch.object(local.runtime, 'run_submission', side_effect=AssertionError('no Lean execution')),
              patch.object(bridge, 'require_runtime', side_effect=AssertionError('no Docker required'))):
            report = replay.replay(check_current_task=True)
        self.assertEqual((report['id'], report['selected'], report['recorded_score']), ('sogb-015', 1, 0))
        self.assertEqual((report['recorded_check'], report['recorded_final']),
                         ('proof-rejected', 'proof-rejected'))
        self.assertEqual(report['recorded_output_token_counts'], [21, 21])
        self.assertTrue(report['recorded_output_token_ids_equal'])
        self.assertTrue(report['recorded_proof_body_equal'])
        self.assertTrue(report['current_task_checked'])
        for key in ('model_rerun', 'lean_rerun', 'provenance_authenticated'):
            self.assertIs(report[key], False)

    def test_archive_pin_and_bounded_member_paths_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            archive = Path(tmp) / 'changed.zip'
            archive.write_bytes(replay.ARCHIVE.read_bytes() + b'changed')
            with self.assertRaisesRegex(ValueError, 'SHA-256 mismatch'):
                replay.replay(archive)
        for replacement, mode, message in (
            ('../outside.bin', stat.S_IFREG, 'Unexpected'),
            (min(replay.FILES), stat.S_IFLNK, 'bounded regular'),
        ):
            out = io.BytesIO()
            with zipfile.ZipFile(out, 'w') as archive:
                for name in sorted(replay.FILES):
                    info = zipfile.ZipInfo(replacement if name == min(replay.FILES) else name)
                    info.create_system = 3
                    info.external_attr = (mode if name == min(replay.FILES) else stat.S_IFREG) << 16
                    archive.writestr(info, b'fixture data, not an executable file')
            with self.subTest(replacement=replacement), self.assertRaisesRegex(ValueError, message):
                replay.archive_members(out.getvalue())

    def test_replay_checks_native_frame_exact_feedback_and_recorded_score(self):
        members = replay.archive_members(replay.ARCHIVE.read_bytes())
        cases = (
            ('workspace/actions/0002/verification/runtime-output.bin', lambda raw: raw + b'not JSON',
             'framed output'),
            ('workspace/actions/0002/verification/submission.txt', lambda raw: raw + b'--changed',
             'submitted source'),
            ('02-model.json',
             lambda raw: b.encoded({**json.loads(raw), 'messages': json.loads(raw)['messages'][:-1]}),
             'turn/source/workspace binding'),
            ('pilot-result.json', lambda raw: b.encoded({**json.loads(raw), 'score': 1}),
             'recorded pilot score'),
        )
        for name, mutate, message in cases:
            with self.subTest(name=name), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                changed = replay.EVIDENCE + name
                for path, raw in members.items():
                    dest = root / path
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    dest.write_bytes(mutate(raw) if path == changed else raw)
                with self.assertRaisesRegex(ValueError, message):
                    replay.replay_records(root)


if __name__ == '__main__':
    unittest.main()
