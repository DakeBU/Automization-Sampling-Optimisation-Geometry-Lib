from pathlib import Path
import json,subprocess,hashlib,gzip,re,os,sys
r=Path('runs/20261007-companion-priority/pbps-root-commutation67');base=r.parent;load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
parent='eb3d5ffbb6853f2a0aa4a8c66aefce19d8050176'
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==parent
assert not subprocess.check_output(['git','diff','--cached','--name-only'],text=True).strip()
assert (r/'proved-local.json').is_file()
for dd in ['independent-math67','independent-source67']:assert load(r/dd/'lease.final.json')['status']=='CLOSED_LAST'
observer=Path(os.environ['ASTIS_FOREGROUND_OBSERVER_DIR']).resolve();export=r/'root-science-helpers67';export.mkdir(exist_ok=False)
for p in Path('.astis/pbps-root-commutation67').glob('*.py'):(export/p.name).write_bytes(p.read_bytes())
preproof_helpers=export/'preproof-origin66';preproof_helpers.mkdir()
for name in ['prepare-headers67.py','seal-and-claim67.py','adopt-primary67.py','adopt-headers67.py']:
 p=Path('.astis/pbps-ambient-adjoint66')/name;(preproof_helpers/name).write_bytes(p.read_bytes())
(export/'scope.json').write_text(json.dumps(dict(status='FROZEN_HELPER_SOURCES',active_observer_excluded=observer.as_posix(),scope='Helper sources only; independent execution receipts supply evidence.'),indent=2)+'\n',encoding='utf-8',newline='\n')
plan=load(r/'publication-plan.json');claim=load(r/'claim.json')
paths=claim['proposed_files']+['research-wiki/frontier-cells/'+c+'.json' for c in plan['active_cells']]+['research-wiki/semantic-roundtrip/audits/'+a+'.json' for a in plan['audit_ids']]+['website/content/'+f+'/'+s+'.json' for f in ['publications','declaration_lessons'] for s in plan['slugs']]+['runs/substantive_advances.jsonl','runs/substantive_discoveries.jsonl']
folders=['pbps-root-commutation67','pbps-first-corrector-energy-preproof67']
for folder in folders:
 for p in (base/folder).rglob('*'):
  if p.is_file() and not p.resolve().is_relative_to(observer):paths.append(p.as_posix())
late66=subprocess.check_output(['git','ls-files','--others','--exclude-standard','--',(base/'pbps-ambient-adjoint66').as_posix()],text=True).splitlines()
paths.extend(late66);paths=list(dict.fromkeys(paths))
assert all(Path(p).is_file() and Path(p).stat().st_size<100*1024*1024 for p in paths)
assert not any('pbps-macro-root63/exact-science-verification/inputs/0446.exactraw.snapshot' in p or 'pbps-polar-preproof65' in p or 'pbps-sharp-energy-preproof68' in p for p in paths)
def stage(ps):subprocess.run(['git','-c','core.autocrlf=false','add','-f','--pathspec-from-file=-','--pathspec-file-nul'],input=('\0'.join(ps)+'\0').encode(),check=True)
stage(paths)
full=subprocess.run(['git','-c','core.whitespace=cr-at-eol','diff','--cached','--check'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT);raw=full.stdout;findings=[]
for line in raw.decode('utf-8').splitlines():
 m=re.match(r'^(.+?):([0-9]+): (trailing whitespace|new blank line at EOF|space before tab in indent).*$',line)
 if m:findings.append(dict(path=m[1],line=int(m[2]),kind=m[3]))
assert full.returncode in [0,2] and (full.returncode==0 or findings)
exceptions=list(dict.fromkeys(x['path'] for x in findings))
for p in exceptions:
 assert any(p.startswith((base/f).as_posix()+'/') for f in folders+['pbps-ambient-adjoint66']),('Canonical authored whitespace',p)
 assert p in paths and not p.endswith(('proved-local.json','publication-plan.json','claim.json'))
authored=[p for p in paths if p not in set(exceptions)]
for start in range(0,len(authored),64):subprocess.run(['git','-c','core.whitespace=cr-at-eol','diff','--cached','--check','--']+authored[start:start+64],check=True)
diag=r/'whitespace-diagnosis67';diag.mkdir(exist_ok=False)
(diag/'staged.raw-negative.log.gz').write_bytes(gzip.compress(raw,mtime=0))
(diag/'diagnosis.json').write_text(json.dumps(dict(full_staged_exit=full.returncode,findings=findings,negative_RAW_sha256=sha(raw),immutable_native_exceptions=[dict(path=p,raw_sha256=sha(Path(p).read_bytes())) for p in exceptions],authored_complement_exit=0,scope='Exact source/native/diagnostic bytes preserved; explicit immutable exceptions only. Full staged whitespace PASS is not claimed.',active_observer_excluded=observer.as_posix()),indent=2)+'\n',encoding='utf-8',newline='\n')
paths.extend(p.as_posix() for p in diag.iterdir() if p.is_file());stage(paths)
actual=subprocess.check_output(['git','diff','--cached','--name-only'],text=True).splitlines();assert set(actual)<=set(paths)
for p in claim['proposed_files']:assert subprocess.check_output(['git','show',':'+p])==Path(p).read_bytes()
subprocess.run([sys.executable,'-X','utf8','tools/astis_publication.py','check','--base',parent],check=True)
subprocess.run([sys.executable,'-X','utf8','tools/astis_contributor_contract.py','check','--base',parent],check=True)
subprocess.run(['git','commit','-q','-m','Prove same PBPS root inverse commutation and corrector coefficient identity'],check=True)
print('PASS67 science commit',subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'explicit paths',len(actual),'immutable whitespace findings',len(findings),'active observer excluded')
