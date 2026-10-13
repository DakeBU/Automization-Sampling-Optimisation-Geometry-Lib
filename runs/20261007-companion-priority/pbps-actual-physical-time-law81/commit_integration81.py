from pathlib import Path
import json,subprocess,hashlib,gzip
r=Path('runs/20261007-companion-priority/pbps-actual-physical-time-law81');out=r/'integration81'
assert json.loads((r/'integration.notes.json').read_bytes())['state_distinctions']['local_aggregate_and_generated_site_gates']
assert not subprocess.check_output(['git','diff','--cached','--name-only'],text=True).strip()
exclude=set()
if (r/'immutable-whitespace-archives81.json').exists():exclude={x['raw_path'] for x in json.loads((r/'immutable-whitespace-archives81.json').read_bytes())['files']}
logs=[]
for p in sorted(r.rglob('*.log')):
 raw=p.read_bytes();a=p.with_name(p.name+'.gz')
 if not a.exists():a.write_bytes(gzip.compress(raw,mtime=0))
 assert gzip.decompress(a.read_bytes())==raw
 logs.append(dict(path=p.as_posix(),RAW_sha256=hashlib.sha256(raw).hexdigest(),archive=a.as_posix(),archive_RAW_sha256=hashlib.sha256(a.read_bytes()).hexdigest()))
(out/'immutable-integration-log-archives81.json').write_text(json.dumps(logs,indent=2)+'\n',encoding='utf8',newline='\n')
owned=json.loads((out/'integration-scope.json').read_bytes())['owned']+[
 'research-wiki/frontier-cells/ASTIS-SW-PBPS-ideal-half-turn-kernel.json',
 'runs/substantive_advances.jsonl','docs/module-graph.svg','docs/assets/astis_lean_arsenal_module_graph.svg',
 'research-wiki/sampling-sde-library/lean-leaf-module-graph.md',
 'research-wiki/retrieval-index/astis-lean-arsenal-module-graph.json',
 'research-wiki/sampling-sde-library/cards/AutoSamplingTheory.ExampleCases.ProximalBPS.IdealHalfTurnKernel.md']
for p in r.rglob('*'):
 name=p.as_posix()
 if not p.is_file() or name in exclude or '__pycache__' in p.parts or p.suffix in {'.log','.html','.pyc'} or name.endswith('.text.txt'):continue
 owned.append(name)
source_preread=Path('runs/20261007-companion-priority/pbps-physical-time-law-preread81')
owned += [p.as_posix() for p in source_preread.rglob('*') if p.is_file() and p.suffix in {'.json','.md','.py'} and '__pycache__' not in p.parts]
next_preread=Path('runs/20261007-companion-priority/pbps-process-regularity-preread82')
owned += [p.as_posix() for p in next_preread.rglob('*') if p.is_file() and p.suffix in {'.json','.md','.py'} and '__pycache__' not in p.parts]
subprocess.run(['git','-c','core.autocrlf=false','add','--',*sorted(set(owned))],check=True)
check=subprocess.run(['git','-c','core.whitespace=cr-at-eol','diff','--cached','--check'],capture_output=True)
if check.returncode:
 (out/'staged-diff-check.failed.log').write_bytes(check.stdout+check.stderr)
 print(check.stdout.decode('utf8',errors='replace'));raise SystemExit(check.returncode)
(out/'staged-scope81.json').write_text(json.dumps(dict(paths=subprocess.check_output(['git','diff','--cached','--name-only'],text=True).splitlines(),preserved_unstaged=True),indent=2)+'\n',encoding='utf8',newline='\n')
subprocess.run(['git','-c','core.autocrlf=false','add','--',(out/'staged-scope81.json').as_posix()],check=True)
subprocess.run(['git','commit','-m','Integrate verified ideal PBPS half-turn kernel and reader evidence'],check=True)
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
(out/'commit-observed81.json').write_text(json.dumps(dict(commit=head,science=json.loads((out/'integration-scope.json').read_bytes())['science_commit'],main_merged=False,purified=False,Goal_complete=False),indent=2)+'\n',encoding='utf8',newline='\n')
print(head)
