from pathlib import Path
import json,subprocess,hashlib,datetime,os,sys
O=Path(__file__).parent;H=lambda b:hashlib.sha256(b).hexdigest()
for label,script in [('finalizer','foreground-finalizer.py'),('readback','foreground-readback.py')]:
 started=datetime.datetime.now(datetime.timezone.utc).isoformat();p=subprocess.Popen([sys.executable,str(O/script)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,cwd=str(O));out,err=p.communicate();(O/('foreground.'+label+'.stdout.log')).write_bytes(out);(O/('foreground.'+label+'.stderr.log')).write_bytes(err);d=dict(schema='diagnosis66-actually-observed-foreground-terminal-v1',label=label,actual_foreground_pid=p.pid,actual_exit_code=p.returncode,terminal_closed=True,observer_pid=os.getpid(),started_utc=started,finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),stdout_RAW_sha256=H(out),stderr_RAW_sha256=H(err));(O/('foreground.'+label+'.receipt.json')).write_bytes((json.dumps(d,sort_keys=True,indent=2)+'\n').encode());print(json.dumps(d,sort_keys=True),flush=True);print(out.decode(),flush=True)
 if p.returncode:print(err.decode(),flush=True);sys.exit(p.returncode)
