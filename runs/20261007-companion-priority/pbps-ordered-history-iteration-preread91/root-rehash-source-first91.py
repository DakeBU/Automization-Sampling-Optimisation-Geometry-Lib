from pathlib import Path
import datetime, hashlib, json

base = Path(__file__).parent
p = base / "independent-source-first91"
manifest = p / "closed-raw-manifest.source-first91.v2.native.json"
assert hashlib.sha256(manifest.read_bytes()).hexdigest() == "82aaa96abf20592b355b594e478784032b6ce604ff060136d4d0df8242695d2b"
j = json.loads(manifest.read_bytes())
assert j["closed"] and not j["creator_self_independent_approval"]
checked = {}
def verify(x):
    if isinstance(x, dict):
        if "path" in x and "raw_sha256" in x:
            b = Path(x["path"]).read_bytes()
            actual = hashlib.sha256(b).hexdigest()
            assert actual == x["raw_sha256"], (x["path"], actual, x["raw_sha256"])
            if "bytes" in x:
                assert len(b) == x["bytes"], x["path"]
            checked[x["path"]] = {"raw_sha256": actual, "bytes": len(b)}
        for v in x.values():
            verify(v)
    elif isinstance(x, list):
        for v in x:
            verify(v)
verify(j)
out = base / "root.source-first91.rehash.json"
assert not out.exists()
out.write_text(json.dumps({
    "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "creator_manifest": str(manifest).replace("\\", "/"),
    "creator_manifest_sha256": hashlib.sha256(manifest.read_bytes()).hexdigest(),
    "checked": checked,
    "scope": "RAW closure binding only. Distinct topology review pending; no mathematical admission, header, Seal, claim or proof.",
    "Goal_status": "active",
}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
print(json.dumps({"checked_RAW": len(checked), "receipt": str(out)}))
