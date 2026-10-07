from pathlib import Path
import json, hashlib, re, datetime

ROOT = Path('E:/Samplinglib')
OUT = ROOT / 'runs/20261007-companion-priority/gaussian-flip-energy-preread'
P = 'runs/20261007-companion-priority/'
M = '.lake/packages/mathlib/Mathlib/'
A = P + 'gaussian-functional-availability/'
def lf(b): return b.replace(b'\r\n', b'\n').replace(b'\r', b'\n')
def sha(b): return hashlib.sha256(b).hexdigest()
def emit(name, obj):
    b = (json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode()
    (OUT / name).open('xb').write(b)
    return sha(b)
inputs, regions = [], []
def pin(path, rs=(), kind='PINNED_API_SOURCE_NOT_CURRENT_COMPILER_CERTIFICATE'):
    b = (ROOT / path).read_bytes()
    idx = len(inputs)
    raw, normalized = 'input.%03d.raw.snapshot' % idx, 'input.%03d.lf.snapshot' % idx
    (OUT / raw).open('xb').write(b)
    (OUT / normalized).open('xb').write(lf(b))
    e = dict(path=path, kind=kind, raw_sha256=sha(b), lf_sha256=sha(lf(b)), bytes=len(b), raw_snapshot=raw, lf_snapshot=normalized)
    inputs.append(e)
    lines = b.splitlines(keepends=True)
    for a, z, role in rs:
        assert 1 <= a <= z <= len(lines), (path, a, z, len(lines))
        rb = b''.join(lines[a-1:z])
        rn = 'region.%03d.raw.snapshot' % len(regions)
        ln = rn.replace('.raw.', '.lf.')
        (OUT / rn).open('xb').write(rb)
        (OUT / ln).open('xb').write(lf(rb))
        regions.append(dict(path=path, lines=[a,z], role=role, raw_sha256=sha(rb), lf_sha256=sha(lf(rb)), raw_snapshot=rn, lf_snapshot=ln))
    return e

whole = pin(P+'gaussian-transport-preread/source-primary.raw.snapshot.html', kind='PRIMARY_WHOLE')
assert whole['raw_sha256'] == 'ec485cdad5fe140114be35eef93d19398e0cafcf21abb3fff1bdbbf462e5f94d'
for name,a,z,h in [
    ('primary.S4.E6.raw.snapshot.html',281135,283519,'601c07c36f592ec891b13b22cb0574c21a0c6df7e60c7b4fe9d8139c3c9cf822'),
    ('primary.S4.SS1.p4.3.raw.snapshot.html',283520,285390,'31e5b0a24c6d8b3055713cd2c48ae293a859cc209b5df82150162f4b9a471fa6')]:
    e = pin(P+'gaussian-clt-entropy-preread/'+name, kind='PRIMARY_ORIGINAL_BALANCED_SPAN')
    assert e['raw_sha256'] == h
    assert (ROOT/e['path']).read_bytes() == (ROOT/whole['path']).read_bytes()[a:z]
for path,kind in [
    (P+'gaussian-flip-energy-preread/primary.contract.json','PRIMARY_FIRST_FROZEN_BEFORE_API'),
    (P+'gaussian-compact-entropy-preread/source-detail-packet.json','CLOSED_DEPENDENCY_AUDIT_NOT_OWN_GRAPH'),
    (P+'gaussian-compact-entropy/preproof/signature.prospective.txt','SEALED_PARENT36_PUBLIC_SIGNATURE_ONLY'),
    (P+'gaussian-compact-entropy/preproof/root.statement-proposal.json','HISTORICAL_PARENT36_INTERFACE_METADATA_NO_PROOF'),
    (P+'bernoulli-function-lsi/preproof/bernoulli.signature.txt','ACTUAL_PARENT34_PUBLIC_SIGNATURE_ONLY')]: pin(path,kind=kind)

api = [
 ('Analysis/Calculus/ContDiff/Deriv.lean',[(87,141,"ContDiff.deriv', ContDiff.iterate_deriv', ContDiff.differentiable_deriv_two: C2 supplies C1 first derivative and continuous second derivative; no C3")]),
 ('Analysis/Calculus/Deriv/Support.lean',[(35,62,'HasCompactSupport.deriv: apply twice, no extra regularity binder')]),
 ('Analysis/Normed/Group/Bounded.lean',[(96,106,'Generated additive HasCompactSupport.exists_bound_of_continuous: compact + continuous gives real norm bound, replace by max0 internally')]),
 ('Analysis/Calculus/MeanValue.lean',[(697,748,'Convex.norm_image_sub_le_of_norm_deriv_le / root lipschitzWith_of_nnnorm_deriv_le: differentiability + actual derivative bound internally derived')]),
 ('Analysis/Calculus/Deriv/MeanValue.lean',[(75,79,'Standing scalar MVT: a<b, continuous on Icc, differentiable on Ioo'),(120,158,'exists_deriv_eq_slope: order negative-step endpoints and preserve signed secant')]),
 ('Algebra/BigOperators/Group/Finset/Piecewise.lean',[(235,250,'Generated additive Finset.sum_update_of_mem; authored sigma-after-Bool-update equality needed')]),
 ('Algebra/BigOperators/Group/Finset/Basic.lean',[(739,749,'Generated additive Finset.sum_erase_add')]),
 ('Data/Fintype/Card.lean',[(294,303,'Fintype.card_pos: actual finite cube nonempty even at N0')]),
 ('MeasureTheory/Measure/Count.lean',[(159,168,'Measure.count.isFiniteMeasure / count_univ, actual finite total cardinal')]),
 ('MeasureTheory/Measure/Typeclasses/Finite.lean',[(299,302,'Measure.smul_finite: coefficient not top from card positivity')]),
 ('MeasureTheory/Function/L1Space/Integrable.lean',[(164,169,'Integrable.of_finite requires finite carrier, measurable singletons AND finite measure')]),
 ('MeasureTheory/Integral/Bochner/Basic.lean',[(237,268,'integral_finsetSum / integral_sub: genuine summand and difference L1'),(952,970,'norm_integral_le_of_norm_le_const: integrate uniform error then actual probability mass1')]),
 ('MeasureTheory/Integral/Bochner/SumMeasure.lean',[(210,217,'integral_fintype: real finite Bochner formula still requires genuine Integrable')]),
 ('Analysis/Real/Sqrt.lean',[(128,140,'Real.tendsto_sqrt_atTop: successor nat cast goes infinity')]),
 ('Topology/Algebra/Order/Field.lean',[(74,78,'tendsto_inv_atTop_zero: inverse sqrt error tends0')])]
for path, rs in api: pin(M+path,rs)
external_regions = [
 ('SLT__GaussianPoincare__EfronSteinApp.lean.raw.snapshot',[(40,50,'CompactlySupportedSmooth = C2 AND compact support')]),
 ('SLT__GaussianPoincare__TaylorBound.lean.raw.snapshot',[(35,61,'Plus/minus step relation'),(77,241,'First and second derivative continuity, compact support, bounds and differentiability')]),
 ('SLT__GaussianPoincare__Limit.lean.raw.snapshot',[(592,1123,'Bounded full-energy route: MVT, error16, derivative observer reuse, permutation symmetry, AE signs, shift identity')]),
 ('SLT__GaussianLSI__BernoulliLSI.lean.raw.snapshot',[(1600,1634,'bernoulli_logSobolev_app: exact half full-flip consumer on external real carrier')]),
 ('SLT__GaussianLSI__OneDimGLSICompSmo.lean.raw.snapshot',[(45,82,'gaussian_logSobolev_CompSmo: actual compact consumer half*4=2')]),
 ('SLT__GaussianLSI__Entropy.lean.raw.snapshot',[(34,49,'Homogeneous entropy, no imposed mass normalization')])]
for path,rs in external_regions: pin(A+path,rs,kind='EXTERNAL_REFERENCE_NOT_CALLABLE')
for path in ['LICENSE.raw.snapshot','lean-toolchain.raw.snapshot','lake-manifest.json.raw.snapshot','import-closure-audit.json']: pin(A+path,kind='EXTERNAL_PIN_PROVENANCE')
for path in ['lean-toolchain','lake-manifest.json']: pin(path,kind='LOCAL_PIN_NO_CURRENT_COMPILER')
pin('.agents/skills/astis-source-dependency-audit/SKILL.md',kind='APPLIED_SKILL_TASK_LOCAL_SCOPE_OVERRIDE')

signature = '''theorem compact_count_full_flip_energy_limit
    (f : ℝ → ℝ) (hf : ContDiff ℝ 2 f) (hs : HasCompactSupport f) :
    let μ : (n : ℕ) → Measure (Fin n → Bool) := fun n =>
      (Fintype.card (Fin n → Bool) : ℝ≥0∞)⁻¹ • Measure.count
    let S : (n : ℕ) → (Fin n → Bool) → ℝ := fun n ε =>
      (Real.sqrt (n : ℝ))⁻¹ * ∑ j : Fin n, if ε j then (1 : ℝ) else -1
    let γ : Measure ℝ := gaussianReal 0 1
    let D : (n : ℕ) → (Fin n → Bool) → ℝ := fun n ε =>
      ∑ j : Fin n,
        (f (S n (Function.update ε j (!ε j))) - f (S n ε)) ^ 2
    Integrable (fun x => (deriv f x) ^ 2) γ ∧
      (∀ n : ℕ, Integrable (D n) (μ n)) ∧
      Tendsto (fun n : ℕ => ∫ ε, D (n + 1) ε ∂μ (n + 1)) atTop
        (𝓝 (4 * ∫ x, (deriv f x) ^ 2 ∂γ))
'''
(OUT/'prospective.signature.txt').open('xb').write(signature.encode())
route = [
 'Derive actual count mass1 from positive finite cardinal; produce finite-measure and allN finite cube L1, including N0 empty coordinate sum. Finite carrier alone and totalized integral notation do not establish domain.',
 'From C2compact derive continuous fprime/fsecond and compact support twice, hence internal nonnegative bounds B,K. Genuine local derivative MVT bound makes fprime globally K-Lipschitz.',
 'For N>0 prove literal Bool flip displacement s_j=-2 sigma(eps_j)/sqrtN; |s_j|=delta=2/sqrtN and N delta²=4. These are actual pointwise identities, no law/symmetry certificate.',
 'Scalar MVT on ordered endpoints gives secant a_j=fprime(xi_j), |xi_j-S_N|<=delta. Derive |a_j-fprime(S_N)|<=Kdelta; both values bounded by B, so squared error <=2BKdelta.',
 'Sum delta² times squared error over ALL coordinates: |D_N-4 fprime(S_N)²|<=16BK/sqrtN. Integrate the actual difference under mass1 mu_N, with genuine L1 and integral_sub.',
 'Compose real sqrt atTop and inverse->0 with successor nat casts to squeeze actual integral error to0; never divide by B,K or mass of f².',
 'Call admitted36 compact_count_gaussian_entropy_limits internally for SAME mu/S/gamma derivative-square limit and Gaussian L1, then add error0 to4 times that limit. Final Bernoulli+entropy comparison is later.'
]
closure=json.loads((ROOT/(A+'import-closure-audit.json')).read_text())
external=[]
for name in ['SLT/GaussianPoincare/Limit.lean','SLT/GaussianPoincare/TaylorBound.lean','SLT/GaussianPoincare/EfronSteinApp.lean','SLT/GaussianLSI/BernoulliLSI.lean','SLT/GaussianLSI/OneDimGLSICompSmo.lean','SLT/GaussianLSI/Entropy.lean']:
    e=next(x for x in closure['files'] if x['path']==name)
    b=(ROOT/e['local_snapshot']).read_bytes()
    assert sha(b)==e['raw_sha256']
    hits=[dict(line=i,text=x) for i,x in enumerate(b.decode().splitlines(),1) if re.search(r'\b(sorry|admit|axiom)\b',x)]
    external.append(dict(path=name,raw_sha256=sha(b),imports=e['imports'],current_direct_text_placeholder_hits=hits,local_callable=False))
shape=dict(path='prospective.signature.txt',raw_sha256=sha(signature.encode()),lf_sha256=sha(signature.encode()),typechecked=False,StatementSeal=False,only_public_inputs=['f:Real->Real','ContDiff Real2 f','HasCompactSupport f'],certificate_binders=[])
constants=dict(delta='2/sqrtN',signed_step='-2 sigma(eps_j)/sqrtN',secant_square_error='2BKdelta=4BK/sqrtN',full_pointwise_sum_error='Ndelta²*2BKdelta=16BK/sqrtN',limit_factor=4,future_LSI_coefficient='(1/2)*4=2')
blockers=[
 dict(type='UNIMPLEMENTED_ACTUAL_FLIP_ADAPTER',first_required='Literal Bool-update/sign sum displacement, per-coordinate signed secant-square bound, and genuine integral error squeeze are new authored producers.',minimal_next_delta='The one prospective theorem above, no extra public premise.'),
 dict(type='EXTERNAL_CARRIER_ADAPTER_IF_SOURCE_ROUTE_CHOSEN',first_required='Bool-count pushforward to real RademacherProduct law, same S/flip intertwining, AE-sign and sum-integral adapters.',required_for='External SLT route only; authored Bool-direct OR avoids this.'),
 dict(type='PARENT_ADMISSION_NOT_CERTIFIED_BY_PREREAD',first_required='36 independent proof/source admission belongs to root and distinct reviewers; current packet reads only sealed interface. Root reports focused3162PASS and review active, no proof verdict inferred.')]
remaining=['compact Gaussian LSI final half Bernoulli + entropy36 + fullenergy37 comparison','noncompact literal32 sqrt-RN W12/cutoff domains','finite Hilbert Gaussian extension','full GaussianLSI','GaussianTalagrand T2 finite-moment/metric/canonicalKL adapters','SPHMC FIRST4.6','bias/main/numerical/work/cost/composition']
packet=dict(schema_version=1,artifact_kind='primary-first-source-API-dependency-preread',status='CLOSED_DEPENDENCY_READY_MATHEMATICAL_SHAPE_NOT_STATEMENTSEAL',actor='gaussian_domain_preproof_reviewer_29',history='Authored36 source graph; no selfvalidation here. Distinct phase review remains its truth provenance. Exact sealed36 interface read, no current36 proof body or37 candidate/body/Test/blind.',primary_first_contract='primary.contract.json',synthesis_first='The full literal Bool flip-energy factor4 is valid for unrestricted signed C2compact f with no convenience premise. Shortest route: per-coordinate pointwise MVT error plus actual36 same-count derivative-observer limit. No external real-product adapter needed.',fixed_definitions=dict(mu_N='inverse ENNReal card(FinN->Bool) smul count; actual mass1 derived, card2^N>0',S_N='inverse sqrt(N:Real) times sum sigma; sigma(true)=1,false=-1',gamma='gaussianReal0(1:NNReal), real scalar variance1',flip='Function.update eps j (!eps_j), full flip, not half difference',D_N='sum_j (f(S_N flip_j eps)-f(S_N eps))², actual integral of sum',entropy='homogeneous entropy(f²), no normalizedmass assumption'),prospective_shape=shape,route_at_most_seven_steps=route,constant_audit=constants,boundary_cases=dict(N0='Fin0 sum empty, D0=0, S0=0, actual mu0 mass1, finite L1. Secants only for positive successor.',signed_f='No positivity assumption; differences squared.',zero_bounds='B,K>=0 may be0, no division by them.',zero_mass='No positive or unit mass of f². Later entropy36 handles zero.',regularity='C2+support twice suffices for bounded fprime and fsecond. No fthird.'),api_inventory=[dict(path=M+p,headers_and_hypotheses=rs) for p,rs in api],intended_import_inventory=['AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianCompactEntropy','Mathlib.Analysis.Calculus.Deriv.MeanValue','Mathlib.Analysis.Calculus.MeanValue','Mathlib.Analysis.Calculus.Deriv.Support','Mathlib.Analysis.Normed.Group.Bounded','Mathlib.Algebra.BigOperators.Group.Finset.Piecewise','Mathlib.Analysis.Real.Sqrt'],actual_parent36='AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianCompactEntropy.compact_count_gaussian_entropy_limits',parent36_status='Sealed interface only. Root current focused PASS is not reverified here. Future actual proof must invoke internally after applicable independent admission.',formal_edge_condition='36 is a formal parent only if future proof actually calls it. API availability/intended reuse does not constitute compiled dependency.',actual_parent34_consumer='AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.BernoulliLogSobolev.bernoulli_function_logSobolev with h=f composed S_N and exact coefficient1/2; downstream sibling for compactLSI, not automatically parent of37.',source_routes=dict(external_SLT='Limit592-1123: real-product carrier MVT error16, derivativeobserver/map reuse, coordinate permutation invariance, ±1 AE signs, shifted difference identity. Final1030-1034 uses sum of integrals; actual target is integral of sum with internally proved L1 finite sum adapter.',authored_Bool_direct_OR='Pointwise Bool signs + every-coordinate uniform secant estimate bypass realcarrier pushforward/permutation/AE-value adapters. It is authored background route, not printed SPHMC proof attribution.',excluded='No whole variance/EfronStein/Han/CLT port needed for this energy increment.'),actual_paper_consumer='SPHMC FIRST S4.E6 uses GaussianLSI AND separate GaussianTalagrand. This compact scalar energy theorem is one omitted-background parent; literal32 RGO sqrt-density is noncompact.',external_provenance=dict(revision=closure['revision'],license='Apache2 exact LICENSE/source headers pinned',upstream_toolchain='Lean4.32.0',upstream_mathlib='81a5d257c8e410db227a6665ed08f64fea08e997',local_toolchain='Lean4.33.0',local_mathlib='db584cd6d46c92f209a44c0f1c829460d327499d',modules=external,prior_static_closure=dict(files=len(closure['files']),failures=len(closure['failures']),placeholder_files=sum(bool(x.get('placeholder_scan_hits')) for x in closure['files']),boundary='Reused existing CLOSED static24file receipt, no transitive rescan or upstream compilation now.'),callable_status='SLT external reference only; no external project imported and no new producer compiled.'),typed_blockers=blockers,remaining_open=remaining,local_search_boundary='ASTIS TechnicalLemmas and technical cards searched first; no existing full-energy producer. Incidental36 minimal call/header snippets returned in search; no36 proof body opened. No37 implementation/candidate/Test/blind or active compiler read. No site/global transcript scan.',compiled_edges=[],compiler_started=False,proof_search=False,claim=False,inputs='inputs.json',regions='source-regions.json',leases='lease.json')
emit('source-detail-packet.json',packet)
emit('source-regions.json',dict(kind='Bounded relevant source/API region pins, not exhaustive entire upstream project or sourcegraph selfvalidation',regions=regions))
emit('inputs.json',dict(raw_LF_bound_inputs=inputs,count=len(inputs),all_original_bytes_unchanged=True))
emit('bounded-synthesis.json',dict(status=packet['status'],synthesis_first=packet['synthesis_first'],prospective_shape=shape,route_at_most_seven_steps=route,first_required_unmet_dependency=blockers[0],constant_audit=constants,actual_paper_consumer=packet['actual_paper_consumer'],remaining_open=remaining,no_compiler_proof_theorem_credit=True))
for e in inputs:
    b=(ROOT/e['path']).read_bytes()
    assert sha(b)==e['raw_sha256'] and sha(lf(b))==e['lf_sha256']
outputs=[]
for name in ['primary.contract.json','prospective.signature.txt','source-detail-packet.json','source-regions.json','inputs.json','bounded-synthesis.json','preread.py']:
    b=(OUT/name).read_bytes()
    outputs.append(dict(path=str((OUT/name).relative_to(ROOT)).replace('\\','/'),raw_sha256=sha(b),lf_sha256=sha(lf(b))))
runid=sha(json.dumps(dict(inputs=inputs,outputs=outputs),sort_keys=True,ensure_ascii=False,separators=(',',':')).encode())
emit('run.closed.json',dict(deterministic_run_sha256=runid,inputs_count=len(inputs),regions_count=len(regions),inputs=inputs,outputs=outputs,checks='All raw/LF inputs unchanged at close; original balanced primary byte intervals exact; external source pins match existing audit.',read_lease='CLOSED',write_lease='CLOSED',compiler_lease='CLOSED',compiler_started=False,retained_helper_failure='An initial nested-quote Python helper failed to parse before creating any output; corrected file-writing method, no source/statement alteration. One lookup used obsolete Mathlib Measure/Basic path; actual Count/Typeclasses/Finite sources inspected.'))
lease=json.loads((OUT/'lease.json').read_text())
lease.update(status='CLOSED',read_lease='CLOSED',write_lease='CLOSED',compiler_lease='CLOSED',compiler_started=False,closed_utc=datetime.datetime.utcnow().isoformat()+'Z',deterministic_run_sha256=runid,inputs_count=len(inputs),outputs_frozen=True)
(OUT/'lease.json').write_bytes((json.dumps(lease,ensure_ascii=False,indent=2)+'\n').encode())
print(json.dumps(dict(run=runid,inputs=len(inputs),regions=len(regions),packet_raw_sha256=sha((OUT/'source-detail-packet.json').read_bytes()),status='CLOSED',compiler_started=False)))
