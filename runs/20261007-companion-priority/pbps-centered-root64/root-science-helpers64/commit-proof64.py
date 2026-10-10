from pathlib import Path
import json,subprocess,hashlib,gzip,re,os
r=Path('runs/20261007-companion-priority/pbps-centered-root64');base=r.parent;load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
assert (r/'proved-local.json').is_file();plan=load(r/'publication-plan.json');claim=load(r/'claim.json');parent='ee6bdf211d0ef8c9db63ecd199a52fa8cbbb81c4'
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==parent
assert not subprocess.check_output(['git','diff','--cached','--name-only'],text=True).strip()
for p in [r/'independent-math64/lease.json',r/'anonymous-decoder/lease.json']:assert load(p)['status']=='CLOSED_LAST',p
assert load(r/'independent-source64/lease.final.json')['state']=='CLOSED_LAST'
observer=Path(os.environ['ASTIS_FOREGROUND_OBSERVER_DIR']).resolve();export=r/'root-science-helpers64';export.mkdir(exist_ok=False)
for p in Path('.astis/pbps-centered-root64').glob('*.py'):(export/p.name).write_bytes(p.read_bytes())
(export/'scope.json').write_text(json.dumps(dict(status='FROZEN_HELPER_SOURCES',scope='Helper source retention; execution is separately bound by actual process receipts.',active_observer_excluded=observer.as_posix()),indent=2)+'\n',encoding='utf-8',newline='\n')
paths=claim['proposed_files']+['research-wiki/frontier-cells/'+cid+'.json' for cid in plan['active_cells']]+['research-wiki/semantic-roundtrip/audits/'+aid+'.json' for aid in plan['audit_ids']]+['website/content/'+folder+'/'+slug+'.json' for folder in ['publications','declaration_lessons'] for slug in plan['slugs']]+['runs/substantive_advances.jsonl']
folders=['pbps-centered-root64','pbps-centered-root-preproof64']
for folder in folders:
 for p in (base/folder).rglob('*'):
  if p.is_file() and not p.resolve().is_relative_to(observer):paths.append(p.as_posix())
paths=list(dict.fromkeys(paths));assert all(Path(p).is_file() and Path(p).stat().st_size<100*1024*1024 for p in paths)
def stage(ps):subprocess.run(['git','-c','core.autocrlf=false','add','-f','--pathspec-from-file=-','--pathspec-file-nul'],input=('\0'.join(ps)+'\0').encode(),check=True)
stage(paths)
full=subprocess.run(['git','-c','core.whitespace=cr-at-eol','diff','--cached','--check'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT);raw=full.stdout;findings=[]
for line in raw.decode('utf-8').splitlines():
 m=re.match(r'^(.+?):([0-9]+): (trailing whitespace|new blank line at EOF|space before tab in indent).*$',line)
 if m:findings.append(dict(path=m[1],line=int(m[2]),kind=m[3]))
assert full.returncode in [0,2] and (full.returncode==0 or findings)
exceptions=list(dict.fromkeys(x['path'] for x in findings))
for p in exceptions:
 assert any(p.startswith((base/f).as_posix()+'/') for f in folders),('Canonical authored whitespace',p)
 assert p in paths and not p.endswith(('proved-local.json','publication-plan.json','claim.json'))
authored=[p for p in paths if p not in set(exceptions)]
for start in range(0,len(authored),64):subprocess.run(['git','-c','core.whitespace=cr-at-eol','diff','--cached','--check','--']+authored[start:start+64],check=True)
diag=r/'whitespace-diagnosis64';diag.mkdir(exist_ok=False);(diag/'staged.raw-negative.log.gz').write_bytes(gzip.compress(raw,mtime=0));(diag/'staged.authored.log').write_bytes(b'')
(diag/'diagnosis.json').write_text(json.dumps(dict(full_staged_exit=full.returncode,findings=findings,negative_RAW_sha256=sha(raw),immutable_native_exceptions=[dict(path=p,raw_sha256=sha(Path(p).read_bytes())) for p in exceptions],authored_complement_exit=0,scope='Exact named immutable source/diagnostic/closed-native bytes retained. No blanket runs exclusion or full staged whitespace PASS.',active_observer_excluded=observer.as_posix()),indent=2)+'\n',encoding='utf-8',newline='\n')
paths += [p.as_posix() for p in diag.iterdir() if p.is_file()];stage(paths)
actual=subprocess.check_output(['git','diff','--cached','--name-only'],text=True).splitlines();assert set(actual)<=set(paths)
for p in claim['proposed_files']:assert subprocess.check_output(['git','show',':'+p])==Path(p).read_bytes()
subprocess.run([__import__('sys').executable,'-X','utf8','tools/astis_publication.py','check','--base',parent],check=True)
subprocess.run(['git','commit','-q','-m','Prove actual PBPS centered root order and bounded inverse'],check=True)
print('PASS64 science commit',subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'explicit staged paths',len(actual),'immutable whitespace findings',len(findings),'active observer EXCLUDED')
