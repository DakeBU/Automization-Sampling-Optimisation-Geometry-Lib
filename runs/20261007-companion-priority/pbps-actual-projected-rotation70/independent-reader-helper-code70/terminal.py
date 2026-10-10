import os,sys,json,hashlib,subprocess,datetime
from pathlib import Path
O=Path(__file__).resolve().parent;mode=sys.argv[1];label=sys.argv[2] if len(sys.argv)>2 else mode;assert not(O/'lease.final.json').exists()
def pin(p):
 b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');return dict(path=p.as_posix(),raw_bytes=len(b),raw_sha256=hashlib.sha256(b).hexdigest(),lf_bytes=len(lf),lf_sha256=hashlib.sha256(lf).hexdigest())
stamp=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat();snap=O/(label+'.executed-helper.RAW.py');snap.write_bytes((O/'review.py').read_bytes())
with (O/(label+'.stdout.log')).open('wb') as out,(O/(label+'.stderr.log')).open('wb') as err:
 start=stamp();p=subprocess.Popen([sys.executable,'-B','-X','utf8',str(O/'review.py'),mode,label],cwd='E:/Samplinglib',stdout=out,stderr=err);print(json.dumps(dict(event='START',actual_worker_PID=p.pid,actual_runner_PID=os.getpid(),mode=mode,label=label)),flush=True);code=p.wait()
r=dict(stage=mode,label=label,actual_worker_PID=p.pid,actual_runner_PID=os.getpid(),started_utc=start,finished_utc=stamp(),exit_code=code,terminal_closed=True,executed_helper_RAW=pin(snap));(O/(label+'.terminal.json')).write_bytes((json.dumps(r,sort_keys=True,indent=2)+'\n').encode());print(json.dumps(r));sys.exit(code)
