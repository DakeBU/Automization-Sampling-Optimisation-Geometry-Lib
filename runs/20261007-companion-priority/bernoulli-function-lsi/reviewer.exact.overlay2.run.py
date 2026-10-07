from pathlib import Path
import json,os,subprocess,hashlib,datetime
R=Path('runs/20261007-companion-priority/bernoulli-function-lsi');C='6d5df34cdb124e28022f16f566ff549145eb7e65'
def w(p,d):Path(p).write_bytes((json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode())
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==C
w(R/'reviewer.exact.overlay2.lease.json',{'status':'OPEN','checked_commit':C,'verifier_id':'picard_commit_verifier_20261005','compiler':'EXCLUSIVE_FOREGROUND','read':'OPEN','write':'own scoped verifier outputs and VERIFIED append only if warranted','Python':'OPEN'})
env=dict(os.environ,PYTHONUTF8='1',LEAN_NUM_THREADS='2',ELAN_TOOLCHAIN='leanprover/lean4:v4.33.0');py='C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
commands=[('aggregate',[py,'tools/astis.py','check']),('publication',[py,'tools/astis_publication.py','check','--base','origin/main']),('semantic',[py,'tools/astis_semantic_roundtrip.py','check']),('frontier',[py,'tools/astis_frontier_cells.py','check']),('process-memory',[py,'tools/astis_process_memory.py','check'])]
rows=[]
for name,cmd in commands:
 p=R/('reviewer.exact.overlay2.'+name+'.log')
 with p.open('wb') as f:q=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,env=env)
 b=p.read_bytes();rows.append({'name':name,'command':cmd,'returncode':q.returncode,'path':p.as_posix(),'raw_sha256':hashlib.sha256(b).hexdigest(),'lf_sha256':hashlib.sha256(b.replace(b'\r\n',b'\n')).hexdigest()});print(name,q.returncode,flush=True)
w(R/'reviewer.exact.overlay2.gates.json',{'checked_commit':C,'verifier_id':'picard_commit_verifier_20261005','results':rows,'compiler':'CLOSED','foreground_serialized':True,'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
