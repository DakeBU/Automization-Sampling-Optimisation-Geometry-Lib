"""Authorized normal-API parking and sole-cell local-stage evidence update."""
from contextlib import redirect_stdout, redirect_stderr
from datetime import datetime, timezone
import gzip
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from tools import astis_advance
sys.path.insert(0, str(ROOT / "tools"))
import astis_site

ACTOR = "/root/affinity_integration_reader_review"
PRIMARY = "ASTIS-SA-20261106-GaussianComplexityConditionalBlockLaw"
OWNER = "huanjian_gc_20261106_block_law_integration"
SOURCE_VERIFIER = "/root/block_law_fresh_source_module_review"
SOURCE_COMMIT = "83bb8c9361d0dba4077db5994f682a1f4b45d85a"
ACCEPTED_METADATA = "11c6b994a8639c8343b3c099469cf8197caf7c06"
CORE = "672d19fce913733a52cb1ad42596a8229ffc6d6d"
CELL = "research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-conditional-block-law.json"
DECL = "AutoSamplingTheory.ExampleCases.GaussianComplexity.GaussianBlockLaw.actual_conditional_block_product"
REVIEW_DIR = "research-wiki/paper-contributions/GaussianComplexity/conditional-block-law-semantic-evidence/fresh-source-module-review"
BINDING = "abc7158a0b068f10f16b9f7f09ae4e88647b78f5817b2b53424f0a874ebf1982"
SOURCE_DIGEST = "ca0f75bd3977ecd19cbcd664c1f44ab87882d1c876ab97e5b51f86107967600d"


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def file_hash(path):
    return digest((ROOT / path).read_bytes())


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def read(path):
    return json.loads((ROOT / path).read_text())


def canonical_hash(value):
    return digest(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode())


assert git("rev-parse", "HEAD").decode().strip() == CORE
ledger = ROOT / "runs/substantive_advances.jsonl"
before_raw = ledger.read_bytes()
assert before_raw == git("show", f"{CORE}:runs/substantive_advances.jsonl")
before_states = astis_advance.current_advances()
assert before_states[PRIMARY]["state"] == "STABILIZING"
assert before_states[PRIMARY]["latest_evidence"]["integration_owner"] == OWNER
assert before_states[PRIMARY]["owner_id"] == "huanjian_gc_20261106_block_law"
assert astis_site.source_digest() == SOURCE_DIGEST

old_affinity_ids = ["ASTIS-SA-20261106-GaussianComplexitySingleBlockAffinity",
                    "ASTIS-SA-20261106-NormalizedDensityAffinity"]
assert all(before_states[k]["state"] == "VERIFIED" for k in old_affinity_ids)
assert read(f"{REVIEW_DIR}/final-verification-summary.json")["reviewer"] == SOURCE_VERIFIER
assert file_hash(f"{REVIEW_DIR}/final-verification-summary.json") == "9de7375e958e8b7d5ef1dcde12d0d3a8eb64721a6eaf4b6e0312fc337a0ec411"
assert file_hash(str((OUT / "candidate-672d19fc-independent-final-browser-site-acceptance.json").relative_to(ROOT))) == "d4311e28723650476e13b12057e78c71144efce59d5fef86d308c03232286e50"
audit_path = "research-wiki/semantic-roundtrip/audits/huanjian-conditional-block-law.json"
audit = read(audit_path)
assert audit["state"] == "accepted" and audit["source_review"]["state"] == "accepted"
assert audit["publication_binding_sha256"] == BINDING
assert file_hash(audit_path) == "3fda2b878f35f0bae152f0ec5c6143bdced0b6f0c4a037fd76e6b89aaf4d71b5"
assert (ROOT / audit_path).read_bytes() == git("show", f"{ACCEPTED_METADATA}:{audit_path}")
for path in ["AutoSamplingTheory/ExampleCases/GaussianComplexity/GaussianBlockLaw.lean",
             "Tests/GaussianComplexityConditionalBlockLaw.lean",
             "website/content/declaration_lessons/huanjian-conditional-block-law.json",
             "website/content/publications/huanjian-conditional-block-law.json"]:
    assert (ROOT / path).read_bytes() == git("show", f"{SOURCE_COMMIT}:{path}")

