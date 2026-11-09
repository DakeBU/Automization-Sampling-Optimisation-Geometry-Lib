"""Replay the bounded cutoff publication evidence without registering it."""
from __future__ import annotations

import json
from pathlib import Path
import sys


PACKET_DIR = Path(__file__).resolve().parent
ROOT = PACKET_DIR.parents[1]
sys.path[:0] = [str(ROOT / "tools"), str(ROOT / "website/scripts")]

import astis_publication as publication
import astis_semantic_roundtrip as roundtrip
import declaration_lessons as reader


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def main() -> None:
    evidence = PACKET_DIR / "cutoff-publication-evidence-v1"
    for label, was_blocked in (("superseded-extension", True),
                               ("superseded-extension-v2", True),
                               ("superseded-cutoff-limits", False)):
        prior_packet = read(evidence / f"{label}.reviewer_packet.json")
        prior_review = read(evidence / f"{label}.review_result.json")
        prior_packet_hash = prior_packet.pop("packet_sha256")
        prior_review_hash = prior_review.pop("review_run_sha256")
        require(roundtrip.sha256_json(prior_packet) == prior_packet_hash
                and roundtrip.sha256_json(prior_review) == prior_review_hash
                and prior_review["reviewer_packet_sha256"] == prior_packet_hash
                and any(row["blocking"] for row in prior_review["deltas"]) == was_blocked,
                f"{label}: the preserved older review is missing or changed")
    candidates = [read(PACKET_DIR / "cutoff-publication-candidate-v3.json"),
                  read(evidence / "gaussian-successor-publication.json")]
    items = [item for candidate in candidates for item in candidate["items"]]
    units = [unit for candidate in candidates for unit in candidate["units"]]
    bindings = {b["audit_id"]: (i, b) for i in items for b in i["bindings"]}
    audits = []
    for path in sorted(evidence.glob("*.audit.json")):
        fragment = read(path)
        audit = roundtrip._artifact_backed_audit(fragment, path)
        ident = audit["id"]
        require(audit["state"] == "source-reviewed" and audit["verdict"] in
                {"exact", "equivalent-after-elaboration"}
                and not any(row["severity"] == "blocking" for row in audit["deltas"]),
                f"{ident}: no acceptance for this bounded candidate")
        for field, hash_field in (("decoder_result", "decoder_run_sha256"),
                                  ("review_result", "review_run_sha256")):
            result = read(ROOT / fragment[field])
            pin = result.pop(hash_field)
            require(roundtrip.sha256_json(result) == pin, f"{ident}: invalid {field} pin")
        require(read(ROOT / fragment["decoder_packet"]) == roundtrip.decoder_packet(audit),
                f"{ident}: decoder packet changed")
        require(read(ROOT / fragment["reviewer_packet"]) == roundtrip.semantic_reviewer_packet(audit),
                f"{ident}: reviewer packet changed")
        audits.append(audit)
    require(len(audits) == 3 and {a["id"] for a in audits} == set(bindings),
            "Expected three distinct candidate bindings and their exact reviews")
    registry = {"schema_version": 1, "protocol": roundtrip.load_registry()["protocol"],
                "audits": audits}
    errors = roundtrip.validate_registry(registry)
    require(not errors, "\n".join(errors))

    data = publication.inputs()
    data["lessons"].update({unit["declaration"]: unit for unit in units})
    data["audits"].update({a["id"]: a for a in audits})
    for audit in audits:
        item, binding = bindings[audit["id"]]
        require(audit["publication_binding_sha256"] == publication.binding_digest(item, binding, data),
                f"{audit['id']}: code, source, or lesson has drifted")
        require(audit["publication_context"] == publication.review_context(item, binding, data),
                f"{audit['id']}: independent reviewer context is stale")
    for unit in units:
        html = reader.render_unit(unit, reader.lesson_path(unit["declaration"]))
        require("reader-progressive" in html and "Corresponding Lean step" in html
                and html.count("proof-reader-equation") >= 3,
                f"{unit['declaration']}: progressive lesson fragment is incomplete")
    print("3 exact source reviews and lesson fragments validated. No Cell or publication status changed.")


if __name__ == "__main__":
    main()
