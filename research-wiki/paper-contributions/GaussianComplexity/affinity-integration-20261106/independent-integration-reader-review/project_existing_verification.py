"""Project two already-existing independent VERIFIED facts into owned cells.

This is metadata reconciliation, not a new mathematical/source verdict or SAU
transition. It never writes the ledger or calls a state API.
"""
import hashlib
import json
import pathlib
import subprocess
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[5]
OUT = pathlib.Path(__file__).resolve().parent
ACTOR = "/root/affinity_integration_reader_review"
VERIFIER = "/root/affinity_fresh_source_module_review"
REVIEWED = "a5d10714ca01eb29c934acec06bb8983413182c2"
REPORT = "research-wiki/paper-contributions/GaussianComplexity/single-block-affinity-semantic-evidence/independent-fresh-source-module-review/candidate-a5d10714-independent-source-module-reader-review.json"
EXPECTED_REPORT = "84094263876ddc034e64499fc3c8fc6899d4be5414e157ba4dfb3be6ab72a258"
CELLS = [
    ("ASTIS-SHARED-normalized-density-affinity", "ASTIS-SA-20261106-NormalizedDensityAffinity", "normalized-density-affinity", "1b3f2db33d7804f70f8b59072ff428d7585f3e740384282e598cee7a2411b07f"),
    ("ASTIS-SW-GAUSSIAN-COMPLEXITY-single-block-affinity", "ASTIS-SA-20261106-GaussianComplexitySingleBlockAffinity", "huanjian-single-block-affinity", "e2bf9be8465a3e73cf410714b0995a1c14c12edb1ace064e54c1ac0255e55599")]


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def read_json(path):
    return json.loads((ROOT / path).read_text())


assert digest((ROOT / REPORT).read_bytes()) == EXPECTED_REPORT
ledger_path = ROOT / "runs/substantive_advances.jsonl"
ledger_before = ledger_path.read_bytes()
ledger = [json.loads(line) for line in ledger_before.splitlines()]
all_frontiers = sorted((ROOT / "research-wiki/frontier-cells").glob("*.json"))
before_frontiers = {str(p.relative_to(ROOT)): digest(p.read_bytes()) for p in all_frontiers}
owned = {f"research-wiki/frontier-cells/{cell}.json" for cell, *_ in CELLS}
head_before = git("rev-parse", "HEAD").decode().strip()
assert git("diff", "--name-only").decode().strip() == ""
checks = []
for cell, advance, item, binding in CELLS:
    events = [e for e in ledger if e.get("advance_id") == advance and e.get("event") == "transition" and e.get("to_state") == "VERIFIED"]
    assert len(events) == 1
    event = events[0]
    assert event["worker_id"] == VERIFIER
    assert event["evidence"]["verifier_id"] == VERIFIER
    assert event["evidence"]["verified_commit"] == REVIEWED
    assert event["evidence"]["source_audit"]["report_raw_sha256"] == EXPECTED_REPORT
    audit = read_json(f"research-wiki/semantic-roundtrip/audits/{item}.json")
    context = json.loads((OUT / f"{item}-current-review-context.json").read_text())
    assert audit["state"] == "accepted" and audit["source_review"]["state"] == "accepted"
    assert audit["publication_binding_sha256"] == binding == context["publication_binding_sha256"]
    assert audit["publication_context"] == context["publication_context"]
    checks.append({"cell_id": cell, "advance_id": advance, "original_verifier": VERIFIER,
        "event_sha256": digest(json.dumps(event, sort_keys=True, separators=(",", ":")).encode()),
        "event_created_at": event["created_at"], "publication_binding_sha256": binding,
        "audit_raw_sha256": digest((ROOT / f"research-wiki/semantic-roundtrip/audits/{item}.json").read_bytes())})

protected = ["runs/substantive_advances.jsonl", "lean-toolchain", "lake-manifest.json",
    "research-wiki/paper-contributions/GaussianComplexity/single-block-affinity-statement-seal.json",
    "research-wiki/paper-contributions/GaussianComplexity/normalized-density-affinity-statement-seal.json",
    "research-wiki/paper-contributions/GaussianComplexity/single-block-affinity-source-graph.json",
    "research-wiki/paper-contributions/GaussianComplexity/single-block-affinity-source-to-code-map.json",
    "research-wiki/semantic-roundtrip/audits/normalized-density-affinity.json",
    "research-wiki/semantic-roundtrip/audits/huanjian-single-block-affinity.json"]
protected += list(read_json("research-wiki/paper-contributions/GaussianComplexity/affinity-integration-20261106/core-integration-manifest.json")["accepted_source_and_prose_files_unchanged"])
protected_before = {p: digest((ROOT / p).read_bytes()) for p in protected}

