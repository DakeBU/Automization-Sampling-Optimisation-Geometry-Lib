"""Commit only reviewed SAU95 science and immutable evidence, preserving raw bytes."""
from pathlib import Path
import json,hashlib,gzip,subprocess,sys
root=Path.cwd();r=Path(__file__).resolve().parent.relative_to(root);pre=r.parent/'pbps-bounded-path-expansion-preread95';old=r.parent/'pbps-actual-prescribed-path-density94'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git',*a])
assert git('rev-parse','HEAD').decode().strip()=='2ebf4ad2e323ad26f62fcf0c9859e66579549536'
existing_staged=set(git('diff','--cached','--name-only').decode().splitlines())
assert subprocess.run(['git','merge-base','--is-ancestor','origin/main','HEAD']).returncode==0
sys.path.insert(0,str(root/'tools'));import astis_publication as pub
c=load(r/'claim.json');ap=Path('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261011-PBPSActualBoundedPathExpansion.json');a=load(ap)
assert a['state']=='accepted' and a['source_review']['state']=='accepted'
pub.check_advance(c['target_declarations'],reviewed=True)
assert sha(Path(c['proposed_files'][0]).read_bytes())=='c3d4bcf73990d704244225ea647f44ed21fcbd339db49bf2c45f21af5b90d689'
saved=load(old/'exact-commit-verification94/closed-RAW-manifest94.json')['preserved_collaborator_inputs']
for d in saved:assert sha(Path(d['path']).read_bytes())==d['raw_sha256'],d['path']
roots=[r,pre,old/'next-source-graph95',old/'next-primary95',Path('runs/semantic-roundtrip/anonymous95')]
files=[]
for folder in roots:
    for p in sorted(folder.rglob('*')):
        if p.is_file() and not {'__pycache__','next-primary96'}.intersection(p.parts) and p.suffix not in {'.olean','.ilean','.pyc','.gz'}:files.append(p)
files += [Path(n) for n in [c['proposed_files'][0],f"research-wiki/frontier-cells/{c['frontier_cell']}.json",str(ap),'website/content/publications/pbps-actual-bounded-path-expansion.json','website/content/declaration_lessons/pbps-actual-bounded-path-expansion.json','runs/substantive_advances.jsonl']]
files += [old/'integration94/push-confirmation94.json',old/'integration94/pr315-body94.md']
allowed={p.as_posix() for p in files}|{p.as_posix()+'.gz' for p in files}|{p.as_posix()+'.science95.raw.gz' for p in files}
assert existing_staged<=allowed,existing_staged-allowed
archives=[];staged=[]
for p in sorted(set(files)):
    name=p.as_posix();raw=p.read_bytes()
    assert name not in {d['path'] for d in saved}
    if sha(raw)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760':continue
    archive_only=name.startswith('runs/') and (p.suffix in {'.lean','.log','.html','.snapshot'} or 'exactraw.snapshot' in p.name or len(raw)>200000)
    normal=raw.replace(b'\r\n',b'\n')
    if name.startswith('runs/') and normal:
        normal=b'\n'.join(x.rstrip(b' \t') for x in normal.split(b'\n')).rstrip(b'\n')+b'\n'
    if archive_only or normal!=raw:
        z=Path(str(p)+'.gz')
        if z.exists() and gzip.decompress(z.read_bytes())!=raw:
            z=Path(str(p)+'.science95.raw.gz')
        assert not z.exists() or gzip.decompress(z.read_bytes())==raw,(p,z)
        if not z.exists():z.write_bytes(gzip.compress(raw,mtime=0))
        zn=z.as_posix();git('-c','core.autocrlf=false','add','-f','--',zn);staged.append(zn)
        archives.append(dict(raw_path=name,raw_sha256=sha(raw),archive=zn,archive_sha256=sha(z.read_bytes()),archive_only=archive_only,public_text_sha256=None if archive_only else sha(normal)))
    if not archive_only:
        blob=subprocess.check_output(['git','hash-object','-w','--stdin'],input=normal).decode().strip()
        subprocess.run(['git','update-index','--add','--cacheinfo','100644',blob,name],check=True);staged.append(name)
manifest=r/'science-staging95.json';assert not manifest.exists()
manifest.write_text(json.dumps(dict(files=staged,raw_archives=archives,preserved_collaborator_inputs=saved,source_review=a['source_review'],independent_math='independent-whole-math95/whole-math-decision95.native.json',scope='Reviewed science; independent exact-commit verification and aggregate integration pending'),indent=2)+'\n',encoding='utf8',newline='\n')
git('-c','core.autocrlf=false','add','--',manifest.as_posix())
q=subprocess.run(['git','diff','--cached','--check'],capture_output=True);(r/'science-staged-diff-check95.log').write_bytes(q.stdout+q.stderr);assert q.returncode==0,q.stdout.decode(errors='replace')[-5000:]
assert set(git('diff','--cached','--name-only').decode().splitlines())<=set(staged)|{manifest.as_posix()}
for d in saved:assert sha(Path(d['path']).read_bytes())==d['raw_sha256']
git('commit','-q','-m','Prove actual PBPS bounded signed path expansion over all event counts')
commit=git('rev-parse','HEAD').decode().strip()
(r/'science-commit95.receipt.json').write_text(json.dumps(dict(commit=commit,source_review='accepted',independent_exact_commit='pending',aggregate_integration='pending',collaborator_files_preserved=len(saved)),indent=2)+'\n',encoding='utf8')
print(commit,len(staged),'science files; independent exact-commit verification pending')
