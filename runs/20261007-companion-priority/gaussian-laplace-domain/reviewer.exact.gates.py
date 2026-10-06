import os,subprocess,json,hashlib
from pathlib import Path
R=Path('runs/20261007-companion-priority/gaussian-laplace-domain')
P='C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
env=os.environ.copy();env.update(PYTHONUTF8='1',ELAN_TOOLCHAIN='leanprover/lean4:v4.33.0',LEAN_NUM_THREADS='2')
commands=[('focused',['lake','build','Tests.GaussianLipschitzExponential','Tests.FullRangeProximalGaussianOracle','Tests.StandardizedRGOPositionFisher']),('publication',[P,'tools/astis_publication.py','check','--base','origin/main']),('semantic',[P,'tools/astis_semantic_roundtrip.py','check']),('frontier',[P,'tools/astis_frontier_cells.py','check']),('contributor',[P,'tools/astis_contributor_contract.py','check','--base','origin/main'])]
results=[]
for label,command in commands:
 path=R/f'reviewer.exact.{label}.log';assert not path.exists()
 with path.open('wb') as out: done=subprocess.run(command,env=env,stdout=out,stderr=subprocess.STDOUT)
 b=path.read_bytes();result=dict(name=label,command=command,exit_code=done.returncode,path=str(path).replace('\\','/'),raw_sha256=hashlib.sha256(b).hexdigest(),lf_sha256=hashlib.sha256(b.replace(b'\r\n',b'\n')).hexdigest(),bytes=len(b));results.append(result)
 print(json.dumps(result),flush=True)
 if done.returncode:break
out=R/'reviewer.exact.gate-results.json';assert not out.exists()
out.write_bytes((json.dumps(results,indent=2)+'\n').encode())
