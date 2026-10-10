from pathlib import Path
import hashlib,json,os,subprocess,sys
root=Path.cwd();sys.path.insert(0,str(root/'tools'));import astis_advance as adv
r=Path('runs/20261007-companion-priority/pbps-actual-corrector-change71');o=r/'exact-science-verification71'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest();can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def check(z):
 b=Path(z['path']).read_bytes();lf=b.replace(b'\r\n',b'\n')
 assert (len(b),sha(b),len(lf),sha(lf))==(z['RAW_bytes'],z['RAW_sha256'],z['LF_bytes'],z['LF_sha256']),z['path'];return b
lease=load(o/'lease.final.json');assert sha((o/'lease.final.json').read_bytes())=='6d72b3697c5f80c11dc6b4c58fd00c4e0d3eddbd1bb626991c92dac58e3e2444'
assert lease['status']=='CLOSED_LAST' and lease['actor']=='/root/exact_science63' and lease['approved_nonowner_VERIFIED'] and lease['no_more_owned_writes']
rows=lease['all_owned_outputs_except_only_self'];assert len(rows)+1==lease['owned_file_count_including_self']==116
assert sha(can(rows))==lease['closure_manifest_logical_sha256']=='97708cd1d49a9f28278606cf040942c5dbe259bcf770f2388ccfbf3e03a37bbe'
assert {p.resolve() for p in o.rglob('*') if p.is_file()}=={Path(z['path']).resolve() for z in rows}|{(o/'lease.final.json').resolve()}
for z in rows:check(z);assert Path(z['path']).stat().st_mtime_ns<=(o/'lease.final.json').stat().st_mtime_ns
q=subprocess.run([sys.executable,'-B','-X','utf8',str(o/'verify71.py'),'postclose'],capture_output=True,check=True)
readonly=json.loads(q.stdout);assert readonly['status']=='READ_ONLY_PASS' and readonly['owned_writes']==0 and readonly['closed']
run=load(o/'run.json');h=sha(can({k:v for k,v in run.items() if k!='run_sha256'}))
assert h==run['run_sha256']==lease['whole_logical_run_sha256']=='803d933f5677d76b97f07b5ddb1ccd56c83e53d3955d4ce0adbb4648290092fe'
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();assert head==run['checked_commit']==lease['checked_commit']=='4e7ce5d2996ffe1d1b0ab570778e02425c6be34e'
assert run['status']=='VERIFIED' and run['actor']=='/root/exact_science63' and run['closed_math_source_blind_counts']==[95,277,10]
assert check(run['named_complete_RAW_payload']) and run['named_complete_RAW_payload']['RAW_sha256']=='623a9b2828524b4aaa0c2c92b6660e961c83d8fb97be66d75259a67bef03272a'
payload=load(run['named_complete_RAW_payload']['path']);assert payload['checked_commit']==head
for name,x in payload['complete_named_payload'].items():
 p=o/name;assert x==(load(p) if name.endswith('.json') else p.read_text(encoding='utf8')),name
union=load(run['complete_input_manifest']['path']);assert len(union['entries'])==union['input_count']==469 and sha(can(union['entries']))==union['entries_logical_sha256']
for z in union['entries']:check(z)
core=load(o/'inputs.manifest.json');assert len(core['entries'])==core['input_count']==59 and core['snapshot_count']==8
native=load(o/'native-authorities.integrity.json');assert len(native['bindings'])==native['native_file_count']==382
tree={}
for record in subprocess.check_output(['git','ls-tree','-rz','--full-tree',head]).split(b'\0'):
 if record:
  meta,name=record.split(b'\t',1);tree[name.decode()]=meta.split()[2].decode()
bindings=[z for z in core['entries']+native['bindings'] if 'git_blob_oid' in z]
proc=subprocess.run(['git','cat-file','--batch'],input=('\n'.join(z['git_blob_oid'] for z in bindings)+'\n').encode(),capture_output=True,check=True)
buf=proc.stdout;offset=0;qualified=0
for z in bindings:
 end=buf.index(b'\n',offset);oid,kind,size=buf[offset:end].split();n=int(size);b=buf[end+1:end+1+n];assert buf[end+1+n:end+2+n]==b'\n';offset=end+2+n
 assert oid.decode()==z['git_blob_oid']==tree[z['path']] and kind==b'blob' and z['git_commit']==head,z['path']
 assert n==z['Git_RAW_bytes'] and sha(b)==z['Git_RAW_sha256'] and sha(b.replace(b'\r\n',b'\n'))==z['Git_LF_sha256'],z['path']
 current=check(z)
 if z['Git_RAW_equals_current']:assert current==b
 else:assert current.replace(b'\r\n',b'\n')==b.replace(b'\r\n',b'\n');qualified+=1
assert offset==len(buf)
for z in run['gate_receipts']:
 check(z);gate=load(z['path']);assert gate['exit_code']==0 and gate['terminal_closed']
transition=load(run['transition_receipt']['path']);completion=load(run['transition_completion_receipt']['path'])
assert transition['actual_foreground_PID']==17972 and transition['exit_code']==1 and transition['terminal_closed']
assert completion['actual_foreground_PID']==47856 and completion['exit_code']==0 and completion['terminal_closed']
v=load(r/'verified.json');assert v['status']=='VERIFIED' and v['verified_commit']==head and v['verifier_id']==run['actor'] and v['owner_id']!=v['verifier_id']
assert v['readback_no_second_transition'] and v['transition_terminal_EXIT1_after_successful_append_retained']
assert v['source_audit']['semantic_slots']==7 and v['source_audit']['informational_deltas']==16 and v['source_audit']['blocking_deltas']==v['source_audit']['mathematical_repairs']==0 and v['fake_closure_scan']['hits']==0
before=load(o/'ledger.before.compact.json');after=load(o/'ledger.after.compact.json');ledger=Path('runs/substantive_advances.jsonl').read_bytes();n=before['ledger_RAW_bytes']
assert len(ledger)==after['after_RAW_bytes'] and sha(ledger)==after['after_RAW_sha256'] and sha(ledger[:n])==before['ledger_RAW_sha256']
append=ledger[n:];assert len(append.splitlines())==1 and append==check(v['ledger_append'])
event=json.loads(append);assert event['advance_id']==v['advance_id'] and event['to_state']=='VERIFIED' and event['from_state']=='PROVED_LOCAL' and event['worker_id']==v['verifier_id']
assert adv.current_advances()[v['advance_id']]['state']=='VERIFIED'
p=r/'root.exact-verification71.adoption.json';assert not p.exists()
p.write_text(json.dumps(dict(status='ACCEPTED_NONOWNER_EXACT_SCI71_VERIFICATION',actual_root_PID=os.getpid(),native_verified=True,verified_commit=head,native_files=116,core_inputs=59,finite_input_union=469,native_reused_Git_bindings=382,Git_CRLF_only_qualified_references=qualified,native_whole_logical_run_sha256=h,native_lease_RAW_sha256=sha((o/'lease.final.json').read_bytes()),root_fresh_readonly_validator=readonly,root_readonly_terminal_EXIT=q.returncode,unique_VERIFIED_append_SHA256=sha(append),append_call_PID17972_EXIT1_retained=True,completion_readback_PID47856_EXIT0=True,no_second_transition=True,aggregate=False,reader=False,remoteCI=False,main_live=False,PURIFIED=False,Goal_complete=False),ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print('PASS71 exact nonowner VERIFIED CLOSED116/59core/469finite with uniqueappend and preserved17972EXIT1; root readonly',readonly['actual_foreground_PID'],'EXIT0. Aggregate/reader pending.')
