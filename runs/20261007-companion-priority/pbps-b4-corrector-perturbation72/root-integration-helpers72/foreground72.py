from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys
root=Path.cwd();label,command=sys.argv[1],sys.argv[2:]
r=root/'runs/20261007-companion-priority/pbps-b4-corrector-perturbation72'
pre=root/'runs/20261007-companion-priority/pbps-b4-perturbation-preproof72'
assert (r/'claim.json').is_file()
if label in {'integration72/graph-check-actual-final','integration72/graph-check-generic-final','integration72/site-check-final','integration72/publication-final-admin','integration72/frontier-final-admin','integration72/contributor-final-admin','integration72/semantic-final-admin'} and not (r/'integration72/final-admin.json').is_file():
 raise RuntimeError('Final admin not written; reject premature dependent gate before any output writes.')
out=r/label;out.mkdir(parents=True,exist_ok=False)
def pin(p):
 p=Path(p);b=p.read_bytes()
 return dict(path=p.resolve().as_posix(),RAW_bytes=len(b),RAW_sha256=hashlib.sha256(b).hexdigest(),LF_sha256=hashlib.sha256(b.replace(b'\r\n',b'\n')).hexdigest())
names=[root/p for p in ['lean-toolchain','lake-manifest.json','AutoSamplingTheory/ExampleCases/ProximalBPS/ActualCorrectorChange.lean','AutoSamplingTheory/TechnicalLemmas/Analysis/HilbertCorrectorPerturbation.lean','AutoSamplingTheory/ExampleCases/ProximalBPS/ActualCorrectorPerturbation.lean','research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-corrector-perturbation.json']]
names += [pre/p for p in ['root.statement-seal72.json','header72.generic.proposed.lean','header72.actual.named-literal.proposed.lean','root.header-math72.adoption.json','root.header-source72.adoption.json','library-retrieval72/retrieval.json']]
inputs=[pin(p) for p in names if p.is_file()]
snap=out/'inputs';snap.mkdir()
for i,z in enumerate(inputs):
 b=Path(z['path']).read_bytes();(snap/f'{i}.exactraw.snapshot').write_bytes(b);(snap/f'{i}.LF.snapshot').write_bytes(b.replace(b'\r\n',b'\n'))
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();started=datetime.datetime.now(datetime.timezone.utc).isoformat()
env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf8',ASTIS_FOREGROUND_OBSERVER_DIR=out.resolve().as_posix());env.pop('ELAN_TOOLCHAIN',None)
with (out/'stdout.log').open('wb') as o,(out/'stderr.log').open('wb') as e:
 child=subprocess.Popen(command,cwd=root,env=env,stdout=o,stderr=e)
 print(json.dumps(dict(label=label,actual_foreground_PID=child.pid,status='RUNNING_INPUTS_PINNED')),flush=True)
 code=child.wait()
receipt=dict(command=command,checked_parent=head,started_utc=started,finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),actual_foreground_PID=child.pid,exit_code=code,terminal_closed=True,inputs=inputs,stdout=pin(out/'stdout.log'),stderr=pin(out/'stderr.log'),Goal_complete=False)
(out/'receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print(json.dumps(dict(label=label,PID=child.pid,EXIT=code)))
lines=(out/'stdout.log').read_text(encoding='utf8',errors='replace').splitlines()+(out/'stderr.log').read_text(encoding='utf8',errors='replace').splitlines()
selected=[s for s in lines if any(t in s for t in ['error:','error(','Build completed','PASS','FAIL','checked','depends on axioms:'])]
print('\n'.join(selected[-24:]))
if code:print('\n'.join(lines[-50:]))
sys.exit(code)
