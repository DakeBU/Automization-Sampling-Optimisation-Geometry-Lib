from common_v2 import *
import traceback
pre=json.loads((OUT/'pre-invariants.json').read_bytes());payload=json.loads((OUT/'actual-VERIFIED-evidence.full.json').read_bytes())
old=(ROOT/LEDGER).read_bytes();assert len(old)==pre['ledger']['bytes'] and sha(old)==pre['ledger']['sha256']
assert git('rev-parse','HEAD').decode().strip()==HEAD
assert git('rev-parse','refs/heads/main').decode().strip()==LOCAL_MAIN and git('rev-parse','refs/remotes/origin/main').decode().strip()==ORIGIN_MAIN
state=advance._replay_advances(records(old))[TARGET];assert state['state']=='PROVED_LOCAL' and state['owner_id']==OWNER
assert not any(r.get('advance_id')==TARGET and r.get('to_state')=='VERIFIED' for r in records(old))
assert payload['verifier_id']==WORKER and payload['verified_commit']==CANDIDATE
sentinel=OUT/'normal-api-attempted.once.json'
with sentinel.open('x') as f:json.dump({'method':'tools.astis_advance.transition_advance','advance_id':TARGET,'to_state':'VERIFIED','worker_id':WORKER,'attempts':1,'automatic_retry':False},f,indent=2);f.write('\n')
api_error=None
try:advance.transition_advance(TARGET,'VERIFIED',worker_id=WORKER,evidence=payload)
except BaseException:api_error=traceback.format_exc()
now=(ROOT/LEDGER).read_bytes();rs=records(now);own=advance._replay_advances(rs)[TARGET];suffix=now[len(old):] if now.startswith(old) else b''
outcome={'normal_API_calls':1,'api_returned_successfully':api_error is None,'actual_state':own['state'],'actual_target_VERIFIED_events':sum(r.get('advance_id')==TARGET and r.get('to_state')=='VERIFIED' for r in rs),'ledger_prefix_preserved':now.startswith(old),'append_bytes':len(suffix),'append_sha256':sha(suffix),'error':api_error,'retry':'No replay under any outcome.'}
write(OUT/'normal-api-outcome.json',outcome);print(json.dumps(outcome,indent=2),flush=True)
assert now.startswith(old) and len(records(suffix))==1,'Inspect saved actual outcome; never replay API.'
event=records(suffix)[0]
assert event['advance_id']==TARGET and event['from_state']=='PROVED_LOCAL' and event['to_state']=='VERIFIED' and event['worker_id']==WORKER and event['evidence']==payload
assert own['state']=='VERIFIED' and outcome['actual_target_VERIFIED_events']==1
with (OUT/'actual-VERIFIED-append.original.jsonl').open('xb') as f:f.write(suffix)
cell=json.loads((ROOT/CELL).read_bytes());rest=json.loads(json.dumps(cell));rest.pop('status');rest['evidence'].pop('independent_verification')
assert sha(canonical(rest))==pre['own_cell']['semantic_rest_sha256'] and cell['status']=='proved_locally' and cell['evidence']['independent_verification']==''
cell['status']='independently_verified';cell['evidence']['independent_verification']=rel(E/'actual-VERIFIED-independent-decision.json')
(ROOT/CELL).write_text(json.dumps(cell,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'actual_cell_status':cell['status'],'only_two_preseeded_cell_fields_changed':True,'original_append_sha256':sha(suffix),'full_payload_sha256':sha((OUT/'actual-VERIFIED-evidence.full.json').read_bytes())},indent=2))
if api_error is not None:raise RuntimeError('Actual successful event preserved and inspected; API error retained; never replay.')
