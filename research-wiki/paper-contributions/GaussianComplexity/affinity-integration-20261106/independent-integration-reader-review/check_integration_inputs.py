"""Read-only integration-input checks; writes only this reviewer's own report."""
import hashlib
import json
import pathlib
import subprocess
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[5]
OUT = pathlib.Path(__file__).resolve().parent
BASE = "d9bcd4231df69061c5221f8d557ee179a945c1eb"
REVIEWED = "a5d10714ca01eb29c934acec06bb8983413182c2"
VERIFIED_RECEIPT_COMMIT = "03ce9786f225de7db33917c4c3b41ace64b29fb7"
PRIMARY = "ASTIS-SA-20261106-GaussianComplexitySingleBlockAffinity"
SHARED = "ASTIS-SA-20261106-NormalizedDensityAffinity"


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def paths_changed(before, after, path=()):
    if type(before) is not type(after):
        return [list(path)]
    if isinstance(before, dict):
        keys = set(before) | set(after)
        return sum((paths_changed(before.get(k), after.get(k), path + (k,))
                    for k in sorted(keys)), [])
    if isinstance(before, list) and len(before) == len(after):
        return sum((paths_changed(x, y, path + (i,))
                    for i, (x, y) in enumerate(zip(before, after))), [])
    return [] if before == after else [list(path)]


manifest_path = "research-wiki/paper-contributions/GaussianComplexity/affinity-integration-20261106/core-integration-manifest.json"
manifest = json.loads((ROOT / manifest_path).read_text())
preserved = []
for path, expected in manifest["accepted_source_and_prose_files_unchanged"].items():
    current = (ROOT / path).read_bytes()
    old = git("show", f"{REVIEWED}:{path}")
    preserved.append({"path": path, "raw_sha256": digest(current),
                      "matches_manifest": digest(current) == expected,
                      "matches_reviewed_git_object": current == old})

report_path = "research-wiki/paper-contributions/GaussianComplexity/single-block-affinity-semantic-evidence/independent-fresh-source-module-review/candidate-a5d10714-independent-source-module-reader-review.json"
report_digest = digest((ROOT / report_path).read_bytes())

ledger_path = "runs/substantive_advances.jsonl"
old_ledger = git("show", f"{REVIEWED}:{ledger_path}")
verified_ledger = git("show", f"{VERIFIED_RECEIPT_COMMIT}:{ledger_path}")
now_ledger = (ROOT / ledger_path).read_bytes()
assert now_ledger.startswith(old_ledger)
assert now_ledger.startswith(verified_ledger)
events = [json.loads(line) for line in now_ledger[len(old_ledger):].splitlines()]
integration_events = [json.loads(line) for line in now_ledger[len(verified_ledger):].splitlines()]
states = {}
for line in now_ledger.splitlines():
    event = json.loads(line)
    if event.get("event") == "transition":
        states[event["advance_id"]] = event["to_state"]

reader_path = "website/content/samplewiki_companion_frontiers.json"
reader_before = json.loads(git("show", f"{REVIEWED}:{reader_path}"))
reader_now = json.loads((ROOT / reader_path).read_text())
reader_deltas = paths_changed(reader_before, reader_now)
expected_reader_deltas = [["cases", 4, "reader_guide", 3],
                          ["cases", 4, "theorems", 0, "boundary"]]

inventory_path = "research-wiki/paper-contributions/GaussianComplexity/affinity-integration-20261106/public-import-registry-delta.json"
inventory = json.loads((ROOT / inventory_path).read_text())
public_imports = []
for path in inventory["shared_imports"]:
    old = git("show", f"{REVIEWED}:{path}")
    now = (ROOT / path).read_bytes()
    public_imports.append({"path": path, "before_sha256": digest(old),
                           "after_sha256": digest(now),
                           "manifest_before_matches": digest(old) == inventory["before_sha256"][path],
                           "manifest_after_matches": digest(now) == inventory["after_sha256"][path]})

registry = (ROOT / "AutoSamplingTheory/TechnicalLemmas/Registry.lean").read_text()
target_counts = {name: registry.count(f'localDecl := "{name}"') for name in [
    "AutoSamplingTheory.TechnicalLemmas.InformationTheory.DensityAffinity.normalized_density_tv_affinity",
    "AutoSamplingTheory.ExampleCases.GaussianComplexity.SingleBlockAffinity.single_block_affinity_bound"]}

