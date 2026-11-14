"""Project one actual independent VERIFIED fact into its sole owned frontier."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent
ACTOR = "/root/affinity_integration_reader_review"
VERIFIER = "/root/block_law_fresh_source_module_review"
CANDIDATE = "83bb8c9361d0dba4077db5994f682a1f4b45d85a"
ADVANCE = "ASTIS-SA-20261106-GaussianComplexityConditionalBlockLaw"
CELL = "research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-conditional-block-law.json"
DECL = "AutoSamplingTheory.ExampleCases.GaussianComplexity.GaussianBlockLaw.actual_conditional_block_product"
ITEM = "huanjian-conditional-block-law"
AUDIT = f"research-wiki/semantic-roundtrip/audits/{ITEM}.json"
REVIEW = "research-wiki/paper-contributions/GaussianComplexity/conditional-block-law-semantic-evidence/fresh-source-module-review"
BINDING = "abc7158a0b068f10f16b9f7f09ae4e88647b78f5817b2b53424f0a874ebf1982"


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path):
    return json.loads((ROOT / path).read_text())


def file_hash(path):
    return digest((ROOT / path).read_bytes())


head = git("rev-parse", "HEAD").decode().strip()
assert head == CANDIDATE
summary_path = f"{REVIEW}/final-verification-summary.json"
summary_raw = (ROOT / summary_path).read_bytes()
assert digest(summary_raw) == "9de7375e958e8b7d5ef1dcde12d0d3a8eb64721a6eaf4b6e0312fc337a0ec411"
summary = json.loads(summary_raw)
assert summary["candidate_commit"] == CANDIDATE and summary["reviewer"] == VERIFIER
artifact_checks = []
for filename, expected in summary["artifacts"].items():
    path = f"{REVIEW}/{filename}"
    assert file_hash(path) == expected
    artifact_checks.append({"path": path, "raw_sha256": expected})
receipt_path = f"{REVIEW}/normal-api-verification.receipt.json"
assert file_hash(receipt_path) == "7449e5d87ced824c6e8f710184800b3118f38dfdced513a0da2159708674cc1f"
receipt = read(receipt_path)
assert receipt["api_succeeded"] and receipt["actor"] == VERIFIER
assert receipt["state_after"] == "VERIFIED" and receipt["verified_commit"] == CANDIDATE
prefix = (ROOT / REVIEW / "pre-verification-ledger-prefix.jsonl").read_bytes()
append = (ROOT / REVIEW / "verification-ledger-exact-append.jsonl").read_bytes()
ledger_path = ROOT / "runs/substantive_advances.jsonl"
ledger_before = ledger_path.read_bytes()
assert ledger_before == prefix + append
assert len(append.splitlines()) == 1
assert digest(prefix) == receipt["prefix_sha256"]
assert digest(append) == receipt["append_sha256"] == "78f921a39b760dca90c0b988230a0c248964decded654d4460a8c012a7a4cb28"
event = json.loads(append)
assert event["advance_id"] == ADVANCE and event["worker_id"] == VERIFIER
assert event["from_state"] == "PROVED_LOCAL" and event["to_state"] == "VERIFIED"
assert event["evidence"]["verifier_id"] == VERIFIER
assert event["evidence"]["verified_commit"] == CANDIDATE
assert event["evidence"]["publication_declarations"] == [DECL]
assert event["evidence"]["semantic_roundtrip_audit"]["publication_binding_sha256"] == BINDING

def check_referenced_artifacts(value):
    if isinstance(value, dict):
        if "path" in value and "sha256" in value:
            assert file_hash(value["path"]) == value["sha256"]
        for child in value.values():
            check_referenced_artifacts(child)
    elif isinstance(value, list):
        for child in value:
            check_referenced_artifacts(child)


check_referenced_artifacts(event["evidence"])
audit_raw = (ROOT / AUDIT).read_bytes()
audit = json.loads(audit_raw)
assert digest(audit_raw) == summary["semantic_audit_sha256"]
assert audit["state"] == "accepted" and audit["source_review"]["state"] == "accepted"
assert audit["publication_binding_sha256"] == BINDING
context_raw = subprocess.check_output(["python3", "tools/astis_publication.py", "review-context",
    "--item", ITEM, "--declaration", DECL], cwd=ROOT)
context = json.loads(context_raw)
assert context["publication_binding_sha256"] == BINDING
assert context["publication_context"] == audit["publication_context"]
(OUT / "current-publication-context.json").write_bytes(context_raw)

reviewed_inputs = []
for path in ["AutoSamplingTheory/ExampleCases/GaussianComplexity/GaussianBlockLaw.lean",
             "Tests/GaussianComplexityConditionalBlockLaw.lean",
             "website/content/declaration_lessons/huanjian-conditional-block-law.json",
             "website/content/publications/huanjian-conditional-block-law.json",
             "research-wiki/paper-contributions/GaussianComplexity/conditional-block-law-statement-seal.json"]:
    raw = (ROOT / path).read_bytes()
    assert raw == git("show", f"{CANDIDATE}:{path}")
    reviewed_inputs.append({"path": path, "raw_sha256": digest(raw), "same_as_reviewed_git_object": True})
bindings = read(f"{REVIEW}/initial-candidate-bindings.json")
for path, expected in bindings["hashes"].items():
    assert file_hash(path) == expected

guard = read(f"{REVIEW}/mutation-guards.before.json")
guard_paths = set(guard["protected_file_hashes"])
guard_paths.update(git("ls-files", "*.lean").decode().splitlines())
guard_paths.update([AUDIT, "runs/substantive_discoveries.jsonl", "AutoSamplingTheory.lean", "Tests.lean",
                    "AutoSamplingTheory/TechnicalLemmas/Registry.lean", "lake-manifest.json", "lean-toolchain"])
guard_paths.discard(CELL)
protected_before = {p: file_hash(p) for p in sorted(guard_paths)}
frontiers = sorted((ROOT / "research-wiki/frontier-cells").glob("*.json"))
frontier_before = {str(p.relative_to(ROOT)): digest(p.read_bytes()) for p in frontiers}
tracked_diff_before = set(git("diff", "--name-only").decode().splitlines())
old_drafts = {
    "candidate-compressed-spine-example.json": "18f1c82e5af658419c00bfaeef0c030643c8d268e7421c15d9c6ef4a54b27d34",
    "candidate-five-step-lossless-expansion.json": "2f6b871817ae14a1f9776c80c1be09bb406c4df837596ca26371a8991c0458dd",
    "candidate-purification-preparation.json": "2ad4b3f9bb34c00c3cdc81ed581246f2c592027f0c986ecefafb12efadc8c091"
}
old_dir = "research-wiki/paper-contributions/GaussianComplexity/affinity-integration-20261106/independent-integration-reader-review"
for name, expected in old_drafts.items():
    assert file_hash(f"{old_dir}/{name}") == expected

cell_before_raw = (ROOT / CELL).read_bytes()
data = json.loads(cell_before_raw)
assert data["status"] == "proved_locally" and data["advance_id"] == ADVANCE
historical = {
    "projection_actor": ACTOR,
    "meaning": "Exact earlier local-proof/preproof process wording retained as history; source omissions and theorem boundaries are unchanged.",
    "previous_status": data["status"],
    "source_detail_audit.gap": data["source_detail_audit"]["gap"],
    "source_detail_audit.fidelity_boundary": data["source_detail_audit"]["fidelity_boundary"],
    "evidence.execution_boundary": data["evidence"]["execution_boundary"],
    "graph_contribution.visual_review": data["graph_contribution"]["visual_review"]
}
data["historical_preintegration_checkpoints"] = historical
data["status"] = "independently_verified"
data["source_detail_audit"]["gap"] = "The source asserts prior-averaged Eq6 and leaves the fixed-matrix Gaussian block-product/coordinate prerequisite implicit. This exact fixed arbitrary-tuple producer, its full module and genuine marginal/coordinate/zero-tail consumers were independently accepted by /root/block_law_fresh_source_module_review at83bb8c9361d0dba4077db5994f682a1f4b45d85a. Full Eq6 averaging remains open. Root/Registry/publication integration, browser/graph/desktop/mobile/live delivery, merge and purification remain pending."
data["source_detail_audit"]["fidelity_boundary"] = "Only the actual fixed arbitrary-tuple Gaussian factorization is compiled and independently source/module/static-reader accepted. No full Eq6 prior mixture, actual product density Ex70, affinity Ex71, amplified TV Ex72, oracle/precision/query cap/expected-cost adapter, hidden-eigenbasis or main lower bound is concluded. No root/Registry/browser/live, M/P or whole-Goal completion is claimed."
data["evidence"]["execution_boundary"] = "Existing actual independent normal-API VERIFIED by /root/block_law_fresh_source_module_review at83bb8c9361d0dba4077db5994f682a1f4b45d85a covers the exact fixed-tuple source meaning, whole production module, focused genuine marginal/coordinate/zero-dimensional consumers, expanded statement and generated static reader content. This frontier projection adds no mathematical/source verdict. Full root/Registry/publication integration and real browser/graph/desktop/mobile/live delivery, actual merge and postmerge purification remain pending."
data["evidence"]["independent_verification"] = "Existing independent normal-API VERIFIED by /root/block_law_fresh_source_module_review at83bb8c9361d0dba4077db5994f682a1f4b45d85a. Actual final-verification-summary.json SHA9de7375e958e8b7d5ef1dcde12d0d3a8eb64721a6eaf4b6e0312fc337a0ec411 and normal-api-verification.receipt.json SHA7449e5d87ced824c6e8f710184800b3118f38dfdced513a0da2159708674cc1f are independently checked. This field cites that prior reviewer; /root/affinity_integration_reader_review only projects the already-recorded fact, with no new source verdict or VERIFIED event."
data["graph_contribution"]["visual_review"] = "Final integration graph/browser visual acceptance remains pending. Existing independent static reader-content acceptance is distinct from MathJax execution, graph visual QA, desktop/mobile and live delivery."
projection_report = "research-wiki/paper-contributions/GaussianComplexity/block-law-integration-20261106/independent-integration-reader-review/existing-verification-frontier-projection.json"
data["evidence"]["existing_verification_projection"] = {
    "projection_actor": ACTOR, "projection_kind": "existing-independent-ledger-fact-only",
    "original_source_verifier": VERIFIER, "verified_commit": CANDIDATE,
    "canonical_advance_id": ADVANCE,
    "final_verification_summary": summary_path,
    "final_verification_summary_raw_sha256": digest(summary_raw),
    "normal_api_verification_receipt": receipt_path,
    "normal_api_verification_receipt_raw_sha256": file_hash(receipt_path),
    "exact_original_VERIFIED_append_raw_sha256": digest(append),
    "accepted_current_publication_binding_sha256": BINDING,
    "new_VERIFIED_event_or_source_verdict": False,
    "projection_report": projection_report,
    "scope": "Fixed arbitrary-tuple Gaussian product-law prerequisite only; full prior-averaged Eq6 and all downstream density/affinity/amplification/complexity claims remain open."
}
(OUT / "frontier.before.json").write_bytes(cell_before_raw)
(ROOT / CELL).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
assert ledger_path.read_bytes() == ledger_before
assert all(file_hash(p) == expected for p, expected in protected_before.items())
frontier_after = {str(p.relative_to(ROOT)): digest(p.read_bytes()) for p in frontiers}
assert [p for p in frontier_before if frontier_before[p] != frontier_after[p]] == [CELL]
tracked_diff_after = set(git("diff", "--name-only").decode().splitlines())
assert tracked_diff_after == tracked_diff_before | {CELL}
assert (ROOT / AUDIT).read_bytes() == audit_raw
for name, expected in old_drafts.items():
    assert file_hash(f"{old_dir}/{name}") == expected

states = {}
for raw in ledger_before.splitlines():
    e = json.loads(raw)
    if e.get("event") == "transition":
        states[e["advance_id"]] = {"state": e["to_state"], "actor": e["worker_id"]}
assert states[ADVANCE] == {"state": "VERIFIED", "actor": VERIFIER}
diff = git("diff", "--", CELL)
(OUT / "existing-verification-frontier-projection.diff").write_bytes(diff)
result = {
    "schema": "astis-independent-existing-block-law-verification-projection/v1",
    "actor": ACTOR, "checked_at": datetime.now(timezone.utc).isoformat(),
    "checked_head": head,
    "authorization": "Only the new conditional-block-law owned frontier is writable for mechanical projection; root/import/Registry, producer, lessons/publication/audit, other frontier and queue/ledger changes remain outside scope.",
    "original_independent_verifier": VERIFIER,
    "source_or_mathematical_verdict_created_by_this_action": False,
    "normal_state_API_called": False, "new_ledger_events": 0,
    "actual_summary_raw_sha256": digest(summary_raw),
    "actual_original_verification_receipt_raw_sha256": file_hash(receipt_path),
    "actual_original_event_raw_sha256": digest(append),
    "actual_original_event": {k: event[k] for k in ["advance_id", "from_state", "to_state", "worker_id", "created_at"]},
    "original_prefix_plus_exact_append_equals_current_ledger": True,
    "all_referenced_original_gate_source_module_reader_artifact_hashes_verified": True,
    "summary_artifacts_checked": artifact_checks,
    "accepted_audit_raw_sha256": digest(audit_raw),
    "freshly_computed_current_publication_binding_sha256": context["publication_binding_sha256"],
    "current_publication_context_equals_accepted_audit_context": True,
    "reviewed_git_inputs_unchanged": reviewed_inputs,
    "changed_frontier": CELL,
    "frontier_before_raw_sha256": digest(cell_before_raw),
    "frontier_after_raw_sha256": file_hash(CELL),
    "frontier_count": len(frontiers),
    "all_other_frontiers_preserved": True,
    "all_other_frontier_hashes_unchanged": {p: v for p, v in frontier_before.items() if p != CELL},
    "protected_Lean_prose_audit_discovery_files_checked": len(protected_before),
    "protected_input_manifest_sha256": digest(json.dumps(protected_before, sort_keys=True, separators=(",", ":")).encode()),
    "all_protected_input_bytes_unchanged": True,
    "tracked_diff_before": sorted(tracked_diff_before),
    "tracked_diff_after": sorted(tracked_diff_after),
    "ledger_raw_sha256_unchanged": digest(ledger_before),
    "foreign_queue_or_state_changes": False,
    "current_owned_advance_state": states[ADVANCE],
    "single_stabilization_lane_unchanged": [k for k, v in states.items() if v["state"] == "STABILIZING"],
    "old_affinity_three_purification_drafts_unchanged": old_drafts,
    "exact_owned_diff_raw_sha256": digest(diff),
    "accepted_fact_scope": "The actual fixed arbitrary-tuple conditional Gaussian product-law prerequisite is independently source/whole-module/focused-consumer/static-reader accepted. Full averaged Eq6 is not accepted by this fact.",
    "still_pending": ["full root/Registry and publication integration", "real browser MathJax/desktop/mobile/graph visual QA", "public/live delivery", "actual repository merge", "postmerge purification/ExpositionSeal", "full Eq6 prior averaging and subsequent density/affinity/tensorization/TV amplification", "oracle/precision/caps/expected cost/hidden eigenbasis/main lower bounds and whole Goal"],
    "M_P_ExpositionSeal_Goal_completion_claims": False
}
(OUT / "protected-inputs.before-after-identical.json").write_text(json.dumps(protected_before, indent=2) + "\n")
output = ROOT / projection_report
output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"projection": "existing fact only; status independently_verified",
    "changed_frontiers": 1, "other_frontiers_preserved": len(frontiers) - 1,
    "protected_files_preserved": len(protected_before), "ledger_events_added": 0,
    "projection_report": projection_report, "projection_report_raw_sha256": file_hash(projection_report)}))
