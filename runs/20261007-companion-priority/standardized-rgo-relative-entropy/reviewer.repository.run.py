from pathlib import Path
import subprocess,os,json,hashlib,datetime
R=Path('runs/20261007-companion-priority/standardized-rgo-relative-entropy')
C='171acfcefee8fee3f2858e8550d3c4b393f7a10c';V='picard_commit_verifier_20261005'
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==C
assert not (R/'reviewer.repository.gates.json').exists()
def w(p,x):Path(p).write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode())
def sha(b):return hashlib.sha256(b).hexdigest()
w(R/'reviewer.repository.lease.open.json',{'status':'OPEN','checked_commit':C,'verifier_id':V,'compiler':'EXCLUSIVE_FOREGROUND','Python':'OPEN','read':'current33 exact integration and matching prior independent proof evidence','write':'own reviewer.repository files only','canonical_read_only':True})
env=dict(os.environ,PYTHONUTF8='1',LEAN_NUM_THREADS='2',ELAN_TOOLCHAIN='leanprover/lean4:v4.33.0')
py='C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
commands=[('aggregate',[py,'tools/astis.py','check']),('publication',[py,'tools/astis_publication.py','check','--base','origin/main']),('semantic',[py,'tools/astis_semantic_roundtrip.py','check']),('frontier',[py,'tools/astis_frontier_cells.py','check']),('process-memory',[py,'tools/astis_process_memory.py','check']),('contributor',[py,'tools/astis_contributor_contract.py','check','--base','origin/main']),('graph',[py,'tools/astis_publication.py','graph-check','--cell','ASTIS-SW-SPHMC-standardized-rgo-relative-entropy'])]
results=[]
for name,cmd in commands:
 p=R/('reviewer.repository.'+name+'.log')
 with p.open('wb') as f:q=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,env=env)
 b=p.read_bytes();results.append({'name':name,'command':cmd,'returncode':q.returncode,'path':p.as_posix(),'raw_sha256':sha(b),'lf_sha256':sha(b.replace(b'\r\n',b'\n'))})
 print(name,q.returncode,flush=True)
 if q.returncode:break
w(R/'reviewer.repository.gates.json',{'checked_commit':C,'verifier_id':V,'results':results,'serialized_foreground':True,'compiler':'CLOSED','completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
