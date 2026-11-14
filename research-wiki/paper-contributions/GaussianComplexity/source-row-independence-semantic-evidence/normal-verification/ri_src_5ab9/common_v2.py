import hashlib,json,pathlib,os,stat,subprocess,sys
sys.dont_write_bytecode=True
ROOT=pathlib.Path('/Users/zhouhuanjian/ASTIS-GC')
sys.path.insert(0,str(ROOT))
from tools import astis_advance as advance
OUT=pathlib.Path(__file__).resolve().parent
E=OUT.parents[1]
TARGET='ASTIS-SA-20261112-GaussianComplexitySourceRowIndependence'
OWNER='huanjian_gc_20261112_source_row_independence'
WORKER='/root/row_indep_fresh_source_5ab9'
HEAD='e5a4eadca4a6208e54cc90b7cb351e664f922cd5'
CANDIDATE='66e0bb9b748d68816a8443d60696656c9340222f'
LOCAL_MAIN='a7cc97fc2376896ad6a666b87ca611dc4b815a49'
ORIGIN_MAIN='ab87352ce7689d885b49dd854a39e77a7c1cae6c'
CELL='research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-row-independence.json'
LEDGER='runs/substantive_advances.jsonl'
DISC='runs/substantive_discoveries.jsonl'
sha=lambda b:hashlib.sha256(b).hexdigest()
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def records(b):return [json.loads(x) for x in b.splitlines() if x.strip()]
def rel(p):return str(p.relative_to(ROOT))
def info(p):
 b=p.read_bytes();return {'path':rel(p),'bytes':len(b),'sha256':sha(b)}
def write(path,value):
 assert not path.exists(),str(path)
 path.write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
def git(*args):return subprocess.run(['git',*args],cwd=ROOT,check=True,capture_output=True).stdout
def inventory(paths):
 rows=[]
 for name in sorted(paths):
  p=ROOT/name;s=p.lstat()
  if stat.S_ISLNK(s.st_mode):b=os.readlink(p).encode()
  elif stat.S_ISREG(s.st_mode):b=p.read_bytes()
  elif stat.S_ISDIR(s.st_mode):b=b'gitlink-directory'
  else:raise AssertionError(name)
  rows.append([name,s.st_mode&0o177777,len(b),sha(b)])
 return {'count':len(rows),'aggregate_full_file_bytes_and_modes_sha256':sha(canonical(rows))}
def snapshot():
 assert git('rev-parse','HEAD').decode().strip()==HEAD
 assert git('rev-parse','refs/heads/main').decode().strip()==LOCAL_MAIN
 assert git('rev-parse','refs/remotes/origin/main').decode().strip()==ORIGIN_MAIN
 lb=(ROOT/LEDGER).read_bytes();db=(ROOT/DISC).read_bytes()
 rs=records(lb);states=advance._replay_advances(rs);discs=advance._replay_discoveries(records(db))
 own=states[TARGET];foreign={k:v for k,v in states.items() if k!=TARGET}
 assert len(foreign)==306 and len(discs)==43
 tracked=[p for p in git('ls-files','-z').decode().split('\0') if p]
 othertracked=[p for p in tracked if p not in {CELL,LEDGER}]
 frontier=[rel(p) for p in (ROOT/'research-wiki/frontier-cells').rglob('*') if stat.S_ISREG(p.lstat().st_mode)]
 otherfrontier=[p for p in frontier if p!=CELL]
 assert 'research-wiki/frontier-cells/README.md' in otherfrontier
 cell=json.loads((ROOT/CELL).read_bytes());rest=json.loads(json.dumps(cell));rest.pop('status');rest['evidence'].pop('independent_verification')
 ownrest={k:v for k,v in own.items() if k not in {'state','last_actor','latest_evidence','updated_at'}}
 source_manifest=E/'source-review/ri_src_5ab9/portable-manifest.json'
 assert sha(source_manifest.read_bytes())=='e8e8ea9535828275c070d6502eb97085a91ed2d3a26a1fdd32f7900a9fa0bae4'
 sm=json.loads(source_manifest.read_bytes());assert sm['exact_count']==59
 for ent in sm['entries']:
  p=ROOT/ent['destination'];assert len(p.read_bytes())==ent['bytes'] and sha(p.read_bytes())==ent['sha256']
 own_events=[r for r in rs if r.get('advance_id')==TARGET]
 s={'HEAD':HEAD,'local_main':LOCAL_MAIN,'origin_main':ORIGIN_MAIN,'advances_total':len(states),'foreign_full_states':{'count':len(foreign),'canonical_full_state_sha256':sha(canonical(foreign))},'discovery_full_states':{'count':len(discs),'canonical_full_state_sha256':sha(canonical(discs))},'discovery_ledger':info(ROOT/DISC),'all_other_tracked_files':inventory(othertracked),'all_regular_frontier_files_total':len(frontier),'prior_other_regular_frontier_files_including_README':inventory(otherfrontier),'ledger':{**info(ROOT/LEDGER),'records':len(rs)},'own_state':own['state'],'own_owner':own.get('owner_id'),'own_state_rest_sha256':sha(canonical(ownrest)),'own_cell':{'status':cell['status'],'independent_verification':cell['evidence']['independent_verification'],'semantic_rest_sha256':sha(canonical(rest)),'raw_sha256':sha((ROOT/CELL).read_bytes())},'own_PL_events':sum(r.get('to_state')=='PROVED_LOCAL' for r in own_events),'own_V_events':sum(r.get('to_state')=='VERIFIED' for r in own_events),'source_package_59_entries_unchanged':True,'source_package_manifest_sha256':sha(source_manifest.read_bytes()),'stabilizing_identity_summary':[{'advance_id':k,'state':v['state'],'owner_id':v.get('owner_id'),'integration_owner':v.get('latest_evidence',{}).get('integration_owner')} for k,v in foreign.items() if v.get('state')=='STABILIZING']}
 return s,lb,states,cell
