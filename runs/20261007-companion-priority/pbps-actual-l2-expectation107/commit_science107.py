"""Commit reviewed SAU107 science only, with exact RAW archival and no primary-copy publication."""
from pathlib import Path
import json,hashlib,gzip,subprocess,sys
root=Path.cwd();r=Path(__file__).resolve().parent.relative_to(root);pre=r.parent/'pbps-actual-l2-expectation-preread107';old=r.parent/'pbps-actual-bounded-gibbs-duality106'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git','-c','core.autocrlf=false','-c','core.fscache=false',*a])
assert git('rev-parse','HEAD').decode().strip()=='3b751684524a228265731d27dd43519036b35bc3'
assert not git('diff','--cached','--name-only').strip()
assert git('rev-parse','origin/main').decode().strip()=='26dce3a7442577b8bdfbfb20e8b77f681c052528'
# The fetched upstream main is already an ancestor; preserve all unrelated local modifications.
assert subprocess.run(['git','merge-base','--is-ancestor','origin/main','HEAD']).returncode == 0
sys.path.insert(0,str(root/'tools'));import astis_publication as pub
c=load(r/'claim.json');ap=Path('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261012-PBPSActualL2Expectation.json');a=load(ap)
assert a['state']=='accepted' and a['source_review']['state']=='accepted'
pub.check_advance(c['target_declarations'],reviewed=True)
assert sha(Path(c['proposed_files'][0]).read_bytes())=='4c35e0b71362bec3563e3d07c9f122d6b7ca4cae604f7a88aad397d2a028f4d6'
saved=load(old/'exact-commit-verification106/closed-RAW-manifest106.json')['preserved_collaborator_inputs']
for d in saved:assert sha(Path(d['path']).read_bytes())==d['raw_sha256'],d['path']
# Preserve the committed ledger prefix and normalize only this unit's appended events.
ledger=Path('runs/substantive_advances.jsonl');before=ledger.read_bytes();prefix=git('show','HEAD:runs/substantive_advances.jsonl')
assert before.startswith(prefix)
tail=before[len(prefix):]
assert all(json.loads(line)['advance_id']==c['advance_id'] for line in tail.splitlines())
normalized_tail=tail.replace(b'\r\n',b'\n')
assert tail.splitlines()==normalized_tail.splitlines()
if normalized_tail!=tail:
 z=r/'ledger-before-owned-tail-EOL107.exactraw.gz';assert not z.exists();z.write_bytes(gzip.compress(before,mtime=0))
 ledger.write_bytes(prefix+normalized_tail)
 (r/'ledger-owned-tail-EOL107.json').write_text(json.dumps(dict(committed_prefix_unchanged=True,all_record_payloads_unchanged=True,only_owned_advance=c['advance_id'],events=len(tail.splitlines()),before_raw_sha256=sha(before),after_raw_sha256=sha(ledger.read_bytes()),original_archive=z.as_posix()),indent=2)+'\n',encoding='utf8',newline='\n')
roots=[r,pre,Path('runs/semantic-roundtrip/anonymous107'),old/'next-primary107']
files=[]
for folder in roots:
 for p in sorted(folder.rglob('*')):
  if p.is_file() and not {'__pycache__','exact-commit-verification107','next-primary108','upstream-reconciliation107'}.intersection(p.parts) and p.suffix not in {'.olean','.ilean','.pyc'}:files.append(p)
files += [Path(n) for n in [c['proposed_files'][0],f"research-wiki/frontier-cells/{c['frontier_cell']}.json",str(ap),'website/content/publications/pbps-actual-l2-expectation.json','website/content/declaration_lessons/pbps-actual-l2-expectation.json','runs/substantive_advances.jsonl']]
# Prior delivery already committed separately; do not restage it.
archives=[];staged=[]
primary_hash='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
for p in sorted(set(files)):
 if not p.exists():continue
 name=p.as_posix();raw=p.read_bytes()
 if name == 'runs/substantive_advances.jsonl':
  prior=git('show','HEAD:'+name)
  assert raw.startswith(prior), 'Canonical ledger prefix must remain byte-identical'
  assert all(json.loads(line)['advance_id']==c['advance_id'] for line in raw[len(prior):].splitlines()), 'Only owned107 events may append'
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
  if z.exists() and gzip.decompress(z.read_bytes())!=raw:z=Path(str(p)+'.science107.raw.gz')
  assert not z.exists() or gzip.decompress(z.read_bytes())==raw,(p,z)
  if not z.exists():z.write_bytes(gzip.compress(raw,mtime=0))
  zn=z.as_posix();git('-c','core.autocrlf=false','add','-f','--',zn);staged.append(zn)
  archives.append(dict(raw_path=name,raw_sha256=sha(raw),archive=zn,archive_sha256=sha(z.read_bytes()),archive_only=archive_only,public_text_sha256=None if archive_only else sha(normal)))
 if not archive_only:
  blob=subprocess.check_output(['git','hash-object','-w','--stdin'],input=normal).decode().strip()
  subprocess.run(['git','update-index','--add','--cacheinfo','100644',blob,name],check=True);staged.append(name)
manifest=r/'science-staging107.json';assert not manifest.exists()
manifest.write_text(json.dumps(dict(files=staged,raw_archives=archives,preserved_collaborator_inputs=saved,source_review=a['source_review'],independent_math='independent-whole-math107/whole-math-decision107.native.json',scope='Reviewed science; independent exact-commit verification, aggregate integration pending'),indent=2)+'\n',encoding='utf8',newline='\n')
git('-c','core.autocrlf=false','add','--',manifest.as_posix())
q=subprocess.run(['git','diff','--cached','--check'],capture_output=True);(r/'science-staged-diff-check107.log').write_bytes(q.stdout+q.stderr);assert q.returncode==0,q.stdout.decode(errors='replace')[-5000:]
assert set(git('diff','--cached','--name-only').decode().splitlines())<=set(staged)|{manifest.as_posix()}
for d in saved:assert sha(Path(d['path']).read_bytes())==d['raw_sha256']
git('commit','-q','-m','Prove actual PBPS L2 expectation contraction and zero-time identity')
commit=git('rev-parse','HEAD').decode().strip()
(r/'science-commit107.receipt.json').write_text(json.dumps(dict(commit=commit,source_review='accepted',independent_exact_commit='pending',aggregate_integration='pending',collaborator_files_preserved=len(saved)),indent=2)+'\n',encoding='utf8',newline='\n')
print(commit,len(staged),'science files; independent exact-commit verification pending')
