from pathlib import Path
import sys,subprocess,os,datetime,json,hashlib
r=Path('runs/20261007-companion-priority/pbps-actual-physical-time-cover79');out=r/('focused79-attempt'+sys.argv[1]);out.mkdir(exist_ok=False)
env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf8');env.pop('ELAN_TOOLCHAIN',None);env['PATH']=str(Path('.astis/toolchain/lean-4.33.0-windows/bin').resolve())+os.pathsep+env['PATH']
cmd=[str(Path('.astis/toolchain/lean-4.33.0-windows/bin/lake.exe').resolve()),'build','AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhysicalTimeCover']
with (out/'stdout.log').open('wb') as stdout,(out/'stderr.log').open('wb') as stderr:
 p=subprocess.Popen(cmd,env=env,stdout=stdout,stderr=stderr);print('Foreground PID',p.pid,flush=True);code=p.wait()
f=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPhysicalTimeCover.lean');raw=f.read_bytes()
(out/'receipt.json').write_text(json.dumps(dict(command=cmd,actual_PID=p.pid,exit_code=code,terminal_closed=True,module_RAW_sha256=hashlib.sha256(raw).hexdigest(),utc=datetime.datetime.now(datetime.timezone.utc).isoformat()),indent=2)+'\n',encoding='utf8',newline='\n');(out/'module.exactraw.snapshot.lean').write_bytes(raw)
print((out/'stdout.log').read_text(encoding='utf8',errors='replace')[-7000:]);print((out/'stderr.log').read_text(encoding='utf8',errors='replace')[-2000:]);raise SystemExit(code)
