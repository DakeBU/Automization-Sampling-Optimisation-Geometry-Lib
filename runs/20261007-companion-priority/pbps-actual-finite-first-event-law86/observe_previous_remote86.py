from pathlib import Path
import subprocess,json,datetime,hashlib
r=Path(__file__).parent;out=r/'previous85-remote-observation86';out.mkdir(exist_ok=False)
cmd=['gh','run','view','38074998616','--json','headSha,status,conclusion,jobs,url']
p=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
(out/'stdout.native.json').write_bytes(p.stdout);(out/'stderr.native.log').write_bytes(p.stderr)
x=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),command=cmd,exit_code=p.returncode,terminal_closed=True,stdout_RAW_sha256=hashlib.sha256(p.stdout).hexdigest(),stderr_RAW_sha256=hashlib.sha256(p.stderr).hexdigest())
(out/'receipt.json').write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8',newline='\n')
if p.returncode==0:
 a=json.loads(p.stdout);assert a['headSha']=='8280ef700ea01a1e94c9e7a3cba05a26b4156b56';print(json.dumps({k:a[k] for k in ['headSha','status','conclusion','url']}));print([(j['name'],j['status'],j['conclusion']) for j in a['jobs']])
else:print(p.stderr.decode(errors='replace'))
