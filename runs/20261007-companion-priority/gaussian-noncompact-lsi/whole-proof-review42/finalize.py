import datetime,hashlib,json,pathlib,re,subprocess
ROOT=pathlib.Path('E:/Samplinglib');RUN=ROOT/'runs/20261007-companion-priority/gaussian-noncompact-lsi';OUT=RUN/'whole-proof-review42'
BASE='5e808dacffd1c97d8d0dcc01c8e92052bf180426'
def H(b):return hashlib.sha256(b).hexdigest()
def LF(b):return b.replace(b'\r\n',b'\n')
def J(p):return json.loads(p.read_text(encoding='utf-8'))
def put(n,d):
 with (OUT/n).open('xb') as f:f.write((json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode())
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=str(ROOT)).decode().strip()==BASE
a=J(OUT/'reachability.analysis.json');assert a['status']=='PASS' and not a['fake_closure_hits'] and not a['compiled_local_axiom_declarations']
bindings=J(OUT/'reviewer.math.inputs.initial.json');known={x['path'] for x in bindings}
extra=[RUN.relative_to(ROOT).as_posix()+'/math-freeze.json']+[x['path'] for x in a['reached_modules'].values()]
extra+=['.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/SetToL1.lean','.lake/packages/mathlib/Mathlib/Util/PrintSorries.lean']
for i in range(3):
 for suffix in ['.log','.status.json','.lean.snapshot']:extra.append(RUN.relative_to(ROOT).as_posix()+'/tests-build.'+str(i)+suffix)
for path in extra:
 if path in known:continue
 b=(ROOT/path).read_bytes();i=len(bindings);stem='input.%03d'%i
 for suffix,data in [('.raw.snapshot',b),('.lf.snapshot',LF(b))]:
  with (OUT/(stem+suffix)).open('xb') as f:f.write(data)
 bindings.append(dict(path=path,raw_sha256=H(b),lf_sha256=H(LF(b)),bytes=len(b),raw_snapshot=stem+'.raw.snapshot',lf_snapshot=stem+'.lf.snapshot',additional_scope='Actual compiled reachable local source token scan, bounded DCT/API definition, or preserved historical typed Test failure; not new parent theorem credit'))
 known.add(path)
for x in bindings:
 b=(ROOT/x['path']).read_bytes();assert H(b)==x['raw_sha256'] and H(LF(b))==x['lf_sha256'],x['path']
 assert (OUT/x['raw_snapshot']).read_bytes()==b and (OUT/x['lf_snapshot']).read_bytes()==LF(b)
put('inputs.json',dict(checked_working_base=BASE,frozen_original_input_count=46,total_bound_inputs=len(bindings),bindings=bindings,scope='Exact working base plus frozen uncommitted mathematical delta; no exact proof-commit/VERIFIED admission'))

