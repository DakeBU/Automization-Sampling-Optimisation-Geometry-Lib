"""Project one already-recorded source V into its current frontier; never append."""
from __future__ import annotations

import copy
import datetime as dt
import gzip
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / "tools"))
import astis_advance as advance
import astis_publication as publication

BASE = "research-wiki/paper-contributions/GaussianComplexity/"
REVIEW = BASE + "product-density-semantic-evidence/fresh-source-module-review/"
CELL = "research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-product-density.json"
AUDIT = "research-wiki/semantic-roundtrip/audits/huanjian-product-density.json"
TARGET = "AutoSamplingTheory.ExampleCases.GaussianComplexity.ProductDensity.actual_product_density"
ADVANCE = "ASTIS-SA-20261106-GaussianComplexityProductDensity"
SOURCE_ACTOR = "/root/ex70_fresh_source_module_review"
PROJECTION_ACTOR = "/root/ex70_integration_reader_review"
CANDIDATE = "a83254ef00c8e6fd0548a25fae03f07e2a82e2b7"
BINDING = "f764e7b080de73ded904fb5a89d6424878a1b2c2b292ca9648d70ed3ce19eca8"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def raw(rel: str) -> bytes:
    return (ROOT / rel).read_bytes()


def read(rel: str) -> object:
    return json.loads(raw(rel))


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":")).encode()


def dump(name: str, value: object) -> None:
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def verify_hashes(manifest: dict) -> list:
    return [rel for rel, expected in manifest.items()
            if not (ROOT / rel).is_file() or sha(raw(rel)) != expected]


