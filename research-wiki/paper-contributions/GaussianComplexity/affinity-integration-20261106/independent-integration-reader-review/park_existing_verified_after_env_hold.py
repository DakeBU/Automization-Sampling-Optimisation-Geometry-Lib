"""One authorized normal-API parking transition; no new source verdict."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from tools import astis_advance

ACTOR = "/root/affinity_integration_reader_review"
PRIMARY = "ASTIS-SA-20261106-GaussianComplexitySingleBlockAffinity"
SHARED = "ASTIS-SA-20261106-NormalizedDensityAffinity"
ORIGINAL_VERIFIER = "/root/affinity_fresh_source_module_review"
ACCEPTED_SOURCE = "a5d10714ca01eb29c934acec06bb8983413182c2"
ACCEPTED_AUDITS = "03ce9786f225de7db33917c4c3b41ace64b29fb7"
PUBLISHED = "5a257960edfbeff0905d1ee938db32bb7303ea7e"
CI_CHECKOUT = "f76487e3f6c1d56daa6364e8f093471b4d1b9479"
REPORT = "research-wiki/paper-contributions/GaussianComplexity/single-block-affinity-semantic-evidence/independent-fresh-source-module-review/candidate-a5d10714-independent-source-module-reader-review.json"
REPORT_SHA = "84094263876ddc034e64499fc3c8fc6899d4be5414e157ba4dfb3be6ab72a258"
REMOTE = ROOT / "research-wiki/paper-contributions/GaussianComplexity/affinity-integration-20261106/remote-ci-hold-20261106"


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def file_hash(path):
    return digest((ROOT / path).read_bytes())


ledger = ROOT / "runs/substantive_advances.jsonl"
before_raw = ledger.read_bytes()
assert before_raw == git("show", f"{PUBLISHED}:runs/substantive_advances.jsonl")
before_states = astis_advance.current_advances()
assert before_states[PRIMARY]["state"] == "STABILIZING"
assert before_states[PRIMARY]["latest_evidence"]["integration_owner"] == "huanjian_gc_20261106_affinity_integration"
assert before_states[SHARED]["state"] == "VERIFIED"
assert file_hash(REPORT) == REPORT_SHA
assert git("rev-parse", f"{PUBLISHED}^{{tree}}") == git("rev-parse", f"{CI_CHECKOUT}^{{tree}}")

manifest = json.loads((ROOT / "research-wiki/paper-contributions/GaussianComplexity/affinity-integration-20261106/core-integration-manifest.json").read_text())
protected = dict(manifest["accepted_source_and_prose_files_unchanged"])
checks = []
for path, expected in protected.items():
    raw = (ROOT / path).read_bytes()
    assert digest(raw) == expected
    assert raw == git("show", f"{ACCEPTED_SOURCE}:{path}")
    checks.append({"path": path, "raw_sha256": expected,
        "unchanged_from_original_reviewed_source": ACCEPTED_SOURCE})
for item in ["normalized-density-affinity", "huanjian-single-block-affinity"]:
    path = f"research-wiki/semantic-roundtrip/audits/{item}.json"
    raw = (ROOT / path).read_bytes()
    assert raw == git("show", f"{ACCEPTED_AUDITS}:{path}")
    audit = json.loads(raw)
    assert audit["state"] == "accepted" and audit["source_review"]["state"] == "accepted"
    protected[path] = digest(raw)
    checks.append({"path": path, "raw_sha256": digest(raw),
        "unchanged_from_original_accepted_audits": ACCEPTED_AUDITS,
        "publication_binding_sha256": audit["publication_binding_sha256"]})
frontiers = sorted((ROOT / "research-wiki/frontier-cells").glob("*.json"))
frontier_hashes = {str(p.relative_to(ROOT)): digest(p.read_bytes()) for p in frontiers}
discoveries_raw = (ROOT / "runs/substantive_discoveries.jsonl").read_bytes()
for path in ["lean-toolchain", "lake-manifest.json",
             "research-wiki/paper-contributions/GaussianComplexity/single-block-affinity-statement-seal.json",
             "research-wiki/paper-contributions/GaussianComplexity/normalized-density-affinity-statement-seal.json"]:
    protected[path] = file_hash(path)

old_events = [json.loads(line) for line in before_raw.splitlines()]
prior = [e for e in old_events if e.get("advance_id") == PRIMARY and e.get("to_state") == "VERIFIED"]
assert len(prior) == 1 and prior[0]["worker_id"] == ORIGINAL_VERIFIER
original = prior[0]
assert original["evidence"]["source_audit"]["report_raw_sha256"] == REPORT_SHA
fake_record = original["evidence"]["fake_closure_scan"]["textual_scan_and_binding_record"]
assert file_hash(fake_record) == original["evidence"]["fake_closure_scan"]["raw_sha256"]
formal_pass = REMOTE / "pr385-formalization-attempt2-actual-pass.json"
assert digest(formal_pass.read_bytes()) == "a2e89e555449445e54991e675908001b43438e511255ef2f870a1501fdf1ba38"
pass_record = json.loads(formal_pass.read_text())
assert pass_record["conclusion"] == "success" and pass_record["build_jobs"] == 9636

evidence = {
    "parking_kind": "mechanical-existing-verification-parking",
    "verifier_id": ACTOR,
    "verified_commit": PUBLISHED,
    "original_source_verified_commit": ACCEPTED_SOURCE,
    "original_source_verifier_id": ORIGINAL_VERIFIER,
    "new_source_or_semantic_verdict": False,
    "authorization": "Current integration owner explicitly authorized this distinct reviewer to return only the primary STABILIZING item to its existing VERIFIED state, freeing the serialized lane during the external Bench acceptance hold.",
    "gate": {
        "kind": "reuse-actual-remote-canonical-9636-pass-on-identical-tracked-tree",
        "run_id": 42155528465, "attempt": 2,
        "actual_ci_checkout": CI_CHECKOUT,
        "actual_ci_tree_equals_published_candidate": True,
        "actual_pass_record": str(formal_pass.relative_to(ROOT)),
        "actual_pass_record_raw_sha256": digest(formal_pass.read_bytes()),
        "normal_publication_gate": "Normal transition API revalidates the unchanged exact declaration with reviewed=True; it does not invent a source verdict."
    },
    "source_audit": {
        "kind": "reuse-existing-independent-source-whole-module-review",
        "original_verifier_id": ORIGINAL_VERIFIER,
        "original_verified_commit": ACCEPTED_SOURCE,
        "report": REPORT, "report_raw_sha256": REPORT_SHA,
        "accepted_audit_commit": ACCEPTED_AUDITS,
        "current_source_lesson_publication_audit_bytes_unchanged": True,
        "new_source_verdict": False
    },
    "fake_closure_scan": {
        "kind": "reuse-existing-exact-source-proof-cleanliness-and-actual-remote-ASTIS-check",
        "original_record": fake_record,
        "original_record_raw_sha256": file_hash(fake_record),
        "original_verifier_id": ORIGINAL_VERIFIER,
        "current_module_bytes_unchanged": True,
        "original_findings": 0,
        "original_transitive_axioms": ["propext", "Classical.choice", "Quot.sound"],
        "new_scan_or_verdict_fabricated": False
    },
    "publication_declarations": ["AutoSamplingTheory.ExampleCases.GaussianComplexity.SingleBlockAffinity.single_block_affinity_bound"],
    "external_hold": {
        "Bench_run_id": 42155528532,
        "kind": "wall-time-limit/native-null on sogb-025",
        "diagnosis": str((REMOTE / "pr385-native-runtime-attempt1-wall-limit-diagnosis.json").relative_to(ROOT)),
        "not_mathematical_refutation": True,
        "no_unchanged_retry_or_budget_widening": True
    },
    "canonical_branch_preserved": "huanjian/gaussian-affinity-integration-20261106",
    "immutable_PR385_head_preserved": PUBLISHED,
    "reclaim_rule": "The integration owner must explicitly reclaim STABILIZING through the normal API after the Bench owner resolves the acceptance boundary; this parking grants no MERGED/PURIFIED/main/deployment credit.",
    "truth_boundary": "Existing local VERIFIED mathematics and source/reader acceptance remain intact. Only the primary serialized integration lease is released. Actual product laws/tensorization/amplification, oracle/precision/caps/cost/hidden eigenbasis and both main lower bounds remain open. No Goal status changes."
}
(OUT / "existing-verification-parking-request.json").write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n")
astis_advance.transition_advance(PRIMARY, "VERIFIED", worker_id=ACTOR,
    modes=["mechanical-existing-verification-parking", "release-serialized-lane-during-external-Bench-hold"],
    evidence=evidence)

after_raw = ledger.read_bytes()
assert after_raw.startswith(before_raw)
appended = after_raw[len(before_raw):]
assert len(appended.splitlines()) == 1
event = json.loads(appended)
assert event["advance_id"] == PRIMARY and event["from_state"] == "STABILIZING" and event["to_state"] == "VERIFIED"
assert event["worker_id"] == ACTOR and event["evidence"]["new_source_or_semantic_verdict"] is False
after_states = astis_advance.current_advances()
foreign_ids = set(before_states) - {PRIMARY}
assert all(before_states[k] == after_states[k] for k in foreign_ids)
assert after_states[SHARED]["state"] == "VERIFIED"
assert not any(v["state"] == "STABILIZING" for v in after_states.values())
assert all(file_hash(path) == expected for path, expected in protected.items())
assert all(file_hash(path) == expected for path, expected in frontier_hashes.items())
assert (ROOT / "runs/substantive_discoveries.jsonl").read_bytes() == discoveries_raw
(OUT / "existing-verification-parking.exact-append.jsonl").write_bytes(appended)
foreign_before = b"".join(line + b"\n" for line in before_raw.splitlines() if json.loads(line).get("advance_id") != PRIMARY)
foreign_after = b"".join(line + b"\n" for line in after_raw.splitlines() if json.loads(line).get("advance_id") != PRIMARY)
assert foreign_before == foreign_after
receipt = {
    "schema": "astis-normal-api-existing-verification-parking/v1",
    "actor": ACTOR, "checked_at": datetime.now(timezone.utc).isoformat(),
    "operation": "Normal API STABILIZING->VERIFIED for the primary only; no new source verdict.",
    "normal_api": "tools.astis_advance.transition_advance; no direct ledger write",
    "authorization": evidence["authorization"],
    "prior_raw_prefix": {
        "lossless_locator": f"git:{PUBLISHED}:runs/substantive_advances.jsonl",
        "git_blob": git("rev-parse", f"{PUBLISHED}:runs/substantive_advances.jsonl").decode().strip(),
        "raw_sha256": digest(before_raw), "bytes": len(before_raw),
        "entire_current_ledger_starts_with_that_exact_prefix": True,
        "reason_not_duplicated": "The immutable committed raw prefix plus this separately saved exact one-line append reconstructs the entire ledger losslessly; no duplicate status ledger is created."
    },
    "exact_append_path": str((OUT / "existing-verification-parking.exact-append.jsonl").relative_to(ROOT)),
    "exact_append_raw_sha256": digest(appended), "new_events": 1,
    "resulting_ledger_raw_sha256": digest(after_raw),
    "foreign_record_bytes_before_sha256": digest(foreign_before),
    "foreign_record_bytes_after_sha256": digest(foreign_after),
    "all_foreign_record_bytes_and_projected_states_preserved": True,
    "foreign_projected_state_count": len(foreign_ids),
    "shared_state": after_states[SHARED]["state"],
    "primary_state": after_states[PRIMARY]["state"],
    "single_stabilization_lane_after": [],
    "all_frontier_files_unchanged": True, "frontier_file_count": len(frontiers),
    "frontier_hashes_unchanged": frontier_hashes,
    "protected_source_lesson_publication_audit_hashes_unchanged": protected,
    "original_accepted_input_checks": checks,
    "discovery_ledger_bytes_unchanged": True,
    "new_math_source_or_semantic_verdict": False,
    "MERGED_PURIFIED_ExpositionSeal_Goal_status_changes": False,
    "boundary": evidence["reclaim_rule"]
}
receipt_path = OUT / "existing-verification-parking-receipt.json"
receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n")
hold_path = OUT / "pr385-independent-integration-env-hold-review.json"
previous = hold_path.read_bytes()
(OUT / "pr385-independent-integration-env-hold-before-parking.json").write_bytes(previous)
hold = json.loads(previous)
hold["hold_verdict"] = "External native Bench acceptance remains on hold. The authorized normal API has parked only the primary STABILIZING item back at its existing VERIFIED state, releasing the serialized lane. Original mathematical/source/local reader acceptance is preserved; actual merge/public delivery/purification remain pending."
hold["queue_preservation"]["before_parking_ledger_raw_sha256"] = hold["queue_preservation"].pop("ledger_raw_sha256")
hold["queue_preservation"]["ledger_raw_sha256_after_parking"] = digest(after_raw)
hold["queue_preservation"]["ledger_byte_equal_to_immutable_pr_head"] = False
hold["queue_preservation"]["immutable_pr_ledger_is_preserved_exact_byte_prefix"] = True
hold["queue_preservation"]["single_stabilization_lane"] = []
hold["queue_preservation"]["primary"] = {"state": "VERIFIED", "actor": ACTOR, "kind": "mechanical-existing-verification-parking"}
hold["queue_preservation"]["parking_receipt"] = str(receipt_path.relative_to(ROOT))
hold["queue_preservation"]["parking_receipt_raw_sha256"] = digest(receipt_path.read_bytes())
hold["new_VERIFIED_MERGED_PURIFIED_or_goal_state_events"] = {"mechanical_return_to_existing_VERIFIED": 1, "new_source_verdict": 0, "MERGED": 0, "PURIFIED": 0, "Goal_state": 0}
hold["parking_update"] = {"actor": ACTOR, "prior_hold_report_preserved_at": str((OUT / "pr385-independent-integration-env-hold-before-parking.json").relative_to(ROOT)), "prior_hold_report_raw_sha256": digest(previous), "result": "serialized lane released through normal API; no permanent hold on a foreign queue"}
hold["parking_update"]["supersession"] = "The initial held-STABILIZING recommendation is preserved unchanged; the later integration-owner authorization and actual normal-API parking event supersede only that control-plane recommendation."
supplement_path = OUT / "pr385-independent-integration-env-hold-final-supplement.json"
supplement_path.write_text(json.dumps(hold, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"normal_api_result": "primary parked VERIFIED; lane released", "actor": ACTOR,
    "new_append_events": 1, "all_foreign_states_and_records_preserved": True,
    "parking_receipt_raw_sha256": digest(receipt_path.read_bytes()),
    "final_env_hold_supplement_raw_sha256": digest(supplement_path.read_bytes())}))
