import os,sys,pathlib,json,hashlib,datetime
sys.dont_write_bytecode=True;sys.stdout.reconfigure(encoding='utf8')
R=pathlib.Path('E:/Samplinglib');B=R/'runs/20261007-companion-priority/pbps-macroscopic-centered-range58';A=B/'exposition-api-overlay58';O=B/'exposition-api-overlay-review58';ACTOR='whole_math52_API_locator58'
def path(p):
 p=pathlib.Path(str(p).replace('\\','/'));return p if p.is_absolute() else R/p
def load(p):return json.loads(path(p).read_text(encoding='utf8'))
def sha(b):return hashlib.sha256(b).hexdigest()
def logical(d):return sha(json.dumps(d,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode('utf8'))
def dump(p,d):path(p).write_bytes((json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode('utf8'))
def pin(p):
 p=path(p);b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');return dict(path=p.relative_to(R).as_posix(),bytes=len(b),lf_bytes=len(lf),raw_sha256=sha(b),lf_sha256=sha(lf))
def same(e,a):return all(e[k]==a[k] for k in ['bytes','raw_sha256','lf_sha256']) and ('lf_bytes' not in e or e['lf_bytes']==a['lf_bytes'])
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def guard(e,a):
 if e=='open' and a and isinstance(a[0],(str,bytes,os.PathLike)):
  s=os.fsdecode(a[0]).replace('\\','/').lower()
  if ('/runs/' in s or '/.astis/' in s) and any(('59' in c or '60' in c) and any(k in c for k in ['pbps','preproof','sourcegraph','preread','future']) for c in s.split('/')):raise PermissionError('API58 excludes future59/60')
  if '/pbps-macroscopic-centered-range58/' in s and any(k in s for k in ['/source-review58/','/anonymous-decoder/']):raise PermissionError('API58 excludes postproof source/decoder verdict')
sys.addaudithook(guard);O.mkdir(exist_ok=True)
opened=dict(status='OPEN',actor=ACTOR,actual_foreground_Python_PID=os.getpid(),opened_utc=utc(),read='OPEN',write='OPEN',Python='OPEN',compiler='NOT_STARTED_CLOSED',scope='Exact independent metadata API locator only, no original CLOSED/canonical/Lean/formula/proof/source edits or verdict/state credit')
dump(O/'lease.json',opened);inputs={}
def current(p):a=pin(p);inputs[a['path']]=a;return a
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
proposal=load(A/'proposal.json');h=logical({k:v for k,v in proposal.items() if k!='proposal_sha256'});assert h==proposal['proposal_sha256']=='e7d198c84011146d18eaf2ddc4177a8eb2f0577e94a69df5ddda7da03af56b80';current(A/'proposal.json')
original=current(proposal['original_snapshot']);assert same(proposal['original'],original);proposed=current(proposal['proposed']);x=load(proposal['original_snapshot']);y=load(proposal['proposed']);changes=diff(x,y)
assert changes==[proposal['exact_pointer']]==['/units/0/mathlib_dependencies/2'];assert x['units'][0]['mathlib_dependencies'][2]==proposal['old_exact']=='Lp.norm_map' and y['units'][0]['mathlib_dependencies'][2]==proposal['new_exact']=='LinearIsometry.norm_map'
assert proposal['theorem_proof_signature_source_assumption_change'] is False
api=current(proposal['actual_fixed_API']['path']);assert same(proposal['actual_fixed_API'],api)
text=path(api['path']).read_bytes().replace(b'\r\n',b'\n').decode('utf8');lines=text.splitlines();assert lines[135]=='namespace LinearIsometry' and lines[199]=='protected lemma norm_map (x : E) : ‖f x‖ = ‖x‖ := by simp'
selected=(lines[199]+'\n').encode('utf8')
freeze=load(B/'math-freeze.json');current(B/'math-freeze.json');f='Tests/ProximalBPSMacroscopicRange.lean';test=current(f);expected=next(e for e in freeze['inputs'] if e['path']==f);assert same(expected,test)
code=path(f).read_text(encoding='utf8');assert 'let M : Lp ℝ 2 ν →ₗᵢ[ℝ] Lp ℝ 2 J := Lp.compMeasurePreservingₗᵢ ℝ Prod.snd hp' in code and code.count('M.norm_map')==3
reason='The actual Test M is a real linear isometry on the actual L2 spaces. The fixed Mathlib file declares protected lemma norm_map inside namespace LinearIsometry at line200, giving norm(M u)=norm(u). Thus LinearIsometry.norm_map is the precise dependency locator for the actual three M.norm_map uses. Only this metadata reference string changes; the whole JSON comparison shows no statement, formula, binder, proof, source condition or other dependency change.'
dump(O/'checks.json',dict(status='PASS_EXACT_SINGLE_POINTER_API_LOCATOR',proposal=current(A/'proposal.json'),proposal_complete_minus_proposal_sha256=h,original_snapshot=original,proposed_full_JSON=proposed,actual_ALL_JSON_differences=changes,old='Lp.norm_map',new='LinearIsometry.norm_map',fixed_API=api,selected_API=dict(namespace='LinearIsometry',line=200,text=lines[199],selected_LF_bytes=len(selected),selected_LF_sha256=sha(selected)),immutable_real_Test=test,original_frozen_Test=expected,actual_M_type='Lp real2nu -> linear isometry[real] Lp real2J',M_norm_map_actual_uses=3,mathematical_reason=reason,no_Lean_formula_statement_proof_binder_source_assumption_change=True,no_compiler=True,derived_successor_requirements=proposal['derived_rebinding_required'],successor_source_verdict_granted=False,no_VERIFIED_or_Purified_credit=True))
dump(O/'inputs.json',dict(status='PASS',count=len(inputs),inputs=[inputs[k] for k in sorted(inputs)],recipe='Exact raw and only CRLF pairs -> LF with actual lengths; no canonical mutable-byte substitution'))
payload=dict(proposal=current(A/'proposal.json'),proposal_complete_minus_proposal_sha256=h,exact_pointer=changes[0],old='Lp.norm_map',new='LinearIsometry.norm_map',fixed_API=api,selected_API_LF_sha256=sha(selected),immutable_Test=test,checks=pin(O/'checks.json'),inputs=pin(O/'inputs.json'),reference_locator_only=True,no_source_or_VERIFIED_credit=True,derived_successor_requirements=proposal['derived_rebinding_required']);ph=logical(payload)
receipt=dict(schema_version=1,status='ACCEPTED_EXACT_API_REFERENCE_LOCATOR_ONLY',verdict='ACCEPT_SINGLE_POINTER_LINEARISOMETRY_NORM_MAP_REFERENCE',reviewer=ACTOR,proposal_sha256=h,exact_pointer=changes[0],reason=reason,checks=pin(O/'checks.json'),inputs=pin(O/'inputs.json'),API_binding_payload_sha256=ph,source_successor_requirement=proposal['derived_rebinding_required'],remaining='Original math58/editorial review and closing32-input successor source stage remain immutable. Root must wait for closure, then refresh only audit2 derived binding/context and fresh final reviewer packet. No source fidelity, PROVED_LOCAL, VERIFIED, PURIFIED or theorem repair granted.',compiler='NOT_STARTED_CLOSED',receipt_self_recipe='Entire receipt minus ONLY receipt_sha256; sorted compact UTF8 ensure_ascii=False allow_nan=False no newline');receipt['receipt_sha256']=logical(receipt);dump(O/'receipt.json',receipt)
rr=dict(schema_version=1,status='COMPLETE_API_LOCATOR_REVIEW58',reviewer=ACTOR,inputs=[inputs[k] for k in sorted(inputs)],receipt=pin(O/'receipt.json'),checks=pin(O/'checks.json'),API_binding_payload=payload,API_binding_payload_sha256=ph,run_self_recipe='Entire complete native object minus ONLY run_sha256; sorted compact UTF8 JSON',component_recipe='Entire named API_binding_payload only, same compact recipe; distinct from complete run self digest',compiler='NOT_STARTED_CLOSED');rr['run_sha256']=logical(rr);dump(O/'run.json',rr)
outs=[pin(p) for p in sorted(O.iterdir()) if p.is_file() and p.name not in ['lease.json','outputs.final.json','readback.json']];om=dict(status='PASS',count=len(outs),outputs=outs,exclusions=['outputs.final.json:self','readback.json:successor','lease.json:CLOSED-last']);om['content_self_sha256']=logical(om);dump(O/'outputs.final.json',om)
for p,f in [(O/'receipt.json','receipt_sha256'),(O/'run.json','run_sha256'),(O/'outputs.final.json','content_self_sha256')]:d=load(p);assert logical({k:v for k,v in d.items() if k!=f})==d[f]
assert logical(load(O/'run.json')['API_binding_payload'])==ph
for e in inputs.values():assert same(e,pin(e['path']))
for e in outs:assert same(e,pin(e['path']))
rb=dict(status='PASS_CLOSED_READY',input_readbacks=len(inputs),output_readbacks=len(outs),output_manifest=pin(O/'outputs.final.json'),receipt=pin(O/'receipt.json'),run=pin(O/'run.json'),complete_run_minus_run_sha256=rr['run_sha256'],API_binding_payload_sha256=ph,actual_foreground_finalizer_PID=os.getpid(),compiler='NOT_STARTED_CLOSED');rb['content_self_sha256']=logical(rb);dump(O/'readback.json',rb)
assert logical({k:v for k,v in load(O/'readback.json').items() if k!='content_self_sha256'})==rb['content_self_sha256']
finalouts=[pin(p) for p in sorted(O.iterdir()) if p.is_file() and p.name!='lease.json']
for e in finalouts:assert same(e,pin(e['path']))
ll=dict(schema_version=1,status='CLOSED',reviewer=ACTOR,read='CLOSED',write='CLOSED',Python='CLOSED',compiler='NOT_STARTED_CLOSED',actual_finalizer_PID=os.getpid(),actual_foreground_exit_code=0,exit_evidence='Successful synchronous tools.exec_command terminal EXIT0 confirms exit after final CLOSED lease write; no compiler/child/background process started.',original_open=opened,closed_utc=utc(),input_count=len(inputs),output_count=len(finalouts),outputs=finalouts,receipt=pin(O/'receipt.json'),run=pin(O/'run.json'),readback=pin(O/'readback.json'),complete_run_minus_run_sha256=rr['run_sha256'],API_binding_payload_sha256=ph,closure_order='LAST filesystem write after all input/output/full-self/named-payload/readback validations; only precomputed stdout and process exit follow.',lease_self_recipe='Entire complete lease minus ONLY lease_sha256; sorted compact UTF8 JSON recipe');ll['lease_sha256']=logical(ll);lb=(json.dumps(ll,ensure_ascii=False,indent=2)+'\n').encode('utf8')
summary=dict(status='CLOSED',verdict=receipt['verdict'],receipt=pin(O/'receipt.json'),run=pin(O/'run.json'),complete_run_minus_run_sha256=rr['run_sha256'],API_binding_payload_sha256=ph,lease=dict(path=(O/'lease.json').relative_to(R).as_posix(),bytes=len(lb),raw_sha256=sha(lb),lf_sha256=sha(lb),lease_sha256=ll['lease_sha256']),actual_finalizer_PID=os.getpid(),input_count=len(inputs),output_count=len(finalouts),actual_JSON_diff_count=1,compiler='NOT_STARTED_CLOSED');stdout=json.dumps(summary,ensure_ascii=False)
dump(O/'lease.json',ll)
print(stdout)
