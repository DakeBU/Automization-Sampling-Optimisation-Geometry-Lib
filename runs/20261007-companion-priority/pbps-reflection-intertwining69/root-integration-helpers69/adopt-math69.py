from pathlib import Path
import hashlib,json,os,subprocess
r=Path('runs/20261007-companion-priority/pbps-reflection-intertwining69');o=r/'independent-math69'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def check(z):
 p=Path(z['path']);b=p.read_bytes();lf=b.replace(b'\r\n',b'\n')
 assert len(b)==z['raw_bytes'] and sha(b)==z['raw_sha256'],p
 assert len(lf)==z['lf_bytes'] and sha(lf)==z['lf_sha256'],p
lease=load(o/'lease.final.json')
assert sha((o/'lease.final.json').read_bytes())=='aaae65625bf8d014c19d7dd1e0ff07e258d661bc4e154bf38570d16a6c32f702'
assert lease['status']=='CLOSED_LAST' and lease['last_owned_write']=='lease.final.json' and lease['no_more_owned_writes']
assert lease['actor']=='/root/exact_science63' and not lease['VERIFIED']
rows=lease['all_owned_outputs_except_only_self'];actual={p.resolve() for p in o.rglob('*') if p.is_file()}
assert actual=={Path(z['path']).resolve() for z in rows}|{(o/'lease.final.json').resolve()}
assert len(rows)==111 and len(actual)==lease['owned_file_count_including_self']==112
last=(o/'lease.final.json').stat().st_mtime_ns
for z in rows:check(z);assert Path(z['path']).stat().st_mtime_ns<=last
run=load(o/'run.json');h=run.pop('run_sha256')
assert sha(can(run))==h==lease['whole_logical_run_sha256']=='11dbc903eceb91f2d53fb58397299cfe74acd746e8dc6145b60f38ef2bcbe3e1'
assert run['status']=='ACCEPTED_THEOREM_ONLY69_PRECOMMIT' and run['mathematical_blockers']==run['mathematical_repairs']==[]
assert run['fakeclosures']==run['private_mathematical_providers']==0 and run['same_existential_witnesses']==12
assert run['all_kerP_not_rangeV'] and run['no_sharp_energy68_dependency'] and run['rank0_alphaeta1_retained']
assert set(run['exact_standard3'])=={'propext','Classical.choice','Quot.sound'}
assert run['fresh_compiler']['exit_code']==0 and run['fresh_compiler']['terminal_closed'] and run['fresh_compiler']['actual_foreground_Lake_PID']==1612
assert run['checked_base_commit']==subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
check(run['candidate_RAW']);check(run['input_manifest']);check(run['named_complete_RAW_review'])
assert run['named_complete_RAW_review']['raw_sha256']=='59bae5745f3d575ac2f1d2548f1b240326dabd0cf3198ab7520e8c38ffab84fd'
m=load(o/'inputs.manifest.json');assert m['input_count']==len(m['inputs'])==28 and m['finite_current_to_frozen_maps']==[]
for z in m['inputs']:
 for k in ['original','RAW_snapshot','LF_snapshot']:check(z[k])
 b=Path(z['original']['path']).read_bytes()
 assert Path(z['RAW_snapshot']['path']).read_bytes()==b
 assert Path(z['LF_snapshot']['path']).read_bytes()==b.replace(b'\r\n',b'\n')
dest=r/'root.math69.adoption.json';assert not dest.exists()
payload=dict(status='ACCEPTED_NATIVE_THEOREM_ONLY69_MATHEMATICS',actual_root_pid=os.getpid(),
 native_files=112,current_inputs=28,native_whole_logical_run_sha256=h,native_complete_RAW_sha256=run['named_complete_RAW_review']['raw_sha256'],native_lease_RAW_sha256=sha((o/'lease.final.json').read_bytes()),
 candidate_RAW=run['candidate_RAW'],mathematical_repairs=[],fresh_compiler=run['fresh_compiler'],native_bytes_unchanged=True,
 source_review=False,publication_review=False,reader_admission=False,VERIFIED=False,full_paper=False,Goal_complete=False)
dest.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('PASS native math69 CLOSED112/28 exact current inputs accepted; theorem only, not source/VERIFIED/integration.')