def main() -> None:
    pins = {
        REVIEW + "normal-api-verified-transition.receipt.json": "685ce47914735fd4f888cc07466bb71ae60a6e54072a7e9ead6f63f477f183c0",
        REVIEW + "verified-phase-closeout.json": "68e045442404e4e46a6b960c9ff7c8398a0c85bf3f9f431540c8692e3df42c32",
        REVIEW + "verified-api-result.json": "479fb86f83a464b422cda1cb0c9771d80cbb933fb960384c23a79f3693e39135",
        AUDIT: "91a0565ed2da64800cf3ff0f1bc5169c9d0e54e643ba892a1d81284b30644332",
        "AutoSamplingTheory/ExampleCases/GaussianComplexity/ProductDensity.lean": "a75340883fb065e782a802f6dc8184f52d25fa96930e681d89dfc97fe87bd228",
        "Tests/GaussianComplexityProductDensity.lean": "ad9d4fa4048a2fb88b5eaade4a7bc202f05e0a4b48a13790893f8cc768fbfccd",
    }
    assert not verify_hashes(pins)
    receipt = read(REVIEW + "normal-api-verified-transition.receipt.json")
    closeout = read(REVIEW + "verified-phase-closeout.json")
    result = read(REVIEW + "verified-api-result.json")
    assert receipt["returncode"] == 0
    assert receipt["head_before"] == receipt["head_after"] == CANDIDATE
    receipt_log = gzip.decompress(raw(receipt["log"] + ".gz"))
    assert sha(receipt_log) == receipt["log_sha256"]
    assert len(receipt_log) == receipt["log_bytes"]
    ledger = raw("runs/substantive_advances.jsonl")
    before_ledger = gzip.decompress((OUT / "baseline-advance-ledger.jsonl.gz").read_bytes())
    before_source = gzip.decompress(raw(result["prefix_archive"]["path"]))
    assert before_ledger == before_source
    assert sha(before_ledger) == result["ledger_before_sha256"] == closeout["ledger_before_sha256"]
    assert ledger.startswith(before_ledger)
    appended = ledger[len(before_ledger):]
    assert appended == raw(result["append_path"])
    assert sha(appended) == result["append_sha256"] == closeout["unique_append_sha256"]
    appended_rows = [json.loads(line) for line in appended.splitlines() if line.strip()]
    assert len(appended_rows) == 1
    event = appended_rows[0]
    assert event == result["appended_event"]
    assert event["advance_id"] == ADVANCE
    assert event["worker_id"] == SOURCE_ACTOR
    assert event["from_state"] == "PROVED_LOCAL" and event["to_state"] == "VERIFIED"
    assert event["evidence"]["verified_commit"] == CANDIDATE
    assert event["evidence"]["publication_declarations"] == [TARGET]
    assert sha(ledger) == result["ledger_after_sha256"] == closeout["ledger_after_sha256"]
    current = advance._replay_advances(json.loads(line) for line in ledger.splitlines() if line.strip())
    baseline_hashes = json.loads((OUT / "baseline-projected-state-hashes.json").read_text())
    foreign_failures = [key for key, expected in baseline_hashes.items() if key != ADVANCE
                        and sha(canonical(current[key])) != expected]
    assert len(baseline_hashes) - 1 == 276 and not foreign_failures
    assert current[ADVANCE]["state"] == "VERIFIED"
    assert current[ADVANCE]["last_actor"] == SOURCE_ACTOR
    assert current[ADVANCE]["owner_id"] == "huanjian_gc_20261106_ex70"
    assert not [key for key, value in current.items() if value.get("state") == "STABILIZING"]
    old_frontiers = json.loads((OUT / "baseline-old-frontier-hashes.json").read_text())
    protected_inputs = json.loads((OUT / "baseline-protected-input-hashes.json").read_text())
    assert not verify_hashes(old_frontiers) and not verify_hashes(protected_inputs)
    initial = read(BASE + "product-density-semantic-evidence/initial-environment-queue-protection.json")
    old_snapshot = initial["lossless_raw_snapshot"]
    assert sha(raw(old_snapshot["path"])) == old_snapshot["gzip_sha256"]
    assert sha(gzip.decompress(raw(old_snapshot["path"]))) == old_snapshot["uncompressed_sha256"]
    assert sha(raw(initial["source"])) == initial["source_sha256"]
    audit = read(AUDIT)
    assert audit["state"] == "source-reviewed" and audit["source_review"]["state"] == "accepted"
    assert audit["source_review"]["reviewer"] == SOURCE_ACTOR
    assert audit["source_review"]["candidate_commit"] == CANDIDATE
    item = next(item for item in publication.load() if item["id"] == "huanjian-product-density")
    binding = next(binding for binding in item["bindings"] if binding["declaration"] == TARGET)
    actual_binding = publication.binding_digest(item, binding)
    assert actual_binding == BINDING == audit["publication_binding_sha256"]
    candidate_audit_raw = subprocess.check_output(["git", "show", CANDIDATE + ":" + AUDIT], cwd=ROOT)
    candidate_audit = json.loads(candidate_audit_raw)
    assert candidate_audit["state"] != "source-reviewed"
    assert sha(candidate_audit_raw) != sha(raw(AUDIT))

    before_raw = raw(CELL)
    before = json.loads(before_raw)
    assert before["status"] == "proved_locally"
    assert before["owner_id"] == "huanjian_gc_20261106_ex70"
    after = copy.deepcopy(before)
    after["status"] = "independently_verified"
    evidence = after["evidence"]
    evidence["local_phase_execution_boundary_history"] = before["evidence"]["execution_boundary"]
    evidence["execution_boundary"] = (
        "The existing source/whole-module VERIFIED fact was recorded by distinct reviewer "
        + SOURCE_ACTOR + " at mathematical candidate " + CANDIDATE
        + ". This frontier is a mechanical projection only, with no new source verdict or ledger event. "
        "Actual Ex70 density/coordinate-volume/L1/mass1 and both actual ambient/split measurable-set "
        "consumers are the accepted source scope. Root Tests/Registry/shared integration, canonical "
        "root gate, final site/graph and actual Chrome acceptance remain pending; Ex71/72, main query "
        "bounds, remote/public/live delivery, purification/ExpositionSeal and whole Goal completion remain open.")
    evidence["independent_verification"] = (
        "Existing independent normal-API VERIFIED by " + SOURCE_ACTOR + " at " + CANDIDATE
        + "; verified-phase-closeout.json SHA68e045442404e4e46a6b960c9ff7c8398a0c85bf3f9f431540c8692e3df42c32 "
        "and normal-api-verified-transition.receipt.json SHA685ce47914735fd4f888cc07466bb71ae60a6e54072a7e9ead6f63f477f183c0. "
        + PROJECTION_ACTOR + " independently checks and projects this already-recorded fact; it does not originate a source verdict.")
    report_rel = str((OUT / "existing-verification-frontier-projection.json").relative_to(ROOT))
    evidence["existing_verification_projection"] = {
        "projection_actor": PROJECTION_ACTOR,
        "kind": "existing-independent-ledger-fact-only",
        "original_source_verifier": SOURCE_ACTOR,
        "verified_commit": CANDIDATE,
        "proof_owner_preserved": "huanjian_gc_20261106_ex70",
        "actual_normal_API_receipt": REVIEW + "normal-api-verified-transition.receipt.json",
        "actual_normal_API_receipt_raw_sha256": pins[REVIEW + "normal-api-verified-transition.receipt.json"],
        "original_closeout": REVIEW + "verified-phase-closeout.json",
        "original_closeout_raw_sha256": pins[REVIEW + "verified-phase-closeout.json"],
        "actual_API_result": REVIEW + "verified-api-result.json",
        "actual_API_result_raw_sha256": pins[REVIEW + "verified-api-result.json"],
        "actual_existing_VERIFIED_append_raw_sha256": sha(appended),
        "current_source_reviewed_audit_raw_sha256": sha(raw(AUDIT)),
        "current_accepted_publication_binding_sha256": BINDING,
        "candidate_audit_state": candidate_audit["state"],
        "candidate_audit_byte_equal_current": False,
        "new_source_verdict_or_VERIFIED_event": False,
        "ledger_written_by_projection": False,
        "projection_report": report_rel,
        "remaining": "Root/Registry/Tests/shared integration, real canonical root gate, final site/graph/Chrome, remote/main/live, purification/ExpositionSeal and all Ex71/72/main/oracle/cost obligations remain separate pending phases."
    }
    after["source_proof_coverage"]["source_gaps"] = (
        "Typed author omissions remain visible without alteration in the frozen source graph. "
        "Actual-code discharge is mapped in actual-local-proof-capsule.json and independently accepted "
        "by " + SOURCE_ACTOR + " at " + CANDIDATE + "; see " + REVIEW + "verified-phase-closeout.json "
        "and review-run.json. This existing postproof source fact does not rewrite the author's omitted "
        "provenance or certify Ex71/72, root integration, remote delivery or purification.")
    # The current in-memory file, including root's recently added protocol fields,
    # is the source of this projection. No old commit snapshot is restored.
    unchanged = [key for key in before if key not in {"status", "evidence", "source_proof_coverage"}]
    assert all(after[key] == before[key] for key in unchanged)
    assert {key: value for key, value in after["source_proof_coverage"].items() if key != "source_gaps"} == {
        key: value for key, value in before["source_proof_coverage"].items() if key != "source_gaps"}
    assert raw(CELL) == before_raw and raw("runs/substantive_advances.jsonl") == ledger
    (OUT / "projection-frontier-before.json").write_bytes(before_raw)
    after_raw = (json.dumps(after, ensure_ascii=False, indent=2) + "\n").encode()
    (ROOT / CELL).write_bytes(after_raw)
    assert raw("runs/substantive_advances.jsonl") == ledger
    assert not verify_hashes(old_frontiers) and not verify_hashes(protected_inputs)
    assert not verify_hashes(pins)
    report = {
        "kind": "existing-independent-verification-mechanical-frontier-projection",
        "recorded_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "projection_actor": PROJECTION_ACTOR,
        "source_verifier": SOURCE_ACTOR,
        "verified_commit": CANDIDATE,
        "actual_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "source_target": TARGET,
        "frontier": CELL,
        "frontier_before_raw_sha256": sha(before_raw),
        "frontier_after_raw_sha256": sha(after_raw),
        "projected_status": "independently_verified",
        "preserved_current_top_level_fields": unchanged,
        "modified_fields": ["status", "evidence (phase history and existing fact references only)", "source_proof_coverage.source_gaps (postproof acceptance reference; frozen source graph unchanged)"],
        "pins_independently_recomputed": pins,
        "actual_publication_binding_sha256": actual_binding,
        "current_audit": {"state": audit["state"], "source_review_state": audit["source_review"]["state"],
                          "raw_sha256": sha(raw(AUDIT)), "candidate_state": candidate_audit["state"],
                          "candidate_raw_sha256": sha(candidate_audit_raw), "byte_equal_candidate": False},
        "normal_API_receipt_log": {"raw_sha256": sha(receipt_log), "raw_bytes": len(receipt_log), "returncode": receipt["returncode"]},
        "ledger": {"before_raw_sha256": sha(before_ledger), "after_raw_sha256": sha(ledger),
                   "exact_before_prefix_preserved": True, "appended_events": 1,
                   "existing_append_raw_sha256": sha(appended), "existing_append_actor": event["worker_id"],
                   "existing_append_transition": "PROVED_LOCAL -> VERIFIED", "new_projection_events": 0,
                   "ledger_written_by_projection": False, "actual_state": current[ADVANCE]["state"],
                   "actual_last_actor": current[ADVANCE]["last_actor"], "original_owner": current[ADVANCE]["owner_id"]},
        "protection": {"foreign_projected_states_preserved": 276, "old_frontier_files_preserved": 435,
                       "old_eq6_protected_inputs_preserved": 3680, "source_snapshot_and_lossless_gzip_preserved": True,
                       "source_actors_full_input_inventory_claim": "121328 is cited from original source closeout; this projection directly rechecks its own bounded 3680-input baseline, source/proof pins, old276states and old435frontiers."},
        "single_stabilization_lane": [],
        "new_source_verdict": False,
        "root_shared_integration_gate_site_graph_actual_browser": "PENDING",
        "remote_main_live_purification_ExpositionSeal_Goal": "OPEN; no status event",
        "phase_write_status": "Projection complete. Freeze all writes until parent supplies the final integration candidate and new authorization."
    }
    dump("existing-verification-frontier-projection.json", report)
    print(json.dumps({"report": report_rel, "report_raw_sha256": sha((OUT / "existing-verification-frontier-projection.json").read_bytes()),
                      "frontier_after_raw_sha256": sha(after_raw), "ledger_raw_sha256_unchanged": sha(ledger),
                      "new_projection_events": 0, "status": "WRITES_FROZEN"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