for cell, advance, item, binding in CELLS:
    path = ROOT / f"research-wiki/frontier-cells/{cell}.json"
    data = json.loads(path.read_text())
    assert data["status"] == "proved_locally"
    history = {"recorded_by": ACTOR,
        "meaning": "Exact pre-integration process prose retained as historical checkpoints; the source graph and prior review files remain unchanged.",
        "previous_status": data["status"],
        "evidence.execution_boundary": data["evidence"]["execution_boundary"],
        "source_detail_audit.gap": data["source_detail_audit"]["gap"],
        "graph_contribution.visual_review": data["graph_contribution"]["visual_review"],
        "graph_contribution.reason": data["graph_contribution"]["reason"],
        "conceptual_mirror_audit.reason": data["conceptual_mirror_audit"]["reason"]}
    if "note" in data["shared_floor_audit"]:
        history["shared_floor_audit.note"] = data["shared_floor_audit"]["note"]
        data["shared_floor_audit"]["note"] = "The shared B node and exact actual source consumer are compiled and independently reviewed at a5d10714ca01eb29c934acec06bb8983413182c2. Final root/site/graph delivery and post-merge purification remain separate."
    data["historical_preintegration_checkpoints"] = history
    data["status"] = "independently_verified"
    data["source_detail_audit"]["gap"] = "The exact declaration/module, source fidelity and authored reader content were accepted by the distinct original reviewer at a5d10714ca01eb29c934acec06bb8983413182c2. Current code, lesson, publication context and source-binding bytes remain identical. Final site/graph/desktop/mobile integration and post-merge purification remain pending."
    data["evidence"]["execution_boundary"] = "Preproof restrictions were satisfied before implementation; their exact prior wording is preserved in historical_preintegration_checkpoints. The current local proof and actual independent normal-API VERIFIED event are recorded below."
    data["conceptual_mirror_audit"]["reason"] = "One exact compiled common-measure density comparison is canonically reused by the actual Gaussian source adapter. No cross-domain conceptual transport or certified functor is claimed."
    data["graph_contribution"]["visual_review"] = "Final stabilization graph/reader visual acceptance pending; the independent local source/module/content review does not certify final UI delivery."
    data["graph_contribution"]["reason"] = "The original declaration identities are reused in serialized integration. No conceptual overlay is promoted into a formal dependency."
    data["evidence"]["independent_verification"] = "Existing independent normal-API VERIFIED by /root/affinity_fresh_source_module_review at a5d10714ca01eb29c934acec06bb8983413182c2; report candidate-a5d10714-independent-source-module-reader-review.json SHA84094263876ddc034e64499fc3c8fc6899d4be5414e157ba4dfb3be6ab72a258. The frontier status is a metadata projection of that actual event by a distinct integration reviewer, not a new verdict."
    data["evidence"]["existing_verification_projection"] = {
        "projection_actor": ACTOR, "projection_kind": "existing-independent-ledger-fact-only",
        "source_verifier_id": VERIFIER, "verified_commit": REVIEWED,
        "canonical_advance_id": advance, "prior_report": REPORT,
        "prior_report_raw_sha256": EXPECTED_REPORT, "current_publication_binding_sha256": binding,
        "new_verdict_or_VERIFIED_event": False,
        "evidence": "research-wiki/paper-contributions/GaussianComplexity/affinity-integration-20261106/independent-integration-reader-review/existing-verification-frontier-projection.json",
        "remaining": "Root/site/graph/UI acceptance, actual merge and post-merge purification remain separate. Whole-Goal completion is not claimed."}
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")

after_frontiers = {str(p.relative_to(ROOT)): digest(p.read_bytes()) for p in all_frontiers}
changed = sorted(p for p in before_frontiers if before_frontiers[p] != after_frontiers[p])
assert set(changed) == owned
assert ledger_path.read_bytes() == ledger_before
assert all(digest((ROOT / p).read_bytes()) == h for p, h in protected_before.items())
tracked_changed = git("diff", "--name-only").decode().splitlines()
assert set(tracked_changed) == owned
diff = git("diff", "--", *sorted(owned))
(OUT / "existing-verification-frontier-projection.diff").write_bytes(diff)
result = {"schema": "astis-independent-frontier-fact-projection/v1", "actor": ACTOR,
    "checked_at": datetime.now(timezone.utc).isoformat(), "checked_head": head_before,
    "authorization": "Root explicitly authorized only these two owned metadata files after prior read-only review. No producer, seal, source graph, lesson, publication, other frontier, audit or ledger write is authorized.",
    "projection_is_new_math_or_source_verdict": False, "state_api_called": False,
    "existing_verification_checks": checks, "prior_report_raw_sha256": EXPECTED_REPORT,
    "changed_frontiers": changed, "all_frontier_files_count": len(all_frontiers),
    "all_uninvolved_frontiers_preserved": all(before_frontiers[p] == after_frontiers[p] for p in before_frontiers if p not in owned),
    "frontier_hashes_before": before_frontiers, "frontier_hashes_after": after_frontiers,
    "protected_input_hashes_unchanged": protected_before,
    "ledger_bytes_unchanged": True, "all_tracked_changes_are_owned_frontiers": True,
    "exact_diff_raw_sha256": digest(diff),
    "boundary": "Existing local independent verification only. Final site/graph/UI, merge, purification and overall Goal remain unaccepted by this action."}
(OUT / "existing-verification-frontier-projection.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"changed": changed, "uninvolved_frontiers_preserved": len(all_frontiers)-2,
    "ledger_unchanged": True, "protected_inputs_unchanged": len(protected_before), "new_VERIFIED_events": 0,
    "report_raw_sha256": digest((OUT / "existing-verification-frontier-projection.json").read_bytes())}))
