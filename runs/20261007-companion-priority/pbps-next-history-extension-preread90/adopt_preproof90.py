import datetime
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent

def load(p):
    return json.loads(p.read_bytes())

def pin(p):
    b = p.read_bytes()
    return {"path": p.relative_to(ROOT).as_posix(), "raw_sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)}

checked = []
def verify(obj):
    if isinstance(obj, dict):
        sha = obj.get("raw_sha256", obj.get("sha256"))
        if "path" in obj and sha:
            p = Path(obj.get("closed_snapshot", obj["path"]))
            p = p if p.is_absolute() else ROOT / p
            actual = pin(p)
            assert actual["raw_sha256"] == sha, (p, actual["raw_sha256"], sha)
            if "bytes" in obj:
                assert actual["bytes"] == obj["bytes"], p
            checked.append(actual)
        for value in obj.values():
            verify(value)
    elif isinstance(obj, list):
        for value in obj:
            verify(value)

pinned = {
    "independent-header-math90/closed-RAW-manifest90.json": "ca5529bce86373a806e97179ae11193aaa8f7fd2753ee4e0d760790f90eab94d",
    "independent-header-source90/closed-raw-manifest.header-source90.v2.native.json": "5308c31bd9c01da717c84ac50590e46af3fd193e2835690973e67d0cfbd809d1",
}
# The inherited V1 manifest is pinned by the closed V2 manifest.
roots = []
for rel, sha in pinned.items():
    p = HERE / rel
    assert pin(p)["raw_sha256"] == sha, p
    roots.append(pin(p))
    verify(load(p))
v1 = HERE / "independent-header-source90/closed-raw-manifest.header-source90.native.json"
verify(load(v1))
roots.append(pin(v1))
math = HERE / "independent-header-math90/decision90.json"
source = HERE / "independent-header-source90/header90.source-decision.v2.native.json"
m, s = load(math), load(source)
assert m["status"] == "ACCEPT_PROSPECTIVE_WHOLE_HEADER_V2_MATHEMATICS_TYPE_AND_SOURCE_TOPOLOGY_ONLY"
assert not m["required_repairs"] and s["verdict"] == "equivalent-after-elaboration"
assert not s["repairs"] and not s["blocking_deltas"]
assert m["reviewer_id"] != s["reviewer"]
expected = "5c976dcfe91fe074db71ddbf13385086735c41c273e937b0c6ef432b7dba9037"
assert m["header"]["raw_sha256"] == s["header"]["raw_sha256"] == expected
assert pin(HERE / "header90.v2.proposed.lean")["raw_sha256"] == expected
target = HERE / "root.preproof90.authorization.json"
assert not target.exists()
target.write_text(json.dumps({
    "status": "DISTINCT_CURRENT_HEADER_MATH_SOURCE_AND_TOPOLOGY_ACCEPTED_BEFORE_SEAL",
    "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "all_independent_reviews_accepted": True, "accepted_header_raw_sha256": expected,
    "math_decision": pin(math)["path"], "source_decision": pin(source)["path"],
    "closed_evidence": roots, "checked_RAW_descriptors": checked,
    "statement_sealed": False, "proof_BODY_created": False, "SAU_claimed": False,
    "scope": "Prospective bounded statement only; full A7, main theorem and Goal remain OPEN."
}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8", newline="\n")
print(json.dumps({"status": "PREPROOF90_ACCEPTED", "RAW_descriptors": len(checked), "authorization": pin(target)}))
