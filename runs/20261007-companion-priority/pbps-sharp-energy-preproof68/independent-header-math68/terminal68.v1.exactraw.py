import sys, subprocess, json, os, datetime, hashlib
from pathlib import Path
O=Path(__file__).resolve().parent
mode=sys.argv[1]
assert mode not in ['close','postclose']
assert not (O/'lease.final.json').exists()
b=(O/'review68.py').read_bytes();snapshot=O/(mode+'.executed-helper.RAW.py');snapshot.write_bytes(b)
stamp=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
with (O/(mode+'.stdout.log')).open('wb') as a,(O/(mode+'.stderr.log')).open('wb') as c:
 start=stamp();p=subprocess.Popen([sys.executable,'-B','-X','utf8',str(O/'review68.py'),mode],cwd='E:/Samplinglib',stdout=a,stderr=c)
 print(json.dumps(dict(event='START',stage=mode,actual_worker_pid=p.pid,actual_runner_pid=os.getpid())),flush=True);code=p.wait()
t=dict(stage=mode,actual_worker_pid=p.pid,actual_runner_pid=os.getpid(),exit_code=code,terminal_closed=True,started_utc=start,finished_utc=stamp(),executed_helper_RAW=dict(path=snapshot.as_posix(),raw_bytes=len(b),raw_sha256=hashlib.sha256(b).hexdigest()))
(O/(mode+'.terminal.json')).write_text(json.dumps(t,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(t));sys.exit(code)
