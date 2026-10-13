from pathlib import Path
import hashlib,json,os
pre=Path('runs/20261007-companion-priority/pbps-bounce-rate-preproof74');load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def check(z):
 p=Path(z['path']);b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');assert len(b)==z['RAW_bytes'] and sha(b)==z['RAW_sha256'] and sha(lf)==z['LF_sha256'],p
 if 'LF_bytes' in z:assert len(lf)==z['LF_bytes']
 return b
def pins(x):
 if isinstance(x,dict):
  if {'path','RAW_bytes','RAW_sha256','LF_sha256'}<=x.keys():check(x)
  for v in x.values():pins(v)
 elif isinstance(x,list):
  for v in x:pins(v)
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),LF_sha256=sha(b.replace(b'\r\n',b'\n')))
specs=[dict(folder='independent-header-math74',lease='d6b16336152c7e05551d299ae2dce01bfb48e80c11a6d6de8378d99e5723e495',count=12,manifest='native.manifest.json',rows='owned_files',run='run.json',whole='e595949040afb2baab29c8f24d000bebf490deffba66d209c08278c08c94f3cb'),dict(folder='independent-header-source74',lease='8e26413602672e647bd5b6692d6b9519ca003807ad1c44c4bd3a276a7c6abd67',count=38,manifest='manifest.final.json',rows='members',run='source-header.0.run.json',whole='9c082d518f023710eece97087f8c549e8d559b18d72821894cec2be85be2e5ce')]
results=[]
for s in specs:
 o=pre/s['folder'];lp=o/'lease.final.json';assert sha(lp.read_bytes())==s['lease'];l=load(lp);assert l.get('status',l.get('state')) in ['CLOSED_LAST','CLOSED']
 m=load(o/s['manifest']);rows=m[s['rows']];assert len(rows)==s['count']-2
 assert {p.resolve() for p in o.rglob('*') if p.is_file()}=={Path(z['path']).resolve() for z in rows}|{lp.resolve(),(o/s['manifest']).resolve()}
 for z in rows:
  check(z);assert Path(z['path']).stat().st_mtime_ns<=lp.stat().st_mtime_ns
 pins(l);run=load(o/s['run']);h=sha(can({k:v for k,v in run.items() if k!='run_sha256'}));assert h==run['run_sha256']==s['whole'];pins(run)
 payload=load(o/'complete-named-review-decision-input-payload.json')
 if s['folder']=='independent-header-math74':
  d=load(o/'decision.json');assert payload['complete_named_decision_and_input_payload']==d
  assert d['verdict']=='ACCEPT_HEADER_MATHEMATICS_ONLY' and d['minimal_mathematical_repair'] is None and not d['missing_conditions'] and not d['extra_public_regularities'] and not d['false_premises']
  assert len(run['inputs'])==25 and d['complete_literal_reviewed'] and d['same_original_six_callers_byte_equal'] and d['no_actual73_formal_parent']
  assert payload['full_exact_candidate_inputs']['candidate_complete_exact_RAW_UTF8']==(pre/'header74.proposed.lean').read_text(encoding='utf8')
 else:
  d=load(o/'source-header.0.decision.json');assert payload==run['complete_named_review_decision_input_payload'] and payload['decision']==d
  assert d['status']=='ACCEPT_PROSPECTIVE_HEADER_SOURCE_ONLY' and d['verdict']=='equivalent-after-elaboration'
  assert not d['mathematical_or_source_blocking_deltas'] and not d['required_statement_repairs'] and not d['canonical_changes_made'] and not d['old_closed_writes']
  c=d['source_contract_counts'];assert c['source_items']==95 and c['source_nodes']==28 and c['source_edges']==52 and c['source_obligations']==26 and c['internal_future_bridges']==13 and c['excess_public_premises']==0
 results.append(dict(kind=s['folder'],native_owned_files=s['count'],native_lease=pin(lp),native_whole_logical_run_sha256=h,native_complete_named=pin(o/'complete-named-review-decision-input-payload.json')))
dest=pre/'root.header-reviews74.adoption.json';assert not dest.exists()
dest.write_text(json.dumps(dict(status='ACCEPTED_INDEPENDENT_HEADER_MATH_AND_SOURCE_ONLY',actual_root_PID=os.getpid(),header=pin(pre/'header74.proposed.lean'),reviews=results,no_header_repairs=True,no_theorem_proof=True,VERIFIED=False,Goal_complete=False),ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print('PASS74 independent HEADER-only CLOSED12math/38source accepted; six binders/tenclauses/95items; no proof or VERIFIED credit.')
