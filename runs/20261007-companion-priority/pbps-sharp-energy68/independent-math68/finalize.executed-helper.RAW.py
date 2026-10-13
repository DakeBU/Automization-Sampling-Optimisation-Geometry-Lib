import sys,os,json,hashlib,traceback,subprocess
from pathlib import Path
import review68 as R
import final68 as F
O=R.O;pin=R.pin;sha=R.sha;save=R.save;get=R.get;now=R.now

def canonical(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def owned(exclude=()):return [pin(p) for p in sorted(O.rglob('*')) if p.is_file() and p.relative_to(O).as_posix() not in exclude]
def finalize():
 F.stable();assert not (O/'lease.final.json').exists();assert get('mathematical-review.json')['mathematical_blockers']==[] and get('presentation-overlay.decision.json')['decision']=='APPROVED_PROPOSED_V2_NOT_APPLIED'
 manifests={n:get(n) for n in ['leaf.inputs.manifest.json','final.inputs.manifest.json','audit.inputs.manifest.json','overlay.inputs.manifest.json']}
 rows=[x for m in manifests.values() for x in m['inputs']];unique={x['original']['path'] for x in rows}
 payload=dict(schema_version=1,name='COMPLETE_NATIVE_INDEPENDENT_MATHEMATICS68_RAW_PAYLOAD',actor=R.ACTOR,checked_base=R.BASE,candidates_uncommitted=True,mathematical_review=get('mathematical-review.json'),stage1_shared_leaf_review=get('shared-leaf.mathematical-review.json'),complete_named_input_manifests=manifests,all_pre_payload_owned_RAW_LF_outputs=owned(),input_row_count=len(rows),distinct_original_input_paths=len(unique),finite_proposed_presentation_maps=get('presentation-overlay.decision.json')['complete_before_after_differences'],self_and_terminal_layer_binding='The final CLOSED_LAST lease binds this complete named RAW payload, run, output manifest and every finalizer/readback/close/self file. This payload does not claim a RAW digest of itself or future bytes.',no_source_VERIFIED_or_whole_paper_credit=True)
 save('named-mathematical-review.payload.json',payload)
 outputrows=owned(exclude=['outputs.manifest.json','run.json','lease.final.json'])
 save('outputs.manifest.json',dict(schema_version=1,actual_finalizer_PID=os.getpid(),utc=now(),rows=outputrows,file_count=len(outputrows),self_layer_rule='outputs.manifest/run/finalizer-terminal/readback/close files are bound by CLOSED_LAST lease, avoiding circular RAW digests. No unlisted owned files may survive closure.'))
 run=dict(schema_version=1,actor=R.ACTOR,status='MATHEMATICS_ACCEPTED_WITH_APPROVED_UNAPPLIED_PRESENTATION_V2',advance_id='ASTIS-SA-20261009-PBPSSharpCorrectorEnergy',checked_base=R.BASE,checked_SCI68_commit=None,actual_finalizer_PID=os.getpid(),utc=now(),native_named_complete_RAW_payload=pin(O/'named-mathematical-review.payload.json'),native_verdict=pin(O/'mathematical-review.json'),outputs_manifest=pin(O/'outputs.manifest.json'),inputs_manifests={n:pin(O/n) for n in manifests},input_row_count=len(rows),distinct_original_input_paths=len(unique),final_original_input_rows=44,focused_fresh_Lean_checks={q:get(f'{q}.compiler.receipt.json') for q in ['leaf','main','test']},all3_standard3=True,private_full_Props=2,private_math_providers=0,fake_closure_hits=0,original_BODY_strict_RAW=9,original_BODY_negative_LF_boundaries=2,proposed_V2_BODY_strict_RAW=11,approved_overlay=pin(O/'presentation-overlay.decision.json'),closure_policy=dict(logical_hash='Canonical JSON of the WHOLE run object after deleting ONLY top-level run_sha256; no other fields removed.',named_RAW_hash='Exact complete bytes of explicitly named named-mathematical-review.payload.json; no reserialization.',all_owned_layers='Final CLOSED_LAST lease enumerates RAW/LF hashes of every owned output except only its own last-write file; actual postclose validator hashes lease externally and performs0writes.',lease_not_yet_closed_at_run_creation=True),VERIFIED=False,canonical_Git_ledger_writes=False,PURIFIED=False,full_Exposition=False,whole_paper=False,Goal=False)
 run['run_sha256']=sha(canonical(run));save('run.json',run)
 print(json.dumps(dict(status='FINALIZED',actual_PID=os.getpid(),whole_logical_run_sha256=run['run_sha256'],named_complete_RAW_payload=pin(O/'named-mathematical-review.payload.json'),inputs_total_rows=len(rows),distinct_input_paths=len(unique))))
def readback():
 q=subprocess.run([sys.executable,'-B','-X','utf8',str(O/'readonly-validator68.py'),'preclose'],cwd=R.ROOT,capture_output=True)
 (O/'readback.validator.stdout.log').write_bytes(q.stdout);(O/'readback.validator.stderr.log').write_bytes(q.stderr)
 save('readback.validator.receipt.json',dict(actual_parent_PID=os.getpid(),exit_code=q.returncode,terminal_closed=True,stdout=pin(O/'readback.validator.stdout.log'),stderr=pin(O/'readback.validator.stderr.log'),validator_result=json.loads(q.stdout.decode()) if q.returncode==0 else None))
 assert q.returncode==0;print(q.stdout.decode(),end='')
if __name__=='__main__':
 try:{'finalize':finalize,'readback':readback}[sys.argv[1]]()
 except Exception as e:
  if not (O/'lease.final.json').exists():save((sys.argv[2] if len(sys.argv)>2 else sys.argv[1])+'.failure.json',dict(actual_PID=os.getpid(),utc=now(),error=repr(e),traceback=traceback.format_exc()))
  raise
