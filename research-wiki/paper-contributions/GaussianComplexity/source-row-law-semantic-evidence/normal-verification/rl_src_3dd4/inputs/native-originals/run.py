"""Private bounded command runner: exact argv/cwd, original streams, receipts."""
import datetime, hashlib, json, os, pathlib, subprocess, sys, time
ROOT=pathlib.Path(__file__).resolve().parent
REPO=ROOT.parents[2]
def sha(b): return hashlib.sha256(b).hexdigest()
def run(label,argv,*,cwd=None,env=None,timeout=240):
    d=ROOT/'receipts';d.mkdir(exist_ok=True)
    assert not (d/(label+'.json')).exists(),label
    start=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic()
    try:
        p=subprocess.run(argv,cwd=str(cwd or REPO),env=env,capture_output=True,timeout=timeout)
    except subprocess.TimeoutExpired as e:
        p=subprocess.CompletedProcess(argv,124,e.stdout or b'',(e.stderr or b'')+b'\nTIMEOUT\n')
    except OSError as e:
        p=subprocess.CompletedProcess(argv,126,b'',str(e).encode())
    streams={}
    for name,data in [('stdout',p.stdout),('stderr',p.stderr)]:
        f=d/(label+'.'+name);f.write_bytes(data)
        streams[name]={'path':str(f.relative_to(ROOT)),'bytes':len(data),'sha256':sha(data)}
    rec={'label':label,'argv':argv,'cwd':str(cwd or REPO),'started_utc':start,'duration_seconds':time.monotonic()-t,'exit_code':p.returncode,'timeout_seconds':timeout,**streams}
    if env: rec['LEAN_PATH']=env.get('LEAN_PATH')
    (d/(label+'.json')).write_text(json.dumps(rec,indent=2)+'\n')
    print(json.dumps({'label':label,'exit_code':p.returncode,'stdout_bytes':len(p.stdout),'stderr_bytes':len(p.stderr)}),flush=True)
    return p
if __name__=='__main__': sys.exit(run(sys.argv[1],sys.argv[2:]).returncode)
