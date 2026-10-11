"""Finish the owned staging transaction, preserving exact snapshots in gzip."""
from pathlib import Path
import gzip, hashlib, json, subprocess
root=Path.cwd().resolve()
r=Path(__file__).resolve().parent.relative_to(root)
pre=r.parent/'pbps-phase-reversal-volume-preread96'
load=lambda p:json.loads(Path(p).read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
git=lambda *a:subprocess.check_output(['git',*a])
note=load(r/'integration.notes.json')
assert git('rev-parse','HEAD').decode().strip()==note['science_commit']
saved=load(r/'exact-commit-verification95/closed-RAW-manifest95.json')['preserved_collaborator_inputs']
for d in saved:assert sha(Path(d['path']).read_bytes())==d['raw_sha256']
scope=set(load(r/'integration95/integration-scope.json')['owned'])
scope.update(['runs/substantive_advances.jsonl','docs/module-graph.svg','docs/assets/astis_lean_arsenal_module_graph.svg','research-wiki/sampling-sde-library/lean-leaf-module-graph.md','research-wiki/retrieval-index/astis-lean-arsenal-module-graph.json','research-wiki/sampling-sde-library/cards/AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBoundedPathExpansion.md','research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-bounded-path-expansion.json'])
paths=git('diff','--cached','--name-only').decode().splitlines()
assert paths
assert all(n in scope or n.startswith(r.as_posix()+'/') or n.startswith(pre.as_posix()+'/') for n in paths)
manifest=r/'integration95/immutable-integration-RAW-archives95.json'
m=load(manifest);fixed=[]
for name in paths:
    p=Path(name)
    if p.suffix!='.exactraw':continue
    assert subprocess.run(['git','cat-file','-e','HEAD:'+name],capture_output=True).returncode!=0
    raw=p.read_bytes();assert git('show',':'+name)==raw
    z=Path(str(p)+'.integration95.raw.gz');assert not z.exists()
    z.write_bytes(gzip.compress(raw,mtime=0));assert gzip.decompress(z.read_bytes())==raw
    subprocess.run(['git','update-index','--force-remove','--',name],check=True)
    subprocess.run(['git','-c','core.autocrlf=false','add','-f','--',z.as_posix()],check=True)
    row=dict(raw_path=name,raw_sha256=sha(raw),raw_bytes=len(raw),archive=z.as_posix(),archive_raw_sha256=sha(z.read_bytes()),public_text_raw_sha256=None)
    m['files'].append(row);fixed.append(row)
manifest.write_text(json.dumps(m,indent=2)+'\n',encoding='utf8',newline='\n')
script=r/'commit_integration95.py'
s=script.read_text(encoding='utf8');assert "'.exactraw'" not in s
script.write_text(s.replace("'.stdout','.stderr'}", "'.stdout','.stderr','.exactraw'}"),encoding='utf8',newline='\n')
receipt=r/'integration95/staging-encoding-correction95.json'
receipt.write_text(json.dumps(dict(reason='New preproof96 .exactraw suffix was not classified as opaque; cached diff-check rejected native CRLF text. Preserve all native bytes in lossless archives, remove only newly staged plain snapshots from index, and extend suffix classification.',working_files_preserved=True,files=fixed),indent=2)+'\n',encoding='utf8',newline='\n')
subprocess.run(['git','-c','core.autocrlf=false','add','--',manifest.as_posix(),script.as_posix(),receipt.as_posix(),Path(__file__).resolve().relative_to(root).as_posix()],check=True)
for args in [('diff','--cached','--check'),('diff','--check')]:
    q=subprocess.run(['git',*args],capture_output=True);assert q.returncode==0,(q.stdout+q.stderr).decode(errors='replace')[:3000]
for d in m['files']:assert sha(gzip.decompress(git('show',':'+d['archive'])))==d['raw_sha256']
actual=git('diff','--cached','--name-only').decode().splitlines()
assert not set(actual).intersection(d['path'] for d in saved)
stage=r/'integration95/staged-scope95.json';assert not stage.exists()
stage.write_text(json.dumps(dict(paths=actual,preserved_collaborator_files=len(saved),sole_lane=note['sole_lane'],independently_verified=True,prospective96='Only reviewed statement and seal; no proof/claim',main_merged=False,purified=False,Goal_complete=False),indent=2)+'\n',encoding='utf8',newline='\n')
subprocess.run(['git','-c','core.autocrlf=false','add','--',stage.as_posix()],check=True)
subprocess.run(['git','commit','-q','-m','Integrate verified bounded PBPS path expansion'],check=True)
for d in saved:assert sha(Path(d['path']).read_bytes())==d['raw_sha256']
print('INTEGRATION95_COMMIT',git('rev-parse','HEAD').decode().strip(),'files',len(actual)+1)
