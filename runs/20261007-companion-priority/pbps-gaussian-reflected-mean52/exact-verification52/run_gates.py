import os,sys,pathlib,json,hashlib,subprocess,shutil
from datetime import datetime,timezone
from concurrent.futures import ThreadPoolExecutor
ROOT=pathlib.Path('E:/Samplinglib');OUT=ROOT/'runs/20261007-companion-priority/pbps-gaussian-reflected-mean52/exact-verification52';COMMIT='a18cd1cf8e8310f228391d4c53a2ac8f1a8900ec'
def now():return datetime.now(timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
 b=p.read_bytes();return {'path':p.relative_to(ROOT).as_posix(),'raw_sha256':sha(b),'lf_sha256':sha(b.replace(b'\r\n',b'\n')),'bytes':len(b)}
def write(p,o):p.write_text(json.dumps(o,sort_keys=True,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
env=os.environ.copy();old=env.pop('ELAN_TOOLCHAIN',None);env['LEAN_NUM_THREADS']='2';env['PYTHONUTF8']='1'
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip()==COMMIT
assert (ROOT/'lean-toolchain').read_text().strip()=='leanprover/lean4:v4.33.0'
assert subprocess.check_output(['git','-C','.lake/packages/mathlib','rev-parse','HEAD'],cwd=ROOT).decode().strip()=='db584cd6d46c92f209a44c0f1c829460d327499d'
lake=shutil.which('lake')
def run(label,cmd):
 opened=now()
 with (OUT/(label+'.log')).open('wb') as f:
  p=subprocess.Popen(cmd,cwd=ROOT,env=env,stdout=f,stderr=subprocess.STDOUT)
  lease={'status':'OPEN','opened_utc':opened,'process_id':p.pid,'Python_pid':os.getpid(),'command':cmd,'checked_commit':COMMIT,'ELAN_TOOLCHAIN_unset':True,'inherited_override_was_set':old is not None,'LEAN_NUM_THREADS':'2','PYTHONUTF8':'1'}
  write(OUT/(label+'.lease.json'),lease);rc=p.wait()
 status={'command':cmd,'process_id':p.pid,'Python_pid':os.getpid(),'checked_commit':COMMIT,'exit_code':rc,'opened_utc':opened,'finished_utc':now(),'log':pin(OUT/(label+'.log')),'source_inputs':[pin(ROOT/'AutoSamplingTheory/TechnicalLemmas/Measure/GaussianReflectedMean.lean'),pin(ROOT/'Tests/ProximalBPSGaussianReflectedMean.lean')],'toolchain':pin(ROOT/'lean-toolchain'),'manifest':pin(ROOT/'lake-manifest.json'),'ELAN_TOOLCHAIN_unset':True,'LEAN_NUM_THREADS':'2','PYTHONUTF8':'1'}
 write(OUT/(label+'.status.json'),status)
 lease.update(status='CLOSED',closed_utc=now(),exit_code=rc,Python='CLOSED',compiler='CLOSED' if label=='focused' else 'NOT_STARTED_CLOSED')
 write(OUT/(label+'.lease.json'),lease)
 print(json.dumps({'label':label,'pid':p.pid,'exit_code':rc,'log_sha256':status['log']['raw_sha256']}),flush=True)
 return status
version=run('toolchain-version',[lake,'env','lean','--version']);assert version['exit_code']==0 and '4.33.0' in (OUT/'toolchain-version.log').read_text()
focused=run('focused',[lake,'build','Tests.ProximalBPSGaussianReflectedMean']);assert focused['exit_code']==0
gates=[('publication',[sys.executable,'tools/astis_publication.py','check','--base','origin/main']),('semantic',[sys.executable,'tools/astis_semantic_roundtrip.py','check']),('frontier',[sys.executable,'tools/astis_frontier_cells.py','check']),('contributor',[sys.executable,'tools/astis_contributor_contract.py','check','--base','origin/main'])]
with ThreadPoolExecutor(max_workers=4) as pool:results=list(pool.map(lambda args:run(*args),gates))
write(OUT/'gate-summary.json',{'commit':COMMIT,'focused':focused,'noncompiler_gates':results,'all_pass':all(r['exit_code']==0 for r in results)})
assert all(r['exit_code']==0 for r in results),'A gate failed; inspect exact logs before VERIFIED'
