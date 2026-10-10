from pathlib import Path
import datetime, hashlib, json, os, subprocess, sys
O=Path(__file__).parent
R=Path('E:/Samplinglib')
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
cmd=[sys.executable,'-X','utf8',str(O/'audit_exact_proposal86.py')]
env=dict(os.environ,PYTHONUTF8='1')
p=subprocess.run(cmd,cwd=R,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
log=O/'audit-attempt1.log'
with log.open('xb') as f:f.write(p.stdout)
r=dict(command=cmd,cwd=str(R),environment={'PYTHONUTF8':'1'},started_utc=start,ended_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),exit_code=p.returncode,foreground=True,log=dict(path=log.relative_to(R).as_posix(),raw_sha256=hashlib.sha256(p.stdout).hexdigest(),bytes=len(p.stdout)))
with (O/'audit-attempt1.receipt.json').open('x',encoding='utf8',newline='\n') as f:json.dump(r,f,indent=2);f.write('\n')
print(p.stdout.decode('utf8',errors='replace'))
print('TERMINAL_EXIT',p.returncode)
sys.exit(p.returncode)
