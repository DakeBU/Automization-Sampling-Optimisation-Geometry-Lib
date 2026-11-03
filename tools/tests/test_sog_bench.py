"""Paired identities, exact reference extraction, no-answer exports and reader contracts."""
from copy import deepcopy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / 'tools'), str(ROOT / 'website/scripts')]
import sog_bench as bench
import sog_bench_reader as reader


class BenchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cores = bench.materialize()

    def test_three_shared_cores_six_views_same_families_and_split(self):
        prompts = bench.prompts(self.cores)
        self.assertEqual(len(self.cores), 3)
        self.assertEqual(len(prompts), 6)
        for core in self.cores:
            views = [r for r in prompts if r['id'] == core['id']]
            self.assertEqual({r['track'] for r in views}, set(bench.TRACKS))
            for row in views:
                self.assertEqual(row['family'], core['family'])
                self.assertEqual(row['binding_sha256'], core['binding_sha256'])
                self.assertEqual(row['split'], 'public-dev')

    def test_prompt_export_has_no_answers_rubrics_or_reference_proofs(self):
        allowed = {'id', 'family', 'domain', 'title', 'split', 'assumptions', 'binding_sha256', 'track', 'question'}
        for row in bench.prompts(self.cores):
            self.assertEqual(set(row), allowed)
            self.assertNotIn(':= by\n  intro', row['question'])
        self.assertTrue(all('-- Replace this comment' in r['question']
                            for r in bench.prompts(self.cores) if r['track'] == 'lean'))

    def test_extracts_existing_proof_not_target_import_or_wrapper(self):
        for core in self.cores:
            reference = core['lean_reference']
            target_module = core['source_file'].removesuffix('.lean').replace('/', '.')
            self.assertNotIn('import ' + target_module + '\n', reference)
            self.assertRegex(reference, r'\bexample\s')
            self.assertNotIn('end AutoSamplingTheory', reference)
            self.assertNotIn(core['declaration'], reference)
            self.assertNotIn('sorry', reference)
            self.assertEqual(core['source_sha256_lf'], bench.text_hash(ROOT / core['source_file']))
        self.assertIn('ENNReal.tsum_comm', self.cores[0]['lean_reference'])
        self.assertIn('by_cases hq', self.cores[1]['lean_reference'])
        self.assertIn('hV.2', self.cores[2]['lean_reference'])

    def test_binding_changes_with_prose_or_context(self):
        for key in ('question', 'context', 'boundary'):
            changed = deepcopy(bench.load())
            changed['cores'][0][key] += '\nChanged contract.'
            rows = bench.materialize(changed)
            self.assertNotEqual(rows[0]['binding_sha256'], self.cores[0]['binding_sha256'])

    def test_export_determinism_license_and_portable_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / 'export'
            bench.export(output, self.cores)
            before = {p.relative_to(output).as_posix(): p.read_bytes() for p in output.rglob('*') if p.is_file()}
            bench.export(output, self.cores)
            self.assertEqual(before, {p.relative_to(output).as_posix(): p.read_bytes() for p in output.rglob('*') if p.is_file()})
            manifest = json.loads((output / 'manifest.json').read_text())
            self.assertEqual(manifest['qa_views'], 6)
            self.assertEqual(manifest['independent_semantic_review'], 'pending')
            for name, digest in manifest['files'].items():
                self.assertEqual(digest, bench.sha((output / name).read_bytes()))
            for name in bench.project_licensing.LICENSE_FILES:
                self.assertEqual((output / name).read_bytes(), (ROOT / name).read_bytes())
            one, two = Path(tmp) / 'one.zip', Path(tmp) / 'two.zip'
            bench.archive_bytes(output, one)
            bench.archive_bytes(output, two)
            self.assertEqual(one.read_bytes(), two.read_bytes())
            with zipfile.ZipFile(one) as archive:
                self.assertIn('questions.jsonl', archive.namelist())
                self.assertTrue(all(not Path(n).is_absolute() and '..' not in Path(n).parts for n in archive.namelist()))

    def test_absent_and_stale_receipt_do_not_claim_compilation(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(bench, 'RECEIPT', Path(tmp) / 'receipt.json'):
            self.assertFalse(bench.receipt_current(self.cores))

    def test_export_does_not_overwrite_or_bundle_unrelated_work(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            unrelated = output / 'README.md'
            unrelated.write_text('User work', encoding='utf-8')
            with self.assertRaises(ValueError):
                bench.export(output, self.cores)
            self.assertEqual(unrelated.read_text(), 'User work')

    def test_receipt_requires_exact_source_and_qa_bindings(self):
        receipt = {'schema_version': 1, 'passed': True, 'environment_sha256': 'environment',
                   'compiler_version': 'Lean (version 4.33.0, test fixture)',
                   'bindings': {c['id']: c['binding_sha256'] for c in self.cores},
                   'reference_sha256': {c['id']: bench.sha(c['lean_reference'].encode()) for c in self.cores},
                   'commands': [{'returncode': 0}] * 5}
        with tempfile.TemporaryDirectory() as tmp, \
             patch.object(bench, 'RECEIPT', Path(tmp) / 'receipt.json'), \
             patch.object(bench, 'environment_digest', return_value='environment'):
            bench.RECEIPT.write_bytes(bench.encoded(receipt))
            self.assertTrue(bench.receipt_current(self.cores))
            receipt['bindings']['sogb-001'] = 'old-question'
            bench.RECEIPT.write_bytes(bench.encoded(receipt))
            self.assertFalse(bench.receipt_current(self.cores))
            bench.RECEIPT.write_text('{"passed": true}', encoding='utf-8')
            self.assertFalse(bench.receipt_current(self.cores))

    def test_review_and_split_cannot_be_promoted_by_editing_badge(self):
        for key, value in (('split', 'heldout'), ('review_status', 'verified')):
            data = bench.load()
            data[key] = value
            with patch.object(bench.Path, 'read_text', return_value=json.dumps(data)):
                with self.assertRaises(ValueError):
                    bench.load()

    def test_reader_is_layered_and_does_not_cross_promote_projects(self):
        text = reader.home(self.cores)
        self.assertIn('natural-language/index.html', text)
        self.assertIn('lean/index.html', text)
        self.assertIn('independent semantic review pending', text)
        self.assertNotIn('Quantum', text)
        for core in self.cores:
            rendered = reader.core_page(core, False, {'decl:' + core['declaration']})
            self.assertIn('Reference mathematical proof', rendered)
            self.assertIn('Reference Lean and explanation', rendered)
            self.assertNotIn('<details open', rendered)
            self.assertIn('focus=decl%3A', rendered)
            self.assertIn('data-lean-copy-status', rendered)
            self.assertIn('No current trusted-reference compiler receipt', rendered)
            fallback = reader.core_page(core, False, set())
            self.assertIn('focus=module%3A', fallback)
            self.assertIn('declaration not yet indexed', fallback)


if __name__ == '__main__':
    unittest.main()
