"""Close independent prospective whole-header review, not a theorem proof."""
from pathlib import Path
import hashlib,json,re,subprocess
from datetime import datetime,timezone
R=Path('E:/Samplinglib');D=R/'runs/20261007-companion-priority/pbps-conditional-next-wait-density-preread89/header-math89'
def pin(p):
 p=Path(p);b=p.read_bytes();return {'path':p.as_posix(),'raw_sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def load(p):return json.loads(Path(p).read_text(encoding='utf8'))
def out(name,v):
 p=D/name;assert not p.exists(),p
 with p.open('x',encoding='utf8',newline='\n') as f:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
 return pin(p)
def digest(t):return hashlib.sha256(t.encode('utf8')).hexdigest()
now=datetime.now(timezone.utc).isoformat();head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip()
assert head=='7c108c3181cee58bb9305445f903c5f71efda9c5'
hpath=D.parent/'header89.proposed.lean';h=hpath.read_text(encoding='utf8')
assert pin(hpath)['raw_sha256']=='47bb14ee9e720d22ddefa4645860d1fcd6a984cfaf2f64085e41eea1ccc9a696'
parent_rel=[
 'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteFirstEventLaw.lean',
 'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteHistoryTailLaw.lean',
 'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHazardClock.lean',
 'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteJumpRecursion.lean',
 'AutoSamplingTheory/TechnicalLemmas/Probability/UnitExponentialProduct.lean']
parents=[R/p for p in parent_rel]
p86,p87,p75,p76,p77=[p.read_text(encoding='utf8') for p in parents]
def bind(t):return t[t.index('    {E :'):t.index(' : Prop :=')]
assert bind(h)==bind(p86)==bind(p87)==bind(p75)==bind(p76)
common=h[h.index('    let c :'):h.index('    let waitObs')]
assert common==p87[p87.index('    let c :'):p87.index('    let tail')]
def block(t,name):
 s=t[t.index('    let '+name+' :'):]
 return s[:s.index('\n    let ',1)]
for name in ['c','Φ','S','rate','Λ','τ']:assert block(h,name)==block(p86,name)
for name in ['c','Φ','S','rate','Λ','τ','next','record']:assert block(h,name)==block(p76,name)
for name in ['c','Φ','rate','Λ','τ']:assert block(h,name)==block(p75,name)
for forbidden in [r'\bsorry\b',r'\badmit\b',r'\baxiom\b',r'Prop\s*:=\s*True',r':=\s*trivial']:
 assert not re.search(forbidden,h),forbidden
assert h.count('private def actual_conditional_next_wait_density_statement')==1
assert not re.search(r'^\s*(?:private\s+)?theorem\b',h,re.M)
receipt=load(D/'header89.v2-current.whole-typecheck.receipt.json')
neg=load(D/'header89.v1-negative.whole-typecheck.receipt.json')
assert receipt['exit_code']==0 and neg['exit_code']!=0
for rr in (receipt,neg):
 for x in rr['raw_inputs']+[rr['native_log']]:
  pp=pin(x['path']);assert pp['raw_sha256']==x['raw_sha256'] and pp['bytes']==x['bytes']
mathlib=R/'.lake/packages/mathlib'
mathlib_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=mathlib,text=True).strip()
assert mathlib_commit=='db584cd6d46c92f209a44c0f1c829460d327499d'
source_rel=[
 'Mathlib/Probability/Kernel/WithDensity.lean',
 'Mathlib/Probability/Kernel/Defs.lean',
 'Mathlib/MeasureTheory/Measure/WithDensity.lean',
 'Mathlib/MeasureTheory/Measure/Restrict.lean',
 'Mathlib/MeasureTheory/Measure/Prod.lean',
 'Mathlib/MeasureTheory/Integral/Lebesgue/Map.lean',
 'Mathlib/MeasureTheory/Constructions/BorelSpace/WithTop.lean',
 'Mathlib/MeasureTheory/Measure/Map.lean']
