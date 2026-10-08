from common import *
with (D/'review.actual.log').open('wb') as log:
 p=subprocess.Popen([sys.executable,'-B','-X','utf8',str(D/'review.py')],cwd=ROOT,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONUTF8='1'),stdout=log,stderr=subprocess.STDOUT);pid=p.pid;rc=p.wait()
write(D/'review.actual.status.json',dict(actual_worker_PID=pid,actual_wrapper_PID=os.getpid(),exit_code=rc,resource='CLOSED',log=pin(D/'review.actual.log')))
if rc:print((D/'review.actual.log').read_text(encoding='utf8')[-6000:])
else:print((D/'review.actual.log').read_text(encoding='utf8'))
sys.exit(rc)
