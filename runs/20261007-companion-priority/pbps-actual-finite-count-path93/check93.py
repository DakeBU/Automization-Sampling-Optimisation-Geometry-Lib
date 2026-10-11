"""Foreground bounded check runner with immutable raw outputs."""
from pathlib import Path
import subprocess,os,sys,json,datetime,time
root=Path(__file__).resolve().parents[3];run=Path(__file__).resolve().parent
label=sys.argv[1];args=sys.argv[2:];out=run/'checks93'/label
out.mkdir(parents=True,exist_ok=False)
env=os.environ.copy();env.pop('ELAN_TOOLCHAIN',None)
env['PATH']=str(root/'.astis/toolchain/lean-4.33.0-windows/bin')+os.pathsep+env.get('PATH','')
start=time.monotonic();utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
with (out/'stdout.log').open('wb') as stdout,(out/'stderr.log').open('wb') as stderr:
    p=subprocess.run(args,cwd=root,env=env,stdout=stdout,stderr=stderr)
r=dict(started_utc=utc,ended_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),seconds=time.monotonic()-start,argv=args,exit_code=p.returncode,terminal_closed=True)
(out/'receipt.json').write_text(json.dumps(r,indent=2)+'\n',encoding='utf8')
print(json.dumps(r))
for f in ['stdout.log','stderr.log']:
    text=(out/f).read_text(encoding='utf8',errors='replace')
    print(text if len(text)<6500 else text[-6500:])
sys.exit(p.returncode)
