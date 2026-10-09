import json,hashlib,os,sys,subprocess,datetime
from pathlib import Path
O=Path(__file__).parent
H=lambda b:hashlib.sha256(b).hexdigest()
def put(n,d):(O/n).write_bytes(json.dumps(d,ensure_ascii=False,sort_keys=True,indent=2).encode('utf-8')+b'\n')
assert not (O/'lease.final.json').exists()
child=subprocess.Popen([sys.executable,str(O/'close-validator.py')],stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=child.communicate();assert child.returncode==0 and not err
j=json.loads(out);assert j['actual_pid']==child.pid
(O/'terminal.close.stdout.log').write_bytes(out);(O/'terminal.close.stderr.log').write_bytes(err)
put('terminal.close.observed.json',dict(schema='source65-actually-observed-foreground-terminal-v1',role='close-validator',actual_foreground_pid=child.pid,actual_exit_code=child.returncode,terminal_closed=True,stdout_RAW_sha256=H(out),stderr_RAW_sha256=H(err),observed_by_foreground_lease_writer_pid=os.getpid(),validator_result=j))
# Finite, exhaustive closure manifest. Its own bytes are pinned by final lease;
# final lease bytes are pinned by the immediately following read-only tool result.
rows=[]
for p in sorted(O.iterdir()):
 if not p.is_file() or p.name in ['owned-manifest.json','lease.final.json']:continue
 b=p.read_bytes();lf=b.replace(b'\r\n',b'\n').replace(b'\r',b'\n');rows.append(dict(name=p.name,RAW_bytes=len(b),RAW_sha256=H(b),LF_sha256=H(lf)))
manifest=dict(schema='source65-exhaustive-owned-closure-manifest-v1',owned_directory=O.as_posix(),files=rows,all_owned_file_names=sorted([x['name'] for x in rows]+['owned-manifest.json','lease.final.json']),self_binding=dict(owned_manifest='RAW hash in lease.final.json',final_lease='external actual read-only postclose tool pin',no_self_hash_fixed_point_claim=True),negative_and_terminal_and_scripts_included=True,recursive_external_scope=False)
put('owned-manifest.json',manifest)
c=json.loads((O/'closure-index.json').read_bytes());f=json.loads((O/'terminal.finalizer.observed.json').read_bytes());r=json.loads((O/'terminal.readback.observed.json').read_bytes())
lease=dict(schema='source65-CLOSED_LAST-owned-lease-v1',status='CLOSED_LAST',owner='/root/independent_source64',owned_path=O.as_posix(),last_owned_write=True,postclose_writes_permitted=False,owned_file_count=len(manifest['all_owned_file_names']),manifest_RAW_sha256=H((O/'owned-manifest.json').read_bytes()),whole_logical_run_sha256=c['whole_logical_run_sha256'],COMPLETE_RAW_REVIEW=c['COMPLETE_RAW_REVIEW'],COMPLETE_RAW_DECISION=c['COMPLETE_RAW_DECISION'],SEPARATE_COMPLETE_RAW_INPUT=c['SEPARATE_COMPLETE_RAW_INPUT'],actual_finalizer_pid=f['actual_foreground_pid'],actual_finalizer_exit=f['actual_exit_code'],actual_readback_pid=r['actual_foreground_pid'],actual_readback_exit=r['actual_exit_code'],actual_close_validator_pid=child.pid,actual_close_validator_exit=child.returncode,foreground_lease_writer_pid=os.getpid(),lease_writer_exit_to_be_observed_by_tool=True,closed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
put('lease.final.json',lease)
# Nothing after this line writes owned files.
print(json.dumps(dict(status='CLOSED_LAST',actual_lease_writer_pid=os.getpid(),actual_close_validator_pid=child.pid,actual_close_validator_exit=child.returncode,owned_file_count=lease['owned_file_count'],manifest_RAW_sha256=lease['manifest_RAW_sha256'],lease_RAW_sha256=H((O/'lease.final.json').read_bytes()),whole_logical_run_sha256=c['whole_logical_run_sha256'],COMPLETE_RAW_REVIEW=c['COMPLETE_RAW_REVIEW'],COMPLETE_RAW_DECISION=c['COMPLETE_RAW_DECISION'],SEPARATE_COMPLETE_RAW_INPUT=c['SEPARATE_COMPLETE_RAW_INPUT']),sort_keys=True))
