from __future__ import annotations

import dataclasses
import json
import multiprocessing
import tempfile
import unittest
from pathlib import Path

from tools.astis_harness import (
    MemoryRecord,
    ProofBranch,
    append_jsonl,
    append_branch,
    append_memory,
    bounded_memory_capsule,
    classify_retry,
    load_jsonl,
    ordered_control_events,
    reconcile_frontier,
    record_route_attempt,
    recover_run_events,
    recover_jsonl,
    restore_branch,
    route_fingerprint,
    run_with_retry,
    statement_header_hash,
    validate_role_preflight,
    validate_role_artifact,
)


def append_worker(path: str, worker: int, count: int) -> None:
    for index in range(count):
        append_jsonl(Path(path), {"worker": worker, "index": index})


def append_same_memory_worker(path: str) -> None:
    record = MemoryRecord(
        record_id="same",
        kind="analytic_contract",
        task_id="ASTIS-CHEWI-001",
        target="target",
        exact_assumptions=("assumption",),
        measure="measure",
        codomain="Real",
        declaration_hash="hash",
        source="source",
    )
    try:
        append_memory(Path(path), record)
    except ValueError:
        pass


class HarnessStorageTests(unittest.TestCase):
    def test_append_preserves_prefix_and_exact_utf8_lf_payload(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "events.jsonl"
            prefix = b'{"old":1}\r\n'
            path.write_bytes(prefix)
            append_jsonl(path, {"new": "\u03bc"})
            self.assertEqual(path.read_bytes(), prefix + '{"new":"\u03bc"}\n'.encode("utf-8"))

    def test_interrupted_append_is_recovered(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "events.jsonl"
            path.write_bytes(b'{"ok":1}\n{"interrupted":')
            records, recovered = recover_jsonl(path)
            self.assertTrue(recovered)
            self.assertEqual(records, [{"ok": 1}])
            append_jsonl(path, {"ok": 2})
            self.assertEqual(load_jsonl(path), [{"ok": 1}, {"ok": 2}])

    def test_concurrent_append_serializes_complete_records(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "events.jsonl"
            processes = [
                multiprocessing.Process(target=append_worker, args=(str(path), worker, 20))
                for worker in range(4)
            ]
            for process in processes:
                process.start()
            for process in processes:
                process.join(10)
                self.assertEqual(process.exitcode, 0)
            records = load_jsonl(path)
            self.assertEqual(len(records), 80)
            self.assertEqual(len({(item["worker"], item["index"]) for item in records}), 80)

    def test_concurrent_memory_check_and_append_is_one_transaction(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "memory.jsonl"
            processes = [
                multiprocessing.Process(target=append_same_memory_worker, args=(str(path),))
                for _ in range(4)
            ]
            for process in processes:
                process.start()
            for process in processes:
                process.join(10)
                self.assertEqual(process.exitcode, 0)
            self.assertEqual([item["record_id"] for item in load_jsonl(path)], ["same"])

    def test_interrupted_role_is_closed_once(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "events.jsonl"
            append_jsonl(path, {
                "event": "role_started",
                "execution_id": "cycle-1-lower",
                "task_id": "ASTIS-CHEWI-001",
                "role": "lower",
            })
            self.assertEqual(recover_run_events(path), ["cycle-1-lower"])
            self.assertEqual(recover_run_events(path), [])
            self.assertEqual(load_jsonl(path)[-1]["event"], "role_interrupted")


class HarnessMemoryTests(unittest.TestCase):
    def test_typed_memory_requires_exact_fields_and_supersession(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "memory.jsonl"
            first = MemoryRecord(
                record_id="r1",
                kind="analytic_contract",
                task_id="ASTIS-CHEWI-001",
                target="weighted IBP",
                exact_assumptions=("ContDiff R 1 V", "CompactlySupportedC2 f"),
                measure="volume",
                codomain="Real",
                declaration_hash="abc",
                source="Chewi Example 1.2.8",
            )
            append_memory(path, first)
            second = MemoryRecord(
                record_id="r2",
                kind="verified_lemma",
                task_id="ASTIS-CHEWI-001",
                target="weighted IBP",
                exact_assumptions=first.exact_assumptions,
                measure="volume",
                codomain="Real",
                declaration_hash="def",
                source="AutoSamplingTheory/.../Langevin.lean",
                verifier_status="accepted",
                local_status="compiled",
                supersedes=("r1",),
            )
            append_memory(path, second)
            self.assertEqual([item["record_id"] for item in load_jsonl(path)], ["r1", "r2"])

    def test_bounded_capsule_preserves_exact_assumptions(self) -> None:
        records = [
            {
                "record_id": f"r{index}",
                "task_id": "ASTIS-CHEWI-001",
                "exact_assumptions": ["ContDiff ℝ 2 f", "Integrable G μ"],
                "measure": "volume.withDensity rho",
                "supersedes": [],
            }
            for index in range(30)
        ]
        capsule = bounded_memory_capsule(records, task_id="ASTIS-CHEWI-001", max_records=5)
        self.assertEqual(capsule["record_count"], 5)
        self.assertEqual(capsule["omitted_count"], 25)
        self.assertEqual(
            capsule["records"][-1]["exact_assumptions"],
            ["ContDiff ℝ 2 f", "Integrable G μ"],
        )

    def test_immutable_branch_tree_restores_exact_contract(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "branches.jsonl"
            root = ProofBranch(
                branch_id="root",
                task_id="ASTIS-CHEWI-001",
                parent_branch_id="",
                target_statement="integral (generator V f) π = 0",
                exact_assumptions=("ContDiff ℝ 1 V", "CompactlySupportedC2 f"),
                measure="normalizedGibbs V",
                spaces=("EuclideanSpace ℝ (Fin n)",),
                regularity=("V is C1", "f is C2"),
                integrability=("exp(-V) is integrable",),
                domination=("compact support of f",),
                domains=("C_c^2 core",),
                source_citations=("Chewi Example 1.2.8",),
            )
            append_branch(path, root)
            child = dataclasses.replace(
                root,
                branch_id="child",
                parent_branch_id="root",
                target_statement="core invariance",
            )
            append_branch(path, child)
            restored = restore_branch(path, "child")
            self.assertEqual(restored["parent_branch_id"], "root")
            self.assertEqual(restored["exact_assumptions"], list(root.exact_assumptions))
            self.assertEqual(restored["measure"], "normalizedGibbs V")

    def test_statement_fence_ignores_proof_body(self) -> None:
        one = "theorem foo (h : P) : Q := by exact first"
        two = "theorem foo (h : P) : Q := by exact second"
        changed = "theorem foo (h : P) (h2 : R) : Q := by exact second"
        self.assertEqual(statement_header_hash(one), statement_header_hash(two))
        self.assertNotEqual(statement_header_hash(one), statement_header_hash(changed))


class RoutePolicyTests(unittest.TestCase):
    def test_two_unchanged_repeats_freeze_route(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "routes.jsonl"
            fingerprint = route_fingerprint(
                target_statement="theorem target : P",
                missing_property="Integrable f mu",
                assumptions=["Measurable f"],
                mathlib_candidates=["MeasureTheory.Integrable"],
                compiler_error_class="type_mismatch",
            )
            decisions = [
                record_route_attempt(
                    path,
                    task_id="ASTIS-CHEWI-001",
                    leaf_id="leaf",
                    fingerprint=fingerprint,
                    candidate="same candidate",
                    exact_subgoal="same subgoal",
                )["decision"]
                for _ in range(3)
            ]
            self.assertEqual(decisions, ["continue", "continue", "freeze_for_review"])

    def test_changed_candidate_resets_repeat_counter(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "routes.jsonl"
            for candidate in ["a", "a", "b"]:
                result = record_route_attempt(
                    path,
                    task_id="task",
                    leaf_id="leaf",
                    fingerprint="fp",
                    candidate=candidate,
                    exact_subgoal="goal",
                )
            self.assertEqual(result["unchanged_repeat_count"], 0)
            self.assertEqual(result["decision"], "continue")

    def test_retry_only_transient_provider_failures(self) -> None:
        self.assertEqual(classify_retry("provider_timeout"), "retry")
        self.assertEqual(classify_retry("lean_type_mismatch"), "freeze_for_review")

    def test_faux_provider_retry_policy(self) -> None:
        calls = []

        def transient_provider() -> str:
            calls.append("call")
            if len(calls) == 1:
                raise RuntimeError("timeout")
            return "ok"

        value, attempts = run_with_retry(
            transient_provider, lambda _: "provider_timeout", max_transient_retries=2
        )
        self.assertEqual((value, attempts), ("ok", 2))

        def proof_failure() -> str:
            raise RuntimeError("type mismatch")

        with self.assertRaises(RuntimeError):
            run_with_retry(proof_failure, lambda _: "lean_type_mismatch")

    def test_steering_precedes_followup_and_preserves_fifo(self) -> None:
        events = [
            {"kind": "followup", "id": 1},
            {"kind": "steering", "id": 2},
            {"kind": "steering", "id": 3},
            {"kind": "followup", "id": 4},
        ]
        self.assertEqual([item["id"] for item in ordered_control_events(events)], [2, 3, 1, 4])


class FrontierReplayTests(unittest.TestCase):
    def test_shadow_replay_ignores_stale_cycle_28_frontier(self) -> None:
        frontier = reconcile_frontier()
        statuses = {item["node_id"]: item["local_status"] for item in frontier["nodes"]}
        for node in [
            "generator_display_integrability",
            "gibbs_tail",
            "whole_space_weighted_ibp",
            "generator_core_contract",
            "normalized_core_annihilation",
            "abstract_semigroup_invariance_bridge",
            "conditional_langevin_core_invariance",
            "unit_cutoff_second_derivative_bound",
            "second_order_cutoff_scaling",
            "chapter1_product_coupling",
        ]:
            self.assertEqual(statuses[node], "compiled")
        self.assertEqual(statuses["concrete_langevin_semigroup"], "external_dependency")
        self.assertIsNone(frontier["selected_ready_leaf"])

    def test_role_preflight_is_role_specific(self) -> None:
        self.assertEqual(
            validate_role_preflight("lower", ["rg", "lake_env_lean", "apply_patch"]), []
        )
        self.assertIn(
            "missing tool: source_reader",
            validate_role_preflight("upper", ["frontier_reader", "memory_reader"]),
        )

    def test_role_artifact_schema_is_restored_per_role(self) -> None:
        lower = {
            "artifact": "proof_attempt",
            "leaf_id": "leaf",
            "statement_header_hash": "abc",
            "compiler_status": "compiled",
            "exact_subgoal": "none",
        }
        self.assertEqual(validate_role_artifact("lower", lower), [])
        self.assertIn(
            "artifact kind must be analytic_contract",
            validate_role_artifact("upper", lower),
        )


if __name__ == "__main__":
    unittest.main()