guard_paths = set(read(f"{REVIEW_DIR}/mutation-guards.before.json")["protected_file_hashes"])
guard_paths.update(git("ls-files", "*.lean").decode().splitlines())
guard_paths.update([audit_path, "runs/substantive_discoveries.jsonl", "AutoSamplingTheory.lean",
                    "Tests.lean", "Tests/Basic.lean", "AutoSamplingTheory/TechnicalLemmas/Registry.lean",
                    "lake-manifest.json", "lean-toolchain", "website/content/samplewiki_companion_frontiers.json"])
guard_paths.discard(CELL)
protected = {p: file_hash(p) for p in sorted(guard_paths)}
frontiers = sorted((ROOT / "research-wiki/frontier-cells").glob("*.json"))
frontier_before = {str(p.relative_to(ROOT)): digest(p.read_bytes()) for p in frontiers}
cell_raw = (ROOT / CELL).read_bytes()
cell = json.loads(cell_raw)
assert cell["status"] == "independently_verified"
tracked_diff_before = set(git("diff", "--name-only").decode().splitlines())

# A deterministic compressed archive saves every exact raw byte, including CRLF.
# Decompression is checked against the live prefix before any state mutation.
archive_path = OUT / "before-parking-ledger-prefix.raw.jsonl.gz"
archive = gzip.compress(before_raw, mtime=0)
archive_path.write_bytes(archive)
assert gzip.decompress(archive_path.read_bytes()) == before_raw
(OUT / "frontier.before-local-integration-parking.json").write_bytes(cell_raw)
(OUT / "local-integration-parking.protected-inputs.json").write_text(json.dumps(protected, indent=2) + "\n")
(OUT / "local-integration-parking.foreign-state-hashes.before.json").write_text(json.dumps(
    {k: canonical_hash(v) for k, v in before_states.items() if k != PRIMARY}, indent=2) + "\n")

event_candidates = [json.loads(line) for line in before_raw.splitlines()
    if json.loads(line).get("advance_id") == PRIMARY and json.loads(line).get("to_state") == "VERIFIED"]
assert len(event_candidates) == 1 and event_candidates[0]["worker_id"] == SOURCE_VERIFIER
original = event_candidates[0]
fake = original["evidence"]["fake_closure_scan"]
assert file_hash(fake["path"]) == fake["sha256"]
core_gate = read("research-wiki/paper-contributions/GaussianComplexity/block-law-integration-20261106/actual-root-gate-at-core-commit.json")
assert core_gate["actual_full_root_gate"]["commit"] == CORE
assert core_gate["actual_full_root_gate"]["passed"] and core_gate["actual_jobs"] == 9638
assert file_hash(core_gate["actual_raw_log"]) == core_gate["actual_raw_log_sha256"] == "31133f24d8158ee2f80c5862a8bf49702c5cb849d930b7c95544277bb764decf"

