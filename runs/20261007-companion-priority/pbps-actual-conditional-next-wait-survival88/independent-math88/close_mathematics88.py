from pathlib import Path
import datetime, hashlib, json, re, subprocess, sys
R=Path('E:/Samplinglib');O=Path(__file__).parent;B=O.parent
P88=R/'runs/20261007-companion-priority/pbps-conditional-next-wait-preread88'
M=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualConditionalNextWaitSurvival.lean'
MR='2f509ce49343d349f7a9fb21d2f7b1697c1a6de942353f6cd8ff16d522911569'
ME='/root/exact_verify77'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),raw_sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
def read(p):return json.loads(Path(p).read_text('utf8'))
def put(n,d):
 p=O/n
 with p.open('x',encoding='utf8',newline='\n') as f:json.dump(d,f,ensure_ascii=False,indent=2);f.write('\n')
 return pin(p)
def check(d):
 p=Path(d['path']);p=p if p.is_absolute() else R/p
 assert pin(p)['raw_sha256']==d['raw_sha256'],d['path']
 assert pin(p)['bytes']==d['bytes'],d['path']

assert pin(M)['raw_sha256']==MR
frozen=read(O/'input-freeze88.json')
for d in frozen['actual_inputs']:check(d)
for d in read(O/'collaborator-preservation88.json')['RAWs']:check(d)
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip()
assert head==frozen['observed_head']
for n in ['fresh-focused-build','fresh-whole-source-kernel']:
 rec=read(O/(n+'.receipt.json'));assert rec['exit_code']==0 and rec['terminal_closed']
 for k in ['source','stdout','stderr']:check(rec[k])
 if rec['probe']:check(rec['probe'])

log=(O/'fresh-whole-source-kernel.stdout.log').read_text('utf8')
ax=re.search(r'depends on axioms:\s*\[([^]]+)\]',log,re.S);assert ax
axioms=sorted(x.strip() for x in ax.group(1).split(','))
assert axioms==sorted(['propext','Classical.choice','Quot.sound'])
def marks(p):return sorted(set(x[len(p)+1:].strip() for x in log.splitlines() if x.startswith(p+' ')))
local=marks('LOCAL_PROOF_CONSTANT');external=marks('EXTERNAL_ASTIS_DEPENDENCY')
trans=marks('TRANSITIVE_ASTIS_CONSTANT');generic=marks('GENERIC_DEPENDENCY')
le=marks('LOCAL_EDGE');te=marks('TRANSITIVE_ASTIS_EDGE')
assert not marks('LOCAL_NO_VALUE') and not marks('PROJECT_NO_VALUE')
public=[n for n in external if not n.startswith('_private.')]
expected=sorted([
 'AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteHistoryTailLaw.actual_finite_history_tail_law',
 'AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHazardClock.actual_integrated_hazard_clock_laws',
 'AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws'])
assert public==expected
assert len(local)==10 and len(external)==12 and len(trans)==58
kernel=put('kernel-dependency-summary88.json',dict(status='ACCEPTED_ELABORATED_TYPE_AND_VALUE_ASTIS_CLOSURE',reviewer_id=ME,module=pin(M),probe=pin(O/'FreshWholeSourceKernelClosure88.lean'),native_log=pin(O/'fresh-whole-source-kernel.stdout.log'),standard_axioms_only=True,axioms=axioms,local_proof_constant_count=len(local),local_proof_constants=local,immediate_ASTIS_dependency_count=len(external),immediate_ASTIS_dependencies=external,immediate_public_theorem_parents=public,immediate_private_type_or_proof_constants=len(external)-len(public),transitive_ASTIS_constant_count=len(trans),transitive_ASTIS_constants=trans,unique_owned_edges=le,unique_transitive_ASTIS_edges=te,unique_owned_edge_count=len(le),unique_transitive_ASTIS_edge_count=len(te),generic_immediate_constant_count=len(generic),generic_immediate_constants=generic,method='Traverse both elaborated ConstantInfo.type and actual value, including generated match and proof constants. Recurse through all ASTIS constants. Generic direct dependencies of owned constants recorded, not recursive enumeration of Mathlib internals.',native_private_name_scope='Fresh exact source copy has reviewer-module private names; its full source prefix is byte-identical to production. Public anchor and imported-parent identities are unchanged.',mathematical_vs_kernel_scope='Only P probability and coordinate law of UnitExp are used mathematically here; its entire theorem proof, including SLLN, remains in the kernel constant closure. This supplies no new all-time/nonexplosion/source credit.'))
bindings=[]
for n in trans:
 tokens=n[n.find('AutoSamplingTheory.'):].split('.');hits=[]
 for k in range(2,len(tokens)+1):
  p=R.joinpath(*tokens[:k]).with_suffix('.lean')
  if p.is_file():hits.append(p)
 assert hits,n
 bindings.append(dict(constant=n,source=pin(hits[-1])))
