from pathlib import Path
import gzip,hashlib,json,subprocess
r=Path(__file__).parent;pre=r.parent/'pbps-transition-kernel-preread85';load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
claim=load(r/'claim.json');assert load(r/'root.source85.adoption.json')['publication_binding_unchanged']
assert load(r/'root.math85.adoption.json')['status']=='ACCEPTED_INDEPENDENT_MATH_ONLY'
cached=set(subprocess.check_output(['git','diff','--cached','--name-only'],text=True).splitlines())
if cached:
 prior=load(r/'science-staging85.attempt1.json');allowed={Path(x['path']).resolve().relative_to(Path.cwd()).as_posix() for x in prior['files']}|{(r/'science-staging85.json').resolve().relative_to(Path.cwd()).as_posix()}
 assert cached.issubset(allowed) and load(r/'science-staging-diagnosis85.json')['all_staged_paths_owned']
saved=load(pre/'pre-fetch85.workspace-RAW.json')['tracked_modified'];assert len(saved)==21
for p,h in saved.items():assert sha(Path(p).read_bytes())==h,p
ledger=Path('runs/substantive_advances.jsonl');prefix=subprocess.check_output(['git','show','HEAD:runs/substantive_advances.jsonl']);raw=ledger.read_bytes();assert raw.startswith(prefix)
tail=raw[len(prefix):];events=[json.loads(x) for x in tail.splitlines() if x.strip()]
assert events and all(x['advance_id']==claim['advance_id'] for x in events)
ledger.write_bytes(prefix+tail.replace(b'\r\n',b'\n'))
rows=[];excluded_native=set()
for folder in [r,pre]:
 for p in sorted(folder.rglob('*')):
  if not p.is_file() or p.suffix not in {'.log','.diff'}:continue
  b=p.read_bytes();z=Path(str(p)+'.gz')
  if not z.exists():z.write_bytes(gzip.compress(b,mtime=0))
  assert gzip.decompress(z.read_bytes())==b;excluded_native.add(p.as_posix())
  rows.append(dict(raw_path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),archive=z.as_posix(),archive_RAW_sha256=sha(z.read_bytes())))
(r/'immutable-whitespace-archives85.json').write_text(json.dumps(dict(status='RAW_NATIVE_RETAINED_LOSSLESS_ARCHIVES',files=rows),indent=2)+'\n',encoding='utf8',newline='\n')
paths=claim['proposed_files']+['research-wiki/frontier-cells/'+claim['frontier_cell']+'.json','research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261011-PBPSActualPhaseTransitionKernel.json','website/content/declaration_lessons/pbps-actual-phase-transition-kernel.json','website/content/publications/pbps-actual-phase-transition-kernel.json','runs/substantive_advances.jsonl']
excluded={'.pyc','.html','.log','.diff','.olean','.ilean','.c','.o','.ir'}
for folder in [r,pre]:
 paths += [p.as_posix() for p in folder.rglob('*') if p.is_file() and p.as_posix() not in excluded_native and p.suffix not in excluded and not p.name.endswith('.text.txt') and '__pycache__' not in p.parts]
paths=sorted({Path(p).resolve().relative_to(Path.cwd()).as_posix() for p in paths});assert all(Path(p).exists() for p in paths)
assert not set(paths).intersection(saved)
inventory=[dict(path=p,RAW_bytes=Path(p).stat().st_size,RAW_sha256=sha(Path(p).read_bytes())) for p in paths]
(r/'science-staging85.json').write_text(json.dumps(dict(files=inventory,preserved_collaborator_modified_files=21,source_review='accepted',exact_commit_verification='pending',aggregate='pending',Goal_complete=False),indent=2)+'\n',encoding='utf8',newline='\n')
paths.append((r/'science-staging85.json').as_posix())
for offset in range(0,len(paths),25):subprocess.run(['git','-c','core.autocrlf=false','add','-f','--',*paths[offset:offset+25]],check=True)
actual=set(subprocess.check_output(['git','diff','--cached','--name-only'],text=True).splitlines())
assert actual.issubset(set(paths)) and set(claim['proposed_files']).issubset(actual)
q=subprocess.run(['git','-c','core.whitespace=cr-at-eol','diff','--cached','--check'],capture_output=True)
(r/'science-stage-whitespace85.log').write_bytes(q.stdout+q.stderr);assert q.returncode==0,(q.stdout+q.stderr).decode(errors='replace')[:4000]
subprocess.run(['git','commit','-q','-m','Prove actual PBPS jointly indexed full-phase probability kernel'],check=True)
print('SCIENCE_COMMIT',subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip())
