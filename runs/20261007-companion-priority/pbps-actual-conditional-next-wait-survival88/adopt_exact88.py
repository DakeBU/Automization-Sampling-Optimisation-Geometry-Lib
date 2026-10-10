from pathlib import Path
import hashlib,json,subprocess,sys,gzip
sys.path.insert(0,str(Path.cwd()/'tools'));import astis_advance as adv
r=Path(__file__).parent;d=r/'exact-commit-verification88';load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
assert sha((d/'verified.json').read_bytes())=='0136d3cb0c4d674101e38423e94b459c3b50e6868516fc3354eeba1276f34186'
assert sha((d/'closed-RAW-manifest88.json').read_bytes())=='6e8bd0493e1a33bbe863b169984b459c069738e0c619a25c3804cd732ce97f31'
assert sha((d/'admission88.json').read_bytes())=='3ad3e8e323d1ba7dfbbc54495daebf8e868f1a89ec1fd1c183d56a3a92998586'
m=load(d/'closed-RAW-manifest88.json');a=load(d/'admission88.json');commit='456e13f9561abcf01a285133e91b3951bf2ed892'
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
 if x['path'] not in ['runs/substantive_advances.jsonl','research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-conditional-next-wait-survival.json']:current(x)
for group in ['nested_pinned_mathlib','local_fixed_primary_and_excluded_extracts','preexisting_collaborator_inputs','owned_artifacts']:current(m[group])
current(a)
saved=load(r.parent/'pbps-conditional-next-wait-preread88/pre-fetch88.workspace-RAW.json')['tracked_modified'];assert len(saved)==21
for p,h in saved.items():assert sha(Path(p).read_bytes())==h,p
assert subprocess.check_output(['git','-C','.lake/packages/mathlib','rev-parse','HEAD'],text=True).strip()=='db584cd6d46c92f209a44c0f1c829460d327499d'
claim=load(r/'claim.json');state=adv.current_advances()[claim['advance_id']];assert state['state']=='VERIFIED' and state['latest_evidence']['verified_commit']==commit
assert a['exactly_one_append_only_event'] and a['all_other_advances_unchanged'] and a['all21collaborator_RAWs_preserved']
assert [x['id'] for x in a['existing_stabilizing_lane_unchanged']]==['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel']
out=r/'root.exact88.adoption.json';assert not out.exists();out.write_text(json.dumps(dict(status='INDEPENDENT_EXACT_COMMIT_VERIFIED_ADOPTED',science_commit=commit,verifier='/root/exact_verify77',native_verified_sha256=sha((d/'verified.json').read_bytes()),native_closed_manifest_sha256=sha((d/'closed-RAW-manifest88.json').read_bytes()),RAW_descriptors_rechecked=checked,all21preserved=True,stabilization=False,wholepaper=False,Goal_complete=False),indent=2)+'\n',encoding='utf8',newline='\n');print('Independent VERIFIED88 exact RAW closure adopted;',checked,'descriptors; existing sole lane only.')
