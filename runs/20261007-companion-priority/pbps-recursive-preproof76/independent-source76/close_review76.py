"""Foreground final closer. lease.final.json is the last write; no post-close writes."""
import sys
sys.dont_write_bytecode=True
import os,json,hashlib,datetime,argparse
from pathlib import Path
OWN=Path(__file__).resolve().parent
assert not (OWN/"lease.final.json").exists(), "CLOSED directory is immutable"
def sha(b):return hashlib.sha256(b).hexdigest()
def compact(o):return json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode("utf-8")
def pin(b):
    lf=b.replace(b"\r\n",b"\n")
    return {"RAW_bytes":len(b),"RAW_sha256":sha(b),"LF_bytes":len(lf),"LF_sha256":sha(lf)}
def write(n,o):
    b=(json.dumps(o,ensure_ascii=False,sort_keys=True,indent=2)+"\n").encode("utf-8");(OWN/n).write_bytes(b);return b
run=json.loads((OWN/"source.0.run.json").read_bytes())
args=argparse.ArgumentParser()
args.add_argument("--observed-review-exit",required=True,type=int)
args.add_argument("--review-terminal-chunk",required=True)
args=args.parse_args()
assert args.observed_review_exit==0
review_writer_pid=run["writer_pid"]
claimed=run["run_sha256"];body={k:v for k,v in run.items() if k!="run_sha256"}
assert sha(compact(body))==claimed
# The review builder has already returned terminalEXIT0 in the foreground tool.
write("review76.execution-receipt.json",{"review_writer_pid":review_writer_pid,"actual_terminal_exit":args.observed_review_exit,"terminal_chunk":args.review_terminal_chunk,"source_first_writer_pid":29040,"source_first_terminal_exit":0,"source_first_readonly_verifier_pid":3188,"source_first_verifier_exit":0,"source_first_verifier_chunk":"dcdf81","review_status":"ACCEPT_PROSPECTIVE_SOURCE_HEADER_ONLY","no_compiler_or_implementation_claim":True,"final_closer_pid":os.getpid(),"final_closer_exit_contract":0,"final_exit_observation":"Actual close terminal exit must be checked externally after this foreground process returns; readonly verifier requires --observed-close-exit 0."})
files=[]
for p in sorted(OWN.rglob("*"),key=lambda p:str(p.relative_to(OWN)).replace("\\","/")):
    if p.is_file() and p.name not in ["whole-owned.manifest.json","lease.final.json"]:
        files.append({"owned_relative_path":str(p.relative_to(OWN)).replace("\\","/"),**pin(p.read_bytes())})
logical={"schema":"whole-owned-review-logical-run-v1","files":files}
whole=sha(compact(logical))
manifest=write("whole-owned.manifest.json",{"schema":"whole-owned-manifest-v1","files":files,"owned_files_excluding_manifest_and_lease":len(files),"whole_logical_run_sha256":whole,"whole_logical_run_recipe":"SHA256 compact sorted-key UTF8 JSON of {schema:whole-owned-review-logical-run-v1,files:the complete ordered file pin list}; final manifest and lease excluded to prevent circular hashes.","native_run_sha256":claimed,"complete_five_RAW_payload_sha256":sha((OWN/"complete-named-review-decision-input-payload.json").read_bytes()),"manifest_self_excluded_lease_binds_manifest":True})
leasefiles=files+[{"owned_relative_path":"whole-owned.manifest.json",**pin(manifest)}]
leasefiles.sort(key=lambda x:x["owned_relative_path"])
lease={"schema":"whole-owned-final-lease-v1","status":"CLOSED_LAST","closed_UTC":datetime.datetime.now(datetime.timezone.utc).isoformat(),"owned_directory":str(OWN),"close_writer_pid":os.getpid(),"close_writer_expected_terminal_exit":0,"actual_close_exit_evidence_location":"Foreground exec result and subsequent standalone readonly verifier, not a fictitious pre-exit observation.","review_writer_pid":review_writer_pid,"review_writer_actual_terminal_exit":0,"source_first_writer_pid":29040,"source_first_writer_actual_terminal_exit":0,"files":leasefiles,"all_other_owned_files_bound_RAW_and_LF":True,"owned_file_count_including_lease":len(leasefiles)+1,"manifest_RAW_sha256":sha(manifest),"native_run_sha256":claimed,"run_RAW_sha256":sha((OWN/"source.0.run.json").read_bytes()),"complete_five_RAW_payload_sha256":sha((OWN/"complete-named-review-decision-input-payload.json").read_bytes()),"whole_logical_run_sha256":whole,"no_further_writes":True,"write_order":"lease.final.json CLOSED_LAST is written after every other owned file; this process performs no further filesystem writes.","review_scope":"PROSPECTIVE_SOURCE_HEADER_ONLY; no implementation76/SAU/VERIFIED/official source-body admission."}
raw=write("lease.final.json",lease)
# CLOSED_LAST has been written. From this point onward only stdout and process exit.
print(json.dumps({"status":"CLOSED_LAST","close_writer_pid":os.getpid(),"expected_terminal_exit":0,"owned_file_count":len(leasefiles)+1,"native_run_sha256":claimed,"run_RAW_sha256":lease["run_RAW_sha256"],"lease_RAW_sha256":sha(raw),"complete_five_RAW_payload_sha256":lease["complete_five_RAW_payload_sha256"],"whole_logical_run_sha256":whole},sort_keys=True))
