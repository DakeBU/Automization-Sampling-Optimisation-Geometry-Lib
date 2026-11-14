from pathlib import Path
import subprocess,json,hashlib
from datetime import datetime,timezone
R=Path('/Users/zhouhuanjian/ASTIS-GC');B=R/'.astis/semantic-neutral-20261112/mv_src_6e28/normal-verification-v2'
a=['python3','-B',str(B/'freeze_normal.py')];start=datetime.now(timezone.utc).isoformat();p=subprocess.run(a,cwd=R,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
for n,d in [('postseal-command.stdout',p.stdout),('postseal-command.stderr',p.stderr)]:
 with (B/n).open('xb') as f:f.write(d)
r={'argv':a,'cwd':str(R),'started_utc':start,'finished_utc':datetime.now(timezone.utc).isoformat(),'exit':p.returncode,'stdout_sha256':hashlib.sha256(p.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(p.stderr).hexdigest(),'script_sha256':hashlib.sha256((B/'freeze_normal.py').read_bytes()).hexdigest()}
with (B/'postseal-command-receipt.json').open('x') as f:f.write(json.dumps(r,indent=2)+'\n')
print(p.stdout.decode());print(p.stderr.decode());raise SystemExit(p.returncode)
