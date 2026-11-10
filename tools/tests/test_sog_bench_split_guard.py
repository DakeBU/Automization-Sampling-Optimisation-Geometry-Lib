"""Synthetic reservation data only; these are not hidden benchmark items."""
import copy
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from tools import sog_bench_split_guard as guard


PDF = "a" * 64
OTHER_PDF = "b" * 64


def public_core(**changes):
    core = {
        "id": "dev-one", "family": "public-family",
        "assumptions": ["A", "B"], "question": "Synthetic public text",
        "declaration": "Synthetic.Public.answer",
    }
    return {**core, **changes}


def catalog(*rows, schema=2):
    return {"schema_version": schema, "name": "SamplingOptimisationGeometryBench",
            "split": "public-dev", "cores": list(rows)}


def exercises(pdf=PDF):
    return {"schema_version": 1, "books": {"book": {"pdf_sha256": pdf}},
            "exercises": [{"id": "source-old", "book_id": "book", "chapter": "01", "number": "6"}]}


def reservation(**changes):
    family = {
        "family": "candidate-family", "aliases": [], "derived_from_families": [],
        "source_exercise_ids": [], "numbered_sources": [],
        "tasks": [{"id": "candidate-one", "nl_prompt_sha256": "c" * 64}],
        "provenance": {"author": "author", "reviewer": "reviewer", "review_sha256": "d" * 64,
                       "rights": "project-original", "uses_restricted_material": False,
                       "original_independent_family_attested": True},
    }
    return {"schema_version": 1, "split": "private-test", "families": [{**family, **changes}]}


class ReservationGateTests(unittest.TestCase):
    def setUp(self):
        self.exposed = guard.Exposure()
        public = catalog(public_core(textbook_exercise_id="source-old"))
        self.exposed.add_catalog(public, exercises())
        self.exposed.add_graph_ids({"core_id": "dev-one", "tasks": [{"id": "dev-graph"}]}, public)

    def test_fresh_synthetic_reservation_reports_only_aggregate_fields(self):
        item = reservation()
        report = guard.check_reservation(item, self.exposed)
        self.assertEqual(report, {"reservation_families": 1, "reservation_tasks": 1,
                                  "issues": {}, "no_known_conflict": True})
        self.assertNotIn(item["families"][0]["family"], json.dumps(report))
        self.assertNotIn(item["families"][0]["tasks"][0]["nl_prompt_sha256"], json.dumps(report))

    def test_exact_prompt_family_source_answer_and_graph_id_leaks_are_distinct(self):
        item = reservation(
            aliases=["PUBLIC-FAMILY"], derived_from_families=["public-family"],
            source_exercise_ids=["SOURCE-OLD"],
            numbered_sources=[{"pdf_sha256": PDF, "chapter": "1", "number": "6"}],
            tasks=[{"id": "dev-graph",
                    "nl_prompt_sha256": guard.prompt_digest([" B ", "A"], " Synthetic  public text\n"),
                    "lean_answer_declaration": "Synthetic.Public.answer"}],
        )
        report = guard.check_reservation(item, self.exposed)
        self.assertFalse(report["no_known_conflict"])
        self.assertEqual(report["issues"], {
            "known-public-answer_declarations": 1, "known-public-exercise_ids": 1,
            "known-public-families": 1, "known-public-numbered_sources": 1,
            "known-public-prompt_digests": 1, "known-public-task_ids": 1, "public-lineage": 1,
        })

    def test_unknown_and_cross_family_lineage_fail_and_same_family_alias_can_group(self):
        clean = reservation(aliases=["same-family-v0"], derived_from_families=["same-family-v0"])
        self.assertTrue(guard.check_reservation(clean, self.exposed)["no_known_conflict"])
        bad = reservation(derived_from_families=["unknown-lineage", "other-private"])
        other = copy.deepcopy(bad["families"][0])
        other.update(family="other-private", derived_from_families=[],
                     tasks=[{"id": "other-task", "nl_prompt_sha256": "e" * 64}])
        bad["families"].append(other)
        report = guard.check_reservation(bad, self.exposed)
        self.assertEqual(report["issues"], {"unresolved-or-cross-family-lineage": 2})

    def test_duplicates_and_nonindependent_or_restricted_provenance_rejected(self):
        item = reservation()
        other = copy.deepcopy(item["families"][0])
        other["provenance"].update(reviewer="AUTHOR", uses_restricted_material=True,
                                   original_independent_family_attested=False)
        item["families"].append(other)
        report = guard.check_reservation(item, self.exposed)
        self.assertEqual(report["issues"], {
            "missing-independence-attestation": 1, "no-distinct-reviewer": 1,
            "repeated-private-families": 1, "repeated-private-prompt_digests": 1,
            "repeated-private-task_ids": 1, "rights-or-restricted-material": 1,
        })

    def test_shared_prose_support_is_not_mistaken_for_an_aligned_answer(self):
        self.exposed.add_catalog(catalog(public_core(
            id="prose", family="prose-family", lean_enabled=False,
            declaration="Synthetic.Public.supportOnly")), None)
        fresh = reservation(tasks=[{"id": "candidate-lean",
                                    "lean_answer_declaration": "Synthetic.Public.supportOnly"}])
        self.assertTrue(guard.check_reservation(fresh, self.exposed)["no_known_conflict"])

    def test_duplicate_keys_extra_fields_and_empty_reservations_fail_closed(self):
        with self.assertRaisesRegex(guard.GuardError, "duplicate-json-key"):
            guard.parse(b'{"schema_version":1,"schema_version":2}')
        malformed = reservation()
        malformed["families"][0]["tasks"][0]["answer"] = "fixture-sensitive-value"
        with self.assertRaisesRegex(guard.GuardError, "^private-task-schema$"):
            guard.check_reservation(malformed, self.exposed)
        with self.assertRaisesRegex(guard.GuardError, "reservation-needs-families"):
            guard.check_reservation({"schema_version": 1, "split": "private-test", "families": []}, self.exposed)
        with self.assertRaisesRegex(guard.GuardError, "not-a-known-public-catalog"):
            guard.Exposure().add_catalog({"schema_version": 2, "split": "private-test"}, None)

    def test_prompt_hash_preserves_math_case_and_normalizes_unicode_and_spacing(self):
        self.assertEqual(guard.prompt_digest(["B", "Cafe\u0301"], "x  = y"),
                         guard.prompt_digest(["Café", " B "], "x =\ny"))
        self.assertNotEqual(guard.prompt_digest([], "X = y"), guard.prompt_digest([], "x = y"))

    def test_graph_binding_must_agree_with_current_catalog_family(self):
        public = catalog(public_core())
        with self.assertRaisesRegex(guard.GuardError, "public-graph-family-mismatch"):
            self.exposed.add_graph_ids({"core_id": "dev-one", "tasks": [
                {"id": "graph-wrong-family", "family": "unrelated"}]}, public)
        with self.assertRaisesRegex(guard.GuardError, "public-graph-core-not-found"):
            self.exposed.add_graph_ids({"core_id": "missing", "tasks": [
                {"id": "graph-missing-core"}]}, public)


