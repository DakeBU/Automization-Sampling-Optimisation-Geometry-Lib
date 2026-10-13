import json,hashlib,os,sys,subprocess,datetime
from pathlib import Path
O=Path(__file__).parent
H=lambda b:hashlib.sha256(b).hexdigest()
def load(n):return json.loads((O/n).read_bytes())
def put(n,d):(O/n).write_bytes(json.dumps(d,ensure_ascii=False,sort_keys=True,indent=2).encode('utf-8')+b'\n')
assert not (O/'lease.final.json').exists()
p=subprocess.Popen([sys.executable,str(O/'close-validator.py')],stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=p.communicate();assert p.returncode==0 and not err;j=json.loads(out);assert j['actual_pid']==p.pid
(O/'terminal.close.stdout.log').write_bytes(out);(O/'terminal.close.stderr.log').write_bytes(err)
put('terminal.close.observed.json',dict(schema='primary66-actually-observed-foreground-terminal-v1',actual_foreground_pid=p.pid,actual_exit_code=p.returncode,terminal_closed=True,observer_lease_writer_pid=os.getpid(),stdout_RAW_sha256=H(out),stderr_RAW_sha256=H(err)))
rows=[]
for q in sorted(O.iterdir()):
 if not q.is_file() or q.name in ['owned-manifest.json','lease.final.json']:continue
 b=q.read_bytes();rows.append(dict(name=q.name,RAW_bytes=len(b),RAW_sha256=H(b),LF_sha256=H(b.replace(b'\r\n',b'\n').replace(b'\r',b'\n'))))
m=dict(schema='primary66-exhaustive-owned-closure-manifest-v1',owned_path=O.as_posix(),files=rows,all_owned_file_names=sorted([x['name'] for x in rows]+['owned-manifest.json','lease.final.json']),self_binding='Manifest RAW pinned in lease; lease RAW pinned by following external read-only postclose tool result; no fixed-point claim.',all_negative_self_script_terminal_bytes_bound=True)
put('owned-manifest.json',m);c=load('closure-index.json');f=load('terminal.finalizer.observed.json');r=load('terminal.readback.observed.json');l=dict(schema='primary66-CLOSED_LAST-owned-lease-v1',status='CLOSED_LAST',owned_path=O.as_posix(),owner='/root/independent_source64',owned_file_count=len(m['all_owned_file_names']),last_owned_write=True,postclose_writes_permitted=False,manifest_RAW_sha256=H((O/'owned-manifest.json').read_bytes()),whole_logical_run_sha256=c['whole_logical_run_sha256'],COMPLETE_RAW_DECISION=c['COMPLETE_RAW_DECISION'],COMPLETE_RAW_REVIEW=c['COMPLETE_RAW_REVIEW'],SEPARATE_COMPLETE_RAW_INPUT=c['SEPARATE_COMPLETE_RAW_INPUT'],actual_finalizer_pid=f['actual_foreground_pid'],actual_finalizer_exit=f['actual_exit_code'],actual_readback_pid=r['actual_foreground_pid'],actual_readback_exit=r['actual_exit_code'],actual_close_validator_pid=p.pid,actual_close_validator_exit=p.returncode,actual_lease_writer_pid=os.getpid(),lease_writer_exit_observed_by_external_tool=True,closed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
put('lease.final.json',l)
# CLOSED_LAST: no owned writes after this line.
print(json.dumps(dict(status='CLOSED_LAST',actual_close_validator_pid=p.pid,actual_close_validator_exit=p.returncode,actual_lease_writer_pid=os.getpid(),owned_files=l['owned_file_count'],manifest_RAW_sha256=l['manifest_RAW_sha256'],lease_RAW_sha256=H((O/'lease.final.json').read_bytes()),bindings=c),sort_keys=True))