sourcepins={b['source']['path']:b['source'] for b in bindings}
source_binding=put('transitive-kernel-source-binding88.json',dict(status='ALL_TRANSITIVE_PROJECT_CONSTANTS_BOUND_TO_EXISTING_CURRENT_SOURCE',module=pin(M),bindings=bindings,distinct_project_source_files=list(sourcepins.values()),source_file_count=len(sourcepins),compiled_parent_scope='Current target source freshly elaborated. Imported parents exercised by fresh pinned lake build and reused exact-hash prior verified parents. Source hashes bind the actual elaborated project closure; no parent mathematical proof is reproved by this review.'))

sys.path.insert(0,str(R/'tools'))
import astis
hits=astis.forbidden_pattern_hits();assert not hits,hits
fake=put('fake-closure-scan88.json',dict(status='PASS',utc=now(),reviewer_id=ME,module=pin(M),scanner=pin(R/'tools/astis.py'),method='tools.astis.forbidden_pattern_hits() repository Lean scan plus actual fresh public-anchor axiom check',hits=hits,standard_axioms_only=True,axioms=axioms))

src=M.read_text('utf8');header=(P88/'header88.proposed.lean').read_text('utf8')
seal=read(B/'root.statement-seal88.json')
literal=seal['expanded_literal_Prop'];assert literal in src
header_literal=header.split('private def ',1)[1].split('\n#check',1)[0].rstrip()
assert literal.rstrip()==header_literal
decl=src.split('theorem actual_conditional_next_wait_survival',1)[1]
body=decl.split(':= by\n',1)[1]
canonical=lambda s:'\n'.join(x.strip() for x in s.strip().splitlines())
literal_defs=literal.split('    let c',1)[1].split('\n    ∀ y xRef',1)[0]
body_defs=body.split('  let c',1)[1].split('\n  change',1)[0]
assert canonical(literal_defs)==canonical(body_defs)
bind_private=literal.split('    {E : Type*}',1)[1].split(' : Prop :=',1)[0]
bind_public=decl.split('    {E : Type*}',1)[1].split(' :\n    actual_conditional',1)[0]
assert bind_private==bind_public
prior_defs=read(P88/'header-math88/definition-readback88.json')
statement_audit=put('statement-definition-audit88.json',dict(status='SEALED_PRIVATE_PROP_PUBLIC_BINDERS_AND_BODY_LITERAL_DEFINITIONS_IDENTICAL',module=pin(M),header=pin(P88/'header88.proposed.lean'),seal=pin(B/'root.statement-seal88.json'),expanded_literal_Prop_byte_substring=True,header_private_Prop_identical=True,six_analytic_binders_public_and_private_identical=True,thirteen_literal_definitions=prior_defs['thirteen_literal_definitions'],BODY_repeated_literal_definitions_identical_after_indentation_only=True,eleven_actual87_definitions_reused=prior_defs['exact_eleven_shared87_definitions'],prior_definition_readback=pin(P88/'header-math88/definition-readback88.json'),no_extra_provider_premises=True,observable_guard='waitObs(dead,e)=0 is a proof-only measurable observable; hwaitEq uses u>=0 to make u<0 false. Public liveSurvival dead branch remains False and weight dead branch remains0. No stopped phase/wait/process transition added.',test_class='Measurable d and MeasurableSet A restrict duration functions and history events. They are not analytic/probability/regularity provider hypotheses.',index_association='Fin(n+1) last indexn equals actual recordn; full raw tail Y(w)(k)=w(n+k), so next clock is Y(w)(0)=w(n). Lambda joint tuple uses ((y,ref),phase),time; tau uses (y,ref),(phase,threshold), with explicit compositions matching each parent type.'))

