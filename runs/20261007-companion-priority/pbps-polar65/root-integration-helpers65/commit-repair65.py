from pathlib import Path
import os,json,subprocess,hashlib,gzip,re,sys
r=Path('runs/20261007-companion-priority/pbps-polar65');active=Path(os.environ['ASTIS_FOREGROUND_OBSERVER_DIR']).resolve();sha=lambda b:hashlib.sha256(b).hexdigest()
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()=='dad6e38c9beed3476cb5d1db06eb57b955c8e3eb'
assert not subprocess.check_output(['git','diff','--cached','--name-only'],text=True).strip()
assert json.loads((r/'frontier-repair-gate65-v2/receipt.json').read_bytes())['exit_code']==0
export=r/'root-metadata-repair-helpers65';export.mkdir(exist_ok=False)
for p in Path('.astis/pbps-polar65').glob('*.py'):(export/p.name).write_bytes(p.read_bytes())
cell='research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-polar-isometry.json'
changed=subprocess.check_output(['git','diff','--name-only'],text=True).splitlines();assert changed==[cell],changed
untracked=subprocess.check_output(['git','ls-files','--others','--exclude-standard','--',r.as_posix()],text=True).splitlines()
paths=[cell]+[p for p in untracked if not Path(p).resolve().is_relative_to(active)]
assert all(Path(p).stat().st_size<100*1024*1024 for p in paths) and not any('preproof66' in p for p in paths)
def stage(ps):subprocess.run(['git','-c','core.autocrlf=false','add','-f','--pathspec-from-file=-','--pathspec-file-nul'],input=('\0'.join(ps)+'\0').encode(),check=True)
stage(paths);q=subprocess.run(['git','-c','core.whitespace=cr-at-eol','diff','--cached','--check'],capture_output=True);raw=q.stdout;hits=[]
for line in raw.decode().splitlines():
 m=re.match(r'^(.+?):([0-9]+): (trailing whitespace|new blank line at EOF|space before tab in indent).*$',line)
 if m:hits.append(dict(path=m[1],line=int(m[2]),kind=m[3]))
assert q.returncode in [0,2] and (q.returncode==0 or hits)
bad={x['path'] for x in hits};assert all(p.startswith(r.as_posix()+'/') for p in bad)
authored=[p for p in paths if p not in bad]
for i in range(0,len(authored),64):subprocess.run(['git','-c','core.whitespace=cr-at-eol','diff','--cached','--check','--']+authored[i:i+64],check=True)
d=r/'frontier-search-repair65-v2/staging';d.mkdir();(d/'negative.raw.gz').write_bytes(gzip.compress(raw,mtime=0));(d/'diagnosis.json').write_text(json.dumps(dict(full_staged_exit=q.returncode,immutable_native_paths=[dict(path=p,RAW_sha256=sha(Path(p).read_bytes())) for p in sorted(bad)],negative_RAW_sha256=sha(raw),findings=hits,authored_complement_exit=0,full_staged_PASS=q.returncode==0,active_observer_excluded=active.as_posix()),indent=2)+'\n',encoding='utf-8',newline='\n');stage([p.as_posix() for p in d.iterdir()])
subprocess.run([sys.executable,'-X','utf8','tools/astis_publication.py','check','--base','dad6e38c9beed3476cb5d1db06eb57b955c8e3eb'],check=True)
subprocess.run(['git','commit','-q','-m','Record explicit Samplinglib reuse search for PBPS polar frontier'],check=True)
print('PASS corrected SCI65b',subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'one metadata field in each consistent search description; all proof/source bytes unchanged.')
