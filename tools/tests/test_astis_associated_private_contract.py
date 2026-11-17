"""Private associations retain scope and fail closed on stale/ambiguous review."""
import copy
import hashlib
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from tools import astis_contributor_contract as c


class AssociatedPrivateContractTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.module = 'Tests/Consumer.lean'
        self.text = 'private theorem consumer : True := by trivial\n'
        p = self.root / self.module
        p.parent.mkdir()
        p.write_text(self.text)
        self.registry_path = 'research-wiki/private/registry.json'
        p = self.root / self.registry_path
        p.parent.mkdir(parents=True)
        p.write_text('{}')
        self.sha = hashlib.sha256(self.text.encode()).hexdigest()
        self.lesson = {'declaration': 'Consumer'}
        self.association = {'declaration': 'Consumer', 'owner_public_declaration': 'Public',
                            'audit_id': 'private', 'separate_public_node': False}
        self.binding = {'declaration': 'Public', 'cell': 'cell', 'audit_id': 'public'}
        self.items = [{'bindings': [self.binding], 'associated_private_consumers': [self.association]}]
        self.cell = {'associated_private_consumer_audits': [{
            'declaration': 'Consumer', 'audit_id': 'private', 'registry': self.registry_path}]}
        self.audit = {
            'id': 'private', 'state': 'source-reviewed',
            'lean': {'declaration': 'Consumer', 'file': self.module, 'statement': 'True'},
            'source_review': {'state': 'accepted', 'whole_module_review': {
                'file': self.module, 'sha256': self.sha,
                'all_helpers_imports_scoped_context_reviewed': True, 'new_axiom_or_placeholder_found': False}},
            'publication_binding_sha256': 'binding',
            'publication_context': {'binding': {'declaration': 'Public'}, 'associated_private_consumer': {
                'owner_public_declaration': 'Public', 'separate_public_node': False,
                'whole_module': {'file': self.module, 'text': self.text, 'sha256': self.sha},
                'lesson': self.lesson, 'lean_statement': 'True'}}}
        self.registry = {'audits': [self.audit]}
        self.data = {'cells': {'cell': self.cell}, 'lessons': {'Consumer': self.lesson},
                     'declarations': {'Consumer': SimpleNamespace(source_text=self.text, source_file=self.module, has_placeholder=False)},
                     'audits': {'public': {'state': 'source-reviewed', 'source_review': {'state': 'accepted'}}}}
        self.addCleanup(patch.stopall)
        patch.object(c, 'ROOT', self.root).start()
        patch.object(c.publication, 'file_digest', return_value=self.sha).start()
        patch.object(c.publication, 'binding_digest', return_value='binding').start()
        patch.object(c.publication, 'validate', return_value=[]).start()
        patch.object(c.publication.roundtrip, 'load_registry', return_value=self.registry).start()
        self.semantic = patch.object(c.publication.roundtrip, 'validate_registry', return_value=[]).start()

    def check(self):
        return c.associated_private_cell('Consumer', self.items, self.data)

    def test_exact_association_keeps_target_and_checks_private_lesson(self):
        with patch.object(c, 'validate_cell', return_value=[]) as check_cell:
            self.assertEqual(c.validate_targets({'Consumer'}, self.items, self.data), [])
        check_cell.assert_called_once_with('Consumer', self.cell, self.lesson, canonical_owner='Public')
        self.semantic.assert_called_once_with(self.registry)
        self.assertEqual(len(self.items[0]['bindings']), 1)

    def test_absent_or_ambiguous_association_is_rejected(self):
        for rows in ([], [self.association, copy.deepcopy(self.association)]):
            with self.subTest(rows=len(rows)):
                self.items[0]['associated_private_consumers'] = rows
                with self.assertRaises(ValueError): self.check()

    def test_false_marker_alone_is_insufficient(self):
        self.cell['associated_private_consumer_audits'] = []
        with self.assertRaises(ValueError): self.check()

    def test_private_consumer_does_not_become_an_extra_shared_node(self):
        cell = {'cell_id': 'cell', 'shared_floor_audit': {'decision': 'new_canonical_shared'},
                'reuse_plan': {'new_shared_declarations': ['Public'], 'known_consumers': ['a', 'b']}}
        errors = c.validate_cell('Consumer', cell, canonical_owner='Public')
        self.assertFalse(any('canonical shared target missing' in e for e in errors))
        errors = c.validate_cell('Consumer', cell)
        self.assertTrue(any('canonical shared target missing' in e for e in errors))

    def test_wrong_or_escaping_registry_is_rejected(self):
        for path in ('missing.json', '../outside.json', '/tmp/registry.json'):
            with self.subTest(path=path):
                self.cell['associated_private_consumer_audits'][0]['registry'] = path
                with self.assertRaises(ValueError): self.check()

    def test_semantic_failure_is_not_ignored(self):
        self.semantic.return_value = ['decoder not blind']
        with self.assertRaises(ValueError): self.check()

    def test_public_declaration_cannot_claim_private_exemption(self):
        self.data['declarations']['Consumer'].source_text = 'theorem consumer : True := by trivial'
        with self.assertRaises(ValueError): self.check()

    def test_unknown_astis_parent_or_helper_cannot_be_hidden_in_reuse_plan(self):
        for field in ('astis_dependencies', 'helpers'):
            with self.subTest(field=field):
                self.lesson[field] = ['Missing.parent']
                self.cell['reuse_plan'] = {'reused_declarations': ['Missing.parent']}
                with self.assertRaisesRegex(ValueError, 'unknown lesson dependency'): self.check()
                del self.lesson[field]

    def test_placeholder_private_declaration_is_rejected(self):
        self.data['declarations']['Consumer'].has_placeholder = True
        with self.assertRaisesRegex(ValueError, 'without placeholders'): self.check()

    def test_stale_module_lesson_or_binding_is_rejected(self):
        originals = copy.deepcopy(self.audit)
        changes = [('module', lambda: self.audit['publication_context']['associated_private_consumer']['whole_module'].update(text='old')),
                   ('lesson', lambda: self.audit['publication_context']['associated_private_consumer'].update(lesson={'old': True})),
                   ('binding', lambda: self.audit.update(publication_binding_sha256='old')),
                   ('declaration', lambda: self.audit['lean'].update(declaration='Other')),
                   ('helpers', lambda: self.audit['source_review']['whole_module_review'].update(all_helpers_imports_scoped_context_reviewed=False))]
        for label, change in changes:
            self.audit.clear()
            self.audit.update(copy.deepcopy(originals))
            change()
            with self.subTest(label=label), self.assertRaises(ValueError): self.check()

    def test_stale_public_owner_or_duplicate_private_audit_is_rejected(self):
        self.data['audits']['public']['state'] = 'pending'
        with self.assertRaises(ValueError): self.check()
        self.data['audits']['public']['state'] = 'source-reviewed'
        self.registry['audits'].append(copy.deepcopy(self.audit))
        with self.assertRaises(ValueError): self.check()


if __name__ == '__main__': unittest.main()
