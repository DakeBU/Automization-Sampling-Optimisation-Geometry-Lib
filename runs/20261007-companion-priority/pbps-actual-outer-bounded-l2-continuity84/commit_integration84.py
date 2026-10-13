from pathlib import Path
import gzip,hashlib,json,subprocess
r=Path(__file__).parent;out=r/'integration84';pre=r.parent/'pbps-outer-bounded-l2-preread84';load=lambda p:json.loads(Path(p).read_bytes())
assert load(r/'integration.notes.json')['state_distinctions']['local_aggregate_and_generated_site_gates'];assert not subprocess.check_output(['git','diff','--cached','--name-only'],text=True).strip()
exclude={x['raw_path'] for x in load(r/'immutable-whitespace-archives84.json')['files']};logs=[]
for p in sorted(r.rglob('*.log')):
 raw=p.read_bytes();a=Path(str(p)+'.gz')
 if not a.exists():a.write_bytes(gzip.compress(raw,mtime=0))
 assert gzip.decompress(a.read_bytes())==raw
 logs.append(dict(path=p.as_posix(),RAW_sha256=hashlib.sha256(raw).hexdigest(),archive=a.as_posix(),archive_RAW_sha256=hashlib.sha256(a.read_bytes()).hexdigest()))
(out/'immutable-integration-log-archives84.json').write_text(json.dumps(logs,indent=2)+'\n',encoding='utf8',newline='\n')
owned=load(out/'integration-scope.json')['owned']+['research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-outer-bounded-l2-continuity.json','runs/substantive_advances.jsonl','docs/module-graph.svg','docs/assets/astis_lean_arsenal_module_graph.svg','research-wiki/sampling-sde-library/lean-leaf-module-graph.md','research-wiki/retrieval-index/astis-lean-arsenal-module-graph.json','research-wiki/sampling-sde-library/cards/AutoSamplingTheory.ExampleCases.ProximalBPS.ActualOuterBoundedL2Continuity.md']
for folder in [r,pre]:
 for p in folder.rglob('*'):
  name=p.as_posix()
  if p.is_file() and name not in exclude and '__pycache__' not in p.parts and p.suffix not in {'.log','.diff','.html','.pyc','.olean','.ilean','.c','.o','.ir'} and not name.endswith('.text.txt'):owned.append(name)
paths=sorted(set(owned))
if (r/'next-source85.readiness.json').exists():
 readiness=load(r/'next-source85.readiness.json');manifest=readiness['manifest']
 assert hashlib.sha256(Path(manifest['path']).read_bytes()).hexdigest()==manifest['RAW_sha256']
 paths.append(manifest['path'])
 for x in readiness['raw_outputs']:
  assert hashlib.sha256(Path(x['path']).read_bytes()).hexdigest()==x['raw_sha256']
  paths.append(x['path'])
 paths=sorted(set(paths))

for offset in range(0,len(paths),25):subprocess.run(['git','-c','core.autocrlf=false','add','--',*paths[offset:offset+25]],check=True)
q=subprocess.run(['git','-c','core.whitespace=cr-at-eol','diff','--cached','--check'],capture_output=True);assert q.returncode==0,q.stdout.decode(errors='replace')[:4000]
for p,h in load(pre/'pre-fetch84.workspace-RAW.json')['tracked_modified'].items():assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==h,p
(out/'staged-scope84.json').write_text(json.dumps(dict(paths=subprocess.check_output(['git','diff','--cached','--name-only'],text=True).splitlines(),preserved_unstaged=True),indent=2)+'\n',encoding='utf8',newline='\n')
subprocess.run(['git','-c','core.autocrlf=false','add','--',(out/'staged-scope84.json').as_posix()],check=True)
subprocess.run(['git','commit','-q','-m','Integrate verified actual PBPS bounded-test outer square integral and reader evidence'],check=True)
print('INTEGRATION_COMMIT',subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip())
