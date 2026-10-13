"""Commit only current-main94 integration evidence, retaining exact native archives."""
from pathlib import Path
import json,gzip,hashlib,subprocess
root=Path.cwd().resolve();r=Path(__file__).resolve().parent.relative_to(root);out=r/'integration94'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest();git=lambda *a:subprocess.check_output(['git',*a])
note=load(out/'post-main.notes.json');assert note['status']=='CURRENT_MAIN_AGGREGATE_AND_GENERATED_READER_PASS_VISUAL_PENDING'
assert git('rev-parse','HEAD').decode().strip()==note['checked_merge_commit'];assert not git('diff','--cached','--name-only').strip()
saved=load(r/'exact-commit-verification94/closed-RAW-manifest94.json')['preserved_collaborator_inputs']
for d in saved:assert sha(Path(d['path']).read_bytes())==d['raw_sha256'],d['path']
tracked=set(git('ls-files').decode().splitlines())
old_rows=load(r/'science-staging94.json')['raw_archives']+load(out/'immutable-integration-RAW-archives94.json')['files']
old={}
for d in old_rows:old.setdefault(d['raw_path'],set()).add(d['raw_sha256'])
owned=['runs/substantive_advances.jsonl','docs/module-graph.svg','docs/assets/astis_lean_arsenal_module_graph.svg','research-wiki/sampling-sde-library/lean-leaf-module-graph.md','research-wiki/retrieval-index/astis-lean-arsenal-module-graph.json','research-wiki/sampling-sde-library/cards/AutoSamplingTheory.TechnicalLemmas.Geometry.AffineGradient.md']
paths=set(owned);archives=[];normalize={}
excluded={'next-primary95','next-source-graph95','header95-type-only','__pycache__'}
for p in sorted(r.rglob('*')):
    if not p.is_file() or excluded.intersection(p.parts) or p.suffix in {'.olean','.ilean','.pyc','.o','.c','.ir'}:continue
    name=p.as_posix();raw=p.read_bytes()
    if sha(raw)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760' or ('primary' in p.name.lower() and p.suffix=='.html'):continue
    if name in tracked and git('show','HEAD:'+name)==raw:continue
    if name in old and sha(raw) in old[name]:continue
    if p.suffix=='.gz':paths.add(name);continue
    if name in old:assert p.parent==r and p.suffix=='.py',('unexpected historical evidence mutation',name)
    raw_only=p.suffix in {'.log','.diff','.patch','.html','.lean','.snapshot','.stdout','.stderr','.merge-input'} or '.snapshot.' in p.name or len(raw)>200000
    normal=raw
    if p.suffix in {'.json','.jsonl','.md','.py','.txt'}:normal=('\n'.join(x.rstrip(' \t') for x in raw.decode('utf8').splitlines()).rstrip('\n')+'\n').encode('utf8')
    if raw_only or normal!=raw:
        z=Path(str(p)+'.post-main94.raw.gz');assert not z.exists();z.write_bytes(gzip.compress(raw,mtime=0));assert gzip.decompress(z.read_bytes())==raw
        paths.add(z.as_posix());archives.append(dict(raw_path=name,raw_sha256=sha(raw),archive=z.as_posix(),archive_raw_sha256=sha(z.read_bytes()),public_text_raw_sha256=None if raw_only else sha(normal)))
    if not raw_only:
        paths.add(name)
        if normal!=raw:normalize[name]=normal
manifest=out/'post-main-RAW-archives94.json';assert not manifest.exists();manifest.write_text(json.dumps(dict(files=archives,status='LOSSLESS_NATIVE_RAW_ARCHIVES',old_native_not_restaged=sorted(old)),indent=2)+'\n',encoding='utf8',newline='\n');paths.add(manifest.as_posix())
assert not set(paths).intersection(d['path'] for d in saved)
paths=sorted(paths)
for i in range(0,len(paths),25):subprocess.run(['git','-c','core.autocrlf=false','add','-f','--',*paths[i:i+25]],check=True,capture_output=True)
for name,b in normalize.items():
    blob=subprocess.check_output(['git','hash-object','-w','--stdin'],input=b).decode().strip();subprocess.run(['git','update-index','--cacheinfo','100644',blob,name],check=True)
actual=set(git('diff','--cached','--name-only').decode().splitlines());assert actual<=set(paths)
for d in archives:assert sha(gzip.decompress(git('show',':'+d['archive'])))==d['raw_sha256']
for args in [('diff','--cached','--check'),('diff','--check')]:
    q=subprocess.run(['git',*args],capture_output=True);assert q.returncode==0,(q.stdout+q.stderr).decode(errors='replace')[-5000:]
for d in saved:assert sha(Path(d['path']).read_bytes())==d['raw_sha256']
subprocess.run(['git','commit','-q','-m','Validate PBPS density integration against merged affine-gradient main'],check=True)
print('POST_MAIN94_COMMIT',git('rev-parse','HEAD').decode().strip(),'files',len(actual))
