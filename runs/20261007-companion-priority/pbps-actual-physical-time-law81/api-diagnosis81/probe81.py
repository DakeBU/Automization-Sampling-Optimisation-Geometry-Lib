from pathlib import Path
import hashlib,json,os,subprocess,datetime,difflib,sys
R=Path('E:/Samplinglib');B=R/'runs/20261007-companion-priority/pbps-actual-physical-time-law81';O=B/'api-diagnosis81';O.mkdir(parents=True,exist_ok=True)
def raw(p):
 b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),RAW_bytes=len(b),RAW_sha256=hashlib.sha256(b).hexdigest())
def save(n,d):
 with (O/n).open('x',encoding='utf-8',newline='\n') as f:json.dump(d,f,ensure_ascii=False,indent=2);f.write('\n')
SRC=B/'focused81-attempt3/source.snapshot.lean';s=SRC.read_text(encoding='utf-8');assert raw(SRC)['RAW_sha256']=='8eb2cfe48244ada2af79740b07430cf72167fe4aaa5cf6c692098e66568c657b'
old='      exact hτM.comp haM';new='      have hcomp := hτM.comp haM\n      exact hcomp'
assert s.count(old)==1
path=O/'full81.inferred-composition.lean'
with path.open('x',encoding='utf-8',newline='\n') as f:f.write(s.replace(old,new))
with (O/'inferred-composition.diff').open('x',encoding='utf-8',newline='\n') as f:f.write(''.join(difflib.unified_diff(s.splitlines(True),s.replace(old,new).splitlines(True),fromfile=str(SRC.relative_to(R)),tofile=str(path.relative_to(R)))))
save('input-freeze81.json',dict(scope='API/definitional-equality diagnosis only; no production or statement repair',reviewer='/root/exact_verify77',inputs=[raw(SRC),raw(B/'focused81-attempt3/receipt.json'),raw(B/'focused81-attempt3/stdout.log'),raw(B/'header81.proposed.lean'),raw(R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHazardClock.lean'),raw(R/'lean-toolchain'),raw(R/'lake-manifest.json')],experimental_copy=raw(path)))
env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf8');env.pop('ELAN_TOOLCHAIN',None)
cmd=[str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'),'env',str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lean.exe'),str(path)]
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
with (O/'inferred-composition.stdout.log').open('xb') as out,(O/'inferred-composition.stderr.log').open('xb') as err:
 p=subprocess.Popen(cmd,cwd=R,env=env,stdout=out,stderr=err);print('full inferred composition foreground PID',p.pid,flush=True);code=p.wait()
save('inferred-composition.receipt.json',dict(command_argv=cmd,cwd=str(R),actual_foreground_PID=p.pid,exit_code=code,terminal_closed=True,start_utc=start,end_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),input=raw(path),stdout=raw(O/'inferred-composition.stdout.log'),stderr=raw(O/'inferred-composition.stderr.log'),production_edited=False))
print('FULL INFERRED COMPOSITION EXIT',code,flush=True)
