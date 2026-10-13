from pathlib import Path
import hashlib,json,os
root=Path.cwd();r=root/'runs/20261007-companion-priority/pbps-real-root-unique62';d=r/'independent-math62'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest();can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def path(s):
 p=Path(s);return p if p.is_absolute() else root/p
seen=set()
def walk(x):
 if isinstance(x,dict):
  if {'path','raw_sha256'}<=x.keys():
   p=path(x['path']);b=p.read_bytes();k=(str(p.resolve()),x['raw_sha256'],x.get('lf_sha256'))
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
assert sha(can({k:v for k,v in run.items() if k!='run_sha256'}))==run['run_sha256']==lease['run_sha256']=='a10112e1d8e3aef039697ed6e9a431fb8d59b17e59ead228e82c8178cf2c6683'
assert sha((d/'named-mathematics.payload.json').read_bytes())==run['named_mathematics_payload_sha256']==lease['named_mathematics_payload_sha256']=='9e22abf9c25a379dcd7c04bb3eddb55c70f3300347dbd39e2f33e15445bfc475'
assert verdict['verdict']=='accepted-scoped-whole-math62' and not verdict['repairs'] and not verdict['blocking_issues']
assert verdict['original27_unchanged'] and verdict['exact_headers'] and verdict['seven_formula_steps_checked'] and verdict['genuine_actual_input_all_positive_alternative_Test']
assert run['compiler']['terminal_closed'] and run['compiler']['exit_code']==0 and run['compiler']['actual_foreground_pid']==3700
assert run['compiler_runs']==1 and run['nonforced'] and run['decoder_not_read'] and lease['decoder_read_before_decision']==False
for p in d.glob('*.json'):walk(load(p))
out=r/'root.math62.adoption.json';assert not out.exists()
out.write_text(json.dumps(dict(status='INDEPENDENT_PRECOMMIT_SCOPED_MATHEMATICS62_ACCEPTED',actual_adopter_pid=os.getpid(),native_reviewer=run['reviewer'],native_run_sha256=run['run_sha256'],native_named_RAW_payload_sha256=run['named_mathematics_payload_sha256'],qualified_current_readbacks=len(seen),compiler_actual_pid=3700,compiler_exit_code=0,checked_base_commit=run['checked_science_base'],remaining_boundary=verdict['remaining_boundary'],source_review_separate=True,new_VERIFIED_transition=False,full_paper=False),ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('Accepted independent CLOSED math62;',len(seen),'exact current pin readbacks; no source verdict or VERIFIED transition.')
