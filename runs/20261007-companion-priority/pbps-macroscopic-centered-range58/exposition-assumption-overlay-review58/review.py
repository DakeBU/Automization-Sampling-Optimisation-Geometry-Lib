import os,sys,pathlib,json,hashlib,datetime,collections
sys.dont_write_bytecode=True;sys.stdout.reconfigure(encoding='utf8')
R=pathlib.Path('E:/Samplinglib');B=R/'runs/20261007-companion-priority/pbps-macroscopic-centered-range58';A=B/'exposition-assumption-overlay58';O=B/'exposition-assumption-overlay-review58';ACTOR='whole_math52_assumption_metadata58'
def path(p):
 p=pathlib.Path(str(p).replace('\\','/'));return p if p.is_absolute() else R/p
def load(p):return json.loads(path(p).read_text(encoding='utf8'))
def sha(b):return hashlib.sha256(b).hexdigest()
def logical(d):return sha(json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode('utf8'))
def dump(p,d):path(p).write_bytes((json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode('utf8'))
def pin(p):
 p=path(p);b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');return dict(path=p.relative_to(R).as_posix(),bytes=len(b),lf_bytes=len(lf),raw_sha256=sha(b),lf_sha256=sha(lf))
def same(e,a):return all(e[k]==a[k] for k in ['bytes','raw_sha256','lf_sha256']) and ('lf_bytes' not in e or e['lf_bytes']==a['lf_bytes'])
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def guard(e,a):
 if e=='open' and a and isinstance(a[0],(str,bytes,os.PathLike)):
  s=os.fsdecode(a[0]).replace('\\','/').lower()
  if ('/runs/' in s or '/.astis/' in s) and any(('59' in c or '60' in c) and any(k in c for k in ['pbps','preproof','sourcegraph','preread','future']) for c in s.split('/')):raise PermissionError('Assumption metadata58 excludes future59/60')
  if '/pbps-macroscopic-centered-range58/' in s and any(k in s for k in ['/source-review58/','/anonymous-decoder/']):raise PermissionError('No native source/decoder verdict read')
sys.addaudithook(guard);O.mkdir(exist_ok=True)
opened=dict(status='OPEN',actor=ACTOR,actual_foreground_Python_PID=os.getpid(),opened_utc=utc(),read='OPEN',write='OPEN',Python='OPEN',compiler='NOT_STARTED_CLOSED',scope='Independent exact one-pointer assumption alignment and exhaustive twelve-current-file dimension inventory only. Original CLOSED/native/canonical/Lean/source/proof files untouched; no verdict/state credit.')
dump(O/'lease.json',opened);inputs={}
def current(p):a=pin(p);inputs[a['path']]=a;return a
def strings(x,p=''):
 if isinstance(x,dict):
  for k,v in x.items():yield from strings(v,p+'/'+k.replace('~','~0').replace('/','~1'))
 elif isinstance(x,list):
  for i,v in enumerate(x):yield from strings(v,p+'/'+str(i))
 elif isinstance(x,str):yield p,x
def diff(x,y,p=''):
 if isinstance(x,dict) and isinstance(y,dict):
  z=[]
  for k in sorted(set(x)|set(y)):
   q=p+'/'+k.replace('~','~0').replace('/','~1');z+=([q] if k not in x or k not in y else diff(x[k],y[k],q))
  return z
 if isinstance(x,list) and isinstance(y,list) and len(x)==len(y):
  z=[]
  for i,(a,b) in enumerate(zip(x,y)):z+=diff(a,b,p+'/'+str(i))
  return z
 return [] if x==y else [p]
proposal=load(A/'proposal.json');h=logical({k:v for k,v in proposal.items() if k!='proposal_sha256'});assert h==proposal['proposal_sha256']=='e1c33fb3e425ff4453d1c1fc3158a1b5951a272780a930fc516cb72325027c4f';current(A/'proposal.json')
orig=current(proposal['original_snapshot']);assert same(proposal['original'],orig);newpin=current(proposal['proposed']);x=load(proposal['original_snapshot']);y=load(proposal['proposed']);delta=diff(x,y);assert delta==[proposal['exact_pointer']]==['/items/0/bindings/0/assumption_deltas/1/lean']
assert x['items'][0]['bindings'][0]['assumption_deltas'][1]['lean']==proposal['old_exact'] and y['items'][0]['bindings'][0]['assumption_deltas'][1]['lean']==proposal['new_exact']
assert proposal['new_exact']=='Actual AE pullback range and full centered image; the same actual conditional mean and reflection give the exact sharp contraction and squared defect lower bound for all centered macro inputs, including rank zero and alpha*eta=1. No finite-dimensionality is imposed on real L2.'
assert not proposal['theorem_signature_binder_proof_change'] and proposal['future_source_review_required'] and proposal['original_native_negative_immutable']
inventory=load(proposal['inventory']);current(proposal['inventory']);assert len(inventory['current_files'])==12 and len(inventory['all_infinite_L2_fields'])==41
rows=[];broad=[];old=[];objects={}
for f in inventory['current_files']:
 objects[f]=load(f);current(f)
 for p,v in strings(objects[f]):
  row=dict(path=f,pointer=p,value=v)
  if 'infinite' in v.lower():
   broad.append(row)
   if 'l2' in v.lower() or 'l²' in v.lower():rows.append(row)
  if proposal['old_exact'] in v:old.append(row)
assert len(rows)==41 and rows==inventory['all_infinite_L2_fields'] and old==inventory['old_exact_hits'] and len(old)==2
assert { (r['path'],r['pointer']) for r in old}=={(proposal['original']['path'],proposal['exact_pointer']),('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261008-PBPSCenteredMacroDefectGap.json','/publication_context/candidate_assumptions/1/lean')}
assert proposal['expected_derived_old_hits']==[r for r in old if r['path']!=proposal['original']['path']]
assert objects[proposal['original']['path']]==x
# Every complete string is checked and classified; repeated full strings share only the explanation.
reviewed=[];unique={}
for i,r in enumerate(rows):
 v=r['value'];key=sha(v.encode('utf8'));unique.setdefault(key,v)
 if proposal['old_exact'] in v:
  verdict='KNOWN_UNQUALIFIED_DUPLICATE_PENDING_EXACT_PUBLICATION_REPLACEMENT_AND_DERIVED_AUDIT_REFRESH';reason='Original old prose overstates infinite L2 at rank0. Exactly proposed publication pointer and its derived audit candidate-assumption copy; no additional independent mathematical defect.'
 elif 'potentially infinite-dimensional' in v:
  verdict='QUALIFIED_POTENTIAL_DIMENSION_CORRECT';reason='Explicitly allows rank zero and states no finite-dimensionality imposed on L2. Complete reflected-law/contraction statement retains source hypotheses and Test/Gamma boundary.'
 else:
  assert 'trueL2 generally infinite dimensional' in v
  verdict='QUALIFIED_GENERALLY_DIMENSION_CORRECT';reason='Generally explicitly qualifies dimension and retains finite Hilbert/Borel/rank0 extension. Remaining weakH1/Gamma/dynamics/main/cost boundary explicit; generic arbitrary-measure/factorization and actual macro range restatements are not new dimension assumptions.'
 reviewed.append(dict(index=i,field=r,whole_value_utf8_bytes=len(v.encode('utf8')),whole_value_utf8_sha256=key,verdict=verdict,semantic_review=reason))
extra=[r for r in broad if r not in rows];assert len(broad)==42 and len(extra)==1 and extra[0]['pointer']=='/lean/decoder_context/0' and extra[0]['value']=='The two type variables carry arbitrary measurable spaces. Both measures may be infinite. A measure-preserving function is measurable and its pushforward equals the target measure.'
assert proposal['old_exact'] not in json.dumps(y,ensure_ascii=False)
reason='The original assumption-delta entry causally duplicates the whole theorem, including its already corrected dimension prose. The exact concise replacement states the actual AE range/full centered image, SAME mean/reflection, sharp contraction and squared B defect boundary, includes rank0 and alpha*eta=1, and imposes no finite-dimensional L2 premise. Exhaustive whole-JSON diff is one metadata leaf. All41 current dimension strings fully reviewed: only the two known copied old claims remain before adoption; all other strings explicitly say generally or potentially. One additional broad infinite string describes measure mass, valid for arbitrary measures and unrelated to L2 dimension. No new semantic blocker among these dimension strings; other full-paper/source obligations remain separate.'
dump(O/'inventory-review.json',dict(status='PASS_EXHAUSTIVE_CURRENT_TWELVE_FILE_DIMENSION_REVIEW',actual_current_files=inventory['current_files'],actual_current_dimension_count=41,actual_broad_infinite_string_count=42,all_41_full_value_reviews=reviewed,actual_distinct_full_value_count=len(unique),distinct_complete_values=unique,exact_known_unqualified_current_hits=old,other_unqualified_dimension_hits=[],broad_non_dimension_extra=extra,extra_reason='Infinite measure mass is allowed by generic pullback theorem, not an infinite-dimensional L2 assertion.',after_actual_adoption_requirement='Current publication old literal disappears under exact proposal, then root must actually rederive audit2 binding/context/candidate assumptions and rescan all12 current files for zero old literal hits. This review does not pretend that future canonical zero-hit scan has occurred.',no_source_verdict_or_full_exposition_credit=True))
dump(O/'checks.json',dict(status='PASS_EXACT_ASSUMPTION_ALIGNMENT_AND_INVENTORY',proposal=current(A/'proposal.json'),proposal_complete_minus_proposal_sha256=h,original_snapshot=orig,proposed_full_JSON=newpin,actual_ALL_JSON_differences=delta,inventory=pin(O/'inventory-review.json'),actual_metadata_pointer_count=1,actual_dimension_string_count=41,current_pre_adoption_known_old_hits=2,additional_unqualified_claims=0,mathematical_reason=reason,theorem_signature_binder_proof_formula_source_hypothesis_changes=False,canonical_edits=False,compiler_started=False,original_CLOSED_stages_unmodified=True,derived_refresh_required=proposal['derived_refresh_required'],future_source_verdict_granted=False))
dump(O/'inputs.json',dict(status='PASS',count=len(inputs),inputs=[inputs[k] for k in sorted(inputs)],recipe='Actual raw bytes and only CRLF pairs -> LF with exact lengths; bounded12-file explicit current set only. Historical closed negatives untouched.'))
payload=dict(proposal=current(A/'proposal.json'),proposal_complete_minus_proposal_sha256=h,exact_pointer=delta[0],old_exact_utf8_sha256=sha(proposal['old_exact'].encode()),new_exact_utf8_sha256=sha(proposal['new_exact'].encode()),inventory_review=pin(O/'inventory-review.json'),checks=pin(O/'checks.json'),inputs=pin(O/'inputs.json'),current_files=inventory['current_files'],dimension_strings=41,current_known_old_hits=old,additional_unqualified_dimension_claims=0,derived_refresh_required=proposal['derived_refresh_required'],editorial_metadata_only=True,no_source_verdict_or_state_promotion=True);ph=logical(payload)
receipt=dict(schema_version=1,status='ACCEPTED_EXACT_METADATA_ALIGNMENT_AND_EXHAUSTIVE_INVENTORY',verdict='ACCEPT_ONE_POINTER_ALIGNMENT_WITH_REQUIRED_DERIVED_AUDIT_REFRESH',reviewer=ACTOR,proposal_sha256=h,reason=reason,exact_pointer=delta[0],checks=pin(O/'checks.json'),inputs=pin(O/'inputs.json'),inventory_review=pin(O/'inventory-review.json'),actual_current_files=12,actual_dimension_strings=41,actual_distinct_full_strings=len(unique),known_pre_adoption_unqualified_hits=2,other_unqualified_dimension_claims=0,assumption_binding_payload_sha256=ph,derived_refresh_required=proposal['derived_refresh_required'],remaining='Actual zero-old-literal12-file scan after canonical adoption/audit2 derived refresh and fresh final independent source reviewer packet/verdict still required. Gamma/root/inverse/fullweakH1/dynamics/main/cost/composition/state/reader purification remain open. No source/PROVED_LOCAL/VERIFIED/PURIFIED credit.',compiler='NOT_STARTED_CLOSED',receipt_self_recipe='Entire receipt minus ONLY receipt_sha256; sorted compact UTF8 JSON ensure_ascii=False allow_nan=False no newline');receipt['receipt_sha256']=logical(receipt);dump(O/'receipt.json',receipt)
rr=dict(schema_version=1,status='COMPLETE_ASSUMPTION_METADATA_REVIEW58',reviewer=ACTOR,inputs=[inputs[k] for k in sorted(inputs)],receipt=pin(O/'receipt.json'),checks=pin(O/'checks.json'),assumption_binding_payload=payload,assumption_binding_payload_sha256=ph,run_self_recipe='Entire complete native object minus ONLY run_sha256; sorted compact UTF8 JSON',component_recipe='Entire named assumption_binding_payload only, same compact recipe; distinct from whole native run self digest',compiler='NOT_STARTED_CLOSED');rr['run_sha256']=logical(rr);dump(O/'run.json',rr)
outs=[pin(p) for p in sorted(O.iterdir()) if p.is_file() and p.name not in ['lease.json','outputs.final.json','readback.json']];om=dict(status='PASS',count=len(outs),outputs=outs,exclusions=['outputs.final.json:self','readback.json:successor','lease.json:CLOSED-last']);om['content_self_sha256']=logical(om);dump(O/'outputs.final.json',om)
for p,f in [(O/'receipt.json','receipt_sha256'),(O/'run.json','run_sha256'),(O/'outputs.final.json','content_self_sha256')]:d=load(p);assert logical({k:v for k,v in d.items() if k!=f})==d[f]
assert logical(load(O/'run.json')['assumption_binding_payload'])==ph
for e in inputs.values():assert same(e,pin(e['path']))
for e in outs:assert same(e,pin(e['path']))
rb=dict(status='PASS_CLOSED_READY',input_readbacks=len(inputs),output_readbacks=len(outs),output_manifest=pin(O/'outputs.final.json'),receipt=pin(O/'receipt.json'),run=pin(O/'run.json'),complete_run_minus_run_sha256=rr['run_sha256'],assumption_binding_payload_sha256=ph,actual_foreground_finalizer_PID=os.getpid(),compiler='NOT_STARTED_CLOSED');rb['content_self_sha256']=logical(rb);dump(O/'readback.json',rb)
assert logical({k:v for k,v in load(O/'readback.json').items() if k!='content_self_sha256'})==rb['content_self_sha256']
finalouts=[pin(p) for p in sorted(O.iterdir()) if p.is_file() and p.name!='lease.json']
for e in finalouts:assert same(e,pin(e['path']))
ll=dict(schema_version=1,status='CLOSED',reviewer=ACTOR,read='CLOSED',write='CLOSED',Python='CLOSED',compiler='NOT_STARTED_CLOSED',actual_finalizer_PID=os.getpid(),actual_foreground_exit_code=0,exit_evidence='Successful synchronous tools.exec_command terminal EXIT0 confirms exit after final CLOSED lease write; no compiler/child/background process started.',original_open=opened,closed_utc=utc(),input_count=len(inputs),output_count=len(finalouts),outputs=finalouts,receipt=pin(O/'receipt.json'),run=pin(O/'run.json'),readback=pin(O/'readback.json'),complete_run_minus_run_sha256=rr['run_sha256'],assumption_binding_payload_sha256=ph,closure_order='LAST filesystem write after all input/output/native self/named-payload/readback validation; only precomputed stdout and process exit follow.',lease_self_recipe='Entire lease minus ONLY lease_sha256; sorted compact UTF8 JSON recipe');ll['lease_sha256']=logical(ll);lb=(json.dumps(ll,ensure_ascii=False,indent=2)+'\n').encode('utf8')
summary=dict(status='CLOSED',verdict=receipt['verdict'],receipt=pin(O/'receipt.json'),run=pin(O/'run.json'),complete_run_minus_run_sha256=rr['run_sha256'],assumption_binding_payload_sha256=ph,lease=dict(path=(O/'lease.json').relative_to(R).as_posix(),bytes=len(lb),raw_sha256=sha(lb),lf_sha256=sha(lb),lease_sha256=ll['lease_sha256']),actual_finalizer_PID=os.getpid(),input_count=len(inputs),output_count=len(finalouts),actual_JSON_diff_count=1,current_files=12,dimension_strings=41,broad_infinite_strings=42,distinct_full_dimension_strings=len(unique),current_known_bad_hits=2,additional_unqualified_claims=0,compiler='NOT_STARTED_CLOSED');stdout=json.dumps(summary,ensure_ascii=False)
dump(O/'lease.json',ll)
print(stdout)
