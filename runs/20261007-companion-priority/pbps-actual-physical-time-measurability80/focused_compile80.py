from pathlib import Path
import hashlib,json,os,subprocess,sys
r=Path('runs/20261007-companion-priority/pbps-actual-physical-time-measurability80')/('focused80-attempt'+sys.argv[1]);r.mkdir(exist_ok=False)
p=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPhysicalTimeMeasurability.lean');(r/'source.exact-snapshot.lean').write_bytes(p.read_bytes())
env=dict(os.environ);env.pop('ELAN_TOOLCHAIN',None);env['PATH']=str(Path('.astis/toolchain/lean-4.33.0-windows/bin').resolve())+os.pathsep+env['PATH']
cmd=[str(Path('.astis/toolchain/lean-4.33.0-windows/bin/lake.exe').resolve()),'build','AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhysicalTimeMeasurability']
with (r/'stdout.log').open('wb') as o,(r/'stderr.log').open('wb') as e:
 process=subprocess.Popen(cmd,env=env,stdout=o,stderr=e);print('focused80 foreground PID',process.pid,flush=True);code=process.wait()
receipt=dict(exit_code=code,terminal_closed=True,actual_PID=process.pid,command=cmd,source_RAW_sha256=hashlib.sha256(p.read_bytes()).hexdigest())
for name in ['stdout','stderr']:
 q=r/(name+'.log');receipt[name]=dict(path=q.as_posix(),RAW_sha256=hashlib.sha256(q.read_bytes()).hexdigest())
(r/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf8',newline='\n')
print('EXIT',code)
lines=(r/'stdout.log').read_text(encoding='utf8').splitlines()
for i,line in enumerate(lines):
 if line.startswith('error: AutoSamplingTheory'):print('\n'.join(lines[i:i+12]))
print('\n'.join(lines[-8:]));print((r/'stderr.log').read_text(encoding='utf8')[-1000:])
