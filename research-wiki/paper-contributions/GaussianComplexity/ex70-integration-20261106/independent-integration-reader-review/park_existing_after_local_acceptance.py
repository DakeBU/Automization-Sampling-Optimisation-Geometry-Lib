"""One authorized normal-API lease release; retain the existing source verdict."""
from contextlib import redirect_stdout, redirect_stderr
from datetime import datetime, timezone
import copy
import difflib
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT))
from tools import astis_advance as advance
sys.path.insert(0, str(ROOT / "tools"))
import astis_site

ACTOR = "/root/ex70_integration_reader_review"
SOURCE_ACTOR = "/root/ex70_fresh_source_module_review"
SAU = "ASTIS-SA-20261106-GaussianComplexityProductDensity"
OWNER = "huanjian_gc_20261106_ex70"
INTEGRATOR = "huanjian_gc_20261106_ex70_integration"
SOURCE = "a83254ef00c8e6fd0548a25fae03f07e2a82e2b7"
ACCEPTED = "a1196bf6ad741a261ebc70db4c5193a00b64662e"
CORE = "e566930dccfa74a50fd86b743a3b8eddda21798b"
DIGEST = "5a2978a955ea15d1c1de0cec1c4d201b9d005040ae8018be6d8068b4de04583d"
CELL = "research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-product-density.json"
DECL = "AutoSamplingTheory.ExampleCases.GaussianComplexity.ProductDensity.actual_product_density"
INTEGRATION = "research-wiki/paper-contributions/GaussianComplexity/ex70-integration-20261106/"
REVIEW = "research-wiki/paper-contributions/GaussianComplexity/product-density-semantic-evidence/fresh-source-module-review/"
AUDIT = "research-wiki/semantic-roundtrip/audits/huanjian-product-density.json"
BINDING = "f764e7b080de73ded904fb5a89d6424878a1b2c2b292ca9648d70ed3ce19eca8"
FINAL = OUT / "candidate-e566930d-independent-final-browser-site-acceptance.json"
FINAL_SHA = "9d9ed225770c8271a5eb1c52fc0107241f47ef6eb5607f047b0317d2c26769c9"
RECEIPT = OUT / "local-integration-parking-receipt.json"