oleans=[R/'.lake/build/lib/lean'/p.replace('.lean','.olean') for p in parent_rel]
assert all(p.exists() for p in oleans)
defs=re.findall(r'^    let (\S+)',h,re.M)
assert defs==['c','Φ','S','rate','Λ','τ','next','record','P','ε','history','waitObs','timeObs','density']
semantics={
 'c':'Actual center y-eta gradV(reference).',
 'Φ':'Literal real-time harmonic flow with sqrt(eta) scaling, all real times.',
 'S':'Literal total momentum reflection; denominator zero in Lean gives identity when normal is zero.',
 'rate':'sqrt(eta) times positive part of actual inner product; nonnegative continuous along flow.',
 'Λ':'Actual integral of rate from0 to finite NNReal t, real Lebesgue interval integral.',
 'τ':'Actual >= threshold hittingAfter at0, flattened tuple ((y,reference),state,e) with product projections a.1.1/a.1.2/a.2.1/a.2.2.',
 'next':'Stopped absorbs; live infinite wait gives stopped; otherwise finite time plus wait and actual postbounce state.',
 'record':'Nat.rec live(0,z0); depth k step consumes e k.',
 'P':'Concrete countable raw real Exp1 product, not a supplied probability law.',
 'ε':'Real.toNNReal raw coordinate; declared total null-set extension.',
 'history':'Complete Fin(n+1) vector of actual records0..n; consumes only first n coordinates.',
 'waitObs':'Live actual tau at clipped raw threshold; stopped extension0. This observable does not invent a stopped phase/wait.',
 'timeObs':'WithTop.untopD0 finite extraction then real coercion; infinity defaults0 only as a total observable, excluded from B.',
 'density':'Finite ENNReal.ofReal of actual free-arc rate times exp(-actual hazard); stopped0. Negative real times are allowed in the total definition but eliminated by D.'}
readback=out('header89.definition-readback.json',{
 'schema':1,'reviewer_id':'/root/exact_verify77','exact_header':pin(hpath),
 'six_binders_LF_text_sha256':digest(bind(h)), 'six_binders_LF_bytes':len(bind(h).encode()),
 'six_binders_exact_LF_identity_parents':[pin(p) for p in parents[:4]],
 'six_conditions':['0<alpha','alpha<=beta','V globally C2','global lower AND upper Hessian bounds','0<eta','beta*eta<=1'],
 'same_eleven_actual_definitions_as87_LF_sha256':digest(common),'same_eleven_actual_definitions_as87_LF_bytes':len(common.encode()),
 'newline_policy':'Only read_text CRLF/LF decoding for region comparison; original full-file RAWs pinned independently. Region digests are not full-file digests.',
 'literal_definitions':[{'name':n,'semantics':semantics[n],'identity':('Exact eleven-definition LF text prefix of actual87' if j<11 else 'New literal total observable/density, independently audited')} for j,n in enumerate(defs)],
 'dynamics_exact_identity_with86':['c','Φ','S','rate','Λ','τ'],
 'recursion_exact_identity_with76':['c','Φ','S','rate','Λ','τ','next','record'],
 'hazard_exact_identity_with75':['c','Φ','rate','Λ','τ'],
 'local_lets':{'Hist':'Fin(n+1) vector of tagged finite record or stopped','last':'Fin index n, exactly H(w)(last)=record(...,n)','H':'literal actual history','mu':'map H P','D':'0<s<d(h) guarded density, finite nonnegative jointly Borel','K':'const real Lebesgue kernel withDensity D, measurable branch explicitly asserted','B':'actual strictly positive extended wait < finite d(H), so excludes top and stopped0','X':'(H,total extracted real wait)','nu':'mu product real volume with joint density D; no arbitrary reference measure'},
 'tuple_association_checked':True,'all_original_source_binders_retained':True,'no_new_provider_binders':True})
