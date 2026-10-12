"""Stage only the admitted unit and its sole-lane integration, preserving RAW evidence."""
from pathlib import Path
import gzip, hashlib, json, subprocess
R=Path.cwd().resolve();r=Path(__file__).resolve().parent.relative_to(R);out=r/'integration109'
load=lambda p:json.loads(Path(p).read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git','-c','core.autocrlf=false','-c','core.fscache=false',*a])
note=load(r/'integration.notes.json')
assert note['state_distinctions']['local_aggregate_and_generated_site_gates']
assert git('rev-parse','HEAD').decode().strip()==note['integration_base_commit']
assert not git('diff','--cached','--name-only').strip()
claim=load(r/'claim.json');cp='research-wiki/frontier-cells/'+claim['frontier_cell']+'.json'
assert load(cp)['status']=='independently_verified'
saved=load(r/'exact-commit-verification109/closed-RAW-manifest109.json')['preserved_collaborator_inputs']
for d in saved:assert sha(Path(d['path']).read_bytes())==d['raw_sha256'],d['path']
owned=load(out/'integration-scope.json')['owned']+[cp,'runs/substantive_advances.jsonl','docs/module-graph.svg','docs/assets/astis_lean_arsenal_module_graph.svg','research-wiki/sampling-sde-library/lean-leaf-module-graph.md','research-wiki/retrieval-index/astis-lean-arsenal-module-graph.json','research-wiki/sampling-sde-library/cards/AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPositionL2Averaging.md']
owned += ['website/content/declaration_lessons/pbps-actual-position-l2-averaging.json','research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261012-PBPSActualPositionL2Averaging.json']
files={Path(x) for x in owned};tracked=set(git('ls-files').decode().splitlines())
for p in list(r.rglob('*')) + list(Path('runs/20261007-companion-priority/pbps-actual-position-l2-preread109/upstream-reconciliation109').rglob('*')):
    if not p.is_file() or {'__pycache__','next-primary110','next-primary110-source-completion','integration-storage-review109'}.intersection(p.parts):continue
    if p.suffix in {'.pyc','.olean','.ilean','.c','.o','.ir'}:continue
    if p.name.endswith('.private.json') or p.name.endswith('.text.txt'):continue
    files.add(p)
old=load(r/'science-staging109.json')['raw_archives']
old_raw={}
for x in old:old_raw.setdefault(x['raw_path'],set()).add(x['raw_sha256'])
staged=[];archives=[]
for p in sorted(files):
    name=p.as_posix();raw=p.read_bytes()
    assert name not in {d['path'] for d in saved}
    if sha(raw)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760':continue
    if name in tracked and git('show','HEAD:'+name)==raw:continue
    if name not in owned and sha(raw) in old_raw.get(name,set()):continue
    if p.suffix.lower() in {'.gz', '.png', '.jpg', '.jpeg', '.webp', '.pdf'}:
        git('-c','core.autocrlf=false','add','-f','--',name);staged.append(name);continue
    opaque=(name.startswith(r.as_posix()+'/') or '/upstream-reconciliation109/' in name) and (p.suffix in {'.log','.html','.lean','.snapshot','.stdout','.stderr','.exactraw','.raw','.lf','.candidate'} or '.snapshot.' in p.name or len(raw)>200000)
    normalized=raw.replace(b'\r\n',b'\n')
    if name.startswith('runs/'):
        normalized=b'\n'.join(x.rstrip(b' \t') for x in normalized.split(b'\n')).rstrip(b'\n')+b'\n'
    if opaque or normalized!=raw:
        z=Path(str(p)+'.integration109.raw.gz')
        assert not z.exists() or gzip.decompress(z.read_bytes())==raw,z
        if not z.exists():z.write_bytes(gzip.compress(raw,mtime=0))
        git('-c','core.autocrlf=false','add','-f','--',z.as_posix());staged.append(z.as_posix())
        archives.append(dict(raw_path=name,raw_sha256=sha(raw),archive=z.as_posix(),archive_raw_sha256=sha(z.read_bytes()),public_text_raw_sha256=None if opaque else sha(normalized)))
    if not opaque:
        blob=subprocess.check_output(['git','hash-object','-w','--stdin'],input=normalized).decode().strip()
        subprocess.run(['git','update-index','--add','--cacheinfo','100644',blob,name],check=True)
        staged.append(name)
manifest=out/'immutable-integration-RAW-archives109.json'
assert not manifest.exists()
manifest.write_text(json.dumps(dict(status='LOSSLESS_NATIVE_ARCHIVES',files=archives,all21collaboratorRAWs_preserved=True),indent=2)+'\n',encoding='utf8',newline='\n')
git('-c','core.autocrlf=false','add','--',manifest.as_posix());staged.append(manifest.as_posix())
for d in archives:assert sha(gzip.decompress(git('show',':'+d['archive'])))==d['raw_sha256']
actual=set(git('diff','--cached','--name-only').decode().splitlines())
assert actual<=set(staged)
for args in [('diff','--cached','--check'),('diff','--check')]:
    q=subprocess.run(['git','-c','core.fscache=false',*args],capture_output=True)
    assert q.returncode==0,(q.stdout+q.stderr).decode(errors='replace')[:5000]
stage=out/'staged-scope109.json';assert not stage.exists()
stage.write_text(json.dumps(dict(paths=sorted(actual),preserved_collaborator_files=21,sole_lane=note['sole_lane'],independently_verified=True,main_merged=False,purified=False,Goal_complete=False),indent=2)+'\n',encoding='utf8',newline='\n')
git('-c','core.autocrlf=false','add','--',stage.as_posix())
git('commit','-q','-m','Integrate verified PBPS Gaussian position L2 averaging')
for d in saved:assert sha(Path(d['path']).read_bytes())==d['raw_sha256'],d['path']
print('INTEGRATION109_COMMIT',git('rev-parse','HEAD').decode().strip())
