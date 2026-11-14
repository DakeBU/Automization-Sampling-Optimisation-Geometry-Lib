from pathlib import Path
import json,hashlib,datetime,subprocess,contextlib,traceback,os,tempfile
import sys
sys.path.insert(0, str(Path.cwd()))
from tools import astis_advance as advance
from tools import astis_frontier_cells as frontier
ROOT=Path.cwd();B=ROOT/'.astis/semantic-neutral-20261110/src_c75d42/sourcev_execution_20261110';P=B/'public';V=B/'private';aid='ASTIS-SA-20261110-GaussianComplexityFixedSpectrumBias';actor='/root/source_reader_c75d42';owner='huanjian_gc_20261110_fixed_spectrum_bias';ledger=ROOT/'runs/substantive_advances.jsonl';cell=ROOT/'research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-fixed-spectrum-bias.json'
def sha(b):return hashlib.sha256(b).hexdigest()
def canonical(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def save(path,x):path.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def replay(raw):return advance._replay_advances([json.loads(x) for x in raw.splitlines() if x.strip()])
assert subprocess.run(['git','rev-parse','HEAD'],stdout=subprocess.PIPE,check=True).stdout.decode().strip()=='92587bb187dbc1e15e46870297613f80f02a508f'
before=(V/'ledger.before.raw.jsonl').read_bytes();assert ledger.read_bytes()==before;assert before.endswith(b'\n');state=replay(before);assert state[aid]['state']=='PROVED_LOCAL' and state[aid]['owner_id']==owner
assert cell.read_bytes()==(P/'own-frontier.before.json').read_bytes()
foreign_cells_before=json.loads((V/'foreign-frontiers.before.json').read_text())
for name,x in foreign_cells_before.items():assert sha((ROOT/name).read_bytes())==x['sha256']
assert sha((ROOT/'research-wiki/semantic-roundtrip/audits/huanjian-fixed-spectrum-bias.json').read_bytes())=='b0a87e68a56e2651d19273dd8d031a4d672e5679f5ab98c0015f120b9438867a'
eraw=(P/'original-evidence.raw.json').read_bytes();evidence=json.loads(eraw);eh=json.loads((P/'original-evidence-hashes-and-keys.json').read_text());assert sha(eraw)==eh['raw_sha256'] and sha(canonical(evidence))==eh['canonical_sha256'];assert list(evidence)==eh['top_level_keys'];assert len(evidence)==17
marker=P/'NORMAL_TRANSITION_CALL_STARTED.marker'
with marker.open('x') as f:f.write(datetime.datetime.now(datetime.timezone.utc).isoformat()+'\n')
result={'api':'tools.astis_advance.transition_advance','advance_id':aid,'worker_id':actor,'from_state':'PROVED_LOCAL','to_state':'VERIFIED','started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_call_count':1,'evidence_raw_sha256':eh['raw_sha256'],'evidence_canonical_sha256':eh['canonical_sha256'],'evidence_full_top_level_keys':eh['top_level_keys'],'native_rerun':False}
try:
 with (P/'normal-api.stdout.log').open('w') as out,(P/'normal-api.stderr.log').open('w') as err,contextlib.redirect_stdout(out),contextlib.redirect_stderr(err):
  returned=advance.transition_advance(aid,'VERIFIED',worker_id=actor,modes=['independent-source-verification','full-module-source-exposition-review','native-evidence-preflight'],evidence=evidence)
 result.update({'api_return_repr':repr(returned),'exit_code':0,'exception':None,'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
except BaseException as exc:
 result.update({'exit_code':1,'exception':repr(exc),'traceback':traceback.format_exc(),'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()});save(P/'normal-api-result.json',result);raise
save(P/'normal-api-result.json',result)
after=ledger.read_bytes();assert after.startswith(before);appended=after[len(before):];assert len(appended.splitlines())==1
(P/'actual-normal-append.raw.jsonl').write_bytes(appended);event=json.loads(appended);assert event['advance_id']==aid and event['from_state']=='PROVED_LOCAL' and event['to_state']=='VERIFIED' and event['worker_id']==actor and event['evidence']==evidence
assert sha(canonical(event['evidence']))==eh['canonical_sha256']
newstate=replay(after);assert newstate[aid]['state']=='VERIFIED' and newstate[aid]['owner_id']==owner and newstate[aid]['last_actor']==actor
foreign_before=json.loads((V/'foreign-sau-states.before.json').read_text());foreign_after={k:v for k,v in newstate.items() if k!=aid};assert foreign_after==foreign_before and len(foreign_after)==291;save(V/'foreign-sau-states.after.json',foreign_after)
prepared=(P/'own-frontier.proposed.json').read_bytes();proposed=json.loads(prepared);assert proposed['status']=='independently_verified' and proposed['owner_id']==owner
assert not frontier.validate_cells([dict(proposed,__path__=str(cell.relative_to(ROOT)))])
fd,name=tempfile.mkstemp(prefix='.bias-sourcev-',suffix='.tmp',dir=cell.parent)
try:
 with os.fdopen(fd,'wb') as f:f.write(prepared);f.flush();os.fsync(f.fileno())
 os.replace(name,cell)
finally:
 if os.path.exists(name):os.unlink(name)
(P/'own-frontier.after.json').write_bytes(cell.read_bytes());assert cell.read_bytes()==prepared
foreign_cells_after={str(p.relative_to(ROOT)):{'sha256':sha(p.read_bytes()),'raw_utf8':p.read_text()} for p in sorted((ROOT/'research-wiki/frontier-cells').rglob('*.json')) if p!=cell};assert foreign_cells_after==foreign_cells_before and len(foreign_cells_after)==450;save(V/'foreign-frontiers.after.json',foreign_cells_after)
protected_before=json.loads((V/'protected-source-model-tree.before.json').read_text());changed=[]
for name,expected in protected_before.items():
 p=ROOT/name
 if not p.is_file():changed.append(name);continue
 h=hashlib.sha256()
 with p.open('rb') as f:
  for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
 if h.hexdigest()!=expected:changed.append(name)
assert not changed, 'Protected source/model changes detected; no reset attempted'
protected= {'protected_file_count':len(protected_before),'changed_count':len(changed),'all_unchanged':not changed,'comparison':'Content SHA256 of all tracked source/model text files outside .astis, excluding exactly own ledger and own frontier; includes shared source/model surfaces. Private raw filename/hash inventories are not public artifacts.'};save(P/'protected-source-model-preservation.json',protected)
def diff(a,b,path=''):
 if type(a)!=type(b):return [path]
 if isinstance(a,dict):
  result=[]
  for k in set(a)|set(b):
   p=path+'.'+k if path else k
   if k not in a or k not in b:result.append(p)
   else:result.extend(diff(a[k],b[k],p))
  return result
 return [] if a==b else [path]
frontier_before=json.loads((P/'own-frontier.before.json').read_text());proof={'path':str(cell.relative_to(ROOT)),'from_status':frontier_before['status'],'to_status':proposed['status'],'owner_before':frontier_before['owner_id'],'owner_after':proposed['owner_id'],'before_raw_sha256':sha((P/'own-frontier.before.json').read_bytes()),'after_raw_sha256':sha(prepared),'changed_fields':sorted(diff(frontier_before,proposed)),'single_cell_validation_errors':frontier.validate_cells([dict(proposed,__path__=str(cell.relative_to(ROOT)))]),'foreign_frontier_files_unchanged':450};save(P/'own-frontier-mutation-proof.json',proof)
summary={'advance_id':aid,'normal_API_actual_call_count':1,'normal_API_exit_code':0,'api_return_repr':result['api_return_repr'],'actual_append_bytes':len(appended),'actual_append_raw_sha256':sha(appended),'actual_append_one_event':True,'original_evidence_raw_sha256':eh['raw_sha256'],'original_evidence_canonical_sha256':eh['canonical_sha256'],'entire_original_evidence_key_count':17,'entire_original_evidence_top_level_keys':eh['top_level_keys'],'appended_evidence_equals_entire_original':True,'new_own_advance_state':'VERIFIED','new_own_frontier_status':'independently_verified','owner_preserved':owner,'foreign_SAU_states_unchanged':291,'foreign_frontier_files_unchanged':450,'foreign_sau_canonical_before_sha256':sha(canonical(foreign_before)),'foreign_sau_canonical_after_sha256':sha(canonical(foreign_after)),'foreign_frontier_canonical_before_sha256':sha(canonical(foreign_cells_before)),'foreign_frontier_canonical_after_sha256':sha(canonical(foreign_cells_after)),'protected_source_model_files_unchanged':len(protected_before),'private_raw_snapshots_publication_authorized':False,'only_future_evidence_added_field':'post_integration','no_STAB_shared_root_site_browser_push':True};save(P/'selected-public-safe-execution-summary.json',summary)
print(json.dumps(summary,ensure_ascii=False,indent=2))
