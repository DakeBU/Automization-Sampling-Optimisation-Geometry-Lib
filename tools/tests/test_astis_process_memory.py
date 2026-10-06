import copy
import json
import unittest
from pathlib import Path

from tools import astis_frontier_cells
from tools import astis_process_memory


ROOT = Path(__file__).resolve().parents[2]


class ProcessMemoryTests(unittest.TestCase):
    def test_current_process_memory_validates(self):
        self.assertEqual(astis_process_memory.validate(), [])

    def _schema3_cell(self):
        path = ROOT / "research-wiki/frontier-cells/ASTIS-SHARED-random-scan-reversibility.json"
        cell = json.loads(path.read_text(encoding="utf-8"))
        cell["schema_version"] = 3
        cell["learning_contract"] = {
            "control_plane_math_authority": False,
            "process_memory_checked": True,
            "process_memory_ids": ["ASTIS-PM-QUADRATIC-TILT-MEASURE-ROLES"],
            "failure_class": "NONE",
            "salvage": {
                "required": False,
                "status": "not-applicable",
                "reason": "synthetic passing cell has no failed route",
                "promoted_fragments": [],
                "discarded_fragments": [],
            },
            "parallelism": {
                "decision": "serial",
                "direction_fingerprints": [],
                "expected_information_gain": "",
                "shared_verified_context_digest": "",
            },
            "cross_route_blind_spot_audit": {
                "required": False,
                "status": "not-applicable",
                "evidence": "",
                "canonical_route": "",
                "selection_reason": "",
            },
            "reader_backpressure": {
                "purification_status": "not-applicable",
                "exposition_seal_status": "not-applicable",
                "exposition_evidence": "",
                "source_expansion_nodes": [],
                "lean_expansion_nodes": [],
                "assumptions_preserved": False,
                "boundary_preserved": False,
            },
        }
        return cell

    def test_schema3_learning_contract_passes(self):
        errors = astis_frontier_cells.validate_cells([self._schema3_cell()])
        self.assertEqual(errors, [])

    def test_parallel_schema3_requires_cross_route_audit(self):
        cell = self._schema3_cell()
        cell["learning_contract"]["parallelism"] = {
            "decision": "parallel",
            "direction_fingerprints": ["route-a", "route-b"],
            "expected_information_gain": "different proof mechanisms",
            "shared_verified_context_digest": "sha256:test",
        }
        cell["learning_contract"]["cross_route_blind_spot_audit"] = {
            "required": False,
            "status": "not-applicable",
            "evidence": "",
            "canonical_route": "",
            "selection_reason": "",
        }
        errors = astis_frontier_cells.validate_cells([cell])
        self.assertTrue(any("common-blind-spot" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
