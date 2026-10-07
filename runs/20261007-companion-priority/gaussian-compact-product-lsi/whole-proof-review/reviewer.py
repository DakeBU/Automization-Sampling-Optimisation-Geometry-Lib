from pathlib import Path
import hashlib,json,subprocess,os,datetime,sys
ROOT=Path('E:/Samplinglib'); R=ROOT/'runs/20261007-companion-priority/gaussian-compact-product-lsi'; O=R/'whole-proof-review'
V='picard_commit_verifier_20261005'
def j(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def d(p):
 p=Path(p); b=p.read_bytes(); return dict(path=p.relative_to(ROOT).as_posix(),bytes=len(b),raw_sha256=hashlib.sha256(b).hexdigest(),lf_sha256=hashlib.sha256(b.replace(b'\r\n',b'\n')).hexdigest())
def put(p,x):
 p=Path(p); assert not p.exists(),p; p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()); return d(p)
def head(): return subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip()
if __name__=='__main__':
 mode=sys.argv[1]
 if mode=='freeze':
  assert head()=='1eb2e29307d59fab662db842c3a6264c65245fe3'
  f=j(R/'math-freeze.json'); rows=[]
  for n,item in enumerate(f['inputs']):
   p=ROOT/item['path']; actual=d(p); assert all(actual[k]==item[k] for k in ['raw_sha256','lf_sha256','bytes']),(n,item,actual)
   snap=O/f'input.{n:02}.raw.snapshot'; assert not snap.exists(); snap.write_bytes(p.read_bytes()); rows.append(dict(original=actual,snapshot=d(snap)))
  put(O/'lease.json',dict(actor=V,advance_id=f['advance_id'],status='OPEN',read='OPEN',write='OPEN',compiler='OPEN',python='OPEN',checked_base_commit=head(),scope='Whole mathematics only; no decoder/source verdict access, canonical writes or transitions.',initial_exposure='Initial math-freeze/production/Test read before this owned freeze; all 44 current hashes exactly rechecked.'))
  put(O/'initial-input-bindings.json',dict(root_freeze=d(R/'math-freeze.json'),count=len(rows),inputs=rows,checked_base_commit=head()))
  print('FROZEN',len(rows),flush=True)
 elif mode=='compile':
  env=dict(os.environ,PYTHONUTF8='1',LEAN_NUM_THREADS='2',ELAN_TOOLCHAIN='leanprover/lean4:v4.33.0')
  commands=[('focused',['lake','build','Tests.GaussianCompactProductLogSobolev'],None),('production',['lake','env','lean','AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/GaussianCompactProductLogSobolev.lean'],None),('test-axioms',['lake','env','lean','Tests/GaussianCompactProductLogSobolev.lean'],None),('stress',['lake','env','lean','--stdin'],(O/'stress.stdin.txt').read_bytes())]
  rows=[]
  for label,cmd,stdin in commands:
   p=O/f'{label}.log'; assert not p.exists()
   with p.open('wb') as out: code=subprocess.run(cmd,input=stdin,env=env,cwd=ROOT,stdout=out,stderr=subprocess.STDOUT).returncode
   st=put(O/f'{label}.status.json',dict(command=cmd,exit_code=code,compiler='CLOSED',stdin_source=d(O/'stress.stdin.txt') if stdin else None,completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()))
   rows.append(dict(label=label,command=cmd,exit_code=code,log=d(p),status=st)); print(label,code,flush=True)
   if code:break
  put(O/'compiler-checks.json',dict(checks=rows,compiler='CLOSED'))
