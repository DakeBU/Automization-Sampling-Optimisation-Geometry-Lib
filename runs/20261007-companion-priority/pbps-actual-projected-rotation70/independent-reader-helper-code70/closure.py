from review import *

def validate():
 final_stable();d=get('decision.json');assert d['accepted'] and not d['full_browser_integration'] and not d['SAU_VERIFIED'];check(d['named_complete_RAW_payload'])
 assert get('negative.terminal.json')['exit_code']==1 and 'playwright' in get('negative.failure.json')['error']
 for n in ['freeze','negative-v2','renderer-negative','freeze-final','final-checks','multiplicity','decision']:
  t=get(n+'.terminal.json');assert t['exit_code']==0 and t['terminal_closed'];check(t['executed_helper_RAW'])
 for name in ['focused31.receipt.json','syntax.receipt.json']:
  r=get(name);assert r['exit_code']==0 and r['terminal_closed']
 for k in ['stdout','stderr']:check(get('focused31.receipt.json')[k])
 for q in get('syntax.receipt.json')['scripts']:check(q['input']);check(q['owned_pyc'])
 for m in ['fixture-results-final-v3.json','fixture-results-intermediate-v2.json','multiplicity.results.json']:
  r=get(m)
  if m=='fixture-results-intermediate-v2.json':assert r['target_script']['raw_sha256']==read(C/'V3.open-count-repair.json')['before_RAW_sha256']
  else:check(r['target_script'])
  for q in r['cases']:check(q['fixture'])
 for q in get('renderer-final.results.json')['cases']:check(q['output'])
 check(get('renderer-final.results.json')['nested_helper'])
def finalize():
 validate();rows=[dict(review_phase=phase,**q) for phase,n in [('V1_historical','inputs-v1.manifest.json'),('final_current','inputs-final.manifest.json')] for q in get(n)['inputs']]
 save('inputs.manifest.json',dict(input_count=len(rows),distinct_original_path_count=len({q['original']['path'] for q in rows}),inputs=rows,LF_recipe=get('inputs-v1.manifest.json')['LF_recipe'],finite_history_map=pin(O/'finite-historical-maps.json'),qualification='Original19 V1 rows are exact frozen historical bytes. Exactly2 script rows map through the named root repairs to final scripts; all17 other originals remain equal. Final10 rows current. No arbitrary fallback/exclusion.'))
 baseline=[dict(relative_path=p.relative_to(O).as_posix(),**pin(p)) for p in files() if p.name!='run.json' and not p.name.startswith('finalizer.')]
 r=dict(schema='independent-reader-helper-code70-native-run-v1',actor=ACTOR,status=get('decision.json')['status'],actual_finalizer_PID=os.getpid(),utc=now(),complete_named_review=get('named-review.payload.json'),named_complete_RAW_payload=pin(O/'named-review.payload.json'),decision=get('decision.json'),inputs=get('inputs.manifest.json'),baseline_owned_files=baseline,stage_terminals={n:get(n+'.terminal.json') for n in ['freeze','negative','negative-v2','renderer-negative','freeze-final','final-checks','multiplicity','decision']},hash_contract='Canonical UTF8 logical JSON removes ONLY top-level run_sha256. Complete named RAW independently hashes full exact payload bytes.',closure_contract='Every owned input/helper/negative/terminal/self layer bound by final manifest and last CLOSED_LAST lease; lease self RAW read externally; no owned write after lease.')
 r['run_sha256']=logical(r);save('run.json',r);print(json.dumps(dict(status='FINALIZED',actual_PID=os.getpid(),whole_logical_run_sha256=r['run_sha256'],input_count=len(rows))))
def readback():
 validate();r=get('run.json');assert logical(r)==r['run_sha256']
 for q in r['baseline_owned_files']:check({k:v for k,v in q.items() if k!='relative_path'})
 save('readback.json',dict(status='PASS',actual_PID=os.getpid(),utc=now(),run=pin(O/'run.json'),whole_logical_run_sha256=r['run_sha256'],named_complete_RAW_payload=pin(O/'named-review.payload.json'),inputs_manifest_RAW=pin(O/'inputs.manifest.json')));print(json.dumps(dict(status='READBACK_PASS',actual_PID=os.getpid())))
def preclose():
 validate();r=get('run.json');assert logical(r)==r['run_sha256'];check(get('readback.json')['run'])
 for n in ['finalizer','readback']:assert get(n+'.terminal.json')['exit_code']==0 and get(n+'.terminal.json')['terminal_closed']
 print(json.dumps(dict(status='PRECLOSE_PASS',actual_PID=os.getpid())))
def postclose():
 l=get('lease.final.json');assert l['status']=='CLOSED_LAST';rows=l['manifest'];assert len(rows)==l['owned_file_count']-1;assert {p.relative_to(O).as_posix() for p in files()}=={q['relative_path'] for q in rows}|{'lease.final.json'}
 for q in rows:check({k:v for k,v in q.items() if k!='relative_path'})
 assert sha(json.dumps(rows,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode())==l['manifest_logical_sha256'];validate();r=get('run.json');assert logical(r)==r['run_sha256'];m=get('outputs.manifest.json');assert m['expected_owned_file_count']==l['owned_file_count']
 for q in m['files']:check({k:v for k,v in q.items() if k!='relative_path'})
 print(json.dumps(dict(status='POSTCLOSE_READONLY_PASS',actual_postclose_PID=os.getpid(),postclose_owned_writes=0,owned_file_count=l['owned_file_count'],whole_logical_run_sha256=r['run_sha256'],named_complete_RAW_payload=pin(O/'named-review.payload.json'),inputs_manifest_RAW=pin(O/'inputs.manifest.json'),outputs_manifest_RAW=pin(O/'outputs.manifest.json'),closure_manifest_logical_sha256=l['manifest_logical_sha256'],lease_RAW=pin(O/'lease.final.json'),foreground_terminals={n:dict(worker_PID=get(n+'.terminal.json')['actual_worker_PID'],runner_PID=get(n+'.terminal.json')['actual_runner_PID'],exit_code=get(n+'.terminal.json')['exit_code']) for n in ['freeze','negative','negative-v2','renderer-negative','freeze-final','final-checks','multiplicity','decision','finalizer','readback','close']})))
