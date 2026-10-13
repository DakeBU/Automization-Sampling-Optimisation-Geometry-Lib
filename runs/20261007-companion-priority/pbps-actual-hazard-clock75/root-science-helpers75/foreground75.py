from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys
r=Path('runs/20261007-companion-priority/pbps-actual-hazard-clock75');pre=r.parent/'pbps-clock-preproof75'
label,cmd=sys.argv[1],sys.argv[2:];out=r/label;out.mkdir(parents=True,exist_ok=False)
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.resolve().as_posix(),RAW_bytes=len(b),RAW_sha256=hashlib.sha256(b).hexdigest(),LF_sha256=hashlib.sha256(b.replace(b'\r\n',b'\n')).hexdigest())
paths=[Path(p) for p in ['lean-toolchain','lake-manifest.json','AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHarmonicFlow.lean','AutoSamplingTheory/ExampleCases/ProximalBPS/ActualBounceRate.lean','AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHazardClock.lean','research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-hazard-clock.json']]+[pre/p for p in ['header75.v2.proposed.lean','root.statement-seal75.json','root.header-reviews75.adoption.json']]
inputs=[pin(p) for p in paths if p.is_file()];snap=out/'inputs';snap.mkdir()
for i,z in enumerate(inputs):
 b=Path(z['path']).read_bytes();(snap/f'{i}.exactraw.snapshot').write_bytes(b);(snap/f'{i}.LF.snapshot').write_bytes(b.replace(b'\r\n',b'\n'))
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();started=datetime.datetime.now(datetime.timezone.utc).isoformat()
env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf8',PYTHONUNBUFFERED='1',ASTIS_FOREGROUND_OBSERVER_DIR=out.resolve().as_posix());env.pop('ELAN_TOOLCHAIN',None)
with (out/'stdout.log').open('wb') as s,(out/'stderr.log').open('wb') as e:
 p=subprocess.Popen(cmd,env=env,stdout=s,stderr=e);print(json.dumps(dict(label=label,actual_foreground_PID=p.pid,status='RUNNING')),flush=True);code=p.wait()
q=dict(command=cmd,checked_parent=head,started_utc=started,finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),actual_foreground_PID=p.pid,exit_code=code,terminal_closed=True,inputs=inputs,stdout=pin(out/'stdout.log'),stderr=pin(out/'stderr.log'),Goal_complete=False)
(out/'receipt.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print(json.dumps(dict(label=label,PID=p.pid,EXIT=code)))
lines=(out/'stdout.log').read_text(encoding='utf8',errors='replace').splitlines()+(out/'stderr.log').read_text(encoding='utf8',errors='replace').splitlines()
print('\n'.join(lines[-80:] if code else [s for s in lines if any(t in s for t in ['Build completed','error:','PASS','axioms:'])][-18:]))
sys.exit(code)
