import json,hashlib,os,time,subprocess,datetime
from pathlib import Path
B=Path('E:/Samplinglib/runs/20261007-companion-priority/pbps-macroscopic-centered-range58/reader-controls58/independent-review')
def h(b):return hashlib.sha256(b).hexdigest()
def load(n):return json.loads((B/n).read_text(encoding='utf-8'))
def rec(p):
 b=Path(p).read_bytes();l=b.replace(b'\r\n',b'\n');return dict(path=str(p).replace('\\','/'),raw_bytes=len(b),raw_sha256=h(b),lf_bytes=len(l),lf_sha256=h(l))
def write(n,o):(B/n).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
start=time.monotonic()
with (B/'validator.stdout.log').open('wb') as out,(B/'validator.stderr.log').open('wb') as err:
 child=subprocess.Popen([r'C:/Users/admin/AppData/Local/Programs/Python/Python38/python.exe',str(B/'validate.py')],stdout=out,stderr=err,env=dict(os.environ,PYTHONIOENCODING='utf-8'));exitcode=child.wait()
assert exitcode==0,(B/'validator.stderr.log').read_text();run=load('run.json');v=load('validator.json');assert v['resource']['pid']==child.pid
resource=dict(wrapper_pid=os.getpid(),validator_pid=child.pid,validator_actual_exit_code=exitcode,validator_waited=True,wall_seconds=time.monotonic()-start,cpu_user_seconds=os.times().user,cpu_system_seconds=os.times().system,validator_resource=v['resource'])
complete=dict(schema_version=1,status='CLOSED_ACCEPT_SCOPED_READER_CONTROLS_REPAIR',run=rec(B/'run.json'),run_sha256=run['run_sha256'],reader_controls_repair_payload_sha256=run['reader_controls_repair_payload_sha256'],output_manifest=rec(B/'output.manifest.json'),validator=rec(B/'validator.json'),resource=resource,seal_actual_exit_code=0,full_reader_accepted=False,PURIFIED=False)
write('complete.json',complete)
lease=dict(schema_version=1,status='CLOSED',actor='/root/statement_topology58',run=rec(B/'run.json'),run_sha256=run['run_sha256'],reader_controls_repair_payload_sha256=run['reader_controls_repair_payload_sha256'],complete=rec(B/'complete.json'),output_manifest=rec(B/'output.manifest.json'),validator=rec(B/'validator.json'),initial_lease=rec(B/'lease.open.json'),resource=resource,raw_lf_readbacks=v['actual_raw_lf_readback_count'],compiler='NOT_STARTED_CLOSED',browser='CLOSED_ACTUAL_FOREGROUND_EXIT',full_reader_accepted=False,PURIFIED=False,closed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),last_filesystem_operation=True)
print(json.dumps(dict(status='CLOSEDLAST_READY',run_sha256=run['run_sha256'],reader_controls_repair_payload_sha256=run['reader_controls_repair_payload_sha256'],readbacks=lease['raw_lf_readbacks'],resource=resource)))
write('lease.json',lease)
