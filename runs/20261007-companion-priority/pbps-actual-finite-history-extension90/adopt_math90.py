from pathlib import Path
import hashlib,json
R=Path('E:/Samplinglib');r=Path(__file__).parent;d=r/'independent-math90'
load=lambda p:json.loads(p.read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
dp=d/'decision90.json';mp=d/'closed-RAW-manifest90.json'
assert sha(dp.read_bytes())=='bf3c1b835098ce3f651abd2440b97f85aa4be7430c218f2b90515dd813a6b724'
assert sha(mp.read_bytes())=='e1c7416c51b114e634d6eb1e9928e2d5bd5a75c3bcf8135bb7bcb928399ae647'
res=load(d/'historical-input-resolution90.json')['resolutions']
mapping={(x['path'],x['raw_sha256']):x['closed_snapshot'] for x in res};seen=[]
def verify(x):
 if isinstance(x,dict):
  if 'path' in x and 'raw_sha256' in x:
   p=Path(mapping.get((x['path'],x['raw_sha256']),x['path']));p=p if p.is_absolute() else R/p;b=p.read_bytes()
   assert sha(b)==x['raw_sha256'],p
   if 'bytes' in x:assert len(b)==x['bytes'],p
   seen.append(str(p))
  for v in x.values():verify(v)
 elif isinstance(x,list):
  for v in x:verify(v)
n=load(dp);verify(load(mp));verify(n)
assert n['status']=='ACCEPTED_INDEPENDENT_MATHEMATICS_AND_CURRENT_EXPOSITION_ONLY' and n['reviewer_id']=='/root/exact_verify77'
assert not n['required_repairs'] and n['standard_axioms_only'] and n['all_21_collaborator_RAW_preserved']
assert n['axioms']==['propext','Classical.choice','Quot.sound'] and n['kernel_counts']['immediate_public']==4 and n['actual88_absent']
out=r/'root.math90.adoption.json';assert not out.exists()
out.write_text(json.dumps(dict(status='ACCEPTED_INDEPENDENT_MATH_ONLY',native_decision_SHA256=sha(dp.read_bytes()),native_closed_manifest_SHA256=sha(mp.read_bytes()),exact_descriptors_rechecked=len(seen),checked_module=n['reviewed_worktree_module_not_yet_science_commit'],reviewer=n['reviewer_id'],exposition_accepted=True,exposition_repairs_required=False,resolved_exposition_repair=n['historical_exposition_gap_resolved_by_distinct_reviewer'],historical_snapshot_resolution='independent-math90/historical-input-resolution90.json',PROVED_LOCAL=False,VERIFIED=False),indent=2)+'\n',encoding='utf8',newline='\n')
print('Independent whole mathematics/kernel/six-region exposition adopted;',len(seen),'RAW descriptors; no VERIFIED.')
