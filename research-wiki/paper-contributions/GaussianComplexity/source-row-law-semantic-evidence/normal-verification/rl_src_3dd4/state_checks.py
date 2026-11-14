import hashlib,json,pathlib,os,stat,subprocess,sys
ROOT=pathlib.Path('/Users/zhouhuanjian/ASTIS-GC');sys.path.insert(0,str(ROOT))
from tools import astis_advance as advance
OUT=pathlib.Path(__file__).resolve().parent;E=OUT.parents[1]
TARGET='ASTIS-SA-20261112-GaussianComplexitySourceRowLaw';WORKER='/root/row_law_fresh_source_3dd4';HEAD='2c57883183937fdef1578a2b33e4ea892af2c694'
CELL='research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-row-law.json';LEDGER='runs/substantive_advances.jsonl';DISC='runs/substantive_discoveries.jsonl'
sha=lambda b:hashlib.sha256(b).hexdigest()
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def read_records(b):return [json.loads(x) for x in b.splitlines() if x.strip()]
def inventory(paths):
 rows=[]
 for rel in sorted(paths):
  p=ROOT/rel;s=p.lstat()
  if stat.S_ISLNK(s.st_mode):b=os.readlink(p).encode()
  elif stat.S_ISREG(s.st_mode):b=p.read_bytes()
  elif stat.S_ISDIR(s.st_mode):b=b'gitlink-directory'
  else:raise AssertionError(rel)
  rows.append([rel,s.st_mode&0o177777,len(b),sha(b)])
 return {'count':len(rows),'sha256':sha(canonical(rows))}
def snapshot():
 head=subprocess.run(['git','rev-parse','HEAD'],cwd=ROOT,check=True,capture_output=True).stdout.decode().strip();assert head==HEAD
 lb=(ROOT/LEDGER).read_bytes();db=(ROOT/DISC).read_bytes();rs=read_records(lb);states=advance._replay_advances(rs);discs=advance._replay_discoveries(read_records(db));own=states[TARGET]
 foreign={k:v for k,v in states.items() if k!=TARGET};assert len(foreign)==305 and len(discs)==43
 tracked=subprocess.run(['git','ls-files','-z'],cwd=ROOT,check=True,capture_output=True).stdout.decode().split('\0');tracked=[x for x in tracked if x]
 others=[x for x in tracked if x not in {CELL,LEDGER}]
 older=[str(p.relative_to(ROOT)) for p in (ROOT/'research-wiki/frontier-cells').glob('*.json') if stat.S_ISREG(p.lstat().st_mode) and str(p.relative_to(ROOT))!=CELL];assert len(older)==465
 oldfront=inventory(older+['research-wiki/frontier-cells/README.md'])
 cell=json.loads((ROOT/CELL).read_text());rest=json.loads(json.dumps(cell));rest.pop('status');rest['evidence'].pop('independent_verification')
 ownrest={k:v for k,v in own.items() if k not in {'state','last_actor','latest_evidence','updated_at'}}
 own_events=[r for r in rs if r.get('advance_id')==TARGET]
 return {'head':head,'advances_total':len(states),'foreign_full_states':{'count':len(foreign),'sha256':sha(canonical(foreign))},'discoveries_full_states':{'count':len(discs),'sha256':sha(canonical(discs))},'discovery_ledger':{'bytes':len(db),'sha256':sha(db)},'older_regular_frontier_and_README':oldfront,'all_other_tracked_files':inventory(others),'ledger':{'bytes':len(lb),'sha256':sha(lb),'records':len(rs)},'own_state':own['state'],'own_owner':own.get('owner_id'),'own_state_rest_sha256':sha(canonical(ownrest)),'own_cell':{'status':cell['status'],'independent_verification':cell['evidence']['independent_verification'],'rest_sha256':sha(canonical(rest)),'raw_sha256':sha((ROOT/CELL).read_bytes())},'own_verified_events':sum(r.get('to_state')=='VERIFIED' for r in own_events),'own_proved_local_events':sum(r.get('to_state')=='PROVED_LOCAL' for r in own_events)},lb,states,cell
if __name__=='__main__':
 phase=sys.argv[1];s,lb,states,cell=snapshot()
 if phase=='pre':
  assert s['own_state']=='PROVED_LOCAL' and s['own_owner']=='huanjian_gc_20261112_source_row_law' and s['own_verified_events']==0 and s['own_proved_local_events']==1
  assert s['own_cell']['status']=='proved_locally' and s['own_cell']['independent_verification']==''
  pl=json.loads((E/'actual-PROVED_LOCAL-evidence.full.json').read_text());assert states[TARGET]['latest_evidence']==pl
  lines=[x for x in lb.splitlines(keepends=True) if json.loads(x).get('advance_id')==TARGET and json.loads(x).get('to_state')=='PROVED_LOCAL'];assert len(lines)==1 and sha(lines[0])=='46ff845ad22e1432b616a7a2f7c12971356aa2072da3efdbe3643a92f844f4e4'
  (OUT/'actual-PROVED_LOCAL-append.original.jsonl').write_bytes(lines[0])
  (OUT/'pre-invariants.json').write_text(json.dumps(s,indent=2)+'\n')
 elif phase=='post':
  pre=json.loads((OUT/'pre-invariants.json').read_text());payload=json.loads((OUT/'actual-VERIFIED-evidence.full.json').read_text())
  for key in ['head','advances_total','foreign_full_states','discoveries_full_states','discovery_ledger','older_regular_frontier_and_README','all_other_tracked_files','own_owner','own_state_rest_sha256']:assert s[key]==pre[key],key
  assert s['own_state']=='VERIFIED' and s['own_verified_events']==1 and s['own_proved_local_events']==1
  assert s['own_cell']['status']=='independently_verified' and s['own_cell']['independent_verification']==str((E/'actual-VERIFIED-independent-decision.json').relative_to(ROOT))
  assert s['own_cell']['rest_sha256']==pre['own_cell']['rest_sha256']
  prefix=lb[:pre['ledger']['bytes']];assert sha(prefix)==pre['ledger']['sha256'];suffix=lb[pre['ledger']['bytes']:];events=read_records(suffix);assert len(events)==1 and suffix.endswith(b'\n')
  event=events[0];assert event['advance_id']==TARGET and event['from_state']=='PROVED_LOCAL' and event['to_state']=='VERIFIED' and event['worker_id']==WORKER and event['evidence']==payload
  assert states[TARGET]['latest_evidence']==payload
  pl=json.loads((E/'actual-PROVED_LOCAL-evidence.full.json').read_text());assert all(payload[k]==v for k,v in pl.items())
  assert payload['formalizer_preseal_API_pristine'] is False and payload['preseal_exposure']['formalizer_API_pristine'] is False
  assert suffix==(OUT/'actual-VERIFIED-append.original.jsonl').read_bytes()
  s.update({'result':'pass','normal_VERIFIED_API_calls':1,'appended_events':1,'append_sha256':sha(suffix),'full_payload_raw_sha256':sha((OUT/'actual-VERIFIED-evidence.full.json').read_bytes()),'full_PL_fields_preserved_inline':len(pl),'own_cell_only_status_and_preseed_IV_pointer_changed':True,'decision_sha256':sha((E/'actual-VERIFIED-independent-decision.json').read_bytes()),'no_full_foreign_or_control_snapshots_exported':True})
  (OUT/'post-invariants.json').write_text(json.dumps(s,indent=2)+'\n')
 else:raise AssertionError(phase)
 print(json.dumps(s,indent=2))
