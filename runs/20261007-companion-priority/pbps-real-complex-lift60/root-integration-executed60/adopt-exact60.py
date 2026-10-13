from pathlib import Path
import json,hashlib,subprocess
r=Path('runs/20261007-companion-priority/pbps-real-complex-lift60');d=r/'exact-science-verification';load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest();can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def path(p):return Path(str(p).replace('\\','/')).resolve()
def pin(p):
 p=path(p);b=p.read_bytes();z=b.replace(b'\r\n',b'\n');return dict(path=p.as_posix(),bytes=len(b),lf_bytes=len(z),raw_sha256=sha(b),lf_sha256=sha(z))
def key(q):return (path(q['path']).as_posix().lower(),q['raw_sha256'],q['lf_sha256'])
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();assert head=='0a77416f5ec38702c46ec1358966b9dd4846c8d3';run,lease,receipt=[load(d/n) for n in ['run.json','lease.json','receipt.json']];assert lease['status']=='CLOSEDLAST' and lease['checked_commit']==run['checked_commit']==receipt['checked_commit']==head
assert sha(can({k:v for k,v in run.items() if k!='run_sha256'}))==run['run_sha256']==lease['run_sha256']=='3cc320a6f0c7cc63659ecf5689bb7e1ef3093431a3b937724ca19fe6bf5413ed';assert sha(can(run['named_exact_verification_payload']))==run['named_exact_verification_payload_sha256']==lease['named_exact_verification_payload_sha256']=='f266652619988b650a289667fe493e2a9b72406b7532a899b132eac30eb05212';assert sha(can({k:v for k,v in lease.items() if k!='lease_sha256'}))==lease['lease_sha256'];assert receipt['verdict']=='ACCEPT_EXACT_SCIENCE_SCOPED_INDEPENDENT_VERIFICATION' and not receipt['blockers'];assert all(lease[k]['exit_code']==0 for k in ['compiler','check_reader','promotion','readback'])
maps={}
for x in load(d/'historical-mappings.json')['mappings']:maps[key(x['original'])]=x['snapshot']
for x in load(d/'before-admin-mappings.json')['mappings']:maps[key(x['original'])]=x['exact_snapshot']
seen={};resolved=[]
def walk(x):
 if isinstance(x,dict):
  if {'path','raw_sha256','lf_sha256'}<=x.keys():
   k=key(x)
   if k not in seen:
    a=pin(x['path'])
    if any(a[z]!=x[z] for z in ['raw_sha256','lf_sha256']):
     assert k in maps,('UNMAPPED',x);a=pin(maps[k]['path']);resolved.append(dict(original=x,exact_raw_snapshot=a))
    assert all(a[z]==x[z] for z in ['raw_sha256','lf_sha256']);assert all(a[z]==x[z] for z in ['bytes','lf_bytes'] if z in x);seen[k]=a
  for v in x.values():walk(v)
 elif isinstance(x,list):
  for v in x:walk(v)
for q in [run,lease,receipt,load(d/'input.manifest.json'),load(d/'outputs.final.json')]:walk(q)
transition=load(d/'transition.json')['record'];assert transition['advance_id']=='ASTIS-SA-20261008-PBPSPositiveDefectComplexLift' and transition['to_state']=='VERIFIED' and transition['worker_id']!='companion_root_20261005';assert transition in [json.loads(s) for s in Path('runs/substantive_advances.jsonl').read_text(encoding='utf-8').splitlines() if s.strip()]
for q in load(r/'math-freeze.json')['inputs']:walk(q)
out=dict(status='INDEPENDENT_EXACT_SCIENCE60_ACCEPTED',native_verified=True,verified_commit=head,verifier=run['actor'],native_run=pin(d/'run.json'),native_receipt=pin(d/'receipt.json'),native_lease=pin(d/'lease.json'),native_run_sha256=run['run_sha256'],native_named_payload_sha256=run['named_exact_verification_payload_sha256'],qualified_pin_readbacks=len(seen),exact_historical_resolutions=resolved,observer_split=load(r/'commit-observer-split.json'),independent_ledger_transition=transition,canonical_mutations_by_root=False,full_paper=False,integration_pending=True)
p=r/'root.exact-verification60.adoption.json';assert not p.exists();p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n');(r/'verified.json').write_bytes((d/'receipt.json').read_bytes());print('Independent exact-science60 accepted;',len(seen),'qualified pins;',len(resolved),'exact history resolutions; no root verification transition.')
