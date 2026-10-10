import json,hashlib,os,time,datetime,subprocess,sys,ctypes
from pathlib import Path
B=Path('E:/Samplinglib/runs/20261007-companion-priority/pbps-macro-range-preproof-review58')
def h(b):return hashlib.sha256(b).hexdigest()
def rec(p):
    b=Path(p).read_bytes();l=b.replace(b'\r\n',b'\n');return dict(path=str(p).replace('\\','/'),bytes=len(b),raw_sha256=h(b),lf_bytes=len(l),lf_sha256=h(l))
def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def write(n,o):
    o.pop('content_self_sha256',None);o['content_self_sha256']=h(json.dumps(o,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode());(B/n).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def stamp():return datetime.datetime.now(datetime.timezone.utc).isoformat()
start=time.monotonic()
ps=load(B/'process.status.json');ps['native_process_receipts'].append(dict(chunk='715dfa',process='author_review.py',actual_exit_code=0,pid=40612));write('process.status.json',ps)
r=load(B/'reviewer.run.json');r['process_status']=rec(B/'process.status.json');r['closure_wrapper_pid']=os.getpid();r['preclose_utc']=stamp();write('reviewer.run.json',r)
artifacts=[rec(p) for p in sorted(B.rglob('*')) if p.is_file() and p.name not in ['output.manifest.json','validator.json','complete.json','lease.json','validator.foreground.stdout.txt','validator.foreground.stderr.txt']]
write('output.manifest.json',dict(actor='/root/statement_topology58',artifacts=artifacts,excluded=['output.manifest.json','validator.json','complete.json','lease.json','validator.foreground.stdout.txt','validator.foreground.stderr.txt'],reason='No recursive hashes; final closure separately binds validator/run/output manifest.'))
env=dict(os.environ);env['PYTHONIOENCODING']='utf-8'
p=subprocess.Popen([sys.executable,str(B/'validate_run.py')],stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=env);stdout,stderr=p.communicate();assert p.returncode==0,stderr.decode('utf-8',errors='replace')
(B/'validator.foreground.stdout.txt').write_bytes(stdout);(B/'validator.foreground.stderr.txt').write_bytes(stderr)
v=load(B/'validator.json')
write('complete.json',dict(actor='/root/statement_topology58',status='INDEPENDENT_SCOPED_STATEMENT_AND_TOPOLOGY_REVIEW_CLOSED',statement_verdict='ACCEPTED_WITH_EXPLICIT_SETTING_EXTENSION',topology_verdict='ACCEPTED_SCOPED',blocking_repairs=[],run=rec(B/'reviewer.run.json'),statement_review=rec(B/'statement-review.json'),topology_review=rec(B/'topology-review.json'),output_manifest=rec(B/'output.manifest.json'),validator=rec(B/'validator.json'),validator_actual_exit_code=p.returncode,compiler='NOT_STARTED_CLOSED',formal_admission=False))
resource=dict(wrapper_pid=os.getpid(),validator_pid=p.pid,validator_waited=True,validator_actual_exit_code=p.returncode,wall_seconds=time.monotonic()-start,cpu_user_seconds=os.times().user,cpu_system_seconds=os.times().system,validator_resource=v['resource'])
class IO(ctypes.Structure):_fields_=[(n,ctypes.c_ulonglong) for n in ['ReadOperationCount','WriteOperationCount','OtherOperationCount','ReadTransferCount','WriteTransferCount','OtherTransferCount']]
kernel=ctypes.WinDLL('kernel32',use_last_error=True);kernel.GetCurrentProcess.restype=ctypes.c_void_p;kernel.GetProcessIoCounters.argtypes=[ctypes.c_void_p,ctypes.POINTER(IO)];io=IO();ok=kernel.GetProcessIoCounters(kernel.GetCurrentProcess(),ctypes.byref(io));resource['native_io_query_success']=bool(ok)
if ok:resource['native_io']={n:getattr(io,n) for n,_ in IO._fields_}
print(json.dumps(dict(status='CLOSED_LAST_FOREGROUND',pid=os.getpid(),validator_pid=p.pid,validator_actual_exit_code=p.returncode,run=rec(B/'reviewer.run.json'),complete=rec(B/'complete.json'),resource=resource)))
# This is deliberately the last filesystem operation; actual wrapper exit is observed by exec.
write('lease.json',dict(actor='/root/statement_topology58',status='CLOSED',compiler='NOT_STARTED_CLOSED',python='CLOSED_LAST_FOREGROUND',foreground_wrapper_pid=os.getpid(),validator_actual_exit_code=p.returncode,validator_waited_and_completed=True,run=rec(B/'reviewer.run.json'),complete=rec(B/'complete.json'),outputs=rec(B/'output.manifest.json'),resource=resource,closed_utc=stamp(),last_filesystem_operation=True,formal_admission=False))
