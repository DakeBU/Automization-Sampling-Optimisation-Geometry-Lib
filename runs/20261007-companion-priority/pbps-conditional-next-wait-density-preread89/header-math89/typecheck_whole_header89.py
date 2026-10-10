from pathlib import Path
import hashlib, json, os, subprocess, time
from datetime import datetime, timezone
R=Path('E:/Samplinglib')
D=R/'runs/20261007-companion-priority/pbps-conditional-next-wait-density-preread89/header-math89'
def pin(p):
 b=Path(p).read_bytes(); return {'path':Path(p).as_posix(),'raw_sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def write(name,v):
 p=D/name;assert not p.exists(),p
 with p.open('x',encoding='utf8',newline='\n') as f:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
 return pin(p)
h=D.parent/'header89.proposed.lean'
assert pin(h)['raw_sha256']=='b569fe4a45e669f85f2d57e5c7ed6089c736e4bb0433ef34781d02e2e5dc735d'
assert pin(R/'lean-toolchain')['raw_sha256']=='b2b5068d5a4835675e651ce83b29c0ddb308d28b80076e7c007aef4630af0477'
assert pin(R/'lake-manifest.json')['raw_sha256']=='b1f16b43aaf4a886cfe0382d5e3ae63d6904281c00afd8f35af20f0270a747e2'
snap=D/'header89.original.exactraw.lean';assert not snap.exists();snap.write_bytes(h.read_bytes())
inputs=[pin(h),pin(snap),pin(R/'lean-toolchain'),pin(R/'lake-manifest.json')]
write('header89.typecheck.inputs.json',{'checked_workspace_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),'raw_inputs':inputs,'whole_named_private_Prop':True,'overlay':None,'theorem_BODY':False})
env=os.environ.copy();env['PYTHONUTF8']='1';env['PATH']=str(R/'.astis/toolchain/lean-4.33.0-windows/bin')+os.pathsep+env.get('PATH','')
cmd=[str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'),'env','lean',str(snap)]
started=datetime.now(timezone.utc).isoformat();t=time.monotonic()
with (D/'header89.whole-typecheck.log').open('xb') as log:
 p=subprocess.run(cmd,cwd=R,env=env,stdout=log,stderr=subprocess.STDOUT)
receipt=write('header89.whole-typecheck.receipt.json',{'command':cmd,'cwd':R.as_posix(),'started_utc':started,'completed_utc':datetime.now(timezone.utc).isoformat(),'elapsed_seconds':time.monotonic()-t,'exit_code':p.returncode,'foreground':True,'raw_inputs':inputs,'native_log':pin(D/'header89.whole-typecheck.log'),'scope':'Complete unmodified named private Prop plus its original #check. No theorem BODY, placeholder or proof credit.'})
print(json.dumps({'receipt':receipt,'exit_code':p.returncode,'log':pin(D/'header89.whole-typecheck.log')}))
raise SystemExit(p.returncode)
