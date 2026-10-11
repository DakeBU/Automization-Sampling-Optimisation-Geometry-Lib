"""Commit only this independently reviewed science packet; aggregate integration is later."""
from pathlib import Path
import json,hashlib,gzip,subprocess,sys
R=Path(__file__).resolve().parents[3];run=Path(__file__).resolve().parent
load=lambda p:json.loads(p.read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=R)
assert git('rev-parse','HEAD').decode().strip()=='87975b5682bec621644b12e701aa5e45fefc3c2d'
assert not git('diff','--cached','--name-only').strip()
assert subprocess.run(['git','merge-base','--is-ancestor','origin/main','HEAD'],cwd=R).returncode==0
sys.path.insert(0,str(R/'tools'));import astis_publication as pub
claim=load(run/'claim.json');pub.check_advance(claim['target_declarations'],reviewed=True)
audit=load(R/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261011-PBPSActualPrescribedPathDensity.json')
assert audit['state']=='accepted' and audit['source_review']['state']=='accepted'
assert sha((R/claim['proposed_files'][0]).read_bytes())=='60792981d3d2bac30d78a2373f7eed0002def8600e92553e9b5b0c87761599ec'
saved=load(run.parent/'pbps-actual-finite-count-path93/exact-commit-verification93/closed-RAW-manifest93.json')['preserved_collaborator_inputs']
for x in saved:assert sha((R/x['path']).read_bytes())==x['raw_sha256'],x['path']
roots=[run,run.parent/'pbps-prescribed-path-density-preread94',run.parent/'pbps-actual-finite-count-path93/next-source-graph94',R/'runs/semantic-roundtrip/anonymous94']
files=[]
for p in roots:
 for q in sorted(p.rglob('*')):
  if q.is_file() and '__pycache__' not in q.parts and q.suffix not in {'.olean','.ilean','.pyc','.gz'}:files.append(q)
files += [R/x for x in [claim['proposed_files'][0],'research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-prescribed-path-density.json','research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261011-PBPSActualPrescribedPathDensity.json','website/content/publications/pbps-actual-prescribed-path-density.json','website/content/declaration_lessons/pbps-actual-prescribed-path-density.json','runs/substantive_advances.jsonl']]
archives=[];staged=[]
for p in sorted(set(files)):
 name=p.relative_to(R).as_posix();raw=p.read_bytes()
 assert name not in {x['path'] for x in saved}
 archive_only=name.startswith('runs/') and (p.suffix=='.lean' or 'exactraw.snapshot' in p.name or len(raw)>200000)
 normal=raw.replace(b'\r\n',b'\n')
 if name.startswith('runs/'):
  normal=b'\n'.join(x.rstrip(b' \t') for x in normal.split(b'\n')).rstrip(b'\n')+b'\n' if normal else b''
 if archive_only or normal!=raw:
  z=Path(str(p)+'.gz');assert not z.exists() or gzip.decompress(z.read_bytes())==raw
  if not z.exists():z.write_bytes(gzip.compress(raw,mtime=0))
  zname=z.relative_to(R).as_posix();git('-c','core.autocrlf=false','add','-f','--',zname);staged.append(zname)
  archives.append(dict(raw_path=name,raw_sha256=sha(raw),archive=zname,archive_sha256=sha(z.read_bytes()),archive_only=archive_only,public_text_sha256=None if archive_only else sha(normal)))
 if not archive_only:
  blob=subprocess.check_output(['git','hash-object','-w','--stdin'],input=normal,cwd=R).decode().strip()
  subprocess.run(['git','update-index','--add','--cacheinfo','100644',blob,name],cwd=R,check=True);staged.append(name)
manifest=run/'science-staging94.json';assert not manifest.exists()
manifest.write_bytes((json.dumps(dict(files=staged,raw_archives=archives,preserved_collaborator_inputs=saved,source_review=audit['source_review'],independent_math='independent-whole-math94/lf-transfer94/LF-transfer-decision94.native.json',scope='Science commit only; exact-commit verifier and aggregate integration pending'),indent=2)+'\n').encode())
git('-c','core.autocrlf=false','add','--',manifest.relative_to(R).as_posix())
check=subprocess.run(['git','diff','--cached','--check'],cwd=R,capture_output=True)
(run/'science-staged-diff-check94.log').write_bytes(check.stdout+check.stderr)
assert check.returncode==0,check.stdout.decode(errors='replace')[-6000:]
assert set(git('diff','--cached','--name-only').decode().splitlines())<=set(staged)|{manifest.relative_to(R).as_posix()}
for x in saved:assert sha((R/x['path']).read_bytes())==x['raw_sha256']
git('commit','-q','-m','Prove actual PBPS prescribed-path hazard and density identity')
commit=git('rev-parse','HEAD').decode().strip()
(run/'science-commit94.receipt.json').write_bytes((json.dumps(dict(commit=commit,source_review='accepted',independent_exact_commit='pending',aggregate_integration='pending',collaborator_files_preserved=len(saved)),indent=2)+'\n').encode())
print(commit,len(staged),'science files; exact-commit verification pending')
