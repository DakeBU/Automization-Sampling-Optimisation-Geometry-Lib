import os,sys,json,hashlib,datetime,subprocess
from pathlib import Path
O=Path(__file__).resolve().parent
mode=sys.argv[1];assert mode in ['finalize','readback'];assert not (O/'lease.final.json').exists()
label='finalizer' if mode=='finalize' else 'readback'
env=dict(os.environ);env['PYTHONIOENCODING']='utf-8'
p=subprocess.Popen([sys.executable,str(O/'native-finalizer.py'),mode],stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=env)
out,err=p.communicate();(O/('foreground-'+label+'.stdout.txt')).write_bytes(out);(O/('foreground-'+label+'.stderr.txt')).write_bytes(err)
r={'schema':'primary65-foreground-terminal-receipt-v1','role':label,'pid':p.pid,'runner_pid':os.getpid(),'exit_code':p.returncode,'foreground_waited':True,'detached':False,'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'stdout_sha256':hashlib.sha256(out).hexdigest(),'stderr_sha256':hashlib.sha256(err).hexdigest(),'stdout_result':json.loads(out.decode('utf-8')) if p.returncode==0 else None}
(O/('foreground-'+label+'.receipt.json')).write_bytes((json.dumps(r,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode());sys.stdout.buffer.write(out);sys.stderr.buffer.write(err);print(json.dumps({'runner_pid':os.getpid(),'child_pid':p.pid,'exit_code':p.returncode,'receipt':'foreground-'+label+'.receipt.json'},sort_keys=True));sys.exit(p.returncode)
