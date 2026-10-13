import os,sys,pathlib,json,hashlib,copy,datetime,subprocess
ROOT=pathlib.Path('E:/Samplinglib');BASE=ROOT/'runs/20261007-companion-priority';R=BASE/'pbps-root-commutation67';O=R/'independent-attribution-overlay67';P=R/'presentation-attribution-overlay67';H=BASE/'pbps-first-corrector-energy-preproof67/independent-header-source67';PRIMARY=BASE/'pbps-first-corrector-energy-preproof67/independent-primary67'
sys.path[:0]=[str(ROOT/'tools'),str(ROOT/'website/scripts')]
import astis_publication as publication
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(j):return json.dumps(j,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()
def load(p):return json.loads(pathlib.Path(p).read_bytes())
def write(n,j):(O/n).write_bytes(json.dumps(j,sort_keys=True,ensure_ascii=False,indent=2).encode()+b'\n')
def pin(p,b=None):
 p=pathlib.Path(p);b=p.read_bytes() if b is None else b;n=b.replace(b'\r\n',b'\n');return {'path':p.as_posix(),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_bytes':len(n),'LF_sha256':sha(n)}
snapshots=[]
def snap(p):
 p=pathlib.Path(p);b=p.read_bytes();d=O/'inputs';d.mkdir(exist_ok=True);i=len(snapshots);a=d/f'{i:03}.RAW.snapshot';l=d/f'{i:03}.LF.snapshot';a.write_bytes(b);l.write_bytes(b.replace(b'\r\n',b'\n'));z={'original':pin(p,b),'RAW_snapshot':pin(a),'LF_snapshot':pin(l)};snapshots.append(z);return json.loads(b) if p.suffix=='.json' else b
def differences(a,b,path=''):
 if isinstance(a,dict) and isinstance(b,dict):
  out=[]
  for k in sorted(set(a)|set(b)):
   assert k in a and k in b,('key added/removed',path,k)
   out+=differences(a[k],b[k],path+'/'+k)
  return out
 if isinstance(a,list) and isinstance(b,list):
  assert len(a)==len(b),('list changed length',path)
  return [z for i,(x,y) in enumerate(zip(a,b)) for z in differences(x,y,path+'/'+str(i))]
 return [] if a==b else [{'field':path,'before':a,'after':b}]
pid=os.getpid();print(json.dumps({'actual_foreground_PID':pid,'stage':'bounded-attribution-review'}),flush=True)
sourcefirst=load(O/'source-first-adoption.json');assert not sourcefirst['proposal67_seen']
for z in sourcefirst['primary_frozen_pins']:assert sha(pathlib.Path(z['path']).read_bytes())==z['RAW_sha256']
assert sha((PRIMARY/'lease.final.json').read_bytes())=='c4ec5c43dff4f4ddedeba0cb1cf4a0c969d8bac33029133a3df63e150cacad8c'
assert sha((H/'lease.final.json').read_bytes())=='8af44d6dfd0e79e75f2f86accbc728cefa9f3f43b50b07469bba0ec4091596fb'
for p in [PRIMARY/'source-proof-graph.json',PRIMARY/'source-coverage-inventory.json',PRIMARY/'residual-next-header.json',H/'header-decisions.json',H/'literal-representation-and-inherited-contract-audit.json']:snap(p)
proposal=snap(P/'proposal.json');assert sha((P/'proposal.json').read_bytes())=='61b585a8148530cd203ea28b33034b75c32ba02dc665c9f4f27a7f9de88b3088'
assert proposal['exact_text_before']=='The genuine original-input Test derives f=' and proposal['exact_text_after']=='The preceding independently reviewed ambient-adjoint Test derives f='
before=[];after=[];diffs=[];approvedfiles=[]
allowed=[{'/items/0/statement'},{'/units/0/statement','/units/0/lean_statement'},{'/publication_binding_sha256','/publication_context/lesson/lean_statement','/publication_context/lesson/statement','/publication_context/statement','/source/original_text','/source/text_sha256'}]
for i,c in enumerate(proposal['changes']):
 a=snap(P/c['before_snapshot']);b=snap(P/c['after_snapshot']);current=ROOT/c['path'];raw=current.read_bytes();assert sha(raw)==c['before_raw_sha256']==sha((P/c['before_snapshot']).read_bytes());assert sha((P/c['after_snapshot']).read_bytes())==c['after_raw_sha256']
 d=differences(a,b);assert {z['field'] for z in d}==allowed[i]
 for z in d:
  if z['field'] not in {'/publication_binding_sha256','/source/text_sha256'}:assert z['before'].count(proposal['exact_text_before'])==1 and z['before'].replace(proposal['exact_text_before'],proposal['exact_text_after'])==z['after']
 before.append(a);after.append(b);diffs.append({'canonical_path':c['path'],'exact_leaf_deltas':d});approvedfiles.append({'canonical_path':c['path'],'exact_before_RAW_sha256':c['before_raw_sha256'],'approved_proposed_after_RAW_sha256':c['after_raw_sha256'],'approved_after_snapshot':pin(P/c['after_snapshot'])})
olditem=before[0]['items'][0];newitem=after[0]['items'][0];name=newitem['bindings'][0]['declaration'];data=publication.inputs();olddata=copy.deepcopy(data);newdata=copy.deepcopy(data);olddata['lessons'][name]=before[1]['units'][0];newdata['lessons'][name]=after[1]['units'][0]
oldbinding=publication.binding_digest(olditem,olditem['bindings'][0],olddata);newbinding=publication.binding_digest(newitem,newitem['bindings'][0],newdata);oldcontext=publication.review_context(olditem,olditem['bindings'][0],olddata);newcontext=publication.review_context(newitem,newitem['bindings'][0],newdata)
assert oldbinding==proposal['previous_binding']==before[2]['publication_binding_sha256'];assert newbinding==proposal['proposed_binding']==after[2]['publication_binding_sha256'];assert oldcontext==before[2]['publication_context'] and newcontext==after[2]['publication_context']
for a in [before[2],after[2]]:assert sha(a['source']['original_text'].encode())==a['source']['text_sha256']
assert oldcontext['current_lean_module']==newcontext['current_lean_module']
modules=['AutoSamplingTheory/TechnicalLemmas/Measure/L2RealSquareCommute.lean','AutoSamplingTheory/ExampleCases/ProximalBPS/ActualRootCommutation.lean','Tests/ProximalBPSActualRootCommutation.lean','Tests/ProximalBPSAmbientAdjointCorrector.lean'];texts={};modulepins=[]
for n in modules:
 b=snap(ROOT/n);texts[n]=b.decode();modulepins.append(pin(ROOT/n,b))
assert sha((ROOT/modules[3]).read_bytes())=='3df807d4c8e456830c8ecbaeb6d20bd2331df6f09a951d8e5061ee18b6045685'
main=texts[modules[1]];test=texts[modules[2]];oldtest=texts[modules[3]];leaf=texts[modules[0]]
representations=[]
for i,text in [(1,main),(2,test)]:
 p=H/f'statement{i}.definition.lean.RAW.snapshot';sealed=snap(p).decode();actual=text[text.index('private def '):text.index('\ntheorem ')].strip();assert actual==sealed.strip();representations.append({'index':i,'sealed_definition':pin(p),'current_private_literal_equals_seal':True,'asserts_proof_or_provider':False})
leafheader=snap(H/'header0-expanded.lean.RAW.snapshot').decode().strip();actual=leaf[leaf.index('theorem positive_square_commutation'):leaf.index(' := by')].strip();assert actual==leafheader
assert 'have hKself : IsSelfAdjoint (A0*Inv)' in test
assert 'have hCoefficient : (1 : HP0 →L[ℝ] HP0)+(A0*Inv)*(A0*Inv)=Inv*Inv' in test
assert 'exact hGlobal' in test and 'exact hGlobal' in main
assert 'f=HP.subtypeL (HP0.subtypeL fP)+(fperp : Lp ℝ 2 J)' in oldtest
assert '‖fV‖^2≤‖f‖^2-‖fP‖^2' in oldtest
assert 'f=HP.subtypeL (HP0.subtypeL fP)+(fperp : Lp ℝ 2 J)' not in test
assert '‖fV‖^2≤‖f‖^2-‖fP‖^2' not in test
assert 'L2RealSquareCommute.positive_square_commutation\n    ν Γ (1+T) hΓ hDpos hCommSquare' in main
write('finite-diff-binding-and-consumer-audit.json',{'schema':'overlay67-exact-finite-attribution-audit-v1','actual_foreground_PID':pid,'source_first_process':sourcefirst,'proposal_RAW':pin(P/'proposal.json'),'approved_proposed_files':approvedfiles,'exhaustive_leaf_deltas':diffs,'before_binding_recomputed':oldbinding,'after_binding_recomputed':newbinding,'before_context_sha256':sha(canon(oldcontext)),'after_context_sha256':sha(canon(newcontext)),'audit_source_text_hashes_recomputed':True,'current_three_canonical_files_equal_exact_BEFORE':True,'all_other_JSON_values_formulae_BODY_and_context_module_unchanged':True,'full_module_input_pins':modulepins,'private_literal_expansions':representations,'generic_leaf_header_equals_sealed_header0':True,'Test66_explicit_reconstruction_and_squared_norm_budget':True,'Test67_explicit_new_K_selfadjoint_and_I_plus_Ksquare_eq_Invsquare':True,'Test67_inherits_global_centered_clause_without_explicit_Test66_reconstruction_conclusion':True,'no_proof_search_or_compiler_started':True,'no_final_source67_verdict':True})
slots={
 'objects':{'relation':'unchanged','evidence':'Same actual laws/P/e/U/T/Gamma/GammaP/HP0/Inv/A0/B0/V0/R and actual globally centered input. Only the Test origin is clarified.'},
 'assumptions':{'relation':'unchanged','evidence':'No Lean/header/binder, metadata assumptions, generic positive-G,D supplement or actual internally produced D=I+T premise changes. Original C2/Hessian/eta conditions only.'},
 'quantifiers':{'relation':'unchanged','evidence':'Every original potential/space/step and globally centered f quantifier retained. No new certificate or Nontrivial/H1/floor/strict endpoint premise.'},
 'conclusion':{'relation':'attribution-corrected-no-mathematical-delta','evidence':'Test66 explicitly concludes f reconstruction/B*f/norm budget. Test67 explicitly adds K=A0 Inv selfadjoint and I+K²=Inv² while retaining inherited global clause. The after paragraph names each correctly.'},
 'domains':{'relation':'unchanged','evidence':'Real scalar-valued L2 operators; full ambient adjoint versus exact kerP and exact centered HP0 remain distinct. No full-space inverse, onto kerP or reverse product.'},
 'constant_dependencies':{'relation':'unchanged','evidence':'Same gamma, original positive capped eta and legal rank0/alphaeta=1. No source bound or estimate is altered.'},
 'scopes':{'relation':'presentation-attribution-only','evidence':'Primary graph B23 coefficient ingredient and separate B21 consumer remain ASTIS source-derived supplementation. Full sharp B23 energy/B21 rotation/dynamics/cost/composition/full Exposition/PURIFIED remain open. Overlay approval is not final whole-module source67 acceptance.'}}
decision={'schema':'overlay67-independent-attribution-decision-v1','reviewer':'/root/independent_source64','actual_review_PID':pid,'reviewed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'verdict':'APPROVE_EXACT_PROPOSED_ATTRIBUTION_OVERLAY_ONLY','proposal_RAW_sha256':sha((P/'proposal.json').read_bytes()),'proposal_path':(P/'proposal.json').as_posix(),'exact_phrase_before':proposal['exact_text_before'],'exact_phrase_after':proposal['exact_text_after'],'approved_proposed_files':approvedfiles,'seven_semantic_slots':slots,'publication_binding_before':oldbinding,'publication_binding_proposed_after':newbinding,'publication_context_proposed_after_sha256':sha(canon(newcontext)),'source_mathematical_repair':False,'canonical_application_by_reviewer':False,'no_self_approved_root_application':True,'Lean_header_BODY_private_values_or_blind_packet_change':False,'compiler_required':False,'compiler_reason':'Only presentation attribution and its cryptographic binding/context updates change; mathematical statements, binders, formulae and Lean modules are byte unchanged. This is not a new proof review.','source67_final_reviewer_packet_seen':False,'source67_final_verdict':None,'reviewer_packet_sha256':None,'next_required':'Root applies exactly these three proposed after RAW files with before-pin guards, then issues a fresh final source67 packet after blind adoption. Independent whole-module source67 review remains required.','full_Exposition':False,'PURIFIED':False,'whole_paper_or_Goal_claim':False,'closed_repo66_and_primary_header67_writes':False,'canonical_Git_ledger_writes':False}
write('decision.json',decision);write('complete-RAW-decision.json',decision);write('inputs.manifest.json',{'schema':'overlay67-finite-original-RAW-LF-map-v1','inputs':snapshots})
write('negative-boundaries.json',{'schema':'overlay67-negative-boundaries-v1','canonical_application':False,'compiler_started':False,'new_proof':False,'final_source67_verdict':False,'full_Exposition':False,'PURIFIED':False,'closed_scope_writes':False,'whole_history_or_ledger_copy':False,'console_observer_negative':{'tool_chunk':'e5f9c6','exit':0,'kind':'Tool console truncated the combined full-module display; full exact module snapshots retained and missing Test67 private prefix read independently in00e872.'}})
print(json.dumps({'actual_foreground_PID':pid,'verdict':decision['verdict'],'proposal_RAW_sha256':decision['proposal_RAW_sha256'],'after_binding':newbinding,'owned_input_count':len(snapshots)}))
