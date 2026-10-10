"""Standalone read-only CLOSED76 verifier. Writes nothing, including bytecode."""
import sys
sys.dont_write_bytecode=True
import json,hashlib,os,argparse
from pathlib import Path
OWN=Path(__file__).resolve().parent
ROOT=OWN.parents[3]
def sha(b):return hashlib.sha256(b).hexdigest()
def compact(o):return json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode("utf-8")
def pins(b):
    lf=b.replace(b"\r\n",b"\n")
    return {"RAW_bytes":len(b),"RAW_sha256":sha(b),"LF_bytes":len(lf),"LF_sha256":sha(lf)}
def check(p,v):
    b=p.read_bytes();assert pins(b)=={k:v[k] for k in pins(b)},str(p);return b
def load(n):return json.loads((OWN/n).read_bytes())
args=argparse.ArgumentParser()
args.add_argument("--observed-close-exit",required=True,type=int)
args=args.parse_args()
assert args.observed_close_exit==0
lease=load("lease.final.json");manifest=load("whole-owned.manifest.json")
assert lease["status"]=="CLOSED_LAST" and lease["no_further_writes"]
actual={str(p.relative_to(OWN)).replace("\\","/") for p in OWN.rglob("*") if p.is_file()}
assert actual=={x["owned_relative_path"] for x in lease["files"]}|{"lease.final.json"}
assert actual=={x["owned_relative_path"] for x in manifest["files"]}|{"whole-owned.manifest.json","lease.final.json"}
for p in lease["files"]:check(OWN/p["owned_relative_path"],p)
assert lease["manifest_RAW_sha256"]==sha((OWN/"whole-owned.manifest.json").read_bytes())
logical={"schema":"whole-owned-review-logical-run-v1","files":manifest["files"]}
whole=sha(compact(logical))
assert whole==manifest["whole_logical_run_sha256"]==lease["whole_logical_run_sha256"]
run=load("source.0.run.json");run_sha=run.pop("run_sha256")
assert sha(compact(run))==run_sha==lease["native_run_sha256"]
for value in run["artifacts"].values():check(ROOT/value["path"],value)
complete=load("complete-named-review-decision-input-payload.json")
expected=["source.0.run.json","source.0.decision.json","source.0.review.json","source.0.input-manifest.json","source.0.admission-fields.json"]
assert complete["payload_count"]==5 and [x["name"] for x in complete["named_RAW_payloads"]]==expected
for p in complete["named_RAW_payloads"]:
    raw=p["RAW_payload_utf8"].encode("utf-8")
    assert raw==(OWN/p["name"]).read_bytes() and pins(raw)=={k:p[k] for k in pins(raw)}
f=load("stageA.freeze76.json");assert sha((OWN/"stageA.freeze76.json").read_bytes())=="2261177fd6b375113aaa262d0dc0a4908f07e85a9fc84e4f045b69623f724c91"
for v in f["artifacts"].values():check(ROOT/v["path"],v)
primary=check(OWN/"inputs/primary-pbps.exactraw.snapshot.html",f["source_pin"])
coverage=load("source-coverage-inventory76.json")
assert coverage["counts"]=={"EXCLUDED":24,"NODE":70,"classification_promotions":3,"items":94,"math_items":58,"regions":11}
for x in coverage["items"]:
    b=primary[slice(*x["primary_RAW_range"])]
    assert len(b)==x["RAW_bytes"] and sha(b)==x["RAW_sha256"]
    assert x["independent_reason"] and not x["public_binder_credit"] and not x["Lean_proof_credit"]
im=load("source.0.input-manifest.json")
for v in im["source_first_manifest"]["inputs"]+im["candidate_and_parent_full_RAW_snapshots"]:check(ROOT/v["snapshot_path"],v)
review=load("source.0.review.json")
assert set(review["semantic_slots"])=={"objects","domains","quantifiers","assumptions","conclusion","scopes","constant_dependencies"}
assert len(review["full_exhaustive_source_coverage"])==94 and len(review["all_thirteen_internal_proof_ingredients"])==13
assert not review["repairs"] and review["blocking_delta_count"]==0
header=(OWN/"inputs/candidate-and-parent/header76.v3.proposed.lean").read_bytes()
assert sha(header)=="996b8a89ffe84cfef8faf75551f962f2378db221841f5e1a38137eb81281d015"
for x in review["literal_definition_audit"]+review["conclusion_group_audit"]:
    b=header[slice(*x["header_RAW_range"])]
    assert b==x["RAW_utf8"].encode("utf-8") and pins(b)=={k:x[k] for k in pins(b)}
neutral=load("header76.neutral-expanded-binder-inventory.json")
def clean(o):
    if isinstance(o,dict):
        assert not set(o)&{"semantic_slots","deltas","verdict","review_run_sha256"}
        for v in o.values():clean(v)
    elif isinstance(o,list):
        for v in o:clean(v)
clean(neutral)
assert neutral["counts"]=={"callers":6,"typing":5,"literal_definitions":11,"conclusion_groups":10}
a=load("source.0.admission-fields.json")
assert a["audit_fields"] is None and a["cell_source_proof_coverage"] is None and a["publication_source_proof_coverage"] is None
assert a["fresh_postcompile_source_review_required"]
assert load("source.0.decision.json")["status"]=="ACCEPT_PROSPECTIVE_SOURCE_HEADER_ONLY"
assert (OWN/"lease.final.json").stat().st_mtime_ns>=max((OWN/x).stat().st_mtime_ns for x in actual if x!="lease.final.json")
print(json.dumps({"status":"PASS_READONLY_CLOSED76","owned_files_including_manifest_and_lease":len(actual),"native_run_sha256":run_sha,"run_RAW_sha256":sha((OWN/"source.0.run.json").read_bytes()),"lease_RAW_sha256":sha((OWN/"lease.final.json").read_bytes()),"complete_five_RAW_payload_sha256":sha((OWN/"complete-named-review-decision-input-payload.json").read_bytes()),"whole_logical_run_sha256":whole,"source_counts":coverage["counts"],"header_counts":neutral["counts"],"review_writer_pid":lease["review_writer_pid"],"close_writer_pid":lease["close_writer_pid"],"observed_close_terminal_exit":args.observed_close_exit,"verifier_pid":os.getpid(),"verifier_readonly":True},sort_keys=True))