evidence = {
    "parking_kind": "mechanical-existing-verification-parking-after-local-root-reader-acceptance",
    "verifier_id": ACTOR,
    "verified_commit": CORE,
    "original_source_verified_commit": SOURCE_COMMIT,
    "original_source_verifier_id": SOURCE_VERIFIER,
    "new_mathematical_source_or_semantic_verdict": False,
    "authorization": "The current integration owner explicitly authorized only this primary STABILIZING->existing VERIFIED parking, releasing its local integration lease after the independent672d local root/site/14PNG acceptance. The proving owner remains unchanged.",
    "gate": {
        "kind": "actual672d-canonical-root9638-and-independent-local-reader-acceptance-reused",
        "actual_core_commit": CORE, "actual_source_digest": SOURCE_DIGEST,
        "actual_root_gate_record": "research-wiki/paper-contributions/GaussianComplexity/block-law-integration-20261106/actual-root-gate-at-core-commit.json",
        "actual_root_raw_log_sha256": core_gate["actual_raw_log_sha256"],
        "independent_root_receipt_review": str((OUT / "candidate-672d19fc-actual-root-receipt-inspection.json").relative_to(ROOT)),
        "independent_final_local_reader_review": str((OUT / "candidate-672d19fc-independent-final-browser-site-acceptance.json").relative_to(ROOT)),
        "independent_final_local_reader_review_raw_sha256": "d4311e28723650476e13b12057e78c71144efce59d5fef86d308c03232286e50",
        "normal_reviewed_publication_gate": "Normal API revalidates the exact unchanged target with reviewed=True; no substitute source verdict is generated."
    },
    "source_audit": {
        "kind": "reuse-actual-existing-fresh-independent-source-whole-module-static-reader-verdict",
        "original_reviewer": SOURCE_VERIFIER, "original_source_commit": SOURCE_COMMIT,
        "original_summary": f"{REVIEW_DIR}/final-verification-summary.json",
        "original_summary_raw_sha256": "9de7375e958e8b7d5ef1dcde12d0d3a8eb64721a6eaf4b6e0312fc337a0ec411",
        "accepted_audit": audit_path,
        "accepted_audit_raw_sha256": file_hash(audit_path),
        "current_publication_binding_sha256": BINDING,
        "original_source_Test_lesson_publication_and_accepted_audit_inputs_unchanged": True,
        "new_source_verdict": False
    },
    "fake_closure_scan": {
        "kind": "reuse-existing-independent-exact-module-cleanliness-plus-actual-root-ASTIS-success",
        "original_reviewer": SOURCE_VERIFIER,
        "original_record": fake["path"], "original_record_raw_sha256": fake["sha256"],
        "actual_current_module_bytes_unchanged": True,
        "actual_root_ASTIS_success_at": CORE,
        "new_scan_or_source_verdict_fabricated": False
    },
    "publication_declarations": [DECL],
    "local_acceptance_scope": "Exact fixed arbitrary-tuple Gaussian joint product and real marginal/coordinate/zero-tail consumer result; current root/Registry611/site/graph and local Chrome1440/390 reader accepted. Full prior-averaged Eq6 is not established.",
    "canonical_branch_preserved": "huanjian/gaussian-block-law-integration-20261106",
    "released_integration_owner": OWNER,
    "proving_owner_preserved": "huanjian_gc_20261106_block_law",
    "external_hold": "The oldPR385 at5a and its unmodified Bench native wall-limit remain separate. No push, retry, foreignPR384/385 action, merge or live deployment is performed.",
    "reclaim_rule": "Only a later authorized normal API STABILIZING claim may reacquire serialized integration before an eventual actual remote merge/delivery; this mechanical return grants no MERGED/PURIFIED/ExpositionSeal credit.",
    "truth_boundary": "The original83bb mathematical/source verdict is reused. Full Eq6 prior average, Ex70 densities, affinity tensorization, amplifiedTV, oracle/precision/deterministiccaps/expectedcost/hiddeneigenbasis and both main bounds remain open. Actual remote merge/live delivery, postmerge purification and ExpositionSeal remain pending. No Goal status is changed."
}
(OUT / "local-integration-parking.request.json").write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n")
captured = io.StringIO()
with redirect_stdout(captured), redirect_stderr(captured):
    astis_advance.transition_advance(PRIMARY, "VERIFIED", worker_id=ACTOR,
        modes=["mechanical-existing-verification-parking", "release-local-integration-lease-after-actual-root-reader-acceptance"],
        evidence=evidence)
(OUT / "local-integration-parking.normal-api.log").write_text(captured.getvalue())

after_raw = ledger.read_bytes()
assert after_raw.startswith(before_raw)
append = after_raw[len(before_raw):]
assert len(append.splitlines()) == 1
new_event = json.loads(append)
assert new_event["advance_id"] == PRIMARY and new_event["worker_id"] == ACTOR
assert new_event["from_state"] == "STABILIZING" and new_event["to_state"] == "VERIFIED"
assert new_event["evidence"]["new_mathematical_source_or_semantic_verdict"] is False
after_states = astis_advance.current_advances()
foreign_ids = set(before_states) - {PRIMARY}
assert all(before_states[k] == after_states[k] for k in foreign_ids)
assert after_states[PRIMARY]["owner_id"] == before_states[PRIMARY]["owner_id"]
assert all(after_states[k] == before_states[k] for k in old_affinity_ids)
assert not any(v["state"] == "STABILIZING" for v in after_states.values())
foreign_before = b"".join(line for line in before_raw.splitlines(keepends=True)
    if json.loads(line).get("advance_id") != PRIMARY)