mathematics=out('header89.mathematics.json',{
 'schema':1,'reviewer_id':'/root/exact_verify77','header':pin(hpath),'status':'ACCEPTED_PROSPECTIVE_MATHEMATICS_ONLY',
 'whole_Prop_review':[
  {'clause':'waitObs measurable','assessment':'Actual75 joint tau Borel plus clipping and Sum case split. Stopped constant0 is measurable, not a process wait claim.'},
  {'clause':'density jointly measurable and finite everywhere','assessment':'Actual flow/rate and joint hazard compose with state/time and toNNReal; exp and ofReal are Borel. Real arithmetic is finite at every finite input; stopped case0. No finite global rate bound is required.'},
  {'clause':'D jointly measurable','assessment':'Finite history evaluation at last, Borel d, real coercion and strict comparison define a Borel guard; density times its indicator. Jointness precedes kernel construction/integration.'},
  {'clause':'kernel fiber equality','assessment':'Pinned Kernel.withDensity defines a zero kernel when uncurry D is not measurable. The target explicitly asserts uncurry D measurability AND every fiber equals volume.withDensity(D h), so zero fallback cannot discharge a nonzero law.'},
  {'clause':'all histories finite subprobability kernel','assessment':'For each abstract h, stopped branch has mass0. For live last(T,z), fixed t=d(h), actual86 supplies the Ioc density measure with mass<=1. Restriction by Iio(t) yields exactly Ioo(0,t). A restriction cannot increase mass. Uniform bound1 supplies IsFiniteKernel; no global boundedness of d or realizability of h is needed.'},
  {'clause':'B measurable and X measurable','assessment':'Actual87 H/record measurability, measurable coordinate n, actual75 waitObs, Borel strict comparison with d(H), and measurable untopD0/coercion. X is measurable on whole raw sample space, including samples outside B.'},
  {'clause':'exact joint mapped restricted law','assessment':'Actual87 gives map(w->(H(w),Y_n(w)))P=mu product P and Y_n(w)0=w n. Last history coordinate is exactly record_n. For each fixed h, evaluate the parent86 strict restricted measure law using the tail coordinate0. Product measure section integration gives map X(P restrict B)=nu for every Borel joint history/time set. This is an unnormalized law, no conditional point division or simultaneous-parameter AE substitution.'},
  {'clause':'joint mass<=1','assessment':'Left side is the pushforward of a restriction of the internally probability P. Equivalently integrate K(h,univ)<=1 against probability mu. No infinite waiting mass is renormalized away.'},
  {'clause':'every jointly Borel nonnegative extended F','assessment':'F times D is jointly measurable; real Lebesgue is sigma-finite, so the parameter lintegral is measurable. Values and integrals may be infinity. Neither L1 nor boundedness is needed for nonnegative Tonelli.'},
  {'clause':'every Borel A restricted test identity','assessment':'Integrate F after restricting the mapped law by the first-coordinate history event, then use withDensity and Tonelli. B intersect preimage(H,A) matches the exact restricted sample event. Parentheses in V2 bind outer mu and inner real volume correctly. Null A is valid even when F takes infinity because null-restricted measure integrates to0.'}
 ],
 'reference_measure':'Exactly real volume, restricted via Ioc(0,d) further by Iio(d). Positive s has Real.toNNReal s=s under real coercion, so parent86 density agrees exactly. No NNReal Jacobian, scale, arbitrary time measure or endpoint-mass equivalence is used.',
 'counterexample_audit':[
  {'case':'n0','outcome':'H0 is deterministic live(0,z0), raw w0 fresh; reduces to strict parent86 law for fixed section.'},
  {'case':'A empty/null','outcome':'No positive conditioning mass; both unnormalized test integrals0.'},
  {'case':'d0','outcome':'B empty, D zero, K/nu zero; no positive duration premise.'},
  {'case':'wait exactly d','outcome':'Excluded by actual strict upper bound and D guard on both sides; no closed/strict probability identification asserted.'},
  {'case':'live infinite wait','outcome':'Top fails finite upper guard; extraction0 does not create finite density atom; missing mass retained.'},
  {'case':'already stopped','outcome':'waitObs0 fails strict positive guard and density0; no stopped source phase introduced.'},
  {'case':'rank0 or identically zero orbit hazard','outcome':'Positive Exp threshold has infinite wait, density0 and finite kernel mass0.'},
  {'case':'flat hazard or instantaneous rate0','outcome':'No strictly positive derivative/invertible hazard assumption. A zero instantaneous rate is not confused with an identically zero orbit rate.'},
  {'case':'zero/negative raw coordinate','outcome':'Clipped threshold0 has wait0, excluded from B; actual Exp1 nonpositive inputs null internally.'},
  {'case':'zero normal','outcome':'Literal total reflection gives identity and rate vanishes at that state; no discontinuity-based extra premise.'},
  {'case':'unbounded finite d across histories','outcome':'Fiberwise finite cutoffs and uniform probability mass bound suffice; no global cutoff bound.'},
  {'case':'F infinite/unbounded','outcome':'Extended nonnegative Tonelli valid; do not claim all test integrals finite or density<=1.'},
  {'case':'unrealizable abstract h','outcome':'Kernel statements depend only on its last tag/state, so still hold; actual mu weights realized histories only.'}
 ],
 'strict_new_edge':'Actual random finite-history next finite-wait joint measure and all joint nonnegative tests, beyond parent86 deterministic state law and parent87 unused-tail product. Parent88 survival is adjacent, not an AND prerequisite.',
 'source_consumer':'At fixed horizon T choose Borel d(h)=max(T-last_live_time,0); F may compose with the actual Borel finite next-record constructor to represent an ordered-time jump factor. This does not itself implement iteration or a full path functional.',
 'mathematical_derivation_or_counterexample_audit_only':True,'own_theorem_proof_implementation':False,
 'required_mathematical_repairs':[],'remaining':['Whole BODY construction/review','Independent source-blind decoder/final source review/later exact science admission','Remainder S87-I5/fullG86-11/A7 and all global process/invariance/cost/main/PURIFIED/reader/Goal obligations OPEN']})
