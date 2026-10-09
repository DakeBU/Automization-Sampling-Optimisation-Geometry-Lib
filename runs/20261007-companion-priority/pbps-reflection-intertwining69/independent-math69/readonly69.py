import os,sys,json
from pathlib import Path
import review69 as R
O=R.O;get=R.get;pin=R.pin;mode=sys.argv[1];run=get('run.json');assert R.logical(run)==run['run_sha256']
for k in ['input_manifest','native_mathematical_review','complete_decision','named_complete_RAW_review','outputs_manifest']:R.checkpin(run[k])
for q in get('outputs.manifest.json')['rows']:R.checkpin(q)
m=get('inputs.manifest.json');assert m['input_count']==len(m['inputs']) and m['original_frozen_input_count']==22
for row in m['inputs']:
 R.checkpin(row['RAW_snapshot']);R.checkpin(row['LF_snapshot']);raw=Path(row['RAW_snapshot']['path']).read_bytes();assert R.sha(raw)==row['original']['raw_sha256'] and raw.replace(b'\r\n',b'\n')==Path(row['LF_snapshot']['path']).read_bytes()
review=get('mathematical-review.json');src=Path(next(x['RAW_snapshot']['path'] for x in m['inputs'] if x['original']['path']==R.CODE.as_posix())).read_bytes()
for region in review['implementation_BODY_regions']:
 b=src[region['start_byte']:region['end_byte_exclusive']];assert R.sha(b)==region['region_RAW_sha256'] and len(b)==region['region_RAW_bytes']
if mode=='preclose':R.stable();lease=None
elif mode=='postclose':
 lease=get('lease.final.json');assert lease['status']=='CLOSED_LAST';files={p.relative_to(O).as_posix() for p in O.rglob('*') if p.is_file()};listed={Path(q['path']).relative_to(O).as_posix() for q in lease['all_owned_outputs_except_only_self']}|{'lease.final.json'};assert files==listed and len(files)==lease['owned_file_count_including_self']
 for q in lease['all_owned_outputs_except_only_self']:R.checkpin(q)
else:raise ValueError(mode)
print(json.dumps(dict(status='PASS',mode=mode,actual_readonly_validator_PID=os.getpid(),whole_logical_run_sha256=run['run_sha256'],complete_named_RAW=pin(O/'named-mathematical-review.payload.json'),lease_RAW=pin(O/'lease.final.json') if lease else None,owned_file_count=len([p for p in O.rglob('*') if p.is_file()]),owned_writes=0,VERIFIED=False)))