api=[
 dict(file='.lake/packages/mathlib/Mathlib/Analysis/Calculus/Gradient/Basic.lean',lines=[74,83],name='_root_.gradient',role='Literal inverse complete-Hilbert Riesz map on fderiv; not a supplied representative'),
 dict(file='.lake/packages/mathlib/Mathlib/Analysis/Calculus/Gradient/Basic.lean',lines=[340,348],name='Filter.EventuallyEq.gradient_eq',role='Neighborhood equality implies actual total-gradient equality even in rank0; no Nontrivial or differentiability premise'),
 dict(file='.lake/packages/mathlib/Mathlib/Analysis/Calculus/Gradient/Basic.lean',lines=[363,376],name='gradient_fun_const\'',role='Actual function equality to zero used by zero/signed constant Tests'),
 dict(file='.lake/packages/mathlib/Mathlib/Analysis/Calculus/FDeriv/Mul.lean',lines=[260,268],name='fderiv_fun_mul',role='Product derivative with actual differentiability inputs; inverse real Riesz map is linear'),
 dict(file='.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/Dual.lean',lines=[128,139],name='InnerProductSpace.toDual',role='Complete-space linear isometry equivalence; inverse preserves norm and scalar/additive operations'),
 dict(file='.lake/packages/mathlib/Mathlib/Analysis/SpecialFunctions/Log/NegMulLog.lean',lines=[174,185],name='Real.negMulLog_mul',role='Zero-aware product identity; no positive a or q/log division premise'),
 dict(file='.lake/packages/mathlib/Mathlib/Analysis/SpecialFunctions/Log/NegMulLog.lean',lines=[33,64],name='Real.self_sub_one_le_mul_log/Real.continuous_mul_log/Real.Continuous.mul_log',role='Uniform entropy domination and continuity including mass zero'),
 dict(file='.lake/packages/mathlib/Mathlib/MeasureTheory/Function/L2Space.lean',lines=[42,55],name='MeasureTheory.MemLp.integrable_sq/memLp_two_iff_integrable_sq_norm',role='Actual q=f² and norm-gradient² L1 from genuine MemLp2'),
 dict(file='.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/DominatedConvergence.lean',lines=[54,65],name='MeasureTheory.tendsto_integral_of_dominated_convergence',role='Actual Bochner DCT with measurable approximants, integrable dominator, AE bound and AE pointwise convergence'),
 dict(file='.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/SetToL1.lean',lines=[1252,1276],name='MeasureTheory.tendsto_setToFun_of_dominated_convergence',role='Internally derives approximant fs_int via bound_integrable.mono\' and limit f_int; real complete codomain avoids totalized fallback'),
 dict(file='.lake/packages/mathlib/Mathlib/Topology/Algebra/Support.lean',lines=[479,482],name='HasCompactSupport.mul_right',role='Actual cutoff support yields compact approximant support without support certificate binder'),
 dict(file='.lake/packages/mathlib/Mathlib/Topology/Order/OrderClosed.lean',lines=[472,474],name='le_of_tendsto_of_tendsto',role='Closed real order comparison preserves exact coefficient2'),
 dict(file='AutoSamplingTheory/TechnicalLemmas/Analysis/Calculus/Cutoff.lean',lines=[231,292],name='radialSmoothCutoff_fderiv_bound',role='Genuine existing parent chooses C>0 before every positive R, boundC/R; origin branch plateau avoids norm differentiation at0'),
 dict(file='AutoSamplingTheory/TechnicalLemmas/Analysis/Calculus/Gradient.lean',lines=[107,119],name='continuous_gradient_of_contDiff_one',role='C1 actual gradient continuity gives AE strongly measurable squared energy'),
 dict(file='AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/GaussianCompactHilbertLogSobolev.lean',lines=[44,112],name='compact_stdGaussian_logSobolev',role='Actual stdGaussian finite-Hilbert law, true three L1 outputs and constant2; internally basis law map/Parseval; sole public functional-inequality parent'),
 dict(file='AutoSamplingTheory/ExampleCases/SmoothedPicardHMC/StandardizedRGOSqrtDensity.lean',lines=[22,53],name='standardized_rgo_sqrt_density_domain',role='Test consumes actual uncut f, same produced stationaryp, positiveZ, q=f², C2/fL2/gradL2 and qlogqL1; no supplied source result certificate')]
for x in api:
 b=(ROOT/x['file']).read_bytes();x.update(raw_sha256=H(b),lf_sha256=H(LF(b)))
put('api-evidence.json',api)

failures=[]
for i,diagnosis in [(0,'Unknown API memLp_zero; corrected actual API MemLp.zero/gradient_fun_const\'.'),(1,'Partial-gradient simplification under MemLp did not eta-expand to the actual function identity.'),(2,'Manual constant fderiv simplification left genuine pointwise-zero goals; existing gradient_fun_const\' is the correct function API.')]:
 st=J(RUN/('tests-build.%d.status.json'%i));assert st['exit_code']==1
 log=(RUN/('tests-build.%d.log'%i)).read_text(encoding='utf-8')
 failures.append(dict(label='tests-build.%d'%i,exit_code=1,typed_class='API_OR_ELABORATION_MISMATCH_NOT_MATHEMATICAL_STATEMENT_FAILURE',diagnosis=diagnosis,actual_errors=[l for l in log.splitlines() if l.startswith('error:')],preserved_exact_raw_LF_inputs=True,not_success_evidence=True))
