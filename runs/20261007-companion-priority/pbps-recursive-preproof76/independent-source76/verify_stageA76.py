"""Read-only verifier of frozen source-only stageA; never reads candidate files."""
import sys
sys.dont_write_bytecode=True
import hashlib,json,os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
OWN=Path(__file__).resolve().parent
def sha(b): return hashlib.sha256(b).hexdigest()
def check(path,pin):
    b=path.read_bytes(); lf=b.replace(b"\r\n",b"\n")
    assert len(b)==pin["RAW_bytes"] and sha(b)==pin["RAW_sha256"],str(path)
    assert len(lf)==pin["LF_bytes"] and sha(lf)==pin["LF_sha256"],str(path)
    return b
f=json.loads((OWN/"stageA.freeze76.json").read_bytes())
assert f["frozen_before_any76_header_or_body"] and not f["prior76_review_decisions_visible"]
for value in f["artifacts"].values(): check(ROOT/value["path"],value)
manifest=json.loads((OWN/"source-first76.input-manifest.json").read_bytes())
for value in manifest["inputs"]:
    check(ROOT/value["snapshot_path"],value)
primary=check(OWN/"inputs/primary-pbps.exactraw.snapshot.html",f["source_pin"])
inv=json.loads((OWN/"source-coverage-inventory76.json").read_bytes())
for x in inv["items"]:
    b=primary[slice(*x["primary_RAW_range"])]
    assert len(b)==x["RAW_bytes"] and sha(b)==x["RAW_sha256"]
    assert x["independent_reason"] and not x["public_binder_credit"] and not x["Lean_proof_credit"]
for value in manifest["derived_exact_primary_regions"]:
    assert check(ROOT/value["snapshot_path"],value)==primary[slice(*value["primary_RAW_range"])]
g=json.loads((OWN/"source-proof-graph76.json").read_bytes())
ids={x["id"] for x in g["nodes"]}; assert len(ids)==34
assert len(g["edges"])==75 and len({x["id"] for x in g["edges"]})==75
assert all(x["producer"] in ids and x["consumer"] in ids for x in g["edges"])
assert all(x["consumer"]=="N20" for x in g["edges"] if x["id"] in ["E25","E26"])
adj={x:[] for x in ids}
for x in g["edges"]:adj[x["producer"]].append(x["consumer"])
done=set(); active=set()
def visit(n):
    assert n not in active
    if n in done:return
    active.add(n)
    for m in adj[n]:visit(m)
    active.remove(n);done.add(n)
for n in ids:visit(n)
v=json.loads((OWN/"source-first76.validation.json").read_bytes())
assert all(v["checks"].values()) and v["literal_rendering_difference_count"]==0
assert inv["counts"]=={"EXCLUDED":24,"NODE":70,"classification_promotions":3,"items":94,"math_items":58,"regions":11}
b=json.loads((OWN/"source-boundary76.json").read_bytes())
assert len(b["original_six_callers"])==6 and len(b["typing_classes"])==5 and len(b["internal_proof_ingredients"])==13
print(json.dumps({"status":"PASS_READONLY_STAGEA76","freeze_RAW_sha256":sha((OWN/"stageA.freeze76.json").read_bytes()),"counts":inv["counts"],"graph_counts":g["counts"],"writer_pid":f["writer_pid"],"verifier_pid":os.getpid(),"verifier_readonly":True,"candidate_read":False},sort_keys=True))
