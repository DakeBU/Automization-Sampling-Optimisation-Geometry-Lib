"""Resume staged integration after an absolute-vs-index-relative archive lookup error."""
from pathlib import Path
import json,hashlib,gzip,subprocess
R=Path.cwd();r=Path(__file__).parent;out=r/'integration91';load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
note=load(r/'integration.notes.json');assert note['state_distinctions']['local_aggregate_and_generated_site_gates']
assert subprocess.check_output(['git','rev-parse','HEAD']).decode().strip()==note['science_commit']
saved=load(r/'exact-commit-verification91/closed-RAW-manifest91.json')['preserved_collaborator_inputs']
for d in saved:assert sha(Path(d['path']).read_bytes())==d['raw_sha256']
actual=set(subprocess.check_output(['git','diff','--cached','--name-only']).decode().splitlines())
claim=load(r/'claim.json');cp='research-wiki/frontier-cells/'+claim['frontier_cell']+'.json'
shared=set(load(out/'integration-scope.json')['owned']+[cp,'runs/substantive_advances.jsonl','docs/module-graph.svg','docs/assets/astis_lean_arsenal_module_graph.svg','research-wiki/sampling-sde-library/lean-leaf-module-graph.md','research-wiki/retrieval-index/astis-lean-arsenal-module-graph.json','research-wiki/sampling-sde-library/cards/AutoSamplingTheory.ExampleCases.ProximalBPS.ActualAbsoluteNextEventTime.md'])
prefix=r.resolve().relative_to(R).as_posix()+'/'
assert actual and cp in actual and all(p in shared or p.startswith(prefix) for p in actual)
assert not actual.intersection(d['path'] for d in saved)
index={}
for line in subprocess.check_output(['git','ls-files','-sz']).split(b'\0'):
 if line:
  meta,name=line.split(b'\t',1);index[name.decode()]=meta.split()[1].decode()
rows=load(out/'immutable-integration-RAW-archives91.json')['files']
for d in rows:
 name=Path(d['archive']).resolve().relative_to(R).as_posix()
 b=subprocess.check_output(['git','cat-file','blob',index[name]])
 assert sha(b)==d['archive_raw_sha256'] and sha(gzip.decompress(b))==d['raw_sha256'],name
diag=out/'archive-index-path-resolution.json'
diag.write_text(json.dumps(dict(failure='Initial commit script used absolute native archive path as Git index key.',resolution='Normalize archive path relative to repository, resolve index blob, verify every compressed and native RAW hash.',archive_count=len(rows),math_or_native_evidence_changed=False),indent=2)+'\n',encoding='utf8',newline='\n')
subprocess.run(['git','-c','core.autocrlf=false','add','-f','--',str(Path(__file__).resolve().relative_to(R)),str(diag.resolve().relative_to(R))],check=True)
q=subprocess.run(['git','-c','core.whitespace=cr-at-eol','diff','--cached','--check'],capture_output=True)
assert q.returncode==0,(q.stdout+q.stderr).decode(errors='replace')[:4000]
actual=set(subprocess.check_output(['git','diff','--cached','--name-only']).decode().splitlines())
stage=out/'staged-scope91.json';assert not stage.exists()
stage.write_text(json.dumps(dict(paths=sorted(actual),independently_verified_frontier_staged=True,preserved_collaborator_files=21,archive_count=len(rows),sole_lane=note['sole_lane'],main_merged=False,purified=False,Goal_complete=False),indent=2)+'\n',encoding='utf8',newline='\n')
subprocess.run(['git','-c','core.autocrlf=false','add','--',str(stage.resolve().relative_to(R))],check=True)
subprocess.run(['git','commit','-q','-m','Integrate verified actual PBPS next absolute event-time law'],check=True)
for d in saved:assert sha(Path(d['path']).read_bytes())==d['raw_sha256']
print('INTEGRATION_COMMIT',subprocess.check_output(['git','rev-parse','HEAD']).decode().strip())
