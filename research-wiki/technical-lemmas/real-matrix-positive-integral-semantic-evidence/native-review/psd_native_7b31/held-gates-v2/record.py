import datetime, hashlib, json, os, pathlib, subprocess, sys
ROOT=pathlib.Path(__file__).resolve().parent
REPO=pathlib.Path('/Users/zhouhuanjian/ASTIS-GC')
EXPECTED_HEAD='5f69ac83737e497210d8d8ad9628c45d83089458'
PARENT_HEAD='7d6d61f298e882f54c4bc36b1fb67502d2801e77'
MATH_HEAD='9964c33c4599f85d27dc8687e8bd6fdb5c44ff49'
def sha(data):return hashlib.sha256(data).hexdigest()
def run(label,argv,cwd=REPO,env=None,show=False):
    cwd=str(cwd);effective=os.environ.copy()
    if env:effective.update(env)
    d=ROOT/'receipts';d.mkdir(exist_ok=True)
    stem=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')+'-'+label
    before=subprocess.run(['git','rev-parse','HEAD'],cwd=REPO,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    started=datetime.datetime.now(datetime.timezone.utc).isoformat()
    p=subprocess.run(argv,cwd=cwd,env=effective,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    finished=datetime.datetime.now(datetime.timezone.utc).isoformat()
    after=subprocess.run(['git','rev-parse','HEAD'],cwd=REPO,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    (d/(stem+'.stdout')).write_bytes(p.stdout);(d/(stem+'.stderr')).write_bytes(p.stderr)
    receipt={'phase':'final-held-metadata-gates-v2','label':label,'argv':argv,'cwd':cwd,'environment':effective,'expected_held_HEAD':EXPECTED_HEAD,'parent_failed_held_HEAD':PARENT_HEAD,'fixed_mathematical_candidate':MATH_HEAD,'shared_HEAD_before':before.stdout.decode().strip(),'shared_HEAD_after':after.stdout.decode().strip(),'started_utc':started,'finished_utc':finished,'exit':p.returncode,'stdout_file':stem+'.stdout','stderr_file':stem+'.stderr','stdout_bytes':len(p.stdout),'stderr_bytes':len(p.stderr),'stdout_sha256':sha(p.stdout),'stderr_sha256':sha(p.stderr)}
    path=d/(stem+'.json');path.write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({'label':label,'exit':p.returncode,'receipt':str(path)}),flush=True)
    if show:sys.stdout.buffer.write(p.stdout);sys.stderr.buffer.write(p.stderr)
    return p,path
if __name__=='__main__':
    p,_=run(sys.argv[1],sys.argv[2:],show=True)
    sys.exit(p.returncode)
