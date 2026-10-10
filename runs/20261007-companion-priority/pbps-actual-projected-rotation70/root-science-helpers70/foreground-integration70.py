from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys
root=Path.cwd();label,command=sys.argv[1],sys.argv[2:]
r=root/'runs/20261007-companion-priority/pbps-actual-projected-rotation70'
assert (r/'claim.json').is_file()
out=r/label;out.mkdir(parents=True,exist_ok=False)
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.resolve().as_posix(),RAW_bytes=len(b),RAW_sha256=hashlib.sha256(b).hexdigest(),LF_sha256=hashlib.sha256(b.replace(b'\r\n',b'\n')).hexdigest())
pre=root/'runs/20261007-companion-priority/pbps-actual-projected-rotation-preproof70'
names=[root/'lean-toolchain',root/'lake-manifest.json',
 root/'AutoSamplingTheory/ExampleCases/ProximalBPS/ReflectionIntertwining.lean',
 root/'AutoSamplingTheory/ExampleCases/ProximalBPS/GaussianReflection.lean',
 root/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualProjectedRotation.lean',
 root/'research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-projected-rotation.json',
 pre/'root.statement-seal70.json',pre/'header0-proposed-expanded.lean',
 pre/'root.header-math70.adoption.json',pre/'root.header-source70.adoption.json',
 pre/'root.library-retrieval70.json']
names += [root/p for p in ['AutoSamplingTheory/TechnicalLemmas/Registry.lean',
 'AutoSamplingTheory/ExampleCases.lean','Tests/Basic.lean','docs/companion-papers-handoff.md',
 'website/content/samplewiki_companion_frontiers.json',
 'website/content/publications/pbps-actual-projected-rotation.json',
 'website/content/declaration_lessons/pbps-actual-projected-rotation.json',
 'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261009-PBPSActualProjectedRotation.json',
 'website/scripts/inline_lean.py','website/scripts/check_cross_domain_browser.py',
 'runs/20261007-companion-priority/pbps-actual-projected-rotation70/root.exact-verification70.adoption.json',
 'runs/20261007-companion-priority/pbps-actual-projected-rotation70/verified.json']]
inputs=[pin(p) for p in names if p.is_file()];snaps=out/'inputs';snaps.mkdir()
for i,q in enumerate(inputs):
 b=Path(q['path']).read_bytes();(snaps/f'{i}.exactraw.snapshot').write_bytes(b);(snaps/f'{i}.LF.snapshot').write_bytes(b.replace(b'\r\n',b'\n'))
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
started=datetime.datetime.now(datetime.timezone.utc).isoformat()
env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8',ASTIS_FOREGROUND_OBSERVER_DIR=out.resolve().as_posix());env.pop('ELAN_TOOLCHAIN',None)
with (out/'stdout.log').open('wb') as o,(out/'stderr.log').open('wb') as e:
 child=subprocess.Popen(command,cwd=root,env=env,stdout=o,stderr=e)
 print(json.dumps(dict(label=label,actual_foreground_PID=child.pid,status='RUNNING_INPUTS_PINNED')),flush=True);code=child.wait()
receipt=dict(command=command,cwd=root.as_posix(),checked_parent=head,started_utc=started,
 finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),actual_foreground_PID=child.pid,
 exit_code=code,terminal_closed=True,inputs=inputs,stdout=pin(out/'stdout.log'),stderr=pin(out/'stderr.log'),
 active_observer_excluded_from_staging=True,full_paper=False)
(out/'receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(dict(label=label,PID=child.pid,EXIT=code)))
lines=(out/'stdout.log').read_text(encoding='utf-8',errors='replace').splitlines()+(out/'stderr.log').read_text(encoding='utf-8',errors='replace').splitlines()
selected=[s for s in lines if any(t in s for t in ['error:','error(','Build completed','PASS','FAIL','checked','depends on axioms:'])]
print('\n'.join(selected[-24:]))
if code:print('\n'.join(lines[-45:]))
sys.exit(code)
