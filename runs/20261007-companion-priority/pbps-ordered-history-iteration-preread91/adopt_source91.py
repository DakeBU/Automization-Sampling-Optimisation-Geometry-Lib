from pathlib import Path
import copy, datetime, hashlib, json, subprocess

base = Path(__file__).parent
checked = {}
def descriptor(p):
    p = Path(p)
    b = p.read_bytes()
    return {"path": str(p).replace("\\", "/"), "raw_sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)}
def walk(x):
    if isinstance(x, dict):
        digest = x.get("raw_sha256", x.get("sha256"))
        if "path" in x and digest:
            d = descriptor(x["path"])
            assert d["raw_sha256"] == digest, (x["path"], d["raw_sha256"], digest)
            assert d["bytes"] == x.get("bytes", d["bytes"]), x["path"]
            checked[d["path"]] = d
        for v in x.values():
            walk(v)
    elif isinstance(x, list):
        for v in x:
            walk(v)
def load(p, digest):
    d = descriptor(p)
    assert d["raw_sha256"] == digest, d
    j = json.loads(Path(p).read_bytes())
    walk(j)
    return j

load(base / "independent-source-first91/closed-raw-manifest.source-first91.v2.native.json",
     "82aaa96abf20592b355b594e478784032b6ce604ff060136d4d0df8242695d2b")
load(base / "independent-topology91/closed-RAW-manifest91.second-half.json",
     "9c260798f83dd9fc159090c6eae2b62524a4eb40621e38b806cf0fc5069859d4")
load(base / "independent-topology-repair91/closed-raw-manifest91.json",
     "5b6479bc239f24f2127e1de7b4692b367a6e737ec313363b8577bed7184bd242")
decision = load(base / "independent-topology-repair91/decision91.native.json",
                "a6537fc4fa9b1434e3bb241c3f5ead701545e6ceaf8cd26692547ea9e8001116")
assert decision["decision"] == "ACCEPT_EXACT_THREE_OPERATION_ROUTE_INDEXED_TOPOLOGY_OVERLAY91"
assert decision["reviewer_id"] == "/root/exposition_repair89"
assert decision["required_repairs"] == []
proposal = load(base / "independent-topology91/topology-route-overlay91.proposal.json",
                "829e39866b5eeed33de285e58a18df2bcdba47c10a09ade781554c6346286170")
original = json.loads(Path(proposal["target"]["path"]).read_bytes())
expected = copy.deepcopy(original)
assert len(proposal["operations"]) == 3
for op in proposal["operations"]:
    parts = op["path"].strip("/").split("/")
    node = expected
    for part in parts[:-1]:
        node = node[int(part)] if isinstance(node, list) else node[part]
    leaf = parts[-1]
    if op["op"] == "replace":
        assert node[leaf] == op["before"]
        node[leaf] = op["value"]
    else:
        assert op["op"] == "add" and leaf == "-" and isinstance(node, list)
        node.append(op["value"])
successor = Path(proposal["proposed_successor"]["path"])
assert expected == json.loads(successor.read_bytes())
assert descriptor(successor)["raw_sha256"] == "0a1351bbb9aeeb5556892fcf6c0265527fba38618f297a0a75b9ebef076de5c5"
baseline = json.loads((base / "pre-fetch91.workspace-RAW.json").read_bytes())
for path, digest in baseline["tracked_modified"].items():
    assert descriptor(path)["raw_sha256"] == digest, path
assert subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip() == baseline["HEAD"]
assert not subprocess.check_output(["git", "diff", "--cached", "--name-only"], text=True).strip()
accepted = base / "source-proof-graph91.accepted-successor.json"
out = base / "root.source91.adoption.json"
assert not accepted.exists() and not out.exists()
accepted.write_bytes(successor.read_bytes())
out.write_text(json.dumps({
    "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "status": "SOURCE_GRAPH_AND_BOUNDED_CANDIDATE_ADMITTED_FOR_PROSPECTIVE_HEADER_ONLY",
    "creator": "/root/fresh_source87", "topology_reviewer": "/root/exact_verify77",
    "distinct_repair_reviewer": "/root/exposition_repair89", "applicator": "/root",
    "accepted_graph": descriptor(accepted), "original_graph": proposal["target"],
    "exact_overlay": descriptor(base / "independent-topology91/topology-route-overlay91.proposal.json"),
    "distinct_repair_decision": descriptor(base / "independent-topology-repair91/decision91.native.json"),
    "unchanged_coverage": proposal["unchanged_coverage"],
    "unchanged_candidate": proposal["unchanged_candidate"],
    "checked_RAW": list(checked.values()),
    "exact_operations_only": True, "collaborator_RAWs_preserved": 21,
    "StatementSeal": False, "SAU_claim": False, "Lean_BODY": False,
    "mathematical_proof_or_full_A7_credit": False, "Goal_status": "active",
}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
print(json.dumps({"checked_RAW": len(checked), "accepted_graph": descriptor(accepted), "adoption": descriptor(out)}))
