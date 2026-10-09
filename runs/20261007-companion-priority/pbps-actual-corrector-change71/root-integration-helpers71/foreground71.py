from pathlib import Path
import datetime, hashlib, json, os, subprocess, sys
root=Path.cwd(); r=root/'runs/20261007-companion-priority/pbps-actual-corrector-change71'
assert (r/'claim.json').is_file()
label,command=sys.argv[1],sys.argv[2:]; dest=r/label; dest.mkdir(parents=True,exist_ok=False)
sha=lambda b:hashlib.sha256(b).hexdigest()
pre=root/'runs/20261007-companion-priority/pbps-corrector-change-preproof71'
paths=[root/'lean-toolchain',root/'lake-manifest.json',root/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualProjectedRotation.lean',root/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualCorrectorChange.lean',root/'research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-corrector-change.json',pre/'header71.named-literal.proposed.lean',pre/'root.statement-seal71.json',pre/'root.source-first71.adoption.json',pre/'root.header-math71.adoption.json',pre/'root.header-source71.adoption.json',pre/'library-retrieval71/retrieval.json']
def pin(p):
 b=p.read_bytes(); return dict(path=p.relative_to(root).as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),LF_sha256=sha(b.replace(b'\r\n',b'\n')))
inputs=[pin(p) for p in paths if p.is_file()]
snap=dest/'inputs'; snap.mkdir()
for i,z in enumerate(inputs): (snap/f'{i}.exactraw.snapshot').write_bytes((root/z['path']).read_bytes())
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8',ASTIS_FOREGROUND_OBSERVER_DIR=dest.as_posix());env.pop('ELAN_TOOLCHAIN',None)
started=datetime.datetime.now(datetime.timezone.utc).isoformat()
with (dest/'stdout.log').open('wb') as out,(dest/'stderr.log').open('wb') as err:
 p=subprocess.Popen(command,cwd=root,env=env,stdout=out,stderr=err)
 print(json.dumps(dict(label=label,actual_foreground_PID=p.pid,status='RUNNING_INPUTS_PINNED')),flush=True);code=p.wait()
receipt=dict(command=command,checked_parent=head,started_utc=started,finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),actual_foreground_PID=p.pid,exit_code=code,terminal_closed=True,inputs=inputs,stdout=pin(dest/'stdout.log'),stderr=pin(dest/'stderr.log'),full_paper=False,Goal_complete=False)
(dest/'receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps(dict(label=label,PID=p.pid,EXIT=code)))
lines=(dest/'stdout.log').read_text(encoding='utf8',errors='replace').splitlines()+(dest/'stderr.log').read_text(encoding='utf8',errors='replace').splitlines()
selected=[s for s in lines if any(x in s for x in ['error:','error(','Build completed','PASS','FAIL','depends on axioms:'])]
print('\n'.join(selected[-20:]))
if code: print('\n'.join(lines[-35:]))
sys.exit(code)