assert J(RUN/'tests-build.3.status.json')['exit_code']==0
put('preserved-failures.json',dict(root_Test_failures=failures,reviewer_tool_failure=dict(class_='COUNT_GUARD_CLASSIFICATION',detail='Initial source-private count guard also counted one generated abel proof helper. Five substantive source private theorems plus one generated helper are now explicitly distinguished; compiled rows/log unchanged.',Lean_or_mathematical_failure=False),all_fresh_compiler_attempts_pass=True,no_discarded_compiler_failure=True))
for label in ['focused','direct','reachability']:assert J(OUT/(label+'.status.json'))['exit_code']==0
public=next(x for x in a['compiled_rows'] if x['name'].endswith('.GaussianLogSobolev.gaussian_logSobolev_of_contDiff'))
allprivate=[x['name'] for x in a['compiled_rows'] if x['name'].startswith('_private.') and '.GaussianLogSobolev.' in x['name']]
generated=[x for x in allprivate if x not in a['all5_new_private_providers_reachable']]
assert len(generated)==1 and generated[0].endswith('._abel_1_1')
checks=dict(status='PASS_SCOPED_WHOLE_MATHEMATICS',frozen46_raw_LF_reverified=True,all_bound_input_raw_LF_reverified=True,exact_sealed691_LF_signature=True,production_raw_sha256=bindings[0]['raw_sha256'],Tests_raw_sha256=bindings[1]['raw_sha256'],public_declarations=1,source_private_providers=5,all5_source_private_providers_reachable=True,generated_arithmetic_helpers=generated,compiled_reachable_ASTIS_Test_constants=a['compiled_reachable_ASTIS_Test_constants'],compiled_reachable_local_modules=a['compiled_reachable_source_modules'],fake_closure_hits=[],compiled_local_axioms=[],fresh_focused_exit=0,fresh_direct_exit=0,fresh_reachability_exit=0,standard3_sets=a['standard_axioms'],rank0_specialization_typecheck_pass=True,root_tests_build3_pass_is_historical_only=True,no_extra_public_assumptions=True,no_supplied_limit_or_cutoff_or_LSI_certificate=True,no_totalized_integral_closure=True,no_canonical_RN_pointwise_gradient_inference=True,compiled_public_direct_ASTIS_constants=public['direct_local_constants'])
put('checks.json',checks)
review=dict(schema_version=1,status='accepted-scoped',verdict='ACCEPTED_SCOPED_WHOLE_MATHEMATICAL_PROOF',actor='gaussian_domain_preproof_reviewer_29',formalizer='companion_root_20261005',sourcegraph_creator='gaussian_noncompact_preread_42',advance_id='ASTIS-SA-20261007-GaussianLogSobolev',checked_working_base=BASE,checked_scope='Frozen working production/Test mathematical delta,46 original raw/LF inputs and bounded actual compiled reachable parents/APIs; not exact proofcommit/VERIFIED or source-blind/source-fidelity admission',blockers=[],input_manifest='inputs.json',counts=checks,complete_new_proof_audit=[
 dict(provider='entropy_dilation_bound',finding='Real.negMulLog_mul gives exact Phi(aq)=aPhi(q)+qPhi(a) for zeros as well. a in[0,1] and q>=0 produce absPhi(a)<=1 and genuine entropy dominator absPhi(q)+q. f may be signed because q=f².'),
 dict(provider='gradient_mul',finding='Differentiability of both actual factors is used in fderiv_fun_mul. Literal gradient is inverse real complete-Hilbert Riesz isometry; map_add/map_smul derive actual gradient product internally, without a supplied representative.'),
 dict(provider='cutoff_energy_bound',finding='C>=0 and R>=1 imply actual normgradchi<=C/R<=C. Cutoff range[0,1] and triangle/squared Young bound derive2G²+2C²f². All signs preserved; no hidden positivity of f or third derivative.'),
 dict(provider='cutoff_gradient_eventually_eq',finding='R_n=n+1 eventually exceeds normx+1. On a genuine unit neighborhood chi=1, so actual functions equal; EventuallyEq.gradient_eq gives actual gradient equality. It requires no Nontrivial carrier and handles rank0.'),
 dict(provider='cutoff_integral_limits',finding='Actual C2 approximants are internally produced. MemLp2 gives real q/energy L1. Three DCT invocations have actual AE strongly measurable observers, integrable dominators q / absPhi(q)+q /2G²+2C²q, AE bounds and actual pointwise convergence. Underlying DCT explicitly derives approximant and limit L1, avoiding totalized fallback.'),
 dict(provider='gaussian_logSobolev_of_contDiff',finding='Actual compact41 consumes internally derived C2/support of every chi_Rn*f. Three integral limits, continuous Phi including mass0, scalar2 multiplication and closed-order comparison preserve coefficient2. Public header is byte-exact691LF seal; no extra assumptions or desired conclusion certificates.')],Tests_audit=[
 dict(name='zero_arbitrary_hilbert',finding='Calls actual public LSI with zero C2/MemLp/gradient/Phi domains; actual constant gradient identity. Every finite Hilbert including rank0 is admitted.'),
 dict(name='negative_constant_arbitrary_hilbert',finding='Noncompact signed constant -2 has actual Gaussian mass4, genuine finite L2/entropy domain and zero gradient. No positive f/mass normalization assumption; rank0 specialization also elaborated freshly.'),
 dict(name='actual_posterior_noncompact_lsi',finding='Unit specializes actual32 source theorem with V curvature and eta>0. It selects the same actual producedp and stationary equation, uncut f=exp(-rho/2)/sqrtZ. Actual32 supplies C2/fL2/gradL2 and qlogqL1; pointwise f²=q legitimately rewrites Phi(f²) to Phi(q). No fitted/cutoff/fictional consumer or external domain certificate; distinct33 selector equality is not inferred.')],parent_and_API_boundary='Existing compact41 is the genuine public inequality parent; Cutoff/Gradient and actual32 are real reused local producers. Actual reachable closure and standard3 axioms checked freshly. Old parent source bodies scanned for fake closure and bounded actual definitions inspected; no new old-parent mathematical/theorem credit.',source_history='Previously independent42 primary-before-graph/topology and root representation overlay review disclosed; graph creator distinct. Whole-math role is not blind and is independent of root formalizer. Source admission/seals supply immutable provenance only, not correctness evidence for the new proof. No anonymous decoder/source-fidelity verdict read.',sourcegraph_accounting='Repaired topology has720 actual source-use occurrences:331 asserted,352 unelaborated,37 opaque. Historical331 subset metadata error is preserved with exact correction; it is not reused as total.',conceptual_mirror_audit=dict(status='none-found',scope='Bounded new cutoff/domain passage and actual same-Gaussian posterior consumer. The mechanism is a literal approximation/gradient/entropy proof within the same measure and function class; no additional cross-domain weaker transport candidate identified.'),remaining_truth_boundary=['No independent exactcommit/VERIFIED transition by reviewer','Full weak-W12/density/weak representative extension remains open','Coherent33 p32=p33 canonicalKL/Fisher comparison and half-Fisher consumer remain later edges','GaussianT2, coupling/metric/second-moment adapters and FIRST4.6 W2/bias remain open','Paper main/error/work/cost/composition and fullreader/PURIFIED remain open'],all_real_compiler_attempts='Three sequential fresh foreground checks exit0; terminal compiler lease CLOSED. Root tests0/1/2 failures preserved, tests3 only historical success evidence.',compiler_environment=dict(LEAN_NUM_THREADS='2',ELAN_TOOLCHAIN='leanprover/lean4:v4.33.0',PYTHONUTF8='1'),all_leases='CLOSED at completion',canonical_or_production_edits=False,self_VERIFIED_transition=False)
