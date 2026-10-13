from pathlib import Path
import hashlib,json,os,subprocess
r=Path('runs/20261007-companion-priority/pbps-actual-projected-rotation70');o=r/'exact-science-verification70-label-supplement';load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest();can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def check(z):
 b=Path(z['path']).read_bytes();lf=b.replace(b'\r\n',b'\n');assert len(b)==z['raw_bytes'] and sha(b)==z['raw_sha256'];assert len(lf)==z['lf_bytes'] and sha(lf)==z['lf_sha256'];return b
lease=load(o/'lease.final.json');assert sha((o/'lease.final.json').read_bytes())=='1e18fed5d7144eecda6b45fdef21dba31f011c5ac277c2d663ce3dd75aec15e0'
assert lease['status']=='CLOSED_LAST' and lease['last_owned_write']=='lease.final.json' and lease['no_more_owned_writes'] and lease['VERIFIED']
rows=lease['all_owned_outputs_except_only_self'];assert {p.resolve() for p in o.rglob('*') if p.is_file()}=={Path(z['path']).resolve() for z in rows}|{(o/'lease.final.json').resolve()} and len(rows)+1==94
for z in rows:check(z)
run=load(o/'run.json');h=sha(can({k:v for k,v in run.items() if k!='run_sha256'}));assert h==run['run_sha256']==lease['whole_logical_run_sha256']=='4f824da6f0ff4f285ca54bb5d36e840157dc3413a6eb66d5226ac3a5c76727be'
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();assert head==run['verified_commit']=='c46af8a55e89419109f654c4553cf527993cbeed'
assert run['status']=='VERIFIED_EXACT_CORRECTED_SCI70_BY_NONOWNER' and run['actor']=='/root/exact_science63' and run['VERIFIED'] and run['ledger_one_append']
assert run['fakeclosures']==run['private_mathematical_providers']==0 and run['no68_energy_parent'] and run['source_slots']==7 and run['informational_deltas']==13 and run['literal_BODY_steps']==8
assert run['original_focused_Lake_EXIT']==run['prior_independent_fresh_Lean_EXIT']==0 and run['original_e44_not_VERIFIED']
for k in ['input_manifest','named_complete_RAW_review','Git_blob_manifest','native_verdict','shared_verified_output','transition_receipt']:check(run[k])
assert run['named_complete_RAW_review']['raw_sha256']=='7174165fd97f7d1826834bb2844e3f80c3b4bf844dcf0a4975cd47e4b9a0859a'
m=load(o/'inputs.manifest.json');assert len(m['inputs'])==m['input_count']==45
qualified=0
for z in m['inputs']:
 b=check(z['original'])
 if z.get('RAW_snapshot'):assert check(z['RAW_snapshot'])==b and check(z['LF_snapshot'])==b.replace(b'\r\n',b'\n')
 if 'Git' in z:
  g=z['Git'];blob=subprocess.check_output(['git','cat-file','blob',g['Git_blob_oid']]);assert len(blob)==g['Git_RAW_bytes'] and sha(blob)==g['Git_RAW_sha256']
  if g['qualification']=='EXACT_RAW_EQUAL':assert blob==b
  else:assert blob.replace(b'\r\n',b'\n')==b.replace(b'\r\n',b'\n');qualified+=1
v=load(r/'verified.json');assert v['status']=='VERIFIED' and v['verified_commit']==head and v['verifier_id']==run['actor'] and v['owner_id']!=v['verifier_id']
b=Path('runs/substantive_advances.jsonl').read_bytes();before=v['ledger_before'];after=v['ledger_after'];assert len(b)==after['raw_bytes'] and sha(b)==after['raw_sha256'] and sha(b[:before['raw_bytes']])==before['raw_sha256'];append=b[before['raw_bytes']:];event=json.loads(append);assert event['advance_id']==v['advance_id'] and event.get('state',event.get('to_state'))=='VERIFIED'
dest=r/'root.exact-verification70.adoption.json';assert not dest.exists()
dest.write_text(json.dumps(dict(status='ACCEPTED_NONOWNER_EXACT_CORRECTED_SCI70_VERIFICATION',actual_root_PID=os.getpid(),native_verified=True,verified_commit=head,original_math_commit=run['parent'],native_files=94,current_exact_inputs=45,Git_CRLF_only_qualified_references=qualified,native_whole_logical_run_sha256=h,native_lease_RAW_sha256=sha((o/'lease.final.json').read_bytes()),unique_VERIFIED_append_SHA256=sha(append),original_e44_not_VERIFIED=True,native_observer_failure_and_original_stderr_preserved=True,aggregate=False,reader=False,remoteCI=False,main_live=False,PURIFIED=False,Goal_complete=False),ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('PASS70 CLOSED94/45inputs and exact nonowner VERIFIED append adopted; aggregate/reader remain pending')
