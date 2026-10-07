from pathlib import Path
import json, hashlib, re, datetime

ROOT = Path('E:/Samplinglib')
OUT = ROOT / 'runs/20261007-companion-priority/rademacher-law-source-graph'
PRE = 'runs/20261007-companion-priority/rademacher-law-preproof-review/'
UP = 'runs/20261007-companion-priority/gaussian-functional-availability/'
ML = '.lake/packages/mathlib/Mathlib/'
ACTOR = 'gaussian_domain_preproof_reviewer_29'
def sha(b): return hashlib.sha256(b).hexdigest()
def lf(b): return b.replace(b'\r\n', b'\n').replace(b'\r', b'\n')
def put(name, obj):
    b = (json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode()
    with (OUT / name).open('xb') as f: f.write(b)
    return {'path': str((OUT/name).relative_to(ROOT)).replace('\\','/'), 'raw_sha256':sha(b), 'lf_sha256':sha(lf(b)), 'bytes':len(b)}

prior = json.loads((ROOT / (PRE+'primary.inputs.frozen.json')).read_bytes())
paths = [x['path'] for x in prior['inputs']]
extra = [PRE+'primary.contract.json', PRE+'primary.inputs.frozen.json', PRE+'primary.run.json', PRE+'primary.lease.json',
 ML+'MeasureTheory/Constructions/Pi.lean', ML+'MeasureTheory/Function/ConvergenceInDistribution.lean',
 ML+'MeasureTheory/Measure/CharacteristicFunction/TaylorExpansion.lean', ML+'Analysis/SpecialFunctions/Complex/LogBounds.lean',
 ML+'Algebra/BigOperators/Ring/Finset.lean', ML+'Analysis/Complex/Exponential.lean',
 ML+'Data/Fintype/BigOperators.lean', ML+'Data/Fintype/Card.lean',
 ML+'MeasureTheory/Integral/Bochner/Basic.lean',
 ML+'MeasureTheory/Integral/Bochner/SumMeasure.lean', ML+'MeasureTheory/Function/L1Space/Integrable.lean',
 UP+'SLT__GaussianPoincare__RademacherApprox.lean.raw.snapshot',
 'AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/BernoulliLogSobolev.lean',
 'runs/20261007-companion-priority/bernoulli-function-lsi/whole-proof-review/reviewer.math.review.json',
 '.lake/packages/mathlib/.lake/build/lib/lean/Mathlib/Probability/CentralLimitTheorem.olean',
 '.lake/packages/mathlib/LICENSE']
paths += [p for p in extra if p not in paths]
inputs = []
raws = {}
for i,p in enumerate(paths):
    b=(ROOT/p).read_bytes(); raws[p]=b
    old=next((x for x in prior['inputs'] if x['path']==p),None)
    if old: assert sha(b)==old['raw_sha256'] and sha(lf(b))==old['lf_sha256'], p
    if p.endswith('BernoulliLogSobolev.lean'):
        assert sha(b)=='538bf595878685aa962d90146bcbeb5c7d08b3ecefe698a728565325b9d794bf'
    r=f'input.{i:03d}.raw.snapshot'; l=f'input.{i:03d}.lf.snapshot'
    with (OUT/r).open('xb') as f:f.write(b)
    if not p.endswith('.olean'):
        with (OUT/l).open('xb') as f:f.write(lf(b))
    else:l=None
    inputs.append({'path':p,'bytes':len(b),'raw_sha256':sha(b),'lf_sha256':sha(lf(b)) if l else None,
      'raw_snapshot':str((OUT/r).relative_to(ROOT)).replace('\\','/'),
      'lf_snapshot':str((OUT/l).relative_to(ROOT)).replace('\\','/') if l else None,
      'historical_primary_pin_rechecked':bool(old),
      'kind':'existing_compiled_API_binary_not_new_compile' if not l else 'source_or_closed_evidence'})
binding=put('input-bindings.json', {'actor':ACTOR,'status':'FROZEN','inputs':inputs,'input_count':len(inputs),
 'raw_LF_convention':'LF=raw.replace(CRLF,LF).replace(CR,LF); raw bytes never modified',
 'candidate35_implementation_read':False,'compiler_started':False,'scope':'primary plus pinned bounded source/API; no source35 proof body or future implementation'})

nodes=[]; edges=[]; alternatives=[]; coverage_specs=[]
def node(i,kind,formula,**kw):
    d={'id':i,'kind':kind,'formula_or_contract':formula,'public_target_binder':False};d.update(kw);nodes.append(d)
def deps(to,fr,contract='source/API mathematical ingredient dependency, not a current35 compiled edge'):
    for a in fr:edges.append({'from':a,'to':to,'truth_contract':contract})
def spec(p,lo,hi,ids=None,reason=None):
    coverage_specs.append((p,lo,hi,ids,reason))

node('PRIMARY-RHO','SOURCE_CONTEXT','rho_y(u)=V(p+sqrt(eta)u)-V(p)-sqrt(eta)<grad V(p),u>; actual standardized RGO r_y has density proportional exp(-|u|²/2-rho_y(u)).',
 source_anchor=['S4.Ex8','S4.SS1.p4.2'], retained_context='standing potential assumptions and eta>0 belong to ultimate SPHMC consumer, not to this unconditional scalar CLT target')
node('PRIMARY-FIRST46','SOURCE_CONTEXT','W2(r_y,N(0,I)) <= sqrt(E_(r_y)|grad rho_y|²)',source_anchor=['FIRST relation S4.E6','FIRST explanation S4.SS1.p4.3'],
 source_gap='Paper names Gaussian Talagrand + Gaussian log-Sobolev; does not print a Rademacher CLT or its adapters.')
deps('PRIMARY-FIRST46',['PRIMARY-RHO'],'ultimate consumer context only; not proved by this packet')
node('FINITE-COUNT-DEFINITION','AUTHORED_DEFINITION','A_N=Fin N→Bool; mu_N=(card A_N:ENNReal)^-1 • Measure.count; sign(true)=1, sign(false)=-1; S_N=(sqrt(N:Real))^-1 * sum_(j:Fin N) sign(epsilon j).',source='fresh primary/API contract; scalar background adaptation, not SPHMC printed definition')
node('FINITE-CARDINALITY','DERIVED_INTERNAL','card A_N=2^N, finite and nonzero for every N, including card A_0=1.',
 actual_parent_APIs=['Fintype.card_fun','Fintype.card_fin','Fintype.card_bool'], status='required internally; current35 producer OPEN')
node('COUNT-API','EXISTING_MATHLIB_API','Measure.count=sum dirac; finite count(univ)=card; count singleton=1; finite carrier gives finite count measure.')
node('COUNT-NORMALIZATION','DERIVED_INTERNAL','For every N, mu_N(univ)=1; inverse factor finite/nonzero, so actual IsProbabilityMeasure mu_N.',status='current35 producer OPEN')
deps('COUNT-NORMALIZATION',['FINITE-COUNT-DEFINITION','FINITE-CARDINALITY','COUNT-API'])
node('FINITE-DOMAINS','DERIVED_INTERNAL','Actual finite discrete A_N has measurable singletons; sign, finite sum and S_N are measurable. All Real/Complex functions on A_N are Bochner L1 for mu_N because actual mu_N is finite. No caller L1/AE/domain certificates.',
 actual_parent_APIs=['Integrable.of_finite','Measurable.of_discrete'],status='current35 producer OPEN')
deps('FINITE-DOMAINS',['COUNT-NORMALIZATION','FINITE-CARDINALITY','FINITE-COUNT-DEFINITION'])
node('PROBABILITY-MEASURE','EXISTING_MATHLIB_DEFINITION','ProbabilityMeasure E={mu:Measure E // IsProbabilityMeasure mu}; map by AEMeasurable gives actual probability pushforward. Weak topology induced via FiniteMeasure; equivalently bounded-continuous integral convergence.')
node('ACTUAL-LAWS','DERIVED_INTERNAL','lambda_N := actual ProbabilityMeasure whose underlying measure is mu_N.map S_N, for every N, from internally derived probability and measurability.',status='current35 producer OPEN')
deps('ACTUAL-LAWS',['FINITE-COUNT-DEFINITION','COUNT-NORMALIZATION','FINITE-DOMAINS','PROBABILITY-MEASURE'])
node('ZERO-LAW','DERIVED_INTERNAL','A_0 singleton; S_0=0 (empty sum, totalized sqrt0 inverse harmless); lambda_0.toMeasure=dirac0. Its mean and second moment are 0, not 1.',status='current35 producer OPEN')
deps('ZERO-LAW',['ACTUAL-LAWS','FINITE-CARDINALITY','COUNT-API'])
node('ONE-BOOL','AUTHORED_DEFINITION','kappa=(2:ENNReal)^-1 • count on Bool; X=sign. Actual kappa probability; sign map gives nu=(1/2)dirac(-1)+(1/2)dirac1.',status='local balanced single-coordinate producer OPEN')
deps('ONE-BOOL',['COUNT-API','FINITE-CARDINALITY','COUNT-NORMALIZATION'])
node('ONE-MOMENTS','DERIVED_INTERNAL','For actual kappa and X=sign, AEMeasurable X kappa; genuine L1 X and X²; E_kappa X=0 and E_kappa X²=1. Equivalent finite two-atom nu moments. No mu_0 variance-one substitution.',status='current35 producer OPEN')
deps('ONE-MOMENTS',['ONE-BOOL','FINITE-DOMAINS'])
node('FINITE-INTEGRAL-API','EXISTING_MATHLIB_API','Integrable.of_finite needs finite carrier/measurable singleton/finite measure; integral_fintype needs genuine L1 and sums singleton real masses; integral_count sums the finite carrier; integral_smul_measure supplies the true scalar normalization.')
deps('FINITE-INTEGRAL-API',['COUNT-API'],'existing API context, actual application premises derived internally')
deps('ONE-MOMENTS',['FINITE-INTEGRAL-API'])
node('CF-DEFINITION','EXISTING_MATHLIB_DEFINITION','charFun mu t=integral exp(inner(x,t)*I) dmu; on Real exp(t*x*I). Same actual mu/map, no abstract law certificate.')
node('MAP-INTEGRAL-API','EXISTING_MATHLIB_API','integral_map: actual AEmeasurable phi and AEstronglymeasurable integrand on its map imply equality with composed Bochner integral. CF integrand is continuous/bounded; actual finite source L1 and actual probability map give genuine domains. Totalized integral equality alone never supplies a moment/domain certificate.')
deps('MAP-INTEGRAL-API',['FINITE-DOMAINS','PROBABILITY-MEASURE'])
node('SCALED-CF-API','EXISTING_MATHLIB_API','charFun_map_mul_comp: for AEMeasurable f mu, charFun(mu.map(fun x=>r*f x))t=charFun(mu.map f)(r*t).')
deps('SCALED-CF-API',['CF-DEFINITION'])
node('COUNT-PRODUCT-SUM-API','EXISTING_MATHLIB_API','Fintype.prod_sum under finite dependent carriers and CommSemiring: product_i sum_b h(i,b)=sum_epsilon product_i h(i,epsilon i). Complex.exp_sum converts exponential of actual finite sum to product; no measure/law conclusion supplied by these algebra APIs.')
node('GAP-DIRECT-COUNT-CF','SOURCE_GAP','AUTHORED adapter: charFun(mu_N.map S_N)t = (charFun(kappa.map sign)((sqrt N)^-1*t))^N, by finite actual integral -> 2^-N configuration sum -> exp_sum -> Fintype.prod_sum -> N identical factors. Holds all N, including empty product N0; genuine L1 and inverse-card conversions internal.',
 provenance='root suggested bounded authored background route after primary contract; independently reconstructed from pinned algebra/integral APIs; not printed SPHMC/SLT theorem',status='OPEN no current35 compiled producer')
deps('GAP-DIRECT-COUNT-CF',['ACTUAL-LAWS','FINITE-INTEGRAL-API','FINITE-DOMAINS','FINITE-CARDINALITY','ONE-BOOL','CF-DEFINITION','MAP-INTEGRAL-API','COUNT-PRODUCT-SUM-API'])
node('PI-MEASURE-API','EXISTING_MATHLIB_API','For finite i: Measure.pi mu; probability when each mu_i probability; pi_singleton=product singleton masses; pi_map_pi for AE coordinate maps requires mapped coordinate SigmaFinite (derived from probability), true map pi equality. measurePreserving_eval gives actual coordinate marginals.')
node('GAP-COUNT-REAL-PRODUCT','SOURCE_GAP','AUTHORED adapter: mu_N.map(fun epsilon i=>sign(epsilon i))=Measure.pi(fun _:Fin N=>nu). Derive normalized Bool count=Bool product by equal singleton masses/finite measure ext, then sign-map using pi_map_pi. All measurability/SigmaFinite are actual internally derived facts; N0 empty-product law retained.',status='OPEN no current35 compiled producer')
deps('GAP-COUNT-REAL-PRODUCT',['COUNT-NORMALIZATION','FINITE-DOMAINS','FINITE-CARDINALITY','ONE-BOOL','COUNT-API','PI-MEASURE-API'])
node('PI-INDEPENDENCE-CF-API','EXISTING_MATHLIB_API','charFun_map_sum_pi_eq_prod for Fintype i and probability mu_i: CF((pi mu).map sum)=product CF(mu_i). Source body uses charFunDual_map_sum_pi_eq_prod, actual pi coordinate independence and measurePreserving_eval, finite iIndepFun CF induction. Real satisfies retained Borel/second-countable/inner-product standing types.')
deps('PI-INDEPENDENCE-CF-API',['PI-MEASURE-API','CF-DEFINITION'],'existing public API proof ingredients; no actual35 compiled edge')
node('GAP-PRODUCT-CF','SOURCE_GAP','AUTHORED application: transport actual S_N law via genuine count→real-product equality, sum pi characteristic function product, constant coordinate law and scaled CF; get same CF power for all N.',status='OPEN')
deps('GAP-PRODUCT-CF',['GAP-COUNT-REAL-PRODUCT','PI-INDEPENDENCE-CF-API','SCALED-CF-API','ACTUAL-LAWS','ONE-BOOL','FINITE-DOMAINS'])
node('ACTUAL-CF-POWER','DERIVED_INTERNAL','For all N,t, CF(lambda_N)t=[CF(kappa.map sign)((sqrt N)^-1*t)]^N.',status='OPEN; either finite authored adapter is sufficient, not both required')
alternatives.append({'id':'OR-FINITE-CF','kind':'AUTHORED_OR','to':'ACTUAL-CF-POWER','branches':[
 {'id':'DIRECT-COUNT','requires':['GAP-DIRECT-COUNT-CF'],'source_attribution':'authored finite algebra adapter; no source printed count theorem'},
 {'id':'REAL-PRODUCT','requires':['GAP-PRODUCT-CF'],'source_attribution':'authored actual count/product adapter plus genuine pinned Mathlib finite-product CF'}],
 'semantics':'Each branch proves SAME actual characteristic function formula; not a public premise or completed current35 edge.'})
node('TAYLOR-CF-API','EXISTING_MATHLIB_API','taylor_charFun_two: for probability P, AEMeasurable X, E X=0, E X²=1, CF(P.map X)(t)-(1-t²/2)=o(t²) at0. Nonzero actual second integral gives square L1/MemLp2; actual Taylor/C2 CF background internally supplies regularity.',
 source_dependencies=['taylorWithinEval_charFun_two_zero','taylorWithinEval_charFun_two_zero\u0027','contDiff_charFun','memLp_two_iff_integrable_sq','taylor_isLittleO_univ','Integrable.of_integral_ne_zero'],
 retained_standing_context='Measurable Omega; IsProbabilityMeasure P; Real state; no caller C2/L1 binder in35')
deps('TAYLOR-CF-API',['PROBABILITY-MEASURE','CF-DEFINITION'])
node('CF-MOMENT-REGULARITY','EXISTING_MATHLIB_API','contDiff_charFun: actual finite measure and MemLp id n give C^n characteristic function, using contDiff_fourierIntegral and internally derived lower-order genuine norm-moment L1. Specialize n2 to actual single-coordinate square moment, not an extra35 C2 binder.')
node('CF-TAYLOR-POLYNOMIAL','EXISTING_MATHLIB_API','iteratedFDeriv_charFun -> iteratedDeriv_charFun/zero -> taylorWithinEval_charFun_zero. Actual moment coefficients; n2 polynomial follows genuine map integrals and mean0/moment2=1, with MemLp2 derived from actual nonzero integral.')
deps('CF-TAYLOR-POLYNOMIAL',['CF-MOMENT-REGULARITY','CF-DEFINITION','MAP-INTEGRAL-API'])
deps('TAYLOR-CF-API',['CF-MOMENT-REGULARITY','CF-TAYLOR-POLYNOMIAL'])
node('COMPLEX-POWER-API','EXISTING_MATHLIB_API','Complex.tendsto_pow_exp_of_isLittleO_sub_add_div: f(n)-(1+t/n)=o(1/n) -> f(n)^n→exp t. Source internally uses tendsto_one_add_pow_exp_of_tendsto and eventual n!=0; n0 is never a variance-one hypothesis.')
node('MATHLIB-SCALAR-CLT-LEAF','EXISTING_COMPILED_MATHLIB_API','ProbabilityTheory.tendsto_charFun_inv_sqrt_mul_pow: probability P; X AEmeasurable; E X=0; E X²=1; forall t, CF(P.map X)((sqrt n)^-1*t)^n→exp(-t²/2).',
 exact_header='lemma tendsto_charFun_inv_sqrt_mul_pow {X : Ω → ℝ}\n    (hX : AEMeasurable X P) (h0 : P[X] = 0) (h1 : P[X ^ 2] = 1) (t : ℝ) :\n    Tendsto (fun (n : ℕ) ↦ (charFun (P.map X) ((√n)⁻¹ * t)) ^ n) atTop (𝓝 (exp (- t ^ 2 / 2)))',
 source_line=55,existing_compilation_evidence='.lake/packages/mathlib/.lake/build/lib/lean/Mathlib/Probability/CentralLimitTheorem.olean pinned in inputs; no new compile or new ASTIS35 producer',
 direct_background_dependencies=['TAYLOR-CF-API','COMPLEX-POWER-API','Real.tendsto_sqrt_atTop','tendsto_inv_atTop_zero','tendsto_natCast_atTop_atTop','Asymptotics littleO composition/algebra'],
 primitive_import_boundary='existing compiled Mathlib API imported calculus/Fourier/asymptotics/topology is retained as existing background; no whole kernel/transitive project revalidation claimed')
deps('MATHLIB-SCALAR-CLT-LEAF',['TAYLOR-CF-API','COMPLEX-POWER-API'])
node('ACTUAL-CF-LIMIT','DERIVED_INTERNAL','Apply scalar CLT leaf to actual single Bool law/sign with internally proved mean0 and secondmoment1; combine actual power formula -> CF(lambda_N)t→exp(-t²/2).',status='OPEN current35 application')
deps('ACTUAL-CF-LIMIT',['ACTUAL-CF-POWER','ONE-MOMENTS','MATHLIB-SCALAR-CLT-LEAF'])
node('GAUSSIAN-REAL','EXISTING_MATHLIB_DEFINITION','gaussianReal(mean:Real)(variance:NNReal); actual massone for all variance; at mean0,variance1 its CF=exp(-t²/2). This is scalar variance1, not variance1/2 or just a name stdGaussian.')
node('LEVY-API','EXISTING_MATHLIB_API','ProbabilityMeasure.tendsto_of_tendsto_charFun / tendsto_iff_tendsto_charFun: probability measures on finite-dimensional real inner-product Borel space, pointwise CF convergence to actual limit CF iff weak convergence. Real supplies canonical standing classes; no Wasserstein/TV/entropy assertion.',
 source_dependencies=['isTightMeasureSet_of_tendsto_charFun','tendsto_of_tight_of_separatesPoints','charPoly','tendsto_charPoly_of_tendsto_charFun'],primitive_import_boundary='existing compiled tightness/Stone-Weierstrass background, no new35 theorem credit')
deps('LEVY-API',['PROBABILITY-MEASURE','CF-DEFINITION'])
node('FINITE-WEAK-LIMIT','DERIVED_INTERNAL','lambda_N→ProbabilityMeasure(gaussianReal0,1) by Levy from actual CF limit, or directly successor-composed CF limit.',status='OPEN')
deps('FINITE-WEAK-LIMIT',['ACTUAL-LAWS','ACTUAL-CF-LIMIT','GAUSSIAN-REAL','LEVY-API'])
node('GAP-INFINITE-IID','SOURCE_GAP','AUTHORED alternative: internally construct actual probability space carrying infinite independent balanced Bool/sign coordinates, prove all IdentDistrib and iIndepFun; identify every finite prefix actual pushforward with mu_N.map S_N. Infinite product construction and prefix→finite-count law equality are additional unmet adapters; neither is given publicly.',status='OPEN; not dependency-ready merely because general iid CLT exists')
deps('GAP-INFINITE-IID',['ONE-BOOL','ONE-MOMENTS','ACTUAL-LAWS','PI-MEASURE-API'])
node('IID-CF-API','EXISTING_MATHLIB_API','charFun_inv_sqrt_mul_sum: iIndepFun X P + forall i IdentDistrib(X i)(X0)PP -> actual prefix sum CF power. Its source retains AEmeasurability derived from IdentDistrib and finite range sum.')
deps('IID-CF-API',['PI-INDEPENDENCE-CF-API','SCALED-CF-API'])
node('IID-CLT-API','EXISTING_MATHLIB_API','tendstoInDistribution_inv_sqrt_mul_sum: actual probability P/P\u0027; HasLaw Y gaussianReal0,1 P\u0027; centered secondmoment1 X0; iIndepFun; IdentDistriball -> actual normalized prefix maps converge in ProbabilityMeasure weak topology. Internal alternative can take Y=id under actual gaussianReal0,1, not demand a new target certificate.')
deps('IID-CLT-API',['IID-CF-API','MATHLIB-SCALAR-CLT-LEAF','LEVY-API','GAUSSIAN-REAL'])
node('DISTRIBUTION-TO-LAW','EXISTING_MATHLIB_DEFINITION','TendstoInDistribution includes all actual maps AEmeasurable and exact ProbabilityMeasure-map weak Tendsto field; no stronger discrepancy assertion.')
node('IID-ACTUAL-WEAK','SOURCE_GAP','AUTHORED application: use infinite-iid construction/prefix law equality and existing CLT then extract actual-map tendsto field. Retain both probability spaces, actual HasLaw, all internal moments/independence and prefix map; no extra source/target binder.',status='OPEN')
deps('IID-ACTUAL-WEAK',['GAP-INFINITE-IID','IID-CLT-API','DISTRIBUTION-TO-LAW','ACTUAL-LAWS','GAUSSIAN-REAL'])
node('WEAK-LIMIT','DERIVED_INTERNAL','Same actual lambda_N scalar weak Gaussian0,1 limit, via a finite CF branch OR genuine iid prefix-law branch.',status='OPEN')
alternatives.append({'id':'OR-LAW-LIMIT','kind':'AUTHORED_OR','to':'WEAK-LIMIT','branches':[
 {'id':'FINITE-CF','requires':['FINITE-WEAK-LIMIT'],'source_attribution':'existing Mathlib CF/Levy leaves plus authored finite actual law adapter'},
 {'id':'INFINITE-IID','requires':['IID-ACTUAL-WEAK'],'source_attribution':'general iid Mathlib CLT plus additional authored infinite law/prefix adapter'}],
 'semantics':'Route alternatives for omitted Gaussian background; not two source-printed proofs and not given convergence assumptions.'})
node('SUCCESSOR-LIMIT','DERIVED_INTERNAL','Compose actual weak limit with n↦n+1 (tendsto_add_atTop_nat1), retaining variance1 only for positive cardinal sum indexing.',status='OPEN')
deps('SUCCESSOR-LIMIT',['WEAK-LIMIT'])
node('TARGET35','AUTHORED_TARGET','exists laws:Nat→ProbabilityMeasure Real, (forall N, laws_N.toMeasure=mu_N.map S_N) AND laws_0.toMeasure=dirac0 AND Tendsto(fun n=>laws_(n+1))atTop(nhds ProbabilityMeasure(gaussianReal0,1)). No public mathematical hypothesis or output certificate supplied.',
 declaration='AutoSamplingTheory.TechnicalLemmas.Probability.BalancedRademacherCLT.balanced_count_sum_tendsto_gaussian', status='UNPROVED current35 producer; exact statement previously independently admitted; source graph here not selfvalidated')
deps('TARGET35',['ACTUAL-LAWS','ZERO-LAW','SUCCESSOR-LIMIT'])

node('SLT-NU','EXTERNAL_SOURCE_REFERENCE','SLT actual nu=(1/2)dirac(-1)+(1/2)dirac1, probability, genuine integrable id/square, mean0 secondmoment1.',not_callable=True)
node('SLT-REAL-PRODUCT','EXTERNAL_SOURCE_REFERENCE','SLT RademacherSpace N=Fin N→Real; actual pi nu; normalized sum sqrtN^-1 sum; actual product probability/measurability/coordinate independence.',not_callable=True)
deps('SLT-REAL-PRODUCT',['SLT-NU'],'external pinned source dependency only, not ASTIS compiled edge')
node('SLT-LAW-CF','EXTERNAL_SOURCE_REFERENCE','SLT rademacherLaw(N)[NeZero N] actual real-product normalized sum pushforward; CF=(cos(t/sqrt N))^N. Standard Gaussian defined literally ProbabilityMeasure gaussianReal0,1.',not_callable=True)
deps('SLT-LAW-CF',['SLT-REAL-PRODUCT'],'external source route only')
node('SLT-COS-LIMIT','EXTERNAL_SOURCE_REFERENCE','SLT tendsto_cos_pow_exp uses true cosine Taylor remainder |cosx-(1-x²/2)|<=5|x|⁴/96 for |x|<=1, littleO exponent limit, eventually positive N; invokes external TaylorBound Real.cos_bound and existing complex power limit.',not_callable=True,
 imported_source_boundary='TaylorBound.Real.cos_bound external imported prerequisite not ported/revalidated here; bounded current35 local route uses actual moment-based Mathlib leaf instead')
node('SLT-LIMIT','EXTERNAL_SOURCE_REFERENCE','SLT rademacherLaw_tendsto_stdGaussian: successor actual real-product laws weakly→literal gaussianReal0,1 using CF formula, cos power limit, Gaussian CF, Levy, successor shift. Not a Bool-count or N0 theorem.',not_callable=True)
deps('SLT-LIMIT',['SLT-LAW-CF','SLT-COS-LIMIT'],'external source proof ingredients; no callable producer assertion')
node('PRIOR34-PRIVATE','HISTORICAL_COMPILED_SUBSTRATE','Existing private Bernoulli uniform/count-card/snoc/integral-split/probability helpers establish analogous actual count law internally. Private names are not exported callable35 dependencies; no Bernoulli LSI or Han theorem needed for this CLT proof.',
 status='existing compiled34 substrate independently reviewed; only source/API pattern provenance',compiled_dependency=False)

future=[('GAP-ENTROPY-LIMIT','Actual entropy/compact bounded-continuous integral adapter, including h²log(h²) at zeros.'),
 ('GAP-FLIP-ENERGY','Actual Bernoulli flip energy convergence to 4*integral |h\u0027|²; secants/MVT/domination.'),
 ('GAP-COMPACT-GAUSSIAN-LSI','Combine genuine Bernoulli half constant with actual entropy/energy limits -> Ent_gamma(h²)<=2 integral |h\u0027|² for compact C2 scalar h.'),
 ('GAP-HILBERT-TENSOR','Genuine finite-product Gaussian tensorization/orthonormal finite-Hilbert transport; E0 and covarianceI.'),
 ('GAP-NONCOMPACT','Cutoff/W12 approximation retaining same Dirichlet constant for literal positive noncompact sqrt density32; no compact-only certificate substitution.'),
 ('GAP-T2','Gaussian Talagrand T2 with canonical KL and true metric law/domains; named W2/optimal coupling definitions are not producer.'),
 ('GAP-FIRST46-CONSUMER','Actual standardized RGO r, canonical finiteKL33 and energy32, LSI entropy/Fisher normalization and metric adapters -> FIRST4.6; canonical RN pointwise derivative remains distinct.'),
 ('GAP-OTHER-PAPER','Neighbor SECOND/THIRD4.6, bias/main/work/composition cannot be admitted by this packet.')]
for i,f in future:node(i,'OUT_OF_SCOPE_SOURCE_GAP',f,status='OPEN external residual to current35',current_target_credit=False)
deps('GAP-ENTROPY-LIMIT',['TARGET35'],'future residual only, weak convergence alone does not imply entropy convergence')
deps('GAP-COMPACT-GAUSSIAN-LSI',['GAP-ENTROPY-LIMIT','GAP-FLIP-ENERGY'],'future residual, not current completion')
deps('GAP-HILBERT-TENSOR',['GAP-COMPACT-GAUSSIAN-LSI'],'future residual')
deps('GAP-NONCOMPACT',['GAP-HILBERT-TENSOR'],'future residual')
deps('GAP-FIRST46-CONSUMER',['PRIMARY-RHO','GAP-NONCOMPACT','GAP-T2'],'future consumer residual, no proof credit')
deps('PRIMARY-FIRST46',['GAP-FIRST46-CONSUMER'],'future source gap retained; target35 does not close FIRST4.6')

# Exhaustive dispositions within explicit bounded source footprints, not a whole library scan.
C=ML+'Probability/CentralLimitTheorem.lean'
spec(C,1,43,['MATHLIB-SCALAR-CLT-LEAF','IID-CLT-API'])
spec(C,44,51,['IID-CF-API']);spec(C,52,72,['MATHLIB-SCALAR-CLT-LEAF'])
spec(C,73,90,['IID-CLT-API']);spec(C,91,None,reason='EXCLUDED general variance/mean and zero-variance CLT extensions beyond exact centered variance1 target; no target premise copied')
I=ML+'Probability/Independence/CharacteristicFunction.lean'
spec(I,1,42,['PI-INDEPENDENCE-CF-API']);spec(I,43,76,reason='EXCLUDED Hilbert two-variable CF and independence equivalence variants; finite-product proof uses dual induction branch')
spec(I,77,94,['PI-INDEPENDENCE-CF-API']);spec(I,95,124,reason='EXCLUDED converse independence/WithLp variants not needed')
spec(I,125,158,['PI-INDEPENDENCE-CF-API']);spec(I,159,161,reason='EXCLUDED deprecated alias')
spec(I,162,180,['PI-INDEPENDENCE-CF-API']);spec(I,181,195,['PI-INDEPENDENCE-CF-API'])
spec(I,196,198,reason='EXCLUDED deprecated alias');spec(I,199,209,['PI-INDEPENDENCE-CF-API']);spec(I,210,213,reason='EXCLUDED deprecated alias')
spec(I,214,225,['PI-INDEPENDENCE-CF-API']);spec(I,226,None,reason='EXCLUDED later disjointness/product-law variants outside finite scalar sum branch')
T=ML+'MeasureTheory/Measure/CharacteristicFunction/TaylorExpansion.lean'
spec(T,1,42,['TAYLOR-CF-API']);spec(T,122,138,['TAYLOR-CF-API']);spec(T,139,163,['TAYLOR-CF-API'])
spec(T,43,53,['CF-MOMENT-REGULARITY']);spec(T,54,68,reason='EXCLUDED C-infinity and continuous-only wrappers; scalar CLT needs moment2 finite-order regularity')
spec(T,69,121,['CF-TAYLOR-POLYNOMIAL'])
spec(ML+'Analysis/SpecialFunctions/Complex/LogBounds.lean',30,32,['COMPLEX-POWER-API'])
spec(ML+'Analysis/SpecialFunctions/Complex/LogBounds.lean',358,364,['COMPLEX-POWER-API']);spec(ML+'Analysis/SpecialFunctions/Complex/LogBounds.lean',365,370,reason='EXCLUDED exact (1+t/n)^n variant unused by littleO API proof')
spec(ML+'Analysis/SpecialFunctions/Complex/LogBounds.lean',371,383,['COMPLEX-POWER-API'])
P=ML+'MeasureTheory/Constructions/Pi.lean'
spec(P,63,69,['PI-MEASURE-API']);spec(P,124,126,['PI-MEASURE-API']);spec(P,209,211,['PI-MEASURE-API']);spec(P,277,312,['PI-MEASURE-API']);spec(P,324,324,['PI-MEASURE-API']);spec(P,375,407,['PI-MEASURE-API'])
B=ML+'MeasureTheory/Measure/CharacteristicFunction/Basic.lean'
spec(B,123,135,['CF-DEFINITION']);spec(B,199,218,['SCALED-CF-API'])
PM=ML+'MeasureTheory/Measure/ProbabilityMeasure.lean'
spec(PM,90,120,['PROBABILITY-MEASURE']);spec(PM,286,290,['PROBABILITY-MEASURE']);spec(PM,343,352,['PROBABILITY-MEASURE']);spec(PM,601,620,['PROBABILITY-MEASURE'])
L=ML+'MeasureTheory/Measure/LevyConvergence.lean'
spec(L,1,41,['LEVY-API']);spec(L,198,223,['LEVY-API'])
G=ML+'Probability/Distributions/Gaussian/Real.lean'
spec(G,219,233,['GAUSSIAN-REAL']);spec(G,486,491,['GAUSSIAN-REAL'])
spec(ML+'MeasureTheory/Function/ConvergenceInDistribution.lean',51,71,['DISTRIBUTION-TO-LAW'])
Q=ML+'MeasureTheory/Measure/Count.lean'
spec(Q,29,33,['COUNT-API']);spec(Q,43,61,['COUNT-API']);spec(Q,120,135,['COUNT-API']);spec(Q,157,167,['COUNT-API'])
spec(ML+'MeasureTheory/Integral/Bochner/SumMeasure.lean',175,177,['FINITE-INTEGRAL-API']);spec(ML+'MeasureTheory/Integral/Bochner/SumMeasure.lean',210,219,['FINITE-INTEGRAL-API'])
spec(ML+'MeasureTheory/Function/L1Space/Integrable.lean',48,52,['FINITE-INTEGRAL-API']);spec(ML+'MeasureTheory/Function/L1Space/Integrable.lean',166,169,['FINITE-INTEGRAL-API'])
spec(ML+'Algebra/BigOperators/Ring/Finset.lean',292,293,['COUNT-PRODUCT-SUM-API']);spec(ML+'Algebra/BigOperators/Ring/Finset.lean',298,302,['COUNT-PRODUCT-SUM-API'])
spec(ML+'Analysis/Complex/Exponential.lean',132,137,['COUNT-PRODUCT-SUM-API']);spec(ML+'Analysis/Complex/Exponential.lean',145,147,['COUNT-PRODUCT-SUM-API'])
spec(ML+'Data/Fintype/BigOperators.lean',197,201,['FINITE-CARDINALITY'])
spec(ML+'Data/Fintype/Card.lean',181,183,['FINITE-CARDINALITY']);spec(ML+'Data/Fintype/Card.lean',494,498,['FINITE-CARDINALITY'])
# Actual integral_smul_measure context is an atomic existing pinned API, not a new domain certificate.
basic=ML+'MeasureTheory/Integral/Bochner/Basic.lean'
if basic not in raws:
    b=(ROOT/basic).read_bytes();raws[basic]=b;i=len(inputs);r=f'input.{i:03d}.raw.snapshot';l=f'input.{i:03d}.lf.snapshot'
    with (OUT/r).open('xb') as f:f.write(b)
    with (OUT/l).open('xb') as f:f.write(lf(b))
    inputs.append({'path':basic,'bytes':len(b),'raw_sha256':sha(b),'lf_sha256':sha(lf(b)),
      'raw_snapshot':str((OUT/r).relative_to(ROOT)).replace('\\','/'),'lf_snapshot':str((OUT/l).relative_to(ROOT)).replace('\\','/'),
      'historical_primary_pin_rechecked':False,'kind':'existing_source_API'})
spec(basic,1013,1025,['FINITE-INTEGRAL-API']);spec(basic,1026,1030,reason='EXCLUDED NNReal scalar-measure wrapper; actual count uses ENNReal inverse normalization')
spec(basic,1032,1053,['MAP-INTEGRAL-API'])
SL=UP+'SLT__GaussianPoincare__Limit.lean.raw.snapshot'
spec(SL,1,40,['SLT-LAW-CF']);spec(SL,41,70,['SLT-COS-LIMIT']);spec(SL,71,86,['SLT-LAW-CF'])
spec(SL,87,144,['SLT-LAW-CF']);spec(SL,145,156,['SLT-LAW-CF']);spec(SL,157,217,['SLT-COS-LIMIT']);spec(SL,218,242,['SLT-LIMIT'])
spec(SL,243,249,reason='EXCLUDED subsequent BCF integral lemma: required later entropy adapter, outside current law-limit target')
SRA=UP+'SLT__GaussianPoincare__RademacherApprox.lean.raw.snapshot'
spec(SRA,1,39,['SLT-NU']);spec(SRA,40,109,['SLT-NU']);spec(SRA,110,115,reason='EXCLUDED derived variance restatement; exact CLT consumes genuine moment0/moment2 parents')
SE=UP+'SLT__GaussianPoincare__EfronSteinApp.lean.raw.snapshot'
spec(SE,350,396,['SLT-REAL-PRODUCT'])
BER='AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/BernoulliLogSobolev.lean'
spec(BER,1,24,['PRIOR34-PRIVATE']);spec(BER,25,35,reason='EXCLUDED flip definition and flip lemmas, irrelevant to actual count CLT')
spec(BER,36,84,['PRIOR34-PRIVATE']);spec(BER,154,163,['PRIOR34-PRIVATE'])

inventory=[];covered={};spans=[]
for k,(p,lo,hi,ids,reason) in enumerate(coverage_specs):
    raw=raws[p];lines=raw.splitlines(keepends=True)
    # All inputs use CRLF/LF; no CR-only source line accepted without explicit conversion.
    assert b'\r' not in raw.replace(b'\r\n',b''),p
    hi=hi or len(lines)
    assert 1<=lo<=hi<=len(lines),(p,lo,hi,len(lines))
    used=covered.setdefault(p,set());assert not (set(range(lo,hi+1))&used),p;used.update(range(lo,hi+1))
    start=sum(map(len,lines[:lo-1]));end=sum(map(len,lines[:hi]));b=raw[start:end]
    name=f'source-span.{k:03d}.raw.snapshot';nameLF=f'source-span.{k:03d}.lf.snapshot'
    with (OUT/name).open('xb') as f:f.write(b)
    with (OUT/nameLF).open('xb') as f:f.write(lf(b))
    d={'region_id':f'R{k:03d}','path':p,'source_raw_sha256':sha(raw),'raw_physical_line_start':lo,'raw_physical_line_end':hi,
      'raw_byte_start_inclusive':start,'raw_byte_end_exclusive':end,'raw_sha256':sha(b),'lf_sha256':sha(lf(b)),
      'raw_snapshot':str((OUT/name).relative_to(ROOT)).replace('\\','/'),'lf_snapshot':str((OUT/nameLF).relative_to(ROOT)).replace('\\','/'),
      'disposition':'NODE' if ids else 'EXCLUDED','node_ids':ids or [],'reason':reason}
    inventory.append(d)
    for i in ids or []:
        n=next(n for n in nodes if n['id']==i);n.setdefault('source_regions',[]).append(d['region_id'])
    # Static scan only bounded source regions. Comments stripped; no assertion about imported closure.
    text=b.decode(); text=re.sub(r'/\-.*?\-/','',text,flags=re.S);text=re.sub(r'--[^\n]*','',text)
    spans.append({'region_id':d['region_id'],'direct_placeholder_tokens':re.findall(r'\b(?:sorry|admit|axiom)\b',text)})

primary=[]
for p,ids,scope in [
 ('runs/20261007-companion-priority/gaussian-clt-entropy-preread/primary.S4.Ex8.raw.snapshot.html',['PRIMARY-RHO'],'complete actual rho formula'),
 ('runs/20261007-companion-priority/gaussian-clt-entropy-preread/primary.S4.SS1.p4.2.raw.snapshot.html',['PRIMARY-RHO'],'actual standardized law; Hessian0<=rho<=etaI is retained future consumer context, not a scalar CLT premise'),
 ('runs/20261007-companion-priority/gaussian-clt-entropy-preread/primary.S4.E6.raw.snapshot.html',['PRIMARY-FIRST46'],'ONLY FIRST relation; SECOND eta sqrt(E|U|²), THIRD eta sqrt d EXCLUDED later source obligations'),
 ('runs/20261007-companion-priority/gaussian-clt-entropy-preread/primary.S4.SS1.p4.3.raw.snapshot.html',['PRIMARY-FIRST46'],'ONLY FIRST explanation GaussianTalagrand+GaussianLSI; SECOND Lipschitz and LAST Gibbs IBP explanation EXCLUDED current target')]:
    b=raws[p];whole=raws['runs/20261007-companion-priority/gaussian-transport-preread/source-primary.raw.snapshot.html'];offset=whole.find(b)
    assert offset>=0 and whole.find(b,offset+1)<0,p
    primary.append({'path':p,'raw_sha256':sha(b),'lf_sha256':sha(lf(b)),'whole_primary_raw_sha256':sha(whole),
      'whole_primary_byte_start':offset,'whole_primary_byte_end':offset+len(b),'disposition':'NODE','node_ids':ids,'retained_clause_scope':scope,
      'no_printed_scalar_CLT_claim':True})

footprints=[]
for p,used in covered.items():
    count=len(raws[p].splitlines());uncovered=set(range(1,count+1))-used
    def compress(ns):
        out=[]
        for i in sorted(ns):
            if out and i==out[-1][1]+1:out[-1][1]=i
            else:out.append([i,i])
        return out
    footprints.append({'path':p,'full_raw_physical_line_count':count,'declared_bounded_footprint_lines':len(used),
      'declared_bounded_ranges':compress(used),'every_footprint_line_disposed_exactly_once':True,
      'outside_declared_footprint_ranges':compress(uncovered),
      'outside_footprint_status':'EXCLUDED from audit scope: unrelated source regions or transitive imported library proof internals. No exhaustive whole external project claim.'})

inv=put('source-inventory.json',{'actor':ACTOR,'status':'AUTHORED_UNREVIEWED','line_convention':'1-based raw physical LF/CRLF source lines; byte intervals bind original rawbytes',
 'scope':'Exhaustive NODE/EXCLUDED within the declared bounded relevant source footprints; full CLT and independence-CF files enumerated; other bounded API/source windows explicit. Outside ranges expressly excluded from audit scope.',
 'regions':inventory,'primary_balanced_fragments':primary,'footprints':footprints,
 'source_regions_count':len(inventory),'covered_source_lines':sum(len(v) for v in covered.values()),
 'classification':'Source/API reconstruction only; ASTIS private substrate is historical compiled context, not source topology driver or exported35 dependency.'})
graph=put('source-proof-graph.independent.json',{'schema':1,'actor':ACTOR,'role':'SOURCE_GRAPH_AUTHOR_NOT_VALIDATOR','status':'AUTHORED_UNREVIEWED',
 'target':'actual finite Bool normalized-count scalar laws all N, N0 dirac0, successor weak gaussianReal0,1',
 'history':'Author previously authored34 source graph and reviewed35 exact statement after fresh primary contract; did not read any future35 implementation. No selfvalidation of34 or this graph.',
 'source_governance':'Primary SPHMC prints omitted GaussianLSI/Talagrand background only; scalar count CLT is an authored background leaf. Pinned Mathlib proof/API and external SLT law proof fix topology; implementation does not.',
 'nodes':nodes,'edges':edges,'or_hyperedges':alternatives,'compiled_edges':[],
 'source_inventory_binding':inv,'input_bindings_initial':binding,
 'binding_note':'input-bindings.final.json repeats exact complete input set; all sources pinned before graph output; exact final binding in run.json',
 'truth_contract':'API endpoints can be existing Mathlib compiled truth; no ASTIS actual35 producer/adapter proved by this packet. Edges are mathematical source/API dependencies, never Lean implication or a new formalization badge.',
 'public_binder_classification':{'SOURCE':[],'TYPECLASS':'canonical Real and finite Bool/Fin measurable/discrete/typeclass structures implicit in actual definitions, no added generic carrier binder',
 'DEFINITION':['mu_N','sign','S_N','gaussianReal0,1','ProbabilityMeasure weak topology'],'DERIVED':['law family','actual probability','all map identities','N0 dirac','single-coordinate genuine moment/L1 domains','actual CF power','successor convergence'],
 'EXCESS':[],'AUTHORED_EXTENSION':['Bool count carrier adaptation of upstream real product','explicit N0 law','finite-CF/direct-count and infinite-iid route alternatives']},
 'excluded_completion':['Gaussian entropy convergence','flip-energy4 limit','compact GaussianC2 functionLSI','finite-Hilbert/tensorization','literal32 noncompact sqrt-domain/cutoff','GaussianT2','FIRST4.6','bias/main/work/composition'],
 'api_import_closure_boundary':'Existing pinned compiled public Mathlib scalarCLT/Levy/product CF act as mathematical APIs. Selected proof ingredients enumerated; no full transitive Mathlib or external-project rebuild/scan implied.',
 'validation_required':'Fresh distinct phase source-topology reviewer; this author supplies no accepted verdict.'})
finalbinding=put('input-bindings.final.json',{'actor':ACTOR,'inputs':inputs,'input_count':len(inputs),'all_raw_LF_pinned':True,
 'candidate35_implementation_read':False,'compiler_started':False,'initial_binding':binding})
scan=put('bounded-source-placeholder-scan.json',{'actor':ACTOR,'scope':'comment-stripped exact inventory regions only; no production35 or full reachable external closure scan','results':spans,
 'total_direct_placeholder_tokens':sum(len(x['direct_placeholder_tokens']) for x in spans),'not_theorem_completion_evidence':True})
digest=put('bounded-synthesis.json',{'actor':ACTOR,'status':'AUTHORED_SOURCE_DEPENDENCY_PACKET_AWAITING_DISTINCT_REVIEW',
 'smallest_target':'actual normalized-count Rademacher-sum probability laws, exact N0 and successor scalar weak variance1 Gaussian limit',
 'route_at_most_seven_steps':[
 'Derive actual finite carrier cardinality2^N, inverse normalization, measurability and finite L1; construct every lambda_N actualmap.',
 'Handle N0 singleton/empty sum -> true dirac0 separately; positive successor avoids variance1-at0 misuse.',
 'Derive actual one-Bool sign law probability, genuine mean0 and secondmoment1 internally.',
 'Derive actual CF power by authored direct finite-count exp_sum/prod_sum factorization OR true count→real-product map plus pinned pi-sum/scalingCF.',
 'Apply existing compiled Mathlib scalar characteristic-function CLT leaf to the internally derived actual one-coordinate law/moments.',
 'Match literal gaussianReal0,1 variance1 CF and use genuine Levy weak probability-measure topology; infinite iid CLT is an alternative only with extra internal infinite-space/prefix-law adapters.',
 'Compose with successor shift and assemble same actual allN family, N0 and limit; no Gaussian entropy/LSI/T2/4.6 completion follows.'],
 'first_unmet_dependencies':[{'kind':'SOURCE_GAP','id':'GAP-DIRECT-COUNT-CF','residual':'actual finite count characteristic-power adapter absent as exported local producer'},
 {'kind':'SOURCE_GAP','id':'GAP-COUNT-REAL-PRODUCT','residual':'alternative true count/product/sign pushforward equality'},
 {'kind':'SOURCE_GAP','id':'GAP-INFINITE-IID','residual':'alternative actual infinite iid probability construction and same finite-count prefix law'}],
 'local_existing_endpoints':['ProbabilityTheory.tendsto_charFun_inv_sqrt_mul_pow','ProbabilityTheory.charFun_map_sum_pi_eq_prod','MeasureTheory.charFun_map_mul_comp','ProbabilityTheory.charFun_gaussianReal','MeasureTheory.ProbabilityMeasure.tendsto_iff_tendsto_charFun','Fintype.prod_sum','Complex.exp_sum','MeasureTheory.Integrable.of_finite','MeasureTheory.integral_fintype'],
 'prior34_substrate':'Private law/card/integral/snoc/probability helpers are compiled historical patterns only, no exported35 producer or forced Bernoulli LSI dependence.',
 'pins':{'mathlib_revision':'db584cd6d46c92f209a44c0f1c829460d327499d','ASTIS_toolchain':'leanprover/lean4:v4.33.0','SLT_revision':'d0f506f0a695018265dccb33bcb05e2f5ca1c876','SLT_toolchain':'leanprover/lean4:v4.32.0','SLT_mathlib_revision':'81a5d257c8e410db227a6665ed08f64fea08e997','license':'Apache2 exact source/license snapshots; external-reference only; no ML use or whole-project import'},
 'full_truth_boundary':'Scalar lawlimit only. Entropy/energy/compact GaussianLSI/dimension/cutoff/T2/actual FIRST4.6/bias/main/work all OPEN. No new theorem/proof/SAU/compiler/canonical mutation/selfvalidation.',
 'graph':graph,'inventory':inv,'final_input_binding':finalbinding,'placeholder_scan':scan})

# Last raw/LF equality checks are mechanical snapshot checks, not a topology acceptance.
for x in inputs:
    b=(ROOT/x['path']).read_bytes();assert sha(b)==x['raw_sha256'],x['path']
    if x['lf_sha256']:assert sha(lf(b))==x['lf_sha256'],x['path']
runmaterial={'graph':graph,'inventory':inv,'digest':digest,'bindings':finalbinding,'scan':scan,
 'actor':ACTOR,'input_count':len(inputs),'node_count':len(nodes),'edge_count':len(edges),'or_hyperedge_count':len(alternatives),
 'coverage_regions':len(inventory),'coverage_lines':sum(len(x) for x in covered.values()),'compiled_edges_count':0,
 'all_input_hashes_rechecked_unchanged':True,'compiler_started':False,'self_validation':False}
runhash=sha(json.dumps(runmaterial,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode())
receipt=put('run.json',dict(runmaterial,deterministic_run_sha256=runhash,status='CLOSED_AUTHOR_SOURCE_ONLY'))
lease=json.loads((OUT/'author.lease.json').read_bytes())
lease.update(status='CLOSED',read_lease='CLOSED',write_lease='CLOSED',compiler_lease='CLOSED',compiler_started=False,
 closed_utc=datetime.datetime.utcnow().isoformat()+'Z',deterministic_run_sha256=runhash,run_receipt=receipt,
 outcome='Source graph AUTHORED_UNREVIEWED; distinct phase review required; no theorem/compile/source-topology acceptance')
(OUT/'author.lease.json').write_text(json.dumps(lease,sort_keys=True,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'graph':graph,'inventory':inv,'run':receipt,'runhash':runhash,'counts':{k:runmaterial[k] for k in ['input_count','node_count','edge_count','or_hyperedge_count','coverage_regions','coverage_lines']},'all_leases':'CLOSED'},indent=2))
