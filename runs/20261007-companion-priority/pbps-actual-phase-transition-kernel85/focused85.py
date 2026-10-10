from pathlib import Path
import hashlib,json,os,subprocess,sys
r=Path(__file__).parent;out=r/('focused85-attempt'+sys.argv[1]);out.mkdir(exist_ok=False)
p=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPhaseTransitionKernel.lean')
(out/'module.before.lean').write_bytes(p.read_bytes())
env=os.environ.copy();env.pop('ELAN_TOOLCHAIN',None);env['PYTHONUTF8']='1'
bin=Path('.astis/toolchain/lean-4.33.0-windows/bin').resolve();env['PATH']=str(bin)+os.pathsep+env['PATH']
command=[str(bin/'lake.exe'),'build','AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhaseTransitionKernel']
with (out/'stdout.log').open('wb') as stdout,(out/'stderr.log').open('wb') as stderr:
 q=subprocess.Popen(command,env=env,stdout=stdout,stderr=stderr);print('Foreground PID',q.pid,flush=True);code=q.wait()
receipt=dict(exit_code=code,terminal_closed=True,actual_PID=q.pid,command=command,source_RAW_sha256=hashlib.sha256(p.read_bytes()).hexdigest())
for label in ['stdout','stderr']:
 raw=(out/(label+'.log')).read_bytes();receipt[label]=dict(path=(out/(label+'.log')).as_posix(),RAW_sha256=hashlib.sha256(raw).hexdigest(),RAW_bytes=len(raw))
(out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf8',newline='\n')
print('Focused EXIT',code,flush=True)
if code:print((out/'stdout.log').read_text(encoding='utf8',errors='replace')[-10000:]);print((out/'stderr.log').read_text(encoding='utf8',errors='replace')[-3000:])
raise SystemExit(code)
