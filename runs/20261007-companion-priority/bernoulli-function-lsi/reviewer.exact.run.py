from pathlib import Path
import subprocess,os,json,hashlib,datetime
R=Path('runs/20261007-companion-priority/bernoulli-function-lsi');C='a83ce789bd4f3ce22c3757129282c9ad488c2ccf';V='picard_commit_verifier_20261005'
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==C
assert not (R/'reviewer.exact.gates.json').exists()
def w(p,x):Path(p).write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode())
def sha(b):return hashlib.sha256(b).hexdigest()
w(R/'reviewer.exact.lease.open.json',{'status':'OPEN','checked_commit':C,'verifier_id':V,'compiler':'EXCLUSIVE_FOREGROUND','Python':'OPEN','read':'current34 exact mathematical/source scope only','write':'own reviewer.exact evidence, verified.json and authoritative VERIFIED append only if true checks pass','canonical_read_only':True})
env=dict(os.environ,PYTHONUTF8='1',LEAN_NUM_THREADS='2',ELAN_TOOLCHAIN='leanprover/lean4:v4.33.0');py='C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
cmds=[('focused',['lake','build','AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.TwoPointEntropy','AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.BernoulliLogSobolev','Tests.BernoulliLogSobolev']),('direct-axioms',['lake','env','lean','Tests/BernoulliLogSobolev.lean']),('aggregate',[py,'tools/astis.py','check']),('publication',[py,'tools/astis_publication.py','check','--base','origin/main']),('semantic',[py,'tools/astis_semantic_roundtrip.py','check']),('frontier',[py,'tools/astis_frontier_cells.py','check']),('process-memory',[py,'tools/astis_process_memory.py','check']),('contributor',[py,'tools/astis_contributor_contract.py','check','--base','origin/main'])]
results=[]
for name,cmd in cmds:
 p=R/('reviewer.exact.'+name+'.log')
 with p.open('wb') as f:q=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,env=env)
 b=p.read_bytes();results.append({'name':name,'command':cmd,'returncode':q.returncode,'path':p.as_posix(),'raw_sha256':sha(b),'lf_sha256':sha(b.replace(b'\r\n',b'\n'))})
 print(name,q.returncode,flush=True)
 if q.returncode:break
w(R/'reviewer.exact.gates.json',{'checked_commit':C,'verifier_id':V,'results':results,'foreground_serialized':True,'compiler':'CLOSED','completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
