from pathlib import Path
import hashlib,json,datetime
r=Path('runs/20261007-companion-priority/pbps-real-root-unique-preproof62');n=r/'independent-preproof62'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest();can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
run=load(n/'run.json');lease=load(n/'lease.json');review=load(n/'statement-binder.review.json')
assert lease['status']=='CLOSED' and lease['closed_last'] and lease['actual_foreground_readback_exit_codes']==[0,0]
assert sha(can({k:v for k,v in run.items() if k!='run_sha256'}))==run['run_sha256']==lease['run_sha256']=='80613eceb5309878e9d1b39a292dbf81cd724902d6db8688672a7a71450ea58c'
assert sha((n/'named-preproof.payload.json').read_bytes())==run['named_preproof_payload_sha256']==lease['named_preproof_payload_sha256']=='ea2376297b4bf021ccc4621a6c796ab1935fa98a0e9899a2646a2052e2bdf8b3'
assert review['verdict']=='accepted-preproof-source-contract' and review['independent_of_formalizer_and_scout_creator']
assert review['generic']['zero_excess'] and review['actual']['zero_excess']
seen=set()
def walk(x):
 if isinstance(x,dict):
  if {'path','raw_sha256','lf_sha256'}<=x.keys():
   key=(str(Path(x['path']).resolve()),x['raw_sha256'],x['lf_sha256'])
   if key not in seen:
    b=Path(x['path']).read_bytes();z=b.replace(b'\r\n',b'\n');assert sha(b)==x['raw_sha256'] and sha(z)==x['lf_sha256'],x['path']
    for k,v in [('bytes',len(b)),('raw_bytes',len(b)),('lf_bytes',len(z))]:
     if k in x:assert x[k]==v
    seen.add(key)
  for v in x.values():walk(v)
 elif isinstance(x,list):
  for v in x:walk(v)
for p in n.rglob('*.json'):walk(load(p))
parent=Path('runs/20261007-companion-priority/pbps-real-defect-root61/root.exact-verification61.adoption.json');vp=load(parent)
assert vp['native_verified'] and vp['verified_commit']=='bcd245d90b21b899acb9937fc54dffcea20e86ee'
assert load(r/'root.scout62-and-type.adoption.json')['no62proof_search']
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),bytes=len(b),lf_bytes=len(b.replace(b'\r\n',b'\n')),raw_sha256=sha(b),lf_sha256=sha(b.replace(b'\r\n',b'\n')))
out=dict(status='STATEMENT62_SEALED_NOT_PROVED_NOT_CLAIMED',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),headers=review['exact_headers'],native_run=pin(n/'run.json'),native_lease=pin(n/'lease.json'),named_payload=pin(n/'named-preproof.payload.json'),review=pin(n/'statement-binder.review.json'),whole_run_sha256=run['run_sha256'],named_preproof_payload_sha256=run['named_preproof_payload_sha256'],qualified_pin_readbacks=len(seen),late_parent61_exact_verified_adoption=pin(parent),parent61_verified_commit=vp['verified_commit'],historical_pending_parent_flags_retained=True,source_graph=pin(n/'source-proof-graph.json'),source_coverage=pin(n/'source-coverage.json'),proof_search_started=False,scope=run['source_boundary'])
p=r/'root.statement-seal62.json';assert not p.exists();p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('Exact62 statement sealed after independent source review and separately bound VERIFIED61 parent;',len(seen),'qualified raw/LF pins. No claim/proof.')
