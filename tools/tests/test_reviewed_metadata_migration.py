"""The one-time migration cannot authorize arbitrary Lean or import changes."""
import hashlib
import subprocess
import tempfile
from types import SimpleNamespace
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import astis_publication as p

class ReviewedMetadataMigrationTests(unittest.TestCase):
    def setUp(self):
        self.path = 'AutoSamplingTheory/Probability.lean'
        self.before = 'import Mathlib\n/-- old module description -/\ndef label : String := "fixed"\n'
        self.after = self.before.replace('old module description', 'general module description')
        self.pair = tuple(hashlib.sha256(t.encode()).hexdigest() for t in (self.before, self.after))

    def matches(self, before, after, path=None):
        with patch.object(p, 'REVIEWED_METADATA_MIGRATIONS', {self.path: self.pair}), patch.object(p, 'git', return_value=before):
            return p.reviewed_metadata_migration(path or self.path, 'base', after)

    def test_exact_pair_and_checkout_newlines_only(self):
        self.assertTrue(self.matches(self.before, self.after))
        self.assertTrue(self.matches(self.before.replace('\n', '\r\n'), self.after))

    def test_any_additional_source_change_restores_conservative_gate(self):
        for extra in ('import Other\n', 'theorem claim : False := by sorry\n',
                      'instance : Inhabited Nat := inferInstance\n',
                      'axiom hidden : False\n', 'theorem α : True := True.intro\n',
                      '/-- an extra comment is also outside the sealed pair -/\n'):
            with self.subTest(extra=extra):
                self.assertFalse(self.matches(self.before, self.after + extra))
        self.assertFalse(self.matches(self.before, self.after.replace('"fixed"', '"changed"')))
        self.assertFalse(self.matches(self.before + ' ', self.after))

    def test_other_path_and_missing_base_are_not_exempt(self):
        self.assertFalse(self.matches(self.before, self.after, 'AutoSamplingTheory/Other.lean'))
        with patch.object(p, 'git', side_effect=subprocess.CalledProcessError(1, ['git'])):
            self.assertFalse(p.reviewed_metadata_migration(self.path, 'missing', self.after))

    def changed_targets(self, text, extra=(), seal_current=False):
        scratch = Path(__file__).resolve().parents[2] / '.astis' / 'test-fixtures'
        scratch.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=scratch) as directory:
            root = Path(directory)
            path = root / self.path
            path.parent.mkdir(parents=True)
            path.write_text(text, encoding='utf-8')
            known = [SimpleNamespace(source_file=self.path, source_line=3, kind='def',
                        short_name='label', full_name='label'), *extra]
            def fake_git(*args):
                if args[0] == 'diff': return self.path + '\0'
                if args[0] == 'show': return self.before
                return ''
            pair = (self.pair[0], hashlib.sha256(text.encode()).hexdigest()) if seal_current else self.pair
            with patch.object(p, 'ROOT', root), patch.object(p, 'git', side_effect=fake_git), \
                 patch.object(p, 'inputs', return_value={'declarations': {d.full_name: d for d in known}}), \
                 patch.object(p, 'REVIEWED_METADATA_MIGRATIONS', {self.path: pair}):
                return p.changed_declarations('base')

    def test_changed_module_gate_accepts_only_exact_migration(self):
        self.assertEqual(self.changed_targets(self.after), set())
        for kind, command, name in [('theorem', 'theorem claim : True := True.intro', 'claim'),
                                    ('instance', 'instance instUnit : Inhabited Unit := inferInstance', 'instUnit')]:
            declaration = SimpleNamespace(source_file=self.path, source_line=4, kind=kind,
                              short_name=name, full_name=name)
            with self.subTest(kind=kind):
                self.assertEqual(self.changed_targets(self.after + command + '\n', [declaration]),
                                 {'label', name})

    def test_command_scan_precedes_even_a_matching_pair(self):
        for command in ('theorem α : True := True.intro', 'instance : Inhabited Unit := inferInstance'):
            with self.subTest(command=command):
                with self.assertRaisesRegex(ValueError, 'unindexed declaration'):
                    self.changed_targets(self.after + command + '\n', seal_current=True)

    def test_approved_scope_is_exactly_three_existing_files(self):
        self.assertEqual(set(p.REVIEWED_METADATA_MIGRATIONS), {
            'AutoSamplingTheory/Automation.lean', 'AutoSamplingTheory/Literature.lean',
            'AutoSamplingTheory/Probability.lean'})
        for pair in p.REVIEWED_METADATA_MIGRATIONS.values():
            self.assertEqual(len(pair), 2)
            self.assertTrue(all(len(value) == 64 for value in pair))

if __name__ == '__main__':
    unittest.main()
