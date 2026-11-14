from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys,time
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'lean-toolchain').exists())
BASE=Path(__file__).resolve().parent
name=sys.argv[1];cmd=sys.argv[2:]
log=BASE/(name+'.log');meta=BASE/(name+'.receipt.json')
head=lambda:subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
start=datetime.datetime.now(datetime.timezone.utc).isoformat();h0=head();t=time.monotonic()
with log.open('wb') as f:
 p=subprocess.run(cmd,cwd=ROOT,stdout=f,stderr=subprocess.STDOUT)
b=log.read_bytes()
r={'schema':'independent-review-command-v1','command':cmd,'cwd':str(ROOT),'started_utc':start,'elapsed_seconds':time.monotonic()-t,'returncode':p.returncode,'head_before':h0,'head_after':head(),'log':str(log.relative_to(ROOT)),'log_sha256':hashlib.sha256(b).hexdigest(),'log_bytes':len(b)}
meta.write_text(json.dumps(r,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
print(json.dumps(r,ensure_ascii=False));print(b.decode(errors='replace')[-10000:]);sys.exit(p.returncode)