lesson=R/'website/content/declaration_lessons/pbps-actual-conditional-next-wait-survival.json'
pub=R/'website/content/publications/pbps-actual-conditional-next-wait-survival.json'
pf=read(B/'publication-freeze88.json')
assert pf['module']==pin(M)
for p in [lesson,pub]:assert pin(p) in pf['inputs']
assert lesson.read_bytes()==(O/'lesson88.original.exactraw.json').read_bytes()
assert pub.read_bytes()==(O/'publication88.original.exactraw.json').read_bytes()
u=read(lesson)['units'][0];p=read(pub)['items'][0]
assert u['statement']==u['lean_statement']==p['statement']
assert u['assumptions']==p['assumptions']
assert sorted(u['astis_dependencies'])==expected
assert len(u['steps'])==5
lines=M.read_bytes().splitlines(keepends=True);regions=[];formulas=[]
for i,s in enumerate(u['steps']):
 rg=s['lean_source_region'];a,z=rg['start_line'],rg['end_line']
 b=b''.join(lines[a-1:z]);assert rg['source_raw_sha256']==MR
 assert hashlib.sha256(b).hexdigest()==rg['exact_code_raw_sha256']
 assert b.decode('utf8')==s['lean']
 if i:assert a==regions[-1]['end_line']+1
 regions.append(dict(step=i+1,**rg))
 formulas.append(dict(step=i+1,title=s['title'],formula=s['formula'],decoded_backslash_run_lengths=[len(m.group()) for m in re.finditer(r'\\+',s['formula'])],text_matches_contiguous_BODY=True))
assert regions[0]['start_line']==97 and regions[-1]['end_line']==302
assert '  classical\n'==lines[96].decode()
assert lines[301].decode().strip()=='lintegral_indicator hA weight'
assert all(all(n==1 for n in f['decoded_backslash_run_lengths']) for f in formulas)
exposition=put('whole-exposition-review88.json',dict(status='ACCEPTED_COMPLETE_CURRENT_STATEMENT_ASSUMPTIONS_AND_FIVE_EXHAUSTIVE_FORMULA_BODY_REGIONS',reviewer_id=ME,module=pin(M),draft_lesson=pin(lesson),draft_publication=pin(pub),publication_freeze=pin(B/'publication-freeze88.json'),publication_binding_sha256=pf['publication_binding_sha256'],immutable_original_lesson=pin(O/'lesson88.original.exactraw.json'),immutable_original_publication=pin(O/'publication88.original.exactraw.json'),exact_contiguous_BODY_regions=regions,entire_public_BODY_covered=True,statement_private_Prop_all_six_hypotheses_thirteen_definitions_complete=True,statement_and_assumptions_equal_between_canonical_views=True,formula_reviews=formulas,step_reviews=[
 'Step1 repeats actual definitions and changes to exact sealed target, then consumes three compiled public parents. It already establishes joint law before any conditioning argument; formula Y_n(w)_0=w_n matches raw coordinate association.',
 'Step2 establishes measurability of the guarded event by measurable sum/product distributivity and strict order comparison. Zero on stopped records is explicitly a proof-only observable, never a source wait or post-stop process.',
 'Step3 separately derives measurable exponential weight and <=1 using nonnegative hazard, including stopped zero and arbitrary abstract histories. No future conditional identity is stated prematurely.',
 'Step4 evaluates every fixed-history fiber via exact coordinate0 Exp1 law and probability-preserving hitting-time pushforward. Ioi includes infinity. Finite probability converts measureReal back to ENNReal without loss. It is pointwise in all histories, not AE substitution.',
 'Step5 uses the already Borel C event, actual joint history/tail pushforward, product section formula, pointwise fiber identity, then indicator/restricted-lintegral equality. No normalization by history event mass.'],source_attribution='A1 clock construction/conditional survival implicit in A7 and A2 measurability are attributed; history-dependent unnormalized product integration is explicitly ASTIS source-implicit completion, not quoted as a standalone source theorem.',boundaries='Deterministic event depth only. Null A, n0, rank0, zero rates and live infinite waits included. No random-depth/physical-time residual restart, conditional density/fullA7/reversal/invariance/operator/cost/main/composition claim. Draft pending purification metadata is not treated as completed purification.',required_repairs=[],no_final_source_or_decoder_verdict_read=True))

