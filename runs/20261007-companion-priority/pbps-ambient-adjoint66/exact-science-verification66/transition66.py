import sys,traceback
from verify66 import *
def transition():
 checkpins()
 for f in ['focused.result.json','bindings.result.json','gates.result.json','reviewed-fakeclosure.result.json']:
  assert read(O/f)['status']=='PASS'
 assert not (D/'verified.json').exists()
 sys.path.insert(0,str(R));from tools import astis_advance as advance
 ledger=advance.DEFAULT_ADVANCE_LEDGER
 before=pin(ledger);item=advance.current_advances()[SAU];assert item['state']=='PROVED_LOCAL' and item['owner_id']!=ACTOR
 write('ledger.before.compact.json',{'exact_checked_commit':C,'ledger_RAW_LF':before,'target_advance':SAU,'target_state':item['state'],'proving_owner':item['owner_id'],'independent_verifier':ACTOR,'no_whole_ledger_copy':True,'actual_pid':os.getpid()})
 evidence={'verifier_id':ACTOR,'verified_commit':C,'gate':{'status':'PASS','focused_compiler':pin(O/'focused.result.json'),'fresh_required_admission_gates':pin(O/'gates.result.json'),'checked_scope':'Exact SCI66 main and genuine Test, fresh focused build plus fresh Test compiler, reviewed publication/source/semantic/frontier/contributor checks; no aggregate/site/Registry integration claim'},'source_audit':{'status':'PASS','native_bindings':pin(O/'bindings.result.json'),'semantic_slots':7,'literal_BODY_steps':6,'selected_primary_items':310,'no_mathematical_repair':True,'private_literal_Prop_expansions_whole_module_reviewed':True},'fake_closure_scan':{'status':'PASS','receipt':pin(O/'reviewed-fakeclosure.result.json'),'forbidden_hits':[],'private_mathematical_providers':0,'standard_axioms':['propext','Classical.choice','Quot.sound']},'publication_declarations':[DECL],'independent_actor_not_proving_owner':True,'remaining_boundary':'Canonical ambient adjoint and globally centered actual-input decomposition/norm budget only. No full B20/B21,root commutation,H1,onto,reverse product,dynamics/main/errors/expected cost/actual-input composition,aggregate/reader/full Exposition/PURIFIED/whole paper/Goal credit.'}
 write('transition.evidence.json',evidence)
 assert pin(ledger)==before
 advance.transition_advance(SAU,'VERIFIED',worker_id=ACTOR,evidence=evidence)
 after=pin(ledger)
 with ledger.open('rb') as stream:
  prefix=stream.read(before['raw_bytes']);tail=stream.read()
 assert sha(prefix)==before['raw_sha256'] and tail.endswith(b'\n') and len(tail.splitlines())==1
 event=json.loads(tail);assert event['advance_id']==SAU and event['to_state']=='VERIFIED' and event['worker_id']==ACTOR and event['evidence']['verified_commit']==C
 (O/'verified.appended-event.exactraw.jsonl').write_bytes(tail)
 state=advance.current_advances()[SAU];assert state['state']=='VERIFIED' and state['latest_evidence']['verified_commit']==C
 result={'status':'VERIFIED','checked_commit':C,'actual_parent':P,'verifier_id':ACTOR,'proving_owner':item['owner_id'],'actual_transition_pid':os.getpid(),'actual_terminal_utc':now(),'proper_nonowner_transition':True,'ledger_before':before,'ledger_after':after,'historical_prefix_preserved':True,'appended_events':1,'exact_appended_event':pin(O/'verified.appended-event.exactraw.jsonl'),'gate':evidence['gate'],'source_audit':evidence['source_audit'],'fake_closure_scan':evidence['fake_closure_scan'],'publication_declarations':[DECL],'remaining_boundary':evidence['remaining_boundary'],'full_Exposition':False,'PURIFIED':False,'aggregate_site_Registry_writes':False}
 (D/'verified.json').write_bytes((json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode())
 write('transition.result.json',dict(result,authorized_verified_json=pin(D/'verified.json')))
 print(json.dumps({'status':'VERIFIED','actual_pid':os.getpid(),'exact_commit':C,'one_event_appended':True,'nonowner':True}),flush=True)
if __name__=='__main__':
 try:transition()
 except Exception as e:
  write('transition.failure.json',{'status':'FAIL','actual_pid':os.getpid(),'exception':repr(e),'traceback':traceback.format_exc(),'utc':now()});raise
