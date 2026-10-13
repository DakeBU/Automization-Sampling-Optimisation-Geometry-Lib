import os,sys,json,hashlib,subprocess,datetime
from pathlib import Path
O=Path(__file__).resolve().parent
assert not (O/'lease.final.json').exists()
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
 b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');return dict(path=p.as_posix(),raw_bytes=len(b),raw_sha256=sha(b),lf_bytes=len(lf),lf_sha256=sha(lf))
def write(n,x):
 assert not(O/'lease.final.json').exists();(O/n).write_bytes((json.dumps(x,sort_keys=True,ensure_ascii=False,indent=2)+'\n').encode())
def stamp():return datetime.datetime.now(datetime.timezone.utc).isoformat()
b=(O/'closure71.py').read_bytes();snap=O/'close.executed-helper.RAW.py';snap.write_bytes(b)
with (O/'close.stdout.log').open('wb') as out,(O/'close.stderr.log').open('wb') as err:
 start=stamp();p=subprocess.Popen([sys.executable,'-B','-X','utf8',str(O/'closure71.py'),'preclose','close'],cwd='E:/Samplinglib',stdout=out,stderr=err);print(json.dumps(dict(event='CLOSE_WORKER_START',actual_worker_PID=p.pid,actual_runner_PID=os.getpid())),flush=True);code=p.wait()
receipt=dict(stage='close',actual_worker_PID=p.pid,actual_runner_PID=os.getpid(),started_utc=start,finished_utc=stamp(),exit_code=code,terminal_closed=True,executed_helper_RAW=pin(snap));write('close.terminal.json',receipt)
if code:sys.exit(code)
rows=[dict(relative_path=p.relative_to(O).as_posix(),**pin(p)) for p in sorted(O.rglob('*')) if p.is_file() and p.name not in ['outputs.manifest.json','lease.final.json']]
write('outputs.manifest.json',dict(schema='all-owned-output-RAW-LF-manifest-v1',files=rows,hashed_file_count=len(rows),expected_owned_file_count=len(rows)+2,self_layers=[dict(relative_path='outputs.manifest.json',hash_authority='Final CLOSED_LAST lease exact row.'),dict(relative_path='lease.final.json',hash_authority='External read-only postclose RAW pin; cannot embed its own hash recursively.')],LF_recipe='Replace ONLY CRLF with LF; RAW authoritative.',no_file_exclusions=True))
rows=[dict(relative_path=p.relative_to(O).as_posix(),**pin(p)) for p in sorted(O.rglob('*')) if p.is_file() and p.name!='lease.final.json']
run=json.loads((O/'run.json').read_bytes());lease=dict(schema='independent-source-first71-CLOSED-LAST-v1',status='CLOSED_LAST',actor='/root/exact_science63',actual_close_runner_PID=os.getpid(),actual_close_worker_PID=p.pid,actual_close_worker_exit_code=0,closed_utc=stamp(),owned_file_count=len(rows)+1,manifest=rows,manifest_logical_sha256=sha(json.dumps(rows,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()),lease_self=dict(relative_path='lease.final.json',hash_authority='Read-only postclose stdout; final write itself cannot contain its own RAW hash.'),whole_logical_run_sha256=run['run_sha256'],named_complete_RAW_payload=pin(O/'named-review.payload.json'),all_owned_layers_bound=True,last_owned_write=True,postclose_writes_allowed=False,runner_exit_authority='Actual foreground terminal result outside immutable scope; no receipt appended after closure.')
write('lease.final.json',lease)
print(json.dumps(dict(status='CLOSED_LAST',actual_close_runner_PID=os.getpid(),actual_close_worker_PID=p.pid,actual_close_worker_exit_code=0,owned_file_count=lease['owned_file_count'],lease_RAW=pin(O/'lease.final.json'),whole_logical_run_sha256=run['run_sha256'],named_complete_RAW_payload=pin(O/'named-review.payload.json'))))
