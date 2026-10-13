import os,sys,json,subprocess,traceback
from pathlib import Path
import review69 as R
O=R.O;pin=R.pin;sha=R.sha;save=R.save;get=R.get;now=R.now

def owned(exclude=()):return [pin(p) for p in sorted(O.rglob('*')) if p.is_file() and p.relative_to(O).as_posix() not in exclude]
def finalize():
 R.stable();assert get('header-review.json')['status']=='HEADER69_ACCEPTED_TYPECHECKED_NO_TARGET_PROOF'
 label=sys.argv[2] if len(sys.argv)>2 else 'finalize';active=[label+'.stdout.log',label+'.stderr.log',label+'.terminal.json']
 payload=dict(name='COMPLETE_INDEPENDENT_HEADER_MATH69_RAW_PAYLOAD',actor=R.ACTOR,checked_parent=R.BASE,header_review=get('header-review.json'),complete_original_RAW_LF_inputs=get('inputs.manifest.json'),all_pre_payload_owned_RAW_LF_outputs=owned(exclude=active),target_proof_credit=False,active_terminal_outputs_bound_by_final_lease=active,closure_self_layers='Final CLOSED_LAST lease binds every owned file except only itself; its own RAW is independently read after closure.')
 save('named-header-review.payload.json',payload)
 rows=owned(exclude=active+['outputs.manifest.json','run.json','lease.final.json']);save('outputs.manifest.json',dict(file_count=len(rows),rows=rows,self_layers='Manifest/run/active finalizer/readback/close files are bound in the final CLOSED_LAST lease.'))
 run=dict(schema_version=1,status='HEADER69_ACCEPTED_TYPECHECKED_NO_TARGET_PROOF',actor=R.ACTOR,checked_parent=R.BASE,actual_finalizer_PID=os.getpid(),utc=now(),input_manifest=pin(O/'inputs.manifest.json'),input_count=14,native_header_review=pin(O/'header-review.json'),named_complete_RAW_review=pin(O/'named-header-review.payload.json'),outputs_manifest=pin(O/'outputs.manifest.json'),fresh_compiler=get('compiler.receipt.json'),exact_private_full_Prop_and_original_caller=True,parent_delta_only_D_semantics_intertwining=True,private_mathematical_providers=0,header_blockers=[],no_target_proof_credit=True,SAU_claim=False,VERIFIED=False,canonical_Git_ledger_writes=False,full_Exposition=False,PURIFIED=False,whole_paper=False,Goal=False,logical_hash_policy='Canonical sorted compact JSON of the WHOLE run object after deleting ONLY top-level run_sha256.',named_RAW_hash_policy='Exact complete bytes of named-header-review.payload.json; no JSON reserialization.',closure_policy='CLOSED_LAST final lease enumerates every owned file except itself, including all helper/self/negative/finalization and terminal layers; read-only postclose independently computes lease RAW.')
 run['run_sha256']=sha(json.dumps(run,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode());save('run.json',run);print(json.dumps(dict(status='FINALIZED',actual_PID=os.getpid(),whole_logical_run_sha256=run['run_sha256'],complete_named_RAW=pin(O/'named-header-review.payload.json'))))
def readback():
 p=subprocess.Popen([sys.executable,'-B','-X','utf8',str(O/'readonly69.py'),'preclose'],cwd=R.ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=p.communicate();(O/'readback.validator.stdout.log').write_bytes(out);(O/'readback.validator.stderr.log').write_bytes(err);save('readback.validator.terminal.json',dict(actual_parent_PID=os.getpid(),actual_readonly_validator_PID=p.pid,exit_code=p.returncode,terminal_closed=True,stdout=pin(O/'readback.validator.stdout.log'),stderr=pin(O/'readback.validator.stderr.log')));assert p.returncode==0;print(out.decode(),end='')
if __name__=='__main__':
 try:{'finalize':finalize,'readback':readback}[sys.argv[1]]()
 except Exception as e:
  if not (O/'lease.final.json').exists():save((sys.argv[2] if len(sys.argv)>2 else sys.argv[1])+'.failure.json',dict(actual_PID=os.getpid(),utc=now(),error=repr(e),traceback=traceback.format_exc()))
  raise
