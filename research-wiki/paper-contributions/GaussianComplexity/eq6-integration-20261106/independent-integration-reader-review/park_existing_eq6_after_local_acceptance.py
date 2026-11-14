"""Explicitly authorized normal-API parking; no new source or math verdict."""
from contextlib import redirect_stdout, redirect_stderr
from datetime import datetime, timezone
import difflib
import gzip
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent
CAPSULE = OUT.parent
sys.path.insert(0, str(ROOT))
from tools import astis_advance
from tools.astis_frontier_cells import cell_paths
sys.path.insert(0, str(ROOT / "tools"))
import astis_site

ACTOR = "/root/affinity_integration_reader_review"
SAU = "ASTIS-SA-20261106-GaussianComplexityAveragedBlockLaw"
OWNER = "huanjian_gc_20261106_eq6"
INTEGRATOR = "huanjian_gc_20261106_eq6_integration"
SOURCE_ACTOR = "/root/eq6_fresh_source_module_review"
SOURCE = "98cc6c8953d38dd54bc4e4ef7a547fd68a381ac8"
ACCEPTED = "cd572932eea927a49b1d66f5ab3f1686512fd551"
CORE = "2c09c24ff73b42a2555493fc00616d2a0f803a86"
DIGEST = "cab582b90a6e75d58cb57e05d41ef50cef8e625b5ae8786fd3ec75933177c6fd"
CELL = "research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-averaged-block-law.json"
DECL = "AutoSamplingTheory.ExampleCases.GaussianComplexity.AveragedBlockLaw.actual_averaged_block_product"
REVIEW = "research-wiki/paper-contributions/GaussianComplexity/averaged-block-law-semantic-evidence/fresh-source-module-review"
AUDIT = "research-wiki/semantic-roundtrip/audits/huanjian-averaged-block-law.json"
BINDING = "908c5e4bfdd5276ce6be52f2458c3ad4f45e6a8c1e19c62fd11e81e498a15f7e"
FINAL = OUT / "candidate-2c09c24f-independent-final-browser-site-acceptance.json"
FINAL_SHA = "805f08593af87107064c7dd10d7eb57d3e4f6de00929eb84ecc7df189b3c456d"
RECEIPT = OUT / "local-integration-parking-receipt.json"


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def file_hash(path):
    return sha((ROOT / path).read_bytes())


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def read(path):
    return json.loads((ROOT / path).read_text())


