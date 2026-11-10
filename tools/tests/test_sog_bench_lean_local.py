"""Test the local transport wiring without a model, Docker, or proof scores."""
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
import sog_bench_lean_local as local

b, bridge = local.bench, local.bridge


class LocalModelPilotTests(unittest.TestCase):
    def test_actual_asset_pin_and_local_digest_gate(self):
        pin = local.asset_pin()
        self.assertEqual(pin['model'], 'Qwen/Qwen2.5-0.5B-Instruct')
        self.assertEqual(pin['revision'], '7ae557604adf67be50417f59c2c2f167def9a775')
        self.assertEqual(len(pin['asset_sha256']), 8)
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            file = directory / 'model.safetensors'
            file.write_bytes(b'not an actual weight file')
            expected = {'asset_sha256': {file.name: local.digest(file)}}
            self.assertEqual(local.check_assets(directory, expected), expected['asset_sha256'])
            file.write_bytes(b'different')
            with self.assertRaisesRegex(ValueError, 'hash mismatch'):
                local.check_assets(directory, expected)
            (directory / 'not-allowed.py').write_bytes(b'data')
            with self.assertRaisesRegex(ValueError, 'exact local model'):
                local.check_assets(directory, expected)

    def test_exact_diagnostic_reaches_second_turn_and_submissions_are_unedited(self):
        bodies = ['```lean\n  wrong\n```', '  exact h']
        seen = []
        def generate(messages):
            seen.append(messages)
            return {'input_ids': [1], 'output_ids': [2], 'raw_text': bodies[len(seen)-1]}
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            prefix = 'example (h : True) : True := by\n'
            visible = bridge.line({'kind': 'fixed-target-lean-prompt'})
            pilot = local.FeedbackPilot(prefix.encode()+local.MARKER, visible, generate, output)
            pilot.emit(visible)
            first = pilot.readline(bridge.MAX_REQUEST)
            self.assertEqual(bridge.request(first), {'action': 'check', 'source': prefix+bodies[0]})
            with self.assertRaisesRegex(OSError, 'actual feedback'):
                pilot.readline(bridge.MAX_REQUEST)
            feedback = {'sequence': 1, 'action': 'check', 'kind': 'proof-rejected',
                        'diagnostic': 'fixture diagnostic', 'diagnostic_truncated': False}
            diag = feedback['diagnostic'].encode()
            check = bridge.line({'kind': 'lean-workspace-feedback', 'feedback': feedback})
            pilot.emit(check)
            final = pilot.readline(bridge.MAX_REQUEST)
            self.assertEqual(bridge.request(final), {'action': 'submit', 'source': prefix+bodies[1]})
            self.assertEqual(seen[1][2], {'role': 'assistant', 'content': bodies[0]})
            self.assertEqual(seen[1][3], local.feedback_message(check))
            with self.assertRaisesRegex(OSError, 'actual feedback'):
                pilot.readline(bridge.MAX_REQUEST)
            archive = output / 'bridge'
            archive.mkdir()
            (archive / '0001-request.bin').write_bytes(first)
            (archive / '0002-request.bin').write_bytes(final)
            (archive / '0001-feedback.json').write_bytes(b.encoded(feedback))
            native = output / 'workspace/actions/0001/verification'
            native.mkdir(parents=True)
            (native / 'compiler-diagnostic.bin').write_bytes(diag)
            events = [{'action': a, 'source_sha256': b.sha((prefix + body).encode()),
                       'result': {'kind': k, 'submission_sha256': b.sha((prefix + body).encode()),
                                  'compiler_diagnostic_sha256': b.sha(diag)}}
                      for a, k, body in zip(('check', 'submit'), ('proof-rejected', 'accepted'), bodies)]
            self.assertEqual(len(local.verify_live_records(output, prefix, events)), 4)
            (native / 'compiler-diagnostic.bin').write_bytes(b'drift')
            with self.assertRaisesRegex(ValueError, 'feedback does not match'):
                local.verify_live_records(output, prefix, events)

    def test_wrong_prompt_never_runs_model_and_inference_error_is_transport(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            def fail(messages):
                raise RuntimeError('fixture backend failure')
            pilot = local.FeedbackPilot(b'prefix\n'+local.MARKER, b'visible', fail, output)
            with self.assertRaisesRegex(OSError, 'prompt differs'):
                pilot.emit(b'not the frozen prompt')
            self.assertEqual(pilot.turns, 0)
            pilot.emit(b'visible')
            with self.assertRaisesRegex(OSError, 'did not return'):
                pilot.readline(bridge.MAX_REQUEST)
            self.assertTrue((output / '01-model-failure.json').is_file())
            self.assertFalse((output / '01-model.json').exists())

    def test_runtime_gate_precedes_model_assets_and_candidate_handling(self):
        with (patch.object(bridge.sys, 'platform', 'win32'),
              patch.object(local, 'check_assets') as model,
              patch.object(local.runtime, 'checked_packet') as task):
            with self.assertRaisesRegex(RuntimeError, 'no host Lean fallback'):
                local.run(ROOT, ROOT, ROOT, ROOT, ROOT)
        model.assert_not_called()
        task.assert_not_called()


if __name__ == '__main__':
    unittest.main()
