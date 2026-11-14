from pathlib import Path
import json,hashlib,sys,os,subprocess,traceback
from datetime import datetime,timezone
sys.dont_write_bytecode=True
R=Path('/Users/zhouhuanjian/ASTIS-GC');B=R/'.astis/semantic-neutral-20261112/mv_src_6e28/normal-verification-v2'
sys.path.insert(0,str(R/'tools'))
import astis_advance
ADV='ASTIS-SA-20261112-RealMatrixPositiveIntegral';WORKER='/root/mv_fresh_source_6e28'
CELL=R/'research-wiki/frontier-cells/ASTIS-SHARED-REAL-MATRIX-POSITIVE-INTEGRAL.json';L=R/'runs/substantive_advances.jsonl'
def sha(b):return hashlib.sha256(b).hexdigest()
def wr(name,d):
 with (B/name).open('x') as f:f.write(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()=='5f69ac83737e497210d8d8ad9628c45d83089458'
assert json.loads((B/'precall-guard-comparison.json').read_bytes())['all_before_precall_equal']
snap=json.loads((B/'private/precall.snapshot.private.json').read_bytes())
before=L.read_bytes();assert sha(before)==snap['advance_raw']['sha256']
cb=CELL.read_bytes();assert sha(cb)==snap['own_cell']['sha256']
rows=[json.loads(l) for l in before.splitlines() if l.strip()]
def nV(rs):return sum(r.get('advance_id')==ADV and r.get('event')=='transition' and r.get('to_state')=='VERIFIED' for r in rs)
assert nV(rows)==0
state=astis_advance._replay_advances(rows);assert state[ADV]['state']=='PROVED_LOCAL' and state[ADV]['owner_id']!=WORKER
pl=json.loads((B/'inputs/actual-PROVED_LOCAL-evidence.full.json').read_bytes());v=json.loads((B/'VERIFIED-evidence.full.json').read_bytes());assert len(pl)==20 and all(v[k]==val for k,val in pl.items())
lastpl=[r for r in rows if r.get('advance_id')==ADV and r.get('to_state')=='PROVED_LOCAL'][-1];assert lastpl['evidence']==pl
assert json.loads((B/'independent-decision.json').read_bytes())['decision']=='AUTHORIZE_EXACTLY_ONE_NORMAL_VERIFIED_CALL_IF_PRECALL_GUARDS_UNCHANGED'
wr('ownC.before.json',json.loads(cb));(B/'ownC.before.exact.json').write_bytes(cb)
sentinel={'created_utc':datetime.now(timezone.utc).isoformat(),'advance_id':ADV,'worker_id':WORKER,'historical_verified_count':0,'payload_sha256':sha((B/'VERIFIED-evidence.full.json').read_bytes()),'permitted_attempts':1,'automatic_replay':False}
wr('ONCE-SENTINEL.json',sentinel)
receipt={'started_utc':datetime.now(timezone.utc).isoformat(),'API':'astis_advance.transition_advance','advance_id':ADV,'to_state':'VERIFIED','worker_id':WORKER,'actual_API_calls':0,'actual_API_failures':0,'pre_V_count':0,'post_V_count':None,'owner_released':False}
try:
 receipt['actual_API_calls']=1
 astis_advance.transition_advance(ADV,'VERIFIED',worker_id=WORKER,modes=['independent-verification'],evidence=v)
 after=L.read_bytes();assert after.startswith(before);added=after[len(before):];assert added.endswith(b'\n') and len(added.splitlines())==1
 event=json.loads(added);assert event['advance_id']==ADV and event['from_state']=='PROVED_LOCAL' and event['to_state']=='VERIFIED' and event['worker_id']==WORKER and event['evidence']==v
 (B/'actual-VERIFIED-append.exact.jsonl').write_bytes(added)
 rows2=[json.loads(l) for l in after.splitlines() if l.strip()];receipt['post_V_count']=nV(rows2);assert receipt['post_V_count']==1
 c=json.loads(cb);assert c['status']=='proved_locally' and c['evidence']['independent_verification']==''
 c['status']='independently_verified';c['evidence']['independent_verification']={'verifier_id':WORKER,'verified_commit':v['verified_commit'],'verification_metadata_HEAD':v['verification_metadata_HEAD'],'normal_evidence':str((B/'VERIFIED-evidence.full.json').relative_to(R)),'normal_evidence_sha256':sha((B/'VERIFIED-evidence.full.json').read_bytes()),'append_sha256':sha(added),'decision':str((B/'independent-decision.json').relative_to(R)),'decision_sha256':sha((B/'independent-decision.json').read_bytes()),'boundary':'S only local independent verification. P actual uncentered consumer; no T/fullR9/main/Goal or stabilization/publication/purification credit; owner retained.'}
 CELL.write_text(json.dumps(c,indent=2,ensure_ascii=False)+'\n');(B/'ownC.after.exact.json').write_bytes(CELL.read_bytes())
 receipt.update({'normal_API_returned':True,'single_exact_append_sha256':sha(added),'ownC_before_sha256':sha(cb),'ownC_after_sha256':sha(CELL.read_bytes()),'original20_payload_values_preserved':True,'exit':0})
 print('NORMAL_VERIFIED_ONCE_RETURNED; S V0->1; exact append saved; own cell only status/evidence changed')
except BaseException:
 # This counts actual API exceptions separately from post-call assertions/cell failure.
 receipt['normal_API_returned']=('after' in locals())
 receipt['actual_API_failures']=0 if receipt['normal_API_returned'] else 1
 receipt['exception']=traceback.format_exc();receipt['exit']=1
 traceback.print_exc();raise
finally:
 receipt['finished_utc']=datetime.now(timezone.utc).isoformat();wr('normal-API-receipt.json',receipt)
