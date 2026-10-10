from pathlib import Path
import hashlib,json,os,subprocess
root=Path.cwd();r=root/'runs/20261007-companion-priority/pbps-polar65';d=r/'exact-science-verification-v2';load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
lease,run,verdict=[load(d/n) for n in ['lease.final.json','run.json','verdict.json']]
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();assert head==lease['checked_commit']==run['checked_commit']==verdict['checked_commit']=='ecd9d1f10ad0241312492cefacd5fe48c317e9c2'
assert lease['status']=='CLOSED_LAST' and lease['last_owned_write'] and lease['final_owned_file_count']==62 and lease['VERIFIED_append']
assert sha((d/'lease.final.json').read_bytes())=='48fbd309c21621d685096b7e34d01b15933f20714a72191951d93727beab1c2f'
logical=sha(json.dumps({k:v for k,v in run.items() if k!='run_sha256'},ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
assert logical==run['run_sha256']==lease['whole_logical_run_sha256']=='0e337aa4d1c477f22e78629efdc5e8e5e1be49fdf70f026723b8d9cad2150d09'
assert sha(Path(run['complete_named_RAW_verdict_payload']['path']).read_bytes())==lease['complete_named_RAW_verdict_sha256']=='b9c1cfb5a9b6269c45d0999f03df897a67cb0fb5027f2cdfae3fd1378839ea6e'
def pin(x):
 b=Path(x['path']).read_bytes();assert len(b)==x['raw_bytes'] and sha(b)==x['raw_sha256'],x['path']
 assert sha(b.replace(b'\r\n',b'\n').replace(b'\r',b'\n'))==x['lf_sha256'],x['path']
 return b
listed={Path(x['path']).resolve() for x in lease['all_owned_except_this_final_lease']}|{(d/'lease.final.json').resolve()}
assert listed=={p.resolve() for p in d.rglob('*') if p.is_file()} and len(listed)==62
for x in lease['all_owned_except_this_final_lease']:pin(x)
inputs=load(d/'inputs.manifest.json');assert len(inputs['inputs'])==109
for x in inputs['inputs']:pin(x)
reuse=load(d/'reuse.result.json');assert reuse['status']=='PASS' and reuse['metadata_two_prefixes_only'] and not reuse['new_math_or_source_repair']
focus=load(d/'focused.result.json');assert focus['status']=='PASS' and focus['exit_code']==0 and focus['jobs']==3945 and focus['terminal_closed'] and focus['actual_compiler_pid']==37804
assert verdict['VERIFIED_appended'] and verdict['actor']=='/root/exact_science63'
t=load(d/'transition.result.json');assert t['exact_one_nonowner_append'] and t['to_state']=='VERIFIED' and t['verifier_id']=='/root/exact_science63' and t['verifier_id']!=t['proving_owner']
before=load(d/'ledger.before.pin.json');after=load(d/'ledger.after.pin.json');ledger=(root/'runs/substantive_advances.jsonl').read_bytes();suffix=pin(t['exact_appended_RAW'])
assert sha(ledger[:before['raw_bytes']])==before['raw_sha256'] and ledger[before['raw_bytes']:]==suffix and sha(ledger)==after['raw_sha256']
event=json.loads(suffix);assert event['to_state']=='VERIFIED' and event['worker_id']=='/root/exact_science63'
assert load(r/'verified.json')['verified_commit']==head
out=r/'root.exact-verification65.adoption.json';assert not out.exists()
out.write_text(json.dumps(dict(native_verified=True,verified_commit=head,native_verifier=verdict['actor'],actual_root_pid=os.getpid(),native_whole_logical_run_sha256=logical,native_complete_RAW_verdict_sha256=lease['complete_named_RAW_verdict_sha256'],native_lease_RAW_sha256=sha((d/'lease.final.json').read_bytes()),native_owned_files=62,finite_inputs=109,compiler_jobs=3945,proper_non_owner_transition=t,remaining_boundary=verdict['remaining_boundary'],aggregate_integration=False,full_paper_PURIFIED_ExpositionSeal_Goal=False),ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('PASS exact SCI65b CLOSED62 adoption:109 inputs,3945 jobs,proper nonowner VERIFIED suffix; native named RAW distinct from logical run. Serialized aggregate pending.')
