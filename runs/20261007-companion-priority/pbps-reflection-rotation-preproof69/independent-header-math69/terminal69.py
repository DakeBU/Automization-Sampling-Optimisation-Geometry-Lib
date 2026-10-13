import sys,os,json,hashlib,subprocess,datetime
from pathlib import Path
O=Path(__file__).resolve().parent;mode=sys.argv[1];label=sys.argv[2] if len(sys.argv)>2 else mode;script=sys.argv[3] if len(sys.argv)>3 else 'review69.py';assert not (O/'lease.final.json').exists()
b=(O/script).read_bytes();snap=O/(label+'.executed-helper.RAW.py');snap.write_bytes(b);stamp=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
with (O/(label+'.stdout.log')).open('wb') as out,(O/(label+'.stderr.log')).open('wb') as err:
 start=stamp();p=subprocess.Popen([sys.executable,'-B','-X','utf8',str(O/script),mode,label],cwd='E:/Samplinglib',stdout=out,stderr=err);print(json.dumps(dict(event='START',actual_worker_PID=p.pid,actual_runner_PID=os.getpid(),stage=mode,label=label)),flush=True);code=p.wait()
r=dict(stage=mode,label=label,actual_worker_PID=p.pid,actual_runner_PID=os.getpid(),started_utc=start,finished_utc=stamp(),exit_code=code,terminal_closed=True,executed_helper_RAW=dict(path=snap.as_posix(),raw_bytes=len(b),raw_sha256=hashlib.sha256(b).hexdigest()));(O/(label+'.terminal.json')).write_bytes((json.dumps(r,sort_keys=True,indent=2)+'\n').encode());print(json.dumps(r));sys.exit(code)
