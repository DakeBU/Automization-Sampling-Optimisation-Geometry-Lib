"""Serialize the independently verified child through the existing sole lane."""
from pathlib import Path
import gzip,hashlib,json,subprocess
r=Path(__file__).parent;pre=r.parent/'pbps-clock-tail-preread87';out=r/'integration87'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
assert load(r/'integration.notes.json')['state_distinctions']['local_aggregate_and_generated_site_gates']
assert not subprocess.check_output(['git','diff','--cached','--name-only'],text=True).strip()
claim=load(r/'claim.json');cp=Path('research-wiki/frontier-cells')/(claim['frontier_cell']+'.json')
assert load(cp)['status']=='independently_verified'
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()=='ada2d073d04a78493555b2ac35344b9c5a264bfc'
def publishable(p):
 return '.private.' not in p.name and '__pycache__' not in p.parts and p.suffix not in {'.pyc','.olean','.ilean','.c','.o','.ir'} and not p.name.endswith('.text.txt')
rows=[];excluded=set()
for folder in [r,pre]:
 for p in sorted(folder.rglob('*')):
  if not p.is_file() or not publishable(p) or p.suffix not in {'.log','.diff','.html','.lean','.snapshot'}:continue
  b=p.read_bytes();z=Path(str(p)+'.gz')
  if not z.exists():z.write_bytes(gzip.compress(b,mtime=0))
  assert gzip.decompress(z.read_bytes())==b,p
  excluded.add(p.as_posix());rows.append(dict(raw_path=p.as_posix(),raw_bytes=len(b),raw_sha256=sha(b),archive=z.as_posix(),archive_raw_sha256=sha(z.read_bytes())))
archive=out/'immutable-integration-RAW-archives87.json';assert not archive.exists()
archive.write_text(json.dumps(dict(status='IMMUTABLE_NATIVE_RETAINED_LOSSLESS_ARCHIVES',files=rows),indent=2)+'\n',encoding='utf8',newline='\n')
owned=load(out/'integration-scope.json')['owned']+[cp.as_posix(),'runs/substantive_advances.jsonl','docs/module-graph.svg','docs/assets/astis_lean_arsenal_module_graph.svg','research-wiki/sampling-sde-library/lean-leaf-module-graph.md','research-wiki/retrieval-index/astis-lean-arsenal-module-graph.json','research-wiki/sampling-sde-library/cards/AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteHistoryTailLaw.md']
for folder in [r,pre]:
 owned.extend(p.as_posix() for p in folder.rglob('*') if p.is_file() and publishable(p) and p.as_posix() not in excluded and p.suffix not in {'.log','.diff','.html','.lean','.snapshot'})
paths=sorted({Path(p).resolve().relative_to(Path.cwd()).as_posix() for p in owned})
saved=load(pre/'pre-fetch87.workspace-RAW.json')['tracked_modified'];assert len(saved)==21 and not set(paths).intersection(saved)
for p,h in saved.items():assert sha(Path(p).read_bytes())==h,p
for offset in range(0,len(paths),25):subprocess.run(['git','-c','core.autocrlf=false','add','-f','--',*paths[offset:offset+25]],check=True)
actual=set(subprocess.check_output(['git','diff','--cached','--name-only'],text=True).splitlines())
assert actual.issubset(paths) and cp.as_posix() in actual and not actual.intersection(saved)
q=subprocess.run(['git','-c','core.whitespace=cr-at-eol','diff','--cached','--check'],capture_output=True)
assert q.returncode==0,(q.stdout+q.stderr).decode(errors='replace')[:4000]
stage=out/'staged-scope87.json';assert not stage.exists()
stage.write_text(json.dumps(dict(paths=sorted(actual),independently_verified_frontier_staged=True,preserved_collaborator_files=21,sole_lane='ASTIS-SA-20261005-SPHMCImplementedPhaseKernel',main_merged=False,purified=False,Goal_complete=False),indent=2)+'\n',encoding='utf8',newline='\n')
subprocess.run(['git','-c','core.autocrlf=false','add','--',stage.as_posix()],check=True)
subprocess.run(['git','commit','-q','-m','Integrate verified actual PBPS history and unused-clock tail law'],check=True)
assert subprocess.check_output(['git','show','HEAD:'+cp.as_posix()])==cp.read_bytes()
for p,h in saved.items():assert sha(Path(p).read_bytes())==h,p
print('INTEGRATION_COMMIT',subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip())
