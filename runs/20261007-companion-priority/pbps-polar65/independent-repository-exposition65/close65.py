import json,os,pathlib,sys,traceback
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from review65 import R,O,D,I,C,P,ACTOR,read,write,pin,gitpin,sha,canon,inputcheck,equalpin,owned,now
def checkall():
 inputcheck();s=read(O/'inputs.supplement.json')
 for x in s['external_files']:equalpin(x)
 for x in s['exact_Git_blobs']:assert gitpin(x['path'],x['commit'])==x
 r=read(O/'bounded-review.result.json');a=read(O/'reader-admission.result.json');assert r['status']==a['status']=='ACCEPTED_WITH_EXPLICIT_READER_DEBT' and r['checked_commit']==a['checked_commit']==C
 for x in r['preservation']['cached_RAW_pin_manifest']:equalpin(x)
 for x in r['preservation']['unrelated_exact_restorations']:equalpin(x['lossless_emitted_snapshot'])
 for x in r['preservation']['preserved_existing_cards_Git_pins']:assert gitpin(x['path'],x['commit'])==x
 for label in ['freeze','review-v3','admission']:
  j=read(O/(label+'.terminal.json'));assert j['exit_code']==0 and j['terminal_closed']
 for label in ['review','review-v2']:
  j=read(O/(label+'.terminal.json'));assert j['exit_code']==1 and j['terminal_closed']
 return r,a
def logical():
 j=read(O/'run.json');h=j.pop('run_sha256');assert sha(canon(j))==h;return h
def basic():
 checkall();h=logical();r=read(O/'run.json');p=pin(O/'named-repository-reader.payload.json');assert p==r['complete_named_RAW_review_payload'] and p['raw_sha256']!=h
 for x in read(O/'pre-finalizer.manifest.json')['completed_owned_outputs']:equalpin(x)
 return h,p
def finalize():
 r,a=checkall();existing=owned(exclude=('finalize.stdout.log','finalize.stderr.log'));failures={p.relative_to(O).as_posix():read(p) for p in sorted(O.glob('*failure.json'))}
 verdict={'schema':'independent-INT65-native-bounded-reader-verdict-v1','actor':ACTOR,'status':'ACCEPTED_WITH_EXPLICIT_READER_DEBT','checked_commit':C,'parent':P,'complete_repository_review':r,'complete_reader_admission':a,'original_frozen_inputs':read(O/'inputs.manifest.json'),'finite_input_supplement':read(O/'inputs.supplement.json'),'all_retained_negative_records':failures,'actual_finalizer_pid':os.getpid(),'no_canonical_Git_ledger_source_math_writes':True,'VERIFIED_transition':False,'utc':now()};write('verdict.json',verdict)
 payload={'schema':'COMPLETE_NAMED_RAW_INT65_REPOSITORY_READER_PAYLOAD','complete_native_verdict':verdict,'all_pre_finalizer_owned_output_pins':existing,'exact_RAW_contract':'Complete pretty UTF8 JSON payload. No omitted verdict/input/failure field. Named payload RAW is distinct from verdict.json RAW and whole logical run hash. Closure/self/terminal layers are subsequently fully bound by final CLOSED_LAST lease.','checked_commit':C};write('named-repository-reader.payload.json',payload)
 pending=['pre-finalizer.manifest.json','finalize.stdout.log','finalize.stderr.log','finalize.terminal.json','readback.result.json','readback.stdout.log','readback.stderr.log','readback.terminal.json','closure.result.json','closure.stdout.log','final.manifest.json','lease.final.json']
 run={'schema':'independent-INT65-full-native-logical-run-v1','actor':ACTOR,'checked_commit':C,'parent':P,'status':verdict['status'],'actual_finalizer_pid':os.getpid(),'full_native_logical_review':payload,'complete_named_RAW_review_payload':pin(O/'named-repository-reader.payload.json'),'all_pre_finalizer_owned_output_pins':existing,'pending_self_and_terminal_layers':pending,'run_hash_rule':'Canonical UTF8 JSON sorted keys compact comma/colon ensure_ascii=False; remove ONLY top-level run_sha256. No recursive or additional field omission.','closure_contract':'Final CLOSED_LAST lease RAW/LF binds all own files including negatives, scripts, manifests, self and terminals. External read-only postclose binds final lease itself, avoiding circular self hash.','canonical_Git_ledger_Lean_source_math_writes':False,'VERIFIED_transition':False,'finalized_utc':now()};run['run_sha256']=sha(canon(run));write('run.json',run)
 write('pre-finalizer.manifest.json',{'completed_owned_outputs':owned(exclude=('finalize.stdout.log','finalize.stderr.log')),'whole_logical_run_sha256':run['run_sha256'],'complete_named_RAW_review_payload':run['complete_named_RAW_review_payload'],'explicit_pending_layers':pending,'actual_finalizer_pid':os.getpid()});print(json.dumps({'status':'FINALIZED_ACCEPTED_WITH_DEBT','actual_pid':os.getpid(),'whole_logical_run_sha256':run['run_sha256'],'complete_named_RAW_review_sha256':run['complete_named_RAW_review_payload']['raw_sha256']}),flush=True)
