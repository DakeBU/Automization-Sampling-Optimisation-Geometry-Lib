"""Repair search-evidence discovery field only; retain failed gate and sealed statement."""
from pathlib import Path
import hashlib, json, subprocess, sys

run = Path(__file__).parent
pre = run.parent / "pbps-ordered-history-iteration-preread91"
p = Path("research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-absolute-next-event-time.json")
before = p.read_bytes()
j = json.loads(before)
assert j["status"] == "claimed"
assert j["statement_seal"]["signature_digest"] == "b8bba160f6134c7927167a0a34d99971ce75023ef7ea04f738a91b6862da2680"
queries = json.loads((pre / "independent-source-first91/retrieval91.native.json").read_bytes())["queries"]
assert any("mathlib" in x["path"] for x in queries)
for x in queries:
    b = Path(x["path"]).read_bytes()
    assert hashlib.sha256(b).hexdigest() == x["raw_sha256"]
snapshot = run / "frontier-before-search-evidence91.exactraw.snapshot.json"
assert not snapshot.exists()
snapshot.write_bytes(before)
for field in ["searched", "searched_existing"]:
    parent = j["shared_floor_audit"] if field == "searched" else j["reuse_plan"]
    parent[field] += [x["path"] for x in queries if x["path"] not in parent[field]]
p.write_text(json.dumps(j, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
receipt = {
    "class": "CONTROL_PLANE_SEARCH_DISCOVERABILITY_FIELD",
    "trigger": "frontier-before-proof91 receipt EXIT1: schema-2 cells must search mathlib",
    "strict_fix": "Expose the already executed/pinned actual query receipt paths in searched and searched_existing; no search result, statement, source graph, Seal or Lean changed.",
    "before_cell_sha256": hashlib.sha256(before).hexdigest(),
    "after_cell_sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
    "actual_queries": queries, "proof_started": False,
}
(run / "frontier-search91.diagnosis.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8", newline="\n")
q = subprocess.run([sys.executable, "-X", "utf8", "tools/astis_frontier_cells.py", "check"], capture_output=True)
(run / "frontier-before-proof91-search-fixed.stdout.json").write_bytes(q.stdout)
(run / "frontier-before-proof91-search-fixed.stderr.log").write_bytes(q.stderr)
(run / "frontier-before-proof91-search-fixed.receipt.json").write_text(json.dumps({"exit_code": q.returncode, "terminal_closed": True}) + "\n", encoding="utf-8", newline="\n")
assert q.returncode == 0, (q.stdout + q.stderr).decode(errors="replace")[-4000:]
print("Statement Seal/claim intact; corrected existing search receipt discoverability. Frontier PASS; no proof credit.")