foreign_after = b"".join(line for line in after_raw.splitlines(keepends=True)
    if json.loads(line).get("advance_id") != PRIMARY)
assert foreign_before == foreign_after
(OUT / "local-integration-parking.exact-append.jsonl").write_bytes(append)

history = {
    "updated_by": ACTOR,
    "meaning": "Exact earlier pending/preproof wording preserved as history; the original independent source verdict and current local integration acceptance have separate commit/evidence scopes.",
    "source_detail_audit.gap": cell["source_detail_audit"]["gap"],
    "source_detail_audit.fidelity_boundary": cell["source_detail_audit"]["fidelity_boundary"],
    "evidence.execution_boundary": cell["evidence"]["execution_boundary"],
    "graph_contribution.visual_review": cell["graph_contribution"]["visual_review"],
    "graph_contribution.reason": cell["graph_contribution"]["reason"],
    "learning_contract.salvage.reason": cell["learning_contract"]["salvage"]["reason"],
    "consumers": cell["consumers"],
    "reuse_plan.planned_consumers": cell["reuse_plan"]["planned_consumers"],
    "shared_floor_audit.note": cell["shared_floor_audit"]["note"]
}
cell["historical_local_integration_checkpoints"] = history
cell["source_detail_audit"]["gap"] = "The printed source leaves the fixed-matrix Gaussian block-product/coordinate prerequisite implicit. The exact fixed arbitrary-tuple producer remains independently source/whole-module accepted at83bb by /root/block_law_fresh_source_module_review, with unchanged inputs. Actual local672d canonical root9638, Registry611, generated site/graph and real Chrome1440/390 reader/module/source-index acceptance are complete and independently reviewed. Full prior-averaged Eq6, remote merge/live delivery and postmerge purification/ExpositionSeal remain pending."
cell["source_detail_audit"]["fidelity_boundary"] = "Only the actual fixed arbitrary-tuple Gaussian joint factorization and its real marginal/coordinate/zero-tail consumers are compiled and independently accepted. Actual672d root/Registry and local site/graph/14PNG reader acceptance are complete. No full Eq6 prior average, Ex70 density, Ex71 affinity tensorization, Ex72 amplifiedTV, oracle/precision/deterministic-query-cap/expected-cost adapter, hidden eigenbasis or either main bound is concluded. No remote merge/live deployment, PURIFIED, ExpositionSeal or whole-Goal completion is claimed."
cell["evidence"]["execution_boundary"] = "Original mathematical/source/whole-module acceptance is the actual83bb fresh independent review; accepted audit entered11c and remains byte-identical. Local integration acceptance is the actual672d root9638/sourceDigestca0f75bd, Registry611, site build/check, graph check and independently inspected14ChromePNG at1440/390. The normal API now parks the sole primary integration lease back at its existing VERIFIED state, keeping the proving owner and all foreign queues. No new source verdict, remote merge/live or purification is inferred."
cell["graph_contribution"]["visual_review"] = "Actual local672d graph and reader desktop/mobile inspection accepted by /root/affinity_integration_reader_review:14realChromePNG, one canonical compiled target, solid module structure and dashed source/fidelity overlays. Narrow scanner view is not exhaustive proof-constant dependency certification. See candidate-672d19fc-independent-final-browser-site-acceptance.json."
cell["graph_contribution"]["reason"] = "The unchanged canonical declaration was serialized into root/Test imports and one Registry entry, with a single local source reader/card. This local acceptance adds no formal edge from source/fidelity overlays and does not close full averaged Eq6 or the main bounds."
cell["learning_contract"]["salvage"]["reason"] = "No failed mathematical route or proof fragment is deleted by this local integration/parking pass. The earlier No proof search intake wording is preserved in historical_local_integration_checkpoints; compilation/source acceptance and actual local root/reader acceptance are now separately evidenced."
cell["consumers"] = [
    "Tests.GaussianComplexityConditionalBlockLaw: actual all-source-parameter arbitrary-tuple block/residual Gaussian marginals, contiguous coordinate equations and inverse assembly, and zero-dimensional probability point mass (compiled and independently reviewed).",
    "Actual common-sign independently conditioned prior-averaged Eq6 law (planned, not yet compiled)."
]
cell["reuse_plan"]["planned_consumers"] = ["Actual common-sign independent-prior averaging of this fixed-tuple producer for printed Eq6; product density/tensorization/amplification remain subsequent open obligations."]
cell["shared_floor_audit"]["note"] = "The actual canonical precision definitions and existing Mathlib Gaussian/product/characteristic-function interfaces are reused by the accepted83bb sole source-specific theorem. Local672d root/Registry/reader acceptance is complete. No new generic Gaussian product theorem, duplicate wrapper, full Eq6 or purification credit is claimed."
cell["evidence"]["local_integration_acceptance"] = {
    "local_acceptance_reviewer": ACTOR, "core_commit": CORE,
    "source_digest": SOURCE_DIGEST,
    "canonical_root_jobs": 9638,
    "root_raw_log_sha256": "31133f24d8158ee2f80c5862a8bf49702c5cb849d930b7c95544277bb764decf",
    "site_check_raw_log_sha256": "be60a160420ade95dbef32a2d23734c399a50549414c1ee2969c6820fbf3ce2b",
    "graph_check_raw_log_sha256": "e5ceb3532e45e40d376c0ecb6debe073e72811d60d5236bc1d3dab4a717d9add",
    "actual_Chrome_report_raw_sha256": "ceff2c7687585a71b09e16bc34bdb99a74a3f58f6e5b722383228eac3ee75c02",
    "actual_Chrome_PNG_count": 14, "viewports": [1440, 390],
    "independent_final_reader_report": str((OUT / "candidate-672d19fc-independent-final-browser-site-acceptance.json").relative_to(ROOT)),
    "independent_final_reader_report_raw_sha256": "d4311e28723650476e13b12057e78c71144efce59d5fef86d308c03232286e50",
    "source_verdict_is_new": False,
    "remote_GitHub_HTML_live_merge_PURIFIED_ExpositionSeal": "not certified"
}
cell["evidence"]["local_integration_lease_parking"] = {
    "actor": ACTOR, "kind": evidence["parking_kind"],
    "normal_API": "tools.astis_advance.transition_advance",
    "from_state": "STABILIZING", "to_state": "VERIFIED",
    "new_source_verdict": False, "single_stabilization_lane_after": [],
    "receipt": str((OUT / "local-integration-parking-receipt.json").relative_to(ROOT)),
    "exact_append_raw_sha256": digest(append),
    "remaining": evidence["truth_boundary"]
}
assert cell["status"] == "independently_verified"
(ROOT / CELL).write_text(json.dumps(cell, ensure_ascii=False, indent=2) + "\n")