negative=out('header89.negatives-and-syntax-review.json',{
 'schema':1,'v1_header':pin(D/'header89.v1-negative.exactraw.lean'),'v2_header':pin(D/'header89.v2-current.exactraw.lean'),
 'launcher_RAW_guard':pin(D/'header89.launcher-guard.negative.json'),
 'v1_native_receipt':pin(D/'header89.v1-negative.whole-typecheck.receipt.json'),
 'v1_native_log':pin(D/'header89.v1-negative.whole-typecheck.log'),
 'v1_diagnosis':'At line101 unparenthesized inner lintegral consumed ∂mu, requiring Hist integration for a real-time function and leaving outer Hist volume unspecified. Independent native errors are MeasureSpace Hist and real-vs-Hist integrand mismatch.',
 'exact_author_successor_delta':pin(D/'header89.syntax-successor.delta.json'),
 'current_v2_native_receipt':pin(D/'header89.v2-current.whole-typecheck.receipt.json'),
 'syntax_successor_status':'ACCEPT_EXACT_TWO_PARENTHESES_ONLY_NO_MATHEMATICAL_TARGET_CHANGE',
 'search_diagnostic':{'tool_chunk':'ca2440','exit_code':1,'cause':'Reviewer included nonexistent guessed parent path ProximalBPS/Hitting.lean in a batched rg. It was not a compiler error or mathematical repair. Correct actual parent path ActualHazardClock.lean subsequently inspected with terminal4c15c5/56ed13 EXIT0.','retained_original_command_output_in_tool_transcript':True},
 'native_failures_immutable':True})
api=out('header89.API-and-read-scope.json',{
 'schema':1,'mathlib_commit':mathlib_commit,
 'project_parent_inputs':[pin(p) for p in parents], 'compiled_parent_oleans':[pin(p) for p in oleans],
 'parent_signatures_read':[
  {'file':pin(parents[0]),'range':'private full statement lines20-83 plus public declaration lookup; no whole BODY proof replay','decl':'actual_finite_first_event_law','use':'fixed-state actual finite Ioc density measure equality/mass bound and exact real density'},
  {'file':pin(parents[1]),'range':'private full statement lines17-74 plus public declaration lookup; no whole BODY proof replay','decl':'actual_finite_history_tail_law','use':'full actual history and countable raw-tail product'},
  {'file':pin(parents[2]),'range':'private full statement through line74; initial helper signature lines76-78 visible but no helper proof read','decl':'actual_integrated_hazard_clock_laws','use':'joint actual hazard and crossing measurability, nonnegative/finite-time contracts'},
  {'file':pin(parents[3]),'range':'first95lines including complete measurable recursion and most remaining private contract; no theorem BODY read','decl':'actual_fixed_reference_finite_jump_recursion','use':'literal recursion and joint Borel maps internally reused via87'},
  {'file':pin(parents[4]),'range':'first88lines; private statement AND early existing proof (coordinate maps/Exp positivity) incidentally read by broad Get-Content. No proof replay or theorem credit. This occurred after source topology was already closed.','decl':'unit_exponential_product_laws','use':'internally probability P and actual Exp coordinate law; not a new public premise'}
 ],
 'no_claim_entire_run_parent_BODY_invisible':True,
 'source_topology_not_derived_from_any_Lean_BODY':True,
 'generic_APIs':[{'file':pin(mathlib/p),'names':names} for p,names in zip(source_rel,[
  ['Kernel.withDensity','Kernel.withDensity_of_not_measurable','Kernel.withDensity_apply','Kernel.lintegral_withDensity'],
  ['IsFiniteKernel.exists_univ_le'],['Measure.restrict_withDensity'],['Measure.restrict_restrict'],
  ['Measurable.lintegral_prod_right','lintegral_prod'],['lintegral_map'],['WithTop.measurable_untopD','Measurable.untopD'],
  ['restrict/map source filename searched; no declaration match reported for this final search']])],
 'source_only_topology_admission':pin(D/'source-topology89.decision.json'),
 'generic_API_lookup_only_no_implementation_tactics_or_proof_search':True})
