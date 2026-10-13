from pathlib import Path
import hashlib,json,subprocess
root=Path.cwd(); r=root/'runs/20261007-companion-priority/pbps-centered-defect59'; d=r/'exact-science-verification'; h=d/'pin-history-readback'
load=lambda p:json.loads(Path(p).read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def path(s):
 p=Path(str(s).replace('\\','/'));return p if p.is_absolute() else root/p
def pin(s):
 p=path(s);b=p.read_bytes();z=b.replace(b'\r\n',b'\n');return dict(path=p.as_posix(),raw_sha256=sha(b),lf_sha256=sha(z),bytes=len(b),lf_bytes=len(z))
def equal(a,b):
 return all(a[k]==b[k] for k in ['raw_sha256','lf_sha256']) and all(a[k]==b[k] for k in ['bytes','lf_bytes'] if k in b)
def key(x):return (path(x['path']).as_posix().lower(),x['raw_sha256'],x['lf_sha256'])
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();assert head=='2d6cd0167adc4fae1d8d166068a2eda51cd3c3ad'
run,lease,receipt=map(load,[d/'run.json',d/'lease.json',d/'receipt.json']);hr,hl=map(load,[h/'run.json',h/'lease.json'])
assert lease['status']==hl['status']=='CLOSEDLAST'
assert sha(can({k:v for k,v in run.items() if k!='run_sha256'}))==run['run_sha256']==lease['run_sha256']=='152bde97ad8ed85897e53f593273d950e96df1fc2813d2890a68622d4ad72dbf'
assert sha(can(run['named_exact_verification_payload']))==run['named_exact_verification_payload_sha256']==lease['named_exact_verification_payload_sha256']=='badd35e6dceebd339b39ebe6f4461acb3c830af8c7a3dda18dc173bfe92f6968'
assert sha(can({k:v for k,v in hr.items() if k!='run_sha256'}))==hr['run_sha256']==hl['run_sha256']=='5cd44df1e2e2aa06f80926826c69cf946d511f6f492df40ec526c3d900c1b8e4'
assert sha(can(hr['named_pin_history_payload']))==hr['named_pin_history_payload_sha256']==hl['named_pin_history_payload_sha256']=='11cd71bebab5f52795983328939ae7701dd536b5dc9f6b1f50461add03dab332'
for q in [lease,hl]:assert sha(can({k:v for k,v in q.items() if k!='lease_sha256'}))==q['lease_sha256']
assert pin(d/'receipt.json')['raw_sha256']=='057af37e7648c0b87dc20b41bd3409d32a2466b1ea829431428dbae686ba5562'
assert pin(d/'lease.json')['raw_sha256']=='a90039d9e849b0c2ab389a3261a31d32604ae6fcafc1bff53f4ffde33077d648'
assert pin(h/'lease.json')['raw_sha256']=='4b8555563182115b377751b86f3fc077549581eb9e7de169c53f8cf4973b9aec'
assert receipt['verdict']=='ACCEPT_SCOPED_NO_MATHEMATICAL_OR_SOURCE_BLOCKER' and receipt['checked_commit']==head
assert all(lease[k]==0 for k in ['actual_reader_exit_code','actual_promotion_exit_code','actual_lake_exit_code','actual_readback_exit_code'])
maps={}
payload=hr['named_pin_history_payload']
for x in payload['explicit_historical_resolutions']:
 maps[key(x['original'])]=x['resolved']
x=payload['explicit_promotion_transition_history'];maps[key(x['original'])]=x['exact_snapshot']
seen={};resolved=[]
def walk(x):
 if isinstance(x,dict):
  if {'path','raw_sha256','lf_sha256'}<=x.keys():
   k=key(x)
   if k not in seen:
    p=path(x['path']); a=pin(p) if p.exists() else None
    if a is None or not equal(a,x):
     assert k in maps,('UNMAPPED',x);a=pin(maps[k]['path']);assert equal(a,x),x;resolved.append(dict(original=x,exact_raw_snapshot=a))
    assert equal(a,x),x;seen[k]=a
  for v in x.values():walk(v)
 elif isinstance(x,list):
  for v in x:walk(v)
outputs=load(d/'outputs.final.json');inputs=load(d/'inputs.final.json');assert outputs['count']==len(outputs['artifacts'])==54 and inputs['count']==len(inputs['qualified_unique_input_identities'])==565
for q in [run,lease,receipt,hr,hl,inputs,outputs,load(d/'readback.json')]:walk(q)
for x in outputs['artifacts']:
 p=path(x['path'])
 if p.suffix=='.json':walk(load(p))
transition=load(d/'transition.json')['actual_transition'];assert transition['to_state']=='VERIFIED' and transition['advance_id']=='ASTIS-SA-20261008-PBPSCenteredDefectOperator';assert transition['worker_id']!='companion_root_20261005'
ledger=[json.loads(s) for s in (root/'runs/substantive_advances.jsonl').read_text(encoding='utf-8').splitlines() if s.strip()];assert transition in ledger
native=load(d/'verified.json');assert native['status']=='INDEPENDENT_EXACT_SCIENCE_VERIFIED' and native['checked_commit']==head
out=dict(status='INDEPENDENT_EXACT_SCIENCE59_ACCEPTED',native_verified=True,verified_commit=head,verifier=run['actor'],native_run=pin(d/'run.json'),native_receipt=pin(d/'receipt.json'),native_lease=pin(d/'lease.json'),native_run_sha256=run['run_sha256'],native_named_payload_sha256=run['named_exact_verification_payload_sha256'],historical_pin_supplement=pin(h/'run.json'),qualified_unique_pin_readbacks=len(seen),exact_historical_resolutions=resolved,independent_ledger_transition=transition,canonical_mutations_by_root=False,full_paper=False,integration_pending=True)
assert not (r/'root.exact-verification59.adoption.json').exists()
(r/'root.exact-verification59.adoption.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
(r/'verified.json').write_bytes((d/'verified.json').read_bytes())
print(json.dumps(dict(status=out['status'],qualified_unique_pin_readbacks=len(seen),historical_resolutions=len(resolved),verifier=run['actor'])))
