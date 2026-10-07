from pathlib import Path
import subprocess,os,json,hashlib,datetime
R=Path('runs/20261007-companion-priority/standardized-rgo-relative-entropy')
C='3f01c4be14739067fc458033a74fa3937367fa61'
V='picard_commit_verifier_20261005'
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==C
assert not (R/'reviewer.exact.gates.json').exists()
def write(p,x):Path(p).write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode())
def sha(b):return hashlib.sha256(b).hexdigest()
write(R/'reviewer.exact.lease.open.json',{'status':'OPEN','checked_commit':C,'verifier_id':V,'compiler':'EXCLUSIVE_FOREGROUND','Python':'OPEN','read':'packet33 and actual pinned parents only','write':'owned reviewer.exact evidence plus authorized VERIFIED append only if genuine passes','canonical_math_read_only':True,'root_sole_STABILIZING_preserved':True})
env=dict(os.environ,PYTHONUTF8='1',LEAN_NUM_THREADS='2',ELAN_TOOLCHAIN='leanprover/lean4:v4.33.0')
py='C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
commands=[('focused',['lake','build','Tests.StandardizedRGORelativeEntropy']),('aggregate',[py,'tools/astis.py','check']),('publication',[py,'tools/astis_publication.py','check','--base','origin/main']),('semantic',[py,'tools/astis_semantic_roundtrip.py','check']),('frontier',[py,'tools/astis_frontier_cells.py','check']),('process-memory',[py,'tools/astis_process_memory.py','check']),('contributor',[py,'tools/astis_contributor.py','check','--base','origin/main'])]
results=[]
for name,command in commands:
 p=R/('reviewer.exact.'+name+'.log')
 with p.open('wb') as f:q=subprocess.run(command,stdout=f,stderr=subprocess.STDOUT,env=env)
 b=p.read_bytes();results.append({'name':name,'command':command,'returncode':q.returncode,'path':p.as_posix(),'raw_sha256':sha(b),'lf_sha256':sha(b.replace(b'\r\n',b'\n'))})
 print(name,q.returncode,flush=True)
 if q.returncode:break
write(R/'reviewer.exact.gates.json',{'checked_commit':C,'verifier_id':V,'results':results,'foreground_serialized':True,'LEAN_NUM_THREADS':2,'compiler':'CLOSED','completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
