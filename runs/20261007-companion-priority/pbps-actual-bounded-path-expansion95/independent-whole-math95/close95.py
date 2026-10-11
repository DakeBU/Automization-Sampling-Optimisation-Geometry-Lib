import pathlib,json,hashlib,subprocess,re
ROOT=pathlib.Path('E:/Samplinglib');OUT=pathlib.Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def save(p,x):(OUT/p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
inputs=json.loads((OUT/'inputs.native.json').read_text())
for p in ['tools/astis.py','.lake/packages/mathlib/Mathlib/MeasureTheory/Function/L1Space/Integrable.lean','.lake/packages/mathlib/Mathlib/Topology/Algebra/InfiniteSum/Order.lean']:
 b=(ROOT/p).read_bytes();inputs.append({'path':p,'raw_sha256':sha(b),'bytes':len(b)})
version=subprocess.check_output([str(ROOT/'.astis/toolchain/lean-4.33.0-windows/bin/lean.exe'),'--version'],cwd=ROOT).decode().strip()
mathlib=subprocess.check_output(['git','-C','.lake/packages/mathlib','rev-parse','HEAD'],cwd=ROOT).decode().strip()
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip()
save('runtime.native.json',{'lean':version,'mathlib_commit':mathlib,'checkout_head':head,'production_binding':'Uncommitted frozen worktree RAW; no checked science commit95 claimed.','ELAN_TOOLCHAIN_removed_for_checks':True})
for name in ['fresh-production','fresh-combined-sealed-witness']:
 assert json.loads((OUT/(name+'.receipt.native.json')).read_text())['exit_code']==0
 log=(OUT/(name+'.stdout.log')).read_text();assert 'Quot.sound]' in log and 'sorryAx' not in log
assert json.loads((OUT/'fake-closure.native.json').read_text())['status']=='PASS'
module=ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualBoundedPathExpansion.lean';assert sha(module.read_bytes())=='c3d4bcf73990d704244225ea647f44ed21fcbd339db49bf2c45f21af5b90d689'
decision={
 'status':'ACCEPTED_INDEPENDENT_WHOLE_MATHEMATICAL_AND_KERNEL_REVIEW',
 'reviewer':'/root/independent_whole_math93',
 'production':{'path':module.relative_to(ROOT).as_posix(),'raw_sha256':sha(module.read_bytes()),'declaration':'AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBoundedPathExpansion.actual_bounded_path_functional_expansion','public_theorems':1,'private_helpers':2,'private_literal_Prop_definitions':1},
 'header_raw_sha256':'2a9d3052c353ab8aab448de05a05beeadab320def15ee31b1d353abbb063d002',
 'statement_seal':'runs/20261007-companion-priority/pbps-bounded-path-expansion-preread95/root.statement-seal95.json',
 'exact_target':'Production private literal proposition equals the independently reviewed sealed Header95 body and seal expanded_literal_Prop exactly after line-ending normalization. The combined witness re-elaborates full production source and an independently named copy of Header95 and checks the public theorem against that literal target in the same fresh Lean invocation.',
 'kernel_checks':{'fresh_actual_production':'EXIT0','fresh_combined_sealed_witness':'EXIT0','axioms':['propext','Classical.choice','Quot.sound'],'repository_fake_closure_hits':0,'full_repository_Lake_build_claimed':False},
 'mathematical_findings':[
  {'region':'signed_sector, lines12-51','result':'Accept','reason':'Pushforward integrability equivalence first transports the real observable on the second coordinate through the actual joint law, then pulls it back along (K,Gamma). All maps required for integral_map and integrable_map_measure have explicit measurable proofs. The density rho is pointwise ofReal(nonnegative finite wgt), hence rho<top and rho.toReal=wgt. The withDensity Bochner integrability and integral identities therefore give exactly F(Gamma)*wgt. No finite base-measure assumption, positive density, normalized sector, law equality cancellation or unproved integrability premise is hidden. The private hi assumption is discharged by restriction of the actual globally integrable bounded observable.'},
  {'region':'signed_count_partition, lines53-65','result':'Accept','reason':'The sets {N=n} are measurable, pairwise disjoint and their countable union is all X. hasSum_integral_iUnion consumes integrability of f on that union and supplies an unconditional HasSum, not merely convergence of ordered partial sums. For real series Summable.abs is legitimate (Mathlib summable_abs_iff); hence absolute summability is derived. There is no invalid conditional-convergence-to-absolute-convergence inference.'},
  {'region':'literal statement and public binders, lines67-177','result':'Accept','reason':'Exactly the six original analytic hypotheses, original finite-dimensional/Borel ambient types, arbitrary globally bounded real coordinate-measurable F and fixed deterministic parameters/horizon. No additional density, nonexplosion, regularity, integrability, probability or process-law public binder. Private literal Prop is the full expanded formula, not a vacuous closure.'},
  {'region':'literal local dynamics and change target, lines179-303','result':'Accept','reason':'The local lets reproduce the actual stopped Exp(1)-clock recursion, strict ordered-simplex/comap measure, Fin.induction reflected states, path fold and whole-hazard incoming-rate weight. The kernel change checks definitional equality with the full literal proposition. No altered recurrence or replacement abstract process is introduced.'},
  {'region':'actual witness and bounded integrability, lines305-320','result':'Accept','reason':'The exact Z from93 is retained together with joint measurability, every raw covered-arc equality, uncovered z0 fallback and fixed-parameter AE initialization. hAll at n0 is used only to obtain path and count measurability, whose actual definitions are independent of n. UnitExponentialProduct supplies the actual probability instance; bounded measurable F then yields integrability. hM is redundant once the universal absolute bound is present, but is preserved exactly from the seal and causes no strengthening.'},
  {'region':'actual sector instantiation, lines321-347','result':'Accept','reason':'93 supplies actual joint law, history/path measurability and rho measurability.92 supplies actual K measurability. Nonnegative rate factors and exponential show wgt>=0.94 supplies rho=ofReal(wgt), with only Fin.snoc_castSucc simplifying the incoming grid indices. signed_sector is applied to P restricted to {N=n}, whose integrability comes from hi.integrableOn. No hmass or hcover is reused as an extra assumption; they remain available parent facts while the actual measurable total count partition suffices.'},
  {'region':'countable signed assembly, lines348-352','result':'Accept','reason':'signed_count_partition derives an absolutely summable real sector series from hi and hN. Each actual-sector real integral is replaced by the proven weighted-simplex integral. The output includes global integrability, every simplex integrability, sum of absolute sector integrals and the exact all-count signed expectation identity.'}
 ],
 'direct_ASTIS_dependencies':[
  {'declaration':'ActualFiniteCountPath.actual_finite_count_path_law','role':'Actual process Z, raw path semantics, measurability, count-sector joint law'},
  {'declaration':'ActualPrescribedPathDensity.actual_prescribed_path_density_rewrite','role':'Exact whole-hazard/incoming-rate rho rewrite'},
  {'declaration':'ActualOrderedPrefix.actual_ordered_prefix_law','role':'Measurable prescribed full-history map K'},
  {'declaration':'AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws','role':'Actual infinite Exp(1) product probability instance'}
 ],
 'Mathlib_ingredients':['integrable_map_measure','integral_map','integrable_withDensity_iff_integrable_smul\u0027','integral_withDensity_eq_integral_toReal_smul','hasSum_integral_iUnion','Summable.abs / summable_abs_iff','HasFiniteIntegral.of_bounded','Integrable.integrableOn','Fin.snoc_castSucc'],
 'quantifiers_and_degeneracy':[
  'The path space uses its coordinate-product measurable structure. Joint Z and Gamma measurability are inherited; no claim about the full Borel sigma algebra of an uncountable product topology or Skorokhod space is needed.',
  'The witness is globally jointly measurable, but AE initialization is separately for each fixed parameter tuple. The theorem fixes each T before applying count law93 and integrates an entire path. It does not take an uncountable intersection of coordinate-wise AE identities, or replace forall T AE with AE forall T.',
  'n0 has one empty event tuple and empty incoming product1, retaining the full terminal survival. T0 has empty positive-count simplices and the n0 one-point path;93 AE initialization gives the expected value. The proof never divides by T, event gaps, rates or sector masses.',
  'Rank0, zero rate and individual zero incoming factors are admitted. rho=ofReal(wgt) remains finite including wgt0, so withDensity conversion requires no positive-rate assumption. The reflection zero denominator remains the accepted total Lean convention.',
  'Infinite waits and absorbing records, raw zero clocks and exceptional uncovered times retain exactly93 semantics. The actual total measurable N partitions all streams;93 law already handles AE count/fallback behavior. No raw all-stream nonexplosion claim is inserted.'
 ],
 'source_boundary':'No mathematical/source objection detected at the reviewed target boundary. This is the bounded real coordinate-measurable path expansion, using the independently disclosed signed mass-partition completion of A7 assembly. The printed rate-cap/simplex-factorial route, unbounded observables, Skorokhod compatibility, restart/Markovness, invariance, hypocoercivity, paper main/composition and whole Goal are not certified by this review. Independent source reviewer still owns source fidelity and source-graph coverage.',
 'exposition_dependency_note':'Author exposition must name the two actual additional direct calls92 and UnitExponentialProduct and explain that unconditional real HasSum yields absolute summability. These are proof ingredients/dependency edges, not public assumptions.',
 'required_corrections':[],
 'retained_trials':'Initial shell brace-path parser failure recorded; no failed independent Lean trial. Linter unused-binder/letI style warnings do not affect kernel closure.',
 'publication_decoder_source_pending':True,'VERIFIED_transition_published':False,'production_modified':False,'Goal_complete':False}
save('whole-math-decision95.native.json',decision)
manifest={'status':'CLOSED_RAW_WHOLE_MATH_REVIEW95','production_raw_sha256':sha(module.read_bytes()),'inputs':inputs,'owned_evidence':[],'self_hash_intentionally_omitted':True}
for p in sorted(OUT.rglob('*')):
 if p.is_file() and p.name!='closed-RAW-whole95.native.json':
  b=p.read_bytes();manifest['owned_evidence'].append({'path':p.relative_to(ROOT).as_posix(),'raw_sha256':sha(b),'bytes':len(b)})
save('closed-RAW-whole95.native.json',manifest)
print(json.dumps({p:sha((OUT/p).read_bytes()) for p in ['whole-math-decision95.native.json','closed-RAW-whole95.native.json']},indent=2))
