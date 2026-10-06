import json,os,subprocess,hashlib
from pathlib import Path
R=Path('runs/20261007-companion-priority/gaussian-laplace-domain')
env=os.environ.copy();env.update(PYTHONUTF8='1',ELAN_TOOLCHAIN='leanprover/lean4:v4.33.0',LEAN_NUM_THREADS='2')
jobs=[('focused',['lake','build','Tests.GaussianLipschitzExponential','Tests.FullRangeProximalGaussianOracle','Tests.StandardizedRGOPositionFisher']),
 ('production0',['lake','env','lean','AutoSamplingTheory/TechnicalLemmas/Probability/GaussianLipschitzExponential.lean']),
 ('production1',['lake','env','lean','AutoSamplingTheory/ExampleCases/SmoothedPicardHMC/FullRangeProximalGaussianOracle.lean']),
 ('stress',['lake','env','lean','--stdin'])]
records=[]
for label,cmd in jobs:
 out=R/f'reviewer.{label}.log';assert not out.exists()
 input_bytes=(R/'reviewer.stress.stdin.txt').read_bytes() if label=='stress' else None
 with out.open('wb') as log:
  result=subprocess.run(cmd,input=input_bytes,stdout=log,stderr=subprocess.STDOUT,env=env)
 records.append(dict(label=label,command=cmd,exit_code=result.returncode,log=str(out).replace('\\','/'),raw_sha256=hashlib.sha256(out.read_bytes()).hexdigest()))
 print(json.dumps(records[-1]),flush=True)
 if result.returncode:break
out=R/'reviewer.compile-results.json';assert not out.exists()
out.write_bytes((json.dumps(records,indent=2)+'\n').encode())
