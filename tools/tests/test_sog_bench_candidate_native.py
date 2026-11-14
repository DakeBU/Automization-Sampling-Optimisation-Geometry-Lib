from pathlib import Path
import json
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import sog_bench_candidate_native as candidate


class FixedCandidateTest(unittest.TestCase):
    def test_proofless_stage_and_distinct_controls(self):
        all_sources = candidate.sources(candidate.runtime.ROOT)
        starter = all_sources["starter"]
        self.assertIn("def ProposedTarget : Prop := Positive ∧ Negative", starter)
        self.assertIn("variance (fun x => (W x).toReal) P", starter)
        self.assertIn("∫⁻ x, terminalCharge m x ∂Q", starter)
        self.assertNotIn(candidate.POSITIVE.rsplit(".", 1)[1], starter)
        self.assertNotIn(candidate.NEGATIVE.rsplit(".", 1)[1], starter)
        self.assertNotIn("sorry", starter)
        self.assertTrue(all(line.startswith("import Mathlib.") for line in
                            starter.splitlines() if line.startswith("import ")))
        self.assertIn("sogBenchTarget : SogBenchCandidate.Positive", all_sources["positive-only"])
        self.assertIn("def Negative : Prop := True", all_sources["weakened-negative"])
        self.assertIn("True.intro", all_sources["weakened-negative"])
        self.assertIn("by sorry⟩", all_sources["proof-hole"])
        self.assertNotIn("sorry", all_sources["reference"])
        self.assertEqual(len({all_sources[label] for label in candidate.EXPECTED}), 4)
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "frozen"
            record = candidate.freeze(output)
            self.assertFalse(record["admitted"])
            self.assertFalse(record["model_measurement"])
            self.assertEqual(set(p.relative_to(output / "stage").as_posix()
                                 for p in (output / "stage").rglob("*") if p.is_file()),
                             {"Challenge.lean", "config.json", "project/lakefile.lean",
                              "project/lake-manifest.json", "project/lean-toolchain"})
            self.assertEqual(json.loads((output / "stage/config.json").read_bytes())["definition_names"], [])
            self.assertEqual((output / "fixtures/reference.lean.txt").read_bytes(),
                             all_sources["reference"].encode())
            self.assertTrue(all(candidate.runtime.bench.sha((output / rel).read_bytes()) == digest
                                for rel, digest in record["files"].items()))
            with self.assertRaises(FileExistsError):
                candidate.freeze(output)

    def test_sealed_question_and_proof_changes_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for rel in (candidate.REVIEW, candidate.BENCH / "cores.json",
                        Path("lean-toolchain"), Path("lake-manifest.json"),
                        *(candidate.BENCH / "candidates" / s for s in candidate.SOURCES)):
                path = root / rel
                path.parent.mkdir(exist_ok=True, parents=True)
                shutil.copyfile(candidate.runtime.ROOT / rel, path)
            candidate.load_sources(root)
            proof = root / candidate.BENCH / "candidates" / candidate.SOURCES[0]
            original = proof.read_bytes()
            proof.write_bytes(original + b"\n")
            with self.assertRaisesRegex(ValueError, "Sealed source/toolchain drift"):
                candidate.load_sources(root)
            proof.write_bytes(original)
            catalog = root / candidate.BENCH / "cores.json"
            data = json.loads(catalog.read_bytes())
            core = next(c for c in data["cores"] if c["id"] == candidate.ID)
            core["question"] += " Changed after review."
            catalog.write_bytes(candidate.runtime.bench.encoded(data))
            with self.assertRaisesRegex(ValueError, "reviewed, still-unpaired"):
                candidate.load_sources(root)

    def test_admitted_export_cannot_use_candidate_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "ordinary-export"
            with patch.object(candidate.runtime, "_run_bound_submission") as transport:
                with self.assertRaisesRegex(ValueError, "currently admitted aligned tasks"):
                    candidate.runtime.export(output, [candidate.ID])
                transport.assert_not_called()
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
