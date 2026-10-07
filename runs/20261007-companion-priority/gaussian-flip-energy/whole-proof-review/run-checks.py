from pathlib import Path
import json,hashlib,subprocess,os,datetime
R=Path('runs/20261007-companion-priority/gaussian-flip-energy');O=R/'whole-proof-review';V='picard_commit_verifier_20261005'
def j(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(b):return hashlib.sha256(b).hexdigest()
def d(p):
 b=Path(p).read_bytes();return {'path':Path(p).as_posix(),'raw_sha256':sha(b),'lf_sha256':sha(b.replace(b'\r\n',b'\n')),'bytes':len(b)}
def put(p,x):assert not p.exists();p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode())
C=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();assert C=='5db83cc4b880531c88cb87efe573824458a30bdd'
put(O/'lease.open.json',{'status':'OPEN','actor':V,'base':C,'read':'OPEN','write':'Own whole-proof-review only','compiler':'EXCLUSIVE_FOREGROUND','Python':'OPEN','decoder_source_verdict_access':False})
freeze=j(R/'math-freeze.json');assert len(freeze['inputs'])==27;rows=[]
for i,row in enumerate(freeze['inputs']):
 x=d(row['path']);assert x['raw_sha256']==row['raw_sha256'] and x['lf_sha256']==row['lf_sha256']
 a=O/f'input.{i:03}.raw.snapshot';b=O/f'input.{i:03}.lf.snapshot';assert not a.exists();a.write_bytes(Path(row['path']).read_bytes());b.write_bytes(Path(row['path']).read_bytes().replace(b'\r\n',b'\n'))
 rows.append(dict(x,raw_snapshot=a.as_posix(),lf_snapshot=b.as_posix()))
put(O/'input-bindings.initial.json',{'actor':V,'checked_base_commit':C,'original_frozen_inputs':27,'inputs':rows,'new_source_decoder_or_source_fidelity_verdict_read':False})
env=dict(os.environ,PYTHONUTF8='1',LEAN_NUM_THREADS='2',ELAN_TOOLCHAIN='leanprover/lean4:v4.33.0')
results=[]
commands=[('focused',['lake','build','Tests.GaussianFlipEnergy']),('direct-axioms',['lake','env','lean','Tests/GaussianFlipEnergy.lean']),('stress',['lake','env','lean',(O/'stress.lean').as_posix()])]
for name,cmd in commands:
 log=O/(name+'.log');assert not log.exists()
 with log.open('wb') as f:rc=subprocess.run(cmd,env=env,stdout=f,stderr=subprocess.STDOUT).returncode
 row={'command':cmd,'exit_code':rc,'log':d(log)};put(O/(name+'.status.json'),row);results.append(row);print(name,rc,flush=True)
 if rc:break
put(O/'fresh-checks.json',{'actor':V,'checked_base_commit':C,'results':results,'compiler':'CLOSED','foreground_serialized':True,'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
