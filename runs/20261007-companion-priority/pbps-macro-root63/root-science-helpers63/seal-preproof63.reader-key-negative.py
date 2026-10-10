from pathlib import Path
import hashlib,json,datetime
r=Path('runs/20261007-companion-priority/pbps-macro-root-preproof63');n=r/'independent-preproof63'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest();can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
run=load(n/'run.json');lease=load(n/'lease.json');review=load(n/'statement-binder.review.json')
assert lease['status']=='CLOSED' and lease['closed_last'] and lease['actual_foreground_readback_exit_codes']==[0,0]
assert sha(can({k:v for k,v in run.items() if k!='run_sha256'}))==run['run_sha256']==lease['run_sha256']=='a1d645bfe4e2903bc2b56225e4bb17e434e7d459dc863a5d73347f2403248ad4'
assert sha((n/'named-preproof.payload.json').read_bytes())==run['named_preproof_payload_sha256']==lease['named_preproof_payload_sha256']=='ac5c215d22b782b1c5e9a125e1f91d4fd918c67203940f46134693eaa6696fd4'
assert review['verdict']=='accepted-source-statement-conditional-on-verified62-parent' and review['independent_from_formalizer'] and review['source_first'] and review['source_graph_sealed_before_candidate']
assert review['excess_count']==0 and not review['repairs'] and not review['blocking_statement_issues']
seen=set();history=[]
def key(x):return(str(Path(x['path']).resolve()).lower(),x['raw_sha256'],x['lf_sha256'])
maps={key(q['historical_qualified_original']):q['exact_historical_snapshot'] for q in run['complete_negative_mapping']['qualified_input_maps']}
def walk(x):
 if isinstance(x,dict):
  if {'path','raw_sha256','lf_sha256'}<=x.keys():
   key=(str(Path(x['path']).resolve()),x['raw_sha256'],x['lf_sha256'])
   if key not in seen:
    b=Path(x['path']).read_bytes()
    if sha(b)!=x['raw_sha256']:
     assert key(x) in maps,('UNMAPPED_EXACT_INPUT',x);p=Path(maps[key(x)]['path']);b=p.read_bytes();history.append(dict(original=x,exact_historical_snapshot=maps[key(x)]))
    z=b.replace(b'\r\n',b'\n');assert sha(b)==x['raw_sha256'] and sha(z)==x['lf_sha256'],x['path']
    for k,v in [('bytes',len(b)),('raw_bytes',len(b)),('lf_bytes',len(z))]:
     if k in x:assert x[k]==v
    seen.add(key)
  for v in x.values():walk(v)
 elif isinstance(x,list):
  for v in x:walk(v)
for p in n.rglob('*.json'):walk(load(p))
parent=Path('runs/20261007-companion-priority/pbps-real-root-unique62/root.exact-verification62.adoption.json');vp=load(parent)
assert vp['native_verified'] and vp['verified_commit']=='9d7f7b640c7cb18fea133ccbd300de129af40b83'
assert load(Path('runs/20261007-companion-priority/pbps-real-root-unique62/root.scout63.adoption.json'))['no63proof_search']
assert load(r/'root.named-types63.adoption.json')['status']=='BOTH_FULL_NAMED_THEOREM_TYPES_ELABORATED_NO_PROOF'
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),bytes=len(b),lf_bytes=len(b.replace(b'\r\n',b'\n')),raw_sha256=sha(b),lf_sha256=sha(b.replace(b'\r\n',b'\n')))
out=dict(status='STATEMENT63_SEALED_NOT_PROVED_NOT_CLAIMED',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),headers=review['current_exact_headers'],native_run=pin(n/'run.json'),native_lease=pin(n/'lease.json'),named_payload=pin(n/'named-preproof.payload.json'),review=pin(n/'statement-binder.review.json'),whole_run_sha256=run['run_sha256'],named_preproof_RAW_payload_sha256=run['named_preproof_payload_sha256'],qualified_pin_readbacks=len(seen),finite_negative_history_maps=list(maps.values()),effective_negative_history_resolutions=history,late_parent62_exact_verified_adoption=pin(parent),parent62_verified_commit=vp['verified_commit'],historical_pending_parent_flags_retained=True,source_graph=pin(n/'source.graph.before-candidate.json'),source_coverage=pin(n/'source.coverage.before-candidate.json'),proof_search_started=False,scope=review['remaining_boundary'])
p=r/'root.statement-seal63.json';assert not p.exists();p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n');print('Exact63 statement sealed after independently PRIMARY-FIRST topology/coverage/binders and full namedTYPE review plus CLOSED VERIFIED62 parent;',len(seen),'qualified pins. No claim/proof.')
