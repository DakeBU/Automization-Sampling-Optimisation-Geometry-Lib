from pathlib import Path
import gzip,hashlib,json,subprocess
r=Path(__file__).parent;pre=r.parent/'pbps-bounded-test-preread83';load=lambda p:json.loads(Path(p).read_bytes())
assert load(r/'root.source83.adoption.json')['publication_binding_unchanged']
assert load(r/'root.math83.adoption.json')['status']=='ACCEPTED_INDEPENDENT_MATH_ONLY'
assert not subprocess.check_output(['git','diff','--cached','--name-only'],text=True).strip()
saved=load(pre/'post-fetch83.workspace-RAW.corrected.json')['tracked_modified'];assert len(saved)==21
for p,h in saved.items():assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==h,p
rows=[];excluded_native=set()
for folder in [r,pre]:
 for p in sorted(folder.rglob('*')):
  if not p.is_file() or p.suffix not in {'.log','.diff'}:continue
  b=p.read_bytes();z=Path(str(p)+'.gz')
  if not z.exists():z.write_bytes(gzip.compress(b,mtime=0))
  assert gzip.decompress(z.read_bytes())==b;excluded_native.add(p.as_posix())
  rows.append(dict(raw_path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=hashlib.sha256(b).hexdigest(),archive=z.as_posix(),archive_RAW_sha256=hashlib.sha256(z.read_bytes()).hexdigest()))
(r/'immutable-whitespace-archives83.json').write_text(json.dumps(dict(status='RAW_NATIVE_RETAINED_LOSSLESS_ARCHIVES',files=rows),indent=2)+'\n',encoding='utf8',newline='\n')
paths=['AutoSamplingTheory/ExampleCases/ProximalBPS/ActualBoundedTestContinuity.lean','research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-bounded-test-continuity.json','research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261010-PBPSActualBoundedTestContinuity.json','website/content/declaration_lessons/pbps-actual-bounded-test-continuity.json','website/content/publications/pbps-actual-bounded-test-continuity.json','runs/substantive_advances.jsonl']
excluded={'.pyc','.html','.log','.diff','.olean','.ilean','.c','.o','.ir'}
for folder in [r,pre]:
 paths += [p.as_posix() for p in folder.rglob('*') if p.is_file() and p.as_posix() not in excluded_native and p.suffix not in excluded and not p.name.endswith('.text.txt') and '__pycache__' not in p.parts]
paths=sorted(set(paths));assert all(Path(p).exists() for p in paths)
inventory=[dict(path=p,RAW_bytes=Path(p).stat().st_size,RAW_sha256=hashlib.sha256(Path(p).read_bytes()).hexdigest()) for p in paths]
(r/'science-staging83.json').write_text(json.dumps(dict(files=inventory,preserved_collaborator_modified_files=21,source_review='accepted',exact_commit_verification='pending',aggregate='pending',Goal_complete=False),indent=2)+'\n',encoding='utf8',newline='\n')
paths.append((r/'science-staging83.json').as_posix())
for offset in range(0,len(paths),25):subprocess.run(['git','-c','core.autocrlf=false','add','-f','--',*paths[offset:offset+25]],check=True)
q=subprocess.run(['git','-c','core.whitespace=cr-at-eol','diff','--cached','--check'],capture_output=True)
(r/'science-stage-whitespace83.log').write_bytes(q.stdout+q.stderr);assert q.returncode==0,(q.stdout+q.stderr).decode(errors='replace')[:4000]
subprocess.run(['git','commit','-q','-m','Prove actual PBPS bounded-test clock integrability and expectation continuity'],check=True)
print('SCIENCE_COMMIT',subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip())
