from pathlib import Path
import subprocess,json,hashlib,os
from datetime import datetime,timezone
R=Path('/Users/zhouhuanjian/ASTIS-GC');B=R/'.astis/semantic-neutral-20261112/mv_src_6e28/normal-verification-v2'
argv=['python3','-B',str(B/'normal_verify_once.py')];started=datetime.now(timezone.utc).isoformat()
p=subprocess.run(argv,cwd=R,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','GIT_OPTIONAL_LOCKS':'0'})
for name,data in [('normal-API.stdout',p.stdout),('normal-API.stderr',p.stderr)]:
 with (B/name).open('xb') as f:f.write(data)
r={'argv':argv,'cwd':str(R),'environment':dict(os.environ),'effective_overrides':{'PYTHONDONTWRITEBYTECODE':'1','GIT_OPTIONAL_LOCKS':'0'},'started_utc':started,'finished_utc':datetime.now(timezone.utc).isoformat(),'exit':p.returncode,'stdout_sha256':hashlib.sha256(p.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(p.stderr).hexdigest(),'script_sha256':hashlib.sha256((B/'normal_verify_once.py').read_bytes()).hexdigest()}
with (B/'normal-command-receipt.json').open('x') as f:f.write(json.dumps(r,indent=2)+'\n')
print('exit',p.returncode);print(p.stdout.decode());print(p.stderr.decode());raise SystemExit(p.returncode)
