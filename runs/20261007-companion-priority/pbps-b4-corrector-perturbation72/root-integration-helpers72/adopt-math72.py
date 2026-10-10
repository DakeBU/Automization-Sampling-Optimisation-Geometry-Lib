from pathlib import Path
import hashlib,json,os,subprocess
r=Path('runs/20261007-companion-priority/pbps-b4-corrector-perturbation72');o=r/'independent-math72'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest();can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def check(z):
 b=Path(z['path']).read_bytes();lf=b.replace(b'\r\n',b'\n')
 assert len(b)==z['RAW_bytes'] and sha(b)==z['RAW_sha256'],z['path']
 assert len(lf)==z['LF_bytes'] and sha(lf)==z['LF_sha256'],z['path']
lease=load(o/'lease.final.json');assert sha((o/'lease.final.json').read_bytes())=='8102f8f1cd10715c76774980569abcd9242712e2696f4e24b58ef21d2f36509d'
assert lease['status']=='CLOSED_LAST' and lease['actor']=='/root/exact_science63'
rows=lease['all_owned_outputs_except_only_self'];assert sha(can(rows))==lease['closure_manifest_logical_sha256']
actual={p.resolve() for p in o.rglob('*') if p.is_file()};assert len(actual)==lease['owned_count']==82
assert actual=={Path(z['path']).resolve() for z in rows}|{(o/'lease.final.json').resolve()}
for z in rows:check(z);assert Path(z['path']).stat().st_mtime_ns<=(o/'lease.final.json').stat().st_mtime_ns
run=load(o/'run.json');h=sha(can({k:v for k,v in run.items() if k!='run_sha256'}))
assert h==run['run_sha256']==lease['whole_logical_run_sha256']=='9cc879af1249f956ef103ba0d784f658f1dfa878eb74e8fe96b540dc090c8744'
assert run['status']=='ACCEPTED_MATHEMATICS_ONLY' and not run['VERIFIED'] and not run['source_review']
assert run['checked_HEAD']==subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
for k in ['complete_named_RAW_payload','input_manifest','output_manifest','verdict','compiler']:check(run[k])
payload=load(o/'complete-named-mathematical-review.payload.json')
for key,value in payload.items():
 if key.endswith('.json') and (o/key).is_file():assert value==load(o/key),key
manifest=load(o/'inputs.manifest.json');assert manifest['input_count']==len(manifest['inputs'])==15
for z in manifest['inputs']:
 for k in ['RAW_snapshot','LF_snapshot','original']:check(z[k])
 b=Path(z['RAW_snapshot']['path']).read_bytes();assert Path(z['LF_snapshot']['path']).read_bytes()==b.replace(b'\r\n',b'\n')
 assert Path(z['original']['path']).read_bytes()==b
aux=load(o/'auxiliary.inputs.manifest.json');assert aux['input_count']==len(aux['inputs'])==5
for z in aux['inputs']:check(z)
v=load(o/'mathematical-verdict.json');assert v['status']=='ACCEPTED_LOCAL_TWO_THEOREM_IMPLEMENTATIONS_MATHEMATICS_ONLY'
assert not v['mathematical_repairs'] and v['whole_lines']==494 and v['original_analytic_callers']==6 and v['common_witnesses']==12
assert v['parent71_literal_all_clauses_retained'] and v['fake_closure_hits']==0 and v['private_providers']==0 and v['rank_zero_alphaeta_one_legal']
c=load(o/'compiler.result.json');assert c['new_source_elaborated_without_requested_olean'] and len(c['results'])==2
for i,z in enumerate(c['results']):
 assert z['actual_foreground_PID']==[22524,41536][i] and z['exit_code']==0 and z['fresh_source_elaboration'] and not z['Lake_cache_replay'] and not z['output_olean_requested']
 assert set(z['standard_axioms'])=={'propext','Classical.choice','Quot.sound'};check(z['receipt'])
 p=load(z['receipt']['path']);assert p['terminal_closed'] and p['exit_code']==0
dest=r/'root.math72.adoption.json';assert not dest.exists()
dest.write_text(json.dumps(dict(status='ACCEPTED_INDEPENDENT_TWO_IMPLEMENTATIONS72_MATHEMATICS_ONLY',actual_root_PID=os.getpid(),native_files=82,current_core_inputs=15,auxiliary_current_pins=5,native_whole_logical_run_sha256=h,native_complete_named_RAW_sha256=run['complete_named_RAW_payload']['RAW_sha256'],native_lease_RAW_sha256=sha((o/'lease.final.json').read_bytes()),checked_HEAD=run['checked_HEAD'],fresh_compilers=c['results'],mathematical_repairs=[],native_bytes_unchanged=True,source_review=False,exact_SCI_verified=False,VERIFIED=False,Goal_complete=False),indent=2)+'\n',encoding='utf8',newline='\n')
print('PASS math72 CLOSED82 /15core+5aux; fresh22524+41536EXIT0/standard3; whole494lines/same6callers12witnesses. No source/VERIFIED credit.')
