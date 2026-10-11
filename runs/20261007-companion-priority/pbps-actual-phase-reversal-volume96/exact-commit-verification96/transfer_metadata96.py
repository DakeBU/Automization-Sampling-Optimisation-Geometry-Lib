"""Independently transfer unchanged science checks across the exact two-file metadata repair."""
from pathlib import Path
import json,hashlib,subprocess,copy
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent;T=O/'trial949bd4c';B=O.parent
OLD='949bd4cb5e780c590055aefe327358d7ffe8f2e8';C='2f2e2c01856c902b07406db87026c50639454d71'
CELL='research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-phase-reversal-volume.json';FIX=(B/'reuse-parent-metadata-repair96.json').relative_to(R).as_posix()
sha=lambda b:hashlib.sha256(b).hexdigest();load=lambda p:json.loads(p.read_bytes())
def git(*a):return subprocess.check_output(['git',*a],cwd=R,stderr=subprocess.PIPE)
def save(n,v):
 p=O/n;assert not p.exists();p.write_bytes((json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode())
assert git('rev-parse','HEAD').decode().strip()==C and git('rev-parse',C+'^').decode().strip()==OLD
assert set(git('diff','--name-only',OLD,C).decode().splitlines())=={CELL,FIX}
before=git('show',OLD+':'+CELL);after=git('show',C+':'+CELL);old=json.loads(before);new=json.loads(after);repair=load(R/FIX)
assert after==(R/CELL).read_bytes() and git('show',C+':'+FIX)==(R/FIX).read_bytes()
assert sha(before)==repair['before_raw_sha256'] and sha(after)==repair['after_raw_sha256']
want=copy.deepcopy(old);want['reuse_plan']['reused_declarations']=want['reuse_plan']['planned_dependencies'];want['reuse_plan']['planned_dependencies']=[]
assert want==new and new['reuse_plan']['reused_declarations']==repair['reused_declarations'] and len(repair['reused_declarations'])==2
f=load(T/'input-freeze96.json');assert f['status']=='PASS' and f['verified_commit']==OLD
for x in f['exact_commit_matches']+f['local_pinned_or_excluded_inputs']+f['preserved_collaborator_inputs']:
 if x['path']==CELL:assert x['raw_sha256']==sha(before)
 else:assert sha((R/x['path']).read_bytes())==x['raw_sha256'],x['path']
f['verified_commit']=C;f['transferred_from_commit']=OLD;f['metadata_transfer']='metadata-transfer96.json'
for x in f['exact_commit_matches']:
 if x['path']==CELL:x.update(raw_sha256=sha(after),bytes=len(after),binding='exact Git blob after independently checked metadata-only correction',git_blob=git('rev-parse',C+':'+CELL).decode().strip())
f['exact_commit_matches'].append(dict(path=FIX,raw_sha256=sha((R/FIX).read_bytes()),bytes=(R/FIX).stat().st_size,binding='exact Git blob',git_blob=git('rev-parse',C+':'+FIX).decode().strip()))
save('input-freeze96.json',f)
for name in ['archive-audit96.json','source-decoder-bindings96.json']:
 v=load(T/name);v['verified_commit']=C;v['transferred_from_commit']=OLD;save(name,v)
for name in ['focused-module','current-sealed-kernel']:
 receipt=load(T/(name+'.receipt.json'));assert receipt['verified_commit']==OLD and receipt['exit_code']==0
 out=(T/(name+'.stdout.log')).read_bytes();err=(T/(name+'.stderr.log')).read_bytes()
 (O/(name+'.stdout.log')).write_bytes(out);(O/(name+'.stderr.log')).write_bytes(err)
 receipt.update(verified_commit=C,executed_at_commit=OLD,reused_successful_execution=True,transfer='metadata-transfer96.json',stdout_sha256=sha(out),stderr_sha256=sha(err));save(name+'.receipt.json',receipt)
save('metadata-transfer96.json',dict(status='PASS',verified_commit=C,previous_commit=OLD,only_changed_files=[CELL,FIX],exact_cell_change='Move the two already listed planned compiled parents into reused_declarations; empty planned_dependencies. No other cell field changed.',before_cell_raw_sha256=sha(before),after_cell_raw_sha256=sha(after),all_other_science_inputs_unchanged=True,all21collaborator_RAWs_preserved=True,successful_build_and_fresh_kernel_transferred=True,original_trial='trial949bd4c/closed-trial96.json',no_production_statement_lesson_publication_or_source_change=True))
print('PASS exact two-file metadata repair; unchanged kernel/source RAW checks transferred')
