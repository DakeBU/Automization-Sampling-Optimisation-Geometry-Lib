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
            with self.assertRaisesRegex(ValueError, "reviewed prose question"):
                candidate.load_sources(root)

    def test_admitted_export_cannot_use_candidate_path(self):
        # Model the absence of independent editorial approval, even after a
        # release-shaped core exists. The native admission gate stays in force.
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "ordinary-export"
            import sog_bench_review as editorial
            with patch.object(candidate.runtime, "_run_bound_submission") as transport, patch.object(
                    editorial, "accepted", return_value=False):
                with self.assertRaisesRegex(ValueError, "currently admitted aligned tasks"):
                    candidate.runtime.export(output, [candidate.ID])
                transport.assert_not_called()
            self.assertFalse(output.exists())

    def test_release_shaped_packet_preserves_exact_oracle_and_no_answer_starter(self):
        bench = candidate.runtime.bench
        item = next(c for c in bench.materialize() if c['id'] == candidate.ID)
        if item.get('fixed_candidate') != candidate.ID:
            self.skipTest('Only applicable to the release-shaped catalogue')
        packet = candidate.runtime.packet(item)
        reviewed = candidate.sources(bench.ROOT)
        self.assertEqual(packet['oracle/Solution.lean.txt'], reviewed['reference'].encode())
        self.assertEqual(bench.sha(packet['oracle/Solution.lean.txt']),
                         '9b1ddd8c76e6ed58304fc4b7c8106713c59eb9370c72a8fa1ebe412b57b2dfb6')
        self.assertEqual(bench.sha(packet['verifier/Challenge.lean']),
                         'f700b8fe50562887de7757b815743e4c361594781e656db2d9c65adcdd6c45e5')
        self.assertEqual(bench.sha(packet['verifier/config.json']),
                         '3c36564eaa878374edcab9ed37542c7ee605ffdd184174f74e2af006d328fbb8')
        self.assertNotIn(candidate.POSITIVE.encode(), packet['agent/Solution.lean.txt'])
        self.assertNotIn(candidate.NEGATIVE.encode(), packet['agent/Solution.lean.txt'])
        self.assertEqual(candidate.runtime.local_imports(item['imports']), [])
        self.assertEqual(item['track_levels'], {'natural-language': 'L5', 'lean': 'L4'})


if __name__ == "__main__":
    unittest.main()
