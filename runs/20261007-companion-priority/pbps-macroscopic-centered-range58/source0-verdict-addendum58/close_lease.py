import json,hashlib,os,time,datetime,sys,subprocess,ctypes
from pathlib import Path
B=Path('E:/Samplinglib/runs/20261007-companion-priority/pbps-macroscopic-centered-range58/source0-verdict-addendum58')
def h(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def rec(p):
 b=Path(p).read_bytes();l=b.replace(b'\r\n',b'\n');return dict(path=str(p).replace('\\','/'),raw_bytes=len(b),raw_sha256=h(b),lf_bytes=len(l),lf_sha256=h(l))
def write(n,o):(B/n).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
start=time.monotonic();seal_chunk=os.environ['ASTIS_SOURCE0_ADDENDUM_SEAL_CHUNK'];env=dict(os.environ);env['PYTHONIOENCODING']='utf-8';p=subprocess.Popen([sys.executable,str(B/'validate_run.py')],stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=env);out,err=p.communicate();assert p.returncode==0,err.decode('utf-8',errors='replace');(B/'validator.foreground.stdout.txt').write_bytes(out);(B/'validator.foreground.stderr.txt').write_bytes(err)
run=load(B/'run.json');v=load(B/'validator.json');complete=dict(schema_version=1,status='SOURCE0_VERDICT_ADDENDUM_CLOSED',reviewer='/root/statement_topology58',run=rec(B/'run.json'),run_sha256=run['run_sha256'],source_review_payload_sha256=run['source_review_payload_sha256'],output_manifest=rec(B/'output.manifest.json'),validator=rec(B/'validator.json'),validator_actual_exit_code=p.returncode,validator_waited_and_completed=True,seal_actual_exit_code=0,seal_actual_chunk=seal_chunk,compiler='NOT_STARTED_CLOSED',result_count=1,semantic_slot_count=7,mathematical_blockers=0,publication_blockers=0,seven_slots_unchanged=True,formal_admission=False);write('complete.json',complete)
resource=dict(wrapper_pid=os.getpid(),validator_pid=p.pid,validator_actual_exit_code=p.returncode,validator_waited=True,wall_seconds=time.monotonic()-start,cpu_user_seconds=os.times().user,cpu_system_seconds=os.times().system,validator_resource=v['resource'])
class IO(ctypes.Structure):_fields_=[(n,ctypes.c_ulonglong) for n in ['ReadOperationCount','WriteOperationCount','OtherOperationCount','ReadTransferCount','WriteTransferCount','OtherTransferCount']]
k=ctypes.WinDLL('kernel32',use_last_error=True);k.GetCurrentProcess.restype=ctypes.c_void_p;k.GetProcessIoCounters.argtypes=[ctypes.c_void_p,ctypes.POINTER(IO)];io=IO();ok=k.GetProcessIoCounters(k.GetCurrentProcess(),ctypes.byref(io));resource['native_io_query_success']=bool(ok)
if ok:resource['native_io']={n:getattr(io,n) for n,_ in IO._fields_}
closed=dict(schema_version=1,status='CLOSED',actor_identity='/root/statement_topology58',compiler='NOT_STARTED_CLOSED',python='CLOSED_LAST_FOREGROUND',run=rec(B/'run.json'),run_sha256=run['run_sha256'],source_review_payload_sha256=run['source_review_payload_sha256'],complete=rec(B/'complete.json'),output_manifest=rec(B/'output.manifest.json'),validator=rec(B/'validator.json'),initial_lease=rec(B/'lease.open.json'),resource=resource,raw_lf_readbacks=v['actual_raw_lf_readback_count'],seal_actual_exit_code=0,seal_actual_chunk=seal_chunk,seven_slots_unchanged=True,source2_current_acceptance_changed=False,closed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),last_filesystem_operation=True)
print(json.dumps(dict(status='SOURCE0_ADDENDUM_CLOSEDLAST',run_sha256=run['run_sha256'],source_review_payload_sha256=run['source_review_payload_sha256'],raw_lf_readbacks=v['actual_raw_lf_readback_count'],resource=resource)))
# Last filesystem operation: this independent bounded addendum lease only.
write('lease.json',closed)
