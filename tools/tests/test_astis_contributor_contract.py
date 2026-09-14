"""Regression tests for real comparison scope and metadata-only contributions."""
from __future__ import annotations

import io
import json
import subprocess
import tempfile
import unittest
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path
from unittest.mock import patch

from tools import astis_contributor_contract as c


class MetadataScopeTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.git('init', '-q')
        self.git('config', 'user.email', 'fixture@example.invalid')
        self.git('config', 'user.name', 'Test fixture')
        self.pub = 'website/content/publications/example.json'
        self.lesson = 'website/content/declaration_lessons/example.json'
        self.cell = 'research-wiki/frontier-cells/example.json'
        self.items = [{'id': 'source', 'statement': 'Original', 'bindings': [
            {'declaration': 'Example.one', 'cell': 'cell'},
            {'declaration': 'Example.two', 'cell': 'other'}]}]
        self.write(self.pub, {'items': self.items})
        self.write(self.lesson, {'units': [{'declaration': 'Example.one', 'statement': 'Original'}]})
        self.write(self.cell, {'cell_id': 'cell', 'reader_contract': {'source_ordered': True}})
        self.git('add', '.')
        self.git('commit', '-qm', 'baseline')
        self.base = self.git('rev-parse', 'HEAD').strip()
        self.addCleanup(patch.stopall)
        patch.object(c, 'ROOT', self.root).start()
        patch.object(c.publication, 'git', side_effect=self.git).start()
        patch.object(c.publication, 'changed_declarations', return_value=set()).start()

    def git(self, *args):
        return subprocess.check_output(['git', *args], cwd=self.root, text=True)

    def write(self, path, value):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(value))

    def test_no_changes_is_explicitly_empty(self):
        self.assertEqual(c.scope(self.base, self.items), (set(), set()))

    def test_removed_cell_contract_is_selected_and_rejected(self):
        self.write(self.cell, {'cell_id': 'cell'})
        names, cells = c.scope(self.base, self.items)
        self.assertEqual(names, {'Example.one'})
        errors = c.validate_targets(names, self.items, {'cells': {'cell': {'cell_id': 'cell'}}, 'lessons': {}}, cells)
        self.assertTrue(any('reader_contract required' in e for e in errors))

    def test_source_edit_selects_all_its_bindings(self):
        self.items[0]['statement'] = 'Changed source'
        self.write(self.pub, {'items': self.items})
        self.assertEqual(c.scope(self.base, self.items)[0], {'Example.one', 'Example.two'})

    def test_binding_edit_does_not_select_sibling(self):
        self.items[0]['bindings'][0]['boundary'] = 'Changed'
        self.write(self.pub, {'items': self.items})
        self.assertEqual(c.scope(self.base, self.items)[0], {'Example.one'})

    def test_removed_binding_cannot_disappear_from_review(self):
        self.items[0]['bindings'].pop(0)
        self.write(self.pub, {'items': self.items})
        names, cells = c.scope(self.base, self.items)
        self.assertEqual(names, {'Example.one'})
        self.assertTrue(c.validate_targets(names, self.items, {'cells': {}, 'lessons': {}}, cells))

    def test_deleted_lesson_keeps_original_target(self):
        (self.root / self.lesson).unlink()
        self.assertEqual(c.scope(self.base, self.items)[0], {'Example.one'})

    def test_untracked_lesson_is_checked(self):
        self.write('website/content/declaration_lessons/new.json', {'units': [{'declaration': 'Example.new'}]})
        self.assertEqual(c.scope(self.base, self.items)[0], {'Example.new'})

    def test_lesson_and_publication_filenames_cannot_hide_changes(self):
        self.write('website/content/declaration_lessons/_new.json', {'units': [{'declaration': 'Example.new'}]})
        self.write('website/content/publications/schema.json', {'items': [{
            'id': 'new-source', 'bindings': [{'declaration': 'Example.schema'}]}]})
        self.assertEqual(c.scope(self.base, self.items)[0], {'Example.new', 'Example.schema'})

    def test_changed_unbound_planned_cell_needs_contract(self):
        self.write('research-wiki/frontier-cells/new.json', {'cell_id': 'planned'})
        names, cells = c.scope(self.base, self.items)
        self.assertFalse(names)
        errors = c.validate_targets(names, self.items, {'cells': {'planned': {'cell_id': 'planned'}}, 'lessons': {}}, cells)
        self.assertTrue(any('reuse_plan required' in e for e in errors))

    def test_malformed_metadata_fails_closed(self):
        (self.root / self.lesson).write_text('{broken')
        with self.assertRaises(ValueError):
            c.scope(self.base, self.items)

    def test_no_base_fails_instead_of_empty_pass(self):
        with redirect_stderr(io.StringIO()):
            self.assertEqual(c.main(['check']), 1)

    def test_ci_zero_base_never_falls_back_to_last_commit(self):
        self.git('update-ref', 'refs/remotes/origin/main', self.base)
        self.write('unrelated.txt', {})
        self.git('add', '.')
        self.git('commit', '-qm', 'first topic commit')
        self.write('unrelated.txt', {'second': True})
        self.git('add', '.')
        self.git('commit', '-qm', 'second topic commit')
        with patch.dict('os.environ', {'GITHUB_REF': 'refs/heads/topic'}):
            self.assertEqual(c.resolve_base('0' * 40, ci=True), self.base)

    def test_initial_main_push_requires_explicit_base(self):
        with patch.dict('os.environ', {'GITHUB_REF': 'refs/heads/main'}), self.assertRaises(ValueError):
            c.resolve_base('0' * 40, ci=True)

    def test_explicit_base_wins_over_environment(self):
        with patch.dict('os.environ', {'PUBLICATION_BASE': 'invalid'}):
            self.assertEqual(c.resolve_base(self.base, ci=True), self.base)

    def test_ci_requires_base_instead_of_assuming_head_parent(self):
        with patch.dict('os.environ', {}, clear=True), self.assertRaises(ValueError):
            c.resolve_base(None, ci=True)

    def test_no_targets_prints_na_not_pass(self):
        stream = io.StringIO()
        with patch.object(c.publication, 'load', return_value=self.items), \
             patch.object(c.publication, 'inputs', return_value={'cells': {}, 'lessons': {}}), \
             redirect_stdout(stream):
            self.assertEqual(c.main(['check', '--base', self.base]), 0)
        self.assertIn('N/A', stream.getvalue())
        self.assertNotIn('contract PASS', stream.getvalue())

    def test_production_targets_still_require_coverage(self):
        with patch.object(c.publication, 'changed_declarations', return_value={'Example.new'}):
            names, cells = c.scope(self.base, self.items)
        self.assertEqual(names, {'Example.new'})
        self.assertTrue(c.validate_targets(names, self.items, {'cells': {}, 'lessons': {}}, cells))

    def test_removed_publication_file_keeps_all_old_bindings(self):
        (self.root / self.pub).unlink()
        names, _ = c.scope(self.base, [])
        self.assertEqual(names, {'Example.one', 'Example.two'})

    def test_unchanged_unbound_inventory_is_not_certified(self):
        self.assertEqual(c.validate_targets(set(), self.items, {'cells': {}, 'lessons': {}}), [])


if __name__ == '__main__':
    unittest.main()
