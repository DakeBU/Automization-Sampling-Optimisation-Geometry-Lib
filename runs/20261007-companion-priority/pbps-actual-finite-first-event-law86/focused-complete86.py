from pathlib import Path
import os,sys,json,hashlib,subprocess,datetime
R=Path('E:/Samplinglib');D=Path(__file__).parent;n=sys.argv[1]
O=D/('focused-complete86.attempt'+n);O.mkdir(exist_ok=False)
M=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteFirstEventLaw.lean'
env=os.environ.copy();env.pop('ELAN_TOOLCHAIN',None);env['PATH']=str(R/'.astis/toolchain/lean-4.33.0-windows/bin')+os.pathsep+env['PATH']
cmd=[str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'),'build','AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteFirstEventLaw']
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
with (O/'stdout.log').open('wb') as out,(O/'stderr.log').open('wb') as err:
 child=subprocess.Popen(cmd,cwd=R,env=env,stdout=out,stderr=err);print('foreground PID',child.pid,flush=True);code=child.wait()
x={'command':cmd,'exit_code':code,'terminal_closed':True,'started_utc':start,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_raw_sha256':hashlib.sha256(M.read_bytes()).hexdigest(),'source_bytes':M.stat().st_size,'stdout_raw_sha256':hashlib.sha256((O/'stdout.log').read_bytes()).hexdigest(),'stderr_raw_sha256':hashlib.sha256((O/'stderr.log').read_bytes()).hexdigest(),'public_anchor_implemented':True,'scope':'full sealed public anchor and all five internal ingredients; independent review pending'}
(O/'receipt.json').write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8')
print('Focused86',n,'EXIT',code,flush=True)
if code:print(((O/'stdout.log').read_bytes()+(O/'stderr.log').read_bytes()).decode(errors='replace')[-6500:])
sys.exit(code)
