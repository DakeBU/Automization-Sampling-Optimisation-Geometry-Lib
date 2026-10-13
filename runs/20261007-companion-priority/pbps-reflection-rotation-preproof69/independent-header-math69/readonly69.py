import os,sys,json
from pathlib import Path
import review69 as R
O=R.O;get=R.get;pin=R.pin;sha=R.sha;mode=sys.argv[1];run=get('run.json');v=dict(run);expected=v.pop('run_sha256');assert sha(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())==expected
assert pin(run['named_complete_RAW_review']['path'])==run['named_complete_RAW_review'] and pin(run['outputs_manifest']['path'])==run['outputs_manifest']
for q in get('outputs.manifest.json')['rows']:assert pin(q['path'])==q
m=get('inputs.manifest.json');assert m['input_count']==len(m['inputs'])==14
for q in m['inputs']:
 assert pin(q['RAW_snapshot']['path'])==q['RAW_snapshot'] and pin(q['LF_snapshot']['path'])==q['LF_snapshot'];b=Path(q['RAW_snapshot']['path']).read_bytes();assert sha(b)==q['original']['raw_sha256'] and b.replace(b'\r\n',b'\n')==Path(q['LF_snapshot']['path']).read_bytes()
if mode=='preclose':R.stable();lease=None
elif mode=='postclose':
 lease=get('lease.final.json');assert lease['status']=='CLOSED_LAST';files={p.relative_to(O).as_posix() for p in O.rglob('*') if p.is_file()};assert files=={Path(q['path']).relative_to(O).as_posix() for q in lease['all_owned_outputs_except_only_self']}|{'lease.final.json'}
 for q in lease['all_owned_outputs_except_only_self']:assert pin(q['path'])==q
 assert lease['owned_file_count_including_self']==len(files)
else:raise ValueError(mode)
print(json.dumps(dict(status='PASS',mode=mode,actual_readonly_validator_PID=os.getpid(),whole_logical_run_sha256=expected,complete_named_RAW=pin(O/'named-header-review.payload.json'),lease_RAW=pin(O/'lease.final.json') if lease else None,owned_file_count=len([p for p in O.rglob('*') if p.is_file()]),owned_writes=0)))