@unittest.skipUnless(shutil.which("git"), "Git executable needed for history and path fixtures")
class GitExposureTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.repo = Path(directory.name)
        self.git("init", "-q")
        self.git("config", "user.name", "Synthetic Test")
        self.git("config", "user.email", "synthetic@example.invalid")
        self.git("config", "commit.gpgsign", "false")

    def git(self, *args):
        return subprocess.check_output(["git", *args], cwd=self.repo, stderr=subprocess.STDOUT).strip()

    def write(self, relative, data):
        p = self.repo / relative
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(guard.canonical(data) if not isinstance(data, bytes) else data)
        return p

    def commit(self, *files):
        self.git("add", "--", *files)
        self.git("commit", "-qm", "synthetic catalog snapshot")
        return self.git("rev-parse", "HEAD").decode()

    def test_git_history_detects_retired_catalogs_and_map_only_or_graph_only_changes(self):
        self.write(guard.CATALOG, catalog(public_core(textbook_exercise_id="source-old"), schema=1))
        self.write(guard.EXERCISES, exercises())
        first = self.commit(guard.CATALOG, guard.EXERCISES)
        self.write(guard.EXERCISES, exercises(OTHER_PDF))
        self.commit(guard.EXERCISES)
        graph = guard.GRAPH_SPECS[0]
        self.write(graph, {"tasks": [{"id": "graph-retired", "family": "old-graph-family"}]})
        self.commit(graph)
        self.write(graph, {"tasks": [{"id": "graph-current", "family": "new-graph-family"}]})
        self.write(guard.CATALOG, catalog(public_core(id="dev-two", family="renamed", question="New text")))
        final = self.commit(graph, guard.CATALOG)
        found, receipt = guard.inventory(self.repo, [final])
        self.assertEqual(receipt["public_snapshots"], 4)
        self.assertEqual(receipt["history_status"], "not-shallow-declared-tips-only")
        self.assertEqual(receipt["public_history_sha256"],
                         guard.inventory(self.repo, [final, final])[1]["public_history_sha256"])
        self.assertNotEqual(receipt["public_history_sha256"],
                            guard.inventory(self.repo, [first])[1]["public_history_sha256"])
        self.assertTrue({"dev-one", "dev-two", "graph-retired", "graph-current"} <= found.task_ids)
        self.assertEqual(found.numbered_sources, {(PDF, "1", "6"), (OTHER_PDF, "1", "6")})

    def test_unavailable_declared_tip_and_non_commit_inputs_fail(self):
        self.write(guard.CATALOG, catalog(public_core()))
        self.commit(guard.CATALOG)
        with self.assertRaisesRegex(guard.GuardError, "declare-exact-public-commit-ids"):
            guard.inventory(self.repo, ["HEAD"])
        with self.assertRaisesRegex(guard.GuardError, "public-git-object-unavailable"):
            guard.inventory(self.repo, ["0" * 40])

    def test_registered_compiler_slice_changes_remain_visible_after_retirement(self):
        self.write(guard.CATALOG, catalog(public_core()))
        self.commit(guard.CATALOG)
        spec = f"{guard.DIRECTORY}/compiled_new_slice_graph_tasks.json"
        self.write(guard.GRAPH_INDEX, {"schema_version": 1, "slices": ["new-slice"]})
        self.write(spec, {"core_id": "dev-one", "tasks": [{"id": "graph-first"}]})
        self.commit(guard.GRAPH_INDEX, spec)
        self.write(spec, {"core_id": "dev-one", "tasks": [{"id": "graph-retired"}]})
        self.commit(spec)  # The slice file changes, with no catalog or index change.
        self.write(spec, {"core_id": "dev-one", "tasks": [{"id": "graph-final"}]})
        tip = self.commit(spec)
        found, receipt = guard.inventory(self.repo, [tip])
        self.assertEqual(receipt["public_snapshots"], 4)
        self.assertTrue({"graph-first", "graph-retired", "graph-final"} <= found.task_ids)
        reserved = reservation(tasks=[{"id": "graph-retired", "nl_prompt_sha256": "c" * 64}])
        self.assertEqual(guard.check_reservation(reserved, found)["issues"],
                         {"known-public-task_ids": 1})

    def test_registered_compiler_slice_missing_from_a_public_commit_fails_closed(self):
        self.write(guard.CATALOG, catalog(public_core()))
        self.write(guard.GRAPH_INDEX, {"schema_version": 1, "slices": ["not-present"]})
        tip = self.commit(guard.CATALOG, guard.GRAPH_INDEX)
        with self.assertRaisesRegex(guard.GuardError, "public-git-object-unavailable"):
            guard.inventory(self.repo, [tip])

    def test_retired_family_introduced_in_merge_resolution_is_still_public(self):
        initial = catalog(public_core())
        self.write(guard.CATALOG, initial)
        base = self.commit(guard.CATALOG)
        primary = self.git("branch", "--show-current").decode()
        self.git("switch", "-c", "synthetic-side", base)
        self.write("side.txt", b"Side branch only\n")
        self.commit("side.txt")
        self.git("switch", primary)
        self.write("main.txt", b"Main branch only\n")
        self.commit("main.txt")
        self.git("merge", "--no-ff", "--no-commit", "synthetic-side")
        merge_only = public_core(id="dev-merge-only", family="merge-only-family",
                                 question="Synthetic merge-only prompt",
                                 declaration="Synthetic.MergeOnly.answer")
        self.write(guard.CATALOG, catalog(public_core(), merge_only))
        exposed_merge = self.commit(guard.CATALOG)
        self.assertEqual(len(self.git("rev-list", "--parents", "-n", "1", exposed_merge).split()), 3)
        self.write(guard.CATALOG, initial)
        tip = self.commit(guard.CATALOG)

        found, receipt = guard.inventory(self.repo, [tip])
        self.assertIn("dev-merge-only", found.task_ids)
        self.assertIn("Synthetic.MergeOnly.answer", found.answer_declarations)
        self.assertEqual(receipt["public_snapshots"], 3)
        result = guard.check_reservation(reservation(aliases=["merge-only-family"]), found)
        self.assertEqual(result["issues"], {"known-public-families": 1})

    def test_shallow_history_never_allows_a_reservation(self):
        self.write(guard.CATALOG, catalog(public_core()))
        tip = self.commit(guard.CATALOG)
        actual_git = guard.git_bytes
        def shallow(repo, *args, **kwargs):
            return b"true\n" if args == ("rev-parse", "--is-shallow-repository") else actual_git(repo, *args, **kwargs)
        with patch.object(guard, "git_bytes", side_effect=shallow):
            with self.assertRaisesRegex(guard.GuardError, "shallow-public-history"):
                guard.inventory(self.repo, [tip])
            _, result = guard.inventory(self.repo, [tip], observation_only=True)
        self.assertEqual(result["history_status"], "shallow-observation-only")
        self.assertNotIn("private_check", result)

    def test_reservation_path_must_be_ignored_and_not_tracked(self):
        self.write(".gitignore", b"/.astis/\n")
        ordinary = self.write("ordinary.json", reservation())
        hidden = self.write(".astis/local.json", reservation())
        self.assertEqual(guard.private_input(hidden, self.repo), reservation())
        with self.assertRaisesRegex(guard.GuardError, "reservation-must-stay-out-of-tracked-paths"):
            guard.private_input(ordinary, self.repo)
        self.git("add", "-f", "--", ".astis/local.json")
        with self.assertRaisesRegex(guard.GuardError, "reservation-must-stay-ignored"):
            guard.private_input(hidden, self.repo)


if __name__ == "__main__":
    unittest.main()
