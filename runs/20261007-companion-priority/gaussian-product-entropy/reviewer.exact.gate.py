from pathlib import Path
import os,json,hashlib,subprocess,datetime
R=Path('runs/20261007-companion-priority/gaussian-product-entropy');C='913438726472dcac2483cefbe6b4b2f4746cbe74';V='picard_commit_verifier_20261005'
PY='C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
def j(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(b):return hashlib.sha256(b).hexdigest()
def d(p):
 b=Path(p).read_bytes();return dict(path=Path(p).as_posix(),raw_sha256=sha(b),lf_sha256=sha(b.replace(b'\r\n',b'\n')),bytes=len(b))
def put(p,x):
 assert not p.exists(),p
 p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode());return d(p)
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==C
put(R/'reviewer.exact.lease.json',dict(status='OPEN',verifier_id=V,checked_commit=C,read='OPEN',write='OPEN own verifier outputs and independent ledger transition only',compiler='EXCLUSIVE_FOREGROUND',Python='OPEN',excluded_untracked_scope='gaussian-compact-product-preread future source-only folder; no proof credit'))
env=dict(os.environ,PYTHONUTF8='1',LEAN_NUM_THREADS='2',ELAN_TOOLCHAIN='leanprover/lean4:v4.33.0')
commands=[('focused',['lake','build','Tests.ProductEntropy']),('direct-axioms',['lake','env','lean','Tests/ProductEntropy.lean']),('mandatory',[PY,'tools/astis.py','check']),('publication',[PY,'tools/astis_publication.py','check','--base','origin/main']),('semantic',[PY,'tools/astis_semantic_roundtrip.py','check']),('frontier',[PY,'tools/astis_frontier_cells.py','check']),('process',[PY,'tools/astis_process_memory.py','check']),('contributor',[PY,'tools/astis_contributor_contract.py','check','--base','origin/main'])]
rows=[]
for name,cmd in commands:
 log=R/f'reviewer.exact.{name}.log';assert not log.exists()
 with log.open('wb') as f:code=subprocess.run(cmd,env=env,stdout=f,stderr=subprocess.STDOUT).returncode
 st=put(R/f'reviewer.exact.{name}.status.json',dict(checked_commit=C,command=cmd,exit_code=code,compiler='CLOSED' if name in ['focused','direct-axioms','mandatory'] else 'not-used',completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),log=d(log)))
 rows.append(dict(label=name,command=cmd,returncode=code,**d(log),status=st));print(name,code,flush=True)
 if code:break
put(R/'reviewer.exact.gates.json',dict(checked_commit=C,results=rows,compiler='CLOSED',all_pass=len(rows)==len(commands) and all(x['returncode']==0 for x in rows)))
