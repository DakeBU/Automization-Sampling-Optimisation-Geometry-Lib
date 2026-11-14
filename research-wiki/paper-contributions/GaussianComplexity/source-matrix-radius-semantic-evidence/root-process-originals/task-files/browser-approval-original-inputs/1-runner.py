from pathlib import Path
import subprocess, json, hashlib, datetime, os, sys
ROOT=Path('/Users/zhouhuanjian/ASTIS-GC')
OUT=ROOT/'.astis/semantic-neutral-20261113/radius_native_5bf8'
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def run(label, argv, *, cwd=ROOT, env=None, check=True):
    d=OUT/'receipts';d.mkdir(parents=True,exist_ok=True)
    t=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    p=d/(t+'-'+label)
    head=subprocess.run(['git','rev-parse','HEAD'],cwd=ROOT,capture_output=True)
    meta={'label':label,'argv':list(map(str,argv)),'cwd':str(cwd),'started':t,'HEAD':head.stdout.decode().strip(),'HEAD_probe_exit':head.returncode,'env_overrides':env or {}}
    p.with_suffix('.pending.json').write_text(json.dumps(meta,indent=2)+'\n')
    e=os.environ.copy(); e.update(env or {})
    with p.with_suffix('.stdout').open('wb') as so,p.with_suffix('.stderr').open('wb') as se:
        proc=subprocess.run(list(map(str,argv)),cwd=cwd,env=e,stdout=so,stderr=se)
    meta.update(exit=proc.returncode,ended=datetime.datetime.now(datetime.timezone.utc).isoformat(),stdout_sha256=sha(p.with_suffix('.stdout')),stderr_sha256=sha(p.with_suffix('.stderr')))
    p.with_suffix('.json').write_text(json.dumps(meta,indent=2)+'\n');p.with_suffix('.pending.json').unlink()
    print(json.dumps({'label':label,'exit':proc.returncode,'receipt':str(p.with_suffix('.json'))}),flush=True)
    if check and proc.returncode: raise RuntimeError(label+' failed')
    return p,proc.returncode
if __name__=='__main__': run(sys.argv[1],sys.argv[2:])
