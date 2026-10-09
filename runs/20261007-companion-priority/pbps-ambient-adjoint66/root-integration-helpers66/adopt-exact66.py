from pathlib import Path
import hashlib,json,os,subprocess,sys
root=Path.cwd();r=root/'runs/20261007-companion-priority/pbps-ambient-adjoint66';d=r/'exact-science-verification66';load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
C='a115115d42b3fa2b67885d87fe4d5300af36fcd1';P='31ce36e7ca01b203696918672c33d29a337550c3'
lease,run,verdict=[load(d/n) for n in ['lease.final.json','run.json','verdict.json']]
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==C==lease['checked_commit']==run['checked_commit']==verdict['checked_commit']
assert lease['parent']==P==verdict['actual_parent'] and lease['status']=='CLOSED_LAST' and lease['last_owned_write'] and lease['final_owned_file_count']==72
assert sha((d/'lease.final.json').read_bytes())=='ccd9c9559f0529afcd92325049e970c0cead105d8f14f4c48d780bec25a816ce'
logical=sha(json.dumps({k:v for k,v in run.items() if k!='run_sha256'},ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
assert logical==run['run_sha256']==lease['whole_logical_run_sha256']=='106e65e85805beb1309fbe8b0d4515d7f86087d538e3f1efaa0f435445e88dc6'
def pin(x):
 b=Path(x['path']).read_bytes();assert len(b)==x['raw_bytes'] and sha(b)==x['raw_sha256'],x['path']
 assert sha(b.replace(b'\r\n',b'\n').replace(b'\r',b'\n'))==x['lf_sha256'],x['path'];return b
assert sha(pin(run['complete_named_RAW_payload']))==lease['complete_named_RAW_payload']['raw_sha256']=='a44c25abf8e4014233270cf9e8fe9ba32c3a6e048a65680111b6da1a6f588256'
listed={Path(x['path']).resolve() for x in lease['all_owned_except_this_final_lease']}|{(d/'lease.final.json').resolve()}
assert listed=={p.resolve() for p in d.rglob('*') if p.is_file()} and len(listed)==72
last=(d/'lease.final.json').stat().st_mtime_ns
for x in lease['all_owned_except_this_final_lease']:pin(x);assert Path(x['path']).stat().st_mtime_ns<=last
inputs=load(d/'inputs.manifest.json');assert len(inputs['exact_Git_current_pins'])==18 and len(inputs['external_immutable_pins'])==39 and inputs['finite_maps_only']
for row in inputs['exact_Git_current_pins']:
 pin(row['current']);assert sha(subprocess.check_output(['git','show',C+':'+row['path']]))==row['Git_RAW_sha256']
for row in inputs['external_immutable_pins']:pin(row)
focus=load(d/'focused.result.json');assert focus['status']=='PASS' and focus['jobs']==3946 and focus['fresh_Test_proof_compilation'] and all(set(q['axioms'])=={'propext','Classical.choice','Quot.sound'} for q in focus['standard3'])
assert verdict['status']=='ACCEPTED_VERIFIED' and verdict['independent_verifier']=='/root/exact_science63'
t=load(d/'transition.result.json');assert t['status']=='VERIFIED' and t['proper_nonowner_transition'] and t['appended_events']==1 and t['verifier_id']=='/root/exact_science63' and t['verifier_id']!=t['proving_owner']
before=t['ledger_before'];ledger=pin(t['ledger_after']);suffix=pin(t['exact_appended_event']);assert sha(ledger[:before['raw_bytes']])==before['raw_sha256'] and ledger[before['raw_bytes']:]==suffix
event=json.loads(suffix);assert event['to_state']=='VERIFIED' and event['worker_id']=='/root/exact_science63'
assert load(r/'verified.json')['checked_commit']==C
bindings=load(d/'bindings.result.json');assert bindings['publication_binding_sha256']=='3d1d9d97cc4ae200fb0b07584cc5a89e6805851d05d0c640f3d3e4b3106bdc7f' and bindings['publication_context_sha256']=='d668766750b3e3471ea7b0d50fd3d562a81ec2044cdc8c210891f4671e6ca60b'
assert load(d/'reviewed-fakeclosure.result.json')['actual_repository_forbidden_pattern_hits']==[]
for label in ['freeze','focused','bindings','gates','transition','finalize','readback']:assert load(d/(label+'.terminal.json'))['exit_code']==0,label
before_files={p.as_posix():(sha(p.read_bytes()),p.stat().st_mtime_ns) for p in d.rglob('*') if p.is_file()}
subprocess.run([sys.executable,'-B','-X','utf8',str(d/'close66.py'),'postclose'],check=True)
assert before_files=={p.as_posix():(sha(p.read_bytes()),p.stat().st_mtime_ns) for p in d.rglob('*') if p.is_file()}
out=r/'root.exact-verification66.adoption.json';assert not out.exists()
out.write_text(json.dumps(dict(native_verified=True,verified_commit=C,actual_parent=P,native_verifier=verdict['independent_verifier'],actual_root_pid=os.getpid(),native_whole_logical_run_sha256=logical,native_complete_RAW_payload_sha256=lease['complete_named_RAW_payload']['raw_sha256'],native_lease_RAW_sha256=sha((d/'lease.final.json').read_bytes()),native_owned_files=72,finite_Git_inputs=18,finite_external_inputs=39,compiler_jobs=3946,proper_non_owner_transition=t,remaining_boundary=verdict['remaining_boundary'],postclose_owned_writes=0,aggregate_integration=False,full_paper_PURIFIED_ExpositionSeal_Goal=False),ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('PASS exact SCI66 CLOSED72 adoption:18 Git/39 external inputs,3946 jobs,proper nonowner VERIFIED suffix; native named RAW distinct from logical run. Serialized aggregate pending.')
