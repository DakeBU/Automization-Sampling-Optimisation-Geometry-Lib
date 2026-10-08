from pathlib import Path
import hashlib,json,subprocess,os
root=Path.cwd();r=root/'runs/20261007-companion-priority/pbps-real-root-unique62';d=r/'exact-science-verification'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest();can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def path(s):
 p=Path(str(s).replace('\\','/'));return p if p.is_absolute() else root/p
seen=set()
def check(q,actual=None):
 p=path(actual or q['path']);b=p.read_bytes();assert sha(b)==q['raw_sha256'],p
 if 'lf_sha256' in q:assert sha(b.replace(b'\r\n',b'\n'))==q['lf_sha256'],p
 for n in ['bytes','raw_bytes']:
  if n in q:assert len(b)==q[n],p
 if 'lf_bytes' in q:assert len(b.replace(b'\r\n',b'\n'))==q['lf_bytes'],p
 seen.add((str(path(q['path']).resolve()).lower(),q['raw_sha256'],q.get('lf_sha256')))
def walk(x):
 if isinstance(x,dict):
  if {'path','raw_sha256'}<=x.keys():check(x)
  for v in x.values():walk(v)
 elif isinstance(x,list):
  for v in x:walk(v)
run,lease,receipt,inputs,outputs,transition=[load(d/n) for n in ['run.json','lease.json','receipt.json','strict-inputs.json','outputs.manifest.json','transition.json']]
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();assert head==run['checked_commit']==lease['checked_commit']=='9d7f7b640c7cb18fea133ccbd300de129af40b83'
assert lease['status']=='CLOSED' and lease['closed_last'] and lease['actual_terminal_readback']['exit_code']==0 and lease['actual_terminal_readback']['terminal_closed']
assert lease['compiler']['exit_code']==0 and lease['compiler']['terminal_closed'] and lease['compiler']['actual_PID']==50432
assert sha((d/'lease.json').read_bytes())=='db65ca8459517d594b260133d955a1800b7ba623c43fc5a061ced2f8068a87f3'
assert sha(can({k:v for k,v in run.items() if k!='run_sha256'}))==run['run_sha256']==lease['run_sha256']=='b44df82f5dfddd1780703afbf2f8456b1e64c092f8f8110c4337014f73432a29'
assert sha((d/'named-exact-verification.payload.json').read_bytes())==run['named_payload_raw_sha256']==lease['named_payload_raw_sha256']=='73a35952944bc5f5565ab131d0909389fbb85642e9733c5180c3b043a1b7ea0f'
assert receipt['verdict']=='ACCEPT_SCOPED_EXACT_SCIENCE_VERIFIED' and not receipt['mathematical_blockers'] and not receipt['source_blockers']
history=[]
assert len(inputs['rows'])==inputs['unique_pin_count']==1162
for row in inputs['rows']:
 q=row['expected'];a=path(row['resolved_path']);original=path(q['path'])
 if a.resolve()!=original.resolve():
  assert row['exact_ledger_before_map'] and original==root/'runs/substantive_advances.jsonl' and a.is_relative_to(d),row
  history.append(row)
 else:assert not row['exact_ledger_before_map'],row
 check(q,a)
assert len(history)==1 and len(outputs['artifacts'])==outputs['count']==65
for x in [run,lease,receipt,outputs]:walk(x)
records=[json.loads(s) for s in (root/'runs/substantive_advances.jsonl').read_text(encoding='utf-8').splitlines() if s.strip()]
accepted=[x for x in records if x.get('advance_id')=='ASTIS-SA-20261009-PBPSPositiveRealRootUniqueness' and x.get('to_state')=='VERIFIED']
assert len(accepted)==1 and accepted[0]['worker_id']==run['verifier']=='independent_whole_math52_exact62' and accepted[0]['evidence']['verified_commit']==head
out=r/'root.exact-verification62.adoption.json';assert not out.exists()
out.write_text(json.dumps(dict(status='INDEPENDENT_EXACT_SCIENCE62_ACCEPTED',actual_adopter_pid=os.getpid(),native_verified=True,verified_commit=head,verifier=run['verifier'],native_run_sha256=run['run_sha256'],native_named_RAW_payload_sha256=run['named_payload_raw_sha256'],qualified_pin_readbacks=len(seen),exact_ledger_history_resolution=history,administrative_audit_stages='Four exact snapshots are separate provenance; native source manifest excludes canonical audits; no invented fallback.',independent_ledger_transition=accepted[0],canonical_mutations_by_root=False,full_paper=False,integration_pending=True),ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
(r/'verified.json').write_bytes((d/'receipt.json').read_bytes());print('Adopted independently CLOSED exact-science62 VERIFIED;',len(seen),'strict qualified readbacks; root made no VERIFIED transition.')
