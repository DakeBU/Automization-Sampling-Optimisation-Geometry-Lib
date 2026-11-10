"""Bounded pipe and fixed-target lifecycle fixtures; no Lean is executed here."""
from __future__ import annotations

import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import sog_bench_lean_stdio as bridge
from tools.tests import test_sog_bench_lean_model as fixture

workspace = bridge.workspace
runtime = bridge.runtime


class StdioBridgeTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.output = self.root / 'transcript'
        provenance = {**fixture.provenance(), 'provider': 'controlled-stdio',
                      'kind': 'controlled-software-fixture', 'transport': bridge.PROFILE}
        with patch.object(fixture, 'provenance', return_value=provenance):
            self.directory = fixture.ModelBridgeTests().make_workspace(self.root)

    def run_bridge(self, *frames, emit=None):
        outputs = []
        stream = io.BytesIO(b''.join(frame if isinstance(frame, bytes) else bridge.line(frame)
                                     for frame in frames))
        with (patch.object(bridge, 'require_runtime'), patch.object(runtime, 'checked_packet'),
              patch.object(runtime, 'run_submission', side_effect=fixture.ModelBridgeTests.fake_verifier) as native):
            result = bridge.collect(self.directory, self.output, stream, emit or outputs.append)
        return result, [json.loads(x) for x in outputs], native.call_count

    def end(self):
        return json.loads((self.directory / 'external-end.json').read_bytes())

    def test_checked_inputs_first_final_and_exact_archived_traffic(self):
        check = {'action': 'check', 'source': 'check only; unit fixture'}
        final = {'action': 'submit', 'source': 'first final; unit fixture'}
        result, outputs, calls = self.run_bridge(check, final, {'action': 'submit', 'source': 'late'})
        self.assertEqual((result['final_outcome'], result['denominator'], calls), ('accepted', 1, 2))
        self.assertEqual([v['kind'] for v in outputs],
                         ['fixed-target-lean-prompt', 'lean-workspace-feedback', 'lean-workspace-feedback'])
        self.assertNotIn('PRIVATE GOLD', str(outputs))
        self.assertNotIn(str(self.root), str(outputs))
        self.assertFalse(result['model_measurement'])
        evidence = json.loads((self.directory / 'external-evidence.json').read_bytes())
        for name, digest in evidence['facts']['archived_files_sha256'].items():
            self.assertEqual(bridge.bench.sha((self.output / name).read_bytes()), digest)
        self.assertEqual((self.output / '0002-request.bin').read_bytes(), bridge.line(final))
        self.assertFalse((self.output / '0003-request.bin').exists())
        with self.assertRaisesRegex(ValueError, 'pristine'):
            self.run_bridge(final)

    def test_bare_eof_is_infrastructure_not_a_model_stop(self):
        result, _, calls = self.run_bridge({'action': 'check', 'source': 'fixture'})
        self.assertEqual(calls, 1)
        self.assertEqual((result['final_outcome'], self.end()['reason']),
                         ('infrastructure-error', 'client-interrupted'))

    def test_explicit_model_stop_remains_an_observed_no_final(self):
        result, _, calls = self.run_bridge({'action': 'stop', 'reason': 'model-output-budget'})
        self.assertEqual(calls, 0)
        self.assertEqual((result['final_outcome'], self.end()['reason']),
                         ('no-final-submission', 'model-output-budget'))

    def test_unterminated_transport_frame_does_not_dispatch_lean(self):
        result, _, calls = self.run_bridge(b'{"action":"submit","source":"cut off"}')
        self.assertEqual(calls, 0)
        self.assertEqual((result['stop'], result['final_outcome']),
                         ('unterminated-transport-frame', 'infrastructure-error'))

    def test_check_budget_stops_before_extra_check_or_later_final(self):
        check = {'action': 'check', 'source': 'unit fixture'}
        result, _, calls = self.run_bridge(check, check, {'action': 'submit', 'source': 'not read'})
        self.assertEqual((result['stop'], result['final_outcome'], calls),
                         ('check-budget-exhausted', 'no-final-submission', 1))
        self.assertFalse((self.output / '0003-request.bin').exists())

    def test_invalid_first_submit_is_reserved_and_not_executed(self):
        result, _, calls = self.run_bridge({'action': 'submit'}, {'action': 'submit', 'source': 'late'})
        self.assertEqual(calls, 0)
        self.assertEqual((result['final_outcome'], self.end()['reason']), ('invalid-submission', 'final-submitted'))
        self.assertEqual([x['action'] for x in workspace.history(self.directory)[1]], ['submit'])

    def test_duplicate_key_nonfinite_foreign_encoding_and_extra_command_fail(self):
        for raw in (b'{"action":"submit","action":"check","source":"x"}\n',
                    b'{"action":"submit","source":NaN}\n',
                    '{"action":"submit","source":"x"}\n'.encode('utf-16'),
                    b'{"action":"submit","source":"x","file":"unsafe"}\n'):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                bridge.request(raw)
        result, _, calls = self.run_bridge(b'{"action":"shell","command":"never execute"}\n')
        self.assertEqual(calls, 0)
        self.assertEqual((result['final_outcome'], self.end()['reason']),
                         ('no-final-submission', 'model-protocol-error'))

    def test_wire_budget_never_dispatches_unbounded_payload(self):
        result, _, calls = self.run_bridge(b'x' * (bridge.MAX_REQUEST + 2048))
        self.assertEqual(calls, 0)
        self.assertEqual((self.output / '0001-request.bin').stat().st_size, bridge.MAX_REQUEST + 1)
        self.assertEqual((result['final_outcome'], self.end()['reason']),
                         ('no-final-submission', 'model-output-budget'))

    def test_send_failure_after_native_final_preserves_exact_outcome(self):
        def disconnect(raw):
            if json.loads(raw)['kind'] == 'lean-workspace-feedback':
                raise BrokenPipeError
        result, _, calls = self.run_bridge({'action': 'submit', 'source': 'fixture'}, emit=disconnect)
        self.assertEqual(calls, 1)
        self.assertEqual((result['final_outcome'], self.end()['reason']), ('accepted', 'client-interrupted'))

    def test_platform_gate_precedes_opening_or_exposing_workspace(self):
        with patch.object(bridge.sys, 'platform', 'win32'), patch.object(workspace, 'history') as inspect:
            with self.assertRaisesRegex(RuntimeError, 'no host Lean fallback'):
                bridge.collect(self.directory, self.output, io.BytesIO(), lambda _: self.fail('emitted prompt'))
        inspect.assert_not_called()
        self.assertFalse(self.output.exists())


if __name__ == '__main__':
    unittest.main()
