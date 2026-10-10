from pathlib import Path
import json,hashlib,os
O=Path(__file__).parent;H=lambda b:hashlib.sha256(b).hexdigest();d=json.loads((O/'review-run.json').read_bytes());v=d.pop('run_sha256');assert H(json.dumps(d,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode())==v
for n in ['foreground.finalizer.receipt.json','foreground.readback.receipt.json']:
 q=json.loads((O/n).read_bytes());assert q['actual_exit_code']==0 and q['terminal_closed']
for x in d['pre_finalizer_all_owned_file_bindings']:assert H((O/x['name']).read_bytes())==x['RAW_sha256']
assert not (O/'lease.final.json').exists();assert not (O/'owned-manifest.json').exists();print(json.dumps(dict(schema='diagnosis66-foreground-close-validator-v1',actual_foreground_pid=os.getpid(),all_assertions_passed=True,logical_run_sha256=v,no_existing_closed_lease=True),sort_keys=True),flush=True)
