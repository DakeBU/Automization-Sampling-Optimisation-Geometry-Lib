#!/usr/bin/env python3
import subprocess, os, sys, json, hashlib, datetime
from pathlib import Path
ROOT=Path('/Users/zhouhuanjian/ASTIS-GC')
OUT=ROOT/'.astis/semantic-neutral-20261113/variance_native_61d0'
COMMIT='e654e98642350a615c473bc8190fbc1d47fe52bd'
def sha(b): return hashlib.sha256(b).hexdigest()
ENV={k:os.environ[k] for k in ('HOME','PATH','LANG','LC_ALL','TMPDIR') if k in os.environ}
ENV.update({'LANG':'en_US.UTF-8','PYTHONUNBUFFERED':'1'})
def run(label,argv,cwd=ROOT,env=None,check=True):
    d=OUT/'commands'/label; d.mkdir(parents=True,exist_ok=False)
    effective=ENV.copy(); effective.update(env or {})
    head=subprocess.run(['git','rev-parse','HEAD'],cwd=ROOT,env=ENV,capture_output=True).stdout.decode().strip()
    m={'argv':list(map(str,argv)),'cwd':str(cwd),'effective_env':effective,'observed_shared_head':head,'compiled_commit':COMMIT,'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'runner_sha256':sha(Path(__file__).read_bytes())}
    (d/'start.json').write_text(json.dumps(m,indent=2))
    with (d/'stdout').open('wb') as o,(d/'stderr').open('wb') as e:
        p=subprocess.run(m['argv'],cwd=cwd,env=effective,stdout=o,stderr=e)
    m.update({'exit':p.returncode,'ended_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
    for f in ('stdout','stderr'): m[f]={'path':str(d/f),'bytes':(d/f).stat().st_size,'sha256':sha((d/f).read_bytes())}
    (d/'result.json').write_text(json.dumps(m,indent=2)); print(label,p.returncode,flush=True)
    if check and p.returncode: raise RuntimeError(f'{label}: exit {p.returncode}; see {d}')
    return (d/'stdout').read_bytes()
def show(path,label=None):
    b=run(label or 'read-'+path.replace('/','__'),['git','show',f'{COMMIT}:{path}'])
    p=OUT/'inputs'/path; p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b);return b
if __name__=='__main__':
    for path in sys.argv[1:]: print(show(path).decode())
