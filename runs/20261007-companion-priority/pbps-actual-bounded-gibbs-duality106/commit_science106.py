"""Commit reviewed SAU106 science only, with exact RAW archival and no primary-copy publication."""
from pathlib import Path
import json,hashlib,gzip,subprocess,sys
root=Path.cwd();r=Path(__file__).resolve().parent.relative_to(root);pre=r.parent/'pbps-bounded-gibbs-duality-preread106';old=r.parent/'pbps-actual-countable-endpoint105'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git','-c','core.autocrlf=false','-c','core.fscache=false',*a])
assert git('rev-parse','HEAD').decode().strip()=='bd25af52d971654773edcfeb15bc8e09fb9b76ae'
assert not git('diff','--cached','--name-only').strip()
assert git('rev-parse','origin/main').decode().strip()=='a3a3fc3f2d34c5a013168bea1446a106054c194c'
# Safe upstream synchronization is pending integration, explicitly recorded in Statement Seal.
sys.path.insert(0,str(root/'tools'));import astis_publication as pub
c=load(r/'claim.json');ap=Path('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261012-PBPSActualBoundedGibbsDuality.json');a=load(ap)
assert a['state']=='accepted' and a['source_review']['state']=='accepted'
pub.check_advance(c['target_declarations'],reviewed=True)
assert sha(Path(c['proposed_files'][0]).read_bytes())=='4fad17d78149b7a4a784170309e9de3f70941ef533f90228b0405dee5fc2707d'
saved=load(old/'exact-commit-verification105/closed-RAW-manifest105.json')['preserved_collaborator_inputs']
for d in saved:assert sha(Path(d['path']).read_bytes())==d['raw_sha256'],d['path']
roots=[r,pre,Path('runs/semantic-roundtrip/anonymous106'),old/'next-primary106']
files=[]
for folder in roots:
 for p in sorted(folder.rglob('*')):
  if p.is_file() and not {'__pycache__','exact-commit-verification106','next-primary107','upstream-reconciliation106'}.intersection(p.parts) and p.suffix not in {'.olean','.ilean','.pyc'}:files.append(p)
files += [Path(n) for n in [c['proposed_files'][0],f"research-wiki/frontier-cells/{c['frontier_cell']}.json",str(ap),'website/content/publications/pbps-actual-bounded-gibbs-duality.json','website/content/declaration_lessons/pbps-actual-bounded-gibbs-duality.json','runs/substantive_advances.jsonl']]
# Prior delivery already committed separately; do not restage it.
archives=[];staged=[]
primary_hash='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
for p in sorted(set(files)):
 if not p.exists():continue
 name=p.as_posix();raw=p.read_bytes()
 if name == 'runs/substantive_advances.jsonl':
  prior=git('show','HEAD:'+name)
  assert raw.startswith(prior), 'Canonical ledger prefix must remain byte-identical'
  assert all(json.loads(line)['advance_id']==c['advance_id'] for line in raw[len(prior):].splitlines()), 'Only owned106 events may append'
 assert name not in {d['path'] for d in saved}
 if sha(raw)==primary_hash:continue
 if p.suffix=='.gz' and sha(gzip.decompress(raw))==primary_hash:continue
 if p.suffix.lower() in {'.gz', '.png', '.jpg', '.jpeg', '.webp', '.pdf'}:
  git('-c','core.autocrlf=false','add','-f','--',name);staged.append(name);continue
 archive_only=name != 'runs/substantive_advances.jsonl' and name.startswith('runs/') and (p.suffix in {'.lean','.log','.html','.snapshot','.exactraw','.stdout','.stderr'} or 'exactraw.snapshot' in p.name or len(raw)>200000)
 normal=raw.replace(b'\r\n',b'\n')
 if name.startswith('runs/') and normal:
  normal=b'\n'.join(x.rstrip(b' \t') for x in normal.split(b'\n')).rstrip(b'\n')+b'\n'
 if archive_only or normal!=raw:
  z=Path(str(p)+'.gz')
  if z.exists() and gzip.decompress(z.read_bytes())!=raw:z=Path(str(p)+'.science106.raw.gz')
  assert not z.exists() or gzip.decompress(z.read_bytes())==raw,(p,z)
  if not z.exists():z.write_bytes(gzip.compress(raw,mtime=0))
  zn=z.as_posix();git('-c','core.autocrlf=false','add','-f','--',zn);staged.append(zn)
  archives.append(dict(raw_path=name,raw_sha256=sha(raw),archive=zn,archive_sha256=sha(z.read_bytes()),archive_only=archive_only,public_text_sha256=None if archive_only else sha(normal)))
 if not archive_only:
  blob=subprocess.check_output(['git','hash-object','-w','--stdin'],input=normal).decode().strip()
  subprocess.run(['git','update-index','--add','--cacheinfo','100644',blob,name],check=True);staged.append(name)
manifest=r/'science-staging106.json';assert not manifest.exists()
manifest.write_text(json.dumps(dict(files=staged,raw_archives=archives,preserved_collaborator_inputs=saved,source_review=a['source_review'],independent_math='independent-whole-math106/whole-math-decision106.native.json',scope='Reviewed science; independent exact-commit verification, sphere-Rayleigh main reconciliation and aggregate integration pending'),indent=2)+'\n',encoding='utf8',newline='\n')
git('-c','core.autocrlf=false','add','--',manifest.as_posix())
q=subprocess.run(['git','diff','--cached','--check'],capture_output=True);(r/'science-staged-diff-check106.log').write_bytes(q.stdout+q.stderr);assert q.returncode==0,q.stdout.decode(errors='replace')[-5000:]
assert set(git('diff','--cached','--name-only').decode().splitlines())<=set(staged)|{manifest.as_posix()}
for d in saved:assert sha(Path(d['path']).read_bytes())==d['raw_sha256']
git('commit','-q','-m','Prove actual PBPS bounded Gibbs duality and fixed-time invariance')
commit=git('rev-parse','HEAD').decode().strip()
(r/'science-commit106.receipt.json').write_text(json.dumps(dict(commit=commit,source_review='accepted',independent_exact_commit='pending',aggregate_integration='pending',collaborator_files_preserved=len(saved)),indent=2)+'\n',encoding='utf8',newline='\n')
print(commit,len(staged),'science files; independent exact-commit verification pending')
