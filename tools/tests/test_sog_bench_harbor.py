"""Native task packaging tests; fixture rewards are not model measurements."""
import copy
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import tomllib
import unittest
import zipfile
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / 'tools'), str(ROOT / 'website/scripts')]
import sog_bench_harbor as adapter

spec = importlib.util.spec_from_file_location('sog_harbor_verifier', adapter.TEMPLATES / 'verify.py')
verifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier)
probe_spec = importlib.util.spec_from_file_location('sog_harbor_probe', adapter.TEMPLATES / 'isolation_check.py')
probe = importlib.util.module_from_spec(probe_spec)
probe_spec.loader.exec_module(probe)


class HarborGraphTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.items = adapter.bench.curriculum.graph_items()

    def test_prompt_context_and_canonical_scorer_are_not_rewritten(self):
        for item in self.items:
            files = adapter.task_files(item)
            prompt = json.loads(files['environment/prompt.json'])
            self.assertEqual(prompt, adapter.bench.curriculum.graph_prompts([item])[0])
            self.assertNotIn('answer', prompt)
            self.assertEqual(files['tests/sog_bench_curriculum.py'], (ROOT / 'tools/sog_bench_curriculum.py').read_bytes().replace(b'\r\n', b'\n'))
            self.assertEqual(json.loads(files['tests/question.json']), item)
            self.assertEqual(set(n for n in files if n.startswith('environment/')),
                             {'environment/Dockerfile', 'environment/prompt.json', 'environment/isolation_check.py'})

    def test_config_declares_actual_limits_and_separate_verification(self):
        for item in self.items:
            files = adapter.task_files(item)
            config = tomllib.loads(files['task.toml'].decode())
            self.assertEqual(config['schema_version'], '1.4')
            self.assertEqual(config['artifacts'], ['/output/answer.json'])
            self.assertEqual(config['environment']['network_mode'], 'no-network')
            self.assertEqual(config['environment']['cpus'], 1)
            self.assertEqual(config['environment']['memory_mb'], 256)
            self.assertEqual(config['agent']['user'], 'bench')
            self.assertEqual(config['verifier']['environment_mode'], 'separate')
            self.assertEqual(config['verifier']['network_mode'], 'no-network')
            self.assertIn(adapter.BASE_IMAGE.encode(), files['environment/Dockerfile'])
            self.assertIn(b'touch /output/agent-marker', files['solution/solve.sh'])
            self.assertIn(b'test ! -e /output/agent-marker', files['tests/test.sh'])

    def test_all_original_reference_answers_agree_with_the_actual_scorer(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / 'answer.json'
            for item in self.items:
                answer = adapter.task_files(item)['solution/answer.json']
                path.write_bytes(answer)
                report = verifier.assess(item, path)
                self.assertEqual(report['reward'], 1)
                self.assertEqual(report['result'], adapter.bench.curriculum.grade_graph([item], [json.loads(answer)]))
                self.assertEqual(report['response_sha256'], hashlib.sha256(answer).hexdigest())

    def test_invalid_data_zeroes_without_executing_any_submission(self):
        item = self.items[0]
        answer = json.loads(adapter.task_files(item)['solution/answer.json'])
        invalid = [b'', b'\xff', b'{}', b'[]', b'{"x":1,"x":2}', b'{"x":NaN}', b'[' * 2000,
                   b' ' * (verifier.MAX_BYTES + 1)]
        for key, value in [('id', []), ('id', 'sogb-g999'), ('binding_sha256', 'stale'),
                           ('attempt', True), ('attempt', 2), ('answer', {'nodes': [], 'entails_mathematical_necessity': True})]:
            row = copy.deepcopy(answer)
            row[key] = value
            invalid.append(json.dumps(row).encode())
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / 'answer.json'
            self.assertEqual(verifier.assess(item, path)['reward'], 0)
            for raw in invalid:
                path.write_bytes(raw)
                self.assertEqual(verifier.assess(item, path)['reward'], 0, raw[:100])

    @unittest.skipUnless(os.name == 'posix', 'FIFO/no-follow check uses Linux file semantics')
    def test_special_files_and_symlinks_are_rejected_without_blocking(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            target = base / 'target'
            target.write_bytes(adapter.task_files(self.items[0])['solution/answer.json'])
            link = base / 'link'
            link.symlink_to(target)
            self.assertEqual(verifier.assess(self.items[0], link)['reward'], 0)
            fifo = base / 'fifo'
            os.mkfifo(fifo)
            self.assertEqual(verifier.assess(self.items[0], fifo)['reward'], 0)

    def test_exports_are_fresh_deterministic_and_hash_all_task_files(self):
        with tempfile.TemporaryDirectory() as temporary:
            first, second = Path(temporary) / 'one', Path(temporary) / 'two'
            a = adapter.export(first, [self.items[0]['id']])
            b = adapter.export(second, [self.items[0]['id']])
            self.assertEqual(a, b)
            for name, digest in a['files'].items():
                self.assertEqual(hashlib.sha256((first / name).read_bytes()).hexdigest(), digest)
            with self.assertRaises(ValueError):
                adapter.export(first, [self.items[0]['id']])

    def test_stale_or_unreviewed_tasks_cannot_be_packaged(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / 'fresh'
            with patch.object(adapter.review, 'summary', return_value={'items': {i['id']: {'editorial': 'stale'} for i in self.items}}):
                with self.assertRaises(ValueError):
                    adapter.export(output, [self.items[0]['id']])
            self.assertFalse(output.exists())

    def test_operator_zip_is_deterministic_and_uses_the_same_cli_files(self):
        items = self.items[:2]
        payload = adapter.archive(items)
        self.assertEqual(payload, adapter.archive(items))
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / 'native'
            manifest = adapter.export(output, [i['id'] for i in items])
            with zipfile.ZipFile(io.BytesIO(payload)) as bundle:
                self.assertEqual(set(bundle.namelist()), {*manifest['files'], 'adapter-manifest.json'})
                for name in bundle.namelist():
                    self.assertEqual(bundle.read(name), (output / name).read_bytes())
        stale = copy.deepcopy(items)
        stale[0]['question'] += ' changed'
        with self.assertRaises(ValueError):
            adapter.archive(stale)

    def test_native_receipt_check_preserves_missing_and_failed_trials(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            trial = base / 'trial'
            trial.mkdir()
            row = {'task_name': 'samplinglib/sogb-g001', 'exception_info': None, 'verifier_result': {'rewards': {'reward': 0}}}
            path = trial / 'result.json'
            path.write_text(json.dumps(row))
            self.assertTrue(adapter.check_job(base, ['sogb-g001'], 0)['complete'])
            for ids, value in [(['sogb-g001', 'sogb-g002'], 0), (['sogb-g001'], 1), (['sogb-g001', 'sogb-g001'], 0)]:
                with self.assertRaises(ValueError):
                    adapter.check_job(base, ids, value)
            row['exception_info'] = {'exception_type': 'TimeoutError'}
            path.write_text(json.dumps(row))
            with self.assertRaises(ValueError):
                adapter.check_job(base, ['sogb-g001'], 0)

    def test_egress_probe_does_not_confuse_a_firewalled_interface_with_external_access(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / 'class/net/eth0').mkdir(parents=True)
            (root / 'class/net/lo').mkdir()
            (root / 'fs/cgroup').mkdir(parents=True)
            (root / 'fs/cgroup/memory.max').write_text('256000000')
            (root / 'fs/cgroup/cpu.max').write_text('100000 100000')
            with patch.object(probe, 'Path', side_effect=lambda p: root / p.removeprefix('/sys/')):
                with patch.object(probe.socket, 'create_connection', side_effect=TimeoutError):
                    report = probe.probe()
                    self.assertEqual(report['network_interfaces'], ['eth0', 'lo'])
                    self.assertEqual(len(report['external_tcp_denials']), 2)
                with patch.object(probe.socket, 'create_connection'):
                    with self.assertRaises(RuntimeError):
                        probe.probe()


if __name__ == '__main__':
    unittest.main()
