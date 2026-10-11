from pathlib import Path
import hashlib,json,subprocess,sys,gzip
sys.path.insert(0,str(Path.cwd()/'tools'));import astis_advance as adv
r=Path(__file__).parent;d=r/'exact-commit-verification90';load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
expected={'verified.json':'26ea4bf0423f71453dbfb770776337e1b97c9585e45431b6e9153921550ca51a','closed-RAW-manifest90.json':'a9aea567852cc0735120909a5626f8287f5bd87394ae5aed65e9e2d346788666','admission90.json':'6008aa04b9154f839d5fc41a18bc1ca9b5131f29d61e82f84a054993478c3fc3'}
for name,h in expected.items():assert sha((d/name).read_bytes())==h,name
m=load(d/'closed-RAW-manifest90.json');a=load(d/'admission90.json');commit='e8d38b3002f4562ef254205135c0d213f9efe410'
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
 if x['path'] not in ['runs/substantive_advances.jsonl','research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-finite-history-extension.json']:current(x)
for group in ['nested_pinned_mathlib','local_fixed_primary_runtime_cache_and_excluded_snapshots','preexisting_collaborator_inputs','owned_artifacts']:current(m[group])
current(a)
saved=load(r.parent/'pbps-next-history-extension-preread90/pre-fetch90.workspace-RAW.json')['tracked_modified'];assert len(saved)==21
for p,h in saved.items():assert sha(Path(p).read_bytes())==h,p
assert subprocess.check_output(['git','-C','.lake/packages/mathlib','rev-parse','HEAD'],text=True).strip()=='db584cd6d46c92f209a44c0f1c829460d327499d'
claim=load(r/'claim.json');state=adv.current_advances()[claim['advance_id']];assert state['state']=='VERIFIED' and state['latest_evidence']['verified_commit']==commit
assert a['exactly_one_append_only_event'] and a['all_other_advances_unchanged'] and a['all21collaborator_RAWs_preserved']
assert [x['id'] for x in a['existing_stabilizing_lane_unchanged']]==['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel']
out=r/'root.exact90.adoption.json';assert not out.exists()
out.write_text(json.dumps(dict(status='INDEPENDENT_EXACT_COMMIT_VERIFIED_ADOPTED',science_commit=commit,verifier='/root/exact_verify77',native_verified_sha256=expected['verified.json'],native_closed_manifest_sha256=expected['closed-RAW-manifest90.json'],RAW_descriptors_rechecked=checked,all21preserved=True,stabilization=False,wholepaper=False,Goal_complete=False),indent=2)+'\n',encoding='utf8',newline='\n')
print('Independent VERIFIED90 exact RAW closure adopted;',checked,'descriptors; existing sole lane only.')
