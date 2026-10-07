from pathlib import Path
import json,subprocess,os,hashlib,datetime
R=Path('runs/20261007-companion-priority/gaussian-compact-entropy');O=R/'whole-proof-review';O.mkdir(exist_ok=True)
V='picard_commit_verifier_20261005';env=dict(os.environ,PYTHONUTF8='1',LEAN_NUM_THREADS='2',ELAN_TOOLCHAIN='leanprover/lean4:v4.33.0')
def h(b):return hashlib.sha256(b).hexdigest()
def put(name,d):
 p=O/name;assert not p.exists();p.write_bytes((json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode())
C=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();freeze=json.loads((R/'math-freeze.json').read_text(encoding='utf-8'))
assert C==freeze['checked_base_commit']=='a63df065f186e0363a5393622c242dc6b9fc1434'
assert subprocess.check_output(['git','-C','.lake/packages/mathlib','rev-parse','HEAD'],text=True).strip()=='db584cd6d46c92f209a44c0f1c829460d327499d'
rows=[]
for i,row in enumerate(freeze['inputs']):
 b=Path(row['path']).read_bytes();assert h(b)==row['raw_sha256'] and h(b.replace(b'\r\n',b'\n'))==row['lf_sha256']
 raw=O/f'input.{i:03}.raw.snapshot';lf=O/f'input.{i:03}.lf.snapshot';assert not raw.exists() and not lf.exists();raw.write_bytes(b);lf.write_bytes(b.replace(b'\r\n',b'\n'))
 rows.append({**row,'raw_snapshot':raw.as_posix(),'lf_snapshot':lf.as_posix()})
put('input-bindings.initial.json',{'actor':V,'checked_base_commit':C,'original_frozen_inputs':len(rows),'inputs':rows,'decoder_or_source_verdict_read':False})
put('lease.json',{'status':'OPEN','actor':V,'checked_base_commit':C,'read':'OPEN','write':'OPEN','compiler':'OPEN','Python':'OPEN','role':'independent whole mathematical proof review only','source_authoritative_approval':False})
checks=[]
for name,cmd in [('focused',['lake','build','Tests.GaussianCompactEntropy']),('direct-test-axioms',['lake','env','lean','Tests/GaussianCompactEntropy.lean'])]:
 p=O/(name+'.log');assert not p.exists()
 with p.open('wb') as f:code=subprocess.run(cmd,env=env,stdout=f,stderr=subprocess.STDOUT).returncode
 b=p.read_bytes();checks.append({'name':name,'command':cmd,'exit_code':code,'log':p.as_posix(),'raw_sha256':h(b),'lf_sha256':h(b.replace(b'\r\n',b'\n'))});print(name,code,flush=True)
 if code:break
put('fresh-checks.json',{'actor':V,'checked_base_commit':C,'checks':checks,'compiler':'CLOSED','completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
