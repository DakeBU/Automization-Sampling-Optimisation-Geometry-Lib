from pathlib import Path
from datetime import datetime,timezone
import subprocess,sys,json,hashlib
BASE=Path(__file__).resolve().parent
label=sys.argv[1];argv=sys.argv[2:]
start=datetime.now(timezone.utc).isoformat()
r=subprocess.run(argv,cwd='/Users/zhouhuanjian/ASTIS-GC',capture_output=True)
for ext,b in [('stdout',r.stdout),('stderr',r.stderr)]:
 p=BASE/(label+'.'+ext+'.raw');assert not p.exists();p.write_bytes(b)
rec={'argv':argv,'cwd':'/Users/zhouhuanjian/ASTIS-GC','started':start,'finished':datetime.now(timezone.utc).isoformat(),'returncode':r.returncode,'stdout_bytes':len(r.stdout),'stdout_sha256':hashlib.sha256(r.stdout).hexdigest(),'stderr_bytes':len(r.stderr),'stderr_sha256':hashlib.sha256(r.stderr).hexdigest()}
p=BASE/(label+'.command.receipt.json');assert not p.exists();p.write_text(json.dumps(rec,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(rec,ensure_ascii=False,indent=2));sys.stdout.flush()
sys.stdout.buffer.write(r.stdout);sys.stderr.buffer.write(r.stderr)
sys.exit(r.returncode)
