from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path
from unittest.mock import patch

from tools import astis_semantic_roundtrip as roundtrip_api

from tools.astis_semantic_roundtrip import (
    DECODER_INPUT_ARTIFACTS,
    SEMANTIC_SLOTS,
    decoder_packet,
    repair_proposal_sha256,
    repair_reviewer_packet,
    semantic_reviewer_packet,
    sha256_text,
    validate_registry,
)


class ArtifactDecoderHashTests(unittest.TestCase):
    def load_artifact(self, decoder_hashes):
        fragment = {"id": "ASTIS-RT-ARTIFACT-TEST", **{
            key: key + ".json" for key in
            ("reviewer_packet", "decoder_packet", "decoder_result", "review_result")}}
        documents = [{}, {}, {"decoder_run_sha256": "unchanged-run", **decoder_hashes}, {}]
        with patch.object(Path, "is_file", return_value=True), patch.object(
                roundtrip_api, "_json", side_effect=documents):
            return roundtrip_api._artifact_backed_audit(fragment, Path("audit.json"))

    def test_legacy_and_explicit_hash_fields_preserve_signed_decoder_run(self):
        for fields in ({"packet_sha256": "packet"},
                       {"decoder_packet_sha256": "packet"},
                       {"packet_sha256": "packet", "decoder_packet_sha256": "packet"}):
            with self.subTest(fields=fields):
                reconstruction = self.load_artifact(fields)["reconstruction"]
                self.assertEqual(reconstruction["decoder_packet_sha256"], "packet")
                self.assertEqual(reconstruction["decoder_run_sha256"], "unchanged-run")

    def test_conflicting_hash_aliases_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "conflicting decoder packet hashes"):
            self.load_artifact({"packet_sha256": "old", "decoder_packet_sha256": "different"})


def valid_registry() -> dict:
    source_text = "For every x in the domain, P x implies Q x."
    lean_statement = "∀ x : α, P x → Q x"
    reconstructed_text = "For every x of type α, if P x holds, then Q x holds."
    repaired_text = "Assume x lies in α; if P x holds, then Q x holds."
    slots = {
        slot: {
            "original": f"source {slot}",
            "reconstructed": f"source {slot}",
            "relation": "same",
            "evidence": f"the {slot} agree",
        }
        for slot in SEMANTIC_SLOTS
    }
    audit = {
        "id": "ASTIS-RT-TEST-001",
        "state": "accepted",
        "graph_node": "source:test",
        "source": {
            "source_id": "SOURCE-SECRET-99",
            "anchor": "Theorem 1",
            "original_text": source_text,
            "text_sha256": sha256_text(source_text),
        },
        "lean": {
            "declaration": "Test.theoremOne",
            "file": "Test.lean",
            "statement": lean_statement,
            "statement_sha256": sha256_text(lean_statement),
            "compiled": True,
            "formalizer": "formalizer-test",
            "decoder_context": ["P : α → Prop", "Q : α → Prop"],
        },
        "semantic_slots": slots,
        "deltas": [],
        "verdict": "exact",
        "source_review": {
            "state": "pending",
            "reviewer": "",
            "independent_from_formalizer": False,
            "independent_from_decoder": False,
            "evidence": "",
        },
        "repairs": [],
    }
    packet = decoder_packet(audit)
    audit["reconstruction"] = {
        "text": reconstructed_text,
        "text_sha256": sha256_text(reconstructed_text),
        "decoder": "independent-decoder-test",
        "decoder_run_sha256": sha256_text("decoder-run-test"),
        "decoder_packet_sha256": packet["packet_sha256"],
        "source_text_visible": False,
        "lean_statement_sha256": sha256_text(lean_statement),
        "input_artifacts": packet["input_artifacts"],
    }
    reviewer_packet = semantic_reviewer_packet(audit)
    audit["source_review"] = {
        "state": "accepted",
        "reviewer": "independent-reviewer",
        "independent_from_formalizer": True,
        "independent_from_decoder": True,
        "evidence": "slot-by-slot comparison checked",
        "review_run_sha256": sha256_text("source-review-run-test"),
        "reviewer_packet_sha256": reviewer_packet["packet_sha256"],
    }
    audit["_test_repaired_text"] = repaired_text
    return {
        "schema_version": 1,
        "protocol": {
            "name": "ASTIS Semantic Round-Trip",
            "status": "active",
            "decoder_blindness": "required",
            "decoder_context_content_scan": "required",
            "independent_source_review": "required",
            "source_review_packet_binding": "required",
            "independent_repair_review": "required",
            "repair_review_packet_binding": "required",
            "decoder_allowed_inputs": list(DECODER_INPUT_ARTIFACTS),
            "semantic_slots": list(SEMANTIC_SLOTS),
        },
        "audits": [audit],
    }


