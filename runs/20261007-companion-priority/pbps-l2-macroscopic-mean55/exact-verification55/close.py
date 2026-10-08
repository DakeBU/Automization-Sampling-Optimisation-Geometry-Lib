from common import *
sys.path[:0]=[str(R),str(R/'tools')]
from tools import astis_advance as advance,astis_publication as pub
assert git('rev-parse','HEAD')==SCI
state=advance.current_advances();assert state[ADV]['state']=='VERIFIED' and state[ADV]['latest_evidence']['verifier_id']==ACTOR
assert [k for k,v in state.items() if v['state']=='STABILIZING']==['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel']
assert sorted(git('diff','--name-only').splitlines())==sorted([CELL,'runs/substantive_advances.jsonl'])
pub.check_advance([TARGET],reviewed=True)
committed=load(O/'committed-inputs.json');native=load(O/'native-input-checks.json');closure=load(O/'closure-checks.json');transition=load(O/'transition.readback.json')
changed={CELL:O/'before.cell.raw.snapshot.json','runs/substantive_advances.jsonl':O/'before.ledger.raw.snapshot.jsonl'}
inputs={};final_commit=[]
for e in committed['bindings']:
 p=changed.get(e['path'],e['path']);assert equal(e['current'],p)
 final_commit.append(dict(science_original=e['current'],current_binding=pin(p),mapping='Independent admission BEFORE snapshot; exact scientific raw/LF preserved' if e['path'] in changed else None))
 inputs[pin(p)['path']]=pin(p)
for e in native['checks']+closure['native_closure_actual_pins']:
 p=changed.get(e['actual']['path'],e['actual']['path']);assert equal(e['actual'],p),e['actual']['path'];inputs[pin(p)['path']]=pin(p)
for p in [CELL,AUDIT,'runs/substantive_advances.jsonl','lean-toolchain','lake-manifest.json','tools/astis_publication.py','tools/astis_advance.py','tools/astis_frontier_cells.py','tools/astis_semantic_roundtrip.py','tools/astis_contributor_contract.py']:inputs[pin(p)['path']]=pin(p)
dump('inputs.final.json',dict(status='PASS',checked_commit=SCI,science_entries=1821,original_freeze_count=282,source_original_counts=[297,321],whole_math_original_inputs=1753,whole_math_original_outputs=29,committed_post_admission_bindings=final_commit,all_unique_actual_inputs=sorted(inputs.values(),key=lambda x:x['path']),count=len(inputs),original_historical_mappings=native['exact_historical_mappings'],additional_independent_admission_mappings=[dict(original=p,snapshot=pin(s),current=pin(p)) for p,s in changed.items()],no_skip=True))
for p,field in [(O/'verification.before-transition.receipt.json','receipt_sha256'),(O/'receipt.json','receipt_sha256'),(B/'verified.json','verified_payload_sha256')]:selfcheck(p,field)
for row in native['complete_native_runs']+closure['full_named_self_recipes']:
 assert equal(row['input']);selfcheck(row['input']['path'],row['self_field'])
wr=load(B/'whole-math55/run.json');assert logical(wr['run_binding_payload'])==wr['review_run_binding_sha256']
sr=load(B/'independent-review55/run.json');assert logical(load(B/'independent-review55/payload.json'))==sr['run_payload_sha256']
for f,n,h in [('result0.json','decoder_payload','decoder_payload_sha256'),('run.json','run_payload','run_payload_sha256'),('lease.json','closure_payload','closure_payload_sha256')]:
 d=load(B/'anonymous-decoder'/f);selfcheck(B/'anonymous-decoder'/f,'logical_sha256');assert logical(d[n])==d[h]
