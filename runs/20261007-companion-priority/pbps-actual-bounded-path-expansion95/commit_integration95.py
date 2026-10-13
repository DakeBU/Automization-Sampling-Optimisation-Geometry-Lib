"""Explicit integration staging; native evidence retained in lossless archives."""
from pathlib import Path
import gzip,hashlib,json,subprocess,datetime
R=Path.cwd().resolve();r=Path(__file__).resolve().parent.relative_to(R);out=r/'integration95'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git',*a])
note=load(r/'integration.notes.json');assert note['state_distinctions']['local_aggregate_and_generated_site_gates']
assert not git('diff','--cached','--name-only').strip()
assert git('rev-parse','HEAD').decode().strip()==note['integration_base_commit']
claim=load(r/'claim.json');cp='research-wiki/frontier-cells/'+claim['frontier_cell']+'.json'
assert load(cp)['status']=='independently_verified'
saved=load(r/'exact-commit-verification95/closed-RAW-manifest95.json')['preserved_collaborator_inputs']
for d in saved:assert sha(Path(d['path']).read_bytes())==d['raw_sha256'],d['path']
tracked=set(git('ls-files').decode().splitlines())
old_rows=load(r/'science-staging95.json')['raw_archives']
old_native={d['raw_path'] for d in old_rows}
old_hashes={name:{d['raw_sha256'] for d in old_rows if d['raw_path']==name} for name in old_native}
excluded_parts={'__pycache__'}
def allowed(p):
    name=p.name.lower()
    return not excluded_parts.intersection(p.parts) and not name.startswith('.private') and not name.endswith('.private.json') and p.suffix not in {'.pyc','.olean','.ilean','.c','.o','.ir'} and not name.endswith('.text.txt') and not ('primary' in name and p.suffix=='.html') and sha(p.read_bytes())!='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
owned=load(out/'integration-scope.json')['owned']+[cp,'runs/substantive_advances.jsonl','docs/module-graph.svg','docs/assets/astis_lean_arsenal_module_graph.svg','research-wiki/sampling-sde-library/lean-leaf-module-graph.md','research-wiki/retrieval-index/astis-lean-arsenal-module-graph.json','research-wiki/sampling-sde-library/cards/AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBoundedPathExpansion.md']
paths=set(owned);archives=[];normalize={}
# Do not restage historical native files whose committed public text was normalized.
for p in sorted([*r.rglob('*'), *(r.parent/'pbps-phase-reversal-volume-preread96').rglob('*')]):
    if not p.is_file() or not allowed(p):continue
    name=p.as_posix()
    raw=p.read_bytes()
    if name in tracked and git('show','HEAD:'+name)==raw:continue
    if name in old_native:
        if sha(raw) in old_hashes[name]:continue
        assert p.parent==r and p.suffix=='.py',('unexpected mutation of historical native evidence',name)
    if name in tracked and git('show','HEAD:'+name)==raw:continue
    if p.suffix=='.gz':paths.add(name);continue
    raw_only=p.suffix in {'.log','.diff','.html','.lean','.snapshot','.stdout','.stderr','.exactraw'} or '.snapshot.' in p.name or len(raw)>200000
    normalized=raw
    if p.suffix in {'.json','.jsonl','.md','.py','.txt'}:
        normalized=('\n'.join(x.rstrip(' \t') for x in raw.decode('utf8').splitlines()).rstrip('\n')+'\n').encode('utf8')
    if raw_only or normalized!=raw:
        z=Path(str(p)+'.integration95.raw.gz');assert not z.exists(),z
        z.write_bytes(gzip.compress(raw,mtime=0));assert gzip.decompress(z.read_bytes())==raw
        paths.add(z.as_posix());archives.append(dict(raw_path=name,raw_sha256=sha(raw),raw_bytes=len(raw),archive=z.as_posix(),archive_raw_sha256=sha(z.read_bytes()),public_text_raw_sha256=None if raw_only else sha(normalized)))
    if not raw_only:
        paths.add(name)
        if normalized!=raw:normalize[name]=normalized
archive=out/'immutable-integration-RAW-archives95.json';assert not archive.exists()
archive.write_text(json.dumps(dict(status='LOSSLESS_NATIVE_ARCHIVES',files=archives,old_native_not_restaged=sorted(old_native)),indent=2)+'\n',encoding='utf8',newline='\n')
paths.add(archive.as_posix());assert not paths.intersection(d['path'] for d in saved)
paths=sorted(paths)
for i in range(0,len(paths),25):subprocess.run(['git','-c','core.autocrlf=false','add','-f','--',*paths[i:i+25]],check=True,capture_output=True)
for name,b in normalize.items():
    blob=subprocess.check_output(['git','hash-object','-w','--stdin'],input=b).decode().strip()
    subprocess.run(['git','update-index','--cacheinfo','100644',blob,name],check=True)
actual=set(git('diff','--cached','--name-only').decode().splitlines());assert actual<=set(paths) and cp in actual
for d in archives:
    assert sha(gzip.decompress(git('show',':'+d['archive'])))==d['raw_sha256']
    assert sha(Path(d['raw_path']).read_bytes())==d['raw_sha256']
    if d['public_text_raw_sha256']:assert sha(git('show',':'+d['raw_path']))==d['public_text_raw_sha256']
for args in [('diff','--cached','--check'),('diff','--check')]:
    q=subprocess.run(['git',*args],capture_output=True);assert q.returncode==0,(q.stdout+q.stderr).decode(errors='replace')[:5000]
stage=out/'staged-scope95.json';assert not stage.exists()
stage.write_text(json.dumps(dict(paths=sorted(actual),preserved_collaborator_files=21,sole_lane=note['sole_lane'],independently_verified=True,main_merged=False,purified=False,Goal_complete=False),indent=2)+'\n',encoding='utf8',newline='\n')
subprocess.run(['git','-c','core.autocrlf=false','add','--',stage.as_posix()],check=True)
subprocess.run(['git','commit','-q','-m','Integrate verified bounded PBPS path expansion'],check=True)
for d in saved:assert sha(Path(d['path']).read_bytes())==d['raw_sha256'],d['path']
print('INTEGRATION_COMMIT',git('rev-parse','HEAD').decode().strip())
