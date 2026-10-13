from pathlib import Path
import hashlib,json,os,subprocess
r=Path('runs/20261007-companion-priority/pbps-actual-corrector-change71');o=r/'independent-math71'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest();can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def check(z):
 b=Path(z['path']).read_bytes();lf=b.replace(b'\r\n',b'\n')
 assert len(b)==z['raw_bytes'] and sha(b)==z['raw_sha256'],z['path']
 assert len(lf)==z['lf_bytes'] and sha(lf)==z['lf_sha256'],z['path']
lease=load(o/'lease.final.json');assert sha((o/'lease.final.json').read_bytes())=='13f181fcfcb8eb40ce92808904c4c602199c3a4e0396bb6f1ea1f219195cd820'
assert lease['status']=='CLOSED_LAST' and lease['actor']=='/root/exact_science63' and lease['last_owned_write']=='lease.final.json' and lease['no_more_owned_writes']
rows=lease['all_owned_outputs_except_only_self'];assert sha(can(rows))==lease['closure_manifest_logical_sha256']
actual={p.resolve() for p in o.rglob('*') if p.is_file()};assert len(actual)==lease['owned_file_count_including_self']==95
assert actual=={Path(z['path']).resolve() for z in rows}|{(o/'lease.final.json').resolve()}
for z in rows:check(z);assert Path(z['path']).stat().st_mtime_ns<=(o/'lease.final.json').stat().st_mtime_ns
run=load(o/'run.json');h=sha(can({k:v for k,v in run.items() if k!='run_sha256'}))
assert h==run['run_sha256']==lease['whole_logical_run_sha256']=='90b3b83f5de254f49b90dccb4f046c3dd048ad0ecc2aa1130f30646894f819a5'
assert run['status']=='ACCEPTED_LOCAL_THEOREM_MATHEMATICS71_ONLY'
assert run['checked_base_commit']==subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
check(run['named_complete_RAW_review']);assert run['named_complete_RAW_review']['raw_sha256']=='e7f8c6dcac107780a8752fd146a09e77bd643ea34ee4dd6bbf21b8dff6dfa63b'
manifest=load(o/'inputs.manifest.json');assert manifest['input_count']==len(manifest['inputs'])==14 and manifest['root_frozen_count']==12
for z in manifest['inputs']:
 for k in ['RAW_snapshot','LF_snapshot','original']:check(z[k])
 b=Path(z['RAW_snapshot']['path']).read_bytes();assert Path(z['LF_snapshot']['path']).read_bytes()==b.replace(b'\r\n',b'\n')
 assert Path(z['original']['path']).read_bytes()==b
aux=load(o/'auxiliary.inputs.manifest.json');assert aux['input_count']==len(aux['inputs'])==15
for z in aux['inputs']:check(z)
verdict=load(o/'mathematical-verdict.json');assert verdict['status']=='ACCEPTED_LOCAL_THEOREM_MATHEMATICS_ONLY' and not verdict['mathematical_repairs_required']
assert verdict['all_parent70_clauses_retained'] and verdict['exact147line_seal'] and verdict['fakeclosure_hits']==0 and verdict['no_provider']
compiler=load(o/'compiler.result.json');receipt=compiler['receipt'];assert compiler['fresh_production_Lean_elaboration'] and not compiler['Lake_cache_replay']
assert set(compiler['exact_standard3'])=={'propext','Classical.choice','Quot.sound'}
assert receipt['actual_foreground_PID']==3064 and receipt['exit_code']==0 and receipt['terminal_closed']
dest=r/'root.math71.adoption.json';assert not dest.exists()
dest.write_text(json.dumps(dict(status='ACCEPTED_INDEPENDENT_THEOREM71_MATHEMATICS_ONLY',actual_root_PID=os.getpid(),native_files=95,current_core_inputs=14,auxiliary_current_pins=15,native_whole_logical_run_sha256=h,native_complete_named_RAW_sha256=run['named_complete_RAW_review']['raw_sha256'],native_lease_RAW_sha256=sha((o/'lease.final.json').read_bytes()),candidate_RAW=run['checked_source'],checked_base_commit=run['checked_base_commit'],fresh_compiler=receipt,mathematical_repairs=[],native_bytes_unchanged=True,source_review=False,reader_admission=False,exact_SCI_verified=False,VERIFIED=False,full_paper=False,Goal_complete=False),indent=2)+'\n',encoding='utf8',newline='\n')
print('PASS independent math71 CLOSED95/14 core+15aux; fresh3064EXIT0/standard3; no source/exactSCI/integration credit.')
