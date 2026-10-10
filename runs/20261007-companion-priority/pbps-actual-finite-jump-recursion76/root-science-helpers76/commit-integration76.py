from pathlib import Path
import gzip,hashlib,json,os,re,subprocess
r=Path('runs/20261007-companion-priority/pbps-actual-finite-jump-recursion76');r72=r.parent/'pbps-b4-corrector-perturbation72'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();assert head==load(r/'root.exact-verification76.adoption.json')['verified_commit']
assert load(r/'root.exact-verification76.adoption.json')['native_verified']
assert load(r/'visual.inspection.json')['viewed_by_root'] and load(r/'root.repository76.adoption.json')['accepted_scoped_aggregate']
assert not subprocess.check_output(['git','diff','--cached','--name-only'],text=True).strip()
for label in ['mandatory-astis-check-final','publication-final','frontier-final','contributor-final','semantic-final','site-check-final','graph-check-final','reader-copy-download','reader-render-current']:
 q=load(r/'integration76'/label/'receipt.json');assert q['terminal_closed'] and q['exit_code']==0,label
assert load(r/'integration76/unchanged-regression-reuse.json')['reused_exact_unchanged_helpers_with_runtime_continuity_evidence']
shared=load(r/'integration76/before-generator-state.json')['keep']
changed=set(subprocess.check_output(['git','-c','core.autocrlf=false','diff','--name-only'],text=True).splitlines());assert changed<=set(shared),changed-set(shared)
active=Path(os.environ['ASTIS_FOREGROUND_OBSERVER_DIR']).resolve();assert active.is_relative_to((r/'integration76').resolve())
export=r/'root-integration-helpers76';export.mkdir(exist_ok=False)
for p in Path('.astis/pbps-recursion76').iterdir():
 if p.is_file() and p.suffix in ['.py','.mjs']:(export/p.name).write_bytes(p.read_bytes())
(export/'scope.json').write_text(json.dumps(dict(status='FROZEN_ROOT_INTEGRATION_HELPERS',active_observer_excluded=active.as_posix(),future76_not_admitted=True),indent=2)+'\n',encoding='utf8',newline='\n')
paths=list(dict.fromkeys(shared+[p.as_posix() for p in r.rglob('*') if p.is_file() and not p.resolve().is_relative_to(active)]))
assert all(Path(p).is_file() and Path(p).stat().st_size<100*1024*1024 for p in paths)
assert not any(p.startswith((r.parent/'pbps-recursive-path-preread76').as_posix()+'/') or p.startswith((r.parent/'pbps-recursive-preproof76').as_posix()+'/') or 'pbps-macro-root63' in p for p in paths)
def stage(ps):subprocess.run(['git','-c','core.autocrlf=false','add','-f','--pathspec-from-file=-','--pathspec-file-nul'],input=('\0'.join(ps)+'\0').encode(),check=True)
stage(paths);d=r/'integration76/staging-whitespace';d.mkdir(exist_ok=False)
q=subprocess.run(['git','-c','core.whitespace=cr-at-eol','diff','--cached','--check'],capture_output=True);raw=q.stdout;hits=[]
for line in raw.decode('utf8').splitlines():
 m=re.match(r'^(.+?):([0-9]+): (trailing whitespace|new blank line at EOF|space before tab in indent).*$',line)
 if m:hits.append(dict(path=m[1],line=int(m[2]),kind=m[3]))
assert q.returncode in [0,2] and (q.returncode==0 or hits)
bad=sorted({h['path'] for h in hits})
for p in bad:assert p.startswith(r.as_posix()+'/'),p
authored=[p for p in paths if p not in set(bad)]
for start in range(0,len(authored),64):subprocess.run(['git','-c','core.whitespace=cr-at-eol','diff','--cached','--check','--']+authored[start:start+64],check=True)
(d/'full-staged-immutable-negative.raw.gz').write_bytes(gzip.compress(raw,mtime=0))
(d/'diagnosis.json').write_text(json.dumps(dict(full_staged_exit=q.returncode,full_staged_whitespace_PASS=q.returncode==0,authored_complement_PASS=True,exact_immutable_raw_paths=[dict(path=p,RAW_sha256=sha(Path(p).read_bytes())) for p in bad],findings=hits,negative_RAW_sha256=sha(raw),active_observer_excluded=active.as_posix(),future76_not_staged=True),ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
stage([p.as_posix() for p in d.iterdir() if p.is_file()]);actual=set(subprocess.check_output(['git','diff','--cached','--name-only'],text=True).splitlines());assert actual<=set(paths)|{p.as_posix() for p in d.iterdir() if p.is_file()}
subprocess.run(['git','commit','-q','-m','Integrate independently verified PBPS first hazard clock'],check=True)
print(json.dumps(dict(integration_commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),staged_files=len(actual),immutable_whitespace_findings=len(hits),full_staged_whitespace_PASS=q.returncode==0,authored_whitespace_PASS=True,full_paper=False,Goal_complete=False)))
