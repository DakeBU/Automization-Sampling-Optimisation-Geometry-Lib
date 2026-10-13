from pathlib import Path
import json,hashlib
r=Path(__file__).parent;d=r/'independent-math87';sha=lambda b:hashlib.sha256(b).hexdigest();load=lambda p:json.loads(Path(p).read_bytes())
assert sha((d/'decision87.json').read_bytes())=='48ed04f32f4d1f4f07d3f122730dfe01bf178744b745fd4f932a895ed4d99986'
assert sha((d/'closed-RAW-manifest87.json').read_bytes())=='b43b0e0279c27278b84e7a615a7882e5cb3023de596a6207897945424abc0ee6'
seen=[]
def verify(x):
 if isinstance(x,dict):
  if 'path' in x and 'raw_sha256' in x:
   p=Path(x['path']);b=p.read_bytes();assert sha(b)==x['raw_sha256'],p
   if 'bytes' in x:assert len(b)==x['bytes'],p
   seen.append(x['path'])
  for v in x.values():verify(v)
 elif isinstance(x,list):
  for v in x:verify(v)
n=load(d/'decision87.json');verify(load(d/'closed-RAW-manifest87.json'));verify(n)
assert n['status']=='ACCEPTED_INDEPENDENT_MATHEMATICS_ONLY' and n['reviewer_id']=='/root/exact_verify77'
assert n['required_mathematical_repairs']==[] and n['standard_axioms_only'] and n['all21collaborator_RAWs_preserved']
for x in n['terminal_receipts']:assert load(x['path'])['exit_code']==0
p=r/'root.math87.adoption.json';assert not p.exists()
p.write_text(json.dumps(dict(status='ACCEPTED_INDEPENDENT_MATH_ONLY',native_decision_SHA256=sha((d/'decision87.json').read_bytes()),native_closed_manifest_SHA256=sha((d/'closed-RAW-manifest87.json').read_bytes()),exact_descriptors_rechecked=len(seen),checked_module=n['checked_module'],reviewer=n['reviewer_id'],exposition_overlay_pending_distinct_review=True,PROVED_LOCAL=False,VERIFIED=False),ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print('Independent math RAW closure adopted;',len(seen),'descriptors; no VERIFIED transition.')
