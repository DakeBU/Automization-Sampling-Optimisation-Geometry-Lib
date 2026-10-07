from pathlib import Path
import subprocess,os,json,hashlib,datetime
R=Path('runs/20261007-companion-priority/bernoulli-function-lsi');C='d0b872541758537a4f42d9d3e6e8deb12b5bb028';V='picard_commit_verifier_20261005'
P='C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
env=dict(os.environ,PYTHONUTF8='1',LEAN_NUM_THREADS='2',ELAN_TOOLCHAIN='leanprover/lean4:v4.33.0')
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==C
def put(p,d):p.write_bytes((json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode())
put(R/'reviewer.repository.lease.json',{'status':'OPEN','checked_commit':C,'verifier_id':V,'read':'OPEN','write':'OPEN','compiler':'OPEN','Python':'OPEN'})
commands=[('aggregate',[P,'tools/astis.py','check']),('publication',[P,'tools/astis_publication.py','check','--base','origin/main']),('semantic',[P,'tools/astis_semantic_roundtrip.py','check']),('frontier',[P,'tools/astis_frontier_cells.py','check']),('process-memory',[P,'tools/astis_process_memory.py','check']),('contributor',[P,'tools/astis_contributor_contract.py','check','--base','origin/main'])]
results=[]
for name,cmd in commands:
 log=R/f'reviewer.repository.{name}.log';assert not log.exists()
 with log.open('wb') as f:code=subprocess.run(cmd,env=env,stdout=f,stderr=subprocess.STDOUT).returncode
 b=log.read_bytes();results.append({'name':name,'command':cmd,'returncode':code,'path':log.as_posix(),'raw_sha256':hashlib.sha256(b).hexdigest(),'lf_sha256':hashlib.sha256(b.replace(b'\r\n',b'\n')).hexdigest()});print(name,code,flush=True)
 if code:break
put(R/'reviewer.repository.gates.json',{'checked_commit':C,'verifier_id':V,'results':results,'compiler':'CLOSED','foreground_serialized':True,'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
