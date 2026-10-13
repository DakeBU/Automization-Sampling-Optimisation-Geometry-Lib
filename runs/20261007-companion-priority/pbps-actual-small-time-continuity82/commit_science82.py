from pathlib import Path
import gzip,hashlib,json,subprocess
r=Path(__file__).parent
assert json.loads((r/'root.source82.adoption.json').read_bytes())['publication_binding_unchanged']
assert json.loads((r/'root.math82.adoption.json').read_bytes())['status']=='ACCEPTED_INDEPENDENT_MATH_ONLY'
assert not subprocess.check_output(['git','diff','--cached','--name-only'],text=True).strip()
saved=json.loads((r/'pre-fetch82.workspace-RAW.json').read_bytes())['tracked_modified']
for p,h in saved.items():assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==h,p
rows=[]
for p in sorted(r.rglob('*.log')):
 b=p.read_bytes();z=Path(str(p)+'.gz');assert not z.exists();z.write_bytes(gzip.compress(b,mtime=0));assert gzip.decompress(z.read_bytes())==b
 rows.append(dict(raw_path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=hashlib.sha256(b).hexdigest(),archive=z.as_posix(),archive_RAW_sha256=hashlib.sha256(z.read_bytes()).hexdigest()))
(r/'immutable-log-archives82.json').write_text(json.dumps(dict(status='RAW_LOGS_RETAINED_LOCALLY_LOSSLESS_PUBLIC_ARCHIVES',files=rows),indent=2)+'\n',encoding='utf8',newline='\n')
paths=['AutoSamplingTheory/ExampleCases/ProximalBPS/ActualSmallTimeContinuity.lean','research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-small-time-continuity.json','research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261010-PBPSActualSmallTimeContinuity.json','website/content/declaration_lessons/pbps-actual-small-time-continuity.json','website/content/publications/pbps-actual-small-time-continuity.json','runs/substantive_advances.jsonl']
excluded={'.pyc','.html','.log','.olean','.ilean','.c','.o','.ir'}
paths += [p.as_posix() for p in r.rglob('*') if p.is_file() and p.suffix not in excluded and not p.name.endswith('.text.txt') and '__pycache__' not in p.parts]
pre=Path('runs/20261007-companion-priority/pbps-process-regularity-preread82')
paths += [p.as_posix() for p in pre.rglob('*') if p.is_file() and p.suffix in {'.json','.md','.py'} and '__pycache__' not in p.parts]
paths=list(dict.fromkeys(paths));assert all(Path(p).exists() for p in paths)
inventory=[dict(path=p,RAW_bytes=Path(p).stat().st_size,RAW_sha256=hashlib.sha256(Path(p).read_bytes()).hexdigest()) for p in paths]
(r/'science-staging82.json').write_text(json.dumps(dict(files=inventory,preserved_collaborator_modified_files=len(saved),excluded='Unrelated collaborator files, full raw primary HTML/text copies and native compiler outputs remain local. Raw logs have lossless public archives.',source_review='accepted',exact_commit_verification='pending',aggregate='pending',Goal_complete=False),indent=2)+'\n',encoding='utf8',newline='\n')
paths.append((r/'science-staging82.json').as_posix())
subprocess.run(['git','-c','core.autocrlf=false','add','-f','--pathspec-from-file=-','--pathspec-file-nul'],input=('\0'.join(paths)+'\0').encode(),check=True)
p=subprocess.run(['git','-c','core.whitespace=cr-at-eol','diff','--cached','--check'],capture_output=True)
(r/'science-stage-whitespace82.log').write_bytes(p.stdout+p.stderr)
assert p.returncode==0,(p.stdout+p.stderr).decode(errors='replace')[:4000]
subprocess.run(['git','commit','-q','-m','Prove actual PBPS first-event defect and zero-time stochastic continuity'],check=True)
print('SCIENCE_COMMIT',subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip())
