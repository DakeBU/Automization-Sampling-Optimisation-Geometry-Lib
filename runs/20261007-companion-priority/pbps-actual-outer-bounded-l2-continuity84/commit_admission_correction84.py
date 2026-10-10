from pathlib import Path
import gzip,hashlib,json,subprocess
r=Path(__file__).parent;out=r/'integration84/cell-admission-correction'
load=lambda p:json.loads(Path(p).read_bytes())
decision=load(out/'independent-repair/decision.json')
assert decision['status']=='ACCEPTED_BOUNDED_CONTROL_PLANE_RESTORE_WITH_EXPLICIT_GRAPH_LIMITATION',decision
assert not subprocess.check_output(['git','diff','--cached','--name-only'],text=True).strip()
owned=['docs/companion-papers-handoff.md','research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-outer-bounded-l2-continuity.json']
for name in ['run_gates84.py','commit_integration84.py','fix_integration_admission84.py','scope_graph_evidence84.py','integration.corrected.notes.json','commit_admission_correction84.py','push_and_pr84_corrected.py']:
 owned.append((r/name).as_posix())
for p in out.rglob('*'):
 if p.is_file() and p.suffix not in {'.log','.diff','.pyc'} and '__pycache__' not in p.parts:owned.append(p.as_posix())
for p in out.rglob('*.log'):
 raw=p.read_bytes();a=Path(str(p)+'.gz')
 if not a.exists():a.write_bytes(gzip.compress(raw,mtime=0))
 assert gzip.decompress(a.read_bytes())==raw
 owned.append(a.as_posix())
base=load(r.parent/'pbps-outer-bounded-l2-preread84/pre-fetch84.workspace-RAW.json')['tracked_modified']
for p,h in base.items():assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==h,p
owned=sorted(set(owned));assert not set(owned)&set(base)
for offset in range(0,len(owned),25):subprocess.run(['git','-c','core.autocrlf=false','add','--',*owned[offset:offset+25]],check=True)
subprocess.run(['git','-c','core.whitespace=cr-at-eol','diff','--cached','--check'],check=True)
subprocess.run(['git','commit','-q','-m','Restore verified PBPS84 frontier admission and scope graph evidence'],check=True)
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
path='research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-outer-bounded-l2-continuity.json'
assert subprocess.check_output(['git','show',head+':'+path])==Path(path).read_bytes()
assert load(path)['status']=='independently_verified'
print('CORRECTIVE_COMMIT',head)
