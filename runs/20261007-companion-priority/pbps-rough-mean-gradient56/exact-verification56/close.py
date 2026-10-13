from common import *
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,str(R/'tools'))
import astis_advance,astis_publication
AID='ASTIS-SA-20261008-PBPSRoughMeanGradient';CID='ASTIS-SW-PBPS-rough-mean-gradient'
CELL=R/'research-wiki/frontier-cells'/f'{CID}.json';LEDGER=R/'runs/substantive_advances.jsonl';AUD=R/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261008-PBPSRoughMeanGradient.json'
assert git('rev-parse','HEAD')==BASE
receipt=load(O/'receipt.json');run=load(O/'run.json');verified=load(B/'verified.json');selfcheck(O/'receipt.json','receipt_sha256');selfcheck(O/'run.json');selfcheck(B/'verified.json','verified_sha256')
assert logical(run['verifier_binding_payload'])==run['verifier_binding_sha256'] and verified['checked_commit']==BASE
for e in run['actual_outputs_before_run']:assert equal(e),e['path']
mapped=[]
for e in run['inputs']['inputs']:
 p=e['path'];m=run['inputs']['current_mutable_input_mapping_after_verification'].get(p)
 if m:
  assert equal(m) and equal(e,m['path']);mapped.append({'original':e,'exact_before_snapshot':m,'actual_verified_current':pin(p)})
 else:assert equal(e),p
assert len(mapped)==2
strict('originals.final.post-transition.json')
before=load(O/'cell.before.raw.snapshot.json');after=load(CELL);after2=load(CELL)
assert after['status']=='independently_verified' and after['evidence']['independent_verification']==(O/'receipt.json').relative_to(R).as_posix()
assert isinstance(after['evidence']['independent_verification'],str)
after2['status']=before['status'];del after2['evidence']['independent_verification'];del after2['evidence']['independent_verification_details'];assert after2==before
assert AUD.read_bytes()==(O/'audit.before.raw.snapshot.json').read_bytes()
prefix=(O/'ledger.before.raw.snapshot.jsonl').read_bytes();current=LEDGER.read_bytes();assert current.startswith(prefix)
tail=current[len(prefix):].decode('utf8').splitlines();assert len(tail)==1;record=json.loads(tail[0]);assert record['advance_id']==AID and record['to_state']=='VERIFIED' and record['worker_id']==ACTOR
assert record['evidence']['verified_commit']==BASE and equal(record['evidence']['verification_receipt']) and equal(record['evidence']['verification_native_run'])
state=astis_advance._replay_advances([json.loads(x) for x in current.decode('utf8').splitlines() if x.strip()]);assert state[AID]['state']=='VERIFIED' and state[AID]['last_actor']==ACTOR
assert [k for k,v in state.items() if v['state']=='STABILIZING']==['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel']
astis_publication.check_advance([TARGET],reviewed=True)
env=dict(os.environ);env.update(PYTHONUTF8='1',PYTHONDONTWRITEBYTECODE='1')
cmd=[sys.executable,'-B','tools/astis_frontier_cells.py','check']
with (O/'frontier.post-transition.log').open('wb') as log:
 p=subprocess.Popen(cmd,cwd=R,env=env,stdout=log,stderr=subprocess.STDOUT);code=p.wait()
assert code==0
dump('frontier.post-transition.status.json',{'status':'PASS','command':cmd,'actual_PID':p.pid,'exit_code':code,'Python':'CLOSED','log':pin(O/'frontier.post-transition.log'),'reason':'Recheck newly changed exact cell required string evidence schema; no new compiler'})
for e in load(O/'Git-science.entries.json')['entries']:
 pin_before=e['current'];m=run['inputs']['current_mutable_input_mapping_after_verification'].get(pin_before['path']);assert equal(pin_before,m['path'] if m else None)
