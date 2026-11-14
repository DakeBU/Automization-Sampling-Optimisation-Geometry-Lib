from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,os,subprocess,sys,time
ROOT=Path('/Users/zhouhuanjian/ASTIS-GC')
OUT=Path(__file__).resolve().parent
label,*command=sys.argv[1:]
log=OUT/(label+'.log')
receipt=OUT/(label+'.receipt.json')
assert not log.exists(), label
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip()
assert head=='214b6214c5b08bd52b6faa59a3ccd6ca35998420'
env=os.environ.copy();env['LEAN_NUM_THREADS']='2'
start=time.monotonic()
print(json.dumps({'check':label,'command':command,'checked_head':head}),flush=True)
with log.open('w') as f:
 r=subprocess.run(command,cwd=ROOT,env=env,stdout=f,stderr=subprocess.STDOUT)
b=log.read_bytes()
record={'check':label,'command':command,'cwd':str(ROOT),'checked_commit':head,
 'head_after':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip(),
 'exit_code':r.returncode,'elapsed_seconds':time.monotonic()-start,
 'completed_utc':datetime.now(timezone.utc).isoformat(),'log':str(log.relative_to(ROOT)),
 'log_bytes':len(b),'log_sha256':hashlib.sha256(b).hexdigest(),'LEAN_NUM_THREADS':'2',
 'scope':'Independent focused candidate check; not canonical root/integration acceptance.'}
receipt.write_text(json.dumps(record,indent=2)+'\n')
print('\n'.join(b.decode(errors='replace').splitlines()[-16:]),flush=True)
print(json.dumps(record),flush=True)
sys.exit(r.returncode)
