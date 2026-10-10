from pathlib import Path
import gzip,hashlib,json,subprocess
r=Path(__file__).parent;out=r/'integration86';pre=r.parent/'pbps-path-law-preread86';load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
assert load(r/'integration.notes.json')['state_distinctions']['local_aggregate_and_generated_site_gates']
assert not subprocess.check_output(['git','diff','--cached','--name-only'],text=True).strip()
claim=load(r/'claim.json');cp=Path('research-wiki/frontier-cells')/(claim['frontier_cell']+'.json')
assert load(cp)['status']=='independently_verified'
ledger=Path('runs/substantive_advances.jsonl');prefix=subprocess.check_output(['git','show','HEAD:runs/substantive_advances.jsonl']);raw=ledger.read_bytes();assert raw.startswith(prefix)
tail=raw[len(prefix):];events=[json.loads(x) for x in tail.splitlines() if x.strip()];assert events and all(x['advance_id']==claim['advance_id'] for x in events)
ledger.write_bytes(prefix+tail.replace(b'\r\n',b'\n'))
private_names={'root.primary-anchor-read86.private.json','primary-first86.json','anchor-readback86.json','anchor-readback86.spaced-normalization.json'}
def publishable(p):return '.private.' not in p.name and p.name not in private_names
exclude={x['raw_path'] for x in load(r/'immutable-whitespace-archives86.json')['files']};logs=[]
for p in sorted(x for x in r.rglob('*') if x.is_file() and publishable(x) and x.suffix in {'.log','.diff'}):
 raw=p.read_bytes();a=Path(str(p)+'.gz')
 if not a.exists():a.write_bytes(gzip.compress(raw,mtime=0))
 assert gzip.decompress(a.read_bytes())==raw
 logs.append(dict(path=p.as_posix(),RAW_sha256=sha(raw),archive=a.as_posix(),archive_RAW_sha256=sha(a.read_bytes())))
(out/'immutable-integration-log-archives86.json').write_text(json.dumps(logs,indent=2)+'\n',encoding='utf8',newline='\n')
owned=load(out/'integration-scope.json')['owned']+[cp.as_posix(),'runs/substantive_advances.jsonl','docs/module-graph.svg','docs/assets/astis_lean_arsenal_module_graph.svg','research-wiki/sampling-sde-library/lean-leaf-module-graph.md','research-wiki/retrieval-index/astis-lean-arsenal-module-graph.json','research-wiki/sampling-sde-library/cards/AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteFirstEventLaw.md']
for folder in [r,pre]:
 for p in folder.rglob('*'):
  name=p.as_posix()
  if p.is_file() and publishable(p) and name not in exclude and '__pycache__' not in p.parts and p.suffix not in {'.log','.diff','.html','.pyc','.olean','.ilean','.c','.o','.ir'} and not name.endswith('.text.txt'):owned.append(name)
paths=sorted({Path(p).resolve().relative_to(Path.cwd()).as_posix() for p in owned});saved=load(pre/'pre-fetch86.workspace-RAW.json')['tracked_modified']
assert len(saved)==21 and not set(paths).intersection(saved)
for p,h in saved.items():assert sha(Path(p).read_bytes())==h,p
for offset in range(0,len(paths),25):subprocess.run(['git','-c','core.autocrlf=false','add','--',*paths[offset:offset+25]],check=True)
actual=set(subprocess.check_output(['git','diff','--cached','--name-only'],text=True).splitlines());assert actual.issubset(paths) and cp.as_posix() in actual
q=subprocess.run(['git','-c','core.whitespace=cr-at-eol','diff','--cached','--check'],capture_output=True);assert q.returncode==0,q.stdout.decode(errors='replace')[:4000]
(out/'staged-scope86.json').write_text(json.dumps(dict(paths=sorted(actual),correct_frontier_cell_staged=True,preserved_unstaged=True),indent=2)+'\n',encoding='utf8',newline='\n')
subprocess.run(['git','-c','core.autocrlf=false','add','--',(out/'staged-scope86.json').as_posix()],check=True)
subprocess.run(['git','commit','-q','-m','Integrate verified PBPS first-event law and adjacent reader evidence'],check=True)
assert subprocess.check_output(['git','show','HEAD:'+cp.as_posix()])==cp.read_bytes()
print('INTEGRATION_COMMIT',subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip())
