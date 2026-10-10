from pathlib import Path
import copy, hashlib, json, subprocess, sys
R=Path.cwd();r=Path('runs/20261007-companion-priority/pbps-actual-projected-rotation70');out=r/'search-label-repair70';out.mkdir(exist_ok=False)
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda p:json.loads(Path(p).read_bytes())
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),LF_sha256=sha(b.replace(b'\r\n',b'\n')))
parent=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();assert parent=='e44b6b1e08c8a259a1f48006d822b53efd3fecb8'
native=r/'exact-science-verification70';lease=load(native/'lease.final.json');assert lease['status']=='CLOSED_LAST'
assert sha((native/'lease.final.json').read_bytes())=='2426e1202aa7d96a867587a3c2e1620e3348abb5c2ce456fd93b7c4b481b8c32'
for row in lease['all_owned_outputs_except_only_self']:
 b=Path(row['path']).read_bytes();assert len(b)==row['raw_bytes'] and sha(b)==row['raw_sha256'];assert sha(b.replace(b'\r\n',b'\n'))==row['lf_sha256']
verdict=load(native/'verification-verdict.json');assert verdict['status']=='BLOCKED_REQUIRED_FRONTIER_SEARCH_LABEL' and not verdict['VERIFIED']
p=Path('research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-projected-rotation.json');before=p.read_bytes();old=json.loads(before);new=copy.deepcopy(old)
changes=verdict['typed_blocker']['minimal_honest_correction_after_closure'];assert len(changes)==2
for change in changes:
 parts=change['pointer'].strip('/').split('/');assert parts in [['shared_floor_audit','searched','0'],['reuse_plan','searched_existing','0']]
 assert new[parts[0]][parts[1]][0]==change['before'];assert change['proposed']=='Samplinglib: '+change['before'];new[parts[0]][parts[1]][0]=change['proposed']
(out/'cell.before.exactraw.json').write_bytes(before)
nl='\r\n' if b'\r\n' in before else '\n';after=(json.dumps(new,ensure_ascii=False,indent=2)+'\n').replace('\n',nl).encode();p.write_bytes(after)
assert sha(Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualProjectedRotation.lean').read_bytes())=='03a0721ae952f744d0bfdf568039b77f7035bec0a50642f8bc8ebc895273b998'
receipt=dict(status='EXACT_TWO_RECORDED_SEARCH_LABELS_CORRECTED_ONLY',parent=parent,changes=changes,cell_before=pin(out/'cell.before.exactraw.json'),cell_after=pin(p),native_lease=pin(native/'lease.final.json'),native_count=lease['owned_file_count_including_self'],closed_verdict_observer_limitation='typed_blocker.exact_error is empty; native frontier receipt and stderr retain the real diagnostic.',math_source_statement_BODY_and_native_unchanged=True,VERIFIED=False)
(out/'repair.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
subprocess.run([sys.executable,'-X','utf8','tools/astis_frontier_cells.py','check'],check=True)
subprocess.run([sys.executable,'-X','utf8','tools/astis_publication.py','check','--base',parent],check=True)
subprocess.run([sys.executable,'-X','utf8','tools/astis_contributor_contract.py','check','--base',parent],check=True)
paths=[p.as_posix()]+[q.as_posix() for q in out.iterdir() if q.is_file()]
assert not subprocess.check_output(['git','diff','--cached','--name-only'],text=True).strip()
subprocess.run(['git','-c','core.autocrlf=false','add','-f','--']+paths,check=True)
subprocess.run(['git','-c','core.whitespace=cr-at-eol','diff','--cached','--check'],check=True)
subprocess.run(['git','commit','-q','-m','Label recorded Samplinglib retrieval for projected rotation gate'],check=True)
print('PASS exact two metadata labels; new commit',subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip())
