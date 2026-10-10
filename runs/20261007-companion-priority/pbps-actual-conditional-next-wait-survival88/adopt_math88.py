from pathlib import Path
import json,hashlib
R=Path('E:/Samplinglib');r=Path(__file__).parent;d=r/'independent-math88';load=lambda p:json.loads(p.read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
assert sha((d/'decision88.json').read_bytes())=='b8e32034a4428559c4f85fab60fbf5393f12c3e7182be889d4768df8c35b1fa9'
assert sha((d/'closed-RAW-manifest88.json').read_bytes())=='bf9a452ef8c2de6d83b0fa6b1b4e89f07ca2cb26f7dc89005cb774984a2c4479'
seen=[]
def verify(x):
 if isinstance(x,dict):
  if 'path' in x and 'raw_sha256' in x:
   p=Path(x['path']);p=p if p.is_absolute() else R/p;b=p.read_bytes()
   assert sha(b)==x['raw_sha256'],p
   if 'bytes' in x:assert len(b)==x['bytes'],p
   seen.append(str(p))
  for v in x.values():verify(v)
 elif isinstance(x,list):
  for v in x:verify(v)
n=load(d/'decision88.json');verify(load(d/'closed-RAW-manifest88.json'));verify(n)
assert n['status']=='ACCEPTED_INDEPENDENT_MATHEMATICS_ONLY' and n['reviewer_id']=='/root/exact_verify77'
assert n['required_repairs']==n['blocking_findings']==[] and n['standard_axioms_only'] and n['collaborator_21_RAW_preserved']
for k in ['focused_compile','fresh_complete_source_and_kernel']:
 assert load(R/n[k]['path'])['exit_code']==0
p=r/'root.math88.adoption.json';assert not p.exists();p.write_text(json.dumps(dict(status='ACCEPTED_INDEPENDENT_MATH_ONLY',native_decision_SHA256=sha((d/'decision88.json').read_bytes()),native_closed_manifest_SHA256=sha((d/'closed-RAW-manifest88.json').read_bytes()),exact_descriptors_rechecked=len(seen),checked_module=n['module'],reviewer=n['reviewer_id'],exposition_accepted=True,exposition_repairs_required=False,PROVED_LOCAL=False,VERIFIED=False),indent=2)+'\n',encoding='utf8',newline='\n')
print('Independent whole mathematics/kernel/5exposition regions accepted;',len(seen),'RAW descriptors; no VERIFIED transition.')
