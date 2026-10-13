from pathlib import Path
import json,subprocess,hashlib,gzip,re,os
r=Path('runs/20261007-companion-priority/pbps-macro-root63');base=r.parent;load=lambda p:json.loads(Path(p).read_bytes());sha=lambda a:hashlib.sha256(a).hexdigest()
assert (r/'proved-local.json').exists();plan=load(r/'publication-plan.json');claim=load(r/'claim.json');parent=load(r/'math-freeze.json')['checked_base_commit'];assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==parent
assert not subprocess.check_output(['git','diff','--cached','--name-only'],text=True).strip()
for p in [r/'independent-math63/lease.json',r/'independent-source63/lease.json',r/'anonymous-decoder/lease.json']:
 x=load(p);assert x['status'] in ['CLOSED','CLOSED_LAST'] and (x.get('closed_last') or x['status']=='CLOSED_LAST'),str(p)
observer=Path(os.environ['ASTIS_FOREGROUND_OBSERVER_DIR']).resolve();export=r/'root-science-helpers63';export.mkdir(exist_ok=False)
for p in Path('.astis/pbps-macro-root63').glob('*.py'):(export/p.name).write_bytes(p.read_bytes())
(export/'scope.json').write_text(json.dumps(dict(status='FROZEN_HELPER_SOURCES',scope='Source retention only; actual execution is proved by individual process receipts. Includes prepared integration helper, which has not yet run.',active_commit_observer_excluded=observer.as_posix()),indent=2)+'\n',encoding='utf-8',newline='\n')
paths=list(claim['proposed_files'])+['research-wiki/frontier-cells/'+cid+'.json' for cid in plan['active_cells']]+['research-wiki/semantic-roundtrip/audits/'+aid+'.json' for aid in plan['audit_ids']]+['website/content/'+folder+'/'+slug+'.json' for folder in ['publications','declaration_lessons'] for slug in plan['slugs']]+['runs/substantive_advances.jsonl']
folders=['pbps-macro-root63','pbps-macro-root-preproof63']
for folder in folders:
 for p in (base/folder).rglob('*'):
  if not p.is_file() or p.resolve().is_relative_to(observer):continue
  paths.append(p.as_posix())
paths=list(dict.fromkeys(paths));assert all(Path(p).is_file() and Path(p).stat().st_size<100*1024*1024 for p in paths)
assert not any(Path(p).resolve().is_relative_to(observer) for p in paths)
def stage(ps):subprocess.run(['git','-c','core.autocrlf=false','add','-f','--pathspec-from-file=-','--pathspec-file-nul'],input=('\0'.join(ps)+'\0').encode(),check=True)
stage(paths)
full=subprocess.run(['git','-c','core.whitespace=cr-at-eol','diff','--cached','--check'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT);raw=full.stdout;findings=[]
for line in raw.decode('utf-8').splitlines():
 m=re.match(r'^(.+?):([0-9]+): (trailing whitespace|new blank line at EOF|space before tab in indent).*$',line)
 if m:findings.append(dict(path=m[1],line=int(m[2]),kind=m[3]))
assert full.returncode in [0,2] and (full.returncode==0 or findings)
excluded=list(dict.fromkeys(row['path'] for row in findings))
for p in excluded:
 assert any(p.startswith((base/folder).as_posix()+'/') for folder in folders),('Canonical authored whitespace',p)
 assert p in paths and not p.endswith(('publication-plan.json','proved-local.json','claim.json')),(p,'authored artifact needs fix')
authored=[p for p in paths if p not in set(excluded)]
for start in range(0,len(authored),64):subprocess.run(['git','-c','core.whitespace=cr-at-eol','diff','--cached','--check','--']+authored[start:start+64],check=True)
diag=r/'whitespace-diagnosis63';diag.mkdir(exist_ok=False);(diag/'staged.raw-negative.log.gz').write_bytes(gzip.compress(raw,mtime=0));(diag/'staged.authored.log').write_bytes(b'')
d=dict(full_staged_exit=full.returncode,findings=findings,negative_raw_sha256=sha(raw),immutable_native_exceptions=[dict(path=p,raw_sha256=sha(Path(p).read_bytes()),lf_sha256=sha(Path(p).read_bytes().replace(b'\r\n',b'\n'))) for p in excluded],authored_complement_check_exit=0,scope='Exact named immutable source/diagnostic/closed-actor bytes preserved. No blanket runs exclusion or full staged whitespace PASS.',active_observer_excluded=observer.as_posix())
(diag/'diagnosis.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n');paths += [p.as_posix() for p in diag.iterdir() if p.is_file()];stage(paths)
actual=subprocess.check_output(['git','diff','--cached','--name-only'],text=True).splitlines();assert set(actual)<=set(paths)
for p in claim['proposed_files']:assert subprocess.check_output(['git','show',':'+p])==Path(p).read_bytes(),('Lean staged raw mismatch',p)
subprocess.run(['C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe','-X','utf8','tools/astis_publication.py','check','--base',parent],check=True)
subprocess.run(['git','commit','-q','-m','Prove actual PBPS unique positive macroscopic defect root'],check=True)
print('PASS63 science commit',subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'explicit staged delta',len(actual),'immutable whitespace findings',len(findings),'paths',len(excluded),'active observer EXCLUDED')