def reviewed_repair(audit: dict, *, repair_id: str = "ASTIS-REPAIR-TEST-OK") -> dict:
    repaired_text = audit.get("_test_repaired_text", "Assume x lies in α; if P x holds, then Q x holds.")
    repair = {
        "id": repair_id,
        "class": "assumption-addition",
        "status": "accepted",
        "necessity": "mathematically-necessary",
        "proposed_change": "Add measurability of f.",
        "reconstructed_statement": repaired_text,
        "statement_sha256": sha256_text(repaired_text),
        "justification": "The integral is otherwise not defined.",
        "minimality_evidence": "Only measurability is used.",
        "reference_or_counterexample": "Reference theorem showing the integral requires measurability.",
    }
    packet = repair_reviewer_packet(audit, repair)
    repair["review"] = {
        "state": "accepted",
        "reviewer": "independent-repair-reviewer",
        "independent_from_formalizer": True,
        "independent_from_decoder": True,
        "evidence": "The proposed measurability addition is necessary and minimal.",
        "review_run_sha256": sha256_text("repair-review-run-test"),
        "reviewer_packet_sha256": packet["packet_sha256"],
        "proposal_sha256": repair_proposal_sha256(repair),
    }
    return repair


class SemanticRoundTripTests(unittest.TestCase):
    def test_valid_exact_audit_passes(self) -> None:
        registry = valid_registry()
        registry["audits"][0].pop("_test_repaired_text")
        self.assertEqual(validate_registry(registry), [])

    def test_decoder_packet_is_anonymous_and_source_blind(self) -> None:
        audit = copy.deepcopy(valid_registry()["audits"][0])
        packet = decoder_packet(audit)
        encoded = json.dumps(packet)
        for secret in (
            audit["id"],
            audit["source"]["original_text"],
            audit["source"]["source_id"],
            audit["source"]["anchor"],
            audit["lean"]["declaration"],
            audit["lean"]["file"],
        ):
            self.assertNotIn(secret, encoded)
        self.assertFalse(packet["non_disclosure"]["source_text_included"])
        self.assertFalse(packet["non_disclosure"]["audit_identity_included"])
        self.assertEqual(packet["lean"]["statement"], audit["lean"]["statement"])
        self.assertEqual(packet["input_artifacts"], list(DECODER_INPUT_ARTIFACTS))
        self.assertEqual(len(packet["packet_sha256"]), 64)

    def test_definition_context_cannot_smuggle_source_or_identity(self) -> None:
        registry = valid_registry()
        audit = registry["audits"][0]
        audit.pop("_test_repaired_text")
        audit["lean"]["decoder_context"] = [
            "P : α → Prop",
            f"Source note: {audit['source']['anchor']}",
            f"Declaration: {audit['lean']['declaration']}",
            audit["source"]["original_text"],
        ]
        errors = validate_registry(registry)
        self.assertTrue(any("decoder_context" in error and "source anchor" in error for error in errors))
        self.assertTrue(any("decoder_context" in error and "Lean declaration identity" in error for error in errors))
        self.assertTrue(any("decoder_context" in error and "original theorem" in error for error in errors))

    def test_decoder_context_rejects_structured_side_channel(self) -> None:
        registry = valid_registry()
        audit = registry["audits"][0]
        audit.pop("_test_repaired_text")
        audit["lean"]["decoder_context"] = [{"definition": "P", "source": audit["source"]["source_id"]}]
        errors = validate_registry(registry)
        self.assertTrue(any("decoder_context[0] must be a non-empty string" in error for error in errors))

    def test_decoder_that_saw_source_or_used_wrong_packet_is_rejected(self) -> None:
        registry = valid_registry()
        audit = registry["audits"][0]
        audit.pop("_test_repaired_text")
        reconstruction = audit["reconstruction"]
        reconstruction["source_text_visible"] = True
        reconstruction["input_artifacts"].append("original-theorem")
        reconstruction["decoder_packet_sha256"] = sha256_text("wrong-packet")
        errors = validate_registry(registry)
        self.assertTrue(any("source_text_visible=false" in error for error in errors))
        self.assertTrue(any("canonical blind packet" in error for error in errors))
        self.assertTrue(any("input_artifacts" in error for error in errors))

    def test_formalizer_decoder_and_reviewer_must_be_distinct(self) -> None:
        registry = valid_registry()
        audit = registry["audits"][0]
        audit.pop("_test_repaired_text")
        audit["reconstruction"]["decoder"] = audit["lean"]["formalizer"]
        audit["source_review"]["reviewer"] = audit["lean"]["formalizer"]
        errors = validate_registry(registry)
        self.assertTrue(any("decoder must be independent" in error for error in errors))
        self.assertTrue(any("reviewer identity must differ" in error for error in errors))

    def test_source_review_is_bound_to_packet_and_run(self) -> None:
        registry = valid_registry()
        audit = registry["audits"][0]
        audit.pop("_test_repaired_text")
        audit["source_review"]["reviewer_packet_sha256"] = sha256_text("wrong-review-packet")
        audit["source_review"]["review_run_sha256"] = "not-a-hash"
        errors = validate_registry(registry)
        self.assertTrue(any("canonical reviewer packet" in error for error in errors))
        self.assertTrue(any("review_run_sha256" in error for error in errors))

    def test_valid_independently_reviewed_repair_passes(self) -> None:
        registry = valid_registry()
        audit = registry["audits"][0]
        repair = reviewed_repair(audit)
        audit["repairs"] = [repair]
        audit.pop("_test_repaired_text")
        self.assertEqual(validate_registry(registry), [])

    def test_accepted_repair_requires_its_own_review_and_real_reference(self) -> None:
        registry = valid_registry()
        audit = registry["audits"][0]
        repaired_text = audit.pop("_test_repaired_text")
        audit["repairs"] = [
            {
                "id": "ASTIS-REPAIR-TEST-001",
                "class": "assumption-addition",
                "status": "accepted",
                "necessity": "mathematically-necessary",
                "proposed_change": "Add measurability of f.",
                "reconstructed_statement": repaired_text,
                "statement_sha256": sha256_text(repaired_text),
                "justification": "The integral is otherwise not defined.",
                "minimality_evidence": "Only measurability is used.",
                "reference_or_counterexample": "none",
            }
        ]
        errors = validate_registry(registry)
        self.assertTrue(any("needs its own review object" in error for error in errors))
        self.assertTrue(any("real reference or counterexample" in error for error in errors))

    def test_reviewed_repair_cannot_be_changed_after_review(self) -> None:
        registry = valid_registry()
        audit = registry["audits"][0]
        repair = reviewed_repair(audit)
        repair["minimality_evidence"] = "Changed after the reviewer approved it."
        audit["repairs"] = [repair]
        audit.pop("_test_repaired_text")
        errors = validate_registry(registry)
        self.assertTrue(any("exact proposal payload" in error for error in errors))
        self.assertTrue(any("canonical reviewer packet" in error for error in errors))

    def test_formalization_artifact_cannot_be_accepted_as_source_repair(self) -> None:
        registry = valid_registry()
        audit = registry["audits"][0]
        repair = reviewed_repair(audit, repair_id="ASTIS-REPAIR-TEST-002")
        repair["necessity"] = "formalization-artifact-risk"
        # Rebind the independent review to the exact modified proposal so this
        # test isolates the necessity-policy rejection rather than hash drift.
        packet = repair_reviewer_packet(audit, repair)
        repair["review"]["proposal_sha256"] = repair_proposal_sha256(repair)
        repair["review"]["reviewer_packet_sha256"] = packet["packet_sha256"]
        audit["repairs"] = [repair]
        audit.pop("_test_repaired_text")
        errors = validate_registry(registry)
        self.assertTrue(any("cannot be accepted as source repair" in error for error in errors))
        self.assertTrue(any("mathematically necessary or source implicit" in error for error in errors))

    def test_reviewer_packet_is_anti_anchored_but_contains_comparison_inputs(self) -> None:
        audit = copy.deepcopy(valid_registry()["audits"][0])
        packet = semantic_reviewer_packet(audit)
        encoded = json.dumps(packet, ensure_ascii=False)
        self.assertIn(audit["source"]["original_text"], encoded)
        self.assertIn(audit["reconstruction"]["text"], encoded)
        self.assertNotIn('"verdict": "exact"', encoded)
        self.assertNotIn("slot-by-slot comparison checked", encoded)
        self.assertTrue(packet["anti_anchoring"]["prior_repairs_included"] is False)
        self.assertEqual(set(packet["output_contract"]["semantic_slots"]), set(SEMANTIC_SLOTS))
        self.assertEqual(len(packet["packet_sha256"]), 64)

    def test_repair_reviewer_packet_is_anti_anchored_and_exactly_bound(self) -> None:
        audit = copy.deepcopy(valid_registry()["audits"][0])
        repair = reviewed_repair(audit)
        packet = repair_reviewer_packet(audit, repair)
        encoded = json.dumps(packet, ensure_ascii=False)
        self.assertIn(audit["source"]["original_text"], encoded)
        self.assertIn(repair["proposed_change"], encoded)
        self.assertNotIn('"verdict": "exact"', encoded)
        self.assertNotIn("slot-by-slot comparison checked", encoded)
        self.assertFalse(packet["anti_anchoring"]["prior_source_review_included"])
        self.assertEqual(packet["proposal"]["proposal_sha256"], repair_proposal_sha256(repair))
        self.assertEqual(len(packet["packet_sha256"]), 64)


if __name__ == "__main__":
    unittest.main()