decision=out('decision89.json',{
 'schema':1,'reviewer_id':'/root/exact_verify77','created_utc':now,'checked_workspace_commit':head,
 'status':'ACCEPTED_INDEPENDENT_WHOLE_HEADER_MATHEMATICS_AND_TYPE_ONLY',
 'authoritative_header':pin(hpath),'original_v1_preserved':pin(D/'header89.v1-negative.exactraw.lean'),
 'current_v2_exact_typecheck':pin(D/'header89.v2-current.whole-typecheck.receipt.json'),
 'terminal_exit_code':0,'typecheck_scope':'Complete named private literal Prop with original #check, fixed Lean4.33.0 and pinned manifest; original source copied byte-exact, not a reduced fragment or theorem placeholder.',
 'whole_statement_audit':mathematics,'definition_and_binder_readback':readback,'API_read_scope':api,
 'separate_distinct_source_topology_decision':pin(D/'source-topology89.decision.json'),
 'source_topology_closed_before_any_header_read':True,
 'syntax_successor_and_failures':negative,
 'required_repairs':[], 'additional_mathematical_or_source_hypotheses_found':[],
 'warnings':'Unused-variable warnings in a proposition definition are expected; all six original analytic proof arguments remain in the named interface.',
 'truth_boundary':'Prospective preproof header and source topology admitted only. No StatementSeal, claim, theorem BODY, proof correctness, PROVED_LOCAL, VERIFIED, stabilization, reader/main/PURIFIED/whole-paper/Goal credit is given.'})
run=out('run89.json',{
 'schema':1,'reviewer_id':'/root/exact_verify77','completed_utc':now,'checked_workspace_commit':head,
 'status':'CLOSED_INDEPENDENT_PROSPECTIVE_HEADER_AND_DISTINCT_SOURCE_TOPOLOGY_REVIEW',
 'chronology':[{'event':'Primary-only reconstruction frozen before any author89 graph/candidate read','artifact':pin(D/'source-reconstruction89.chronology.jsonl')},{'event':'Distinct source topology closed before header first read','artifact':pin(D/'source-topology89.closed-RAW-manifest.json'),'terminal_chunk':'244ad8','exit_code':0},{'event':'Whole V1 header first read','terminal_chunk':'d42173','exit_code':0},{'event':'Original compile launcher RAW guard stopped before Lean due to root successor','terminal_chunk':'1e879b','exit_code':1},{'event':'Full V1 negative then full V2 success, sequential foreground pinnedLean','launch_chunk':'7f4e44','terminal_chunk':'6dea8f','exit_code':0,'receipts':[pin(D/'header89.v1-negative.whole-typecheck.receipt.json'),pin(D/'header89.v2-current.whole-typecheck.receipt.json')]},{'event':'Parent literal-definition and six-binder identity comparison','terminal_chunk':'4ed0bf','exit_code':0}],
 'decision':decision,'no_canonical_writes':True,'owned_directory':D.as_posix(),'no_detached_or_background_ASTIS':True,
 'no_fabricated_native_reasoning_trajectory':True})
current=[hpath,D.parent/'header89.proposed.v1.exactraw.snapshot.lean',D.parent/'header89.v2.scope-correction.json',R/'lean-toolchain',R/'lake-manifest.json',R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe',R/'.astis/toolchain/lean-4.33.0-windows/bin/lean.exe']+parents+oleans+[mathlib/p for p in source_rel]
owned=[pin(p) for p in sorted(D.iterdir()) if p.is_file()]
manifest=out('closed-RAW-manifest89.json',{
 'schema':1,'reviewer_id':'/root/exact_verify77','checked_workspace_commit':head,
 'status':'CLOSED_NONCIRCULAR_PROSPECTIVE_HEADER_REVIEW_NO_PROOF_CREDIT',
 'frozen_current_inputs':[pin(p) for p in current],
 'prior_source_only_native_closure':pin(D/'source-topology89.closed-RAW-manifest.json'),
 'owned_artifacts':owned,'decision':decision,'run':run,
 'closure':'Self excluded. Original failed launcher/V1 exact bytes/logs and V2 syntax-only successor retained. Full RAW files and compiled parent oleans pinned; LF region comparison explicitly distinguished. No immutable source originals overwritten.'})
print(json.dumps({'decision':decision,'run':run,'closed_manifest':manifest,'header':pin(hpath)},ensure_ascii=False))
