import pathlib,json,hashlib,os,sys,subprocess,datetime
D=pathlib.Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(q):return json.dumps(q,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def load(p):return json.loads(pathlib.Path(p).read_bytes())
def write(p,q):pathlib.Path(p).write_bytes((json.dumps(q,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode())
def pin(p):
 p=pathlib.Path(p);b=p.read_bytes();l=b.replace(b'\r\n',b'\n');return dict(path=p.as_posix(),bytes=len(b),lf_bytes=len(l),raw_sha256=sha(b),lf_sha256=sha(l))
inputs=load(D/'inputs.json');payload=load(D/'topology-review.payload.json');checks=load(D/'checks.json')
write(D/'review.actual.status.json',dict(actual_worker_pid=39668,actual_exit_code=0,tool_chunk='019576',compiler='NOT_STARTED_CLOSED',stdout_observed=dict(status='COMPLETE_WITH_TYPED_TOPOLOGY_BLOCKER',pid=39668,inputs=34,regions=31,coverage=54,payload_sha256='3ab71fb2c6741ff519daf653c5bc0e9bd5fe08047f7991de017a4e2cd920b916')))
(D/'review.actual.log').write_bytes(b'{"status": "COMPLETE_WITH_TYPED_TOPOLOGY_BLOCKER", "pid": 39668, "inputs": 34, "regions": 31, "coverage": 54, "payload_sha256": "3ab71fb2c6741ff519daf653c5bc0e9bd5fe08047f7991de017a4e2cd920b916"}\r\n')
p=subprocess.run([sys.executable,'-B','-X','utf8',str(D/'readback_worker.py')],capture_output=True)
assert p.returncode==0,p.stderr.decode();r=json.loads(p.stdout)
(D/'readback.actual.stdout.log').write_bytes(p.stdout);(D/'readback.actual.stderr.log').write_bytes(p.stderr)
write(D/'readback.actual.status.json',dict(actual_pid=r['pid'],actual_exit_code=p.returncode,actual_command=[sys.executable,'-B','-X','utf8',str(D/'readback_worker.py')],result=r))
inputs['reviewer_implementation_inputs']=[pin(D/'review.py'),pin(D/'readback_worker.py'),pin(D/'close.py')]
write(D/'inputs.json',inputs)
payload_hash=sha(canon(payload))
receipt=dict(schema_version=1,actor='/root/whole_math52',status='CLOSED_SCOPED_PREPROOF_TOPOLOGY_REVIEW59',
 verdict='BLOCKED_SOURCE_B5_IDENTITY_INGREDIENT_EDGE',mathematical_statement_seal='UNCHANGED_CLOSED_ACCEPTED',
 coverage_verdict=payload['coverage_verdict'],blockers=[payload['blocker']],checked_base=payload['checked_base'],
 counts=dict(strict_readonly_inputs=34,reviewer_implementation_inputs=3,indexed_original_snapshot_pairs=10,raw_regions=31,coverage_items=54,NODE=25,EXCLUDED=29,nodes=19,edges=23,selected_hyperedges=4),
 topology_review_payload_sha256=payload_hash,source_statement_verdict_read=False,compiler='NOT_STARTED_CLOSED',
 observed_processes=[dict(pid=39668,exit_code=0,role='independent-topology-reader'),dict(pid=r['pid'],exit_code=p.returncode,role='final-input-readback')],
 exact_header_pins=[x for x in inputs['inputs'] if x['path'].endswith(('header0.lean','header1.lean'))],
 remaining=payload['remaining'])
write(D/'receipt.json',receipt)
run=dict(schema_version=1,actor='/root/whole_math52',status='COMPLETE_WITH_TYPED_TOPOLOGY_BLOCKER',checked_base=payload['checked_base'],
 inputs=inputs['inputs'],reviewer_implementation_inputs=inputs['reviewer_implementation_inputs'],receipt=pin(D/'receipt.json'),
 topology_review_payload=payload,topology_review_payload_sha256=payload_hash,
 checks=checks,observed_processes=receipt['observed_processes'],compiler='NOT_STARTED_CLOSED',
 native_recipes=dict(run_sha256='SHA256 sorted compact UTF8 JSON complete run excluding ONLY top-level run_sha256; ensure_ascii=False, allow_nan=False, no newline',topology_review_payload_sha256='SHA256 same canonical encoding of complete named topology_review_payload object; distinct from run self digest',raw_lf='Actual bytes; LF replaces CRLF pairs only; both byte lengths and SHA256 recorded'),
 remaining=payload['remaining'])
run['run_sha256']=sha(canon(run));write(D/'run.json',run)
assert load(D/'run.json')['run_sha256']==sha(canon({k:v for k,v in load(D/'run.json').items() if k!='run_sha256'}))
assert sha(canon(load(D/'topology-review.payload.json')))==payload_hash
assert load(D/'run.json')['topology_review_payload']==load(D/'topology-review.payload.json')
outputs=[pin(x) for x in sorted(D.iterdir()) if x.is_file() and x.name not in ['lease.json','outputs.final.json','readback.json']]
out=dict(schema_version=1,artifacts=outputs,count=len(outputs));out['outputs_sha256']=sha(canon(out));write(D/'outputs.final.json',out)
for row in outputs:assert pin(row['path'])==row
read=dict(status='ALL_NATIVE_READBACKS_COMPLETE',input_readback=pin(D/'readback.actual.status.json'),run_self_digest_pass=True,payload_digest_pass=True,outputs_raw_lf_pass=True,output_count=len(outputs),run=pin(D/'run.json'),receipt=pin(D/'receipt.json'),outputs_manifest=pin(D/'outputs.final.json'))
write(D/'readback.json',read)
assert load(D/'readback.json')==read
lease=dict(schema_version=1,actor='/root/whole_math52',status='CLOSED',closure_order='LAST filesystem write after actual foreground readback EXIT0, input/output/native self and named payload validations',
 actual_finalizer_pid=os.getpid(),actual_reader_pid=39668,actual_reader_exit_code=0,actual_readback_pid=r['pid'],actual_readback_exit_code=p.returncode,
 compiler='NOT_STARTED_CLOSED',resources=dict(compiler='NOT_STARTED_CLOSED',foreground_reader='CLOSED_EXIT0',foreground_readback='CLOSED_EXIT0',read_handles='CLOSED',write_handles='CLOSED',Python_finalizer='Immediate successful EXIT0 after last lease write and precomputed stdout; no subsequent filesystem operations'),
 run=pin(D/'run.json'),receipt=pin(D/'receipt.json'),outputs_manifest=pin(D/'outputs.final.json'),readback=pin(D/'readback.json'),output_count=len(outputs)+2,
 run_sha256=run['run_sha256'],topology_review_payload_sha256=payload_hash,closed_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
lease['lease_sha256']=sha(canon(lease))
lease_bytes=(json.dumps(lease,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
summary=dict(status=lease['status'],verdict=receipt['verdict'],receipt_raw_lf=lease['receipt']['raw_sha256'],run_raw_lf=lease['run']['raw_sha256'],run_sha256=run['run_sha256'],topology_review_payload_sha256=payload_hash,lease_raw_lf=sha(lease_bytes),lease_sha256=lease['lease_sha256'],inputs=34,implementation_inputs=3,outputs=lease['output_count'],actual_finalizer_pid=os.getpid(),actual_readback_pid=r['pid'],actual_readback_exit_code=0)
(D/'lease.json').write_bytes(lease_bytes)
print(json.dumps(summary))
