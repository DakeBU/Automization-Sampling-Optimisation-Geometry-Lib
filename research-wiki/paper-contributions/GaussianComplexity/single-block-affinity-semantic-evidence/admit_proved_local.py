from pathlib import Path
import hashlib, json, sys
r = Path.cwd()
sys.path.insert(0, str(r))
from tools import astis_advance as a
e = r / "research-wiki/paper-contributions/GaussianComplexity/single-block-affinity-semantic-evidence"
b = e.parent
sha = lambda raw: hashlib.sha256(raw).hexdigest()
targets = [
 ("ASTIS-SA-20261106-NormalizedDensityAffinity", "ASTIS-SHARED-normalized-density-affinity", "normalized-density-affinity-statement-seal.json", "reusable-interface"),
 ("ASTIS-SA-20261106-GaussianComplexitySingleBlockAffinity", "ASTIS-SW-GAUSSIAN-COMPLEXITY-single-block-affinity", "single-block-affinity-statement-seal.json", "theorem-edge")]
ledger = r / "runs/substantive_advances.jsonl"
before = ledger.read_bytes()
prior = a.current_advances()
receipt_path = e / "20261106T015921188329Z-normalized-affinity-representative-consumer.receipt.json"
receipt = json.loads(receipt_path.read_text())
assert receipt["exit_code"] == 0
for aid, cell, sealname, kind in targets:
 assert prior[aid]["state"] == "CLAIMED"
 seal = json.loads((b / sealname).read_text())
 text = (r / seal["target"]["file"]).read_text()
 signature = "theorem " + text.split("theorem ", 1)[1].split(" := by", 1)[0]
 assert signature == seal["target"]["exact_signature"]
pre = {"old_raw_ledger_sha256": sha(before), "current_states": {x[0]: prior[x[0]]["state"] for x in targets}, "actual_focused_receipt": str(receipt_path.relative_to(r)), "actual_proof_bodies_already_executed": True, "event_clock_rule": "All normal API events are recorded now; no event is backdated."}
(e / "proved-local-preflight.json").write_text(json.dumps(pre, indent=2) + "\n")
for aid, cell, sealname, kind in targets:
 seal = json.loads((b / sealname).read_text())
 decl = seal["target"]["declaration"]
 a.transition_advance(aid, "EXPLORING", worker_id="huanjian_gc_20261106_affinity", modes=["record-current-exploration-before-local-proof-admission"], evidence={"state_sequence_correction": "Already-executed, actually compiled proof acknowledged now using legal normal API sequence; no backdate or new mathematical claim."}, path=ledger)
 evidence = {"result_kind": kind, "theorem_delta": seal["target"]["exact_signature"], "lean_files": [seal["target"]["file"]], "lean_declarations": [decl], "publication_declarations": [decl], "focused_checks": [{"command": receipt["command"], "receipt": str(receipt_path.relative_to(r)), "log_sha256": receipt["log_sha256"], "result": "Actual PASS3723 jobs; normalized endpoints, a.e. representative invariance, actual source-parameter power bound and only standard axioms."}], "truth_boundary": seal["truth_boundary"], "conceptual_mirror_audit": {"status": "none-found", "discovery_ids": [], "reason": "Same compiled normalized-density node shared canonically; no cross-domain conceptual transport claimed."}, "semantic_roundtrip": {"state": "blind-reconstructed; fresh independent source/module/reader review pending", "reviewed": False}, "source_to_code_map": str((b / "single-block-affinity-source-to-code-map.json").relative_to(r))}
 a.transition_advance(aid, "PROVED_LOCAL", worker_id="huanjian_gc_20261106_affinity", modes=["one-proof-worker", "real-consumer-build", "normal-publication-admission"], evidence=evidence, path=ledger)
 fp = r / "research-wiki/frontier-cells" / (cell + ".json")
 j = json.loads(fp.read_text())
 j["status"] = "proved_locally"
 j["evidence"]["focused_checks"] = evidence["focused_checks"]
 j["evidence"]["source_to_code_map"] = evidence["source_to_code_map"]
 j["learning_contract"]["failure_class"] = "NONE"
 j["learning_contract"]["salvage"]["reason"] = "Only implementation scope/sqrt/log API and Harness state sequencing corrections; exact statements unchanged. No mathematical route refuted or verified fragment discarded."
 fp.write_text(json.dumps(j, ensure_ascii=False, indent=2) + "\n")
after = ledger.read_bytes()
now = a.current_advances()
changed = {x[0] for x in targets}
assert after.startswith(before)
assert all(now[k] == v for k, v in prior.items() if k not in changed)
(e / "proved-local-normal-api.exact-append.jsonl").write_bytes(after[len(before):])
post = {"normal_API": "tools.astis_advance.transition_advance", "expected_states": {x: now[x]["state"] for x in changed}, "old_raw_prefix_preserved": True, "other_prior_states_unchanged": True, "new_events": len(after[len(before):].splitlines()), "old_ledger_sha256": sha(before), "new_ledger_sha256": sha(after), "no_VERIFIED_or_integration_transition": True}
(e / "proved-local-postcheck.json").write_text(json.dumps(post, indent=2) + "\n")
print(json.dumps(post, indent=2))
