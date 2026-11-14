from pathlib import Path
import sys,subprocess,json,datetime,hashlib,time
p=Path('/Users/zhouhuanjian/ASTIS-GC/.astis/semantic-neutral-20261111/kr_src_c47e12/phase5-normal-sourceV')
label=sys.argv[1];argv=sys.argv[2:];start=datetime.datetime.now(datetime.timezone.utc).isoformat();t0=time.monotonic()
r=subprocess.run(argv,cwd='/Users/zhouhuanjian/ASTIS-GC',stdout=subprocess.PIPE,stderr=subprocess.PIPE)
(p/'audit'/(label+'.stdout')).write_bytes(r.stdout);(p/'audit'/(label+'.stderr')).write_bytes(r.stderr)
rec={'label':label,'argv':argv,'cwd':'/Users/zhouhuanjian/ASTIS-GC','started_utc':start,'ended_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'elapsed_seconds':time.monotonic()-t0,'exit_code':r.returncode}
for k,b in [('stdout',r.stdout),('stderr',r.stderr)]:rec[k]={'path':label+'.'+k,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
(p/'audit'/(label+'.receipt.json')).write_text(json.dumps(rec,indent=2)+'\n')
sys.stdout.buffer.write(r.stdout);sys.stdout.buffer.flush();sys.stderr.buffer.write(r.stderr);sys.stderr.buffer.flush()
raise SystemExit(r.returncode)

