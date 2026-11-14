"""Mechanical projection of the already-recorded distinct Eq6 VERIFIED fact."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent
CANDIDATE = "98cc6c8953d38dd54bc4e4ef7a547fd68a381ac8"
ACTOR = "/root/affinity_integration_reader_review"
VERIFIER = "/root/eq6_fresh_source_module_review"
ADVANCE = "ASTIS-SA-20261106-GaussianComplexityAveragedBlockLaw"
CELL = "research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-averaged-block-law.json"
AUDIT = "research-wiki/semantic-roundtrip/audits/huanjian-averaged-block-law.json"
DECL = "AutoSamplingTheory.ExampleCases.GaussianComplexity.AveragedBlockLaw.actual_averaged_block_product"
REVIEW = "research-wiki/paper-contributions/GaussianComplexity/averaged-block-law-semantic-evidence/fresh-source-module-review"
BINDING = "908c5e4bfdd5276ce6be52f2458c3ad4f45e6a8c1e19c62fd11e81e498a15f7e"


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def fh(path):
    return digest((ROOT / path).read_bytes())


def read(path):
    return json.loads((ROOT / path).read_text())


assert git("rev-parse", "HEAD").decode().strip() == CANDIDATE
summary_path = f"{REVIEW}/verified-transition-summary.json"
assert fh(summary_path) == "7c2fe73e1bf6175ef7b1b3145ae21fe42d3c46677d07e590c53de7350e7922fd"
summary = read(summary_path)
assert summary["advance_id"] == ADVANCE and summary["state"] == "VERIFIED"
assert summary["verified_commit"] == CANDIDATE and summary["verifier_id"] == VERIFIER
assert summary["proving_owner"] == "huanjian_gc_20261106_eq6"
checked_refs = {}


def verify_refs(value):
    if isinstance(value, dict):
        if "path" in value and "physical_raw_sha256" in value:
            path = value["path"]
            raw = (ROOT / path).read_bytes()
            assert digest(raw) == value["physical_raw_sha256"]
            if "bytes" in value:
                assert len(raw) == value["bytes"]
            checked_refs[path] = digest(raw)
        for child in value.values():
            verify_refs(child)
    elif isinstance(value, list):
        for child in value:
            verify_refs(child)


verify_refs(summary)
receipt = read(summary["normal_api_receipt"]["path"])
assert summary["normal_api_receipt"]["physical_raw_sha256"] == "3112a82ec1dd2425c2c4dba634ecb51af18f538d19389143c5f0631a6cb3b5c4"
verify_refs(receipt)
assert receipt["api"] == "tools.astis_advance.transition_advance"
assert receipt["from_state"] == "PROVED_LOCAL" and receipt["to_state"] == "VERIFIED"
assert receipt["worker_id"] == VERIFIER and receipt["verified_commit"] == CANDIDATE
assert receipt["exit_code"] == 0 and receipt["normal_api_reviewed_publication_gate_passed"]
evidence = read(receipt["evidence"]["path"])
verify_refs(evidence)
append_path = summary["exact_append"]["path"]
append = (ROOT / append_path).read_bytes()
assert len(append.splitlines()) == 1
assert digest(append) == "45eee83c108db95649dbf60e28f28a96f7ae73ad225f02f5ea19bb5750b77093"
event = json.loads(append)
assert event["advance_id"] == ADVANCE and event["worker_id"] == VERIFIER
assert event["from_state"] == "PROVED_LOCAL" and event["to_state"] == "VERIFIED"
assert event["evidence"]["publication_declarations"] == [DECL]
ledger_path = ROOT / "runs/substantive_advances.jsonl"
ledger = ledger_path.read_bytes()
prefix = git("show", f"{CANDIDATE}:runs/substantive_advances.jsonl")
assert ledger == prefix + append
assert digest(ledger) == "f1be5e771854da6b56f9a8cf99c1a9d43ad8e6b1339267253c07785b7795acc1"
protection = read(summary["protection_checks"]["path"])
assert protection["original_prefix_sha256"] == digest(prefix)
assert protection["after_ledger_sha256"] == digest(ledger)

audit_raw = (ROOT / AUDIT).read_bytes()
audit = json.loads(audit_raw)
assert digest(audit_raw) == "7f96a0c943f73010c9ef75b19070394a6037f80d769db52e66ab0ed09f1377da"
assert audit["state"] in {"accepted", "source-reviewed"}
assert audit["source_review"]["state"] == "accepted"
assert audit["publication_binding_sha256"] == BINDING
assert audit_raw != git("show", f"{CANDIDATE}:{AUDIT}")
context_raw = subprocess.check_output(["python3", "tools/astis_publication.py", "review-context",
    "--item", "huanjian-averaged-block-law", "--declaration", DECL], cwd=ROOT)
context = json.loads(context_raw)
assert context["publication_binding_sha256"] == BINDING
assert context["publication_context"] == audit["publication_context"]
(OUT / "projection-current-publication-context.json").write_bytes(context_raw)
source_inputs = []
for path in ["AutoSamplingTheory/ExampleCases/GaussianComplexity/AveragedBlockLaw.lean",
             "Tests/GaussianComplexityAveragedBlockLaw.lean",
             "website/content/declaration_lessons/huanjian-averaged-block-law.json",
             "website/content/publications/huanjian-averaged-block-law.json",
             "research-wiki/paper-contributions/GaussianComplexity/averaged-block-law-statement-seal.json"]:
    raw = (ROOT / path).read_bytes()
    assert raw == git("show", f"{CANDIDATE}:{path}")
    source_inputs.append({"path": path, "physical_raw_sha256": digest(raw), "byte_equal98cc_git_object": True})

baseline = json.loads((OUT / "read-only-protected-foreign-surface-baseline.json").read_text())
protected = dict(baseline["protected_file_hashes"])
protected.pop(CELL)
assert all(fh(p) == expected for p, expected in protected.items())
protected[AUDIT] = digest(audit_raw)
for directory in ["website/content/declaration_lessons", "website/content/publications"]:
    for path in (ROOT / directory).glob("*.json"):
        protected[str(path.relative_to(ROOT))] = digest(path.read_bytes())
frontiers = sorted((ROOT / "research-wiki/frontier-cells").glob("*.json"))
frontier_before = {str(p.relative_to(ROOT)): digest(p.read_bytes()) for p in frontiers}
tracked_before = set(git("diff", "--name-only").decode().splitlines())
cell_raw = (ROOT / CELL).read_bytes()
cell = json.loads(cell_raw)
assert cell["status"] == "proved_locally" and cell["advance_id"] == ADVANCE
history = {
    "projection_actor": ACTOR,
    "meaning": "Exact prior preproof/local-proof wording is retained as history; this actor only projects the actual distinct independent VERIFIED event.",
    "previous_status": cell["status"],
    "evidence.execution_boundary": cell["evidence"]["execution_boundary"],
    "source_detail_audit.gap": cell["source_detail_audit"]["gap"],
    "source_detail_audit.fidelity_boundary": cell["source_detail_audit"]["fidelity_boundary"],
    "graph_contribution.visual_review": cell["graph_contribution"]["visual_review"],
    "learning_contract.salvage.reason": cell["learning_contract"]["salvage"]["reason"],
    "consumers": cell["consumers"]
}
cell["historical_preintegration_checkpoints"] = history
cell["status"] = "independently_verified"
cell["evidence"]["execution_boundary"] = "Actual existing independent normal-API VERIFIED at98cc6c8953d38dd54bc4e4ef7a547fd68a381ac8 by /root/eq6_fresh_source_module_review covers the bounded actual Eq6/source/whole-module/parents/true all-parameter common-sign marginal consumers and static reader. The precommit focused receipts truthfully reportff7; separate fresh direct production/Tests/probe elaboration checks report98cc. This frontier projection adds no source verdict or state event. Current new-root/Registry/site/real Chrome/graph integration, remote/live, merge and purification/ExpositionSeal remain pending."
cell["evidence"]["independent_verification"] = "Existing independent normal-API VERIFIED by /root/eq6_fresh_source_module_review at98cc6c8953d38dd54bc4e4ef7a547fd68a381ac8, verified-transition-summary.json SHA7c2fe73e1bf6175ef7b1b3145ae21fe42d3c46677d07e590c53de7350e7922fd and actual normal-API receipt SHA3112a82ec1dd2425c2c4dba634ecb51af18f538d19389143c5f0631a6cb3b5c4. /root/affinity_integration_reader_review only projects that existing fact, without acting as the source verifier or adding a VERIFIED event."
cell["source_detail_audit"]["gap"] = "The printed Eq6 prior-averaged joint law and its probability/AE-positive-support elaboration are compiled and independently source/whole-module/parent/static-reader accepted at98cc by the distinct fresh reviewer. Source assertions with omitted construction/averaging bridges are explicitly completed using canonical parents. Current root/Registry/real browser/graph and remote/publication/merge/purification delivery remain separate pending stages; Ex70/71/72 are downstream open obligations."
cell["source_detail_audit"]["fidelity_boundary"] = "Only bounded actual prior-averaged Eq6, probability/AE-positive source support and true generic common-sign block/residual marginal consumers are independently accepted. Source code, Tests, lesson, publication and sealed interface remain exact98cc bytes. The accepted source-reviewed audit is subsequent working metadata, not byte-identical to the98cc blind-reconstructed draft. New root/Registry/Chrome/graph, remote merge/live, PURIFIED/ExpositionSeal and whole-Goal acceptance remain pending; Ex70 densities, Ex71 affinity, Ex72 amplification, oracle/precision/caps/cost/hidden-basis and both main bounds remain separate."
cell["graph_contribution"]["visual_review"] = "Actual independent static reader content is accepted, but new-root/Registry generated graph integration and real browser MathJax/desktop/mobile/graph/live visual acceptance remain pending. No graph visual PASS is inferred from static review."
cell["learning_contract"]["salvage"]["reason"] = "No failed mathematical route is retired or proof fragment deleted by this mechanical projection. The earlier No proof search intake wording is preserved in historical_preintegration_checkpoints; actual local proof and independent source/module verification now have their own evidence."
cell["consumers"] = [
    "Tests.GaussianComplexityAveragedBlockLaw: true actual D.bind gamma block-mixture and standard residual marginal pushforwards for every source parameter and either common sign, compiled and independently reviewed.",
    "AppendixB.2.3 Ex70 actual product density, Ex71 affinity tensorization and Ex72 amplification (planned, not proved by this Eq6 result)."
]
report_path = "research-wiki/paper-contributions/GaussianComplexity/eq6-integration-20261106/independent-integration-reader-review/existing-verification-frontier-projection.json"
cell["evidence"]["existing_verification_projection"] = {
    "projection_actor": ACTOR, "kind": "existing-independent-ledger-fact-only",
    "original_source_verifier": VERIFIER, "verified_commit": CANDIDATE,
    "original_summary": summary_path, "original_summary_raw_sha256": fh(summary_path),
    "actual_normal_API_receipt": summary["normal_api_receipt"]["path"],
    "actual_normal_API_receipt_raw_sha256": summary["normal_api_receipt"]["physical_raw_sha256"],
    "actual_existing_VERIFIED_append_raw_sha256": digest(append),
    "current_source_reviewed_audit_raw_sha256": digest(audit_raw),
    "current_accepted_publication_binding_sha256": BINDING,
    "new_source_verdict_or_VERIFIED_event": False,
    "projection_report": report_path,
    "remaining": "New root/Registry/site/realChrome/graph, remote/live, actual merge, PURIFIED/ExpositionSeal and all Ex70/71/72/main/cost/oracle boundaries remain pending."
}
(OUT / "projection-frontier.before.json").write_bytes(cell_raw)
(OUT / "projection-protected-inputs.json").write_text(json.dumps(protected, indent=2) + "\n")
(ROOT / CELL).write_text(json.dumps(cell, ensure_ascii=False, indent=2) + "\n")
assert ledger_path.read_bytes() == ledger
assert all(fh(p) == expected for p, expected in protected.items())
assert [p for p, old in frontier_before.items() if fh(p) != old] == [CELL]
assert set(git("diff", "--name-only").decode().splitlines()) == tracked_before | {CELL}
states = {}
for line in ledger.splitlines():
    e = json.loads(line)
    if e.get("event") == "transition":
        states[e["advance_id"]] = {"state": e["to_state"], "actor": e["worker_id"]}
assert states[ADVANCE] == {"state": "VERIFIED", "actor": VERIFIER}
old_ids = ["ASTIS-SA-20261106-GaussianComplexityConditionalBlockLaw",
           "ASTIS-SA-20261106-GaussianComplexitySingleBlockAffinity", "ASTIS-SA-20261106-NormalizedDensityAffinity"]
assert all(states[k]["state"] == "VERIFIED" for k in old_ids)
diff = git("diff", "--", CELL)
(OUT / "existing-verification-frontier-projection.diff").write_bytes(diff)
result = {
    "schema": "astis-independent-existing-Eq6-fact-frontier-projection/v1",
    "actor": ACTOR, "checked_at": datetime.now(timezone.utc).isoformat(), "checked_head": CANDIDATE,
    "operation": "Mechanical projection of the existing independently recorded normal-API VERIFIED fact into only the new owned frontier. No state API or new source/mathematical verdict.",
    "original_verifier": VERIFIER, "original_summary_raw_sha256": fh(summary_path),
    "actual_normal_API_receipt_raw_sha256": summary["normal_api_receipt"]["physical_raw_sha256"],
    "actual_existing_one_append_raw_sha256": digest(append),
    "actual_original_prefix_git_blob": git("rev-parse", f"{CANDIDATE}:runs/substantive_advances.jsonl").decode().strip(),
    "actual_current_ledger_equals98cc_prefix_plus_existing_reviewer_append": True,
    "current_ledger_raw_sha256_unchanged": digest(ledger),
    "all_referenced_artifact_hashes_checked": checked_refs,
    "source_Test_lesson_publication_seal_git_input_checks": source_inputs,
    "audit_successor_provenance": {"actual_current_state": audit["state"], "actual_source_review_state": audit["source_review"]["state"], "actual_current_raw_sha256": digest(audit_raw), "byte_equal98cc_git_object": False, "meaning": "The distinct reviewer accepted only review fields after98cc; the accepted/source-reviewed audit is a legitimate successor to98cc blind-reconstructed metadata, not an unchanged git object."},
    "fresh_current_publication_binding": context["publication_binding_sha256"],
    "current_context_equals_accepted_audit_context": True,
    "owned_frontier": CELL, "before_raw_sha256": digest(cell_raw), "after_raw_sha256": fh(CELL),
    "actual_owned_diff_raw_sha256": digest(diff),
    "new_ledger_events": 0, "normal_state_API_calls": 0,
    "all_foreign_states_ledger_records_and_frontier_files_unchanged": True,
    "other_frontier_directory_JSON_files_preserved": len(frontiers) - 1,
    "other_frontier_hashes_unchanged": {p: v for p, v in frontier_before.items() if p != CELL},
    "protected_Lean_prose_audit_and_control_files_unchanged": len(protected),
    "old_three_VERIFIED_advances_preserved": {k: states[k] for k in old_ids},
    "single_STAB_lane_unchanged": [k for k, v in states.items() if v["state"] == "STABILIZING"],
    "root_Registry_Test_imports_case_or_Bench_actions": "None by this reviewer. Prior shared/root surfaces remain untouched; real remote-readonly-readback is an observation, not a push/retry/merge/deploy.",
    "projection_scope": "Bounded actual common-sign prior-averaged Eq6 joint law, probability/AE-PD and real generic mixture/residual marginals; Ex70/71/72 and main complexity obligations are not inferred.",
    "root_browser_graph_remote_live_M_P_ExpositionSeal_Goal_claims": False
}
(ROOT / report_path).write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"report": report_path, "raw_sha256": fh(report_path),
    "owned_frontier_raw_sha256": fh(CELL), "other_frontier_files_preserved": len(frontiers) - 1,
    "protected_files_preserved": len(protected), "new_V_or_ledger_events": 0}))
