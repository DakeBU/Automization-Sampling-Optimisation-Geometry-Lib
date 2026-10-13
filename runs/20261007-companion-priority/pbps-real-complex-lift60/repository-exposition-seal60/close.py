import pathlib,json,hashlib,subprocess,os,sys,datetime
D=pathlib.Path('E:/Samplinglib/runs/20261007-companion-priority/pbps-real-complex-lift60/repository-exposition-seal60')
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(q):return json.dumps(q,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def pin(p):
 p=pathlib.Path(p);b=p.read_bytes();l=b.replace(b'\r\n',b'\n');return dict(path=p.as_posix(),bytes=len(b),lf_bytes=len(l),raw_sha256=sha(b),lf_sha256=sha(l))
def load(p):return json.loads(pathlib.Path(p).read_bytes())
def write(p,q):pathlib.Path(p).write_bytes((json.dumps(q,ensure_ascii=False,indent=2)+'\n').encode())
assert not (D/'lease.json').exists()
# Finite cycle exclusions, individually named; readback/lease bind these separately.
excluded={'outputs.final.json','readback.json','readback.stdout.log','readback.stderr.log','readback.status.json','lease.json'}
files=sorted(p for p in D.rglob('*') if p.is_file() and p.relative_to(D).as_posix() not in excluded)
outputs=dict(artifacts=[pin(p) for p in files],count=len(files),excluded_cyclic_paths=sorted(excluded),hash_recipe='Complete sorted compact UTF8 output manifest excluding ONLY outputs_sha256')
outputs['outputs_sha256']=sha(canon(outputs));write(D/'outputs.final.json',outputs)
with (D/'readback.stdout.log').open('wb') as out,(D/'readback.stderr.log').open('wb') as err:
 child=subprocess.Popen([sys.executable,'-B','-X','utf8',str(D/'readback.py')],stdout=out,stderr=err);pid=child.pid;code=child.wait()
status=dict(actual_PID=pid,exit_code=code,terminal_closed=True,foreground=True,stdout=pin(D/'readback.stdout.log'),stderr=pin(D/'readback.stderr.log'));write(D/'readback.status.json',status)
assert code==0,(D/'readback.stderr.log').read_text()
for row in outputs['artifacts']:assert pin(row['path'])==row
run=load(D/'run.json');assert sha(canon({k:v for k,v in run.items() if k!='run_sha256'}))==run['run_sha256']
lease=dict(schema='native-scoped-repository-exposition60-lease-v1',status='CLOSEDLAST',actor=run['actor'],checked_science_commit=run['checked_science_commit'],checked_integration_commit=run['checked_integration_commit'],actual_closure_writer_PID=os.getpid(),closure_writer_scope='Foreground final lease writer; this lease is its LAST filesystem write, then exit. External tool terminal records actual exit.',actual_reader=load(D/'reader.2.status.json'),actual_finalizer=load(D/'finalizer.status.json'),actual_prepare_readback={'actual_PID':33824,'exit_code':0,'terminal_tool_chunk':'00abff'},actual_readback=status,compiler='NOT_STARTED_CLOSED',browser='NOT_STARTED_CLOSED',Python_children='All spawned children waited and EXIT0 CLOSED; original two schema-negative readers EXIT1 CLOSED preserved',read_resources='CLOSED after final byte/self/payload/readback validation',write_resources='This final lease write then close; no later own artifact writes authorized',run=pin(D/'run.json'),receipt=pin(D/'receipt.json'),payload=pin(D/'payload.json'),outputs=pin(D/'outputs.final.json'),readback=pin(D/'readback.json'),whole_run_sha256=run['run_sha256'],named_repository_exposition_payload_sha256=run['named_repository_exposition_payload_sha256'],closed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),lease_hash_recipe='Complete sorted compact UTF8 entire lease excluding ONLY lease_sha256')
lease['lease_sha256']=sha(canon(lease))
write(D/'lease.json',lease)
print(json.dumps(dict(status='CLOSEDLAST',actual_closure_writer_PID=os.getpid(),actual_readback_PID=pid,readback_exit_code=code,run=pin(D/'run.json'),receipt=pin(D/'receipt.json'),lease=pin(D/'lease.json'),whole_run_sha256=run['run_sha256'],named_repository_exposition_payload_sha256=run['named_repository_exposition_payload_sha256'],output_count=outputs['count'])),flush=True)
