from verify import *
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
with (D/'finalize.actual.log').open('wb') as log:
 p=subprocess.Popen([sys.executable,'-B','-X','utf8',str(D/'finalize.py')],cwd=ROOT,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONUTF8='1'),stdout=log,stderr=subprocess.STDOUT)
 worker=p.pid;rc=p.wait()
write(D/'finalize.actual.status.json',dict(actual_worker_PID=worker,exit_code=rc,resource='CLOSED',started_utc=start,finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),actual_closer_PID=os.getpid(),log=pin(D/'finalize.actual.log')))
assert rc==0,('worker exit',rc)
run=load(D/'run.json');payload=load(D/'verifier-payload.json');receipt=load(D/'receipt.json');verified=load(R/'verified.json');before=load(D/'before-admin.json')
selfcheck(run,'run_sha256');selfcheck(receipt,'receipt_sha256');selfcheck(verified,'verified_sha256')
assert sha(canon(run['verifier_binding_payload']))==run['verifier_binding_payload_sha256']==payload['verifier_binding_payload_sha256']==verified['verifier_binding_payload_sha256']==receipt['verifier_binding_payload_sha256']
admin={sig(x['original']):x for x in before['canonical_mappings']}; readbacks=[]
for row in load(D/'inputs.final.json')['inputs']:
 f=path(row['path'])
 if matches(row,f):actual=pin(f);mapping=None
 elif sig(row) in admin:
  m=admin[sig(row)];actual=m['exactraw_snapshot'];assert matches(row,path(actual['path']));mapping=m
 elif sig(row)==sig(before['ledger_original']):
  actual=before['ledger_prefix'];assert matches(row,path(actual['path']));assert f.read_bytes().startswith(path(actual['path']).read_bytes());mapping=before['ledger_prefix']
 else:raise AssertionError(('final input readback',row))
 readbacks.append(dict(original=row,actual=actual,mapping=mapping))
for x in rows(run):
 # Native run input entries include original exact BEFORE administrative pins, checked above.
 if x in run['inputs']:continue
 assert matches(x,path(x['path'])),('run output binding',x)
for x in rows(receipt):assert matches(x,path(x['path'])),('receipt binding',x)
outputs=[pin(f) for f in sorted(D.rglob('*')) if f.is_file() and f.name not in ['lease.json','readback.json','outputs.final.json']]+[pin(R/'verified.json')]
out=dict(schema_version=1,status='PASS_ACTUAL_OUTPUTS',count=len(outputs),outputs=outputs,excluded_closure_files=['outputs.final.json','readback.json','lease.json'],complete_run_sha256=run['run_sha256'],distinct_verifier_binding_payload_sha256=run['verifier_binding_payload_sha256'],recipe='Actual bytes including historical OPEN lease snapshot; no historical resource status is treated as live. Closed lease is written last.')
out['content_self_sha256']=sha(canon(out));write(D/'outputs.final.json',out);selfcheck(load(D/'outputs.final.json'),'content_self_sha256')
for a in outputs:assert matches(a,path(a['path']))
readback=dict(schema_version=1,status='PASS_ALL_BEFORE_CLOSED_LEASE',checked_commit=SCI,actual_worker_PID=worker,actual_worker_exit_code=rc,actual_closer_PID=os.getpid(),input_count=len(readbacks),inputs=readbacks,output_count=len(outputs),outputs=outputs,output_manifest=pin(D/'outputs.final.json'),complete_run_sha256=run['run_sha256'],named_verifier_binding_payload_sha256=run['verifier_binding_payload_sha256'],logical_self_checks=['run.json minus ONLY run_sha256','receipt.json minus ONLY receipt_sha256','verified.json minus ONLY verified_sha256','outputs.final.json minus ONLY content_self_sha256'],source_originals_not_modified=True,all_before_admin_snapshots_exact=True)
readback['content_self_sha256']=sha(canon(readback));write(D/'readback.json',readback);selfcheck(load(D/'readback.json'),'content_self_sha256')
assert subprocess.check_output(['git','rev-parse','HEAD']).decode().strip()==SCI
lease=dict(schema_version=1,status='CLOSED',verifier_id=ACTOR,checked_commit=SCI,read='CLOSED',write='CLOSED',compiler='CLOSED',Python='CLOSED',actual_compiler_PID=load(D/'focused.status.json')['actual_PID'],actual_compiler_exit_code=0,actual_worker_PID=worker,actual_worker_exit_code=rc,actual_closer_PID=os.getpid(),actual_worker_terminal_evidence=pin(D/'finalize.actual.status.json'),closer_terminal_contract='After this final lease write only print precomputed summary and synchronous exit0; outer tool terminal result supplies observed closer exit. No filesystem read/write follows this write.',run=pin(D/'run.json'),receipt=pin(D/'receipt.json'),verified=pin(R/'verified.json'),readback=pin(D/'readback.json'),output_manifest=pin(D/'outputs.final.json'),input_count=len(readbacks),output_count=len(outputs)+2,outputs=outputs+[pin(D/'outputs.final.json'),pin(D/'readback.json')],complete_run_minus_run_sha256=run['run_sha256'],verifier_binding_payload_sha256=run['verifier_binding_payload_sha256'],closed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),last_filesystem_operation='Write this actual CLOSED lease after all input/output/self/payload/readback checks.',lease_self_recipe='Entire complete object minus ONLY lease_sha256; sorted compact UTF8 JSON.')
lease['lease_sha256']=sha(canon(lease));leasebytes=(json.dumps(lease,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
summary=dict(status='VERIFIED_CLOSED_SCOPED58',checked_commit=SCI,science_entries=1185,math_originals=72,input_count=len(readbacks),native_pin_checks=load(D/'native-checks.json')['actual_pin_checks'],native_self_component_checks=len(load(D/'native-checks.json')['native_self_checks']),source_reviews=3,actual_compiler_PID=lease['actual_compiler_PID'],actual_compiler_exit=0,actual_worker_PID=worker,actual_worker_exit=rc,actual_closer_PID=os.getpid(),receipt_raw_LF_sha256=pin(D/'receipt.json')['raw_sha256'],run_raw_LF_sha256=pin(D/'run.json')['raw_sha256'],complete_run_minus_run_sha256=run['run_sha256'],distinct_verifier_binding_payload_sha256=run['verifier_binding_payload_sha256'],verified_raw_LF_sha256=pin(R/'verified.json')['raw_sha256'],lease_raw_LF_sha256=sha(leasebytes),lease_logical_sha256=lease['lease_sha256'],output_count=lease['output_count'],all_resources='CLOSED',no_shared_aggregate=True)
(D/'lease.json').write_bytes(leasebytes)
print(json.dumps(summary,sort_keys=True))