topology=read(P88/'independent-source-first88/source-proof-slice88.native.json')
assert len(topology['nodes'])==9 and len(topology['edges'])==10
graph_use=put('source-ingredient-consumption88.json',dict(status='BOUNDED_SOURCE_IMPLICIT_SURVIVAL_INGREDIENTS_ACTUALLY_CONSUMED_NO_GLOBAL_CLOSURE',module=pin(M),source_slice=pin(P88/'independent-source-first88/source-proof-slice88.native.json'),source_coverage=pin(P88/'independent-source-first88/source-coverage88.native.json'),prior_independent_topology=pin(P88/'header-math88/topology-review88.json'),source_graph_not_inferred_from_BODY=True,proof_consumption=[
 {'source_nodes':['S87-I1','S87-I2','S87-I3'],'BODY':'hH,hY,hjoint from actual87 internally. Existing76 recursion and iid-input independence are genuine ancestors.'},
 {'source_nodes':['S88-A1'],'BODY':'hLambdaTyped/hTauTyped from actual75, nonnegative Lambda for bound. Joint event/weight measurability constructed before product sections.'},
 {'source_nodes':['S88-A2'],'BODY':'Strict survival endpoint is internally proved by actual75 and consumed through its exact hSurv law. Current proof need not rederive hcross directly.'},
 {'source_nodes':['S88-P1'],'BODY':'actual87 full unused-tail joint product and UnitExp actual coordinate0 law; last history includes only consumed coordinates.'},
 {'source_nodes':['S88-P2'],'BODY':'hfiber is pointwise in every fixed history; measurable hC and Measure.prod_apply integrate against actual joint product.'},
 {'source_nodes':['S87-I4'],'BODY':'All four target clauses derived for every admissible d,A, without normalization.'}],AND_OR='Existing local conjunctive route preserved; global OR normalization routes unchanged. No requirement that individual edges suffice alone.',remaining_OPEN=['S87-I5','full G86-11','conditional finite-event density','ordered-time iteration','final factor/path-law assembly/fullA7','physical-time restart/memorylessness/temporal Markov','reversal/invariance','all-L2/Jensen/density','main/composition/fullpaper/Goal'],not_final_source_roundtrip_acceptance=True))

math=put('whole-mathematics-review88.json',dict(status='ACCEPTED_INDEPENDENT_WHOLE_BODY_MATHEMATICS_ONLY',reviewer_id=ME,observed_head=head,module=pin(M),statement_audit=statement_audit,kernel=kernel,source_bindings=source_binding,fake_closure_scan=fake,exposition=exposition,source_ingredient_consumption=graph_use,derivation=[
 'Retain all13 actual literal definitions and all6 analytic assumptions. Parent actual75 internally supplies joint measurable hazard/hitting time and fixed-state strict survival; actual87 internally supplies generated-history measurability and full unused-tail product law; UnitExp internally supplies P probability and exact raw-coordinate laws.',
 'On D times real clocks define measurable waitObs by live hitting time and dead zero, using sum-product Borel equivalence. For every nonnegative duration, dead zero yields false strict comparison, proving pointwise equality to public liveSurvival. This does not alter stopped recursion.',
 'Compose waitObs with last-record, measurable d and tail coordinate0, then use Borel strict comparison to derive the full joint event B. Construct the branchwise exponential weight and prove Borel and <=1 for all histories from nonnegative actual Lambda.',
 'Fix any history. Dead fiber is empty. For a live phase, raw coordinate0 has Exp1 law; measurable clipped hitting-time pushforward is the actual75 probability law. Its Ioi duration real probability equals exp(-Lambda); ofReal_measureReal is justified by the probability instance, hence exact ENNReal fiber equality with infinity mass retained.',
 'For each Borel history eventA form Borel C=A-first-coordinate intersectB. Pull back under actual (H,Y); Y0=w(n) and lastH=recordn definitionally. Replace joint law by mapH(P) timesP. Product-section integration, pointwise hfiber and lintegral_indicator give the exact unnormalized target.'
 ],case_audit=[
 {'case':'n=0','checked':'H0 is deterministic initial live record, Y0 raw input0; no prior consumed coordinates. Generic proof and exact parents include this case.'},
 {'case':'A empty/null or probability1','checked':'The identity integrates over A without division; empty/null both sides0. No positive-mass condition.'},
 {'case':'already stopped','checked':'Both event and weight zero. d may read earlier records; no fictitious current phase/wait is introduced.'},
 {'case':'currently live with next wait top','checked':'Finite duration<top; Ioi on WithTop retains infinity mass. A top next wait is distinct from an already stopped current record.'},
 {'case':'duration0; raw threshold<=0','checked':'Clipping gives threshold0, crossing0 and strict survival false on exceptional clocks; actual Exp1 no mass there. Hazard0 gives live survival probability1. Total event measurability remains valid on exceptional inputs.'},
 {'case':'flat/zero hazard, zero normal, rank0','checked':'No inverse hazard, strict rate or positive dimension used. Total reflection and extended hitting-time law suffice; infinitely waiting live initial and stopped subsequent records remain valid.'},
 {'case':'arbitrary history support/unbounded d','checked':'Joint Borel hazard valid for every phase; finite d(h) with no global bound. Nonnegative finite hazard gives weight<=1 universally. No moment/integrability provider needed.'},
 {'case':'random-state measurability','checked':'Borel full event established before Fubini; fiber identity forallh is pointwise. No arbitrary correlated parameter law or fixed-parameter-AE substitution.'},
 {'case':'event depth vs physical time','checked':'n is deterministic count, d is fresh duration from nth live event. No random stopping or elapsed residual clock/Markov claim.'}],required_repairs=[],additional_assumptions_found=[],mathematical_counterexample_found=False,no_own_theorem_proof_or_canonical_edits=True,no_final_source_or_decoder_verdict_read=True))