def write(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n")


def canonical_hash(obj):
    return sha(json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode())


def pure_states(raw):
    return astis_advance._replay_advances(json.loads(x) for x in raw.splitlines())


assert not RECEIPT.exists(), "Do not replay an already completed parking operation"
assert git("rev-parse", "HEAD").decode().strip() == CORE
assert astis_site.source_digest() == DIGEST
assert sha(FINAL.read_bytes()) == FINAL_SHA
ledger = ROOT / "runs/substantive_advances.jsonl"
before = ledger.read_bytes()
assert before == git("show", f"{CORE}:runs/substantive_advances.jsonl")
states = pure_states(before)
assert states[SAU]["state"] == "STABILIZING"
assert states[SAU]["owner_id"] == OWNER
assert states[SAU]["latest_evidence"]["integration_owner"] == INTEGRATOR
assert [k for k, v in states.items() if v["state"] == "STABILIZING"] == [SAU]
foreign = set(states) - {SAU}
old_ids = ["ASTIS-SA-20261106-GaussianComplexityConditionalBlockLaw",
           "ASTIS-SA-20261106-GaussianComplexitySingleBlockAffinity",
           "ASTIS-SA-20261106-NormalizedDensityAffinity"]
assert all(states[k]["state"] == "VERIFIED" for k in old_ids)
original = [json.loads(x) for x in before.splitlines()
            if json.loads(x).get("advance_id") == SAU and json.loads(x).get("to_state") == "VERIFIED"]
assert len(original) == 1 and original[0]["worker_id"] == SOURCE_ACTOR
original = original[0]
assert original["evidence"]["verified_commit"] == SOURCE
for record in [original["evidence"]["fake_closure_scan"]["report"],
               original["evidence"]["fake_closure_scan"]["axiom_evidence"]]:
    assert file_hash(record["path"]) == record["physical_raw_sha256"]
assert file_hash(f"{REVIEW}/verified-transition-summary.json") == "7c2fe73e1bf6175ef7b1b3145ae21fe42d3c46677d07e590c53de7350e7922fd"
assert file_hash(f"{REVIEW}/verified-normal-api.receipt.json") == "3112a82ec1dd2425c2c4dba634ecb51af18f538d19389143c5f0631a6cb3b5c4"
original_append = (ROOT / REVIEW / "verified-ledger.exact-append.RAW.jsonl").read_bytes()
assert sha(original_append) == "45eee83c108db95649dbf60e28f28a96f7ae73ad225f02f5ea19bb5750b77093"
assert original_append in before
audit = read(AUDIT)
assert audit["state"] == "source-reviewed" and audit["source_review"]["state"] == "accepted"
assert audit["publication_binding_sha256"] == BINDING
assert file_hash(AUDIT) == "7f96a0c943f73010c9ef75b19070394a6037f80d769db52e66ab0ed09f1377da"
assert (ROOT / AUDIT).read_bytes() == git("show", f"{ACCEPTED}:{AUDIT}")
for path in ["AutoSamplingTheory/ExampleCases/GaussianComplexity/AveragedBlockLaw.lean",
             "Tests/GaussianComplexityAveragedBlockLaw.lean",
             "website/content/declaration_lessons/huanjian-averaged-block-law.json",
             "website/content/publications/huanjian-averaged-block-law.json"]:
    assert (ROOT / path).read_bytes() == git("show", f"{SOURCE}:{path}")

# Preserve the bounded proof/source/queue surface; do not scan 4.5GB of unrelated
# tracked fixture material. Extend the established 3556-input protection set.
guard_paths = set(read(str((OUT / "projection-protected-inputs.json").relative_to(ROOT))))
guard_paths.update(git("ls-files", "*.lean").decode().splitlines())
for prefix in ["research-wiki/frontier-cells", "research-wiki/semantic-roundtrip/audits",
               REVIEW, "website/content/declaration_lessons", "website/content/publications",
               ".github/workflows", "tools", "benchmarks/samplingoptimisationgeometrybench/harbor"]:
    guard_paths.update(git("ls-files", prefix).decode().splitlines())
guard_paths.update([AUDIT, "runs/substantive_discoveries.jsonl", "AutoSamplingTheory.lean",
                    "Tests.lean", "Tests/Basic.lean", "AutoSamplingTheory/TechnicalLemmas/Registry.lean",
                    "lake-manifest.json", "lean-toolchain", "lakefile.lean",
                    "website/content/samplewiki_companion_frontiers.json"])
guard_paths.discard(CELL)
guard_paths.discard("runs/substantive_advances.jsonl")
concurrent_owned_metadata = {"README.md", "research-wiki/paper-contributions/GaussianComplexity/README.md"}
guard_paths -= concurrent_owned_metadata
protected = {p: file_hash(p) for p in sorted(guard_paths) if (ROOT / p).is_file()}
frontiers = sorted((ROOT / "research-wiki/frontier-cells").glob("*.json"))
frontier_before = {str(p.relative_to(ROOT)): sha(p.read_bytes()) for p in frontiers}
checker_paths = cell_paths()
assert ROOT / CELL in [p.resolve() for p in checker_paths]
counts = {
    "directory_JSON_files": len(frontiers),
    "other_directory_JSON_files": len(frontiers) - 1,
    "registered_cell_paths": len(checker_paths),
    "other_registered_cell_paths": len(checker_paths) - 1,
    "excluded_template_filenames": sorted(p.name for p in frontiers if p.name not in {q.name for q in checker_paths}),
    "meaning": "Protection inventories only; semantic-audit inventory is a different set."
}
assert counts["directory_JSON_files"] == 435 and counts["registered_cell_paths"] == 432
cell_raw = (ROOT / CELL).read_bytes()
cell = json.loads(cell_raw)
assert cell["status"] == "independently_verified"
tracked_before = set(git("diff", "--name-only").decode().splitlines())

# Save exact raw prefix BEFORE calling the normal API. Never rewrite ledger bytes.
archive = OUT / "before-parking-ledger-prefix.raw.jsonl.gz"
archive.write_bytes(gzip.compress(before, mtime=0))
assert gzip.decompress(archive.read_bytes()) == before
prefix_manifest = {
    "immutable_core_commit": CORE,
    "git_blob": git("rev-parse", f"{CORE}:runs/substantive_advances.jsonl").decode().strip(),
    "raw_prefix_sha256": sha(before), "raw_prefix_bytes": len(before),
    "archive": str(archive.relative_to(ROOT)), "archive_sha256": sha(archive.read_bytes()),
    "lossless_decompression_equals_entire_raw_ledger_and_core_git_blob": True
}
write(OUT / "before-parking-ledger-prefix-manifest.json", prefix_manifest)
(OUT / "frontier.before-local-integration-parking.json").write_bytes(cell_raw)
write(OUT / "local-integration-parking.protected-inputs.json", protected)
write(OUT / "local-integration-parking.foreign-state-hashes.before.json",
      {k: canonical_hash(states[k]) for k in sorted(foreign)})

evidence = {
    "parking_kind": "mechanical-existing-verification-parking-after-local-root-reader-acceptance",
    "verifier_id": ACTOR, "verified_commit": CORE,
    "original_source_verified_commit": SOURCE, "original_source_verifier_id": SOURCE_ACTOR,
    "new_mathematical_source_or_semantic_verdict": False,
    "authorization": "Current integration owner explicitly authorized this sole primary STABILIZING->existing VERIFIED parking after independently accepted local2c09 root/site/graph/14PNG reader QA; release the unique local integration lease, preserving the proof owner.",
    "gate": {
        "kind": "reuse-actual2c09-root9640-and-independent-local-reader-acceptance",
        "actual_core_commit": CORE, "actual_source_digest": DIGEST,
        "actual_root_record": str((CAPSULE / "actual-root-gate-at-core-commit.json").relative_to(ROOT)),
        "actual_root_raw_sha256": "2176d605fb0be8c2652ec326b8d2bb3d92b5020688fc7e0d1161a277ea3d6b28",
        "independent_final_local_reader_report": str(FINAL.relative_to(ROOT)),
        "independent_final_local_reader_report_raw_sha256": FINAL_SHA,
        "normal_reviewed_publication_gate": "Normal API validates this exact unchanged declaration with reviewed=True; this is not a new source review."
    },
    "source_audit": {
        "kind": "reuse-existing-fresh-independent-source-whole-module-static-reader-verdict",
        "original_reviewer": SOURCE_ACTOR, "original_source_commit": SOURCE,
        "original_summary": f"{REVIEW}/verified-transition-summary.json",
        "original_summary_raw_sha256": "7c2fe73e1bf6175ef7b1b3145ae21fe42d3c46677d07e590c53de7350e7922fd",
        "accepted_audit": AUDIT, "accepted_audit_raw_sha256": file_hash(AUDIT),
        "accepted_metadata_commit": ACCEPTED, "current_publication_binding_sha256": BINDING,
        "source_Test_lesson_publication_bytes_equal98cc": True,
        "accepted_audit_bytes_equal_cd572_not98cc_draft": True, "new_source_verdict": False
    },
    "fake_closure_scan": {
        "kind": "reuse-existing-fresh-exact-wholemodule-report-and-actual-root-ASTIS-success",
        "original_reviewer": SOURCE_ACTOR,
        "existing_exact_report": original["evidence"]["fake_closure_scan"]["report"],
        "existing_axiom_record": original["evidence"]["fake_closure_scan"]["axiom_evidence"],
        "actual_current_source_bytes_unchanged": True, "actual_root_ASTIS_success_at": CORE,
        "new_scan_or_source_verdict_fabricated": False
    },
    "publication_declarations": [DECL],
    "released_integration_owner": INTEGRATOR, "proving_owner_preserved": OWNER,
    "canonical_branch_preserved": "huanjian/gaussian-averaged-block-law-integration-20261106",
    "local_acceptance_scope": "Actual common-sign prior-averaged Eq6 law, probabilities, AE-positive support and actual mixture/residual marginal consumers; local root9640/Registry612/site/graph/14PNG1440/390 accepted. Full product densities, tensorized affinity and amplification are separate.",
    "source_link_boundary": "Actual own-site full module/download and2c09 sourceDigest binding only. public_source_links=false; the script GitHub URL conditional branch was NOT executed. Generic immutable_source_link true is not external HTML/HTTP200 evidence; historical504 route remains frozen.",
    "chronology": "Root/site/graph actually ran0751-0757UTC; browser actually ran1312UTC after sandbox approval, all at same2c09/digest. No relabeling or extra build claimed.",
    "external_hold": "Old PR385 remains5a OPEN with unchanged Bench native wall-limit. No push/retry/cap change/foreignPR384 or385 action, merge or deploy.",
    "reclaim_rule": "A later authorized normal API STABILIZING claim is required before further serialized shared integration/actual remote delivery.",
    "truth_boundary": "Original fresh98cc mathematical/source verdict is reused. Ex70 product density, Ex71 affinity tensorization, Ex72 amplifiedTV, oracle/transcript/TVprecision/deterministiccaps/expectedcost/hiddeneigenbasis and both main bounds remain open. Remote merge/live, postmerge purification/ExpositionSeal and whole Goal remain incomplete. No M/P/Seal/Goal event."
}
write(OUT / "local-integration-parking.request.json", evidence)
api_started = datetime.now(timezone.utc).isoformat()
captured = io.StringIO()
with redirect_stdout(captured), redirect_stderr(captured):
    astis_advance.transition_advance(SAU, "VERIFIED", worker_id=ACTOR,
        modes=["mechanical-existing-verification-parking", "release-local-integration-lease-after-local-acceptance"],
        evidence=evidence)
api_finished = datetime.now(timezone.utc).isoformat()
(OUT / "local-integration-parking.normal-api.log").write_text(captured.getvalue())

after = ledger.read_bytes()
assert after.startswith(before)
append = after[len(before):]
assert len(append.splitlines()) == 1
event = json.loads(append)
assert event["advance_id"] == SAU and event["worker_id"] == ACTOR
assert event["from_state"] == "STABILIZING" and event["to_state"] == "VERIFIED"
(OUT / "local-integration-parking.exact-append.jsonl").write_bytes(append)
after_states = pure_states(after)
assert set(after_states) == set(states)
assert all(states[k] == after_states[k] for k in foreign)
assert after_states[SAU]["owner_id"] == OWNER
assert all(states[k] == after_states[k] for k in old_ids)
assert not any(v["state"] == "STABILIZING" for v in after_states.values())
foreign_raw_before = b"".join(x for x in before.splitlines(keepends=True) if json.loads(x).get("advance_id") != SAU)
foreign_raw_after = b"".join(x for x in after.splitlines(keepends=True) if json.loads(x).get("advance_id") != SAU)
assert foreign_raw_before == foreign_raw_after
write(OUT / "local-integration-parking.foreign-state-hashes.after.json",
      {k: canonical_hash(after_states[k]) for k in sorted(foreign)})

# Preserve exact former pending strings before projecting ONLY the current stage.
cell["historical_local_integration_checkpoints"] = {
    "recorded_by": ACTOR,
    "meaning": "Exact prior pending stage wording; original preproof/projection history remains separately untouched.",
    "source_detail_audit.gap": cell["source_detail_audit"]["gap"],
    "source_detail_audit.fidelity_boundary": cell["source_detail_audit"]["fidelity_boundary"],
    "evidence.execution_boundary": cell["evidence"]["execution_boundary"],
    "evidence.existing_verification_projection.remaining": cell["evidence"]["existing_verification_projection"]["remaining"],
    "graph_contribution.visual_review": cell["graph_contribution"]["visual_review"],
    "graph_contribution.reason": cell["graph_contribution"]["reason"]
}
cell["source_detail_audit"]["gap"] = "The printed Eq6 actual common-sign prior-averaged joint law, probabilities/AE-positive support and real all-parameter mixture/residual marginal consumers retain the actual fresh independent source/whole-module/parent/static-reader verdict at98cc. Source-omitted averaging/measurable-family/matrix transport bridges are internal proved producers. Actual local2c09 root9640, Registry612, generated site/graph and real Chrome1440/390 with14 independently viewed PNGs are accepted. Remote merge/live delivery, postmerge purification/ExpositionSeal, Ex70/71/72 and both main bounds remain pending."
cell["source_detail_audit"]["fidelity_boundary"] = "The bounded actual common-sign prior-averaged Eq6 is independently source-accepted at98cc and locally integrated/read at2c09. Source/Test/lesson/publication/sealed interface are exact98cc; accepted source-reviewed audit is a post98cc successor, exactcd572 bytes. Full own-site module/download bytes are exact. GitHub URL conditional branch was not executed because public source links are false; no external HTML/HTTP200 accepted. Ex70 product density, Ex71 affinity, Ex72 amplifiedTV, oracle/precision/caps/cost/hiddenbasis, both main lower bounds and remote merge/live/PURIFIED/ExpositionSeal/whole Goal remain separate pending obligations."
cell["evidence"]["execution_boundary"] = "Original mathematical/source verdict remains fresh independent reviewer /root/eq6_fresh_source_module_review at98cc; precommit focused ff7 and actual fresh98cc checks retain their real heads. Actual local2c09 canonical root9640/sourceDigestcab582b9, Registry612, site build/check, graph and14 real Chrome PNG1440/390 are independently accepted by /root/affinity_integration_reader_review. Root/site/graph ran0751-0757UTC; browser ran1312UTC after approval, sameHEAD/digest. The normal API mechanically parks this sole local lease back to existing VERIFIED, preserving proof owner and foreign queues. No new source verdict, remote/public merge/live, purification, Seal or Goal completion."
cell["evidence"]["existing_verification_projection"]["remaining"] = "Original projection stays historical. Local2c09 root/Registry/site/graph/realChrome acceptance is now separately evidenced; remote merge/live, postmerge purification/ExpositionSeal and Ex70/71/72/main/oracle/cost obligations remain pending."
cell["graph_contribution"]["visual_review"] = "Actual2c09 local graph and reader accepted by /root/affinity_integration_reader_review, final reportSHA805f0859:14 actualChromePNG,1440/390, one canonical averaged node plus old conditional real consumer, solid module structure and dashed incomplete scanner/source/fidelity overlays. No exhaustive formal dependency certificate or external live acceptance inferred."
cell["graph_contribution"]["reason"] = "The sole unchanged averaged theorem is in canonical root/Test imports and one Registry entry; the old conditional entry/card names its genuine production consumer. Local2c09 site/graph/reader acceptance is complete; source/scanner overlays do not become formal implications or main-bound completion."
cell["evidence"]["local_integration_acceptance"] = {
    "reviewer": ACTOR, "core_commit": CORE, "source_digest": DIGEST,
    "canonical_root_jobs": 9640,
    "root_raw_log_sha256": "2176d605fb0be8c2652ec326b8d2bb3d92b5020688fc7e0d1161a277ea3d6b28",
    "site_check_raw_log_sha256": "e4fdd24798e688b5d86828580a319d0a67b079f7f804a4a8c2a50fb9113150c9",
    "graph_check_raw_log_sha256": "2908fa0195127ff07b9affad31a56a401aa787429052d654c5eae10f87c5f83f",
    "browser_raw_report_sha256": "b716b94fe0901b87bfdb82e74113f2c1c417d1e2e3686561eadb2bbe62fc958f",
    "actual_pngs_independently_viewed": 14, "viewports": [1440, 390],
    "independent_final_report": str(FINAL.relative_to(ROOT)), "independent_final_report_sha256": FINAL_SHA,
    "full_module_download_source_bytes": 10943,
    "source_link_scope": evidence["source_link_boundary"], "timing": evidence["chronology"],
    "remote_merge_live_PURIFIED_ExpositionSeal": "not certified", "new_source_verdict": False
}
cell["evidence"]["local_integration_lease_parking"] = {
    "actor": ACTOR, "kind": evidence["parking_kind"],
    "normal_API": "tools.astis_advance.transition_advance",
    "from_state": "STABILIZING", "to_state": "VERIFIED",
    "new_source_verdict": False, "proving_owner_preserved": OWNER,
    "single_stabilization_lane_after": [],
    "receipt": str(RECEIPT.relative_to(ROOT)), "exact_append_raw_sha256": sha(append),
    "remaining": evidence["truth_boundary"]
}
assert cell["status"] == "independently_verified"
(ROOT / CELL).write_text(json.dumps(cell, ensure_ascii=False, indent=2) + "\n")

assert all(file_hash(p) == h for p, h in protected.items())
frontier_after = {str(p.relative_to(ROOT)): sha(p.read_bytes()) for p in frontiers}
assert [p for p in frontier_before if frontier_before[p] != frontier_after[p]] == [CELL]
assert astis_site.source_digest() == DIGEST
tracked_after = set(git("diff", "--name-only").decode().splitlines())
unexpected = tracked_after - tracked_before - {CELL, "runs/substantive_advances.jsonl"} - concurrent_owned_metadata
unexpected = {p for p in unexpected if not p.startswith(str(CAPSULE.relative_to(ROOT)) + "/")}
assert not unexpected, unexpected
diff = "".join(difflib.unified_diff(cell_raw.decode().splitlines(keepends=True),
    (ROOT / CELL).read_text().splitlines(keepends=True), fromfile=CELL+":before", tofile=CELL+":after"))
(OUT / "local-integration-parking.frontier-stage-evidence.diff").write_text(diff)
protected_report = {
    "all_protected_input_hashes_unchanged": True, "protected_input_count": len(protected),
    "manifest": str((OUT / "local-integration-parking.protected-inputs.json").relative_to(ROOT)),
    "manifest_sha256": file_hash(str((OUT / "local-integration-parking.protected-inputs.json").relative_to(ROOT))),
    "frontier_count_scope": counts,
    "all_other_frontier_hashes_unchanged": {p: h for p, h in frontier_before.items() if p != CELL},
    "declared_concurrent_root_owned_metadata_excluded": sorted(concurrent_owned_metadata) + [str(CAPSULE.relative_to(ROOT)) + "/**"],
    "unexpected_tracked_changes": []
}
write(OUT / "protected-inputs.before-after-identical.json", protected_report)
receipt = {
    "schema": "astis-independent-existing-verification-local-integration-parking/v1",
    "actor": ACTOR, "api": "tools.astis_advance.transition_advance",
    "api_started_at_utc": api_started, "api_finished_at_utc": api_finished,
    "script_sha256": sha(Path(__file__).read_bytes()), "actual_candidate": CORE,
    "operation": "STABILIZING->existing VERIFIED; sole local integration lease released through normal API",
    "normal_API_reviewed_publication_gate_passed": True,
    "new_source_mathematical_or_semantic_verdict": False,
    "original_source_verifier": SOURCE_ACTOR, "original_source_commit": SOURCE,
    "original_independent_VERIFIED_append_preserved_sha256": sha(original_append),
    "accepted_audit_baseline": ACCEPTED, "source_binding": BINDING,
    "saved_exact_raw_prefix": prefix_manifest,
    "exact_append": {"path": str((OUT / "local-integration-parking.exact-append.jsonl").relative_to(ROOT)),
        "raw_sha256": sha(append), "bytes": len(append), "events": 1,
        "actor": ACTOR, "from_state": "STABILIZING", "to_state": "VERIFIED"},
    "after_ledger_raw_sha256": sha(after), "old_raw_prefix_preserved_exactly": True,
    "foreign_raw_record_bytes_before_sha256": sha(foreign_raw_before),
    "foreign_raw_record_bytes_after_sha256": sha(foreign_raw_after),
    "foreign_projected_state_count": len(foreign),
    "all_foreign_raw_bytes_and_projected_states_preserved": True,
    "old_conditional_and_two_affinity_VERIFIED_states_preserved": {
        k: {"state": after_states[k]["state"], "owner_id": after_states[k]["owner_id"],
            "last_actor": after_states[k]["last_actor"]} for k in old_ids},
    "primary_proving_owner_unchanged": after_states[SAU]["owner_id"],
    "primary_state_after": after_states[SAU]["state"], "single_stabilization_lane_after": [],
    "frontier_status": "independently_verified (unchanged)",
    "frontier_stage_evidence_only_changed_cell": CELL,
    "frontier_before_sha256": sha(cell_raw), "frontier_after_sha256": file_hash(CELL),
    "frontier_stage_evidence_diff_sha256": sha(diff.encode()),
    "protected_input_count": len(protected), "all_protected_input_bytes_unchanged": True,
    "protection_report": str((OUT / "protected-inputs.before-after-identical.json").relative_to(ROOT)),
    "protection_report_sha256": sha((OUT / "protected-inputs.before-after-identical.json").read_bytes()),
    "frontier_count_scope": counts, "source_digest_after": astis_site.source_digest(),
    "normal_API_output_log_sha256": sha((OUT / "local-integration-parking.normal-api.log").read_bytes()),
    "local_final_reader_report_sha256": FINAL_SHA,
    "external_HTML_and_live_boundary": evidence["source_link_boundary"],
    "no_push_Bench_retry_foreign_PR_action": True,
    "MERGED_PURIFIED_ExpositionSeal_or_Goal_status_events": 0,
    "remaining": evidence["truth_boundary"], "reclaim_rule": evidence["reclaim_rule"]
}
write(RECEIPT, receipt)
write(OUT / "local-integration-release-summary.json", {
    "actor": ACTOR, "result": "NORMAL_API_PARKED_EXISTING_VERIFIED_AND_RELEASED_LOCAL_LANE",
    "receipt": str(RECEIPT.relative_to(ROOT)), "receipt_sha256": sha(RECEIPT.read_bytes()),
    "exact_append_sha256": sha(append), "all_foreign_projected_states_preserved": len(foreign),
    "protected_input_count": len(protected), "frontier_count_scope": counts,
    "primary_state_after": "VERIFIED", "frontier_status_after": "independently_verified",
    "proving_owner": OWNER, "single_stabilization_lane_after": [],
    "old_source_verdict_actor_commit": SOURCE_ACTOR + "@" + SOURCE,
    "local_integration_acceptance_commit": CORE, "new_source_verdict": False,
    "remaining": evidence["truth_boundary"], "no_further_writes_planned_by_this_actor": True
})
print(json.dumps({"normal_API_success": True, "primary_after": "VERIFIED", "single_lane_after": [],
    "new_append_events": 1, "source_verdict_created": False, "foreign_states_preserved": len(foreign),
    "protected_inputs_preserved": len(protected), "frontier_counts": counts,
    "receipt_sha256": sha(RECEIPT.read_bytes()), "frontier_sha256": file_hash(CELL),
    "release_summary_sha256": sha((OUT / "local-integration-release-summary.json").read_bytes())}))
