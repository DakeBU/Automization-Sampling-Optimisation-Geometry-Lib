import json,hashlib
from pathlib import Path
b=Path('runs/20261007-companion-priority/pbps-macroscopic-centered-range58/reader-controls58'); n=b/'independent-review'
load=lambda p:json.loads(p.read_text(encoding='utf-8'))
sha=lambda x:hashlib.sha256(x).hexdigest()
can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
r=load(n/'run.json');l=load(n/'lease.json'); seen=set()
assert r['native_schema']=='independent-scoped-reader-controls-repair-run'
assert sha(can({k:v for k,v in r.items() if k!='run_sha256'}))==r['run_sha256']
assert sha(can(r['reader_controls_repair_payload']))==r['reader_controls_repair_payload_sha256']==l['reader_controls_repair_payload_sha256']
assert l['status']=='CLOSED' and l['last_filesystem_operation'] and l['resource']['validator_actual_exit_code']==0
assert not l['full_reader_accepted'] and not l['PURIFIED']
def walk(x):
 if isinstance(x,dict):
  if 'path' in x and 'raw_sha256' in x:
   key=(x['path'],x['raw_sha256'],x.get('lf_sha256'))
   if key not in seen:
    p=Path(x['path']); a=p.read_bytes();z=a.replace(b'\r\n',b'\n');assert sha(a)==x['raw_sha256'],p
    if 'lf_sha256' in x: assert sha(z)==x['lf_sha256'],p
    for field,v in [('raw_bytes',len(a)),('bytes',len(a)),('lf_bytes',len(z))]:
     if field in x: assert x[field]==v,p
    seen.add(key)
  for v in x.values():walk(v)
 elif isinstance(x,list):
  for v in x:walk(v)
for fn in ['run.json','lease.json','reader-controls.review.json','input.manifest.json','output.manifest.json','validator.json','complete.json']: walk(load(n/fn))
p=r['reader_controls_repair_payload'];assert p['status']=='ACCEPT_SCOPED_READER_CONTROLS_REPAIR' and p['typed_prior_blocker_resolved_for_current_rendered_three_rows']
out=dict(status='STRICT_NATIVE_SCOPED_READER_REPAIR_ADOPTED',actor='companion_root_20261005',run_sha256=r['run_sha256'],named_payload_sha256=r['reader_controls_repair_payload_sha256'],unique_qualified_pin_readbacks=len(seen),scope='Current three rows copy/download controls only. Original negative preserved; broader reader and purification acceptance remain open.',full_reader_accepted=False,PURIFIED=False)
pth=b/'root.adoption.json';assert not pth.exists();pth.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n'); print(json.dumps(out))