decision=put('decision88.json',dict(status='ACCEPTED_INDEPENDENT_MATHEMATICS_ONLY',reviewer_id=ME,created_utc=now(),observed_head=head,module=pin(M),full_BODY_review=math,exposition_review=exposition,standard_axioms_only=True,axioms=axioms,focused_compile=pin(O/'fresh-focused-build.receipt.json'),fresh_complete_source_and_kernel=pin(O/'fresh-whole-source-kernel.receipt.json'),kernel_closure=kernel,source_kernel_binding=source_binding,source_ingredient_consumption=graph_use,fake_closure_scan=fake,required_repairs=[],blocking_findings=[],reviewer_input_failure='Only a guessed generic-library filename failed before any Lean process; native tool chunk9ac6dd and immutable original script/diagnosis retained, exact corrected successor script then completed. No mathematical failure or source/header repair.',collaborator_21_RAW_preserved=True,truth_boundary='Mathematical/kernel/exposition acceptance only for frozen worktree source, not exact science commit admission, source-blind decoder or final source review, VERIFIED, integration, main/reader/PURIFIED/fullA7/fullpaper/composition/Goal completion.'))

extra=[R/'tools/astis.py',R/'.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Real.lean',R/'runs/20261007-companion-priority/pbps-actual-finite-history-tail-law87/independent-math87/prepare_and_compile87.py']
inputs={d['path']:d for d in frozen['actual_inputs']}
for d in sourcepins.values():inputs[d['path']]=d
for p in extra:inputs[pin(p)['path']]=pin(p)
run=put('run-manifest88.json',dict(schema=1,reviewer_id=ME,observed_head=head,created_utc=now(),actual_inputs=list(inputs.values()),complete_frozen_module=pin(M),proof_review='Whole literal statement and entire public BODY read and mathematically audited. Existing compiled-parent signatures/source exactness reused, not re-proved.',source_scope='Only already independently reviewed source slice/coverage/topology and seal source path identities; no new final source or blind decoder verdict opened. Long primary source not republished.',publication_scope='Whole statement, assumptions, formulae and all5 exact adjacent compiled BODY regions; decoded formula backslash lengths checked.',terminal_commands=[pin(O/'fresh-focused-build.receipt.json'),pin(O/'fresh-whole-source-kernel.receipt.json')],decision=decision,kernel=kernel,exposition=exposition,failures_retained=[pin(O/'prepare_and_compile88.py'),pin(O/'reviewer-input-path-diagnosis88.json')],terminal_receipts_closed=True,no_canonical_state_change=True))
for d in inputs.values():check(d)
for d in read(O/'collaborator-preservation88.json')['RAWs']:check(d)
owned=[pin(p) for p in sorted(O.iterdir()) if p.is_file()]
closed=put('closed-RAW-manifest88.json',dict(schema=1,kind='closed-noncircular-independent-whole-mathematics88',reviewer_id=ME,created_utc=now(),observed_head=head,frozen_current_inputs=list(inputs.values()),owned_artifacts=owned,self_hash_omitted_to_avoid_cycle=True,original_publication_snapshots_retained=True,terminal_receipts_closed=True,collaborator_21_RAW_preserved=pin(O/'collaborator-preservation88.json'),no_source_or_blind_verdict_read=True,no_canonical_state_change=True,no_VERIFIED_or_Goal_credit=True))
for d in owned:check(d)
print(json.dumps(dict(decision=decision,closed_manifest=closed,run=run,kernel=kernel,exposition=exposition,source_binding=source_binding,owned_constants=len(local),immediate_project=len(external),public_parents=public,transitive_constants=len(trans),transitive_edges=len(te),generic_constants=len(generic),source_files=len(sourcepins),focused_receipt=pin(O/'fresh-focused-build.receipt.json'),whole_source_receipt=pin(O/'fresh-whole-source-kernel.receipt.json')),ensure_ascii=False))
