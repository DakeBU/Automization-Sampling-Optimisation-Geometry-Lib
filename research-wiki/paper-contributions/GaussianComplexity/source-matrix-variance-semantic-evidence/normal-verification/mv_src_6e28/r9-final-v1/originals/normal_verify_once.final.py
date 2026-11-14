from pathlib import Path
import json,hashlib,sys,os,subprocess,traceback
from datetime import datetime,timezone
sys.dont_write_bytecode=True;os.environ['GIT_OPTIONAL_LOCKS']='0'
R=Path('/Users/zhouhuanjian/ASTIS-GC');B=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'tools'));import astis_advance as advance,astis_frontier_cells as fc
ADV='ASTIS-SA-20261112-GaussianComplexitySourceMatrixVariance';WORKER='/root/mv_fresh_source_6e28';HELD='02fb93c64e4222f112e57c97ced2a548235cd0f6'
CELL='research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-matrix-variance.json';L=R/'runs/substantive_advances.jsonl'
DEST='research-wiki/paper-contributions/GaussianComplexity/source-matrix-variance-semantic-evidence/normal-verification/mv_src_6e28/r9-final-v1/originals/'
def sha(b):return hashlib.sha256(b).hexdigest()
def rd(p):return json.loads(p.read_bytes())
def wr(n,d):
 with (B/n).open('x') as f:f.write(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def count(rows):return sum(x.get('advance_id')==ADV and x.get('event')=='transition' and x.get('to_state')=='VERIFIED' for x in rows)
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()==HELD
assert rd(B/'precall-guard-comparison.json')['all_before_precall_equal']
assert sha((R/'.git/index').read_bytes())=='2f9f667a54d7dcfd9337a26e9c1d3d4c2c398965ca32cb88719b0d9c90f8f978'
assert subprocess.run(['git','diff','--quiet'],cwd=R).returncode==0
assert subprocess.run(['git','diff','--cached','--quiet'],cwd=R).returncode==0
snap=rd(B/'private/precall.snapshot.private.json');before=L.read_bytes();cb=(R/CELL).read_bytes();assert sha(before)==snap['advance_raw']['sha256'] and sha(cb)==snap['own_cell']['sha256']
rows=[json.loads(l) for l in before.splitlines() if l.strip()];assert count(rows)==0
states=advance._replay_advances(rows);assert states[ADV]['state']=='PROVED_LOCAL' and states[ADV]['owner_id']!=WORKER
pl=rd(B/'inputs/actual-PROVED_LOCAL-evidence.full.json');v=rd(B/'VERIFIED-evidence.final.full.json');assert len(pl)==21 and all(v[k]==x for k,x in pl.items());assert [x for x in rows if x.get('advance_id')==ADV and x.get('to_state')=='PROVED_LOCAL'][-1]['evidence']==pl
assert rd(B/'independent-decision.final.json')['decision']=='AUTHORIZE_EXACTLY_ONE_NORMAL_VERIFIED_CALL_IF_PRECALL_GUARDS_UNCHANGED'
assert rd(B/'prospective-fullfrontier-schema-check.json')['errors']==[]
assert (B/'ownC.before.exact.json').read_bytes()==cb
receipt={'started_utc':datetime.now(timezone.utc).isoformat(),'API':'astis_advance.transition_advance','advance_id':ADV,'to_state':'VERIFIED','worker_id':WORKER,'actual_API_calls':0,'actual_API_failures':0,'API_returned':False,'postcheck_failure':False,'pre_V_count':0,'post_V_count':None,'held_metadata_HEAD':HELD,'actual_math_commit':v['verified_commit'],'reader_commit':v['verified_reader_author_commit'],'owner_released':False}
# Exclusive once sentinel is the last durable preparation immediately before this single API invocation.
wr('ONCE-SENTINEL.json',{'created_utc':datetime.now(timezone.utc).isoformat(),'advance_id':ADV,'worker_id':WORKER,'historical_V_count':0,'permitted_attempts':1,'automatic_replay':False,'payload_sha256':sha((B/'VERIFIED-evidence.final.full.json').read_bytes())})
try:
 receipt['actual_API_calls']=1
 try:
  advance.transition_advance(ADV,'VERIFIED',worker_id=WORKER,modes=['independent-verification'],evidence=v)
  receipt['API_returned']=True
 except BaseException:
  receipt['actual_API_failures']=1;raise
 after=L.read_bytes();assert after.startswith(before);added=after[len(before):];assert added.endswith(b'\n') and len(added.splitlines())==1
 (B/'actual-VERIFIED-append.exact.jsonl').write_bytes(added)
 event=json.loads(added);assert event['advance_id']==ADV and event['from_state']=='PROVED_LOCAL' and event['to_state']=='VERIFIED' and event['worker_id']==WORKER and event['evidence']==v
 receipt['post_V_count']=count([json.loads(l) for l in after.splitlines() if l.strip()]);assert receipt['post_V_count']==1
 c=json.loads(cb);assert c['status']=='proved_locally';assert c['evidence'].get('independent_verification') in (None,'')
 c['status']='independently_verified'
 c['evidence']['independent_verification']='Independent local mathematical R9 verification by '+WORKER+'; math '+v['verified_commit']+'; reader '+v['verified_reader_author_commit']+'; held metadata '+HELD+'. Full ORIGINAL V payload '+DEST+'VERIFIED-evidence.final.full.json sha256 '+sha((B/'VERIFIED-evidence.final.full.json').read_bytes())+'; exact single ORIGINAL append '+DEST+'actual-VERIFIED-append.exact.jsonl sha256 '+sha(added)+'; independent decision '+DEST+'independent-decision.final.json sha256 '+sha((B/'independent-decision.final.json').read_bytes())+'. Original production mobile reader ACTUAL FAIL; proposed CSS prototype UNAPPLIED and conditional only. P public uncentered plus actual private T only; no public T API/main/concentration/integration/publication/PURIFIED/whole-Goal credit; owner retained.'
 c['evidence']['independent_verification_details']={'verifier_id':WORKER,'verified_commit':v['verified_commit'],'reader_commit':v['verified_reader_author_commit'],'verification_metadata_HEAD':HELD,'full_V_payload':{'path':DEST+'VERIFIED-evidence.final.full.json','sha256':sha((B/'VERIFIED-evidence.final.full.json').read_bytes())},'exact_append':{'path':DEST+'actual-VERIFIED-append.exact.jsonl','sha256':sha(added)},'independent_decision':{'path':DEST+'independent-decision.final.json','sha256':sha((B/'independent-decision.final.json').read_bytes())},'original_reader_outcome':'ACTUAL FAIL_MOBILE_TABLE_CLIPPING','conditional_CSS':'UNAPPLIED_PROTOTYPE_PASS_ONLY','boundary':v['local_verification_scope_and_remaining_boundary'],'owner_released':False}
 cells=fc.load_cells();assert any(x['__path__']==CELL for x in cells)
 for i,x in enumerate(cells):
  if x['__path__']==CELL:cells[i]={**c,'__path__':CELL}
 errs=fc.validate_cells(cells);wr('actualvalue-prospective-fullfrontier-schema-check.json',{'errors':errs,'error_count':len(errs),'required_field_type':type(c['evidence']['independent_verification']).__name__});assert errs==[]
 (R/CELL).write_text(json.dumps(c,indent=2,ensure_ascii=False)+'\n');(B/'ownC.after.exact.json').write_bytes((R/CELL).read_bytes())
 # Mandatory real actual POSTWRITE fullfrontier schema, not the old S prewrite-only omission.
 postcells=fc.load_cells();posterrs=fc.validate_cells(postcells);wr('actual-postwrite-fullfrontier-schema-check.json',{'errors':posterrs,'error_count':len(posterrs),'loaded_cells':len(postcells),'required_independent_verification_is_nonempty_STRING':isinstance(c['evidence']['independent_verification'],str) and bool(c['evidence']['independent_verification'].strip()),'actual_shared_cell_read_after_write':True});assert posterrs==[]
 receipt.update({'single_exact_append_sha256':sha(added),'ownC_before_sha256':sha(cb),'ownC_after_sha256':sha((R/CELL).read_bytes()),'all21_PL_values_inline_unchanged':True,'actual_postwrite_fullfrontier_errors':0,'exit':0})
 print('NORMAL_R9_VERIFIED_ONCE_RETURNED; actual API1/fail0; historyV0->1; actual postwrite fullfrontier schema0; only ownC status/evidence and exact one-line append.')
except BaseException:
 receipt['exception']=traceback.format_exc();receipt['postcheck_failure']=receipt['API_returned'];receipt['exit']=1
 # No replay: record actual ledger state even if API raised or postprocessing failed.
 raw=L.read_bytes()
 if raw.startswith(before) and raw!=before and not (B/'actual-VERIFIED-append.exact.jsonl').exists():(B/'actual-VERIFIED-append.exact.jsonl').write_bytes(raw[len(before):])
 receipt['post_V_count']=count([json.loads(l) for l in raw.splitlines() if l.strip()]);traceback.print_exc();raise
finally:
 receipt['finished_utc']=datetime.now(timezone.utc).isoformat();wr('normal-API-receipt.json',receipt)
