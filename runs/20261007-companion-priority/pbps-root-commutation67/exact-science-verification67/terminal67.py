import sys,os,json,subprocess,datetime,hashlib
from pathlib import Path
O=Path(__file__).resolve().parent;mode=sys.argv[1];label=sys.argv[2] if len(sys.argv)>2 else mode
assert mode not in ['close','postclose'] and not (O/'lease.final.json').exists()
b=(O/'verify67.py').read_bytes();s=O/(label+'.executed-helper.RAW.py');s.write_bytes(b)
stamp=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
with (O/(label+'.stdout.log')).open('wb') as a,(O/(label+'.stderr.log')).open('wb') as e:
 start=stamp();p=subprocess.Popen([sys.executable,'-B','-X','utf8',str(O/'verify67.py'),mode],cwd='E:/Samplinglib',stdout=a,stderr=e);print(json.dumps(dict(event='START',stage=mode,label=label,actual_worker_PID=p.pid,actual_runner_PID=os.getpid())),flush=True);code=p.wait()
t=dict(stage=mode,label=label,actual_worker_PID=p.pid,actual_runner_PID=os.getpid(),started_utc=start,finished_utc=stamp(),exit_code=code,terminal_closed=True,executed_helper_RAW=dict(path=s.as_posix(),raw_bytes=len(b),raw_sha256=hashlib.sha256(b).hexdigest()));(O/(label+'.terminal.json')).write_text(json.dumps(t,sort_keys=True,indent=2)+'\n',encoding='utf-8',newline='\n');print(json.dumps(t));sys.exit(code)