result = {
    "schema": "astis-independent-integration-input-review/v1",
    "reviewer": "/root/affinity_integration_reader_review",
    "checked_at": datetime.now(timezone.utc).isoformat(),
    "checked_head": git("rev-parse", "HEAD").decode().strip(),
    "official_base": BASE,
    "original_independently_reviewed_source_commit": REVIEWED,
    "role_boundary": "Integration evidence review only. Reuses the actual distinct source/module verifier; no new VERIFIED transition, source-blind reconstruction or fresh source-fidelity verdict is manufactured.",
    "reviewed_inputs": preserved,
    "prior_independent_report": {"path": report_path, "raw_sha256": report_digest,
        "matches_original_receipt": report_digest == "84094263876ddc034e64499fc3c8fc6899d4be5414e157ba4dfb3be6ab72a258"},
    "public_import_registry_hashes": public_imports,
    "registry_target_counts": target_counts,
    "administrative_count_change": "Only Tests/Basic.lean 608 to 610; two canonical Registry entries. The count is inventory, not paper coverage or novelty.",
    "queue_preservation": {
        "reviewed_ledger_byte_prefix_preserved": now_ledger.startswith(old_ledger),
        "independently_verified_ledger_byte_prefix_preserved": now_ledger.startswith(verified_ledger),
        "events_since_original_review": [{k: event.get(k) for k in ["advance_id", "from_state", "to_state", "worker_id"]} for event in events],
        "events_since_original_verification_receipt": [{k: event.get(k) for k in ["advance_id", "from_state", "to_state", "worker_id"]} for event in integration_events],
        "all_appended_events_owned": all(e.get("advance_id") in [PRIMARY, SHARED] for e in events),
        "single_stabilization_lane": [key for key, value in states.items() if value == "STABILIZING"],
        "primary_state": states[PRIMARY], "shared_state": states[SHARED]},
    "reader_semantic_deltas": reader_deltas,
    "reader_only_two_owned_fields_changed": reader_deltas == expected_reader_deltas,
    "source_vs_generic_boundary": {
        "accepted": True,
        "generic": "One ASTIS-authored canonical node on any common measurable carrier/reference measure. Pointwise nonnegative measurable genuine L1 unit densities are public inputs; no finite/probability/sigma-finite base assumption.",
        "source": "Actual full-Haar sign-conditioned inverse-precision Gaussian mixtures, only n>=3 and kappa>=4. Actual density producer and B.7 are internal dependency edges, not new binders.",
        "scalar_consumer": "The test is all-natural-k numerical power of the actual single-block integral. No equality with actual product affinity, independent-block law, tensorization or amplified TV is inferred.",
        "shared_identity": "Exactly one shared canonical declaration; the paper source adapter does genuine law identification and constant/log composition rather than restating an assumed bound."},
    "current_metadata_followup": [
        "At final stabilization update the two owned active frontier records' stale present-tense pending/no-proof prose, while retaining original frozen source-graph and review artifacts unchanged. Cite the actual existing independent verdict rather than creating independently_verified fields.",
        "Final root/site/graph/UI evidence has not yet been supplied to this reviewer.",
        "Post-merge purification and Exposition Seal remain pending until an actual merge."],
    "root_gate_acceptance": "NOT_EVALUATED; gate running, no pass inferred",
    "site_graph_ui_acceptance": "NOT_EVALUATED; final artifacts pending",
    "postmerge_purification": "PENDING_ACTUAL_MERGE",
    "blocking_findings_for_reviewed_integration_inputs": [],
    "remaining_whole_goal_boundary": "Actual product laws/tensorization/amplification, oracle/transcript/precision/caps/expected cost, fixed-spectrum hidden eigenbasis and both main lower bounds remain open. This review cannot complete the overall Goal."
}
assert all(x["matches_manifest"] and x["matches_reviewed_git_object"] for x in preserved)
assert result["prior_independent_report"]["matches_original_receipt"]
assert all(x["manifest_before_matches"] and x["manifest_after_matches"] for x in public_imports)
assert all(x == 1 for x in target_counts.values())
assert result["reader_only_two_owned_fields_changed"]
assert result["queue_preservation"]["single_stabilization_lane"] == [PRIMARY]
assert states[SHARED] == "VERIFIED"
assert len(integration_events) == 1 and integration_events[0]["to_state"] == "STABILIZING"
output_path = OUT / "candidate-970775a5-integration-input-review.json"
output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"report": str(output_path.relative_to(ROOT)), "sha256": digest(output_path.read_bytes()),
                  "reviewed_inputs_preserved": len(preserved), "registry_nodes": len(target_counts),
                  "root_ui_purification_acceptance": "pending"}))
