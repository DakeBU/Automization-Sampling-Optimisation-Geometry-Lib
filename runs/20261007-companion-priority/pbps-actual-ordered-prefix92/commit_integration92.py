from pathlib import Path
import gzip,hashlib,json,subprocess
R=Path.cwd();r=Path(__file__).parent;out=r/'integration92';load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
note=load(r/'integration.notes.json');assert note['state_distinctions']['local_aggregate_and_generated_site_gates']
assert not subprocess.check_output(['git','diff','--cached','--name-only']).strip()
assert subprocess.check_output(['git','rev-parse','HEAD']).decode().strip()==note['science_commit']
claim=load(r/'claim.json');cp=Path('research-wiki/frontier-cells')/(claim['frontier_cell']+'.json');assert load(cp)['status']=='independently_verified'
saved=load(r/'exact-commit-verification92/closed-RAW-manifest92.json')['preserved_collaborator_inputs']
for d in saved:assert sha(Path(d['path']).read_bytes())==d['raw_sha256'],d['path']
def publishable(p):
 return 'next-source-graph93' not in p.parts and 'next-boundary-math93' not in p.parts and not p.name.startswith('.private') and not p.name.endswith('.private.json') and p.name != 'primary-source-slices92.native.json' and '__pycache__' not in p.parts and p.suffix not in {'.pyc','.olean','.ilean','.c','.o','.ir'} and not p.name.endswith('.text.txt') and sha(p.read_bytes())!='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
rows=[];excluded=set()
for p in sorted(r.rglob('*')):
 if not p.is_file() or p.suffix=='.gz' or not publishable(p):continue
 if p.suffix not in {'.log','.diff','.html','.lean','.snapshot'} and '.snapshot.' not in p.name and not p.name.endswith('console.txt'):continue
 b=p.read_bytes();z=Path(str(p)+'.gz')
 if not z.exists():z.write_bytes(gzip.compress(b,mtime=0))
 assert gzip.decompress(z.read_bytes())==b,p
 excluded.add(p.as_posix());rows.append(dict(raw_path=p.as_posix(),raw_bytes=len(b),raw_sha256=sha(b),archive=z.as_posix(),archive_raw_sha256=sha(z.read_bytes())))
archive=out/'immutable-integration-RAW-archives92.json';assert not archive.exists()
archive.write_text(json.dumps(dict(status='LOSSLESS_NATIVE_ARCHIVES',files=rows),indent=2)+'\n',encoding='utf8',newline='\n')
owned=load(out/'integration-scope.json')['owned']+[cp.as_posix(),'runs/substantive_advances.jsonl','docs/module-graph.svg','docs/assets/astis_lean_arsenal_module_graph.svg','research-wiki/sampling-sde-library/lean-leaf-module-graph.md','research-wiki/retrieval-index/astis-lean-arsenal-module-graph.json','research-wiki/sampling-sde-library/cards/AutoSamplingTheory.ExampleCases.ProximalBPS.ActualOrderedPrefix.md']
owned.extend(p.as_posix() for p in r.rglob('*') if p.is_file() and publishable(p) and p.as_posix() not in excluded)
paths=sorted({Path(p).resolve().relative_to(R).as_posix() for p in owned})
assert not set(paths).intersection(d['path'] for d in saved)
for i in range(0,len(paths),25):subprocess.run(['git','-c','core.autocrlf=false','add','-f','--',*paths[i:i+25]],check=True)
actual=set(subprocess.check_output(['git','diff','--cached','--name-only']).decode().splitlines());assert actual.issubset(paths) and cp.as_posix() in actual
index={}
for line in subprocess.check_output(['git','ls-files','-sz']).split(b'\0'):
 if line:
  meta,name=line.split(b'\t',1);index[name.decode()]=meta.split()[1].decode()
for d in rows:
 b=subprocess.check_output(['git','cat-file','blob',index[Path(d['archive']).resolve().relative_to(R).as_posix()]])
 assert sha(b)==d['archive_raw_sha256'] and sha(gzip.decompress(b))==d['raw_sha256'],d['archive']
q=subprocess.run(['git','-c','core.whitespace=cr-at-eol','diff','--cached','--check'],capture_output=True)
assert q.returncode==0,(q.stdout+q.stderr).decode(errors='replace')[:4000]
stage=out/'staged-scope92.json';stage.write_text(json.dumps(dict(paths=sorted(actual),independently_verified_frontier_staged=True,preserved_collaborator_files=21,sole_lane=note['sole_lane'],main_merged=False,purified=False,Goal_complete=False),indent=2)+'\n',encoding='utf8',newline='\n')
subprocess.run(['git','-c','core.autocrlf=false','add','--',stage.as_posix()],check=True)
subprocess.run(['git','commit','-q','-m','Integrate verified actual PBPS ordered finite-prefix law'],check=True)
for d in saved:assert sha(Path(d['path']).read_bytes())==d['raw_sha256'],d['path']
print('INTEGRATION_COMMIT',subprocess.check_output(['git','rev-parse','HEAD']).decode().strip())
