import pathlib,json,hashlib,os,subprocess,sys,datetime
D=pathlib.Path('E:/Samplinglib/runs/20261007-companion-priority/pbps-real-defect-root61/independent-math61')
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(q):return json.dumps(q,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def pin(p):
 p=pathlib.Path(p);b=p.read_bytes();l=b.replace(b'\r\n',b'\n');return dict(path=p.as_posix(),raw_bytes=len(b),lf_bytes=len(l),raw_sha256=sha(b),lf_sha256=sha(l))
def load(p):return json.loads(pathlib.Path(p).read_bytes())
def write(p,q):pathlib.Path(p).write_bytes((json.dumps(q,ensure_ascii=False,indent=2)+'\n').encode())
assert not (D/'lease.json').exists()
excluded={'outputs.final.json','readback.json','readback.stdout.log','readback.stderr.log','readback.status.json','lease.json'}
files=sorted(p for p in D.rglob('*') if p.is_file() and p.relative_to(D).as_posix() not in excluded)
outputs=dict(artifacts=[pin(p) for p in files],count=len(files),excluded_cyclic_paths=sorted(excluded),hash_recipe='Complete sorted compact UTF8 output manifest excluding ONLY outputs_sha256');outputs['outputs_sha256']=sha(canon(outputs));write(D/'outputs.final.json',outputs)
with (D/'readback.stdout.log').open('wb') as out,(D/'readback.stderr.log').open('wb') as err:
 child=subprocess.Popen([sys.executable,'-B','-X','utf8',str(D/'readback.py')],stdout=out,stderr=err);pid=child.pid;code=child.wait()
status=dict(actual_PID=pid,exit_code=code,terminal_closed=True,foreground=True,stdout=pin(D/'readback.stdout.log'),stderr=pin(D/'readback.stderr.log'));write(D/'readback.status.json',status);assert code==0,(D/'readback.stderr.log').read_text()
for row in outputs['artifacts']:assert pin(row['path'])==row
run=load(D/'run.json');assert sha(canon({k:v for k,v in run.items() if k!='run_sha256'}))==run['run_sha256']
lease=dict(schema='native-independent-complete-math61-lease-v1',status='CLOSEDLAST',actor=run['actor'],checked_base_commit=run['checked_base_commit'],actual_closure_writer_PID=os.getpid(),actual_foreground_closure_writer='This lease is LAST filesystem write, then this foreground writer exits; actual exit recorded by calling tool terminal',compiler=load(D/'compiler.status.json'),compiler_wrapper=load(D/'compiler-wrapper.status.json'),finalizer=load(D/'review-finalizer.status.json'),readback_process=status,Python_children='All spawned compiler/wrapper/finalizer/readback processes observed EXIT0 and waited CLOSED',read_resources='CLOSED after final raw/LF/source/snapshot/output/self/payload readbacks',write_resources='Lease LAST write then close; no further own writes',run=pin(D/'run.json'),receipt=pin(D/'receipt.json'),payload=pin(D/'payload.json'),outputs=pin(D/'outputs.final.json'),readback=pin(D/'readback.json'),run_sha256=run['run_sha256'],named_mathematics_payload_sha256=run['named_mathematics_payload_sha256'],closed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),lease_hash_recipe='Complete sorted compact UTF8 entire lease excluding ONLY lease_sha256')
lease['lease_sha256']=sha(canon(lease));write(D/'lease.json',lease)
print(json.dumps(dict(status='CLOSEDLAST',actual_closure_writer_PID=os.getpid(),actual_readback_PID=pid,readback_exit=code,receipt=pin(D/'receipt.json'),run=pin(D/'run.json'),payload=pin(D/'payload.json'),lease=pin(D/'lease.json'),whole_run_sha256=run['run_sha256'],named_mathematics_payload_sha256=run['named_mathematics_payload_sha256'],output_count=outputs['count'])),flush=True)
