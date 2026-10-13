from common import *
sys.stdout.reconfigure(encoding='utf8')
started=datetime.datetime.now(datetime.timezone.utc).isoformat()
p=subprocess.Popen([sys.executable,'-B','-X','utf8',str(O/'check.py')],cwd=R,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
out,_=p.communicate();(O/'check.actual.log').write_bytes(out)
d=dict(status='PASS' if p.returncode==0 else 'FAILED',command=[sys.executable,'-B','-X','utf8',str(O/'check.py')],actual_check_Python_PID=p.pid,actual_driver_Python_PID=os.getpid(),actual_exit_code=p.returncode,resource='CLOSED',compiler='NOT_STARTED_CLOSED',started_utc=started,closed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),log=pin(O/'check.actual.log'))
dump('check.actual.status.json',d);print(out.decode('utf8'));print(json.dumps(d));raise SystemExit(p.returncode)
