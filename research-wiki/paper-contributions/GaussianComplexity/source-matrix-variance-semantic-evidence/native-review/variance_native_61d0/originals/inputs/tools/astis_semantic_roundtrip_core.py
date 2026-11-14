#!/usr/bin/env python3
"""ASTIS semantic round-trip and theorem-repair evidence gate.

The gate separates four claims that are easy to conflate:

1. Lean compiled the proposition written in a declaration.
2. A source-blind decoder reconstructed a natural-language theorem from that
   Lean statement.
3. An independent reviewer compared the original and reconstruction across a
   fixed semantic contract.
4. A proposed theorem repair is mathematically justified and independently
   source-reviewed, rather than merely convenient for one formalization route.

No model is trusted merely because it generated fluent source or Lean text.
The durable object is a structured, hash-pinned audit whose blindness, packet
provenance, review independence, and repair decisions are machine-checkable
while the mathematical verdict itself stays reviewer-owned.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = ROOT / "research-wiki" / "semantic-roundtrip" / "registry.json"

SEMANTIC_SLOTS = (
    "objects",
    "domains",
    "quantifiers",
    "assumptions",
    "conclusion",
    "scopes",
    "constant_dependencies",
)
SLOT_RELATIONS = {
    "same",
    "equivalent",
    "explicit-elaboration",
    "stronger-in-lean",
    "weaker-in-lean",
    "missing-from-lean",
    "missing-from-source",
    "different",
    "not-audited",
}
VERDICTS = {
    "pending",
    "exact",
    "equivalent-after-elaboration",
    "implicit-assumption-exposed",
    "lean-strengthened-assumptions",
    "lean-weakened-conclusion",
    "domain-mismatch",
    "quantifier-mismatch",
    "source-underspecified",
    "possible-source-error",
}
AUDIT_STATES = {
    "draft",
    "blind-reconstructed",
    "semantic-diffed",
    "source-reviewed",
    "accepted",
    "rejected",
}
REVIEW_STATES = {"pending", "accepted", "needs-revision", "rejected"}
REPAIR_CLASSES = {
    "micro-correction",
    "assumption-addition",
    "domain-clarification",
    "quantifier-clarification",
    "notation-resolution",
    "conclusion-correction",
}
REPAIR_STATUSES = {"proposed", "source-reviewed", "accepted", "rejected"}
REPAIR_NECESSITIES = {
    "mathematically-necessary",
    "source-implicit",
    "formalization-artifact-risk",
    "uncertain",
}
DECODER_INPUT_ARTIFACTS = (
    "lean-statement",
    "approved-definition-context",
)
REPAIR_PAYLOAD_FIELDS = (
    "id",
    "class",
    "necessity",
    "proposed_change",
    "reconstructed_statement",
    "statement_sha256",
    "justification",
    "minimality_evidence",
    "reference_or_counterexample",
)
HEX64 = re.compile(r"^[0-9a-f]{64}$")
PLACEHOLDER_REFERENCES = {"", "none", "n/a", "na", "unknown", "pending", "tbd"}


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_json(value: object) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return sha256_text(payload)


def load_registry(path: Path = DEFAULT_REGISTRY) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"registry must be a JSON object: {path}")
    return value


def _nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _hash(value: object) -> bool:
    return isinstance(value, str) and bool(HEX64.fullmatch(value))


def _at(audit_id: str, message: str) -> str:
    return f"{audit_id}: {message}"


def _meaningful_reference(value: object) -> bool:
    return isinstance(value, str) and value.strip().lower() not in PLACEHOLDER_REFERENCES


def _normalized(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip().casefold()


def _decoder_context_violations(audit: dict[str, Any]) -> list[str]:
    """Detect exact identity/source leakage through approved definition context.

    Semantic paraphrase leakage cannot be decided mechanically, but the packet
    generator can and should reject every exact secret already known to the
    registry. Context entries are deliberately restricted to non-empty strings
    so arbitrary structured metadata cannot become an unscanned side channel.
    """

    source = audit.get("source", {}) if isinstance(audit.get("source"), dict) else {}
    lean = audit.get("lean", {}) if isinstance(audit.get("lean"), dict) else {}
    context = lean.get("decoder_context", [])
    if not isinstance(context, list):
        return ["lean.decoder_context must be a list"]

    secrets: list[tuple[str, object]] = [
        ("audit id", audit.get("id")),
        ("graph/source node", audit.get("graph_node")),
        ("source id", source.get("source_id")),
        ("source anchor", source.get("anchor")),
        ("original theorem", source.get("original_text")),
        ("source theorem hash", source.get("text_sha256")),
        ("Lean declaration identity", lean.get("declaration")),
        ("Lean file identity", lean.get("file")),
    ]
    for repair in audit.get("repairs", []) if isinstance(audit.get("repairs"), list) else []:
        if not isinstance(repair, dict):
            continue
        for field in ("id", "proposed_change", "reconstructed_statement", "justification"):
            secrets.append((f"repair {field}", repair.get(field)))

    normalized_secrets = [
        (label, token)
        for label, raw in secrets
        if (token := _normalized(raw))
    ]
    violations: list[str] = []
    for index, item in enumerate(context):
        if not _nonempty(item):
            violations.append(f"lean.decoder_context[{index}] must be a non-empty string")
            continue
        text = _normalized(item)
        for label, token in normalized_secrets:
            leaked = text == token if len(token) < 6 else token in text
            if leaked:
                violations.append(f"lean.decoder_context[{index}] leaks {label}")
    return violations


def _repair_payload(repair: dict[str, Any]) -> dict[str, Any]:
    return {field: repair.get(field, "") for field in REPAIR_PAYLOAD_FIELDS}


def repair_proposal_sha256(repair: dict[str, Any]) -> str:
    """Hash every source-facing field a repair reviewer is asked to approve."""

    return sha256_json(_repair_payload(repair))


def decoder_packet(audit: dict[str, Any]) -> dict[str, Any]:
    """Create a source-blind reconstruction packet from one audit record.

    The packet deliberately omits the audit id, source id, source anchor,
    original theorem, source hash, Lean declaration name, Lean file path,
    semantic verdict, prior audit, and repair proposals. Even an audit id or
    declaration name can leak a theorem number, so the public identifier is an
    opaque prefix of the Lean statement hash.
    """

    lean = audit.get("lean", {}) if isinstance(audit.get("lean"), dict) else {}
    approved = list(lean.get("decoder_context", [])) if isinstance(lean.get("decoder_context"), list) else []
    statement_hash = str(lean.get("statement_sha256", ""))
    artifacts = ["lean-statement"]
    if approved:
        artifacts.append("approved-definition-context")
    core = {
        "schema_version": 1,
        "task": "blind-theorem-reconstruction",
        "packet_id": "ASTIS-BLIND-" + (statement_hash[:16] or "unhashed-target"),
        "non_disclosure": {
            "source_text_included": False,
            "source_anchor_included": False,
            "source_identity_included": False,
            "audit_identity_included": False,
            "lean_declaration_identity_included": False,
            "forbidden_inputs": [
                "original theorem text",
                "source title, theorem number, or anchor",
                "audit id or source-facing Lean declaration name",
                "source semantic audit or fidelity verdict",
                "repair proposal",
            ],
        },
        "input_artifacts": artifacts,
        "lean": {
            "statement": lean.get("statement", ""),
            "statement_sha256": statement_hash,
            "compiled": lean.get("compiled", False),
            "approved_definition_context": approved,
        },
        "output_contract": {
            "reconstructed_theorem_text": "",
            "reconstructed_text_sha256": "",
            "objects": "",
            "domains": "",
            "quantifiers": "",
            "assumptions": "",
            "conclusion": "",
            "scopes": "",
            "constant_dependencies": "",
            "decoder": "",
            "decoder_run_sha256": "",
            "source_text_visible": False,
        },
    }
    return {**core, "packet_sha256": sha256_json(core)}


def _bind_publication_context(core: dict[str, Any], audit: dict[str, Any]) -> None:
    """New publication evidence is part of the actual independent review input.

    Legacy audits keep identical packet hashes. Never call this from the blind
    decoder exporter: this context contains source-facing candidate exposition.
    """
    if audit.get('publication_binding_sha256') or audit.get('publication_context'):
        core['publication_binding_sha256'] = audit.get('publication_binding_sha256', '')
        core['candidate_publication_context'] = audit.get('publication_context', {})
        core['publication_review_rule'] = (
            'Independently compare the current Lean module, its scoped assumptions, '
            'source statement and candidate natural-language formula proof. '
            'These are claims to check, not previous reviewer verdicts. '
            'Do not infer equivalence from a hash or compilation alone.'
        )


def semantic_reviewer_packet(audit: dict[str, Any]) -> dict[str, Any]:
    """Create an independent source-review packet after blind reconstruction.

    This packet intentionally includes the source contract because the reviewer
    must compare it with the reconstruction. It intentionally omits any existing
    semantic slots, deltas, verdict, reviewer decision, or repair proposal so the
    reviewer is not anchored by a previous model's conclusions.
    """

    source = audit.get("source", {}) if isinstance(audit.get("source"), dict) else {}
    lean = audit.get("lean", {}) if isinstance(audit.get("lean"), dict) else {}
    reconstruction = audit.get("reconstruction", {}) if isinstance(audit.get("reconstruction"), dict) else {}
    identity_material = {
        "source_text_sha256": source.get("text_sha256", ""),
        "lean_statement_sha256": lean.get("statement_sha256", ""),
        "reconstructed_text_sha256": reconstruction.get("text_sha256", ""),
    }
    core = {
        "schema_version": 1,
        "task": "independent-semantic-source-review",
        "packet_id": "ASTIS-REVIEW-" + sha256_json(identity_material)[:16],
        "anti_anchoring": {
            "prior_semantic_slots_included": False,
            "prior_deltas_included": False,
            "prior_verdict_included": False,
            "prior_repairs_included": False,
        },
        "roles": {
            "formalizer": lean.get("formalizer", ""),
            "blind_decoder": reconstruction.get("decoder", ""),
            "reviewer_must_differ_from_both": True,
        },
        "source": {
            "source_id": source.get("source_id", ""),
            "anchor": source.get("anchor", ""),
            "original_text": source.get("original_text", ""),
            "text_sha256": source.get("text_sha256", ""),
        },
        "lean": {
            "declaration": lean.get("declaration", ""),
            "file": lean.get("file", ""),
            "statement": lean.get("statement", ""),
            "statement_sha256": lean.get("statement_sha256", ""),
            "compiled": lean.get("compiled", False),
        },
        "blind_reconstruction": {
            "text": reconstruction.get("text", ""),
            "text_sha256": reconstruction.get("text_sha256", ""),
            "decoder": reconstruction.get("decoder", ""),
            "decoder_packet_sha256": reconstruction.get("decoder_packet_sha256", ""),
            "decoder_run_sha256": reconstruction.get("decoder_run_sha256", ""),
            "source_text_visible": reconstruction.get("source_text_visible"),
        },
        "review_contract": {
            "semantic_slots": list(SEMANTIC_SLOTS),
            "slot_relations": sorted(SLOT_RELATIONS),
            "verdicts": sorted(VERDICTS - {"pending"}),
            "repair_classes": sorted(REPAIR_CLASSES),
            "repair_necessities": sorted(REPAIR_NECESSITIES),
            "rule": "Text similarity is not semantic equivalence. Repair proposals remain separate from the pinned source theorem.",
        },
        "output_contract": {
            "semantic_slots": {
                slot: {
                    "original": "",
                    "reconstructed": "",
                    "relation": "not-audited",
                    "evidence": "",
                }
                for slot in SEMANTIC_SLOTS
            },
            "deltas": [],
            "verdict": "",
            "repairs": [],
            "reviewer": "",
            "independent_from_formalizer": True,
            "independent_from_decoder": True,
            "review_evidence": "",
            "review_run_sha256": "",
            "reviewer_packet_sha256": "",
        },
    }
    _bind_publication_context(core, audit)
    return {**core, "packet_sha256": sha256_json(core)}


def repair_reviewer_packet(audit: dict[str, Any], repair: dict[str, Any]) -> dict[str, Any]:
    """Create a fresh packet for deciding whether a repair is source-correct.

    The reviewer necessarily sees the proposal being judged, but not any prior
    fidelity verdict, semantic delta classification, source-review decision, or
    earlier repair-review decision. The decision is bound to the complete repair
    payload by `proposal_sha256`.
    """

    source = audit.get("source", {}) if isinstance(audit.get("source"), dict) else {}
    lean = audit.get("lean", {}) if isinstance(audit.get("lean"), dict) else {}
    reconstruction = audit.get("reconstruction", {}) if isinstance(audit.get("reconstruction"), dict) else {}
    payload = _repair_payload(repair)
    proposal_hash = repair_proposal_sha256(repair)
    identity_material = {
        "source_text_sha256": source.get("text_sha256", ""),
        "lean_statement_sha256": lean.get("statement_sha256", ""),
        "reconstructed_text_sha256": reconstruction.get("text_sha256", ""),
        "proposal_sha256": proposal_hash,
    }
    core = {
        "schema_version": 1,
        "task": "independent-theorem-repair-review",
        "packet_id": "ASTIS-REPAIR-REVIEW-" + sha256_json(identity_material)[:16],
        "anti_anchoring": {
            "prior_fidelity_verdict_included": False,
            "prior_semantic_deltas_included": False,
            "prior_source_review_included": False,
            "prior_repair_review_included": False,
        },
        "roles": {
            "formalizer": lean.get("formalizer", ""),
            "blind_decoder": reconstruction.get("decoder", ""),
            "reviewer_must_differ_from_both": True,
        },
        "source": {
            "source_id": source.get("source_id", ""),
            "anchor": source.get("anchor", ""),
            "original_text": source.get("original_text", ""),
            "text_sha256": source.get("text_sha256", ""),
        },
        "lean": {
            "statement": lean.get("statement", ""),
            "statement_sha256": lean.get("statement_sha256", ""),
            "compiled": lean.get("compiled", False),
        },
        "blind_reconstruction": {
            "text": reconstruction.get("text", ""),
            "text_sha256": reconstruction.get("text_sha256", ""),
            "decoder": reconstruction.get("decoder", ""),
            "decoder_packet_sha256": reconstruction.get("decoder_packet_sha256", ""),
            "decoder_run_sha256": reconstruction.get("decoder_run_sha256", ""),
        },
        "proposal": {**payload, "proposal_sha256": proposal_hash},
        "review_contract": {
            "rule": "Decide whether this exact minimal change is source-correct, not merely helpful to the current Lean proof route.",
            "allowed_states": ["accepted", "needs-revision", "rejected"],
        },
        "output_contract": {
            "state": "",
            "reviewer": "",
            "independent_from_formalizer": True,
            "independent_from_decoder": True,
            "evidence": "",
            "review_run_sha256": "",
            "reviewer_packet_sha256": "",
            "proposal_sha256": proposal_hash,
        },
    }
    _bind_publication_context(core, audit)
    return {**core, "packet_sha256": sha256_json(core)}


def validate_registry(registry: dict[str, Any]) -> list[str]:
    """Return every contract violation without stopping at the first one."""

    errors: list[str] = []
    if registry.get("schema_version") != 1:
        errors.append("schema_version must be 1")

    protocol = registry.get("protocol")
    if not isinstance(protocol, dict):
        errors.append("protocol must be an object")
        protocol = {}
    if protocol.get("decoder_blindness") != "required":
        errors.append("protocol.decoder_blindness must be 'required'")
    if protocol.get("decoder_context_content_scan") != "required":
        errors.append("protocol.decoder_context_content_scan must be 'required'")
    if protocol.get("independent_source_review") != "required":
        errors.append("protocol.independent_source_review must be 'required'")
    if protocol.get("source_review_packet_binding") != "required":
        errors.append("protocol.source_review_packet_binding must be 'required'")
    if protocol.get("independent_repair_review") != "required":
        errors.append("protocol.independent_repair_review must be 'required'")
    if protocol.get("repair_review_packet_binding") != "required":
        errors.append("protocol.repair_review_packet_binding must be 'required'")
    slots = protocol.get("semantic_slots")
    if not isinstance(slots, list) or set(slots) != set(SEMANTIC_SLOTS):
        errors.append("protocol.semantic_slots must contain the seven canonical slots exactly once")
    elif len(slots) != len(SEMANTIC_SLOTS):
        errors.append("protocol.semantic_slots contains duplicates")
    allowed_inputs = protocol.get("decoder_allowed_inputs")
    if not isinstance(allowed_inputs, list) or tuple(allowed_inputs) != DECODER_INPUT_ARTIFACTS:
        errors.append("protocol.decoder_allowed_inputs must equal the canonical source-blind input list")

    audits = registry.get("audits")
    if not isinstance(audits, list):
        errors.append("audits must be a list")
        return errors

    seen_audits: set[str] = set()
    seen_repairs: set[str] = set()
    for index, audit in enumerate(audits):
        if not isinstance(audit, dict):
            errors.append(f"audits[{index}] must be an object")
            continue
        audit_id = str(audit.get("id") or f"audits[{index}]")
        if not _nonempty(audit.get("id")):
            errors.append(_at(audit_id, "id is required"))
        elif audit_id in seen_audits:
            errors.append(_at(audit_id, "duplicate audit id"))
        seen_audits.add(audit_id)

        state = audit.get("state")
        if state not in AUDIT_STATES:
            errors.append(_at(audit_id, f"state must be one of {sorted(AUDIT_STATES)}"))
            state = "draft"

        source = audit.get("source")
        if not isinstance(source, dict):
            errors.append(_at(audit_id, "source must be an object"))
            source = {}
        for field in ("source_id", "anchor", "original_text"):
            if not _nonempty(source.get(field)):
                errors.append(_at(audit_id, f"source.{field} is required"))
        if not _hash(source.get("text_sha256")):
            errors.append(_at(audit_id, "source.text_sha256 must be a lowercase SHA-256"))
        elif _nonempty(source.get("original_text")) and source["text_sha256"] != sha256_text(source["original_text"]):
            errors.append(_at(audit_id, "source.text_sha256 does not match source.original_text"))

        lean = audit.get("lean")
        if not isinstance(lean, dict):
            errors.append(_at(audit_id, "lean must be an object"))
            lean = {}
        for field in ("declaration", "file", "statement", "formalizer"):
            if not _nonempty(lean.get(field)):
                errors.append(_at(audit_id, f"lean.{field} is required"))
        if not isinstance(lean.get("compiled"), bool):
            errors.append(_at(audit_id, "lean.compiled must be a boolean"))
        if not _hash(lean.get("statement_sha256")):
            errors.append(_at(audit_id, "lean.statement_sha256 must be a lowercase SHA-256"))
        elif _nonempty(lean.get("statement")) and lean["statement_sha256"] != sha256_text(lean["statement"]):
            errors.append(_at(audit_id, "lean.statement_sha256 does not match lean.statement"))
        context = lean.get("decoder_context", [])
        if not isinstance(context, list):
            errors.append(_at(audit_id, "lean.decoder_context must be a list"))
        else:
            for violation in _decoder_context_violations(audit):
                errors.append(_at(audit_id, violation))

        reconstruction = audit.get("reconstruction")
        if state != "draft" and not isinstance(reconstruction, dict):
            errors.append(_at(audit_id, "reconstruction is required after draft state"))
            reconstruction = {}
        elif not isinstance(reconstruction, dict):
            reconstruction = {}
        if reconstruction:
            for field in ("text", "decoder"):
                if not _nonempty(reconstruction.get(field)):
                    errors.append(_at(audit_id, f"reconstruction.{field} is required"))
            if not _hash(reconstruction.get("text_sha256")):
                errors.append(_at(audit_id, "reconstruction.text_sha256 must be a lowercase SHA-256"))
            elif _nonempty(reconstruction.get("text")) and reconstruction["text_sha256"] != sha256_text(reconstruction["text"]):
                errors.append(_at(audit_id, "reconstruction.text_sha256 does not match reconstruction.text"))
            if not _hash(reconstruction.get("decoder_run_sha256")):
                errors.append(_at(audit_id, "reconstruction.decoder_run_sha256 must pin the decoder run"))
            if reconstruction.get("source_text_visible") is not False:
                errors.append(_at(audit_id, "blind decoder must record source_text_visible=false"))
            if reconstruction.get("lean_statement_sha256") != lean.get("statement_sha256"):
                errors.append(_at(audit_id, "reconstruction must pin the audited Lean statement hash"))
            expected_packet = decoder_packet(audit)
            if reconstruction.get("decoder_packet_sha256") != expected_packet.get("packet_sha256"):
                errors.append(_at(audit_id, "reconstruction.decoder_packet_sha256 does not match the canonical blind packet"))
            artifacts = reconstruction.get("input_artifacts")
            if artifacts != expected_packet.get("input_artifacts"):
                errors.append(_at(audit_id, "reconstruction.input_artifacts must exactly match the canonical blind packet"))
            if reconstruction.get("decoder") == lean.get("formalizer"):
                errors.append(_at(audit_id, "blind decoder must be independent from the formalizer"))

        semantic_slots = audit.get("semantic_slots")
        if state in {"semantic-diffed", "source-reviewed", "accepted", "rejected"}:
            if not isinstance(semantic_slots, dict):
                errors.append(_at(audit_id, "semantic_slots are required after reconstruction"))
                semantic_slots = {}
            missing = [slot for slot in SEMANTIC_SLOTS if slot not in semantic_slots]
            extra = sorted(set(semantic_slots) - set(SEMANTIC_SLOTS))
            if missing:
                errors.append(_at(audit_id, "semantic_slots missing: " + ", ".join(missing)))
            if extra:
                errors.append(_at(audit_id, "semantic_slots contain unknown keys: " + ", ".join(extra)))
            for slot in SEMANTIC_SLOTS:
                row = semantic_slots.get(slot)
                if not isinstance(row, dict):
                    errors.append(_at(audit_id, f"semantic_slots.{slot} must be an object"))
                    continue
                if row.get("relation") not in SLOT_RELATIONS:
                    errors.append(_at(audit_id, f"semantic_slots.{slot}.relation is invalid"))
                for field in ("original", "reconstructed", "evidence"):
                    if not _nonempty(row.get(field)):
                        errors.append(_at(audit_id, f"semantic_slots.{slot}.{field} is required"))
        elif semantic_slots not in (None, {}) and not isinstance(semantic_slots, dict):
            errors.append(_at(audit_id, "semantic_slots must be an object"))

        deltas = audit.get("deltas", [])
        if not isinstance(deltas, list):
            errors.append(_at(audit_id, "deltas must be a list"))
            deltas = []
        blocking = 0
        for delta_index, delta in enumerate(deltas):
            if not isinstance(delta, dict):
                errors.append(_at(audit_id, f"deltas[{delta_index}] must be an object"))
                continue
            if delta.get("slot") not in SEMANTIC_SLOTS:
                errors.append(_at(audit_id, f"deltas[{delta_index}].slot is invalid"))
            if delta.get("severity") not in {"informational", "review", "blocking"}:
                errors.append(_at(audit_id, f"deltas[{delta_index}].severity is invalid"))
            if delta.get("severity") == "blocking":
                blocking += 1
            if not _nonempty(delta.get("description")) or not _nonempty(delta.get("evidence")):
                errors.append(_at(audit_id, f"deltas[{delta_index}] needs description and evidence"))

        verdict = audit.get("verdict", "pending")
        if verdict not in VERDICTS:
            errors.append(_at(audit_id, f"verdict must be one of {sorted(VERDICTS)}"))
        if state in {"source-reviewed", "accepted", "rejected"} and verdict == "pending":
            errors.append(_at(audit_id, f"state={state} requires a non-pending fidelity verdict"))
        if verdict in {"exact", "equivalent-after-elaboration"} and blocking:
            errors.append(_at(audit_id, f"{verdict} cannot coexist with blocking semantic deltas"))
        if verdict == "exact" and isinstance(semantic_slots, dict):
            bad = [
                slot
                for slot, row in semantic_slots.items()
                if isinstance(row, dict) and row.get("relation") not in {"same", "equivalent"}
            ]
            if bad:
                errors.append(_at(audit_id, "exact verdict has non-equivalent slots: " + ", ".join(bad)))
        if verdict == "equivalent-after-elaboration" and isinstance(semantic_slots, dict):
            allowed = {"same", "equivalent", "explicit-elaboration"}
            bad = [slot for slot, row in semantic_slots.items() if isinstance(row, dict) and row.get("relation") not in allowed]
            if bad:
                errors.append(_at(audit_id, "equivalent-after-elaboration has non-equivalent slots: " + ", ".join(bad)))

        review = audit.get("source_review")
        if not isinstance(review, dict):
            errors.append(_at(audit_id, "source_review must be an object"))
            review = {}
        review_state = review.get("state")
        if review_state not in REVIEW_STATES:
            errors.append(_at(audit_id, f"source_review.state must be one of {sorted(REVIEW_STATES)}"))
        if review_state != "pending":
            reviewer = review.get("reviewer")
            if not _nonempty(reviewer):
                errors.append(_at(audit_id, "reviewed audit needs source_review.reviewer"))
            if review.get("independent_from_formalizer") is not True:
                errors.append(_at(audit_id, "source reviewer must be independent from the formalizer"))
            if review.get("independent_from_decoder") is not True:
                errors.append(_at(audit_id, "source reviewer must be independent from the blind decoder"))
            if reviewer in {lean.get("formalizer"), reconstruction.get("decoder")}:
                errors.append(_at(audit_id, "source reviewer identity must differ from formalizer and decoder"))
            if not _nonempty(review.get("evidence")):
                errors.append(_at(audit_id, "reviewed audit needs source_review.evidence"))
            if not _hash(review.get("review_run_sha256")):
                errors.append(_at(audit_id, "reviewed audit needs source_review.review_run_sha256"))
            expected_review_packet = semantic_reviewer_packet(audit).get("packet_sha256")
            if review.get("reviewer_packet_sha256") != expected_review_packet:
                errors.append(_at(audit_id, "source_review.reviewer_packet_sha256 does not match the canonical reviewer packet"))
        if state in {"source-reviewed", "accepted"} and review_state != "accepted":
            errors.append(_at(audit_id, f"state={state} requires an accepted independent source review"))
        if state == "rejected" and review_state not in {"rejected", "needs-revision"}:
            errors.append(_at(audit_id, "state=rejected requires a rejected or needs-revision source review"))

        repairs = audit.get("repairs", [])
        if not isinstance(repairs, list):
            errors.append(_at(audit_id, "repairs must be a list"))
            repairs = []
        for repair_index, repair in enumerate(repairs):
            if not isinstance(repair, dict):
                errors.append(_at(audit_id, f"repairs[{repair_index}] must be an object"))
                continue
            repair_id = str(repair.get("id") or f"repairs[{repair_index}]")
            if not _nonempty(repair.get("id")):
                errors.append(_at(audit_id, f"{repair_id}: id is required"))
            elif repair_id in seen_repairs:
                errors.append(_at(audit_id, f"duplicate repair id {repair_id}"))
            seen_repairs.add(repair_id)
            if repair.get("class") not in REPAIR_CLASSES:
                errors.append(_at(audit_id, f"{repair_id}: repair class is invalid"))
            repair_status = repair.get("status")
            if repair_status not in REPAIR_STATUSES:
                errors.append(_at(audit_id, f"{repair_id}: repair status is invalid"))
            necessity = repair.get("necessity")
            if necessity not in REPAIR_NECESSITIES:
                errors.append(_at(audit_id, f"{repair_id}: repair necessity is invalid"))
            for field in ("proposed_change", "reconstructed_statement", "justification", "minimality_evidence"):
                if not _nonempty(repair.get(field)):
                    errors.append(_at(audit_id, f"{repair_id}: {field} is required"))
            if not _hash(repair.get("statement_sha256")):
                errors.append(_at(audit_id, f"{repair_id}: statement_sha256 must pin the repaired statement"))
            elif _nonempty(repair.get("reconstructed_statement")) and repair["statement_sha256"] != sha256_text(repair["reconstructed_statement"]):
                errors.append(_at(audit_id, f"{repair_id}: statement_sha256 does not match reconstructed_statement"))

            repair_review = repair.get("review")
            if repair_status in {"source-reviewed", "accepted", "rejected"}:
                if not isinstance(repair_review, dict):
                    errors.append(_at(audit_id, f"{repair_id}: reviewed/rejected repair needs its own review object"))
                    repair_review = {}
                expected_state = {"accepted"} if repair_status in {"source-reviewed", "accepted"} else {"rejected", "needs-revision"}
                if repair_review.get("state") not in expected_state:
                    errors.append(_at(audit_id, f"{repair_id}: repair review state does not match repair status"))
                repair_reviewer = repair_review.get("reviewer")
                if not _nonempty(repair_reviewer):
                    errors.append(_at(audit_id, f"{repair_id}: repair review needs reviewer"))
                if repair_review.get("independent_from_formalizer") is not True:
                    errors.append(_at(audit_id, f"{repair_id}: repair reviewer must be independent from the formalizer"))
                if repair_review.get("independent_from_decoder") is not True:
                    errors.append(_at(audit_id, f"{repair_id}: repair reviewer must be independent from the blind decoder"))
                if repair_reviewer in {lean.get("formalizer"), reconstruction.get("decoder")}:
                    errors.append(_at(audit_id, f"{repair_id}: repair reviewer identity must differ from formalizer and decoder"))
                if not _nonempty(repair_review.get("evidence")):
                    errors.append(_at(audit_id, f"{repair_id}: repair review needs evidence"))
                if not _hash(repair_review.get("review_run_sha256")):
                    errors.append(_at(audit_id, f"{repair_id}: repair review needs review_run_sha256"))
                expected_proposal_hash = repair_proposal_sha256(repair)
                if repair_review.get("proposal_sha256") != expected_proposal_hash:
                    errors.append(_at(audit_id, f"{repair_id}: repair review is not bound to the exact proposal payload"))
                expected_repair_packet = repair_reviewer_packet(audit, repair).get("packet_sha256")
                if repair_review.get("reviewer_packet_sha256") != expected_repair_packet:
                    errors.append(_at(audit_id, f"{repair_id}: repair review is not bound to the canonical reviewer packet"))

            if repair_status in {"source-reviewed", "accepted"}:
                if necessity == "formalization-artifact-risk":
                    errors.append(_at(audit_id, f"{repair_id}: formalization-artifact-risk cannot be accepted as source repair"))
                if not _meaningful_reference(repair.get("reference_or_counterexample")):
                    errors.append(_at(audit_id, f"{repair_id}: reviewed/accepted repair needs a real reference or counterexample"))
            if repair_status == "accepted":
                if state != "accepted":
                    errors.append(_at(audit_id, f"{repair_id}: accepted repair requires state=accepted"))
                if review_state != "accepted":
                    errors.append(_at(audit_id, f"{repair_id}: accepted repair requires accepted theorem source review"))
                if necessity not in {"mathematically-necessary", "source-implicit"}:
                    errors.append(_at(audit_id, f"{repair_id}: accepted repair must be mathematically necessary or source implicit"))

        if state != "draft" and lean.get("compiled") is not True:
            errors.append(_at(audit_id, "round-trip reconstruction may start only from a compiled Lean target"))

    return errors


def summary(registry: dict[str, Any]) -> dict[str, Any]:
    audits = [audit for audit in registry.get("audits", []) if isinstance(audit, dict)]
    repairs = [repair for audit in audits for repair in audit.get("repairs", []) if isinstance(repair, dict)]
    return {
        "audits": len(audits),
        "states": dict(sorted(Counter(str(audit.get("state", "unknown")) for audit in audits).items())),
        "verdicts": dict(sorted(Counter(str(audit.get("verdict", "pending")) for audit in audits).items())),
        "repairs": len(repairs),
        "repair_statuses": dict(sorted(Counter(str(repair.get("status", "unknown")) for repair in repairs).items())),
    }


def _audit_by_id(registry: dict[str, Any], audit_id: str) -> dict[str, Any]:
    for audit in registry.get("audits", []):
        if isinstance(audit, dict) and audit.get("id") == audit_id:
            return audit
    raise KeyError(f"unknown audit id: {audit_id}")


def _repair_by_id(audit: dict[str, Any], repair_id: str) -> dict[str, Any]:
    for repair in audit.get("repairs", []):
        if isinstance(repair, dict) and repair.get("id") == repair_id:
            return repair
    raise KeyError(f"unknown repair id: {repair_id}")


def _write_packet(value: dict[str, Any], output_path: str) -> None:
    output = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    if output_path:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(output, encoding="utf-8", newline="\n")
        print(path)
    else:
        print(output, end="")


def _blind_reconstruction_ready(audit: dict[str, Any]) -> tuple[bool, str]:
    leaks = _decoder_context_violations(audit)
    if leaks:
        return False, "approved decoder context leaks forbidden source/identity information: " + "; ".join(leaks)
    reconstruction = audit.get("reconstruction", {}) if isinstance(audit.get("reconstruction"), dict) else {}
    expected = decoder_packet(audit)
    if reconstruction.get("source_text_visible") is not False:
        return False, "source-blind reconstruction is not established"
    if reconstruction.get("decoder_packet_sha256") != expected.get("packet_sha256"):
        return False, "reconstruction does not pin the canonical decoder packet"
    if not _nonempty(reconstruction.get("text")) or not _hash(reconstruction.get("text_sha256")):
        return False, "reconstruction text and hash are incomplete"
    return True, ""


def command_check(args: argparse.Namespace) -> int:
    registry = load_registry(Path(args.registry))
    errors = validate_registry(registry)
    if errors:
        print("ASTIS semantic round-trip gate failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    result = summary(registry)
    print(
        "semantic round-trip registry valid: "
        f"{result['audits']} audits, {result['repairs']} repair proposals"
    )
    return 0


def command_summary(args: argparse.Namespace) -> int:
    registry = load_registry(Path(args.registry))
    errors = validate_registry(registry)
    if errors and not args.allow_invalid:
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(json.dumps(summary(registry), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


def command_decoder_packet(args: argparse.Namespace) -> int:
    registry = load_registry(Path(args.registry))
    audit = _audit_by_id(registry, args.audit_id)
    lean = audit.get("lean", {}) if isinstance(audit.get("lean"), dict) else {}
    if lean.get("compiled") is not True:
        print("decoder packet refused: Lean target is not marked compiled", file=sys.stderr)
        return 1
    if not _nonempty(lean.get("statement")) or not _hash(lean.get("statement_sha256")):
        print("decoder packet refused: Lean statement and hash are incomplete", file=sys.stderr)
        return 1
    leaks = _decoder_context_violations(audit)
    if leaks:
        print("decoder packet refused: " + "; ".join(leaks), file=sys.stderr)
        return 1
    _write_packet(decoder_packet(audit), args.output)
    return 0


def command_reviewer_packet(args: argparse.Namespace) -> int:
    registry = load_registry(Path(args.registry))
    audit = _audit_by_id(registry, args.audit_id)
    ready, reason = _blind_reconstruction_ready(audit)
    if not ready:
        print("reviewer packet refused: " + reason, file=sys.stderr)
        return 1
    _write_packet(semantic_reviewer_packet(audit), args.output)
    return 0


def command_repair_reviewer_packet(args: argparse.Namespace) -> int:
    registry = load_registry(Path(args.registry))
    audit = _audit_by_id(registry, args.audit_id)
    repair = _repair_by_id(audit, args.repair_id)
    ready, reason = _blind_reconstruction_ready(audit)
    if not ready:
        print("repair reviewer packet refused: " + reason, file=sys.stderr)
        return 1
    if not _nonempty(repair.get("reconstructed_statement")) or not _hash(repair.get("statement_sha256")):
        print("repair reviewer packet refused: repair statement and hash are incomplete", file=sys.stderr)
        return 1
    _write_packet(repair_reviewer_packet(audit, repair), args.output)
    return 0


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    root.add_argument("--registry", default=str(DEFAULT_REGISTRY), help="semantic round-trip registry JSON")
    commands = root.add_subparsers(dest="command", required=True)

    check = commands.add_parser("check", help="fail on blindness, schema, review, or repair-policy violations")
    check.set_defaults(func=command_check)

    show = commands.add_parser("summary", help="print audit/verdict/repair counts")
    show.add_argument("--allow-invalid", action="store_true", help="summarize even when validation fails")
    show.set_defaults(func=command_summary)

    packet = commands.add_parser("decoder-packet", help="export an anonymous source-blind Lean-to-text packet")
    packet.add_argument("--audit-id", required=True)
    packet.add_argument("--output", default="")
    packet.set_defaults(func=command_decoder_packet)

    review = commands.add_parser("reviewer-packet", help="export an anti-anchored source/reconstruction review packet")
    review.add_argument("--audit-id", required=True)
    review.add_argument("--output", default="")
    review.set_defaults(func=command_reviewer_packet)

    repair_review = commands.add_parser("repair-reviewer-packet", help="export an independent exact-proposal theorem-repair review packet")
    repair_review.add_argument("--audit-id", required=True)
    repair_review.add_argument("--repair-id", required=True)
    repair_review.add_argument("--output", default="")
    repair_review.set_defaults(func=command_repair_reviewer_packet)
    return root


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        return int(args.func(args))
    except (KeyError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"semantic round-trip command failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
