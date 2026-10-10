from pathlib import Path
import hashlib,json,os,subprocess
r=Path('runs/20261007-companion-priority/pbps-actual-projected-rotation70');o=r/'independent-math70'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest();can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def check(z):
 b=Path(z['path']).read_bytes();lf=b.replace(b'\r\n',b'\n');assert len(b)==z['raw_bytes'] and sha(b)==z['raw_sha256'];assert len(lf)==z['lf_bytes'] and sha(lf)==z['lf_sha256']
lease=load(o/'lease.final.json');assert sha((o/'lease.final.json').read_bytes())=='cafa34e277b842fb18d0fa826fefaa882a4d777366265ca3cfb323c3fa3c1093'
assert lease['status']=='CLOSED_LAST' and lease['actor']=='/root/exact_science63' and lease['last_owned_write'] and not lease['postclose_writes_allowed']
rows=lease['manifest'];assert sha(can(rows))==lease['manifest_logical_sha256']
actual={p.resolve() for p in o.rglob('*') if p.is_file()};assert len(actual)==lease['owned_file_count']==121
assert actual=={Path(z['path']).resolve() for z in rows}|{(o/'lease.final.json').resolve()}
for z in rows:check(z);assert Path(z['path']).stat().st_mtime_ns<=(o/'lease.final.json').stat().st_mtime_ns
run=load(o/'run.json');h=sha(can({k:v for k,v in run.items() if k!='run_sha256'}))
assert h==run['run_sha256']==lease['whole_logical_run_sha256']=='ccac3218b60a3339a15038e9dd82768e9aa25b85114af3b34a04e27ac39357e0'
assert run['status']=='ACCEPTED_THEOREM_MATHEMATICS_ONLY_LOCAL_UNCOMMITTED70'
assert run['checked_base_commit']==subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
d=run['complete_named_review'];assert not d['mathematical_repairs_required'] and d['all_parent_clauses_preserved']
assert d['fake_closure']['hits']==d['fake_closure']['mathematical_providers']==0
assert d['fake_closure']['private_literal_definitions']==1 and d['fake_closure']['public_theorems']==1
compiler=d['fresh_compiler'];assert compiler['terminal_closed'] and compiler['exit_code']==0 and compiler['fresh_main_elaboration'] and not compiler['Lake_build_cache_replay']
assert set(compiler['axioms'])=={'propext','Classical.choice','Quot.sound'} and compiler['actual_foreground_Lake_PID']==42936
for k in ['freeze','compile','audit-v2','verdict-v2']:assert run['stage_terminals'][k]['terminal_closed'] and run['stage_terminals'][k]['exit_code']==0
assert run['stage_terminals']['audit']['exit_code']==run['stage_terminals']['verdict']['exit_code']==1
check(run['named_complete_RAW_payload']);assert run['named_complete_RAW_payload']['raw_sha256']=='156d6f8e94ace203d6e9e29da6c9f05aa02fd13d38a9b1cb1e459c7551bf82c3'
manifest=load(o/'inputs.manifest.json');assert manifest['input_count']==len(manifest['inputs'])==19 and manifest['root_frozen_input_count']==18
assert len(manifest['explicit_frozen_metadata_rows'])==1 and manifest['explicit_frozen_metadata_rows'][0]['row_index']==17
for i,z in enumerate(manifest['inputs']):
 for k in ['RAW_snapshot','LF_snapshot']:check(z[k])
 b=Path(z['RAW_snapshot']['path']).read_bytes();assert Path(z['LF_snapshot']['path']).read_bytes()==b.replace(b'\r\n',b'\n')
 assert len(b)==z['original']['raw_bytes'] and sha(b)==z['original']['raw_sha256']
 if i==17:
  assert z['original']['path'].endswith('/ASTIS-SW-PBPS-actual-projected-rotation.json')
  assert (r/'cell.before-publication70.json').read_bytes()==b
 else:
  check(z['original']);assert Path(z['original']['path']).read_bytes()==b
aux=run['auxiliary_inputs'];assert aux['input_count']==len(aux['inputs'])==15
for z in aux['inputs']:check(z['original'])
decision=load(o/'decision.json');assert decision['mathematics_accepted'] and not decision['mathematical_repair_required'] and not decision['SAU_VERIFIED'] and not decision['exact_SCI70_review']
dest=r/'root.math70.adoption.json';assert not dest.exists()
dest.write_text(json.dumps(dict(status='ACCEPTED_INDEPENDENT_THEOREM70_MATHEMATICS_ONLY',actual_root_PID=os.getpid(),
 native_files=121,current_core_inputs=18,explicit_frozen_historical_metadata_inputs=1,auxiliary_current_pins=15,
 historical_cell=manifest['explicit_frozen_metadata_rows'][0],
 native_whole_logical_run_sha256=h,native_complete_named_RAW_sha256=run['named_complete_RAW_payload']['raw_sha256'],native_lease_RAW_sha256=sha((o/'lease.final.json').read_bytes()),
 candidate_RAW=manifest['inputs'][0]['original'],checked_base_commit=run['checked_base_commit'],
 fresh_compiler=compiler,mathematical_repairs=[],native_bytes_unchanged=True,
 source_review=False,reader_admission=False,exact_SCI_verified=False,VERIFIED=False,full_paper=False,Goal_complete=False),indent=2)+'\n',encoding='utf-8',newline='\n')
print('PASS independent math70 CLOSED121/19 core+15aux; one explicit frozen cell mapping honored. Fresh42936EXIT0/standard3; mathematics only, source/exactSCI/integration pending.')
