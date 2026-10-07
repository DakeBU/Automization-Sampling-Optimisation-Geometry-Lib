from pathlib import Path
import subprocess,os,json,hashlib,datetime
R=Path('runs/20261007-companion-priority/balanced-rademacher-clt');C='4d9e71a6b835b54453a5cfd2d132f9a51f66f69c';V='picard_commit_verifier_20261005'
def w(p,d):Path(p).write_bytes((json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode())
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==C
assert not (R/'reviewer.exact.gates.json').exists()
w(R/'reviewer.exact.lease.json',{'status':'OPEN','checked_commit':C,'verifier_id':V,'read':'OPEN','write':'Own exact34/35 receipts + independent ledger transition if gates pass','compiler':'EXCLUSIVE_FOREGROUND','Python':'OPEN','canonical_mutations':False})
env=dict(os.environ,PYTHONUTF8='1',LEAN_NUM_THREADS='2',ELAN_TOOLCHAIN='leanprover/lean4:v4.33.0');py='C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
commands=[('focused',['lake','build','AutoSamplingTheory.TechnicalLemmas.Probability.BalancedRademacherCLT','Tests.BalancedRademacherCLT']),('direct-axioms',['lake','env','lean','Tests/BalancedRademacherCLT.lean']),('aggregate',[py,'tools/astis.py','check']),('publication',[py,'tools/astis_publication.py','check','--base','origin/main']),('semantic',[py,'tools/astis_semantic_roundtrip.py','check']),('frontier',[py,'tools/astis_frontier_cells.py','check']),('process-memory',[py,'tools/astis_process_memory.py','check']),('contributor',[py,'tools/astis_contributor_contract.py','check','--base','origin/main'])]
rows=[]
for name,cmd in commands:
 p=R/('reviewer.exact.'+name+'.log')
 with p.open('wb') as f:q=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,env=env)
 b=p.read_bytes();rows.append({'name':name,'command':cmd,'returncode':q.returncode,'path':p.as_posix(),'raw_sha256':hashlib.sha256(b).hexdigest(),'lf_sha256':hashlib.sha256(b.replace(b'\r\n',b'\n')).hexdigest()});print(name,q.returncode,flush=True)
 if q.returncode:break
w(R/'reviewer.exact.gates.json',{'checked_commit':C,'verifier_id':V,'results':rows,'compiler':'CLOSED','foreground_serialized':True,'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
