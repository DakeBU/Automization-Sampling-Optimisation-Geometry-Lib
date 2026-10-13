import os,sys,pathlib,json,hashlib,datetime
sys.dont_write_bytecode=True;sys.stdout.reconfigure(encoding='utf8')
R=pathlib.Path('E:/Samplinglib');B=R/'runs/20261007-companion-priority/pbps-macroscopic-centered-range58';A=B/'exposition-wording-overlay58';O=B/'exposition-wording-overlay-review58';ACTOR='whole_math52_editorial58'
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
  if ('/runs/' in s or '/.astis/' in s) and any(('59' in c or '60' in c) and any(k in c for k in ['pbps','preproof','sourcegraph','preread','future']) for c in s.split('/')):raise PermissionError('Editorial58 excludes future59/60')
  if '/pbps-macroscopic-centered-range58/' in s and any(k in s for k in ['/source-review58/','/anonymous-decoder/']):raise PermissionError('Editorial58 excludes postproof source/decoder verdict')
sys.addaudithook(guard);O.mkdir(exist_ok=True)
opened=dict(status='OPEN',actor=ACTOR,actual_foreground_Python_PID=os.getpid(),opened_utc=utc(),read='OPEN',write='OPEN',Python='OPEN',compiler='NOT_STARTED_CLOSED',scope='Exact independent editorial wording overlay only; no original CLOSED/native/canonical/Lean/source hypothesis/proof changes or source verdict/state promotion')
dump(O/'lease.json',opened)
inputs={};pinchecks=[];selfs=[]
def current(p):a=pin(p);inputs[a['path']]=a;return a
def full(p,f):
 d=load(p);h=logical({k:v for k,v in d.items() if k!=f});assert h==d[f];selfs.append(dict(input=current(p),self_field=f,logical_sha256=h,recipe='Complete native object minus ONLY named top-level self field; sorted compact UTF8 JSON ensure_ascii=False allow_nan=False no newline'));return d
def at(d,p):
 for k in p.split('/')[1:]:
  k=k.replace('~1','/').replace('~0','~');d=d[int(k)] if isinstance(d,list) else d[k]
 return d
def diffs(x,y,p=''):
 if isinstance(x,dict) and isinstance(y,dict):
  z=[]
  for k in sorted(set(x)|set(y)):
   q=p+'/'+k.replace('~','~0').replace('/','~1');z+=([q] if k not in x or k not in y else diffs(x[k],y[k],q))
  return z
 if isinstance(x,list) and isinstance(y,list) and len(x)==len(y):
  z=[]
  for i,(a,b) in enumerate(zip(x,y)):z+=diffs(a,b,p+'/'+str(i))
  return z
 return [] if x==y else [p]
proposal=full(A/'proposal.json','proposal_sha256');assert proposal['proposal_sha256']=='f92fa64a9e22c4671a6448a7aa1e92c4b4955ac8617676afc3837c28f8268cff'
assert proposal['old_exact']=='uses actual infinite-dimensional L²(J)' and proposal['new_exact']=='uses the actual, potentially infinite-dimensional L²(J), without imposing finite-dimensionality on L²'
assert proposal['mathematical_source_theorem_repair']==proposal['assumption_signature_proof_change']==proposal['source_repair_requested']==False and proposal['original_native_reviews_immutable'] is True
expected=[['/items/0/statement'],['/units/0/statement','/units/0/lean_statement'],['/source/original_text','/source/text_sha256']];changes=[]
for i,e in enumerate(proposal['changes']):
 original=current(e['snapshot']);assert same(e['original'],original);pinchecks.append(dict(expected_original=e['original'],actual_exact_snapshot=original));newpin=current(e['proposal']);x=load(e['snapshot']);y=load(e['proposal']);delta=diffs(x,y);assert set(delta)==set(expected[i])==set(e['json_pointers']+e['derived_fields'])
 vals=[]
 for p in e['json_pointers']:
  old=at(x,p);new=at(y,p);assert isinstance(old,str) and old.count(proposal['old_exact'])==1 and new==old.replace(proposal['old_exact'],proposal['new_exact']);vals.append(dict(pointer=p,old_utf8_bytes=len(old.encode()),new_utf8_bytes=len(new.encode()),old_text_sha256=sha(old.encode()),new_text_sha256=sha(new.encode()),exact_replacement_count=1))
 if i==2:
  assert x['source']['text_sha256']==sha(x['source']['original_text'].encode('utf8')) and y['source']['text_sha256']==sha(y['source']['original_text'].encode('utf8'))
  vals.append(dict(pointer='/source/text_sha256',old=x['source']['text_sha256'],new=y['source']['text_sha256'],recipe='Actual whole source.original_text string UTF8 bytes, no newline added',derived_only=True))
 changes.append(dict(original_expected=e['original'],actual_original_snapshot=original,proposed_full_JSON=newpin,actual_ALL_json_pointer_differences=delta,changed_values=vals,no_other_JSON_change=True))
