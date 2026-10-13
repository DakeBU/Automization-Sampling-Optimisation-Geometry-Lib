from review70 import *
def files():return sorted(p for p in O.rglob('*') if p.is_file())
def verify():validate()
def finalize():
 verify();baseline=[dict(relative_path=p.relative_to(O).as_posix(),**pin(p)) for p in files() if p.name!='run.json' and not p.name.startswith('finalizer.')]
 r=dict(schema='independent-named-literal-math70-native-run-v1',actor=ACTOR,status=get('decision.json')['status'],actual_finalizer_PID=os.getpid(),utc=now(),complete_named_review=get('named-review.payload.json'),named_complete_RAW_payload=pin(O/'named-review.payload.json'),decision=get('decision.json'),inputs=get('inputs.manifest.json'),baseline_owned_files=baseline,stage_terminals={n:get(n+'.terminal.json') for n in ['freeze','review']},hash_contract='Whole logical canonical JSON removes ONLY top-level run_sha256; complete named RAW is independently hashed exact bytes.',closure_contract='All owned pre-lease files and self layers bound by final manifest and lease; final lease self RAW externally read back. CLOSED_LAST is last owned write; postclose is read-only and external terminal evidence.')
 r['run_sha256']=logical(r);save('run.json',r);print(json.dumps(dict(status='FINALIZED',actual_PID=os.getpid(),whole_logical_run_sha256=r['run_sha256'])))
def readback():
 verify();r=get('run.json');assert logical(r)==r['run_sha256']
 for q in r['baseline_owned_files']:checkpin({k:v for k,v in q.items() if k!='relative_path'})
 save('readback.json',dict(status='PASS',actual_PID=os.getpid(),utc=now(),run=pin(O/'run.json'),whole_logical_run_sha256=r['run_sha256'],named_complete_RAW_payload=pin(O/'named-review.payload.json'),input_count=get('inputs.manifest.json')['input_count']));print(json.dumps(dict(status='READBACK_PASS',actual_PID=os.getpid())))
def preclose():
 verify();r=get('run.json');assert logical(r)==r['run_sha256'];checkpin(get('readback.json')['run']);assert get('finalizer.terminal.json')['exit_code']==0 and get('readback.terminal.json')['exit_code']==0;print(json.dumps(dict(status='PRECLOSE_PASS',actual_PID=os.getpid())))
def postclose():
 l=get('lease.final.json');assert l['status']=='CLOSED_LAST';rows=l['manifest'];assert len(rows)==l['owned_file_count']-1;assert {p.relative_to(O).as_posix() for p in files()}=={q['relative_path'] for q in rows}|{'lease.final.json'}
 for q in rows:checkpin({k:v for k,v in q.items() if k!='relative_path'})
 assert sha(json.dumps(rows,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode())==l['manifest_logical_sha256'];verify();r=get('run.json');assert logical(r)==r['run_sha256'];m=get('outputs.manifest.json');assert m['expected_owned_file_count']==l['owned_file_count']
 for q in m['files']:checkpin({k:v for k,v in q.items() if k!='relative_path'})
 print(json.dumps(dict(status='POSTCLOSE_READONLY_PASS',actual_postclose_PID=os.getpid(),postclose_owned_writes=0,owned_file_count=l['owned_file_count'],whole_logical_run_sha256=r['run_sha256'],named_complete_RAW_payload=pin(O/'named-review.payload.json'),inputs_manifest_RAW=pin(O/'inputs.manifest.json'),outputs_manifest_RAW=pin(O/'outputs.manifest.json'),closure_manifest_logical_sha256=l['manifest_logical_sha256'],lease_RAW=pin(O/'lease.final.json'),foreground_terminals={n:dict(worker_PID=get(n+'.terminal.json')['actual_worker_PID'],runner_PID=get(n+'.terminal.json')['actual_runner_PID'],exit_code=get(n+'.terminal.json')['exit_code']) for n in ['freeze','review','finalizer','readback','close']})))
if __name__=='__main__':
 try:globals()[sys.argv[1]]()
 except Exception as e:
  if not(O/'lease.final.json').exists():save((sys.argv[2] if len(sys.argv)>2 else sys.argv[1])+'.failure.json',dict(actual_PID=os.getpid(),utc=now(),error=repr(e),traceback=traceback.format_exc()))
  raise
