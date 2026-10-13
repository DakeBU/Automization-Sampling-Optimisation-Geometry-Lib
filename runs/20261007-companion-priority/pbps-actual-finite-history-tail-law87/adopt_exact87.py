from pathlib import Path
import hashlib,json,subprocess,sys,gzip
sys.path.insert(0,str(Path.cwd()/'tools'));import astis_advance as adv
r=Path(__file__).parent;d=r/'exact-commit-verification87';load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
assert sha((d/'verified.json').read_bytes())=='829c00a19c6993e69d1a7eef15c8dbf89ce04c3c78617f059e953b78a9d537bb'
assert sha((d/'closed-RAW-manifest87.json').read_bytes())=='7e72f52635a0e958046e6e4f72132769ba6082059a47fad2fa6f947c3af4441c'
assert sha((d/'admission87.json').read_bytes())=='439dd55f0e86a533be2734b9493ba947921e87460a4c099efd83dd93e15409df'
m=load(d/'closed-RAW-manifest87.json');a=load(d/'admission87.json');commit='ada2d073d04a78493555b2ac35344b9c5a264bfc'
assert m['verified_commit']==a['verified_commit']==subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==commit
checked=0
def current(x):
 global checked
 if isinstance(x,dict):
  if 'path' in x and 'raw_sha256' in x:
   b=Path(x['path']).read_bytes();assert sha(b)==x['raw_sha256'],x['path']
   if 'bytes' in x:assert len(b)==x['bytes'],x['path']
   checked+=1
  for v in x.values():current(v)
 elif isinstance(x,list):
  for v in x:current(v)
for x in m['checked_science_inputs']:
 target=x.get('lossless_archive') or x['path']
 b=subprocess.check_output(['git','show',commit+':'+target])
 if x.get('lossless_archive'):b=gzip.decompress(b)
 assert sha(b)==x['git_blob_raw_sha256'],x['path']
 if x['path'] not in ['runs/substantive_advances.jsonl','research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-finite-history-tail-law.json']:current(x)
for group in ['nested_pinned_mathlib','local_fixed_primary_and_excluded_extracts','owned_artifacts']:current(m[group])
for row in m['historical_descriptors_resolved_without_native_mutation']:
 current(row['authoritative_immutable_snapshot']);current(row['current_science'])
current(a)
saved=load(r.parent/'pbps-clock-tail-preread87/pre-fetch87.workspace-RAW.json')['tracked_modified'];assert len(saved)==21
for p,h in saved.items():assert sha(Path(p).read_bytes())==h,p
assert subprocess.check_output(['git','-C','.lake/packages/mathlib','rev-parse','HEAD'],text=True).strip()=='db584cd6d46c92f209a44c0f1c829460d327499d'
claim=load(r/'claim.json');state=adv.current_advances()[claim['advance_id']];assert state['state']=='VERIFIED' and state['latest_evidence']['verified_commit']==commit
assert a['exactly_one_append_only_event'] and a['all_other_advances_unchanged'] and a['all21collaborator_RAWs_preserved']
assert a['existing_stabilizing_lane_unchanged']==['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel']
out=r/'root.exact87.adoption.json';assert not out.exists();out.write_text(json.dumps(dict(status='INDEPENDENT_EXACT_COMMIT_VERIFIED_ADOPTED',science_commit=commit,verifier='/root/exact_verify77',native_verified_sha256=sha((d/'verified.json').read_bytes()),native_closed_manifest_sha256=sha((d/'closed-RAW-manifest87.json').read_bytes()),RAW_descriptors_rechecked=checked,all21preserved=True,stabilization=False,wholepaper=False,Goal_complete=False),indent=2)+'\n',encoding='utf8',newline='\n');print('Independent VERIFIED87 exact RAW closure adopted;',checked,'descriptors; existing sole lane only.')
