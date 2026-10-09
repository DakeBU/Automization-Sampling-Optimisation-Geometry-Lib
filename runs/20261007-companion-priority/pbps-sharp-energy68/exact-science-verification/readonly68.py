import os,sys,json
from pathlib import Path
import verify68 as R
O=R.O;get=R.get;pin=R.pin;mode=sys.argv[1];run=get('run.json');assert R.logical(run)==run['run_sha256']
for key in ['named_complete_RAW_review','outputs_manifest','input_manifest','Git_blob_manifest','native_verdict']:R.checkpin(run[key])
for q in get('outputs.manifest.json')['rows']:R.checkpin(q)
m=get('inputs.manifest.json');assert m['input_count']==len(m['reference_pins'])
for q in get('Git.blobs.manifest.json')['files']:
 b=R.git('show',R.SCI+':'+q['relative_path']);assert R.sha(b)==q['Git_RAW_sha256'];expected=q['workspace_pin']['raw_sha256'] if q['relation']=='exact RAW' else q['workspace_pin']['lf_sha256'];assert R.sha(b)==expected
 if 'exact_Git_RAW_snapshot' in q:R.checkpin(q['exact_Git_RAW_snapshot'])
if mode=='preclose':R.finalchecks();lease=None
elif mode=='postclose':
 lease=get('lease.final.json');assert lease['status']=='CLOSED_LAST';files={p.relative_to(O).as_posix() for p in O.rglob('*') if p.is_file()};listed={Path(q['path']).relative_to(O).as_posix() for q in lease['all_owned_outputs_except_only_self']}|{'lease.final.json'};assert files==listed and len(files)==lease['owned_file_count_including_self']
 for q in lease['all_owned_outputs_except_only_self']:R.checkpin(q)
else:raise ValueError(mode)
print(json.dumps(dict(status='PASS',mode=mode,actual_readonly_validator_PID=os.getpid(),whole_logical_run_sha256=run['run_sha256'],complete_named_RAW=pin(O/'named-verification.payload.json'),lease_RAW=pin(O/'lease.final.json') if lease else None,owned_file_count=len([p for p in O.rglob('*') if p.is_file()]),owned_writes=0,VERIFIED=False)))
