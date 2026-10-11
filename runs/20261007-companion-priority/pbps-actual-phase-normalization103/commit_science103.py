"""Commit reviewed SAU103 science only, with exact RAW archival and no primary-copy publication."""
from pathlib import Path
import json,hashlib,gzip,subprocess,sys
root=Path.cwd();r=Path(__file__).resolve().parent.relative_to(root);pre=r.parent/'pbps-phase-normalization-preread103';old=r.parent/'pbps-actual-weighted-sector102'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git',*a])
assert git('rev-parse','HEAD').decode().strip()=='86fad532c6217ba512ec0d146a7425338efb1a9c'
assert not git('diff','--cached','--name-only').strip()
assert subprocess.run(['git','merge-base','--is-ancestor','origin/main','HEAD']).returncode==0
sys.path.insert(0,str(root/'tools'));import astis_publication as pub
c=load(r/'claim.json');ap=Path('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261012-PBPSActualPhaseNormalization.json');a=load(ap)
assert a['state']=='accepted' and a['source_review']['state']=='accepted'
pub.check_advance(c['target_declarations'],reviewed=True)
assert sha(Path(c['proposed_files'][0]).read_bytes())=='c7806ada54ca78514a75ea1d13ed4bf08e5af4e92546d9ba0165683d77b36af4'
saved=load(old/'exact-commit-verification102/closed-RAW-manifest102.json')['preserved_collaborator_inputs']
for d in saved:assert sha(Path(d['path']).read_bytes())==d['raw_sha256'],d['path']
roots=[r,pre,Path('runs/semantic-roundtrip/anonymous103'),old/'next-primary103']
files=[]
for folder in roots:
 for p in sorted(folder.rglob('*')):
  if p.is_file() and not {'__pycache__','exact-commit-verification103','next-primary104'}.intersection(p.parts) and p.suffix not in {'.olean','.ilean','.pyc'}:files.append(p)
files += [Path(n) for n in [c['proposed_files'][0],f"research-wiki/frontier-cells/{c['frontier_cell']}.json",str(ap),'website/content/publications/pbps-actual-phase-normalization.json','website/content/declaration_lessons/pbps-actual-phase-normalization.json','runs/substantive_advances.jsonl']]
files += [old/'integration102/postpush-binding102.json',old/'integration102/push102.stdout.log',old/'integration102/push102.stderr.log']
archives=[];staged=[]
primary_hash='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
for p in sorted(set(files)):
 if not p.exists():continue
 name=p.as_posix();raw=p.read_bytes()
 assert name not in {d['path'] for d in saved}
 if sha(raw)==primary_hash:continue
 if p.suffix=='.gz' and sha(gzip.decompress(raw))==primary_hash:continue
 if p.suffix.lower() in {'.gz', '.png', '.jpg', '.jpeg', '.webp', '.pdf'}:
  git('-c','core.autocrlf=false','add','-f','--',name);staged.append(name);continue
 archive_only=name.startswith('runs/') and (p.suffix in {'.lean','.log','.html','.snapshot','.exactraw','.stdout','.stderr'} or 'exactraw.snapshot' in p.name or len(raw)>200000)
 normal=raw.replace(b'\r\n',b'\n')
 if name.startswith('runs/') and normal:
  normal=b'\n'.join(x.rstrip(b' \t') for x in normal.split(b'\n')).rstrip(b'\n')+b'\n'
 if archive_only or normal!=raw:
  z=Path(str(p)+'.gz')
  if z.exists() and gzip.decompress(z.read_bytes())!=raw:z=Path(str(p)+'.science103.raw.gz')
  assert not z.exists() or gzip.decompress(z.read_bytes())==raw,(p,z)
  if not z.exists():z.write_bytes(gzip.compress(raw,mtime=0))
  zn=z.as_posix();git('-c','core.autocrlf=false','add','-f','--',zn);staged.append(zn)
  archives.append(dict(raw_path=name,raw_sha256=sha(raw),archive=zn,archive_sha256=sha(z.read_bytes()),archive_only=archive_only,public_text_sha256=None if archive_only else sha(normal)))
 if not archive_only:
  blob=subprocess.check_output(['git','hash-object','-w','--stdin'],input=normal).decode().strip()
  subprocess.run(['git','update-index','--add','--cacheinfo','100644',blob,name],check=True);staged.append(name)
manifest=r/'science-staging103.json';assert not manifest.exists()
manifest.write_text(json.dumps(dict(files=staged,raw_archives=archives,preserved_collaborator_inputs=saved,source_review=a['source_review'],independent_math='independent-whole-math103/whole-math-decision103.native.json',scope='Reviewed science; independent exact-commit verification and aggregate integration pending'),indent=2)+'\n',encoding='utf8',newline='\n')
git('-c','core.autocrlf=false','add','--',manifest.as_posix())
q=subprocess.run(['git','diff','--cached','--check'],capture_output=True);(r/'science-staged-diff-check103.log').write_bytes(q.stdout+q.stderr);assert q.returncode==0,q.stdout.decode(errors='replace')[-5000:]
assert set(git('diff','--cached','--name-only').decode().splitlines())<=set(staged)|{manifest.as_posix()}
for d in saved:assert sha(Path(d['path']).read_bytes())==d['raw_sha256']
git('commit','-q','-m','Prove actual PBPS phase Gibbs normalization')
commit=git('rev-parse','HEAD').decode().strip()
(r/'science-commit103.receipt.json').write_text(json.dumps(dict(commit=commit,source_review='accepted',independent_exact_commit='pending',aggregate_integration='pending',collaborator_files_preserved=len(saved)),indent=2)+'\n',encoding='utf8',newline='\n')
print(commit,len(staged),'science files; independent exact-commit verification pending')
