import json,os,pathlib,sys,traceback
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from math65 import O,BASE,ACTOR,read,write,pin,sha,canonical,inputs_current,now,verify_run
def owned(exclude=()):
    return [pin(p) for p in sorted(O.rglob('*')) if p.is_file() and p.relative_to(O).as_posix() not in exclude]
def check_rows(rows):
    for x in rows:
        p=pathlib.Path(x['path']);assert p.resolve().is_relative_to(O)
        assert pin(p)==x,('owned RAW/LF mismatch',str(p))
def basic():
    r=read(O/'run.json');whole=r['run_sha256'];assert verify_run(O/'run.json')==whole
    payload=pin(O/'mathematical-review.named.raw.json');assert payload==r['complete_named_RAW_mathematical_review_payload']
    assert payload['raw_sha256']!=whole
    check_rows(read(O/'pre-finalizer.manifest.json')['completed_owned_outputs'])
    inputs_current()
    return whole,payload
def finalize():
    inputs_current()
    review=read(O/'mathematical-review.json');checks=read(O/'checks.result.json');focused=read(O/'focused.result.json')
    assert review['mathematical_blockers']==[] and checks['status']=='PASS' and focused['exit_code']==0
    assert checks['all5_literal_BODY_matches'] and focused['all_inputs_RAW_LF_unchanged']
    failures={p.relative_to(O).as_posix():read(p) for p in sorted(O.rglob('*.failure.json'))}
    completed=owned(exclude=('finalizer.stdout.log','finalizer.stderr.log'))
    full={'schema':'COMPLETE_NAMED_RAW_MATHEMATICAL_REVIEW65_v1','designation':'Complete mathematical review payload: all fields retained, no deletions; this exact pretty JSON RAW is separately pinned from the logical run hash.','mathematical_review':review,'mechanical_checks':checks,'fresh_compiler':focused,'input_manifest':read(O/'inputs.manifest.json'),'retained_own_observer_failures':failures,'retained_own_outputs_before_finalizer':completed,'claim_boundary':'PRECOMMIT mathematical review only; source65 decoder/anti-anchored decisions not consumed; no VERIFIED/exact SCI65/aggregate/PURIFIED/full Goal claim.'}
    write('mathematical-review.named.raw.json',full)
    run={'schema':'independent-math65-full-native-logical-run-v1','actor':ACTOR,'actual_finalizer_pid':os.getpid(),'checked_BASE':BASE,'checked_SCI65_commit':None,'phase':'PRECOMMIT_UNCOMMITTED_CANDIDATES','verdict':review['verdict'],'full_logical_review':full,'complete_named_RAW_mathematical_review_payload':pin(O/'mathematical-review.named.raw.json'),'logical_hash_rule':'Canonical UTF8 JSON ensure_ascii=False sort_keys=True separators=(comma,colon); delete ONLY top-level run_sha256. No other field omitted.','retained_negatives_included':True,'all_pre_finalizer_own_output_pins':completed,'future_owned_closure_layers':['pre-finalizer.manifest.json','finalizer.stdout.log','finalizer.stderr.log','finalizer.terminal.json','readback.result.json','readback.stdout.log','readback.stderr.log','readback.terminal.json','closure.result.json','closure.stdout.log','final.manifest.json','lease.final.json'],'closure_binding':'All owned files, including run/payload/helper scripts/negative and terminal/self layers, are bound at CLOSED_LAST by final lease manifest. Lease itself is externally RAW-pinned by read-only postclose; no impossible self-hash.','finalized_utc':now()}
    run['run_sha256']=sha(canonical(run));write('run.json',run)
    outputs=owned(exclude=('finalizer.stdout.log','finalizer.stderr.log'))
    write('pre-finalizer.manifest.json',{'schema':'math65-prefinalizer-complete-output-manifest-v1','completed_owned_outputs':outputs,'explicit_pending_layers':run['future_owned_closure_layers'],'RAW_payload':run['complete_named_RAW_mathematical_review_payload'],'whole_logical_run_sha256':run['run_sha256'],'actual_finalizer_pid':os.getpid(),'all_existing_negative_layers_bound':True})
    print(json.dumps({'status':'FINALIZED','actual_pid':os.getpid(),'whole_logical_run_sha256':run['run_sha256'],'complete_named_RAW_review_sha256':run['complete_named_RAW_mathematical_review_payload']['raw_sha256'],'completed_files':len(outputs)}),flush=True)
def readback():
    whole,payload=basic();f=read(O/'finalizer.terminal.json');assert f['exit_code']==0 and f['terminal_closed']
    write('readback.result.json',{'status':'PASS','actual_readback_pid':os.getpid(),'checked_BASE':BASE,'phase':'PRECOMMIT','whole_logical_run_sha256':whole,'complete_named_RAW_review':payload,'all_prefinalizer_files_RAW_LF_equal':True,'all191_external_inputs_RAW_LF_equal':True,'finalizer_actual_terminal':f,'readback_utc':now(),'lease_still_open_pending_final_close':True})
    print(json.dumps({'status':'READBACK_PASS','actual_pid':os.getpid(),'whole_logical_run_sha256':whole,'complete_named_RAW_review_sha256':payload['raw_sha256']}),flush=True)
