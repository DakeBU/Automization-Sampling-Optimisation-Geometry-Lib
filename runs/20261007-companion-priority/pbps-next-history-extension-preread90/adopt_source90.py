"""Adopt the independently reviewed source-only successor, never its originals."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent

def digest(path):
    b = path.read_bytes()
    return {"path": str(path), "raw_sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)}

def read(path):
    return json.loads(path.read_bytes())

checked = []
def verify_tree(obj):
    if isinstance(obj, dict):
        sha = obj.get("raw_sha256", obj.get("sha256"))
        if "path" in obj and sha:
            path = Path(obj.get("closed_snapshot", obj["path"]))
            if not path.is_absolute():
                path = ROOT / path
            actual = digest(path)
            assert actual["raw_sha256"] == sha, (path, actual["raw_sha256"], sha)
            if "bytes" in obj:
                assert actual["bytes"] == obj["bytes"], path
            checked.append(actual)
        for value in obj.values():
            verify_tree(value)
    elif isinstance(obj, list):
        for item in obj:
            verify_tree(item)

pinned = {
    "independent-source-first90/closed-raw-manifest.source-first90.native.json":
        "82eed8395f4ddcbeb984847a31e277c8980c171fd6a42c69a0ee9608ef6b845c",
    "independent-topology90/closed-RAW-manifest90.json":
        "1a8b945463a0cc93419ad7790ae0457d4639a0334538b135b0ba067cc5e98729",
    "independent-topology-repair90/closed-raw-manifest90.json":
        "46b232ea7606c88bd7e05e4b5a5f38452b23859b3669d9d34f98ee5539aedb43",
}
for rel, sha in pinned.items():
    path = HERE / rel
    assert digest(path)["raw_sha256"] == sha, path
    checked.append(digest(path))
    verify_tree(read(path))

proposal = read(HERE / "independent-topology90/proposed-topology-scope-overlay90.json")
decision = read(HERE / "independent-topology-repair90/decision90.native.json")
assert decision["decision"] == "ACCEPT_EXACT_TWO_FIELD_SOURCE_TOPOLOGY_SCOPE_OVERLAY"
assert not decision["required_repairs"]
assert decision["distinct_from_graph_creator"]
assert decision["distinct_from_proposer"]
assert decision["distinct_from_root_formalizer"]
original = HERE / "independent-source-first90/source-proof-graph90.native.json"
candidate = HERE / "independent-topology90/source-proof-graph90.proposed-measurability-scope-overlay.json"
expected = read(original)
for change in proposal["changes"]:
    tokens = change["json_pointer"].strip("/").split("/")
    obj = expected
    for token in tokens[:-1]:
        obj = obj[int(token)] if isinstance(obj, list) else obj[token]
    key = int(tokens[-1]) if isinstance(obj, list) else tokens[-1]
    assert obj[key] == change["before"]
    obj[key] = change["after"]
assert {c["json_pointer"] for c in proposal["changes"]} == {
    "/nodes/1/claim", "/edges/1/justification"
}
assert expected == read(candidate)
target = HERE / "source-proof-graph90.accepted-successor.json"
assert not target.exists()
target.write_bytes(candidate.read_bytes())
record = {
    "status": "SOURCE_ONLY_DISTINCT_TOPOLOGY_REPAIR_ADOPTED",
    "utc": datetime.now(timezone.utc).isoformat(),
    "checked_RAW_descriptors": checked,
    "original_unchanged": digest(original),
    "accepted_successor": digest(target),
    "repair_decision": digest(HERE / "independent-topology-repair90/decision90.native.json"),
    "changes": proposal["changes"],
    "header_approved": False, "SAU_claimed": False, "statement_sealed": False,
    "Lean_BODY_started": False, "VERIFIED": False,
    "truth_boundary": "One actual finite-history extension step; full A7 and Goal remain OPEN."
}
(HERE / "root.source90.adoption.json").write_text(
    json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"status": record["status"], "RAW_descriptors": len(checked),
                  "accepted_successor": record["accepted_successor"]}))
