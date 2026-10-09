from pathlib import Path
import gzip, hashlib, json, os, re, subprocess, sys
root=Path.cwd();r=Path('runs/20261007-companion-priority/pbps-actual-projected-rotation70');base=r.parent
parent='aa9dd2cf691489535aa8039850c2ee0bcdacdfb4'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==parent
assert not subprocess.check_output(['git','diff','--cached','--name-only'],text=True).strip()
assert (r/'proved-local.json').is_file() and (r/'root.source70.adoption.json').is_file()
assert load(r/'independent-math70/lease.final.json')['status']=='CLOSED_LAST'
assert load(r/'independent-source70/lease.final.json')['status']=='CLOSED_LAST'
assert load(r/'anonymous-decoder/lease.json')['status']=='CLOSED_LAST'
observer=Path(os.environ['ASTIS_FOREGROUND_OBSERVER_DIR']).resolve()
export=r/'root-science-helpers70';export.mkdir(exist_ok=False)
for p in Path('.astis/pbps-actual-rotation70').glob('*.py'):(export/p.name).write_bytes(p.read_bytes())
(export/'scope.json').write_text(json.dumps(dict(status='FROZEN_ROOT_HELPER_SOURCES',active_observer_excluded=observer.as_posix(),future71_not_admitted=True),indent=2)+'\n',encoding='utf-8',newline='\n')
plan=load(r/'publication-plan.json');claim=load(r/'claim.json')
paths=claim['proposed_files']+['research-wiki/frontier-cells/'+c+'.json' for c in plan['active_cells']]+['research-wiki/semantic-roundtrip/audits/'+a+'.json' for a in plan['audit_ids']]+['website/content/'+folder+'/'+slug+'.json' for folder in ['publications','declaration_lessons'] for slug in plan['slugs']]+['runs/substantive_advances.jsonl']
folders=['pbps-actual-projected-rotation70','pbps-actual-projected-rotation-preproof70']
for folder in folders:paths.extend(p.as_posix() for p in (base/folder).rglob('*') if p.is_file() and not p.resolve().is_relative_to(observer))
paths=list(dict.fromkeys(paths))
assert all(Path(p).is_file() and Path(p).stat().st_size<100*1024*1024 for p in paths)
assert not any('pbps-corrector-change-preproof71' in p or 'pbps-macro-root63/exact-science-verification/inputs/0446.exactraw.snapshot' in p or 'pbps-real-defect-root61/next-macro-source62' in p or 'pbps-centered-defect59/integration59/seal-' in p for p in paths)
def stage(items):subprocess.run(['git','-c','core.autocrlf=false','add','-f','--pathspec-from-file=-','--pathspec-file-nul'],input=('\0'.join(items)+'\0').encode(),check=True)
stage(paths)
full=subprocess.run(['git','-c','core.whitespace=cr-at-eol','diff','--cached','--check'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
raw=full.stdout;findings=[]
for line in raw.decode('utf-8').splitlines():
 m=re.match(r'^(.+?):([0-9]+): (trailing whitespace|new blank line at EOF|space before tab in indent).*$',line)
 if m:findings.append(dict(path=m[1],line=int(m[2]),kind=m[3]))
assert full.returncode in [0,2] and (full.returncode==0 or findings)
exceptions=list(dict.fromkeys(z['path'] for z in findings))
for p in exceptions:
 assert any(p.startswith((base/f).as_posix()+'/') for f in folders),('Authored canonical whitespace',p)
 assert p in paths and not p.endswith(('proved-local.json','publication-plan.json','claim.json'))
authored=[p for p in paths if p not in set(exceptions)]
for i in range(0,len(authored),64):subprocess.run(['git','-c','core.whitespace=cr-at-eol','diff','--cached','--check','--']+authored[i:i+64],check=True)
diag=r/'whitespace-diagnosis70';diag.mkdir(exist_ok=False)
(diag/'staged.raw-negative.log.gz').write_bytes(gzip.compress(raw,mtime=0))
(diag/'diagnosis.json').write_text(json.dumps(dict(full_staged_exit=full.returncode,findings=findings,negative_RAW_sha256=sha(raw),immutable_native_exceptions=[dict(path=p,raw_sha256=sha(Path(p).read_bytes())) for p in exceptions],authored_complement_exit=0,active_observer_excluded=observer.as_posix(),scope='Finite immutable source/native evidence exceptions; full staged whitespace PASS is not claimed.'),indent=2)+'\n',encoding='utf-8',newline='\n')
paths.extend(p.as_posix() for p in diag.iterdir() if p.is_file());stage(paths)
actual=subprocess.check_output(['git','diff','--cached','--name-only'],text=True).splitlines();assert set(actual)<=set(paths)
for p in claim['proposed_files']:assert subprocess.check_output(['git','show',':'+p])==Path(p).read_bytes()
subprocess.run([sys.executable,'-X','utf8','tools/astis_publication.py','check','--base',parent],check=True)
subprocess.run([sys.executable,'-X','utf8','tools/astis_contributor_contract.py','check','--base',parent],check=True)
subprocess.run(['git','commit','-q','-m','Prove actual PBPS projected rotation and pair energy'],check=True)
print('PASS70 science commit',subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'explicit paths',len(actual),'immutable whitespace findings',len(findings))
