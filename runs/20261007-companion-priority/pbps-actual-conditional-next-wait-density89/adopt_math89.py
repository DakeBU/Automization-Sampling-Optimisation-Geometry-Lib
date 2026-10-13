from pathlib import Path
import hashlib,json
R=Path('E:/Samplinglib');r=Path(__file__).parent;d=r/'independent-math89'
load=lambda p:json.loads(p.read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
dp=d/'decision89.json';mp=d/'closed-RAW-manifest89.authoritative.json'
assert sha(dp.read_bytes())=='447f52af66ad16531b60de6753149048ab36c1843ce622ca6783165b928f4832'
assert sha(mp.read_bytes())=='ca1a0ca744a6f27ccaeedaadbcbbac706a71375020fc07d8a5893a87c9adb3e5'
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
n=load(dp);verify(load(mp));verify(n)
assert n['status']=='ACCEPTED_INDEPENDENT_MATHEMATICS_ONLY' and n['reviewer_id']=='/root/exact_verify77'
assert n['required_repairs']==[] and n['standard_axioms_only'] and n['collaborator_RAWs_preserved']==21
assert n['axioms']==['propext','Classical.choice','Quot.sound'] and n['immediate_public_count']==6 and n['actual88_not_a_dependency']
for k in ['focused_gate','whole_source_kernel_gate']:assert load(R/n[k]['path'])['exit_code']==0
out=r/'root.math89.adoption.json';assert not out.exists()
out.write_text(json.dumps(dict(status='ACCEPTED_INDEPENDENT_MATH_ONLY',native_decision_SHA256=sha(dp.read_bytes()),native_closed_manifest_SHA256=sha(mp.read_bytes()),exact_descriptors_rechecked=len(seen),checked_module=n['module'],reviewer=n['reviewer_id'],exposition_accepted=True,exposition_repairs_required=False,resolved_exposition_repair=n['resolved_exposition_repair'],PROVED_LOCAL=False,VERIFIED=False),indent=2)+'\n',encoding='utf8',newline='\n')
print('Independent whole mathematics/kernel/six-region exposition adopted;',len(seen),'RAW descriptors; no VERIFIED.')
