from pathlib import Path
import hashlib,json,os
root=Path.cwd();r=root/'runs/20261007-companion-priority/pbps-macro-root63';d=r/'independent-math63'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
seen=set()
def walk(x):
 if isinstance(x,dict):
  if {'path','raw_sha256'}<=x.keys():
   p=Path(x['path']);p=p if p.is_absolute() else root/p;b=p.read_bytes();k=(str(p.resolve()),x['raw_sha256'],x.get('lf_sha256'))
   if k not in seen:
    assert sha(b)==x['raw_sha256'],p
    if 'lf_sha256' in x:assert sha(b.replace(b'\r\n',b'\n'))==x['lf_sha256'],p
    for n in ['bytes','raw_bytes','raw_byte_count']:
     if n in x:assert len(b)==x[n],p
    if 'lf_bytes' in x:assert len(b.replace(b'\r\n',b'\n'))==x['lf_bytes'],p
    seen.add(k)
  for v in x.values():walk(v)
 elif isinstance(x,list):
  for v in x:walk(v)
run,lease,receipt,verdict=[load(d/n) for n in ['run.json','lease.json','native.receipt.json','verdict.json']]
assert lease['status']=='CLOSED' and lease['closed_last'] and lease['actual_foreground_readback_exit_codes']==[0,0]
assert sha(can({k:v for k,v in run.items() if k!='run_sha256'}))==run['run_sha256']==lease['run_sha256']=='f8ea8bdcb3455d251047f5a24c608a700b25bdfc9190ac82148a8de92c594be6'
assert sha((d/'named-mathematics.payload.json').read_bytes())==run['named_mathematics_payload_sha256']==lease['named_mathematics_payload_sha256']=='1eca96b379d0da483409e761e7c4a86b71524ed1585db566d45c7a66b8e82d64'
assert verdict['verdict']=='accepted-scoped-whole-math63' and not verdict['repairs'] and not verdict['blocking_issues']
assert verdict['original30_and_all58_unchanged'] and verdict['headers_literal_match'] and verdict['all_positive_alternatives_without_energy_premise'] and verdict['alternative_quantifier_outside_every_f']
assert verdict['additional_public_binders']==verdict['EXCESS']==0
issues=verdict['publication_binding_issues'];assert len(issues)==1 and issues[0]['step']==3 and issues[0]['blocking_for_exact_publication_code_seal'] and not issues[0]['blocking_for_mathematics']
assert run['compiler']['terminal_closed'] and run['compiler']['exit_code']==0 and run['compiler']['actual_foreground_pid']==3376
assert run['compiler_runs']==1 and run['nonforced'] and run['decoder_not_read'] and not lease['decoder_read_before_decision']
for p in d.glob('*.json'):walk(load(p))
payload=load(d/'named-mathematics.payload.json');assert payload['complete_decision']==run['complete_decision'] and payload['complete_mathematical_proof_review']==run['complete_mathematical_review']
out=r/'root.math63.adoption.json';assert not out.exists()
out.write_text(json.dumps(dict(status='INDEPENDENT_PRECOMMIT_SCOPED_MATHEMATICS63_ACCEPTED_WITH_EXACT_EXCERPT_BLOCKER',actual_adopter_pid=os.getpid(),native_reviewer=run['reviewer'],native_run_sha256=run['run_sha256'],native_named_RAW_payload_sha256=run['named_mathematics_payload_sha256'],qualified_current_readbacks=len(seen),compiler_actual_pid=3376,compiler_exit_code=0,checked_base_commit=run['checked_science_base'],remaining_boundary=verdict['remaining_boundary'],publication_binding_issues=issues,source_review_separate=True,publication_excerpt_seal=False,new_VERIFIED_transition=False,full_paper=False),ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('PASS independent CLOSED math63;',len(seen),'qualified current raw/LF pins; step3 presentation blocker retained, no source/VERIFIED claim.')
