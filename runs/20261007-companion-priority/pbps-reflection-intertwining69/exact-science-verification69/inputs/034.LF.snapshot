#!/usr/bin/env python3
"""Public ASTIS semantic-roundtrip API with conflict-free audit fragments.

The historical implementation lives in `astis_semantic_roundtrip_core.py`.
This compatibility surface keeps every existing import/CLI stable while allowing
new collaborators to store one audit per file under
`research-wiki/semantic-roundtrip/audits/` instead of rewriting the multi-MB
canonical registry.  The merged registry is still validated by the same core
contract, including duplicate-id rejection, blindness, packet hashes and review
independence.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

try:  # package import in unit tests
    from . import astis_semantic_roundtrip_core as _core
    from .astis_semantic_roundtrip_core import *  # noqa: F401,F403
except ImportError:  # direct script / tools-on-sys.path import
    import astis_semantic_roundtrip_core as _core
    from astis_semantic_roundtrip_core import *  # type: ignore # noqa: F401,F403

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_AUDIT_FRAGMENT_DIR = ROOT / "research-wiki" / "semantic-roundtrip" / "audits"
_core_load_registry = _core.load_registry


def _json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _artifact_backed_audit(fragment: dict[str, Any], fragment_path: Path) -> dict[str, Any]:
    required = ("id", "reviewer_packet", "decoder_packet", "decoder_result", "review_result")
    missing = [key for key in required if not fragment.get(key)]
    if missing:
        raise ValueError(f"{fragment_path}: artifact-backed audit missing {missing}")

    reviewer_path = ROOT / str(fragment["reviewer_packet"])
    decoder_packet_path = ROOT / str(fragment["decoder_packet"])
    decoder_result_path = ROOT / str(fragment["decoder_result"])
    review_result_path = ROOT / str(fragment["review_result"])
    for path in (reviewer_path, decoder_packet_path, decoder_result_path, review_result_path):
        if not path.is_file():
            raise ValueError(f"{fragment_path}: audit artifact missing: {path.relative_to(ROOT)}")

    reviewer_packet = _json(reviewer_path)
    decoder_packet_value = _json(decoder_packet_path)
    decoder_result = _json(decoder_result_path)
    review_result = _json(review_result_path)

    publication_context = reviewer_packet.get("candidate_publication_context", {})
    source = dict(reviewer_packet.get("source", {}))
    publication_source = publication_context.get("source", {}) if isinstance(publication_context, dict) else {}
    if isinstance(publication_source, dict) and publication_source.get("url"):
        source["url"] = publication_source["url"]

    lean = dict(reviewer_packet.get("lean", {}))
    roles = reviewer_packet.get("roles", {}) if isinstance(reviewer_packet.get("roles"), dict) else {}
    lean["formalizer"] = roles.get("formalizer", "")
    decoder_lean = decoder_packet_value.get("lean", {}) if isinstance(decoder_packet_value.get("lean"), dict) else {}
    lean["decoder_context"] = list(decoder_lean.get("approved_definition_context", []))

    reconstruction = {
        "text": decoder_result.get("reconstructed_theorem_text", ""),
        "text_sha256": decoder_result.get("reconstructed_text_sha256", ""),
        "decoder": decoder_result.get("decoder", ""),
        "decoder_run_sha256": decoder_result.get("decoder_run_sha256", ""),
        "decoder_packet_sha256": decoder_result.get("packet_sha256", ""),
        "source_text_visible": decoder_result.get("source_text_visible"),
        "lean_statement_sha256": lean.get("statement_sha256", ""),
        "input_artifacts": decoder_result.get("input_artifacts", []),
        "run_artifact": str(fragment["decoder_result"]),
    }

    delta_slots = fragment.get("delta_slots", {}) if isinstance(fragment.get("delta_slots"), dict) else {}
    deltas = []
    for raw in review_result.get("deltas", []):
        if not isinstance(raw, dict):
            continue
        ident = str(raw.get("id", ""))
        slot = delta_slots.get(ident)
        if slot not in _core.SEMANTIC_SLOTS:
            raise ValueError(f"{fragment_path}: delta {ident!r} needs a canonical semantic slot")
        blocking = bool(raw.get("blocking"))
        classification = str(raw.get("classification", "review"))
        deltas.append({
            "slot": slot,
            "severity": "blocking" if blocking else "informational",
            "description": str(raw.get("description", "")),
            "evidence": f"Independent source review classification: {classification}; {'blocking' if blocking else 'nonblocking'}.",
        })

    source_review = {
        "state": "accepted" if review_result.get("verdict") else "pending",
        "reviewer": review_result.get("reviewer", ""),
        "independent_from_formalizer": review_result.get("independent_from_formalizer"),
        "independent_from_decoder": review_result.get("independent_from_decoder"),
        "reviewer_packet_sha256": review_result.get("reviewer_packet_sha256", ""),
        "evidence": review_result.get("review_evidence", ""),
        "review_run_sha256": review_result.get("review_run_sha256", ""),
        "run_artifact": str(fragment["review_result"]),
    }

    audit = {
        "id": fragment["id"],
        "state": fragment.get("state", "accepted"),
        "source": source,
        "lean": lean,
        "reconstruction": reconstruction,
        "semantic_slots": review_result.get("semantic_slots", {}),
        "deltas": deltas,
        "verdict": review_result.get("verdict", "pending"),
        "source_review": source_review,
        "repairs": review_result.get("repairs", []),
        "publication_binding_sha256": reviewer_packet.get("publication_binding_sha256", ""),
        "publication_context": publication_context,
    }
    if fragment.get("graph_node"):
        audit["graph_node"] = fragment["graph_node"]
    return audit


def _fragment_audits(path: Path) -> list[dict[str, Any]]:
    value = _json(path)
    if isinstance(value, dict) and value.get("kind") == "artifact-backed-audit":
        return [_artifact_backed_audit(value, path)]
    if isinstance(value, dict) and isinstance(value.get("audits"), list):
        rows = value["audits"]
    elif isinstance(value, dict):
        rows = [value]
    elif isinstance(value, list):
        rows = value
    else:
        raise ValueError(f"{path}: semantic audit fragment must be an object or list")
    if any(not isinstance(row, dict) for row in rows):
        raise ValueError(f"{path}: every semantic audit fragment row must be an object")
    return list(rows)


def load_registry(path: Path = DEFAULT_REGISTRY) -> dict[str, Any]:  # type: ignore[name-defined]
    registry = _core_load_registry(Path(path))
    if Path(path).resolve() != Path(DEFAULT_REGISTRY).resolve():  # type: ignore[name-defined]
        return registry
    audits = list(registry.get("audits", []))
    if DEFAULT_AUDIT_FRAGMENT_DIR.exists():
        for fragment in sorted(DEFAULT_AUDIT_FRAGMENT_DIR.glob("*.json")):
            audits.extend(_fragment_audits(fragment))
    return {**registry, "audits": audits}


# Core functions (including CLI command handlers) resolve this global at run time.
# Patch it once so direct CLI use and imported use see the exact same merged data.
_core.load_registry = load_registry


if __name__ == "__main__":
    raise SystemExit(_core.main())