assert len(changes)==3 and sum(len(x['actual_ALL_json_pointer_differences']) for x in changes)==5
# Frozen real Lean and three sealed exact statements; no proof replay or compiler.
freeze=load(B/'math-freeze.json');current(B/'math-freeze.json');names=['l2_pullback_range_eq_lpMeas','actual_macroscopic_centered_range','actual_centered_macro_contraction_and_defect_gap'];files=['AutoSamplingTheory/TechnicalLemmas/Measure/L2PullbackRange.lean','AutoSamplingTheory/ExampleCases/ProximalBPS/MacroscopicRange.lean','Tests/ProximalBPSMacroscopicRange.lean'];seals=['generic-prospective-statement.txt','prospective-statement.txt','consumer-prospective-statement.txt'];signatures=[]
for n,f,s in zip(names,files,seals):
 a=current(f);original=next(e for e in freeze['inputs'] if e['path']==f);assert same(original,a);pinchecks.append(dict(expected_original=original,actual_current=a));text=path(f).read_bytes().replace(b'\r\n',b'\n').decode('utf8');start=text.index('theorem '+n);end=text.index(' := by',start);header=(text[start:end]+'\n').encode();sp=R/'runs/20261007-companion-priority/pbps-macro-range-preproof58'/s;sealed=sp.read_bytes().replace(b'\r\n',b'\n');assert header==sealed;signatures.append(dict(name=n,current_Lean=a,sealed_statement=current(sp),exact_signature_LF_bytes=len(header),exact_signature_LF_sha256=sha(header)))
oldmath=B/'whole-math58';native=[]
for f,h,selfkey in [('receipt.json','a94fcbeca774edcc1a47eceaeb45d3fd250e3e7f1077030c272c17ac4ba00eb6','receipt_sha256'),('run.json','46ba51bf4dc1c78b88c2052f8c30bc7033487dc1ba5b49f8f40ea22c96d8a048','run_sha256'),('lease.json','5701049fa736fe8f02740cdece42959358ee7c458bf621863b2d3c3fbedd1eb8','lease_sha256')]:
 a=current(oldmath/f);assert a['raw_sha256']==h;d=full(oldmath/f,selfkey);native.append(a)
 if f=='lease.json':assert d['status']=='CLOSED'
