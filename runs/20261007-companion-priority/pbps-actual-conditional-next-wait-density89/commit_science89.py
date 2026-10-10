"""Publish only independently admitted local89; exclude all unrelated edits."""
from pathlib import Path
import gzip,hashlib,json,subprocess
r=Path(__file__).parent;pre=r.parent/'pbps-conditional-next-wait-density-preread89';load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
claim=load(r/'claim.json');assert load(r/'root.source89.adoption.json')['status']=='ACCEPTED_INDEPENDENT_SOURCE_FIDELITY_ONLY'
assert load(r/'root.math89.adoption.json')['status']=='ACCEPTED_INDEPENDENT_MATH_ONLY'
assert (r/'proved-local89.json').exists()
for label in ['publication','semantic','frontier','contributor','contributor-regressions','python-compile']:
 receipt=load(r/'checks89'/('proved-local-frontier' if label=='frontier' else label)/'receipt.json');assert receipt['terminal_closed'] and receipt['exit_code']==0,label
 assert receipt['module_raw_sha256']=='36813b659cbdbb4b31c6300abd1300858d42afe683046b8c06ff9c22806e8e37'
assert not subprocess.check_output(['git','diff','--cached','--name-only'],text=True).strip()
saved=load(pre/'pre-fetch89.workspace-RAW.json')['tracked_modified'];assert len(saved)==21
for p,h in saved.items():assert sha(Path(p).read_bytes())==h,p
ledger=Path('runs/substantive_advances.jsonl');prefix=subprocess.check_output(['git','show','HEAD:runs/substantive_advances.jsonl']);raw=ledger.read_bytes();assert raw.startswith(prefix)
tail=raw[len(prefix):];events=[json.loads(x) for x in tail.splitlines() if x.strip()];assert events and all(x['advance_id']==claim['advance_id'] for x in events)
# Only coordinator-owned new89 ledger tail is normalized. Native evidence stays RAW.
ledger.write_bytes(prefix+tail.replace(b'\r\n',b'\n'))
def publishable(p):
 return '.private.' not in p.name and '__pycache__' not in p.parts and p.suffix not in {'.pyc','.olean','.ilean','.c','.o','.ir'} and not p.name.endswith('.text.txt') and sha(p.read_bytes())!='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
folders=[r,pre,Path('runs/semantic-decoder-inputs/round89'),Path('runs/semantic-decoder-outputs/round89')]
private_paths=[p.as_posix() for folder in folders for p in folder.rglob('*') if p.is_file() and not publishable(p)]
(r/'public-source-exclusions89.json').write_text(json.dumps(dict(reason='Only attributed mathematical restatements are published; preserve primary long extracts locally without publishing archives.',paths=sorted(private_paths)),indent=2)+'\n',encoding='utf8',newline='\n')
rows=[];excluded_native=set()
for folder in folders:
 for p in sorted(folder.rglob('*')):
  if not p.is_file() or not publishable(p) or p.suffix not in {'.log','.diff','.html','.lean','.snapshot'}:continue
  b=p.read_bytes();z=Path(str(p)+'.gz')
  if not z.exists():z.write_bytes(gzip.compress(b,mtime=0))
  assert gzip.decompress(z.read_bytes())==b,p;excluded_native.add(p.as_posix())
  rows.append(dict(raw_path=p.as_posix(),raw_bytes=len(b),raw_sha256=sha(b),archive=z.as_posix(),archive_raw_sha256=sha(z.read_bytes())))
(r/'immutable-RAW-archives89.json').write_text(json.dumps(dict(status='RAW_NATIVE_RETAINED_LOSSLESS_ARCHIVES',files=rows),indent=2)+'\n',encoding='utf8',newline='\n')
paths=claim['proposed_files']+['research-wiki/frontier-cells/'+claim['frontier_cell']+'.json','research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261011-PBPSActualConditionalNextWaitDensity.json','website/content/declaration_lessons/pbps-actual-conditional-next-wait-density.json','website/content/publications/pbps-actual-conditional-next-wait-density.json','runs/substantive_advances.jsonl']
for folder in folders:
 paths += [p.as_posix() for p in folder.rglob('*') if p.is_file() and publishable(p) and p.as_posix() not in excluded_native and p.suffix not in {'.log','.diff','.html','.lean','.snapshot'}]
paths=sorted({Path(p).resolve().relative_to(Path.cwd()).as_posix() for p in paths});assert not set(paths).intersection(saved)
inventory=[dict(path=p,raw_bytes=Path(p).stat().st_size,raw_sha256=sha(Path(p).read_bytes())) for p in paths]
p=r/'science-staging89.json';assert not p.exists();p.write_text(json.dumps(dict(files=inventory,preserved_collaborator_modified_files=21,source_review='accepted',exact_commit_verification='pending',aggregate='pending',Goal_complete=False),indent=2)+'\n',encoding='utf8',newline='\n');paths.append(p.resolve().relative_to(Path.cwd()).as_posix())
for offset in range(0,len(paths),25):subprocess.run(['git','-c','core.autocrlf=false','add','-f','--',*paths[offset:offset+25]],check=True)
actual=set(subprocess.check_output(['git','diff','--cached','--name-only'],text=True).splitlines());assert actual==set(paths)
q=subprocess.run(['git','-c','core.whitespace=cr-at-eol','diff','--cached','--check'],capture_output=True);log=r/'science-staged-whitespace89.log';assert not log.exists();log.write_bytes(q.stdout+q.stderr);assert q.returncode==0,(q.stdout+q.stderr).decode(errors='replace')[-2000:]
subprocess.run(['git','commit','-q','-m','Prove actual PBPS conditional finite next-wait density'],check=True)
print('SCIENCE_COMMIT',subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip())