def close():
    assert not (O/'lease.final.json').exists()
    whole,payload=basic();f=read(O/'finalizer.terminal.json');b=read(O/'readback.terminal.json')
    assert f['exit_code']==b['exit_code']==0 and f['terminal_closed'] and b['terminal_closed']
    record={'status':'CLOSURE_PREPARED','actual_close_pid':os.getpid(),'actual_parent_pid':os.getppid(),'actual_finalizer_pid':f['actual_worker_pid'],'actual_finalizer_exit_code':f['exit_code'],'actual_readback_pid':b['actual_worker_pid'],'actual_readback_exit_code':b['exit_code'],'checked_BASE':BASE,'phase':'PRECOMMIT','whole_logical_run_sha256':whole,'complete_named_RAW_review_sha256':payload['raw_sha256'],'close_terminal_exit':'Authoritative close EXIT is observed externally by foreground tool after final lease; no post-lease receipt write.','all191_external_input_pins_unchanged':True,'close_utc':now()}
    write('closure.result.json',record)
    line=json.dumps({'status':'CLOSED_LAST_FINAL_WRITE_NEXT','actual_close_pid':os.getpid(),'whole_logical_run_sha256':whole,'complete_named_RAW_review_sha256':payload['raw_sha256']})+'\n'
    (O/'closure.stdout.log').write_bytes(line.encode('utf-8'))
    previous=owned(exclude=('final.manifest.json','lease.final.json'))
    write('final.manifest.json',{'schema':'math65-final-owned-output-manifest-v1','owned_files_except_this_manifest_and_final_lease':previous,'self_layers':['final.manifest.json','lease.final.json'],'self_binding':'Final lease RAW-pins this manifest plus every other owned file; external readonly postclose RAW-pins final lease.','whole_logical_run_sha256':whole,'complete_named_RAW_review':payload,'actual_close_pid':os.getpid(),'actual_finalizer_pid':f['actual_worker_pid'],'actual_readback_pid':b['actual_worker_pid'],'all_owned_negative_and_terminal_outputs_included':True})
    all_files=owned(exclude=('lease.final.json',))
    lease={'schema':'independent-math65-lease-final-v1','status':'CLOSED_LAST','actor':ACTOR,'owned_prefix':O.as_posix(),'phase':'PRECOMMIT','checked_BASE':BASE,'checked_SCI65_commit':None,'closed_utc':now(),'actual_close_pid':os.getpid(),'actual_finalizer_pid':f['actual_worker_pid'],'actual_finalizer_exit_code':0,'actual_readback_pid':b['actual_worker_pid'],'actual_readback_exit_code':0,'close_exit_observation':'External foreground tools only, after this final write','whole_logical_run_sha256':whole,'complete_named_RAW_review_sha256':payload['raw_sha256'],'all_owned_except_this_final_lease':all_files,'final_owned_file_count':len(all_files)+1,'last_owned_write':True,'postclose_policy':'READ_ONLY; no owned receipt/log/helper mutation after this write','canonical_Git_ledger_Lean_writes':False}
    print(line,end='',flush=True)
    write('lease.final.json',lease)
def postclose():
    lease=read(O/'lease.final.json');assert lease['status']=='CLOSED_LAST' and lease['last_owned_write']
    check_rows(lease['all_owned_except_this_final_lease'])
    expected={pathlib.Path(x['path']).relative_to(O).as_posix() for x in lease['all_owned_except_this_final_lease']}|{'lease.final.json'}
    actual={p.relative_to(O).as_posix() for p in O.rglob('*') if p.is_file()}
    assert actual==expected and len(actual)==lease['final_owned_file_count']
    whole,payload=basic();assert whole==lease['whole_logical_run_sha256'] and payload['raw_sha256']==lease['complete_named_RAW_review_sha256']
    final_time=(O/'lease.final.json').stat().st_mtime_ns
    assert all(p.stat().st_mtime_ns<=final_time for p in O.rglob('*') if p.is_file())
    print(json.dumps({'status':'READ_ONLY_POSTCLOSE_PASS','actual_postclose_pid':os.getpid(),'owned_files':len(actual),'whole_logical_run_sha256':whole,'complete_named_RAW_review_sha256':payload['raw_sha256'],'lease':pin(O/'lease.final.json'),'actual_close_pid':lease['actual_close_pid'],'actual_finalizer_pid':lease['actual_finalizer_pid'],'actual_readback_pid':lease['actual_readback_pid'],'writes':0}),flush=True)
if __name__=='__main__':
    mode=sys.argv[1]
    try:globals()[mode]()
    except Exception as e:
        if mode!='postclose' and not (O/'lease.final.json').exists():write(mode+'.closure.failure.json',{'actual_pid':os.getpid(),'exception':repr(e),'traceback':traceback.format_exc(),'status':'FAIL'})
        raise