assert load(O/'compiler.lease.json')['status']=='CLOSED' and load(O/'focused.status.json')['exit_code']==0
outputs=[pin(p) for p in sorted(O.iterdir()) if p.is_file() and p.name not in ('lease.json','readback.json','outputs.final.json')]+[pin(B/'verified.json')]
for e in outputs:assert equal(e)
manifest={'status':'PASS_ACTUAL_FINAL_OUTPUT_READBACK','checked_commit':BASE,'output_count':len(outputs),'outputs':outputs,'excludes':'Only self outputs.final.json, later readback.json and actual final CLOSED lease, each bound externally by final lease to avoid circular raw hash','complete_self_recipe':'Complete manifest minus ONLY content_self_sha256, sorted compact UTF8 JSON ensure_ascii=False allow_nan=False no newline'}
manifest['content_self_sha256']=logical(manifest);dump('outputs.final.json',manifest);selfcheck(O/'outputs.final.json','content_self_sha256')
readback={'status':'PASS_BEFORE_CLOSED_LAST','checked_commit':BASE,'actual_closing_python_PID':os.getpid(),'strict_originals':418,'Git_committed_entries':1361,'math_distinct_precommit_inputs':423,'source_originals':432,'source_manifest_plus_manifest_complete_outputs':891,'source_historical_before_mappings':2,'exact_verified_admin_before_mappings':mapped,'native_source_math_full_self_checks':len(load(O/'checks.json')['native_complete_self_checks']),'raw_LF_native_pin_checks':load(O/'checks.json')['actual_raw_LF_pin_checks_count'],'distinct_actual_current_inputs_before_transition':len(run['inputs']['inputs']),'actual_final_outputs':len(outputs),'whole_receipt_self_sha256':receipt['receipt_sha256'],'whole_run_self_sha256':run['run_sha256'],'distinct_verifier_payload_sha256':run['verifier_binding_sha256'],'whole_verified_self_sha256':verified['verified_sha256'],'output_manifest':pin(O/'outputs.final.json'),'receipt':pin(O/'receipt.json'),'run':pin(O/'run.json'),'verified':pin(B/'verified.json'),'actual_transition':pin(O/'transition.json'),'cell_actual_independently_verified':pin(CELL),'ledger_actual_VERIFIED':pin(LEDGER),'sole_STABILIZING':'ASTIS-SA-20261005-SPHMCImplementedPhaseKernel','actual_posttransition_frontier_PID':p.pid,'posttransition_frontier_exit_code':0,'all_readbacks_and_hashes_before_closure':True,'no_new_compiler':True,'checked_utc':utc()}
dump('readback.json',readback);assert load(O/'readback.json')==readback
lease={'schema_version':1,'status':'CLOSED','stage':'Independent EXACT-SCIENCE verification56','verifier_id':ACTOR,'checked_commit':BASE,'actual_closing_python_PID':os.getpid(),'opened_utc':load(O/'lease.json')['opened_utc'],'closed_utc':utc(),'read':'CLOSED','write':'CLOSED','Python':'CLOSED','compiler':'CLOSED','compiler_PID':load(O/'focused.status.json')['process_id'],'compiler_exit_code':0,'compiler_closed_lease':pin(O/'compiler.lease.json'),'receipt':pin(O/'receipt.json'),'run':pin(O/'run.json'),'verified':pin(B/'verified.json'),'transition':pin(O/'transition.json'),'output_manifest':pin(O/'outputs.final.json'),'readback':pin(O/'readback.json'),'whole_run_sha256':run['run_sha256'],'distinct_payload_sha256':run['verifier_binding_sha256'],'actual_VERIFIED_actor':ACTOR,'closed_last':'All input/Git/actual outputs/self/distinct payload/canonical transition/required string evidence readbacks complete before this final filesystem write. No filesystem operation afterward.','actual_foreground_exit_condition':'Finalizer prints in-memory bindings and exits0; tool terminal exit0 supplies actual closing Python process completion. No background process or persistent handle.','complete_self_recipe':'Entire lease minus ONLY lease_sha256; sorted compact UTF8 JSON ensure_ascii=False allow_nan=False no newline'}
lease['lease_sha256']=logical(lease);lb=(json.dumps(lease,ensure_ascii=False,indent=2)+'\n').encode();assert logical({k:v for k,v in json.loads(lb).items() if k!='lease_sha256'})==lease['lease_sha256']
result={'status':'VERIFIED_ALL_RESOURCES_CLOSED_ON_FOREGROUND_EXIT0','checked_commit':BASE,'verifier_id':ACTOR,'compiler_PID':lease['compiler_PID'],'compiler_exit_code':0,'closing_python_PID':os.getpid(),'counts':{k:readback[k] for k in ['strict_originals','Git_committed_entries','source_originals','source_manifest_plus_manifest_complete_outputs','distinct_actual_current_inputs_before_transition','actual_final_outputs','raw_LF_native_pin_checks']},'receipt':lease['receipt'],'receipt_logical_sha256':receipt['receipt_sha256'],'run':lease['run'],'run_logical_sha256':run['run_sha256'],'distinct_verifier_binding_sha256':run['verifier_binding_sha256'],'verified':lease['verified'],'verified_logical_sha256':verified['verified_sha256'],'lease':{'path':(O/'lease.json').relative_to(R).as_posix(),'bytes':len(lb),'raw_sha256':sha(lb),'lf_sha256':sha(lb),'logical_sha256':lease['lease_sha256']}}
# Actual last filesystem operation, followed only by in-memory stdout and normal exit0.
(O/'lease.json').write_bytes(lb)
print(json.dumps(result,ensure_ascii=False))
