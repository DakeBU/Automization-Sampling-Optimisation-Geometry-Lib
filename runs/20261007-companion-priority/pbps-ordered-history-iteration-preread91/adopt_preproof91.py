from pathlib import Path
import datetime, hashlib, json

base = Path(__file__).parent
checked = {}
def pin(p):
    p = Path(p)
    b = p.read_bytes()
    return {"path": str(p).replace("\\", "/"), "raw_sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)}
def verify(x):
    if isinstance(x, dict):
        sha = x.get("raw_sha256", x.get("sha256"))
        if "path" in x and sha:
            d = pin(x.get("closed_snapshot", x["path"]))
            assert d["raw_sha256"] == sha, (x["path"], d["raw_sha256"], sha)
            assert d["bytes"] == x.get("bytes", d["bytes"]), x["path"]
            checked[d["path"]] = d
        for v in x.values():
            verify(v)
    elif isinstance(x, list):
        for v in x:
            verify(v)
def load(name, sha):
    p = base / name
    assert pin(p)["raw_sha256"] == sha, p
    j = json.loads(p.read_bytes())
    verify(j)
    return j
load("independent-header-math91/closed-RAW-manifest91.authoritative.json",
     "f281308150b7e86ab7e5f62fea66b358a4f5a76569f2ca5922345358031ecf13")
load("independent-header-source91/closed-raw-manifest.header-source91.native.json",
     "53155fe75be44ff03b7ca735e784a039a10c233a01a6dda860fada73873f119e")
math = load("independent-header-math91/decision91.json",
            "e69acbd40ab2c340347d1295cd58477cacf0ef5b882f61238bdb25b90aa2c528")
source = load("independent-header-source91/header91.source-decision.native.json",
              "fc38b211840a024c6b6dee4664ffa33ad9807e997edca891c279871630685959")
assert math["status"] == "ACCEPT_INDEPENDENT_WHOLE_HEADER_MATHEMATICS_AND_TYPE_ONLY"
assert math["reviewer_id"] == "/root/exact_verify77"
assert math["required_repairs"] == [] and math["native_typechecks_exit_codes"] == [0, 0]
assert source["reviewer"] == "/root/fresh_source87"
assert source["verdict"] == "equivalent-after-elaboration" and source["repairs"] == []
assert source["analytic_binder_count"] == 6 and source["literal_definition_count"] == 35
header = pin(base / "header91.proposed.lean")
assert header["raw_sha256"] == "b8bba160f6134c7927167a0a34d99971ce75023ef7ea04f738a91b6862da2680"
assert math["header"]["raw_sha256"] == header["raw_sha256"] == source["header"]["raw_sha256"]
assert ":= by" not in (base / "header91.proposed.lean").read_text(encoding="utf-8")
out = base / "root.preproof91.authorization.json"
assert not out.exists()
out.write_text(json.dumps({
    "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "all_independent_reviews_accepted": True,
    "accepted_header_raw_sha256": header["raw_sha256"], "header": header,
    "math_decision": pin(base / "independent-header-math91/decision91.json"),
    "source_decision": pin(base / "independent-header-source91/header91.source-decision.native.json"),
    "source_adoption": pin(base / "root.source91.adoption.json"),
    "closed_evidence": [
        pin(base / "independent-header-math91/closed-RAW-manifest91.authoritative.json"),
        pin(base / "independent-header-source91/closed-raw-manifest.header-source91.native.json"),
    ],
    "checked_RAW": list(checked.values()), "StatementSeal": False,
    "SAU_claim": False, "Lean_BODY": False, "proof_credit": False,
    "scope": "Whole exact prospective Prop accepted for subsequent Seal/claim only. Original failures, closures and source-first chronology immutable.",
}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
print(json.dumps({"checked_RAW": len(checked), "authorization": pin(out)}))
