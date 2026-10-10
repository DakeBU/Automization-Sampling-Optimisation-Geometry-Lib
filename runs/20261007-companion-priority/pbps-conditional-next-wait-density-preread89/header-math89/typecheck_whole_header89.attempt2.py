from pathlib import Path
import hashlib, json, os, subprocess, time, difflib
from datetime import datetime, timezone
R=Path('E:/Samplinglib');D=R/'runs/20261007-companion-priority/pbps-conditional-next-wait-density-preread89/header-math89'
def pin(p):
 b=Path(p).read_bytes();return {'path':Path(p).as_posix(),'raw_sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def write(name,v):
 p=D/name;assert not p.exists(),p
 with p.open('x',encoding='utf8',newline='\n') as f:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
 return pin(p)
old=D.parent/'header89.proposed.v1.exactraw.snapshot.lean';new=D.parent/'header89.proposed.lean'
assert pin(old)['raw_sha256']=='b569fe4a45e669f85f2d57e5c7ed6089c736e4bb0433ef34781d02e2e5dc735d'
assert pin(new)['raw_sha256']=='47bb14ee9e720d22ddefa4645860d1fcd6a984cfaf2f64085e41eea1ccc9a696'
ob,nb=old.read_bytes(),new.read_bytes()
oldline='              ∫⁻ h in A, ∫⁻ s : ℝ, F (h, s) * D h s ∂μ'.encode()
newline='              ∫⁻ h in A, (∫⁻ s : ℝ, F (h, s) * D h s) ∂μ'.encode()
assert ob.count(oldline)==1 and ob.replace(oldline,newline)==nb
write('header89.syntax-successor.delta.json',{'v1':pin(old),'v2':pin(new),'delta':'Exactly two parentheses grouping the inner real Lebesgue lintegral; outer restriction uses mu. No binder/definition/semantic mathematical target edit.','mathematical_intended_target_unchanged':True,'author_proposal_reviewed_by_independent_reviewer':'/root/exact_verify77'})
write('header89.launcher-guard.negative.json',{'tool_chunk':'1e879b','exit_code':1,'Lean_started':False,'script':pin(D/'typecheck_whole_header89.py'),'cause':'Original expected b569fe V1 no longer current after root pre-seal syntax-only successor. RAW guard stopped before creating snapshot or invoking Lean. Preserve original launcher.','original_header_read_chunk':'d42173','original_header_read_raw':pin(old),'successor_header':pin(new)})
for p,h in ((R/'lean-toolchain','b2b5068d5a4835675e651ce83b29c0ddb308d28b80076e7c007aef4630af0477'),(R/'lake-manifest.json','b1f16b43aaf4a886cfe0382d5e3ae63d6904281c00afd8f35af20f0270a747e2')): assert pin(p)['raw_sha256']==h
env=os.environ.copy();env['PYTHONUTF8']='1';env['PATH']=str(R/'.astis/toolchain/lean-4.33.0-windows/bin')+os.pathsep+env.get('PATH','')
results=[]
for variant,source in [('v1-negative',old),('v2-current',new)]:
 snap=D/('header89.'+variant+'.exactraw.lean');assert not snap.exists();snap.write_bytes(source.read_bytes())
 inputs=[pin(source),pin(snap),pin(R/'lean-toolchain'),pin(R/'lake-manifest.json')]
 cmd=[str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'),'env','lean',str(snap)]
 started=datetime.now(timezone.utc).isoformat();t=time.monotonic()
 logpath=D/('header89.'+variant+'.whole-typecheck.log')
 with logpath.open('xb') as log:p=subprocess.run(cmd,cwd=R,env=env,stdout=log,stderr=subprocess.STDOUT)
 receipt=write('header89.'+variant+'.whole-typecheck.receipt.json',{'command':cmd,'cwd':R.as_posix(),'started_utc':started,'completed_utc':datetime.now(timezone.utc).isoformat(),'elapsed_seconds':time.monotonic()-t,'exit_code':p.returncode,'foreground':True,'raw_inputs':inputs,'native_log':pin(logpath),'scope':'Complete unmodified named private Prop plus original #check; no theorem BODY, placeholders or proof credit.'})
 results.append({'variant':variant,'receipt':receipt,'exit_code':p.returncode,'log':pin(logpath)})
 print(json.dumps(results[-1]),flush=True)
assert results[0]['exit_code']!=0,'V1 negative unexpectedly accepted; inspect before proceeding'
assert results[1]['exit_code']==0,'V2 current failed; no acceptance'
