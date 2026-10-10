from pathlib import Path
import hashlib, json, os, subprocess, sys, datetime
r=Path('runs/20261007-companion-priority/pbps-actual-nonaccumulation78')
label=sys.argv[1]; d=r/label; d.mkdir(exist_ok=False)
f=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualNonaccumulation.lean')
b=f.read_bytes(); (d/'candidate.exactraw.lean').write_bytes(b)
env=os.environ.copy(); fixed=str(Path('.astis/toolchain/lean-4.33.0-windows/bin').resolve()); env['PATH']=fixed+os.pathsep+env['PATH']; env.pop('ELAN_TOOLCHAIN',None); env['PYTHONUTF8']='1'
cmd=[str(Path(fixed)/'lake.exe'),'build','AutoSamplingTheory.ExampleCases.ProximalBPS.ActualNonaccumulation']
with (d/'stdout.log').open('wb') as out,(d/'stderr.log').open('wb') as err:
    p=subprocess.Popen(cmd,stdout=out,stderr=err,env=env); code=p.wait()
(d/'receipt.json').write_text(json.dumps(dict(command=cmd,actual_PID=p.pid,exit_code=code,terminal_closed=True,source_RAW_sha256=hashlib.sha256(b).hexdigest(),utc=datetime.datetime.now(datetime.timezone.utc).isoformat()),indent=2)+'\n',encoding='utf8')
print('focused',label,'exit',code)
print((d/'stdout.log').read_text(encoding='utf8')[-13000:])
sys.exit(code)
