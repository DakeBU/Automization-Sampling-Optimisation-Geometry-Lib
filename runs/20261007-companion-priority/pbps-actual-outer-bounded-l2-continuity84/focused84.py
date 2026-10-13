from pathlib import Path
import os,sys,subprocess,json,hashlib
r=Path('runs/20261007-companion-priority/pbps-actual-outer-bounded-l2-continuity84');out=r/sys.argv[1];out.mkdir(exist_ok=False)
f=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualOuterBoundedL2Continuity.lean')
(out/'source.snapshot.lean').write_bytes(f.read_bytes())
env=os.environ.copy();env.pop('ELAN_TOOLCHAIN',None);env['PATH']=str(Path('.astis/toolchain/lean-4.33.0-windows/bin').resolve())+os.pathsep+env['PATH'];env['PYTHONUTF8']='1'
cmd=[str(Path('.astis/toolchain/lean-4.33.0-windows/bin/lake.exe').resolve()),'build','AutoSamplingTheory.ExampleCases.ProximalBPS.ActualOuterBoundedL2Continuity']
with (out/'stdout.log').open('wb') as so,(out/'stderr.log').open('wb') as se:
 p=subprocess.Popen(cmd,stdout=so,stderr=se,env=env);code=p.wait()
(out/'receipt.json').write_text(json.dumps(dict(exit_code=code,terminal_closed=True,actual_PID=p.pid,command=cmd,source_RAW_sha256=hashlib.sha256(f.read_bytes()).hexdigest()),indent=2)+'\n')
print('terminal exit',code)
lines=(out/'stdout.log').read_text(encoding='utf8',errors='replace').splitlines()
for i,line in enumerate(lines):
 if line.startswith('error:'): print('\n'.join(lines[i:i+12]))
print('\n'.join(lines[-3:]));sys.exit(code)
