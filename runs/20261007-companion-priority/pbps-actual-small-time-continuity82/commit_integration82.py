from pathlib import Path
import gzip,hashlib,json,subprocess
r=Path(__file__).parent;out=r/'integration82';load=lambda p:json.loads(Path(p).read_bytes())
assert load(r/'integration.notes.json')['state_distinctions']['local_aggregate_and_generated_site_gates'];assert not subprocess.check_output(['git','diff','--cached','--name-only'],text=True).strip()
exclude={x['raw_path'] for x in load(r/'immutable-whitespace-archives82.json')['files']};logs=[]
for p in sorted(r.rglob('*.log')):
 raw=p.read_bytes();a=Path(str(p)+'.gz')
 if not a.exists():a.write_bytes(gzip.compress(raw,mtime=0))
 assert gzip.decompress(a.read_bytes())==raw
 logs.append(dict(path=p.as_posix(),RAW_sha256=hashlib.sha256(raw).hexdigest(),archive=a.as_posix(),archive_RAW_sha256=hashlib.sha256(a.read_bytes()).hexdigest()))
(out/'immutable-integration-log-archives82.json').write_text(json.dumps(logs,indent=2)+'\n',encoding='utf8',newline='\n')
owned=load(out/'integration-scope.json')['owned']+['research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-small-time-continuity.json','runs/substantive_advances.jsonl','docs/module-graph.svg','docs/assets/astis_lean_arsenal_module_graph.svg','research-wiki/sampling-sde-library/lean-leaf-module-graph.md','research-wiki/retrieval-index/astis-lean-arsenal-module-graph.json','research-wiki/sampling-sde-library/cards/AutoSamplingTheory.ExampleCases.ProximalBPS.ActualSmallTimeContinuity.md']
for p in r.rglob('*'):
 name=p.as_posix()
 if p.is_file() and name not in exclude and '__pycache__' not in p.parts and p.suffix not in {'.log','.html','.pyc'} and not name.endswith('.text.txt'):owned.append(name)
for folder in ['pbps-process-regularity-preread82','pbps-bounded-test-preread83']:
 pre=Path('runs/20261007-companion-priority')/folder
 if folder.endswith('83') and not (r/'next-source83.readiness.json').exists():continue
 if folder.endswith('83'):
  manifest=pre/'source_freeze83.closed-raw-manifest.json';m=load(manifest)
  owned.append(manifest.as_posix())
  for entry in m['raw_outputs']:
   p=Path(entry['path']);assert hashlib.sha256(p.read_bytes()).hexdigest()==entry['raw_sha256']
   owned.append(p.relative_to(Path.cwd()).as_posix() if p.is_absolute() else p.as_posix())
 elif pre.exists():owned += [p.as_posix() for p in pre.rglob('*') if p.is_file() and p.suffix in {'.json','.md','.py'} and '__pycache__' not in p.parts]
paths=sorted(set(owned))
for offset in range(0,len(paths),25):
 subprocess.run(['git','-c','core.autocrlf=false','add','--',*paths[offset:offset+25]],check=True)
q=subprocess.run(['git','-c','core.whitespace=cr-at-eol','diff','--cached','--check'],capture_output=True);assert q.returncode==0,q.stdout.decode(errors='replace')[:4000]
for p,h in load(r/'pre-fetch82.workspace-RAW.json')['tracked_modified'].items():assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==h,p
(out/'staged-scope82.json').write_text(json.dumps(dict(paths=subprocess.check_output(['git','diff','--cached','--name-only'],text=True).splitlines(),preserved_unstaged=True),indent=2)+'\n',encoding='utf8',newline='\n')
subprocess.run(['git','-c','core.autocrlf=false','add','--',(out/'staged-scope82.json').as_posix()],check=True)
subprocess.run(['git','commit','-q','-m','Integrate verified actual PBPS stochastic continuity and reader evidence'],check=True)
print('INTEGRATION_COMMIT',subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip())
