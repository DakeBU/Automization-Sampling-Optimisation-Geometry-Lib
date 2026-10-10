"""Resume SAU77 without changing its frozen mathematics or other contributors."""
from pathlib import Path
import copy
import hashlib
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "tools"))
import astis_advance as advance
import astis_publication as publication
import astis_semantic_roundtrip as roundtrip

RUN = ROOT / "runs/20261007-companion-priority/pbps-unit-exponential-product77"
CELL = ROOT / "research-wiki/frontier-cells/ASTIS-SHARED-unit-exponential-product.json"
AUDIT = ROOT / "research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261010-UnitExponentialProduct.json"
PUB = ROOT / "website/content/publications/unit-exponential-product.json"

def load(path):
    return json.loads(Path(path).read_bytes())

def write(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")

def pin(path):
    path = Path(path)
    raw = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(), "RAW_bytes": len(raw),
            "RAW_sha256": hashlib.sha256(raw).hexdigest()}

def proved_local():
    claim = load(RUN / "claim.json")
    current = advance.current_advances()[claim["advance_id"]]
    assert current["state"] == "EXPLORING", current["state"]
    focused = load(RUN / "resume-focused77/receipt.json")
    assert focused["exit_code"] == 0 and focused["terminal_closed"]
    declarations = claim["target_declarations"]
    cell = load(CELL)
    evidence = {
        "result_kind": "reusable-interface",
        "theorem_delta": claim["theorem_delta"],
        "lean_declarations": declarations,
        "publication_declarations": declarations,
        "lean_files": claim["proposed_files"],
        "focused_checks": [pin(RUN / "resume-focused77/receipt.json")],
        "truth_boundary": claim["truth_boundary"],
        "conceptual_mirror_audit": cell["conceptual_mirror_audit"],
        "independent_math": pin(RUN / "root.math77.adoption.json"),
        "blind_decoder": pin(RUN / "root.decoder77.adoption.json"),
        "statement_seal": cell["statement_seal"],
        "source_proof_coverage": cell["source_proof_coverage"],
        "proof_digestion": cell["proof_digestion"],
        "purification": cell["purification"],
        "integration_notes": "Current /root resumes the existing owner lane; no new SAU or proof writer. Exact original public signature, whole module, seven formula/BODY steps and blind reconstruction are unchanged. Source review and exact-commit verification are separate admissions."
    }
    advance.transition_advance(claim["advance_id"], "PROVED_LOCAL", worker_id=current["owner_id"], evidence=evidence)
    cell["status"] = "proved_locally"
    cell["evidence"]["resume_focused_check"] = evidence["focused_checks"][0]
    write(CELL, cell)
    write(RUN / "proved-local.json", evidence)
    print("PROVED_LOCAL: existing SAU77 only; independent source/commit and aggregate remain separate.")

def adopt(report_path):
    report_path = Path(report_path).resolve()
    report = load(report_path)
    audit = load(AUDIT)
    assert audit["state"] == "blind-reconstructed"
    packet = load(RUN / "source-review.packet.json")
    assert roundtrip.semantic_reviewer_packet(audit) == packet
    assert report["reviewer_packet_sha256"] == packet["packet_sha256"]
    hashes = report["input_hashes"]
    assert hashes["publication_binding_sha256_as_supplied"] == audit["publication_binding_sha256"]
    assert pin(ROOT / audit["lean"]["file"])["RAW_sha256"] == hashes["module_sha256"]
    assert pin(RUN / "source-review.packet.json")["RAW_sha256"] == hashes["packet_raw_sha256"]
    for name, key in [("lean-toolchain", "toolchain_normalized_text_sha256"),
                      ("lake-manifest.json", "manifest_normalized_text_sha256")]:
        normalized = (ROOT / name).read_bytes().replace(b"\r\n", b"\n")
        assert hashlib.sha256(normalized).hexdigest() == hashes[key]
    manifest = report_path.parent / "review-run-manifest.json"
    assert pin(manifest)["RAW_sha256"] == report["review_run_sha256"]
    accepted = copy.deepcopy(audit)
    for field in ("semantic_slots", "verdict", "deltas", "repairs", "source_review"):
        accepted[field] = copy.deepcopy(report["audit_fields"][field])
    accepted["state"] = accepted["source_review"]["state"]
    accepted["source_review"]["run_artifact"] = manifest.relative_to(ROOT).as_posix()
    assert accepted["state"] == accepted["source_review"]["state"] == "accepted"
    assert accepted["source_review"]["reviewer"] == "/root/source_review77"
    assert roundtrip.semantic_reviewer_packet(accepted) == packet
    registry = roundtrip.load_registry()
    registry["audits"] = [accepted if a["id"] == accepted["id"] else a for a in registry["audits"]]
    errors = roundtrip.validate_registry(registry)
    assert not errors, errors
    publication.inputs.cache_clear()
    publication.load.cache_clear()
    item = next(x for x in publication.load() if x["id"] == "unit-exponential-product")
    assert publication.binding_digest(item, item["bindings"][0], publication.inputs()) == accepted["publication_binding_sha256"]
    assert publication.review_context(item, item["bindings"][0], publication.inputs()) == accepted["publication_context"]
    snapshot = RUN / "resume-20261010/audit.before-source-adoption.json"
    assert not snapshot.exists()
    snapshot.write_bytes(AUDIT.read_bytes())
    write(AUDIT, accepted)
    topology = report["source_topology"]
    coverage = {
        "source_graph": report_path.relative_to(ROOT).as_posix(),
        "source_inventory": (report_path.parent / "source-only-freeze.json").relative_to(ROOT).as_posix(),
        "inventory": topology["coverage"],
        "reviewed_nodes": [x for x in topology["coverage"] if "NODE" in x["classification"]],
        "excluded_with_reason": [x for x in topology["coverage"] if "EXCLUDED" in x["classification"]],
        "source_gaps": topology["source_gaps"],
        "alternative_routes": topology["or_routes"],
        "coverage_status": "Independently source-first reviewed scoped input-law leaf. Mixed source paragraph split explicitly; direct author moment route and downstream Ex9/time/process remain open.",
        "reviewer": report["reviewer"], "future_scope_status": "OPEN"
    }
    cell = load(CELL)
    cell["source_proof_coverage"] = coverage
    cell["evidence"]["source_review"] = report_path.relative_to(ROOT).as_posix()
    cell["source_detail_audit"]["detail_status"] = "recovered"
    cell["blocked"]["reason"] = "Independent whole-math, blind reconstruction and source review accepted; exact-commit verification and serialized integration remain pending."
    write(CELL, cell)
    pub = load(PUB)
    pub["items"][0]["source_proof_coverage"] = coverage
    write(PUB, pub)
    publication.check_advance([audit["lean"]["declaration"]], reviewed=True)
    write(RUN / "root.source77.adoption.json", {
        "status": "ACCEPTED_INDEPENDENT_SOURCE77_ONLY", "review": pin(report_path),
        "reviewer": "/root/source_review77", "reviewer_packet_unchanged": True,
        "publication_binding_unchanged": True, "mathematics_and_lesson_unchanged": True,
        "source_proof_coverage": coverage, "VERIFIED": False, "Goal_complete": False
    })
    print("Accepted independent source review; current publication binding and clean packet unchanged.")

if __name__ == "__main__":
    if sys.argv[1] == "proved-local":
        proved_local()
    elif sys.argv[1] == "adopt":
        adopt(sys.argv[2])
    else:
        raise ValueError(sys.argv[1])