assert all(file_hash(p) == expected for p, expected in protected.items())
frontier_after = {str(p.relative_to(ROOT)): digest(p.read_bytes()) for p in frontiers}
assert [p for p in frontier_before if frontier_before[p] != frontier_after[p]] == [CELL]
assert set(git("diff", "--name-only").decode().splitlines()) == tracked_diff_before | {CELL, "runs/substantive_advances.jsonl"}
assert astis_site.source_digest() == SOURCE_DIGEST
diff = git("diff", "--", CELL)
(OUT / "local-integration-parking.frontier-stage-evidence.diff").write_bytes(diff)
foreign_hashes_after = {k: canonical_hash(after_states[k]) for k in foreign_ids}
(OUT / "local-integration-parking.foreign-state-hashes.after.json").write_text(json.dumps(foreign_hashes_after, indent=2) + "\n")
receipt = {
    "schema": "astis-independent-normal-API-local-integration-parking/v1",
    "actor": ACTOR, "checked_at": datetime.now(timezone.utc).isoformat(),
    "actual_candidate": CORE,
    "normal_API_operation": "STABILIZING->existing VERIFIED, primary only; no direct ledger write",
    "new_source_mathematical_or_semantic_verdict": False,
    "original_source_verifier": SOURCE_VERIFIER, "original_source_commit": SOURCE_COMMIT,
    "accepted_audit_baseline": ACCEPTED_METADATA,
    "source_binding": BINDING,
    "saved_exact_raw_prefix": {
        "archive": str(archive_path.relative_to(ROOT)),
        "archive_sha256": digest(archive), "raw_prefix_sha256": digest(before_raw),
        "raw_prefix_bytes": len(before_raw),
        "decompression_equals_entire_exact_before_ledger": True,
        "also_equals_immutable_git_blob": git("rev-parse", f"{CORE}:runs/substantive_advances.jsonl").decode().strip()
    },
    "exact_append": {
        "path": str((OUT / "local-integration-parking.exact-append.jsonl").relative_to(ROOT)),
        "raw_sha256": digest(append), "bytes": len(append), "events": 1,
        "actor": ACTOR, "from_state": "STABILIZING", "to_state": "VERIFIED"
    },
    "after_ledger_raw_sha256": digest(after_raw),
    "old_raw_prefix_preserved_exactly": True,
    "foreign_raw_record_bytes_before_sha256": digest(foreign_before),
    "foreign_raw_record_bytes_after_sha256": digest(foreign_after),
    "all_foreign_raw_bytes_and_projected_states_preserved": True,
    "foreign_projected_state_count": len(foreign_ids),
    "old_affinity_two_VERIFIED_states_preserved": {k: {"state": after_states[k]["state"], "owner_id": after_states[k]["owner_id"], "last_actor": after_states[k]["last_actor"]} for k in old_affinity_ids},
    "primary_proving_owner_unchanged": after_states[PRIMARY]["owner_id"],
    "primary_state_after": after_states[PRIMARY]["state"],
    "single_stabilization_lane_after": [],
    "frontier_stage_evidence_only_changed_cell": CELL,
    "frontier_before_raw_sha256": digest(cell_raw), "frontier_after_raw_sha256": file_hash(CELL),
    "all_other_frontier_hashes_unchanged": {p: v for p, v in frontier_before.items() if p != CELL},
    "protected_Lean_Test_root_Registry_lesson_publication_audit_and_other_input_count": len(protected),
    "all_protected_input_bytes_unchanged": True,
    "protected_inputs_manifest": str((OUT / "local-integration-parking.protected-inputs.json").relative_to(ROOT)),
    "actual_current_source_digest_after": astis_site.source_digest(),
    "normal_API_output_log_raw_sha256": file_hash(str((OUT / "local-integration-parking.normal-api.log").relative_to(ROOT))),
    "frontier_stage_evidence_diff_raw_sha256": digest(diff),
    "frontier_status": "independently_verified (unchanged)",
    "local_acceptance_scope": evidence["local_acceptance_scope"],
    "remote_push_Bench_retry_PR384_PR385_action": False,
    "MERGED_PURIFIED_ExpositionSeal_or_Goal_status_events": 0,
    "remaining_and_reclaim_rule": evidence["reclaim_rule"]
}
from tools.astis_frontier_cells import cell_paths
checker_paths = cell_paths()
checker_names = {p.name for p in checker_paths}
receipt["frontier_count_scope"] = {
    "directory_JSON_files_actually_enumerated": len(frontiers),
    "directory_JSON_files_other_than_owned_actually_preserved": len(frontiers) - 1,
    "checker_cell_paths_actually_enumerated": len(checker_paths),
    "other_checker_registered_cell_paths_preserved": len(checker_paths) - 1,
    "checker_excluded_filename_records_also_preserved": sorted(p.name for p in frontiers if p.name not in checker_names),
    "source_of_count_difference": "The protection manifest includes underscore/schema filenames excluded by tools.astis_frontier_cells.cell_paths; semantic audits are another inventory."
}
receipt_path = OUT / "local-integration-parking-receipt.json"
receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"normal_API_success": True, "primary_after": "VERIFIED", "single_lane_after": [],
    "new_append_events": 1, "source_verdict_created": False,
    "other_frontiers_preserved": len(frontiers) - 1,
    "protected_inputs_preserved": len(protected),
    "parking_receipt": str(receipt_path.relative_to(ROOT)),
    "parking_receipt_raw_sha256": digest(receipt_path.read_bytes()),
    "updated_frontier_raw_sha256": file_hash(CELL)}))