def sha(raw): return hashlib.sha256(raw).hexdigest()
def canon(value): return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()
def git(*args): return subprocess.check_output(["git", *args], cwd=ROOT)
def raw(rel): return (ROOT / rel).read_bytes()
def read(rel): return json.loads(raw(rel))
def write(name, value): (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")
def states(raw_ledger): return advance._replay_advances(json.loads(line) for line in raw_ledger.splitlines() if line.strip())
def archive(name, content):
    path = OUT / name
    path.write_bytes(gzip.compress(content, mtime=0))
    assert gzip.decompress(path.read_bytes()) == content
    return {"path": str(path.relative_to(ROOT)), "raw_sha256": sha(content), "raw_bytes": len(content),
            "gzip_sha256": sha(path.read_bytes()), "gzip_bytes": path.stat().st_size, "lossless_verified": True}


assert not RECEIPT.exists(), "Do not repeat a completed parking operation"
assert git("rev-parse", "HEAD").decode().strip() == CORE
assert astis_site.source_digest() == DIGEST and sha(FINAL.read_bytes()) == FINAL_SHA
final = json.loads(FINAL.read_text())
assert final["status"] == "ACCEPTED_LOCAL_INTEGRATION_AND_READER" and not final["blocking_findings"]
assert final["actual_pngs_individually_viewed"] == 14
ledger_path = ROOT / "runs/substantive_advances.jsonl"
before = ledger_path.read_bytes()
assert sha(before) == "108d5df92553290d2408c0d24b94d1ed30cebfbc2b265b8379bbc1d060f6af2d"
assert before == git("show", CORE + ":runs/substantive_advances.jsonl") and before.endswith(b"\n")
old_states = states(before)
assert old_states[SAU]["state"] == "STABILIZING" and old_states[SAU]["owner_id"] == OWNER
assert old_states[SAU]["latest_evidence"]["integration_owner"] == INTEGRATOR
assert [key for key, value in old_states.items() if value.get("state") == "STABILIZING"] == [SAU]
foreign = {key: value for key, value in old_states.items() if key != SAU}
assert len(foreign) == 276
baseline_foreign_hashes = read(str((OUT / "baseline-projected-state-hashes.json").relative_to(ROOT)))
assert all(sha(canon(value)) == baseline_foreign_hashes[key] for key, value in foreign.items())
source_events = [json.loads(line) for line in before.splitlines()
                 if json.loads(line).get("advance_id") == SAU and json.loads(line).get("to_state") == "VERIFIED"]
assert len(source_events) == 1
source_event = source_events[0]
assert source_event["worker_id"] == SOURCE_ACTOR and source_event["evidence"]["verified_commit"] == SOURCE
source_append = raw(REVIEW + "verified-append.jsonl")
assert sha(source_append) == "13ba874ba13ad21ca492434add72b0025fd98aeb97df9e00f858ab49fea6cc84" and source_append in before
assert sha(raw(REVIEW + "normal-api-verified-transition.receipt.json")) == "685ce47914735fd4f888cc07466bb71ae60a6e54072a7e9ead6f63f477f183c0"
pins = {
    "AutoSamplingTheory/ExampleCases/GaussianComplexity/ProductDensity.lean": "a75340883fb065e782a802f6dc8184f52d25fa96930e681d89dfc97fe87bd228",
    "Tests/GaussianComplexityProductDensity.lean": "ad9d4fa4048a2fb88b5eaade4a7bc202f05e0a4b48a13790893f8cc768fbfccd",
    "website/content/declaration_lessons/huanjian-product-density.json": "cf00807161ee7aabf1a9675e25e513bf88c2ae4e7912456953a9f1eec0bf9cd3",
    "website/content/publications/huanjian-product-density.json": "67a09acc094e5fb6023c53e13202e634324b7747f20e568da878c291782c46ac",
    AUDIT: "91a0565ed2da64800cf3ff0f1bc5169c9d0e54e643ba892a1d81284b30644332"
}
assert all(sha(raw(rel)) == expected for rel, expected in pins.items())
assert all(raw(rel) == git("show", SOURCE + ":" + rel) for rel in pins if rel != AUDIT)
assert raw(AUDIT) == git("show", ACCEPTED + ":" + AUDIT)
audit = read(AUDIT)
assert audit["state"] == "source-reviewed" and audit["source_review"]["state"] == "accepted"
assert audit["publication_binding_sha256"] == BINDING
assert json.loads(git("show", SOURCE + ":" + AUDIT))["state"] == "blind-reconstructed"
initial = read("research-wiki/paper-contributions/GaussianComplexity/product-density-semantic-evidence/initial-environment-queue-protection.json")
assert sha(raw(initial["source"])) == initial["source_sha256"]
snapshot = initial["lossless_raw_snapshot"]
assert sha(raw(snapshot["path"])) == snapshot["gzip_sha256"]
assert sha(gzip.decompress(raw(snapshot["path"]))) == snapshot["uncompressed_sha256"]

# Bounded extension of the inherited 3680-input surface, without rereading
# gigabytes of unrelated tracked fixtures. Every old frontier/queue is covered.
guards = set(read(str((OUT / "baseline-protected-input-hashes.json").relative_to(ROOT))))
guards.update(git("ls-files", "*.lean").decode().splitlines())
for prefix in ["research-wiki/frontier-cells", "research-wiki/semantic-roundtrip/audits", REVIEW,
               "website/content/declaration_lessons", "website/content/publications", ".github/workflows", "tools",
               "benchmarks/samplingoptimisationgeometrybench/harbor", INTEGRATION]:
    guards.update(git("ls-files", prefix).decode().splitlines())
guards.update(pins)
guards.update(["runs/substantive_discoveries.jsonl", "lakefile.lean", "lean-toolchain", "lake-manifest.json",
               "README.md", "research-wiki/paper-contributions/GaussianComplexity/README.md",
               ".astis/site-lean-gate.json", initial["source"], snapshot["path"],
               "_site/data/build-metadata.json", "_site/data/underlying-lean-graph.json",
               str(FINAL.relative_to(ROOT)), INTEGRATION + "actual-root-gate-at-core-commit.json",
               INTEGRATION + "final-browser/artifact-manifest.json",
               INTEGRATION + "local-integration-acceptance.json",
               INTEGRATION + "candidate-audit-state-clarification.json"])
guards.update(INTEGRATION + "final-browser/" + entry["file"]
              for entry in read(INTEGRATION + "final-browser/artifact-manifest.json")["artifacts"])
guards.discard(CELL)
guards.discard("runs/substantive_advances.jsonl")
protected = {rel: sha(raw(rel)) for rel in sorted(guards) if (ROOT / rel).is_file()}
frontiers = {str(path.relative_to(ROOT)): sha(path.read_bytes())
             for path in sorted((ROOT / "research-wiki/frontier-cells").glob("*.json"))}
assert len(frontiers) == 436
old_frontiers = read(str((OUT / "baseline-old-frontier-hashes.json").relative_to(ROOT)))
assert len(old_frontiers) == 435 and all(frontiers[rel] == expected for rel, expected in old_frontiers.items())
cell_raw = raw(CELL)
cell = json.loads(cell_raw)
assert cell_raw == git("show", CORE + ":" + CELL) and cell["status"] == "independently_verified"
prefix_archive = archive("before-parking-ledger-prefix.raw.jsonl.gz", before)
protected_archive = archive("local-integration-parking.protected-inputs.json.gz", canon(protected))
foreign_archive = archive("local-integration-parking.foreign-states.before.json.gz", canon(foreign))
frontier_archive = archive("local-integration-parking.frontiers.before.json.gz", canon(frontiers))
(OUT / "frontier.before-local-integration-parking.json").write_bytes(cell_raw)
preflight = {"core": CORE, "ledger_sha256": sha(before), "state": "STABILIZING", "owner": OWNER,
             "integration_owner": INTEGRATOR, "single_lane": [SAU], "old_foreign_states": 276,
             "old_frontiers": 435, "current_directory_frontier_JSONs": 436, "protected_inputs": len(protected),
             "archives": {"prefix": prefix_archive, "protected": protected_archive,
                          "foreign": foreign_archive, "frontiers": frontier_archive},
             "source_digest": DIGEST, "final_local_acceptance_sha256": FINAL_SHA,
             "normal_API_calls_planned": 1, "source_verdict_to_create": False}
write("local-integration-parking.preflight.json", preflight)
evidence = {
    "parking_kind": "mechanical-existing-verification-parking-after-local-root-reader-acceptance",
    "verifier_id": ACTOR, "verified_commit": CORE,
    "original_source_verifier_id": SOURCE_ACTOR, "original_source_verified_commit": SOURCE,
    "new_mathematical_source_or_semantic_verdict": False,
    "authorization": "Root explicitly authorized one normal-API release of the sole local STABILIZING lease after accepting independent e566 root/site/graph/14-original-PNG reader QA. Preserve the original source verdict and proof owner.",
    "publication_declarations": [DECL], "released_integration_owner": INTEGRATOR,
    "proving_owner_preserved": OWNER,
    "gate": {"kind": "reuse-actual-e566-root9642-and-independent-reader-acceptance",
             "actual_core_commit": CORE, "actual_source_digest": DIGEST,
             "root_record": INTEGRATION + "actual-root-gate-at-core-commit.json",
             "actual_root_raw_log_sha256": "7af0a68340c7990ef991f8d2327c399823524336e07161967217e2fb86e5c6cd",
             "independent_final_report": str(FINAL.relative_to(ROOT)), "independent_final_report_sha256": FINAL_SHA,
             "scope": "The normal API validates unchanged publication targets with reviewed=True. No repeated Lean/browser run or new source review is asserted."},
    "source_audit": {"kind": "reuse-existing-independent-source-whole-module-verdict", "source_verifier": SOURCE_ACTOR,
                     "source_commit": SOURCE, "original_normal_API_receipt": REVIEW + "normal-api-verified-transition.receipt.json",
                     "original_VERIFIED_append_sha256": sha(source_append), "current_accepted_audit": AUDIT,
                     "current_accepted_audit_sha256": pins[AUDIT], "accepted_metadata_parent": ACCEPTED,
                     "current_publication_binding_sha256": BINDING,
                     "source_Test_lesson_pub_bytes_equal_mathematical_candidate": True,
                     "candidate_audit_state": "blind-reconstructed", "accepted_successor_audit_state": "source-reviewed",
                     "candidate_audit_byte_equal_accepted_successor": False, "new_source_verdict": False},
    "fake_closure_scan": {"kind": "reuse-exact-source-module-scan-and-current-root-ASTIS-success",
                          "existing_source_scan": source_event["evidence"]["fake_closure_scan"],
                          "actual_source_bytes_unchanged": True, "actual_root_ASTIS_success_at": CORE,
                          "new_scan_or_source_verdict_created": False},
    "chronology": "Actual root/build Nov6 15:09/15:12UTC, actual site/graph checks Nov6 15:42UTC; actual Chrome Nov7 03:55UTC after platform approval. Same e566 HEAD/sourceDigest; no relabelled extra build.",
    "source_link_boundary": "Actual own-site complete module/download and immutable e566 Git object checked. Public source links=false; GitHub URL conditional branch=null/not_executed. External GitHub HTML=false; no external HTTP200 claim.",
    "truth_boundary": "Existing source a832 acceptance is preserved. Actual Ex70 local root/Registry/site/graph/14PNG reader acceptance at e566 is complete. Ex71/72, oracle/transcript/precision/deterministic cap/expectedcost/hidden eigenbasis and both main bounds remain open; remote/main/live, postmerge purification/ExpositionSeal and full Goal completion are not certified.",
    "remote_hold": "Old PR385 exact5a OPEN with original-owner frozen native Bench wallcap diagnostic; no unchanged Bench rerun, cap change, new push, PR384 edit, merge/deploy or provider trial.",
    "reclaim_rule": "Any later serialized shared integration or remote delivery requires a new authorized normal-API STABILIZING claim."
}
write("local-integration-parking.request.json", evidence)
assert ledger_path.read_bytes() == before
api_started = datetime.now(timezone.utc).isoformat()
capture = io.StringIO()
try:
    with redirect_stdout(capture), redirect_stderr(capture):
        advance.transition_advance(SAU, "VERIFIED", worker_id=ACTOR,
            modes=["mechanical-existing-verification-parking", "release-local-integration-lease-after-local-acceptance"],
            evidence=evidence)
except Exception as exc:
    (OUT / "local-integration-parking.normal-api.log").write_text(capture.getvalue())
    write("local-integration-parking.API-refusal.json", {"exception": repr(exc), "bypass_attempted": False,
          "ledger_sha256": sha(ledger_path.read_bytes()), "ledger_unchanged": ledger_path.read_bytes() == before})
    raise
api_finished = datetime.now(timezone.utc).isoformat()
(OUT / "local-integration-parking.normal-api.log").write_text(capture.getvalue())
after = ledger_path.read_bytes()
assert after.startswith(before)
append = after[len(before):]
assert len(append.splitlines()) == 1
event = json.loads(append)
assert event["advance_id"] == SAU and event["worker_id"] == ACTOR
assert event["from_state"] == "STABILIZING" and event["to_state"] == "VERIFIED"
(OUT / "local-integration-parking.exact-append.jsonl").write_bytes(append)
after_states = states(after)
assert {key: value for key, value in after_states.items() if key != SAU} == foreign
assert after_states[SAU]["owner_id"] == OWNER and after_states[SAU]["state"] == "VERIFIED"
assert not any(value.get("state") == "STABILIZING" for value in after_states.values())
foreign_raw_before = b"".join(line for line in before.splitlines(keepends=True) if json.loads(line).get("advance_id") != SAU)
foreign_raw_after = b"".join(line for line in after.splitlines(keepends=True) if json.loads(line).get("advance_id") != SAU)
assert foreign_raw_before == foreign_raw_after
assert all(sha(raw(rel)) == expected for rel, expected in protected.items())
assert all(sha(raw(rel)) == expected for rel, expected in frontiers.items())

updated = copy.deepcopy(cell)
updated["evidence"]["historical_preacceptance_integration_stage"] = {
    "execution_boundary": cell["evidence"]["execution_boundary"],
    "current_local_integration": cell["evidence"]["current_local_integration"],
    "graph_visual_review": cell["graph_contribution"]["visual_review"],
    "scope": "Exact former stage wording retained; the existing independent source verdict and all older results stay unchanged."
}
updated["evidence"]["execution_boundary"] = (
    "Existing independent source/whole-module verdict remains /root/ex70_fresh_source_module_review at a832. "
    "Source/Test/lesson/pub equal that candidate; accepted source-reviewed audit is the distinct91a056 successor, "
    "not the candidate blind-reconstructed71e187 audit. Actual e566 root9642/sourceDigest5a2978, Registry613, "
    "final site/graph and real Chrome1440/390 with14 independently viewed original PNGs are accepted. Root/build "
    "were Nov6 15:09/15:12UTC, site/graph15:42UTC, actual Chrome Nov7 03:55UTC after approval, all sameHEAD/digest. "
    "Normal API parks the sole local lease back to existing VERIFIED, retaining proof owner and all foreign queues. "
    "No new source verdict, remote/main/live publication, purification/Seal or Goal completion.")
updated["evidence"]["current_local_integration"].update({
    "state": "VERIFIED", "lease_released": True,
    "acceptance_core_commit": CORE,
    "boundary": "Actual local root/Registry/site/graph/Chrome acceptance completed; normal API releases this sole local lease. Remote/main/live, postmerge purification/Seal and downstream mathematics remain separate."
})
updated["evidence"]["local_integration_acceptance"] = {
    "reviewer": ACTOR, "core_commit": CORE, "source_digest": DIGEST,
    "canonical_root_jobs": 9642, "actual_pngs_individually_viewed": 14, "viewports": [1440, 390],
    "independent_final_report": str(FINAL.relative_to(ROOT)), "independent_final_report_sha256": FINAL_SHA,
    "browser_report_sha256": "11c6faffd25a1e60117ff88d7ae8e8b6653e5cbfc35aac6359ded1f223ffc49d",
    "source_link_scope": evidence["source_link_boundary"], "chronology": evidence["chronology"],
    "new_source_verdict": False, "remote_main_live_PURIFIED_Seal_Goal": "not certified"
}
updated["evidence"]["local_integration_lease_parking"] = {
    "actor": ACTOR, "kind": evidence["parking_kind"], "normal_API": "tools.astis_advance.transition_advance",
    "from_state": "STABILIZING", "to_state": "VERIFIED", "new_source_verdict": False,
    "proving_owner_preserved": OWNER, "released_integration_owner": INTEGRATOR,
    "single_stabilization_lane_after": [], "receipt": str(RECEIPT.relative_to(ROOT)),
    "exact_append_raw_sha256": sha(append), "remaining": evidence["truth_boundary"]
}
updated["graph_contribution"]["visual_review"] = (
    "Actual e566 local graph and reader independently accepted by /root/ex70_integration_reader_review, "
    "final reportSHA9d9ed225:14 actual Chrome originals at1440/390. One canonical Ex70 node and each actual Eq6/mixture "
    "parent once; solid imports/declares are module structure, dashed incomplete name-scan/source/fidelity overlays are "
    "not theorem implications. Mobile local pan/Fit is explicit; no whole-page overflow. No exhaustive formal "
    "dependency certificate, external GitHub HTML, public/remote/main/live or purification acceptance inferred.")
assert {key: value for key, value in updated.items() if key not in {"evidence", "graph_contribution"}} == {
    key: value for key, value in cell.items() if key not in {"evidence", "graph_contribution"}}
assert {key: value for key, value in updated["graph_contribution"].items() if key != "visual_review"} == {
    key: value for key, value in cell["graph_contribution"].items() if key != "visual_review"}
assert updated["evidence"]["existing_verification_projection"] == cell["evidence"]["existing_verification_projection"]
(ROOT / CELL).write_text(json.dumps(updated, ensure_ascii=False, indent=2) + "\n")
assert all(sha(raw(rel)) == expected for rel, expected in protected.items())
assert all(sha(raw(rel)) == expected for rel, expected in old_frontiers.items())
assert astis_site.source_digest() == DIGEST and git("rev-parse", "HEAD").decode().strip() == CORE
diff = "".join(difflib.unified_diff(cell_raw.decode().splitlines(keepends=True), raw(CELL).decode().splitlines(keepends=True),
                                    fromfile=CELL + ":before", tofile=CELL + ":after"))
(OUT / "local-integration-parking.frontier-stage-evidence.diff").write_text(diff)
after_foreign_hashes = {key: sha(canon(value)) for key, value in after_states.items() if key != SAU}
write("local-integration-parking.foreign-state-hashes.after.json", after_foreign_hashes)
result = {
    "schema": "independent-existing-verification-local-integration-parking-v1",
    "actor": ACTOR, "api": "tools.astis_advance.transition_advance", "api_started_utc": api_started,
    "api_finished_utc": api_finished, "normal_API_call_count": 1,
    "normal_API_reviewed_publication_admission_passed": True,
    "operation": "STABILIZING -> existing VERIFIED; release sole local integration lease",
    "core_commit": CORE, "source_digest": DIGEST, "original_source_verifier": SOURCE_ACTOR,
    "original_source_verified_commit": SOURCE, "original_source_VERIFIED_append_sha256": sha(source_append),
    "new_source_mathematical_or_semantic_verdict": False, "proving_owner_preserved": OWNER,
    "released_integration_owner": INTEGRATOR, "target_state_after": "VERIFIED", "single_stabilization_lane_after": [],
    "ledger_before_raw_sha256": sha(before), "ledger_after_raw_sha256": sha(after),
    "ledger_before_bytes": len(before), "ledger_after_bytes": len(after), "exact_old_prefix_preserved": True,
    "saved_lossless_prefix": prefix_archive,
    "exact_append": {"path": str((OUT / "local-integration-parking.exact-append.jsonl").relative_to(ROOT)),
                     "raw_sha256": sha(append), "events": 1, "bytes": len(append),
                     "actor": ACTOR, "from_state": "STABILIZING", "to_state": "VERIFIED"},
    "foreign_projected_states_preserved": 276, "foreign_raw_records_byte_equal": True,
    "foreign_raw_record_sha256": sha(foreign_raw_after), "old_frontier_files_preserved": 435,
    "current_directory_frontier_JSONs": 436, "protected_input_count": len(protected),
    "all_protected_inputs_byte_preserved": True, "protected_archive": protected_archive,
    "frontier_before_raw_sha256": sha(cell_raw), "frontier_after_raw_sha256": sha(raw(CELL)),
    "frontier_changed_only": ["evidence current/history/acceptance/lease projection", "graph_contribution.visual_review"],
    "frontier_status": "independently_verified (unchanged)",
    "frontier_all_other_fields_preserved": True, "frozen_source_graph_and_author_omissions_preserved": True,
    "source_Test_lesson_pub_pins": pins, "source_binding": BINDING,
    "candidate_audit_state": "blind-reconstructed", "accepted_successor_audit_state": "source-reviewed",
    "candidate_and_accepted_audit_byte_equal": False,
    "final_local_acceptance_report_sha256": FINAL_SHA,
    "normal_API_output_log_sha256": sha((OUT / "local-integration-parking.normal-api.log").read_bytes()),
    "script_sha256": sha(Path(__file__).read_bytes()), "remaining": evidence["truth_boundary"],
    "no_push_Bench_rerun_cap_change_PR384_edit_merge_deploy": True,
    "MERGED_PUBLISHED_PURIFIED_Seal_Goal_events": 0,
    "phase_write_status": "All writes complete; stop and leave root to close metadata and continue the next mathematical packet."
}
write(RECEIPT.name, result)
summary = {"status": "NORMAL_API_PARKED_EXISTING_VERIFIED_AND_RELEASED_LOCAL_LANE",
           "receipt": str(RECEIPT.relative_to(ROOT)), "receipt_raw_sha256": sha(RECEIPT.read_bytes()),
           "exact_append_raw_sha256": sha(append), "ledger_after_raw_sha256": sha(after),
           "target_state": "VERIFIED", "single_stabilization_lane": [], "original_proof_owner": OWNER,
           "foreign_states_preserved": 276, "old_frontiers_preserved": 435, "protected_inputs_preserved": len(protected),
           "new_source_verdict": False, "source_verifier": SOURCE_ACTOR, "source_commit": SOURCE,
           "local_integration_acceptance_commit": CORE, "frontier_raw_sha256": sha(raw(CELL)),
           "no_further_writes_by_this_actor": True, "remaining": evidence["truth_boundary"]}
write("local-integration-release-summary.json", summary)
assert ledger_path.read_bytes() == after
print(json.dumps({**{key: summary[key] for key in ["status", "receipt_raw_sha256", "exact_append_raw_sha256",
                 "ledger_after_raw_sha256", "target_state", "single_stabilization_lane", "frontier_raw_sha256"]},
                 "release_summary_raw_sha256": sha((OUT / "local-integration-release-summary.json").read_bytes()),
                 "protected_inputs": len(protected), "writes": "STOPPED"}))
