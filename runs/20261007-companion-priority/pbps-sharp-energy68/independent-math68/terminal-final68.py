import sys,os,json,subprocess,hashlib,datetime
from pathlib import Path
O=Path(__file__).resolve().parent;mode=sys.argv[1];label=sys.argv[2] if len(sys.argv)>2 else mode
assert not (O/'lease.final.json').exists()
b=(O/'final68.py').read_bytes();p=O/(label+'.executed-helper.RAW.py');p.write_bytes(b)
stamp=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
with (O/(label+'.stdout.log')).open('wb') as a,(O/(label+'.stderr.log')).open('wb') as e:
 start=stamp();q=subprocess.Popen([sys.executable,'-B','-X','utf8',str(O/'final68.py'),mode,label],cwd='E:/Samplinglib',stdout=a,stderr=e);print(json.dumps(dict(event='START',stage=mode,label=label,actual_worker_PID=q.pid,actual_runner_PID=os.getpid())),flush=True);code=q.wait()
t=dict(stage=mode,label=label,actual_worker_PID=q.pid,actual_runner_PID=os.getpid(),started_utc=start,finished_utc=stamp(),exit_code=code,terminal_closed=True,executed_helper_RAW=dict(path=p.as_posix(),raw_bytes=len(b),raw_sha256=hashlib.sha256(b).hexdigest()));(O/(label+'.terminal.json')).write_text(json.dumps(t,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n');print(json.dumps(t));sys.exit(code)

