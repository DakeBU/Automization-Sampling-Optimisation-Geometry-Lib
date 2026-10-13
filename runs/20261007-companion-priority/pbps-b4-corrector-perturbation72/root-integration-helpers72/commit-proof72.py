from pathlib import Path
import gzip,hashlib,json,os,re,subprocess,sys
root=Path.cwd();r=Path('runs/20261007-companion-priority/pbps-b4-corrector-perturbation72');base=r.parent
parent='1e9d2feb727919ebaa17ee1a67b629a0b85b0ba9'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==parent
assert not subprocess.check_output(['git','diff','--cached','--name-only'],text=True).strip()
assert (r/'proved-local.json').is_file() and (r/'root.source72.adoption.json').is_file()
assert load(r/'independent-math72/lease.final.json')['status']=='CLOSED_LAST'
assert load(r/'anonymous-decoder/CLOSED_LAST.json')['status']=='CLOSED_LAST'
source=load(r/'root.source72.adoption.json');sourcelease=source['native_lease'];assert sha(Path(sourcelease['path']).read_bytes())==sourcelease['RAW_sha256']
observer=Path(os.environ['ASTIS_FOREGROUND_OBSERVER_DIR']).resolve()
export=r/'root-science-helpers72';export.mkdir(exist_ok=False)
for p in Path('.astis/pbps-perturbation72').glob('*.py'):(export/p.name).write_bytes(p.read_bytes())
(export/'scope.json').write_text(json.dumps(dict(status='FROZEN_ROOT_HELPER_SOURCES',active_observer_excluded=observer.as_posix(),future73_not_admitted=True),indent=2)+'\n',encoding='utf8',newline='\n')
plan=load(r/'publication-plan.json');claim=load(r/'claim.json')
paths=claim['proposed_files']+['research-wiki/frontier-cells/'+c+'.json' for c in plan['active_cells']]+['research-wiki/semantic-roundtrip/audits/'+a+'.json' for a in plan['audit_ids']]+['website/content/'+folder+'/'+slug+'.json' for folder in ['publications','declaration_lessons'] for slug in plan['slugs']]+['runs/substantive_advances.jsonl']
folders=['pbps-b4-corrector-perturbation72','pbps-b4-perturbation-preproof72']
for folder in folders:paths.extend(p.as_posix() for p in (base/folder).rglob('*') if p.is_file() and not p.resolve().is_relative_to(observer))
paths=list(dict.fromkeys(paths));assert all(Path(p).is_file() and Path(p).stat().st_size<100*1024*1024 for p in paths)
assert not any('preread73' in p or 'pbps-macro-root63' in p for p in paths)
def stage(items):subprocess.run(['git','-c','core.autocrlf=false','add','-f','--pathspec-from-file=-','--pathspec-file-nul'],input=('\0'.join(items)+'\0').encode(),check=True)
stage(paths);full=subprocess.run(['git','-c','core.whitespace=cr-at-eol','diff','--cached','--check'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
raw=full.stdout;findings=[]
for line in raw.decode('utf8').splitlines():
 m=re.match(r'^(.+?):([0-9]+): (trailing whitespace|new blank line at EOF|space before tab in indent).*$',line)
 if m:findings.append(dict(path=m[1],line=int(m[2]),kind=m[3]))
assert full.returncode in [0,2] and (full.returncode==0 or findings)
exceptions=list(dict.fromkeys(z['path'] for z in findings))
for p in exceptions:assert any(p.startswith((base/f).as_posix()+'/') for f in folders),('Authored canonical whitespace',p)
authored=[p for p in paths if p not in set(exceptions)]
for i in range(0,len(authored),64):subprocess.run(['git','-c','core.whitespace=cr-at-eol','diff','--cached','--check','--']+authored[i:i+64],check=True)
diag=r/'whitespace-diagnosis72';diag.mkdir(exist_ok=False)
(diag/'staged.raw-negative.log.gz').write_bytes(gzip.compress(raw,mtime=0))
(diag/'diagnosis.json').write_text(json.dumps(dict(full_staged_exit=full.returncode,findings=findings,negative_RAW_sha256=sha(raw),immutable_native_exceptions=[dict(path=p,RAW_sha256=sha(Path(p).read_bytes())) for p in exceptions],authored_complement_exit=0,active_observer_excluded=observer.as_posix(),scope='Exact immutable source/native evidence retained; full staged whitespace PASS is not claimed if nonzero.'),indent=2)+'\n',encoding='utf8',newline='\n')
paths.extend(p.as_posix() for p in diag.iterdir() if p.is_file());stage(paths)
actual=subprocess.check_output(['git','diff','--cached','--name-only'],text=True).splitlines();assert set(actual)<=set(paths)
for p in claim['proposed_files']:assert subprocess.check_output(['git','show',':'+p])==Path(p).read_bytes()
subprocess.run([sys.executable,'-X','utf8','tools/astis_publication.py','check','--base',parent],check=True)
subprocess.run([sys.executable,'-X','utf8','tools/astis_contributor_contract.py','check','--base',parent],check=True)
subprocess.run(['git','commit','-q','-m','Prove Hilbert and actual PBPS corrector perturbation'],check=True)
print('PASS72 science commit',subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'explicitpaths',len(actual),'immutable whitespace findings',len(findings))
