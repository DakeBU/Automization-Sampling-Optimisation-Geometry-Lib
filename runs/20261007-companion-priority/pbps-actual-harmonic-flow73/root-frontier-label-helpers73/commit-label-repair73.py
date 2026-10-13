from pathlib import Path
import gzip,hashlib,json,os,re,subprocess,sys
r=Path('runs/20261007-companion-priority/pbps-actual-harmonic-flow73')
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
parent='63319104ccad4e81e3a2c59da23ec0009be5e17f'
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==parent
assert not subprocess.check_output(['git','diff','--cached','--name-only'],text=True).strip()
a=load(r/'root.frontier-label-overlay73.adoption.json');cp=a['current']['path'];assert sha(Path(cp).read_bytes())==a['current']['RAW_sha256']
assert subprocess.check_output(['git','diff','--name-only'],text=True).splitlines()==[cp]
observer=Path(os.environ['ASTIS_FOREGROUND_OBSERVER_DIR']).resolve()
folders=['commit-science73','exact-science-verification73','frontier-label-overlay73','independent-frontier-label-repair73','propose-frontier-label-overlay73','apply-frontier-label73']
paths=[cp,(r/'root.failed-science73.adoption.json').as_posix(),(r/'root.frontier-label-overlay73.adoption.json').as_posix()]
for name in folders:paths.extend(p.as_posix() for p in (r/name).rglob('*') if p.is_file() and not p.resolve().is_relative_to(observer))
export=r/'root-frontier-label-helpers73';export.mkdir(exist_ok=False)
for name in ['apply-frontier-label73.py','commit-label-repair73.py','propose-frontier-label73.py','foreground73.py']:(export/name).write_bytes((Path('.astis/pbps-harmonic73')/name).read_bytes())
paths.extend(p.as_posix() for p in export.iterdir());paths=list(dict.fromkeys(paths))
assert not any('74' in Path(p).parts or 'preproof74' in p or 'preread74' in p for p in paths)
def stage(ps):subprocess.run(['git','-c','core.autocrlf=false','add','-f','--pathspec-from-file=-','--pathspec-file-nul'],input=('\0'.join(ps)+'\0').encode(),check=True)
stage(paths);q=subprocess.run(['git','-c','core.whitespace=cr-at-eol','diff','--cached','--check'],capture_output=True)
hits=[]
for line in q.stdout.decode('utf8').splitlines():
 m=re.match(r'^(.+?):([0-9]+): (trailing whitespace|new blank line at EOF|space before tab in indent).*$',line)
 if m:hits.append(dict(path=m[1],line=int(m[2]),kind=m[3]))
assert q.returncode in [0,2] and (q.returncode==0 or hits)
bad={z['path'] for z in hits};assert all(p.startswith((r/'exact-science-verification73').as_posix()+'/') for p in bad),bad
authored=[p for p in paths if p not in bad]
for i in range(0,len(authored),64):subprocess.run(['git','-c','core.whitespace=cr-at-eol','diff','--cached','--check','--']+authored[i:i+64],check=True)
diag=r/'frontier-label-staging73';diag.mkdir(exist_ok=False)
(diag/'raw-whitespace-negative.gz').write_bytes(gzip.compress(q.stdout,mtime=0))
(diag/'diagnosis.json').write_text(json.dumps(dict(full_staged_EXIT=q.returncode,full_staged_whitespace_PASS=q.returncode==0,findings=hits,authored_complement_PASS=True,immutable_paths=[dict(path=p,RAW_sha256=sha(Path(p).read_bytes())) for p in sorted(bad)],observer_excluded=observer.as_posix(),no_mathematical_change=True),indent=2)+'\n',encoding='utf8',newline='\n')
stage([p.as_posix() for p in diag.iterdir()])
for tool in ['tools/astis_frontier_cells.py','tools/astis_publication.py','tools/astis_contributor_contract.py','tools/astis_semantic_roundtrip.py']:
 cmd=[sys.executable,'-B','-X','utf8',tool,'check']
 if tool in ['tools/astis_publication.py','tools/astis_contributor_contract.py']:cmd+=['--base',parent]
 subprocess.run(cmd,check=True)
assert subprocess.check_output(['git','diff','--cached','--name-only','--','*.lean'],text=True).strip()==''
subprocess.run(['git','commit','-q','-m','Label existing PBPS harmonic-flow Samplinglib retrieval'],check=True)
print(json.dumps(dict(status='METADATA_ONLY_SCI73_CHILD_NOT_VERIFIED',commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),parent=parent,files=len(paths),no_mathematical_change=True,immutable_whitespace_findings=len(hits),Goal_complete=False)))
