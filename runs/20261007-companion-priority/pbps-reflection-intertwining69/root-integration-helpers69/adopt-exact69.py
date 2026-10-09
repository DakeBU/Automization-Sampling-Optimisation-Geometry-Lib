from pathlib import Path
import hashlib,json,os,re,subprocess
root=Path.cwd();r=root/'runs/20261007-companion-priority/pbps-reflection-intertwining69';o=r/'exact-science-verification69'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest();can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def check(z):
 b=Path(z['path']).read_bytes();lf=b.replace(b'\r\n',b'\n');assert len(b)==z['raw_bytes'] and sha(b)==z['raw_sha256'];assert len(lf)==z['lf_bytes'] and sha(lf)==z['lf_sha256'];return b
lease=load(o/'lease.final.json');assert sha((o/'lease.final.json').read_bytes())=='d5e37f5b4c88841f65b3b55eec13091df90f31425559705866e7d8faba618938'
assert lease['status']=='CLOSED_LAST' and lease['last_owned_write']=='lease.final.json' and lease['no_more_owned_writes'] and lease['VERIFIED']
rows=lease['all_owned_outputs_except_only_self'];actual={p.resolve() for p in o.rglob('*') if p.is_file()};assert actual=={Path(z['path']).resolve() for z in rows}|{(o/'lease.final.json').resolve()} and len(actual)==159
for z in rows:check(z);assert Path(z['path']).stat().st_mtime_ns<=(o/'lease.final.json').stat().st_mtime_ns
run=load(o/'run.json');h=sha(can({k:v for k,v in run.items() if k!='run_sha256'}));assert h==run['run_sha256']==lease['whole_logical_run_sha256']=='94460a9f1cd9a58d6f437e56a62f6ed578aa52ff299468d54a4be4ef4e43676d'
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();assert head==run['verified_commit']=='2d286c283a6fb5dfc13180204bb0da54531a5c67'
assert run['status']=='VERIFIED_EXACT_SCI69_BY_NONOWNER' and run['actor']=='/root/exact_science63' and run['VERIFIED'] and run['ledger_one_append']
assert run['fakeclosures']==run['private_mathematical_providers']==0 and run['all_kerP_not_rangeV'] and run['no_sharp_energy68_dependency'] and run['rank0_alphaeta1_retained']
assert run['source_slots']==7 and run['retained_native_informational_deltas']==12 and run['literal_BODY_steps']==6
assert run['native_closed_file_counts']=={'blind':17,'math':112,'source':211}
assert run['immutable_native_whitespace_findings']==856 and run['authored_complement_PASS'] and not run['full_staged_whitespace_PASS']
fresh=run['fresh_Lean'];assert fresh['actual_foreground_PID']==27564 and fresh['exit_code']==0 and fresh['terminal_closed']
for k in ['input_manifest','named_complete_RAW_review','Git_blob_manifest','native340_Git_manifest','native_verdict','shared_verified_output','transition_receipt']:check(run[k])
assert run['named_complete_RAW_review']['raw_sha256']=='d25e23b332743df387f707c4801b222b34600eb3daa9d256e93f4d48bedd7d78'
m=load(o/'inputs.manifest.json');assert len(m['inputs'])==m['input_count']==60
snapshots=references=external=qualified=0
for z in m['inputs']:
 b=check(z['original'])
 if z.get('RAW_snapshot'):
  assert check(z['RAW_snapshot'])==b and check(z['LF_snapshot'])==b.replace(b'\r\n',b'\n');snapshots+=1
 if 'Git' in z:
  g=z['Git'];assert g['commit']==head
  blob=subprocess.check_output(['git','cat-file','blob',g['Git_blob_oid']]);assert len(blob)==g['Git_RAW_bytes'] and sha(blob)==g['Git_RAW_sha256'] and sha(blob.replace(b'\r\n',b'\n'))==g['Git_LF_sha256']
  if g['qualification']=='EXACT_RAW_EQUAL':assert blob==b
  else:assert g['qualification']=='ONLY_CRLF_CHECKOUT_DIFFERENCE_EXPLICIT; no RAW equality claim' and blob.replace(b'\r\n',b'\n')==b.replace(b'\r\n',b'\n');qualified+=1
  references+=1
 else:assert z['authority'].startswith('EXTERNAL_POSTCOMMIT_EXECUTION_RECEIPT');external+=1
assert snapshots==38 and references==59 and external==1 and qualified==10
v=load(r/'verified.json');assert v['status']=='VERIFIED' and v['verifier_id']==run['actor'] and v['owner_id']!=v['verifier_id'] and v['verified_commit']==head and v['actual_transition_PID']==46008
b=(root/'runs/substantive_advances.jsonl').read_bytes();before=v['ledger_before'];after=v['ledger_after'];assert len(b)==after['raw_bytes'] and sha(b)==after['raw_sha256'] and sha(b[:before['raw_bytes']])==before['raw_sha256']
append=b[before['raw_bytes']:];assert len(append)==3494 and sha(append)=='f18e0cbfa75c264e8e3f984638bd7ca44b5ae90c771410bf967b7c6164b3b90e'
event=json.loads(append);assert event['advance_id']==v['advance_id'] and event.get('state',event.get('to_state'))=='VERIFIED'
dest=r/'root.exact-verification69.adoption.json';assert not dest.exists()
payload=dict(status='ACCEPTED_NONOWNER_EXACT_SCI69_VERIFICATION',actual_root_PID=os.getpid(),native_verified=True,verified_commit=head,native_files=159,current_exact_inputs=60,Git_RAW_equal_references=49,Git_CRLF_only_qualified_references=10,external_postcommit_receipts=1,native_whole_logical_run_sha256=h,native_named_complete_RAW_sha256=run['named_complete_RAW_review']['raw_sha256'],native_lease_RAW_sha256=sha((o/'lease.final.json').read_bytes()),unique_VERIFIED_append_SHA256=sha(append),source_current_rows_at_SCI69=59,source_finite_historical_rows_at_SCI69=3,source_overlay_and_audit_cell_maps_preserved=True,truth_boundary_temporal_qualification='The native truth_boundary quotes its PROVED_LOCAL historical pending phrase verbatim. Exact status/commit/nonowner append now certify SCI69 VERIFIED; aggregate and reader remain pending. Native bytes unchanged.',aggregate=False,reader=False,remoteCI=False,main_live=False,PURIFIED=False,Goal_complete=False)
dest.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('PASS69 exact SCI nonowner VERIFIED/CLOSED159 adopted;60 inputs and exact append;10 explicitly CRLF-qualified inherited Git refs; aggregate/reader pending.')
