from pathlib import Path
import hashlib,json,os,subprocess
root=Path.cwd();r=root/'runs/20261007-companion-priority/pbps-centered-root64';d=r/'exact-science-verification'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
run,lease,verdict=[load(d/n) for n in ['run.json','lease.json','verdict.json']]
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
assert head==run['checked_commit']==lease['checked_commit']==verdict['checked_commit']=='59fff63d320aa5e3dc4b45e81e40e2029ce42734'
assert lease['status']=='CLOSED_LAST' and lease['state']=='VERIFIED_BOUNDED'
assert verdict['status']=='PASS_BOUNDED_INDEPENDENT_VERIFIED' and verdict['actor']!=verdict['proving_owner']
assert sha(can({k:v for k,v in run.items() if k!='run_sha256'}))==run['run_sha256']==lease['whole_logical_run_sha256']=='e9fed3a1bd5d05a08f5ccc9156b1ae2c187124df1abf1f4be2a30cfbff1df9ae'
assert run['verdict']==verdict
payload=(d/'named-verification.payload.json').read_bytes()
assert payload==(d/'verdict.json').read_bytes()
assert sha(payload)==lease['distinct_COMPLETE_named_RAW_verdict_payload_sha256']=='a24f9dc8046aa2c4df8ab9e5d8104beafddf1bdba3219fbaa66ccbae9d9a5c1a'
def check_pin(x):
 b=Path(x['path']).read_bytes();assert sha(b)==x['raw_sha256'],x['path']
 if 'lf_sha256' in x:assert sha(b.replace(b'\r\n',b'\n'))==x['lf_sha256'],x['path']
 for f in ['raw_bytes','bytes']:
  if f in x:assert len(b)==x[f],x['path']
 return b
owned=lease['complete_owned_output_manifest_after_actual_readback']
for row in owned:check_pin(row)
assert {Path(x['path']).resolve() for x in owned}|{(d/'lease.json').resolve()}=={p.resolve() for p in d.rglob('*') if p.is_file()}
assert len(owned)+1==72
bindings=load(d/'bindings.result.json');supplement=load(d/'supplemental-bindings.result.json')
assert bindings['status']=='PASS' and supplement['status']=='PASS'
for x in bindings['finite_exact_historical_mappings']:
 assert sha(Path(x['explicit_snapshot']).read_bytes())==x['raw_sha256']
for x in bindings['native_pin_resolutions']:
 assert sha(Path(x['resolved_path']).read_bytes())==x['raw_sha256']
for row in supplement['complete_closed_native_and_frozen_input_commit_bindings']:
 assert sha((root/row['path']).read_bytes())==row['working_RAW_sha256']
assert len(supplement['complete_closed_native_and_frozen_input_commit_bindings'])==466
focus=load(d/'focused.result.json');assert focus['status']=='PASS' and focus['jobs']==3944
for label in ['focused','publication','contributor','semantic','frontier','focused-reviewed-fakeclosure','bindings-v5','supplemental-bindings-v2','finalizer','readback']:
 x=load(d/label/'receipt.json');assert x['exit_code']==0 and x['terminal_closed'],label
transition=load(d/'transition.result.json');assert transition['to_state']=='VERIFIED' and transition['non_owner_actor']=='/root/exact_science63'
before,after=load(d/'ledger.before.pin.json'),load(d/'ledger.after.pin.json');ledger=(root/'runs/substantive_advances.jsonl').read_bytes()
assert sha(ledger)==after['raw_sha256'] and sha(ledger[:before['raw_bytes']])==before['raw_sha256']
assert ledger[before['raw_bytes']:]==check_pin(transition['exact_appended_RAW'])
row=json.loads(ledger[before['raw_bytes']:]);assert row['to_state']=='VERIFIED' and row['worker_id']=='/root/exact_science63'
def write(p,x):
 assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
adoption=dict(native_verified=True,verified_commit=head,native_verifier=verdict['actor'],actual_adopter_pid=os.getpid(),native_run_sha256=run['run_sha256'],native_complete_RAW_verdict_sha256=sha(payload),native_lease_RAW_sha256=sha((d/'lease.json').read_bytes()),native_owned_files=72,committed_artifact_bindings=466,finite_historical_maps=len(bindings['finite_exact_historical_mappings']),native_pin_resolutions=len(bindings['native_pin_resolutions']),compiler_jobs=3944,proper_non_owner_transition=transition,remaining_boundary=verdict['remaining_boundary'],aggregate_integration=False,full_paper_PURIFIED_ExpositionSeal_Goal=False)
write(r/'root.exact-verification64.adoption.json',adoption)
write(r/'verified.json',dict(status='VERIFIED',checked_commit=head,verifier=verdict['actor'],native_verdict=(d/'verdict.json').as_posix(),native_lease=(d/'lease.json').as_posix(),root_adoption=(r/'root.exact-verification64.adoption.json').as_posix(),new_VERIFIED_append=False,remaining_boundary=verdict['remaining_boundary']))
print('PASS exact SCI64 CLOSED_LAST adoption:72 owned,466 artifact bindings,3944 jobs; existing non-owner VERIFIED adopted, no new transition.')