compiler=load(O/'compiler.lease.json');focused=load(O/'focused.status.json');assert compiler['status']=='CLOSED' and compiler['exit_code']==0 and compiler['process_id']==focused['process_id']==28008 and equal(compiler['log'])
log=path(O/'focused.log').read_text();assert 'sorryAx' not in log and 'Replayed Tests.ProximalBPSL2MacroscopicMean' in log
lease_open=load(O/'lease.json');assert lease_open['status']=='OPEN'
payload=dict(stage='independent exact scientific commit55',verifier_id=ACTOR,checked_commit=SCI,checked_parent=BASE,verdict='ACCEPT_SCOPED_EXACT_COMMIT_VERIFIED',result_kind='integration-node',exact_statement_LF_bytes=2526,science_inputs=1821,math_freeze_inputs=282,source_original_inputs=[297,321],whole_math_inputs=1753,whole_math_outputs=29,original_input_checks=len(native['checks']),native_closure_pin_checks=len(closure['native_closure_actual_pins']),source_binding_sha256='3429f3b54edb1b9e40456d5f25677a1a54b4984f8d62aae273ce650e3b6ce862',source_review_logical_sha256='7c13e04568d44130aad1266fe067712480c2e6592a76b520720557f369caad1b',focused_compiler_PID=28008,focused_exit_code=0,focused_invocations=1,forced_rebuild=False,fake_closure_hits=0,axiom_closures='three standard3 only',transition='PROVED_LOCAL→VERIFIED by whole_math52',cell='independently_verified',sole_STABILIZING='ASTIS-SA-20261005-SPHMCImplementedPhaseKernel',receipt=pin(O/'receipt.json'),verified=pin(B/'verified.json'),actual_final_inputs=pin(O/'inputs.final.json'),actual_closing_python_PID=os.getpid(),remaining_boundary=load(O/'receipt.json')['remaining_boundary'])
out_before=[pin(p) for p in sorted(O.iterdir()) if p.is_file() and p.name not in ['lease.json','run.json','readback.json','outputs.json']]+[pin(B/'verified.json')]
for e in out_before:assert equal(e)
run=dict(schema_version='independent-native-exact55-run/v1',status='PASS',actor=ACTOR,checked_commit=SCI,actual_closing_python_PID=os.getpid(),actual_inputs=sorted(inputs.values(),key=lambda x:x['path']),actual_outputs_before_run_and_readback=out_before,run_binding_payload=payload,review_run_binding_sha256=logical(payload),payload_recipe='SHA256 exact run_binding_payload sorted compact UTF8 ensure_ascii=False allow_nan=False no newline',full_run_recipe='SHA256 COMPLETE run minus ONLY run_sha256 sorted compact UTF8 ensure_ascii=False allow_nan=False no newline',output_manifest_recipe='Complete actual output pins including run/readback/parent verified in outputs.json, excluding only final lease and manifest self; final lease pins manifest.',compiler=dict(actual_PID=28008,exit_code=0,invocations=1,forced_rebuild=False,actual_CLOSED_lease=pin(O/'compiler.lease.json')),independent_transition=pin(O/'transition.readback.json'),remaining_boundary=payload['remaining_boundary'],exit_code=0)
run['run_sha256']=logical(run);dump('run.json',run)
assert selfcheck(O/'run.json')['logical_sha256']==run['run_sha256'] and logical(load(O/'run.json')['run_binding_payload'])==run['review_run_binding_sha256']
for e in run['actual_inputs']+out_before:assert equal(e)
readback=dict(status='PASS',checked_commit=SCI,all_actual_inputs=len(inputs),pre_run_actual_outputs=len(out_before),run=pin(O/'run.json'),complete_run_minus_self_sha256=run['run_sha256'],separate_payload_sha256=run['review_run_binding_sha256'],receipt=pin(O/'receipt.json'),parent_verified=pin(B/'verified.json'),source_and_whole_and_decoder_complete_native_hashes_recomputed=True,all_original_math282_source297_321_and_whole1753_29_pass=True,Git1821_post_verified_before_mappings_exact=True,actual_compiler_CLOSED=True,final_lease_not_yet_written=True)
dump('readback.json',readback)
out_all=[pin(p) for p in sorted(O.iterdir()) if p.is_file() and p.name not in ['lease.json','outputs.json']]+[pin(B/'verified.json')]
for e in out_all:assert equal(e)
dump('outputs.json',dict(status='PASS',count=len(out_all),actual_output_pins=out_all,output_list_logical_sha256=logical(out_all),recipe='Actual owned files plus parent verified.json; only this manifest and actual final lease excluded to avoid cycles. Readback before actual closure.'))
assert logical(load(O/'outputs.json')['actual_output_pins'])==load(O/'outputs.json')['output_list_logical_sha256']
for e in load(O/'outputs.json')['actual_output_pins']+run['actual_inputs']:assert equal(e)
assert selfcheck(O/'run.json')['logical_sha256']==run['run_sha256']
# Everything below uses already-held values. Actual final owned filesystem operation is CLOSED lease write.
receipt_pin=pin(O/'receipt.json');run_pin=pin(O/'run.json');verified_pin=pin(B/'verified.json');manifest_pin=pin(O/'outputs.json');readback_pin=pin(O/'readback.json');compiler_pin=pin(O/'compiler.lease.json')
lease=dict(lease_open,status='CLOSED',read='CLOSED',write='CLOSED',Python='CLOSED',compiler='CLOSED',closed_utc=utc(),actual_closing_python_PID=os.getpid(),actual_focused_compiler_PID=28008,actual_compiler_exit=0,focused_invocations=1,exit_code=0,receipt=receipt_pin,run=run_pin,run_logical_sha256=run['run_sha256'],review_payload_sha256=run['review_run_binding_sha256'],verified=verified_pin,actual_compiler_CLOSED_lease=compiler_pin,actual_outputs_manifest=manifest_pin,actual_input_count=len(inputs),actual_output_count=len(out_all),readback=readback_pin,closure_recipe='Actual final owned filesystem write. All raw/LF inputs, outputs, complete run-minus-self and separate payload, receipt and readback checked BEFORE CLOSED. No filesystem operation afterward. Actual closing Python completion must be observed externally.')
lease['lease_run_sha256']=logical(lease);lb=(json.dumps(lease,ensure_ascii=False,indent=2)+'\n').encode('utf-8');capsule=dict(status='ACCEPT_SCOPED_EXACT_COMMIT_VERIFIED',checked_commit=SCI,transition='VERIFIED',actual_input_count=len(inputs),actual_output_count=len(out_all),receipt=receipt_pin,run=run_pin,run_logical_sha256=run['run_sha256'],payload_sha256=run['review_run_binding_sha256'],verified=verified_pin,lease=dict(path=(O/'lease.json').relative_to(R).as_posix(),bytes=len(lb),raw_sha256=sha(lb),lf_sha256=sha(lb.replace(b'\r\n',b'\n')),logical_sha256=lease['lease_run_sha256']),compiler_PID=28008,compiler_exit=0,actual_closing_python_PID=os.getpid(),all_leases='CLOSED',remaining_boundary=payload['remaining_boundary'])
(O/'lease.json').write_bytes(lb)
print(json.dumps(capsule,ensure_ascii=False))
