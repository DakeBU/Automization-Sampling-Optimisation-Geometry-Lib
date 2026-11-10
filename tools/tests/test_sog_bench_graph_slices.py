"""Registry routing preserves existing compiled graph bindings."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
import sog_bench_graph_slices as slices
import sog_bench_compiled_graph as compiler


class SliceRegistryTests(unittest.TestCase):
    def test_existing_slice_artifacts_keep_their_exact_identity(self):
        configured = {label: (spec, snapshot) for label, spec, snapshot in slices.configured()}
        self.assertEqual(configured['transport'], (compiler.SPEC, compiler.SNAPSHOT))
        self.assertEqual(configured['flow'], (compiler.FLOW_SPEC, compiler.FLOW_SNAPSHOT))
        for label, (spec, snapshot) in configured.items():
            self.assertEqual(snapshot.name, f'compiled-{label}-graph.json')
            for row in json.loads(spec.read_text(encoding='utf-8'))['tasks']:
                self.assertEqual(slices.artifact_for(row['id']), snapshot.name)

    def test_schema_bounds_and_rejects_paths_or_duplicate_slice_ids(self):
        for data in ({}, {'schema_version': True, 'slices': ['flow']},
                     {'schema_version': 1, 'slices': []},
                     {'schema_version': 1, 'slices': ['flow', 'flow']},
                     {'schema_version': 1, 'slices': ['../private']},
                     {'schema_version': 1, 'slices': ['foreign/file']},
                     {'schema_version': 1, 'slices': [str(x) for x in range(17)]}):
            with self.subTest(data=data), self.assertRaises(ValueError):
                slices.labels(data)

    def test_unregistered_files_are_ignored_but_missing_registered_artifacts_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            (folder / slices.INDEX).write_text('{"schema_version":1,"slices":["candidate"]}')
            (folder / 'compiled_candidate_graph_tasks.json').write_text('{}')
            (folder / 'compiled_unregistered_graph_tasks.json').write_text('{}')
            with self.assertRaises(ValueError):
                slices.configured(folder)
            (folder / 'compiled-candidate-graph.json').write_text('{}')
            self.assertEqual([row[0] for row in slices.configured(folder)], ['candidate'])

if __name__ == '__main__':
    unittest.main()
