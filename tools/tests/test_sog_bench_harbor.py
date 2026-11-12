"""Native task packaging tests; fixture rewards are not model measurements."""
import copy
import errno
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import tomllib
import unittest
import zipfile
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / 'tools'), str(ROOT / 'website/scripts')]
import sog_bench_harbor as adapter
sys.path.insert(0, str(adapter.TEMPLATES))
import collect_answer as collector
import bench_bounded_io as bounded

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
            self.assertNotIn('binding_sha256', prompt)
            for name, contents in files.items():
                if name.startswith('environment/') or name in {'instruction.md', 'task.toml'}:
                    self.assertNotIn(item['binding_sha256'].encode(), contents, name)
            self.assertEqual(files['tests/sog_bench_curriculum.py'], (ROOT / 'tools/sog_bench_curriculum.py').read_bytes().replace(b'\r\n', b'\n'))
            self.assertEqual(json.loads(files['tests/question.json']), item)
            self.assertEqual(set(n for n in files if n.startswith('environment/')),
                             {'environment/Dockerfile', 'environment/docker-compose.yaml', 'environment/prompt.json',
                              'environment/isolation_check.py', 'environment/bench_bounded_io.py', 'environment/collect_answer.py'})
            self.assertEqual(files['environment/bench_bounded_io.py'], files['tests/bench_bounded_io.py'])
            self.assertEqual(files['environment/collect_answer.py'], files['tests/collect_answer.py'])

    def test_config_declares_actual_limits_and_separate_verification(self):
        for item in self.items:
            files = adapter.task_files(item)
            config = tomllib.loads(files['task.toml'].decode())
            self.assertEqual(config['schema_version'], '1.4')
            self.assertEqual(config['artifacts'], ['/handoff/answer.bin', '/handoff/collection.json'])
            self.assertEqual(config['task']['version'], '3')
            self.assertEqual(config['metadata']['prompt_sha256'],
                             adapter.bench.curriculum.graph_prompt(item)['prompt_sha256'])
            self.assertEqual(config['verifier']['collect'], [{'command': 'python -I /app/collect_answer.py',
                'service': 'main', 'user': 'root', 'timeout_sec': 5}])
            self.assertEqual(config['environment']['network_mode'], 'public')
            self.assertIn('network_mode:none', config['metadata']['network_contract'])
            self.assertIn(b'network_mode: none', files['environment/docker-compose.yaml'])
            self.assertIn(b'pids_limit: 128', files['environment/docker-compose.yaml'])
            self.assertEqual(config['environment']['cpus'], 1)
            self.assertEqual(config['environment']['memory_mb'], 256)
            self.assertEqual(config['agent']['user'], 'bench')
            self.assertEqual(config['verifier']['environment_mode'], 'separate')
            self.assertEqual(config['verifier']['network_mode'], 'public')
            self.assertIn(adapter.BASE_IMAGE.encode(), files['environment/Dockerfile'])
            self.assertIn(b'touch /output/agent-marker', files['solution/solve.sh'])
            self.assertIn(b'test ! -e /output/agent-marker', files['tests/test.sh'])

    def test_solver_assets_are_identical_for_alternate_gold(self):
        item = self.items[0]
        prompt = adapter.bench.curriculum.graph_prompt(item)
        visible = {k: v for k, v in prompt.items() if k != 'prompt_sha256'}
        other = {**item['answer'], 'entails_mathematical_necessity': True}
        changed = {**item, 'answer': other, 'binding_sha256': adapter.bench.curriculum.digest(
            {'prompt': visible, 'answer': other})}
        first, second = adapter.task_files(item), adapter.task_files(changed)
        self.assertNotEqual(first['tests/question.json'], second['tests/question.json'])
        self.assertNotEqual(first['solution/answer.json'], second['solution/answer.json'])
        for name, payload in first.items():
            if name.startswith('environment/') or name in {'task.toml', 'instruction.md'}:
                self.assertEqual(payload, second[name], name)

    def test_all_original_reference_answers_agree_with_the_actual_scorer(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / 'answer.json'
            for item in self.items:
                answer = adapter.task_files(item)['solution/answer.json']
                path.write_bytes(answer)
                report = verifier.assess(item, path)
                self.assertEqual(report['reward'], 1)
                row = json.loads(answer)
                self.assertNotIn('binding_sha256', row)
                self.assertEqual(report['result'], adapter.bench.curriculum.grade_graph([item],
                    adapter.bench.curriculum.bind_graph_submissions([item], [row])))
                self.assertEqual(report['response_sha256'], hashlib.sha256(answer).hexdigest())

    def test_invalid_data_zeroes_without_executing_any_submission(self):
        item = self.items[0]
        answer = json.loads(adapter.task_files(item)['solution/answer.json'])
        invalid = [b'', b'\xff', b'{}', b'[]', b'{"x":1,"x":2}', b'{"x":NaN}', b'[' * 2000,
                   b' ' * (verifier.MAX_BYTES + 1)]
        for key, value in [('id', []), ('id', 'sogb-g999'), ('prompt_sha256', 'stale'),
                           ('attempt', True), ('attempt', 2), ('answer', {'nodes': [], 'entails_mathematical_necessity': True})]:
            row = copy.deepcopy(answer)
            row[key] = value
            invalid.append(json.dumps(row).encode())
        legacy = {k: v for k, v in answer.items() if k != 'prompt_sha256'}
        invalid.append(json.dumps({**legacy, 'binding_sha256': item['binding_sha256']}).encode())

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
            self.assertEqual(a['producer_lean_toolchain'], 'leanprover/lean4:v4.33.0')
            self.assertEqual(a['producer_mathlib_manifest_sha256_lf'], adapter.bench.text_hash(ROOT / 'lake-manifest.json'))
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
            handoff = trial / 'artifacts/handoff'
            handoff.mkdir(parents=True)
            source = base / 'answer.json'
            source.write_bytes(b'')
            raw, receipt = collector.capture(source)
            (handoff / 'answer.bin').write_bytes(raw)
            (handoff / 'collection.json').write_bytes(receipt)
            self.assertTrue(adapter.check_job(base, ['sogb-g001'], 0)['complete'])
            for ids, value in [(['sogb-g001', 'sogb-g002'], 0), (['sogb-g001'], 1), (['sogb-g001', 'sogb-g001'], 0)]:
                with self.assertRaises(ValueError):
                    adapter.check_job(base, ids, value)
            row['exception_info'] = {'exception_type': 'TimeoutError'}
            path.write_text(json.dumps(row))
            with self.assertRaises(ValueError):
                adapter.check_job(base, ['sogb-g001'], 0)

    def test_collector_preserves_exact_bounded_bytes_and_the_canonical_score(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            source, raw_path, receipt_path = base / 'source', base / 'raw', base / 'receipt'
            for item in self.items:
                source.write_bytes(adapter.task_files(item)['solution/answer.json'])
                raw, receipt = collector.capture(source)
                self.assertEqual(raw, source.read_bytes())
                raw_path.write_bytes(raw)
                receipt_path.write_bytes(receipt)
                self.assertEqual(verifier.assess_collected(item, raw_path, receipt_path)['reward'], 1)
            source.write_bytes(b'x' * bounded.MAX_BYTES)
            self.assertEqual(len(collector.capture(source)[0]), bounded.MAX_BYTES)
            source.write_bytes(b'x' * (bounded.MAX_BYTES + 1))
            raw, encoded = collector.capture(source)
            self.assertEqual(raw, b'')
            self.assertEqual(json.loads(encoded)['reason'], 'too-large')
            self.assertLessEqual(len(encoded), bounded.MAX_RECEIPT_BYTES)

    def test_missing_or_corrupt_receipts_are_infrastructure_failures_not_zero_scores(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            raw_path, receipt_path = base / 'raw', base / 'receipt'
            with self.assertRaises(RuntimeError):
                verifier.assess_collected(self.items[0], raw_path, receipt_path)

            source = base / 'absent'
            raw, receipt = collector.capture(source)
            raw_path.write_bytes(raw)
            receipt_path.write_bytes(receipt)
            result = verifier.assess_collected(self.items[0], raw_path, receipt_path)
            self.assertEqual(result['reward'], 0)
            self.assertEqual(result['collection']['reason'], 'missing')
            for invalid in [b'{}', b'not-json', b'x' * 1025, receipt.replace(b'"missing"', b'"invented"')]:
                receipt_path.write_bytes(invalid)
                with self.assertRaises(RuntimeError):
                    verifier.assess_collected(self.items[0], raw_path, receipt_path)
            receipt_path.write_bytes(receipt)
            raw_path.write_bytes(b'tampered')
            with self.assertRaises(RuntimeError):
                verifier.assess_collected(self.items[0], raw_path, receipt_path)

    def test_collector_rejects_detected_mutation_instead_of_archiving_a_partial_snapshot(self):
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / 'answer'
            source.write_bytes(b'abc')
            before = source.stat()
            after = SimpleNamespace(**{key: getattr(before, key) for key in
                ('st_dev', 'st_ino', 'st_size', 'st_mode', 'st_ctime_ns')}, st_mtime_ns=before.st_mtime_ns + 1)
            with patch.object(bounded.os, 'fstat', side_effect=[before, after]):
                raw, receipt = collector.capture(source)
            self.assertEqual(raw, b'')
            self.assertEqual(json.loads(receipt)['reason'], 'changed-during-read')

    @unittest.skipUnless(os.name == 'posix', 'Linux no-follow/FIFO semantics')
    def test_collector_rejects_special_files_before_any_host_transfer(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            target = base / 'target'
            target.write_bytes(b'secret must not be collected through symlink')
            link, fifo = base / 'link', base / 'fifo'
            link.symlink_to(target)
            os.mkfifo(fifo)
            for source, reason in [(link, 'symlink'), (fifo, 'not-regular'), (base, 'not-regular')]:
                raw, receipt = collector.capture(source)
                self.assertEqual(raw, b'')
                self.assertEqual(json.loads(receipt)['reason'], reason)

    def test_transport_fixtures_keep_question_binding_and_do_not_enter_default_archive(self):
        item = self.items[0]
        original = adapter.task_files(item)
        for case in adapter.FIXTURES:
            files = adapter.task_files(item, case)
            self.assertEqual(files['environment/prompt.json'], original['environment/prompt.json'])
            self.assertEqual(files['tests/question.json'], original['tests/question.json'])
            self.assertEqual(tomllib.loads(files['task.toml'].decode())['metadata']['software_fixture'], case)

    def test_failed_hook_acceptance_never_manufactures_a_zero_or_positive_score(self):
        with tempfile.TemporaryDirectory() as temporary:
            trial = Path(temporary) / 'trial'
            trial.mkdir()
            path = trial / 'result.json'
            row = {'task_name': 'samplinglib/sogb-g001', 'exception_info': {'exception_type': 'RewardFileNotFoundError'},
                   'verifier_result': None}
            path.write_text(json.dumps(row))
            self.assertTrue(adapter.check_failed_collection(Path(temporary), ['sogb-g001'])['unscored_infrastructure_failure'])
            row['verifier_result'] = {'rewards': {'reward': 0}}
            path.write_text(json.dumps(row))
            with self.assertRaises(ValueError):
                adapter.check_failed_collection(Path(temporary), ['sogb-g001'])

    def test_unknown_input_io_failures_cannot_become_zero_scored_model_answers(self):
        with patch.object(collector, 'read_bounded', side_effect=OSError(errno.EIO, 'controlled IO fault')):
            with self.assertRaises(OSError):
                collector.capture(Path('unused'))
        with patch.object(collector, 'read_bounded', side_effect=OSError(errno.ELOOP, 'controlled no-follow race')):
            raw, receipt = collector.capture(Path('unused'))
            self.assertEqual(raw, b'')
            self.assertEqual(json.loads(receipt)['reason'], 'symlink')
        with patch.object(verifier, 'read_bounded', side_effect=OSError(errno.EIO, 'controlled IO fault')):
            with self.assertRaises(RuntimeError):
                verifier.assess(self.items[0], Path('unused'))

    def test_the_score_uses_the_exact_receipt_checked_snapshot_without_rereading(self):
        item = self.items[0]
        raw = adapter.task_files(item)['solution/answer.json']
        receipt = adapter.bench.encoded({'schema_version': 1, 'policy': collector.POLICY,
            'status': 'captured', 'reason': None, 'raw_bytes': len(raw),
            'raw_sha256': hashlib.sha256(raw).hexdigest()})
        with patch.object(verifier, 'read_bounded', side_effect=[receipt, raw]) as reader:
            report = verifier.assess_collected(item, Path('raw'), Path('receipt'))
        self.assertEqual(reader.call_count, 2)
        self.assertEqual(report['reward'], 1)
        self.assertEqual(report['response_sha256'], json.loads(receipt)['raw_sha256'])

    def test_static_offline_probe_rejects_sidecars_and_unlimited_resources(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / 'class/net/lo').mkdir(parents=True)
            (root / 'fs/cgroup').mkdir(parents=True)
            (root / 'fs/cgroup/memory.max').write_text('256000000')
            (root / 'fs/cgroup/cpu.max').write_text('100000 100000')
            (root / 'fs/cgroup/pids.max').write_text('128')
            with patch.object(probe, 'Path', side_effect=lambda p: root / p.removeprefix('/sys/')):
                self.assertEqual(probe.probe()['network_interfaces'], ['lo'])
                (root / 'class/net/eth0').mkdir()
                with self.assertRaises(RuntimeError):
                    probe.probe()


if __name__ == '__main__':
    unittest.main()
