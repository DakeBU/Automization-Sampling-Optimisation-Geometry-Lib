import os,sys,json
from pathlib import Path
import verify69 as R
O=R.O;get=R.get;pin=R.pin;run=get('run.json');assert R.logical(run)==run['run_sha256']
for k in ['input_manifest','Git_blob_manifest','native340_Git_manifest','native_verdict','named_complete_RAW_review','outputs_manifest','transition_receipt','shared_verified_output']:R.checkpin(run[k])
for q in get('outputs.manifest.json')['rows']:R.checkpin(q)
m=get('inputs.manifest.json');assert m['input_count']==len(m['inputs'])
for row in m['inputs']:
 if 'RAW_snapshot' in row:
  R.checkpin(row['RAW_snapshot']);R.checkpin(row['LF_snapshot']);raw=Path(row['RAW_snapshot']['path']).read_bytes();assert R.sha(raw)==row['original']['raw_sha256'] and raw.replace(b'\r\n',b'\n')==Path(row['LF_snapshot']['path']).read_bytes()
 else:R.checkpin(row['original'])
q=get('ledger.after.pin.json');b=(R.ROOT/'runs/substantive_advances.jsonl').read_bytes();assert len(b)>=q['raw_bytes'] and R.sha(b[:q['raw_bytes']])==q['raw_sha256'];mode=sys.argv[1];lease=None
if mode=='preclose':R.finalchecks()
elif mode=='postclose':
 lease=get('lease.final.json');assert lease['status']=='CLOSED_LAST';files={p.relative_to(O).as_posix() for p in O.rglob('*') if p.is_file()};listed={Path(q['path']).relative_to(O).as_posix() for q in lease['all_owned_outputs_except_only_self']}|{'lease.final.json'};assert files==listed and len(files)==lease['owned_file_count_including_self']
 for q in lease['all_owned_outputs_except_only_self']:R.checkpin(q)
else:raise ValueError(mode)
print(json.dumps(dict(status='PASS',mode=mode,actual_readonly_validator_PID=os.getpid(),verified_commit=R.SCI,whole_logical_run_sha256=run['run_sha256'],complete_named_RAW=pin(O/'named-verification.payload.json'),lease_RAW=pin(O/'lease.final.json') if lease else None,owned_file_count=len([p for p in O.rglob('*') if p.is_file()]),owned_writes=0)))