reason='Rank0 is allowed by all three frozen signatures. On the one-point rank0 state carrier the actual normalized joint law is Dirac, so real L2(J) is one-dimensional and its centered macro space is zero. Thus unconditional infinite-dimensional is inaccurate prose. Potentially infinite-dimensional, with no finite-dimensionality imposed on L2, accurately states the general space boundary while preserving the finite-dimensional carrier extension. The lesson field lean_statement contains the same human mathematical restatement, not a modified Lean theorem header. All actual source hypotheses, formulas, AE laws, operators, binders and proof bodies remain unchanged.'
dump(O/'checks.json',dict(status='PASS_EXACT_EDITORIAL_DIFF_ONLY',proposal=current(A/'proposal.json'),ALL_JSON_diffs=changes,total_actual_JSON_pointer_changes=5,exact_signature_checks=signatures,actual_raw_LF_pin_checks=pinchecks,native_full_self_checks=selfs,original_closed_math_outputs_unchanged=native,mathematical_reason=reason,no_new_assumption_or_Lean_signature_change=True,no_source_hypothesis_or_proof_repair=True,no_compiler=True,pending_after_adoption=proposal['pending_derived_rebinding'],successor_source_verdict_granted=False,scope='Only reviewed exact proposal bytes. Audit2 derived publication binding/context refresh and distinct successor source-review packet remain mandatory; original source reviewer closing frozen101 is not replaced or preaccepted. No PROVED_LOCAL/VERIFIED/PURIFIED/main/live/Goal credit.'))
dump(O/'inputs.json',dict(status='PASS',count=len(inputs),inputs=[inputs[k] for k in sorted(inputs)],recipe='Exact raw bytes and only CRLF pairs to LF, including lengths; originals compared to immutable snapshots, not mutable canonical administrative bytes'))
payload=dict(proposal=current(A/'proposal.json'),proposal_complete_minus_proposal_sha256=proposal['proposal_sha256'],exact_three_full_JSON_changes=changes,checks=pin(O/'checks.json'),inputs=pin(O/'inputs.json'),sealed_Lean_signatures=signatures,original_CLOSED_math_unchanged=native,editorial_only=True,no_successor_source_verdict=True,pending_after_adoption=proposal['pending_derived_rebinding']);ph=logical(payload)
receipt=dict(schema_version=1,status='ACCEPTED_EXACT_EDITORIAL_WORDING_ONLY',verdict='ACCEPT_EDITORIAL_CLARIFICATION_NO_MATHEMATICAL_REPAIR',reviewer=ACTOR,proposal_sha256=proposal['proposal_sha256'],reason=reason,checks=pin(O/'checks.json'),inputs=pin(O/'inputs.json'),actual_JSON_diff_count=5,editorial_binding_payload_sha256=ph,original_math_CLOSED_unchanged=native,pending_after_adoption=proposal['pending_derived_rebinding'],remaining='Successor audit2 derived bindings/context and fresh source reviewer packet/final independent source verdict required. Gamma/root/inverse/fullweakH1/dynamics/main/cost/composition and exact-science/state/reader purification remain open.',compiler='NOT_STARTED_CLOSED',no_canonical_edit=True,no_PROVED_LOCAL_VERIFIED_PURIFIED=True,receipt_self_recipe='Entire receipt minus ONLY receipt_sha256; sorted compact UTF8 JSON ensure_ascii=False allow_nan=False no newline');receipt['receipt_sha256']=logical(receipt);dump(O/'receipt.json',receipt)
rr=dict(schema_version=1,status='COMPLETE_EDITORIAL_REVIEW58',reviewer=ACTOR,inputs=[inputs[k] for k in sorted(inputs)],receipt=pin(O/'receipt.json'),checks=pin(O/'checks.json'),editorial_binding_payload=payload,editorial_binding_payload_sha256=ph,run_self_recipe='Entire complete native object minus ONLY run_sha256; sorted compact UTF8 JSON recipe',component_recipe='Entire named editorial_binding_payload only, same compact recipe; distinct from complete run self hash',compiler='NOT_STARTED_CLOSED');rr['run_sha256']=logical(rr);dump(O/'run.json',rr)
outs=[pin(p) for p in sorted(O.iterdir()) if p.is_file() and p.name not in ['lease.json','outputs.final.json','readback.json']];om=dict(status='PASS',count=len(outs),outputs=outs,exclusions=['outputs.final.json:self','readback.json:successor','lease.json:CLOSED-last']);om['content_self_sha256']=logical(om);dump(O/'outputs.final.json',om)
for p,f in [(O/'receipt.json','receipt_sha256'),(O/'run.json','run_sha256'),(O/'outputs.final.json','content_self_sha256')]:d=load(p);assert logical({k:v for k,v in d.items() if k!=f})==d[f]
assert logical(load(O/'run.json')['editorial_binding_payload'])==ph
for e in inputs.values():assert same(e,pin(e['path']))
for e in outs:assert same(e,pin(e['path']))
rb=dict(status='PASS_CLOSED_READY',input_readbacks=len(inputs),output_readbacks=len(outs),output_manifest=pin(O/'outputs.final.json'),receipt=pin(O/'receipt.json'),run=pin(O/'run.json'),complete_run_minus_run_sha256=rr['run_sha256'],editorial_binding_payload_sha256=ph,actual_foreground_finalizer_PID=os.getpid(),compiler='NOT_STARTED_CLOSED');rb['content_self_sha256']=logical(rb);dump(O/'readback.json',rb)
assert logical({k:v for k,v in load(O/'readback.json').items() if k!='content_self_sha256'})==rb['content_self_sha256']
finalouts=[pin(p) for p in sorted(O.iterdir()) if p.is_file() and p.name!='lease.json']
for e in finalouts:assert same(e,pin(e['path']))
ll=dict(schema_version=1,status='CLOSED',reviewer=ACTOR,read='CLOSED',write='CLOSED',Python='CLOSED',compiler='NOT_STARTED_CLOSED',actual_finalizer_PID=os.getpid(),actual_foreground_exit_code=0,exit_evidence='Successful synchronous tools.exec_command terminal EXIT0 confirms exit after final CLOSED lease write. No compiler/child/background process started.',original_open=opened,closed_utc=utc(),input_count=len(inputs),output_count=len(finalouts),outputs=finalouts,receipt=pin(O/'receipt.json'),run=pin(O/'run.json'),readback=pin(O/'readback.json'),complete_run_minus_run_sha256=rr['run_sha256'],editorial_binding_payload_sha256=ph,closure_order='LAST filesystem write after all input/output/native self/named-payload/readback validations; only precomputed stdout and process exit follow.',lease_self_recipe='Entire lease minus ONLY lease_sha256; sorted compact UTF8 JSON recipe');ll['lease_sha256']=logical(ll);lb=(json.dumps(ll,ensure_ascii=False,indent=2)+'\n').encode('utf8')
summary=dict(status='CLOSED',verdict=receipt['verdict'],receipt=pin(O/'receipt.json'),run=pin(O/'run.json'),complete_run_minus_run_sha256=rr['run_sha256'],editorial_binding_payload_sha256=ph,lease=dict(path=(O/'lease.json').relative_to(R).as_posix(),bytes=len(lb),raw_sha256=sha(lb),lf_sha256=sha(lb),lease_sha256=ll['lease_sha256']),actual_finalizer_PID=os.getpid(),input_count=len(inputs),output_count=len(finalouts),actual_JSON_diff_count=5,source_code_pins=3,exact_sealed_signatures=3,native_full_selfchecks=len(selfs),compiler='NOT_STARTED_CLOSED');stdout=json.dumps(summary,ensure_ascii=False)
dump(O/'lease.json',ll)
print(stdout)
