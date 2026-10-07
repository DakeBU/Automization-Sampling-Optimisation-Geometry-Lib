exec(open('runs/20261007-companion-priority/gaussian-product-entropy/whole-proof-review/freeze.py',encoding='utf-8').read().split('freeze=j(')[0])
import os,datetime
env=dict(os.environ,PYTHONUTF8='1',LEAN_NUM_THREADS='2',ELAN_TOOLCHAIN='leanprover/lean4:v4.33.0')
commands=[('focused',['lake','build','Tests.ProductEntropy'],None),('production',['lake','env','lean','AutoSamplingTheory/TechnicalLemmas/InformationTheory/ProductEntropy.lean'],None),('direct-axioms',['lake','env','lean','Tests/ProductEntropy.lean'],None),('stress',['lake','env','lean','--stdin'],(O/'stress.stdin.txt').read_bytes())]
rows=[]
for label,cmd,input in commands:
 p=O/f'{label}.log';assert not p.exists()
 with p.open('wb') as f:code=subprocess.run(cmd,input=input,env=env,stdout=f,stderr=subprocess.STDOUT).returncode
 st=put(O/f'{label}.status.json',dict(command=cmd,exit_code=code,compiler='CLOSED',stdin_source=d(O/'stress.stdin.txt') if input else None,completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()))
 rows.append(dict(label=label,command=cmd,exit_code=code,log=d(p),status=st));print(label,code,flush=True)
 if code:break
put(O/'compiler-checks.json',dict(checks=rows,compiler='CLOSED'))
