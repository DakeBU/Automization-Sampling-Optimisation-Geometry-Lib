from pathlib import Path
import os, subprocess, json, hashlib, datetime
root=Path('E:/Samplinglib')
out=root/'runs/20261007-companion-priority/balanced-rademacher-clt/whole-proof-review'
env=os.environ.copy()
env.update(LEAN_NUM_THREADS='2',ELAN_TOOLCHAIN='leanprover/lean4:v4.33.0',PYTHONUTF8='1')
checks=[('focused',['lake','build','AutoSamplingTheory.TechnicalLemmas.Probability.BalancedRademacherCLT','Tests.BalancedRademacherCLT']),
        ('direct-test-axioms',['lake','env','lean','Tests/BalancedRademacherCLT.lean'])]
for name,cmd in checks:
    start=datetime.datetime.utcnow().isoformat()+'Z'
    result=subprocess.run(cmd,cwd=root,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    log=out/(name+'.log')
    with log.open('xb') as f:f.write(result.stdout)
    b=result.stdout
    receipt={'actor':'gaussian_domain_preproof_reviewer_29','command':cmd,'cwd':str(root),
       'environment':{k:env[k] for k in ['LEAN_NUM_THREADS','ELAN_TOOLCHAIN','PYTHONUTF8']},
       'exit_code':result.returncode,'status':'PASS' if result.returncode==0 else 'FAIL',
       'started_utc':start,'finished_utc':datetime.datetime.utcnow().isoformat()+'Z',
       'log_raw_sha256':hashlib.sha256(b).hexdigest(),
       'log_lf_sha256':hashlib.sha256(b.replace(b'\r\n',b'\n').replace(b'\r',b'\n')).hexdigest(),
       'compiler_mode':'exclusive foreground sequential, no production edits'}
    with (out/(name+'.status.json')).open('x',encoding='utf-8') as f:json.dump(receipt,f,indent=2)
    print(name+': '+receipt['status'],flush=True)
    print(result.stdout.decode('utf-8',errors='replace'),flush=True)
    if result.returncode:
        raise SystemExit(result.returncode)