def readback():
 h,p=basic();f=read(O/'finalize.terminal.json');assert f['exit_code']==0 and f['terminal_closed'];write('readback.result.json',{'status':'PASS','checked_commit':C,'actual_readback_pid':os.getpid(),'whole_logical_run_sha256':h,'complete_named_RAW_review_payload':p,'all_owned_completed_and_finite_external_Git_RAW_LF_bindings_equal':True,'actual_finalizer_terminal':f,'canonical_Git_ledger_source_math_writes':False,'VERIFIED_transition':False,'utc':now()});print(json.dumps({'status':'READBACK_PASS','actual_pid':os.getpid(),'whole_logical_run_sha256':h}),flush=True)
def close():
 assert not (O/'lease.final.json').exists();h,p=basic();f=read(O/'finalize.terminal.json');b=read(O/'readback.terminal.json');assert f['exit_code']==b['exit_code']==0 and f['terminal_closed'] and b['terminal_closed'];write('closure.result.json',{'status':'ACCEPTED_WITH_READER_DEBT_CLOSURE_PREPARED','checked_commit':C,'actual_close_pid':os.getpid(),'actual_finalizer_pid':f['actual_worker_pid'],'actual_finalizer_exit_code':0,'actual_readback_pid':b['actual_worker_pid'],'actual_readback_exit_code':0,'whole_logical_run_sha256':h,'complete_named_RAW_review_sha256':p['raw_sha256'],'close_exit_observation':'External authoritative foreground terminal observes close EXIT after final lease; no owned write afterward.','canonical_Git_ledger_source_math_writes':False,'VERIFIED_transition':False,'utc':now()})
 line=json.dumps({'status':'CLOSED_LAST_FINAL_WRITE_NEXT','actual_close_pid':os.getpid(),'checked_commit':C,'whole_logical_run_sha256':h,'complete_named_RAW_review_sha256':p['raw_sha256']})+'\n';(O/'closure.stdout.log').write_bytes(line.encode());write('final.manifest.json',{'owned_files_except_this_manifest_and_final_lease':owned(exclude=('final.manifest.json','lease.final.json')),'self_layers':['final.manifest.json','lease.final.json'],'self_binding':'Final lease binds final manifest and all other owned outputs; external read-only postclose binds final lease.','whole_logical_run_sha256':h,'complete_named_RAW_review_payload':p,'actual_close_pid':os.getpid(),'all_negative_and_terminal_layers_included':True})
 files=owned(exclude=('lease.final.json',));lease={'schema':'independent-INT65-repository-reader-CLOSED_LAST-v1','status':'CLOSED_LAST','actor':ACTOR,'owned_prefix':O.as_posix(),'checked_commit':C,'parent':P,'closed_utc':now(),'actual_close_pid':os.getpid(),'actual_finalizer_pid':f['actual_worker_pid'],'actual_finalizer_exit_code':0,'actual_readback_pid':b['actual_worker_pid'],'actual_readback_exit_code':0,'close_exit_observation':'External foreground tool only','whole_logical_run_sha256':h,'complete_named_RAW_review_sha256':p['raw_sha256'],'all_owned_except_this_final_lease':files,'final_owned_file_count':len(files)+1,'last_owned_write':True,'postclose_policy':'READ_ONLY. No own writes after this final lease.','status_scope':'ACCEPTED_WITH_EXPLICIT_READER_DEBT at exact INT65; full Exposition/PURIFIED/remoteCI/main/live/wholepaper/Goal FALSE; ambient/global66 uncredited.','canonical_Git_ledger_Lean_source_math_writes':False,'VERIFIED_transition':False};print(line,end='',flush=True);write('lease.final.json',lease)
def postclose():
 l=read(O/'lease.final.json');assert l['status']=='CLOSED_LAST'
 for x in l['all_owned_except_this_final_lease']:equalpin(x)
 actual={p.relative_to(O).as_posix() for p in O.rglob('*') if p.is_file()};expected={pathlib.Path(x['path']).relative_to(O).as_posix() for x in l['all_owned_except_this_final_lease']}|{'lease.final.json'};assert actual==expected and len(actual)==l['final_owned_file_count'];h,p=basic();assert h==l['whole_logical_run_sha256'];last=(O/'lease.final.json').stat().st_mtime_ns;assert all(q.stat().st_mtime_ns<=last for q in O.rglob('*') if q.is_file());print(json.dumps({'status':'READ_ONLY_POSTCLOSE_PASS','actual_postclose_pid':os.getpid(),'checked_commit':C,'owned_files':len(actual),'whole_logical_run_sha256':h,'complete_named_RAW_review_sha256':p['raw_sha256'],'lease':pin(O/'lease.final.json'),'actual_finalizer_pid':l['actual_finalizer_pid'],'actual_readback_pid':l['actual_readback_pid'],'actual_close_pid':l['actual_close_pid'],'writes':0}),flush=True)
if __name__=='__main__':
 mode=sys.argv[1]
 try:globals()[mode]()
 except Exception as e:
  if mode!='postclose' and not (O/'lease.final.json').exists():write(mode+'.closure.failure.json',{'status':'FAIL','actual_pid':os.getpid(),'exception':repr(e),'traceback':traceback.format_exc(),'utc':now()})
  raise
