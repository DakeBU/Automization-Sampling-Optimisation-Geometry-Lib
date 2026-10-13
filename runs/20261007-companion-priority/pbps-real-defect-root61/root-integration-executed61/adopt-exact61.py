from pathlib import Path
import json,hashlib,subprocess
r=Path('runs/20261007-companion-priority/pbps-real-defect-root61');d=r/'exact-science-verification';load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest();can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def path(p):return Path(str(p).replace('\\','/')).resolve()
def pin(p):
 p=path(p);b=p.read_bytes();z=b.replace(b'\r\n',b'\n');return dict(path=p.as_posix(),raw_bytes=len(b),lf_bytes=len(z),raw_sha256=sha(b),lf_sha256=sha(z))
def key(q):return (path(q['path']).as_posix().lower(),q['raw_sha256'],q['lf_sha256'])
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();assert head=='bcd245d90b21b899acb9937fc54dffcea20e86ee'
run,lease,receipt,review,readback,promotion=[load(d/n) for n in ['run.json','lease.json','receipt.json','native.review.json','readback.json','promotion.json']]
assert lease['status']=='CLOSED_LAST' and lease['checked_commit']==run['checked_commit']==receipt['checked_commit']==head
assert sha(can({k:v for k,v in run.items() if k!='run_sha256'}))==run['run_sha256']==lease['run_sha256']=='3d72c46fa3f45714b4362a6dfc5a46582e1eb0c179c7d71ecfab0642315fb353'
assert sha(can(run['named_verification_payload']))==run['named_verification_payload_sha256']==lease['named_verification_payload_sha256']=='847eb5fb43407e2c212a004d873287fd6ac67137bfa5b2e82ed935a16cbed73d'
assert sha(can({k:v for k,v in lease.items() if k!='lease_sha256'}))==lease['lease_sha256']
assert receipt['verdict']=='ACCEPT_SCOPED_EXACT_SCIENCE_NO_BLOCKER' and lease['actual_readback']['exit_code']==lease['actual_compiler']['exit_code']==0
maps={key(x['original']):x['exact_raw_snapshot'] for x in review['finite_history_mappings']}
for x in readback['explicit_post_transition_before_mappings']:maps[key(x['original'])]=x['exact_before_snapshot']
seen={};resolved=[]
def walk(x):
 if isinstance(x,dict):
  if {'path','raw_sha256','lf_sha256'}<=x.keys():
   k=key(x)
   if k not in seen:
    q=pin(x['path'])
    if any(q[z]!=x[z] for z in ['raw_sha256','lf_sha256']):
     assert k in maps,('UNMAPPED',x);q=pin(maps[k]['path']);resolved.append(dict(original=x,exact_raw_snapshot=q))
    assert all(q[z]==x[z] for z in ['raw_sha256','lf_sha256'])
    for label,actual in [('bytes',q['raw_bytes']),('raw_bytes',q['raw_bytes']),('lf_bytes',q['lf_bytes'])]:
     if label in x:assert actual==x[label]
    seen[k]=q
  for v in x.values():walk(v)
 elif isinstance(x,list):
  for v in x:walk(v)
for q in [run,lease,receipt,review,readback,promotion,load(d/'inputs.before.json'),load(d/'outputs.final.json'),load(r/'math-freeze.json')]:walk(q)
t=promotion['appended_record'];assert t['advance_id']=='ASTIS-SA-20261009-PBPSPositiveRealDefectRoot' and t['to_state']=='VERIFIED' and t['worker_id']=='independent_whole_math52_exact61'
assert t in [json.loads(s) for s in Path('runs/substantive_advances.jsonl').read_text(encoding='utf-8').splitlines() if s.strip()]
out=dict(status='INDEPENDENT_EXACT_SCIENCE61_ACCEPTED',native_verified=True,verified_commit=head,verifier=run['actor'],native_run=pin(d/'run.json'),native_receipt=pin(d/'receipt.json'),native_lease=pin(d/'lease.json'),native_run_sha256=run['run_sha256'],native_named_payload_sha256=run['named_verification_payload_sha256'],qualified_pin_readbacks=len(seen),exact_historical_resolutions=resolved,active_science_observer_excluded=True,independent_ledger_transition=t,canonical_mutations_by_root=False,full_paper=False,integration_pending=True)
p=r/'root.exact-verification61.adoption.json';assert not p.exists();p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n');(r/'verified.json').write_bytes((d/'receipt.json').read_bytes())
print('Independent exact-science61 accepted;',len(seen),'qualified pins;',len(resolved),'exact history resolutions; root made no VERIFIED transition.')
