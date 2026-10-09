from pathlib import Path
import subprocess,sys,json,os,datetime,hashlib
O=Path(__file__).parent
label,target=sys.argv[1:];assert label in ['finalize','readback'];assert target in ['finalize-review.py','readback-review.py'];assert not (O/'lease.final.json').exists()
p=subprocess.Popen([sys.executable,str(O/target)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=dict(os.environ,PYTHONIOENCODING='utf-8',PYTHONDONTWRITEBYTECODE='1'));out,err=p.communicate()
(O/('foreground-'+label+'.stdout.log')).write_bytes(out);(O/('foreground-'+label+'.stderr.log')).write_bytes(err)
rec=dict(schema='source66-actual-foreground-terminal-receipt-v1',label=label,actual_foreground_pid=p.pid,actual_exit=p.returncode,actual_wrapper_pid=os.getpid(),detached=False,observed_by_communicate=True,completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),stdout=dict(name='foreground-'+label+'.stdout.log',RAW_sha256=hashlib.sha256(out).hexdigest(),bytes=len(out)),stderr=dict(name='foreground-'+label+'.stderr.log',RAW_sha256=hashlib.sha256(err).hexdigest(),bytes=len(err)))
(O/('foreground-'+label+'.receipt.json')).write_bytes((json.dumps(rec,sort_keys=True,indent=2)+'\n').encode());sys.stdout.buffer.write(out);sys.stderr.buffer.write(err);print(json.dumps(rec,sort_keys=True));sys.exit(p.returncode)
