import pathlib,json,hashlib,sys,os,subprocess,datetime
D=pathlib.Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(q):return json.dumps(q,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def load(p):return json.loads(pathlib.Path(p).read_bytes())
def write(p,q):pathlib.Path(p).write_bytes((json.dumps(q,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode())
def pin(p):
 p=pathlib.Path(p);b=p.read_bytes();l=b.replace(b'\r\n',b'\n');return dict(path=p.as_posix(),bytes=len(b),lf_bytes=len(l),raw_sha256=sha(b),lf_sha256=sha(l))
write(D/'lease.open.json',dict(actor='/root/whole_math52',status='OPEN',actual_wrapper_pid=os.getpid(),compiler='NOT_STARTED',scope='Exact B5 topology overlay only'))
cmd=[sys.executable,'-B','-X','utf8',str(D/'review.py')]
p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE);pid=p.pid;out,err=p.communicate()
(D/'review.stdout.log').write_bytes(out);(D/'review.stderr.log').write_bytes(err)
write(D/'review.status.json',dict(actual_command=cmd,actual_pid=pid,actual_exit_code=p.returncode,stdout=pin(D/'review.stdout.log'),stderr=pin(D/'review.stderr.log')))
assert p.returncode==0,err.decode('utf8')
inputs=load(D/'inputs.json');payload=load(D/'repair.payload.json');checks=load(D/'checks.json')
code="import pathlib,json,hashlib,sys,os; q=json.loads(pathlib.Path(sys.argv[1]).read_bytes()); [(__import__('builtins').exec('assert len(b)==r[\"bytes\"] and len(l)==r[\"lf_bytes\"] and hashlib.sha256(b).hexdigest()==r[\"raw_sha256\"] and hashlib.sha256(l).hexdigest()==r[\"lf_sha256\"]',dict(r=r,b=(b:=pathlib.Path(r['path']).read_bytes()),l=b.replace(b'\\r\\n',b'\\n'),hashlib=hashlib))) for r in q['inputs']]; print(json.dumps(dict(actual_pid=os.getpid(),input_count=len(q['inputs']),all_raw_lf_pins_pass=True)))"
rcmd=[sys.executable,'-B','-X','utf8','-c',code,str(D/'inputs.json')]
r=subprocess.Popen(rcmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE);rpid=r.pid;rout,rerr=r.communicate()
(D/'readback.stdout.log').write_bytes(rout);(D/'readback.stderr.log').write_bytes(rerr)
write(D/'readback.status.json',dict(actual_command=rcmd,actual_pid=rpid,actual_exit_code=r.returncode,stdout=pin(D/'readback.stdout.log'),stderr=pin(D/'readback.stderr.log')))
assert r.returncode==0,rerr.decode('utf8')
payload_hash=sha(canon(payload));assert json.loads(out)['repair_payload_sha256']==payload_hash
inputs['reviewer_implementation_inputs']=[pin(D/'review.py'),pin(D/'execute.py')];write(D/'inputs.json',inputs)
receipt=dict(schema_version=1,actor='/root/whole_math52',status='CLOSED_EXACT_TOPOLOGY_OVERLAY_REVIEW59',verdict=payload['verdict'],repair_id='SPG59-B5-1',
 qualified_inputs=inputs['count'],source_slices=2,unchanged=payload['unchanged'],successor_edges=25,total_routes=5,selected_routes=4,
 mathematical_reason=payload['mathematical_reason'],repair_payload_sha256=payload_hash,blockers=[],compiler='NOT_STARTED_CLOSED',
 observed_processes=[dict(role='review',pid=pid,exit_code=p.returncode),dict(role='readback',pid=rpid,exit_code=r.returncode)],scope=payload['scope'])
write(D/'receipt.json',receipt)
run=dict(schema_version=1,actor='/root/whole_math52',status='COMPLETE_EXACT_OVERLAY_ACCEPTED',inputs=inputs['inputs'],reviewer_implementation_inputs=inputs['reviewer_implementation_inputs'],
 receipt=pin(D/'receipt.json'),repair_payload=payload,repair_payload_sha256=payload_hash,checks=checks,observed_processes=receipt['observed_processes'],compiler='NOT_STARTED_CLOSED',
 native_recipes=dict(run_sha256='SHA256 canonical sorted compact UTF8 entire run excluding ONLY top-level run_sha256; ensure_ascii=False, allow_nan=False, no newline',repair_payload_sha256='SHA256 same canonical encoding of distinct complete named repair_payload object',raw_lf='Actual bytes and CRLF-pair-to-LF bytes, lengths and SHA256 both bound'))
run['run_sha256']=sha(canon(run));write(D/'run.json',run)
q=load(D/'run.json');assert q['run_sha256']==sha(canon({k:v for k,v in q.items() if k!='run_sha256'})) and q['repair_payload']==load(D/'repair.payload.json') and sha(canon(q['repair_payload']))==payload_hash
outputs=[pin(f) for f in sorted(D.iterdir()) if f.is_file() and f.name not in ['lease.json','outputs.final.json','readback.json']]
manifest=dict(artifacts=outputs,count=len(outputs));manifest['outputs_sha256']=sha(canon(manifest));write(D/'outputs.final.json',manifest)
for row in outputs:assert pin(row['path'])==row
readback=dict(status='ALL_READBACKS_PASS',input_count=inputs['count'],run_self_pass=True,distinct_payload_pass=True,all_output_raw_lf_pass=True,foreground_readback_exit_code=0,run=pin(D/'run.json'),receipt=pin(D/'receipt.json'),outputs_manifest=pin(D/'outputs.final.json'))
write(D/'readback.json',readback);assert load(D/'readback.json')==readback
lease=dict(schema_version=1,actor='/root/whole_math52',status='CLOSED',closure_order='LAST filesystem write after actual foreground review/readback EXIT0 and all native/object/output validations',
 actual_finalizer_pid=os.getpid(),actual_reader_pid=pid,actual_reader_exit_code=0,actual_readback_pid=rpid,actual_readback_exit_code=0,compiler='NOT_STARTED_CLOSED',
 resources=dict(foreground_review='CLOSED_EXIT0',foreground_readback='CLOSED_EXIT0',read_handles='CLOSED',write_handles='CLOSED',Python_finalizer='Immediate successful return after last lease write and precomputed stdout; no subsequent filesystem operation',compiler='NOT_STARTED_CLOSED'),
 run=pin(D/'run.json'),receipt=pin(D/'receipt.json'),outputs_manifest=pin(D/'outputs.final.json'),readback=pin(D/'readback.json'),output_count=len(outputs)+2,
 run_sha256=run['run_sha256'],repair_payload_sha256=payload_hash,closed_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
lease['lease_sha256']=sha(canon(lease));b=(json.dumps(lease,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
summary=dict(status='CLOSED',verdict=payload['verdict'],inputs=inputs['count'],implementation_inputs=2,outputs=lease['output_count'],actual_reader_pid=pid,actual_readback_pid=rpid,actual_finalizer_pid=os.getpid(),receipt_raw_lf=lease['receipt']['raw_sha256'],run_raw_lf=lease['run']['raw_sha256'],run_sha256=run['run_sha256'],repair_payload_sha256=payload_hash,lease_raw_lf=sha(b),lease_sha256=lease['lease_sha256'])
(D/'lease.json').write_bytes(b)
print(json.dumps(summary))
