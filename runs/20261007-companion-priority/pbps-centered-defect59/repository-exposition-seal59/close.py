import pathlib,json,hashlib,subprocess,os,sys,datetime
D=pathlib.Path('E:/Samplinglib/runs/20261007-companion-priority/pbps-centered-defect59/repository-exposition-seal59');ROOT=pathlib.Path('E:/Samplinglib')
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(q):return json.dumps(q,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def load(p):return json.loads(pathlib.Path(p).read_bytes())
def write(p,q):pathlib.Path(p).write_bytes((json.dumps(q,ensure_ascii=False,indent=2)+'\n').encode())
def pin(p):
 b=p.read_bytes();l=b.replace(b'\r\n',b'\n');return dict(path=p.as_posix(),bytes=len(b),lf_bytes=len(l),raw_sha256=sha(b),lf_sha256=sha(l))
processes=[]
for name in ['finalize','readback']:
 command=[sys.executable,'-B','-X','utf8',str(D/(name+'.py'))]
 with (D/(name+'.stdout.log')).open('wb') as out,(D/(name+'.stderr.log')).open('wb') as err:
  p=subprocess.Popen(command,cwd=ROOT,stdout=out,stderr=err);pid=p.pid;code=p.wait()
 status=dict(command=command,actual_pid=pid,exit_code=code,terminal_closed=True,stdout=pin(D/(name+'.stdout.log')),stderr=pin(D/(name+'.stderr.log')))
 write(D/(name+'.status.json'),status);assert code==0,status;processes.append(status)
artifacts=[pin(p) for p in sorted(D.iterdir()) if p.is_file() and p.name not in ['lease.json','outputs.final.json']]
outputs=dict(artifacts=artifacts,count=len(artifacts),schema='All actual owned output bytes before CLOSEDLAST lease; outputs.final self separate',hash_recipe='Complete sorted compact object minus ONLY outputs_sha256')
outputs['outputs_sha256']=sha(canon(outputs));write(D/'outputs.final.json',outputs)
for row in artifacts:assert pin(pathlib.Path(row['path']))==row
q=load(D/'outputs.final.json');assert sha(canon({k:v for k,v in q.items() if k!='outputs_sha256'}))==q['outputs_sha256']
run=load(D/'run.json');assert sha(canon({k:v for k,v in run.items() if k!='run_sha256'}))==run['run_sha256']
lease=dict(status='CLOSEDLAST',actor='/root/whole_math52/repository-exposition59',actual_wrapper_pid=os.getpid(),actual_wrapper_exit_evidence='Final stdout after all checks; parent tool terminal must independently report EXIT0',foreground_child_processes=processes,compiler='NOT_STARTED_CLOSED',browser='NOT_STARTED_CLOSED',HTTP='NOT_STARTED_CLOSED',Python_children='ACTUAL_EXIT0_CLOSED',read_resources='CLOSED',write_resources='CLOSED_AFTER_THIS_FINAL_FILE_WRITE',checked_science_commit=run['checked_science_commit'],checked_integration_commit=run['checked_integration_commit'],run=pin(D/'run.json'),receipt=pin(D/'receipt.json'),payload=pin(D/'payload.json'),outputs=pin(D/'outputs.final.json'),readback=pin(D/'readback.json'),run_sha256=run['run_sha256'],named_repository_exposition_payload_sha256=run['named_repository_exposition_payload_sha256'],output_count=len(artifacts),closed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),lease_hash_recipe='Sorted compact UTF8 complete lease excluding ONLY lease_sha256')
lease['lease_sha256']=sha(canon(lease));write(D/'lease.json',lease)
print(json.dumps(dict(status='CLOSEDLAST',actual_wrapper_pid=os.getpid(),run_sha256=run['run_sha256'],payload_sha256=run['named_repository_exposition_payload_sha256'],receipt=pin(D/'receipt.json'),run=pin(D/'run.json'),lease=pin(D/'lease.json'),lease_sha256=lease['lease_sha256'],input_count=load(D/'input.manifest.json')['count'],output_count=len(artifacts),child_pids=[x['actual_pid'] for x in processes])),flush=True)
