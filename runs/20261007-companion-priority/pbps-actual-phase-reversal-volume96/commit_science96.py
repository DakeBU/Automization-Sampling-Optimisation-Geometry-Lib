"""Commit only reviewed SAU96 science and immutable evidence, preserving raw bytes."""
from pathlib import Path
import json,hashlib,gzip,subprocess,sys
root=Path.cwd();r=Path(__file__).resolve().parent.relative_to(root);pre=r.parent/'pbps-phase-reversal-volume-preread96';old=r.parent/'pbps-actual-bounded-path-expansion95'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git',*a])
assert git('rev-parse','HEAD').decode().strip()=='45e1f1457b59446dc4d1774cea510775c331d590'
existing_staged=set(git('diff','--cached','--name-only').decode().splitlines())
assert subprocess.run(['git','merge-base','--is-ancestor','origin/main','HEAD']).returncode==0
sys.path.insert(0,str(root/'tools'));import astis_publication as pub
c=load(r/'claim.json');ap=Path('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261011-PBPSActualPhaseReversalVolume.json');a=load(ap)
assert a['state']=='accepted' and a['source_review']['state']=='accepted'
pub.check_advance(c['target_declarations'],reviewed=True)
assert sha(Path(c['proposed_files'][0]).read_bytes())=='4b144dfa25d9521803e37518b8a6386fff08396c5804e410e9be593d46833a7b'
saved=load(old/'exact-commit-verification95/closed-RAW-manifest95.json')['preserved_collaborator_inputs']
for d in saved:assert sha(Path(d['path']).read_bytes())==d['raw_sha256'],d['path']
roots=[r,pre,Path('runs/semantic-roundtrip/anonymous96')]
files=[]
for folder in roots:
    for p in sorted(folder.rglob('*')):
        if p.is_file() and not {'__pycache__','next-primary97','exact-commit-verification96'}.intersection(p.parts) and p.suffix not in {'.olean','.ilean','.pyc'}:files.append(p)
files += [Path(n) for n in [c['proposed_files'][0],f"research-wiki/frontier-cells/{c['frontier_cell']}.json",str(ap),'website/content/publications/pbps-actual-phase-reversal-volume.json','website/content/declaration_lessons/pbps-actual-phase-reversal-volume.json','runs/substantive_advances.jsonl']]
files += [old/'integration95/push-confirmation95.json']
allowed={p.as_posix() for p in files}|{p.as_posix()+'.gz' for p in files}|{p.as_posix()+'.science96.raw.gz' for p in files}
assert existing_staged<=allowed,existing_staged-allowed
archives=[];staged=[]
for p in sorted(set(files)):
    name=p.as_posix();raw=p.read_bytes()
    assert name not in {d['path'] for d in saved}
    if sha(raw)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760':continue
    if p.suffix=='.gz':
        git('-c','core.autocrlf=false','add','-f','--',name);staged.append(name);continue
    archive_only=name.startswith('runs/') and (p.suffix in {'.lean','.log','.html','.snapshot'} or 'exactraw.snapshot' in p.name or len(raw)>200000)
    normal=raw.replace(b'\r\n',b'\n')
    if name.startswith('runs/') and normal:
        normal=b'\n'.join(x.rstrip(b' \t') for x in normal.split(b'\n')).rstrip(b'\n')+b'\n'
    if archive_only or normal!=raw:
        z=Path(str(p)+'.gz')
        if z.exists() and gzip.decompress(z.read_bytes())!=raw:
            z=Path(str(p)+'.science96.raw.gz')
        assert not z.exists() or gzip.decompress(z.read_bytes())==raw,(p,z)
        if not z.exists():z.write_bytes(gzip.compress(raw,mtime=0))
        zn=z.as_posix();git('-c','core.autocrlf=false','add','-f','--',zn);staged.append(zn)
        archives.append(dict(raw_path=name,raw_sha256=sha(raw),archive=zn,archive_sha256=sha(z.read_bytes()),archive_only=archive_only,public_text_sha256=None if archive_only else sha(normal)))
    if not archive_only:
        blob=subprocess.check_output(['git','hash-object','-w','--stdin'],input=normal).decode().strip()
        subprocess.run(['git','update-index','--add','--cacheinfo','100644',blob,name],check=True);staged.append(name)
manifest=r/'science-staging96.json';assert not manifest.exists()
manifest.write_text(json.dumps(dict(files=staged,raw_archives=archives,preserved_collaborator_inputs=saved,source_review=a['source_review'],independent_math='independent-whole-math96/whole-math-decision96.native.json',scope='Reviewed science; independent exact-commit verification and aggregate integration pending'),indent=2)+'\n',encoding='utf8',newline='\n')
git('-c','core.autocrlf=false','add','--',manifest.as_posix())
q=subprocess.run(['git','diff','--cached','--check'],capture_output=True);(r/'science-staged-diff-check96.log').write_bytes(q.stdout+q.stderr);assert q.returncode==0,q.stdout.decode(errors='replace')[-5000:]
assert set(git('diff','--cached','--name-only').decode().splitlines())<=set(staged)|{manifest.as_posix()}
for d in saved:assert sha(Path(d['path']).read_bytes())==d['raw_sha256']
git('commit','-q','-m','Prove actual PBPS phase-volume preservation and reversal laws')
commit=git('rev-parse','HEAD').decode().strip()
(r/'science-commit96.receipt.json').write_text(json.dumps(dict(commit=commit,source_review='accepted',independent_exact_commit='pending',aggregate_integration='pending',collaborator_files_preserved=len(saved)),indent=2)+'\n',encoding='utf8',newline='\n')
print(commit,len(staged),'science files; independent exact-commit verification pending')
