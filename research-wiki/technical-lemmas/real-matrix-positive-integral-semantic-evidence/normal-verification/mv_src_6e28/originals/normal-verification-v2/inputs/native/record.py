#!/usr/bin/env python3
import argparse, datetime, hashlib, json, os, pathlib, subprocess, sys
ROOT=pathlib.Path(__file__).resolve().parent
REPO=pathlib.Path('/Users/zhouhuanjian/ASTIS-GC')
COMMIT='9964c33c4599f85d27dc8687e8bd6fdb5c44ff49'
def sha(data): return hashlib.sha256(data).hexdigest()
def run(label, argv, cwd=None, env=None, show=True):
    cwd=str(cwd or REPO); effective=os.environ.copy()
    if env: effective.update(env)
    d=ROOT/'receipts'; d.mkdir(exist_ok=True)
    stem=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')+'-'+label
    started=datetime.datetime.now(datetime.timezone.utc).isoformat()
    p=subprocess.run(argv,cwd=cwd,env=effective,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    (d/(stem+'.stdout')).write_bytes(p.stdout); (d/(stem+'.stderr')).write_bytes(p.stderr)
    h=subprocess.run(['git','rev-parse','HEAD'],cwd=REPO,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    receipt={'label':label,'argv':argv,'cwd':cwd,'environment':effective,'candidate_commit':COMMIT,'shared_head_at_finish':h.stdout.decode().strip(),'started_utc':started,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit':p.returncode,'stdout_file':stem+'.stdout','stderr_file':stem+'.stderr','stdout_sha256':sha(p.stdout),'stderr_sha256':sha(p.stderr)}
    (d/(stem+'.json')).write_text(json.dumps(receipt,indent=2)+'\n')
    if show:
        print(json.dumps({'label':label,'exit':p.returncode,'receipt':str(d/(stem+'.json'))}))
        sys.stdout.flush(); sys.stdout.buffer.write(p.stdout); sys.stderr.buffer.write(p.stderr)
    return p
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('label');ap.add_argument('--cwd',default=str(REPO));ap.add_argument('argv',nargs=argparse.REMAINDER);a=ap.parse_args()
    argv=a.argv[1:] if a.argv and a.argv[0]=='--' else a.argv
    sys.exit(run(a.label,argv,a.cwd).returncode)