put('math.review.json',review)
with (OUT/'reviewer.math.review.json').open('xb') as f:f.write((OUT/'math.review.json').read_bytes())
lp=OUT/'reviewer.math.lease.json';l=J(lp);assert l['compiler_lease']=='CLOSED' and l['compiler_exit_code']==0
l.update(status='CLOSED',read_lease='CLOSED',write_lease='CLOSED',Python_lease='CLOSED',closed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),outcome=review['verdict']);lp.write_bytes((json.dumps(l,indent=2)+'\n').encode());put('reviewer.math.lease.closed.raw.snapshot.json',l)
art=[]
for n in ['math.review.json','reviewer.math.review.json','inputs.json','checks.json','api-evidence.json','preserved-failures.json','reachability.analysis.json','focused.log','focused.status.json','direct.log','direct.status.json','reachability.log','reachability.status.json','ReachabilityProbe.lean','fresh-check.py','analyze.py','finalize.py','reviewer.math.lease.closed.raw.snapshot.json','compiler.lease.closed.raw.snapshot.json']:
 b=(OUT/n).read_bytes();art.append(dict(path=n,raw_sha256=H(b),lf_sha256=H(LF(b))))
rh=H(json.dumps(art,sort_keys=True,separators=(',',':')).encode());put('run.json',dict(status='CLOSED',checked_working_base=BASE,run_sha256=rh,artifacts=art,total_bound_inputs=len(bindings),all_leases_CLOSED=True))
print(json.dumps(dict(verdict=review['verdict'],review_raw_sha256=H((OUT/'math.review.json').read_bytes()),run_sha256=rh,total_bound_inputs=len(bindings),original_math_freeze_inputs=46,all_leases='CLOSED')))
