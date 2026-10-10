from pathlib import Path
import gzip, hashlib, json, os, re, subprocess, sys
r=Path('runs/20261007-companion-priority/pbps-actual-harmonic-flow73');base=r.parent
parent='bc3dca8d76432f71e3abbfdbce2c3b2161ec8d19'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==parent
assert not subprocess.check_output(['git','diff','--cached','--name-only'],text=True).strip()
assert (r/'proved-local.json').is_file() and (r/'root.source73.adoption.json').is_file()
assert load(r/'independent-math73/lease.final.json')['status']=='CLOSED_LAST'
assert load(r/'anonymous-decoder/CLOSED_LAST.json')['status']=='CLOSED_LAST'
adopt=load(r/'root.source73.adoption.json');z=adopt['native_lease']
assert sha(Path(z['path']).read_bytes())==z['RAW_sha256']
observer=Path(os.environ['ASTIS_FOREGROUND_OBSERVER_DIR']).resolve()
export=r/'root-science-helpers73';export.mkdir(exist_ok=False)
for p in Path('.astis/pbps-harmonic73').glob('*.py'):(export/p.name).write_bytes(p.read_bytes())
(export/'scope.json').write_text(json.dumps(dict(status='FROZEN_ROOT_HELPER_SOURCES',active_observer_excluded=observer.as_posix(),future74_not_admitted=True),indent=2)+'\n',encoding='utf8',newline='\n')
plan=load(r/'publication-plan.json');claim=load(r/'claim.json')
paths=claim['proposed_files']+['research-wiki/frontier-cells/'+c+'.json' for c in plan['active_cells']]+['research-wiki/semantic-roundtrip/audits/'+a+'.json' for a in plan['audit_ids']]+['website/content/'+folder+'/'+slug+'.json' for folder in ['publications','declaration_lessons'] for slug in plan['slugs']]+['runs/substantive_advances.jsonl']
folders=['pbps-actual-harmonic-flow73','pbps-harmonic-flow-preproof73','pbps-harmonic-flow-sourcegraph73','pbps-half-turn-construction-preread73']
for folder in folders:
 paths.extend(p.as_posix() for p in (base/folder).rglob('*') if p.is_file() and not p.resolve().is_relative_to(observer))
paths=list(dict.fromkeys(paths));assert all(Path(p).is_file() and Path(p).stat().st_size<100*1024*1024 for p in paths)
assert all('pbps-macro-root63' not in p and 'preread74' not in p for p in paths)
def stage(ps):
 subprocess.run(['git','-c','core.autocrlf=false','add','-f','--pathspec-from-file=-','--pathspec-file-nul'],input=('\0'.join(ps)+'\0').encode(),check=True)
stage(paths)
q=subprocess.run(['git','-c','core.whitespace=cr-at-eol','diff','--cached','--check'],capture_output=True)
raw=q.stdout;hits=[]
for line in raw.decode('utf8').splitlines():
 m=re.match(r'^(.+?):([0-9]+): (trailing whitespace|new blank line at EOF|space before tab in indent).*$',line)
 if m:hits.append(dict(path=m[1],line=int(m[2]),kind=m[3]))
assert q.returncode in [0,2] and (q.returncode==0 or hits)
exceptions=list(dict.fromkeys(z['path'] for z in hits))
for p in exceptions:assert any(p.startswith((base/f).as_posix()+'/') for f in folders),p
authored=[p for p in paths if p not in set(exceptions)]
for i in range(0,len(authored),64):subprocess.run(['git','-c','core.whitespace=cr-at-eol','diff','--cached','--check','--']+authored[i:i+64],check=True)
diag=r/'whitespace-diagnosis73';diag.mkdir(exist_ok=False)
(diag/'full-staged-immutable-negative.raw.gz').write_bytes(gzip.compress(raw,mtime=0))
(diag/'diagnosis.json').write_text(json.dumps(dict(full_staged_EXIT=q.returncode,full_staged_whitespace_PASS=q.returncode==0,
 findings=hits,negative_RAW_sha256=sha(raw),immutable_raw_paths=[dict(path=p,RAW_sha256=sha(Path(p).read_bytes())) for p in exceptions],
 authored_complement_PASS=True,active_observer_excluded=observer.as_posix(),future74_not_staged=True),indent=2)+'\n',encoding='utf8',newline='\n')
stage([p.as_posix() for p in diag.iterdir() if p.is_file()])
actual=set(subprocess.check_output(['git','diff','--cached','--name-only'],text=True).splitlines())
assert actual<=set(paths)|{p.as_posix() for p in diag.iterdir() if p.is_file()}
for p in claim['proposed_files']:assert subprocess.check_output(['git','show',':'+p])==Path(p).read_bytes()
for tool in ['tools/astis_publication.py','tools/astis_contributor_contract.py']:
 subprocess.run([sys.executable,'-B','-X','utf8',tool,'check','--base',parent],check=True)
subprocess.run(['git','commit','-q','-m','Prove actual PBPS harmonic flow and conserved energy'],check=True)
print(json.dumps(dict(status='PASS_SCI73_NOT_VERIFIED',science_commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
 explicit_staged_files=len(actual),immutable_whitespace_findings=len(hits),full_staged_whitespace_PASS=q.returncode==0,authored_whitespace_PASS=True,Goal_complete=False)))
