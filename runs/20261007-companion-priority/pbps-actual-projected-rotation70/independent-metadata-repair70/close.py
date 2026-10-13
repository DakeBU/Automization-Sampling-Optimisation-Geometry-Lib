import os,sys,json,hashlib,subprocess,datetime
from pathlib import Path
O=Path(__file__).resolve().parent;assert not(O/'lease.final.json').exists()
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
 b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');return dict(path=p.as_posix(),raw_bytes=len(b),raw_sha256=sha(b),lf_bytes=len(lf),lf_sha256=sha(lf))
def write(n,x):
 assert not(O/'lease.final.json').exists();(O/n).write_bytes((json.dumps(x,sort_keys=True,ensure_ascii=False,indent=2)+'\n').encode())
stamp=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat();snap=O/'close.executed-helper.RAW.py';snap.write_bytes((O/'review.py').read_bytes())
with (O/'close.stdout.log').open('wb') as out,(O/'close.stderr.log').open('wb') as err:
 start=stamp();p=subprocess.Popen([sys.executable,'-B','-X','utf8',str(O/'review.py'),'preclose','close'],cwd='E:/Samplinglib',stdout=out,stderr=err);print(json.dumps(dict(event='CLOSE_START',actual_worker_PID=p.pid,actual_runner_PID=os.getpid())),flush=True);code=p.wait()
write('close.terminal.json',dict(stage='close',actual_worker_PID=p.pid,actual_runner_PID=os.getpid(),started_utc=start,finished_utc=stamp(),exit_code=code,terminal_closed=True,executed_helper_RAW=pin(snap)))
if code:sys.exit(code)
rows=[dict(relative_path=f.relative_to(O).as_posix(),**pin(f)) for f in sorted(O.rglob('*')) if f.is_file() and f.name not in ['outputs.manifest.json','lease.final.json']]
write('outputs.manifest.json',dict(schema='all-owned-output-RAW-LF-manifest-v1',files=rows,hashed_file_count=len(rows),expected_owned_file_count=len(rows)+2,self_layers=[dict(relative_path='outputs.manifest.json',hash_authority='Exact final lease row.'),dict(relative_path='lease.final.json',hash_authority='External read-only postclose RAW pin; no recursive self hash.')],LF_recipe='Replace ONLY CRLF with LF; RAW authoritative.',no_file_exclusions=True))
rows=[dict(relative_path=f.relative_to(O).as_posix(),**pin(f)) for f in sorted(O.rglob('*')) if f.is_file() and f.name!='lease.final.json'];r=json.loads((O/'run.json').read_bytes())
l=dict(schema='independent-metadata-repair70-CLOSED-LAST-v1',status='CLOSED_LAST',actor='/root/exact_science63',actual_close_runner_PID=os.getpid(),actual_close_worker_PID=p.pid,actual_close_worker_exit_code=0,closed_utc=stamp(),owned_file_count=len(rows)+1,manifest=rows,manifest_logical_sha256=sha(json.dumps(rows,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()),lease_self=dict(relative_path='lease.final.json',hash_authority='External read-only postclose stdout.'),whole_logical_run_sha256=r['run_sha256'],named_complete_RAW_payload=pin(O/'named-review.payload.json'),all_owned_layers_bound=True,last_owned_write=True,postclose_writes_allowed=False,runner_exit_authority='Actual foreground terminal outside immutable scope.')
write('lease.final.json',l);print(json.dumps(dict(status='CLOSED_LAST',actual_close_worker_PID=p.pid,actual_close_runner_PID=os.getpid(),actual_close_worker_exit_code=0,owned_file_count=l['owned_file_count'],lease_RAW=pin(O/'lease.final.json'),whole_logical_run_sha256=r['run_sha256'],named_complete_RAW_payload=pin(O/'named-review.payload.json'))))
