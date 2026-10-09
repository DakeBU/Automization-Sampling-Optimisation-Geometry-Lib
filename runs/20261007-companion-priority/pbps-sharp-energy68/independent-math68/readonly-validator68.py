import sys,os,json,hashlib
from pathlib import Path
import review68 as R
O=R.O;pin=R.pin;sha=R.sha;get=R.get
mode=sys.argv[1];run=get('run.json');v=dict(run);expected=v.pop('run_sha256');assert sha(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())==expected
assert pin(run['native_named_complete_RAW_payload']['path'])==run['native_named_complete_RAW_payload']
assert pin(run['outputs_manifest']['path'])==run['outputs_manifest']
for p in get('outputs.manifest.json')['rows']:assert pin(p['path'])==p,('output drift',p['path'])
for n in ['leaf.inputs.manifest.json','final.inputs.manifest.json','audit.inputs.manifest.json','overlay.inputs.manifest.json','resolution.inputs.manifest.json']:
 m=get(n);assert m['input_count']==len(m['inputs'])
 for q in m['inputs']:
  assert pin(q['RAW_snapshot']['path'])==q['RAW_snapshot'] and pin(q['LF_snapshot']['path'])==q['LF_snapshot']
  b=Path(q['RAW_snapshot']['path']).read_bytes();l=Path(q['LF_snapshot']['path']).read_bytes();assert b.replace(b'\r\n',b'\n')==l and sha(b)==q['original']['raw_sha256']
for n in ['leaf','main','test']:assert get(f'{n}.compiler.receipt.json')['exit_code']==0
if mode=='preclose':
 import final68 as F
 F.stable();lease=None;count=len([p for p in O.rglob('*') if p.is_file()])
elif mode=='postclose':
 lease=get('lease.final.json');assert lease['status']=='CLOSED_LAST'
 files={p.relative_to(O).as_posix():p for p in O.rglob('*') if p.is_file()};rows=lease['all_owned_outputs_except_only_self'];assert set(files)=={Path(q['path']).relative_to(O).as_posix() for q in rows}|{'lease.final.json'}
 for q in rows:assert pin(q['path'])==q,('closed output drift',q['path'])
 assert lease['owned_file_count_including_self']==len(files);count=len(files)
else:raise ValueError(mode)
print(json.dumps(dict(status='PASS',mode=mode,actual_readonly_validator_PID=os.getpid(),exit_code_if_returned=0,owned_file_count=count,whole_logical_run_sha256=expected,named_complete_RAW_payload=pin(O/'named-mathematical-review.payload.json'),lease=pin(O/'lease.final.json') if lease else None,owned_writes=0)))
