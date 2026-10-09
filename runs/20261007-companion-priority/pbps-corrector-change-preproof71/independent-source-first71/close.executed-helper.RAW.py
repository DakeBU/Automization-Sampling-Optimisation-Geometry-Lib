from source71 import *

def files():
 return sorted(p for p in O.rglob('*') if p.is_file())
def verify_inputs():
 stable()
 for q in get('interface.inputs.manifest.json')['inputs']:checkpin(q['original']);checkpin(q['RAW_snapshot']);checkpin(q['LF_snapshot'])
 for q in get('inputs.manifest.json')['inputs']:
  for k in ['RAW_snapshot','LF_snapshot']:
   if k in q:checkpin(q[k])
 primary=PRIMARY.read_bytes()
 for q in get('source.regions.json')['regions']:
  checkpin(q['RAW']);checkpin(q['LF']);assert sha(primary[q['start_byte']:q['end_byte_exclusive']])==q['RAW']['raw_sha256']
 for q in get('source.supplemental-anchors.json')['items']:
  checkpin(q['RAW']);checkpin(q['LF']);a,b=q['source_RAW_range_end_exclusive'];assert sha(primary[a:b])==q['RAW_sha256']
 for q in get('source.math.inventory.json')['items']:
  assert sha(primary[q['start_byte']:q['end_byte_exclusive']])==q['RAW_sha256']
 seal=get('source-first.seal.json')
 for k in ['expectations','formulas','coverage','inputs']:checkpin(seal[k])
 assert get('source.math.inventory.json')['math_count']==255
 assert len(get('source.coverage.json')['items'])==255
 assert get('source.supplemental-anchors.json')['count']==20
 assert get('expectations.terminal.json')['finished_utc']<get('interface.terminal.json')['started_utc']
 assert get('extract.terminal.json')['exit_code']==1 and get('extract-v2.terminal.json')['exit_code']==0
 for n in ['expectations','interface','review']:assert get(n+'.terminal.json')['exit_code']==0
 checkpin(get('decision.json')['named_complete_RAW_payload'])
 assert get('decision.json')['status']=='ACCEPTED_BOUNDED_SOURCE_EXTRACTION_AND_PROSPECTIVE_INTERFACE_MATCH'

def finalize():
 verify_inputs()
 baseline=[dict(relative_path=p.relative_to(O).as_posix(),**pin(p)) for p in files() if p.name not in ['run.json','outputs.manifest.json'] and not p.name.startswith('finalizer.')]
 r=dict(schema='independent-source-first71-native-run-v1',actor=ACTOR,status=get('decision.json')['status'],actual_finalizer_PID=os.getpid(),utc=now(),source_only=True,no_70_BODY_read=True,no_Lean_proof_search=True,no_canonical_Git_ledger_writes=True,named_complete_RAW_payload=pin(O/'named-review.payload.json'),decision=get('decision.json'),input_manifests=dict(source=get('inputs.manifest.json'),interface=get('interface.inputs.manifest.json')),source_first_seal=get('source-first.seal.json'),review_complete_logical_payload=get('named-review.payload.json'),stage_terminals={n:get(n+'.terminal.json') for n in ['extract','extract-v2','expectations','interface','review']},baseline_owned_files=baseline,closure_contract=dict(whole_logical_hash='Canonical UTF8 JSON sort_keys=True ensure_ascii=False separators=(comma,colon), remove ONLY top-level run_sha256.',named_RAW_hash='SHA256 of complete exact named-review.payload.json bytes, separately from logical run and decision RAW.',self_layers='Final outputs.manifest.json binds exact run and all owned pre-lease files except itself; final lease binds every owned file except its self row. Self hashes are verified externally read-only; no impossible recursive self-hash.',last_owned_write='lease.final.json CLOSED_LAST; read-only postclose does not write receipts into closed scope.',foreground_terminal_authority='Actual subprocess PID/exit receipts; runner own exit is external tool terminal. Postclose occurs after final lease and cannot be in its causal past.'))
 r['run_sha256']=logical(r);save('run.json',r)
 print(json.dumps(dict(status='FINALIZED_NATIVE_RUN',actual_PID=os.getpid(),whole_logical_run_sha256=r['run_sha256'],named_complete_RAW=pin(O/'named-review.payload.json'))))

def readback():
 verify_inputs();r=get('run.json');assert r['run_sha256']==logical(r)
 for q in r['baseline_owned_files']:checkpin({k:v for k,v in q.items() if k!='relative_path'})
 save('readback.json',dict(status='READBACK_PASS',actual_PID=os.getpid(),utc=now(),run=pin(O/'run.json'),whole_logical_run_sha256=r['run_sha256'],named_complete_RAW=pin(O/'named-review.payload.json'),source_input_count=3,interface_input_count=2,regions=4,selected_math=255,supplemental_math=20,finite_maps=[],prior_failed_observer_retained=True))
 print(json.dumps(dict(status='READBACK_PASS',actual_PID=os.getpid(),whole_logical_run_sha256=r['run_sha256'])))

def preclose():
 verify_inputs();r=get('run.json');assert r['run_sha256']==logical(r);checkpin(get('readback.json')['run']);assert get('finalizer.terminal.json')['exit_code']==0 and get('readback.terminal.json')['exit_code']==0
 print(json.dumps(dict(status='PRECLOSE_READONLY_PASS',actual_PID=os.getpid(),whole_logical_run_sha256=r['run_sha256'],named_complete_RAW=pin(O/'named-review.payload.json'))))

def postclose():
 assert (O/'lease.final.json').exists();lease=get('lease.final.json');assert lease['status']=='CLOSED_LAST'
 rows=lease['manifest'];assert len(rows)==lease['owned_file_count']-1;actual={p.relative_to(O).as_posix() for p in files()};assert actual=={q['relative_path'] for q in rows}|{'lease.final.json'}
 for q in rows:checkpin({k:v for k,v in q.items() if k!='relative_path'})
 assert lease['manifest_logical_sha256']==sha(json.dumps(rows,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode())
 verify_inputs();r=get('run.json');assert logical(r)==r['run_sha256'];m=get('outputs.manifest.json');assert m['expected_owned_file_count']==len(actual)
 for q in m['files']:checkpin({k:v for k,v in q.items() if k!='relative_path'})
 print(json.dumps(dict(status='POSTCLOSE_READONLY_PASS',actual_postclose_PID=os.getpid(),postclose_owned_writes=0,owned_file_count=len(actual),whole_logical_run_sha256=r['run_sha256'],named_complete_RAW=pin(O/'named-review.payload.json'),input_manifest_RAW=pin(O/'inputs.manifest.json'),interface_manifest_RAW=pin(O/'interface.inputs.manifest.json'),outputs_manifest_RAW=pin(O/'outputs.manifest.json'),closure_manifest_logical_sha256=lease['manifest_logical_sha256'],lease_RAW=pin(O/'lease.final.json'),foreground_terminals={n:dict(worker_PID=get(n+'.terminal.json')['actual_worker_PID'],runner_PID=get(n+'.terminal.json')['actual_runner_PID'],exit_code=get(n+'.terminal.json')['exit_code']) for n in ['expectations','interface','review','finalizer','readback','close']})))

if __name__=='__main__':
 try:globals()[sys.argv[1]]()
 except Exception as e:
  if not(O/'lease.final.json').exists():save((sys.argv[2] if len(sys.argv)>2 else sys.argv[1])+'.failure.json',dict(actual_PID=os.getpid(),utc=now(),error=repr(e),traceback=traceback.format_exc()))
  raise
