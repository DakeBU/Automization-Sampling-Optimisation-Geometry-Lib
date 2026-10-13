from pathlib import Path
import hashlib
import json
import re

ROOT = Path('E:/Samplinglib')
OUT = ROOT / 'runs/20261007-companion-priority/pbps-actual-countable-endpoint105/next-primary106'
BASE = 'runs/20261007-companion-priority/'
PRIMARY = BASE + 'phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'
OLD = BASE + 'pbps-actual-normalized-endpoint104/next-primary105/'
TOP = BASE + 'pbps-countable-endpoint-preread105/independent-header-math105/source-topology-admission105.native.json'
PROD = 'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualCountableEndpointLaw.lean'
ML = '.lake/packages/mathlib/Mathlib/'
inputs = {}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def bind(path):
    p = ROOT / path
    data = p.read_bytes()
    result = {'path': path, 'raw_sha256': sha(data), 'bytes': len(data)}
    inputs[path] = result
    return result


def read(path):
    bind(path)
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


def write(name, obj):
    p = OUT / name
    assert not p.exists(), p
    p.write_bytes((json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
    return {'path': p.relative_to(ROOT).as_posix(), 'raw_sha256': sha(p.read_bytes()), 'bytes': p.stat().st_size}


primary = bind(PRIMARY)
assert primary['raw_sha256'] == 'd81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
raw = (ROOT / PRIMARY).read_bytes()
inventory = read(OLD + 'source-coverage-delta105.native.json')
regions = []
for old in inventory['regions']:
    row = {k: v for k, v in old.items() if not k.startswith('disposition')}
    assert sha(raw[row['byte_start']:row['byte_end_exclusive']]) == row['raw_sha256']
    regions.append(row)
assumptions = [
    'E finite-dimensional real inner-product space with its Borel measurable space; dimension zero allowed.',
    'V:E→ℝ; α,β:ℝ≥0; η:ℝ. Original six analytic binders: 0<(α:ℝ), α≤β, ContDiff ℝ 2 V,',
    '∀x,v, (α:ℝ)*‖v‖² ≤ (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β:ℝ)*‖v‖², 0<η, (β:ℝ)*η≤1.'
]
reds = [
    'Actual process Markov/restart/Chapman–Kolmogorov and semigroup composition.',
    'Identification with the separately existential ActualPhaseTransitionKernel witness without a same-witness or a.e.-identification argument.',
    'L² representative extension, bounded operators, adjoints and the full operator equality A3.',
    'Hypocoercivity, implementation errors/caps, unbounded expected costs, full main results and actual-input composition.',
    'Pointwise right-continuous path reversal at genuine jumps, uniform all-parameter null sets, and path-law uniqueness.'
]
freeze = write('primary-first-reconstruction106.native.json', {
    'kind': 'primary-first prospective source reconstruction, no implementation106 exists',
    'author': '/root/source_final96', 'primary': primary, 'source_regions': regions,
    'license': {'url': 'http://arxiv.org/licenses/nonexclusive-distrib/1.0/', 'lines': [257, 258],
                'policy': 'Reference existing pinned HTML only; authored mathematical restatement, no new full source copy.'},
    'reading_order': 'Re-read Appendix A.1 final signed-averaging sentence and A7/A8 mechanism before selecting the next edge; source105 and implementation105 are existing producer interfaces, not a future106 implementation.',
    'reconstruction': [
        'After matching every finite-count term and applying Tonelli to nonnegative terms, the source passes to bounded signed measurable F,G by positive/negative decomposition.',
        'Its displayed identity is ∫ F(z) T_t G(z) dν(z) = ∫ G(Rz) T_t(F∘R)(z) dν(z).',
        'The next sentence takes F=1 to obtain invariance; the subsequent L² extension is a separate obligation.',
        'For the actual global clock witness, Q=law(z,Z_t) and J(z,z′)=(Rz′,Rz), J_*Q=Q supplies precisely the endpoint identity needed. Finite probability bounds permit signed Fubini without an added integrability premise.',
        'ν is invariant under R because its momentum factor is the standard Gaussian. This fact is necessary when turning the F=1 identity into the unchanged Gibbs marginal; it must be derived internally.'
    ], 'original_assumptions': assumptions, 'remaining_reds': reds,
    'new_header_seen': False, 'new_implementation_seen': False, 'proof_credit': False,
    'prior_involvement': 'Authored primary-first105 and independently reviewed bounded105 source/exposition. These do not certify106.'
})

prod = bind(PROD)
assert prod['raw_sha256'] == '31003aa5df1826329f8e57740860e9a0e7c1b866ab110108974e1a339a96bbca'
text = (ROOT / PROD).read_text(encoding='utf-8')
literal = text[text.index('    let c :'):text.index('    ∃ Z :')]
contract = text[text.index('    ∃ Z :'):text.index('      (∀ y r : E, ∀ T : ℝ≥0,')]
assert len(re.findall(r'^    let ', literal, re.M)) == 37
context = write('literal-definition-context106.native.json', {
    'kind': 'Existing actual105 inputs and exact witness prefix, not a Lean header or proposed proof',
    'producer': prod, 'literal37_LF_text': literal, 'literal37_LF_sha256': sha(literal.encode()),
    'global_witness_prefix_LF_text': contract, 'global_witness_prefix_LF_sha256': sha(contract.encode()),
    'normalization': 'Only universal newline conversion of existing CRLF text; original file RAW separately pinned.',
    'retained_definitions': 'The 34 actual recursion/path/density definitions of93, followed by literal R, Vy and nu of105. Count/simplex auxiliaries retain their old meanings even though the new export does not restate the count expansion.',
    'new_mathematical_definition': 'For fixed y,r,T and the SAME produced Z, T_Z G(z) := ∫ w, G(Z y r z T w) ∂P, a real Bochner integral. Set e_Z(z,w)=Z y r z T w.',
    'internal_only_105_objects': 'M(z,w)=(z,Z y r z T w); Q=map M ((nu y).prod P); J(a,b)=(R b,R a). These literal definitions are used to consume105; no arbitrary Q or Z is a theorem input.',
    'witness_contract': 'One Z exists outside all y,r,z,T and observable quantifiers. Keep joint measurability, pointwise live-arc formula, pointwise no-cover fallback, and for each fixed y,r,z the P-a.e. zero-time law exactly as in the copied prefix. No exchange of ∀ and a.e.'
})

slots = {
    'objects': 'Actual PBPS recursion on H=E×E and Ω=ℕ→ℝ with P=infinitePi Exp(1), the same global actual Z, R(x,p)=(x,-p), literal normalized ν_y=tilted(-Vy)×stdGaussian, and real clock expectation T_Z.',
    'domains': 'All y,r∈E, all finite T∈ℝ≥0, all rank(E)≥0. F,G:H→ℝ are Borel measurable and bounded everywhere by finite nonnegative real C_F,C_G. No continuity, sign, compact-support, positive-rate or positive-horizon restriction.',
    'quantifiers': 'Original ambient parameters and six analytic binders; literal37 definitions; ∃one global Z with exact105 prefix; ∀y r T, endpoint measure preservation and ∀F G, Measurable F→Measurable G→∀C_F C_G, 0≤C_F→0≤C_G→(∀z,|Fz|≤C_F)→(∀z,|Gz|≤C_G)→the two integrability conclusions and duality.',
    'assumptions': 'Exactly the six analytic source binders. Observable measurability and boundedness describe the source test class. Probability, joint measurability, section integrability, Fubini eligibility and Gaussian flip symmetry are internal producer consequences, never new assumptions.',
    'conclusion': 'For the actual witness, MeasurePreserving e_Z ((ν_y).prod P) ν_y. For every bounded measurable F,G, both z↦Fz*T_ZGz and z↦G(Rz)*T_Z(F∘R)z are ν_y-integrable, and their real integrals are equal.',
    'scopes_senses': 'Fixed-time Gibbs stationarity of the actual clock output and bounded signed bilinear reversal identity. Equality of actual measures, not merely equality of possibly undefined real integrals. No process Markovness, restart, semigroup, L² operator/adjoint or full-paper conclusion.',
    'constant_dependencies': 'Exact Vy=V+‖x-y‖²/(2η), harmonic sqrtη and rate retained from105; P has rate1 and ν has variance1 standard Gaussian momentum. Bounds C_F,C_G are arbitrary explicit test bounds; internal product bound C_F*C_G and expectation bound C_G. No new dimension or time restriction/constant.'
}
expected = write('expected-semantic-slots106.native.json', {
    'primary_first': freeze, 'slots': slots, 'decision': 'PROSPECTIVE_EXPECTATIONS_ONLY',
    'header_or_implementation_review': False, 'remaining_reds': reds
})

retrieved = []


def api(path, names, use, boundary):
    retrieved.append({'file': bind(path), 'declarations': names, 'intended_use': use, 'boundary': boundary})


api(PROD, ['AutoSamplingTheory.ExampleCases.ProximalBPS.ActualCountableEndpointLaw.actual_countable_endpoint_law'],
    'Produce the same global Z and actual Q probability/J preservation; prior count assembly is reused without a new sum/Fubini proof.',
    'Science a6060928c393d3efe4c85d4cab2b9af166ab6b37 assigned for independent exact admission; readiness remains conditional on105 acceptance/delivery.')
api('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPhaseNormalization.lean',
    ['AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhaseNormalization.actual_phase_gibbs_normalization'],
    'Derive probability of the literal ν_y; no arbitrary normalizer.', 'Analytically independent normalization; no process invariance is inferred from it alone.')
clock = 'AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws'
api('AutoSamplingTheory/TechnicalLemmas/Probability/UnitExponentialProduct.lean', [clock],
    'Probability of exact P, giving finite measure/SFinite and total mass1 for signed Fubini, T_Z1=1 and first marginal.', 'No new independence or clock assumption.')
api('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPhaseTransitionKernel.lean',
    ['AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhaseTransitionKernel.actual_phase_transition_kernel'],
    'Existing bounded real-test integrability/expectation-transfer pattern and future kernel consumer.',
    'NOT selected as a direct producer: its independently existential Z cannot be silently identified with105 Z; it does not prove process Markovness.')
api('AutoSamplingTheory/ExampleCases/ProximalBPS/GaussianReflection.lean',
    ['AutoSamplingTheory.ExampleCases.ProximalBPS.GaussianReflection.reflection_preserves_augmentation'],
    'Lines47–55 give a local example of stdGaussian_map neg and map_prod_map.',
    'Public theorem concerns a different augmentation/reflection; do not call its private helpers or mislabel it as phase-flip invariance.')
api('AutoSamplingTheory/TechnicalLemmas/Measure/L2Expectation.lean',
    ['AutoSamplingTheory.TechnicalLemmas.Measure.L2Expectation'], 'Screen existing L² integral interface.',
    'Not a producer for106; no actual operator or representative identification follows from this generic interface.')
api('AutoSamplingTheory/TechnicalLemmas/Probability/KernelReversibility.lean',
    ['isReversible_of_singleton_balance'], 'Screen existing reversibility leaf.',
    'Discrete singleton balance is unsuitable for continuous phase and momentum-flipped endpoint duality.')
api(ML + 'Probability/Distributions/Gaussian/Multivariate.lean', ['ProbabilityTheory.stdGaussian_map'],
    'Apply to LinearIsometryEquiv.neg ℝ to preserve standard Gaussian momentum.', 'Valid in rank0; exact pinned API, no upstream port.')
api(ML + 'MeasureTheory/Measure/Prod.lean',
    ['MeasureTheory.Measure.map_prod_map', 'MeasureTheory.Measure.map_fst_prod', 'MeasureTheory.measurePreserving_fst'],
    'Product phase-flip invariance and optional equivalent marginal derivation.', 'Position-first product order retained; probability P discharges marginal mass factor.')
api(ML + 'MeasureTheory/Integral/IntegrableOn.lean', ['MeasureTheory.Integrable.of_bound'],
    'Finite probability plus AEStronglyMeasurable and bound C_F*C_G yield actual signed integrability.', 'Finite-measure typeclass is proved from103/clock/105, never supplied.')
api(ML + 'MeasureTheory/Integral/Prod.lean',
    ['MeasureTheory.StronglyMeasurable.integral_prod_right\u0027', 'MeasureTheory.Integrable.integral_prod_left', 'MeasureTheory.integral_prod'],
    'Measurable clock expectations, outer L¹ and signed Fubini.', 'The left projection integrates out the right/clock factor; do not confuse the similarly named integral_prod_right lemma.')
api(ML + 'MeasureTheory/Integral/Bochner/Basic.lean',
    ['MeasureTheory.integral_map_of_stronglyMeasurable', 'MeasureTheory.integral_map', 'MeasureTheory.norm_integral_le_of_norm_le_const'],
    'Transfer bounded signed test on actual Q through M and J and bound clock expectation.',
    'Avoid MeasurePreserving.integral_comp unless its extra MeasurableEmbedding argument has been proved; integral_map suffices.')
api(ML + 'MeasureTheory/Function/L1Space/Integrable.lean', ['MeasureTheory.integrable_const', 'MeasureTheory.Integrable.mono\u0027'],
    'Alternative bounded domination route.', 'No signed-integral equality justified solely by Bochner totalization.')
catalog = bind('research-wiki/external-lean-libraries/README.md')
retrieval = write('retrieval106.native.json', {
    'kind': 'bounded local and repository-pinned Mathlib retrieval; no proof credit',
    'toolchain': bind('lean-toolchain'), 'manifest': bind('lake-manifest.json'), 'catalog': catalog,
    'searches': ['PBPS files for actual kernel/physical interfaces, reversal, duality and stationarity',
                 'TechnicalLemmas Measure/Probability/StochasticProcesses for existing reversibility and L² expectation',
                 'Pinned Mathlib Integral/Prod, Bochner/Basic, IntegrableOn, Measure/Prod and Gaussian/Multivariate'],
    'results': retrieved, 'upstream_policy': 'Local fixed Mathlib already supplies required generic analysis; no compatible external library port is needed. Catalog is reference-only.',
    'canonical_API_gap': 'No new generic analytic API gap found. Actual bounded signed duality and actual fixed-time ν marginal are still unimplemented. Separate kernel witness identification remains a later obligation, not an added assumption.'
})

top = read(TOP)
oldgraph = bind(BASE + 'pbps-countable-endpoint-preread105/source-graph-repair105/source-proof-graph-delta105.v2.native.json')
coverage105 = bind(BASE + 'pbps-actual-countable-endpoint105/final-source105/compiled-source-coverage105.native.json')
newnodes = [
    {'id': 'SIGNED-FUBINI106', 'kind': 'required-internal-adapter',
     'content': 'For the same actual Z and bounded measurable real F,G, derive section/product integrability, measurable bounded clock expectations and signed endpoint-to-iterated integral transfer.'},
    {'id': 'PHASE-FLIP106', 'kind': 'required-internal-adapter',
     'content': 'R preserves literal ν_y via standard Gaussian negation and position-first product map.'}
]
groups = [
    {'target': 'SIGNED-FUBINI106', 'parents': ['COUNT93', 'NORM', clock, 'ENDPOINT-LAW105'],
     'mechanism': '105 exposes the COUNT93 same-Z joint measurability;103 supplies ν probability; clock supplies P probability;105 supplies Q probability. Bounds give honest signed L¹ and Fubini.'},
    {'target': 'PHASE-FLIP106', 'parents': ['NORM'],
     'mechanism': 'Use exact ν product definition and fixed Mathlib stdGaussian_map neg plus map_prod_map; probability is available but no extra public premise is needed.'},
    {'target': 'AVG100', 'parents': ['ENDPOINT-LAW105', 'SIGNED-FUBINI106'],
     'mechanism': 'J_*Q=Q applied to F(start)G(end), with real integral_map and signed Fubini, gives the source bounded bilinear identity.'},
    {'target': 'INV100', 'parents': ['AVG100', 'PHASE-FLIP106', 'COUNT93', 'NORM', clock],
     'mechanism': 'Take F=1, use T_Z1=1 and R_*ν=ν. Apply bounded indicator tests to identify map e_Z (ν×P)=ν; joint Z gives measurability. Equivalent direct first/second marginal argument from105 may replace this local route, but must be recorded if implemented.'}
]
edges = sorted({(p, g['target']) for g in groups for p in g['parents']})
baseedges = {tuple(e) for e in top['effective_graph']['edges']}
deltaedges = [list(e) for e in edges if e not in baseedges]
graph = write('source-proof-graph-delta106.native.json', {
    'kind': 'prospective source-proof graph delta only', 'author': '/root/source_final96',
    'base_v2_graph105': oldgraph, 'independent_base_topology105': inputs[TOP],
    'inherited_compiled_source_coverage105': coverage105,
    'inherited_count': {'nodes': 60, 'edges': 112}, 'inherited_nodes': top['effective_graph']['nodes'],
    'new_nodes': newnodes, 'AND_dependency_groups': groups, 'new_edges': deltaedges,
    'refined_existing_targets': {
        'AVG100': 'Selected106 source lines3215–3224 bounded signed bilinear identity; reuse canonical identity rather than add a duplicate averaging node.',
        'INV100': 'Selected106 fixed-time actual Gibbs phase marginal only; it is not a semigroup/restart or L² conclusion.',
        'L2A3': 'Still future, requires additional operator/domain work; inherited AVG100/INV100 edges are necessary inputs, not completion.',
        'RESTART': 'Still future and independent of this fixed-time proof.'},
    'unchanged_node_policy': 'All 60 inherited identities and112 edges remain bound through independent105 topology. TIME97 stays canonical; no rho alias duplicate. Existing source-level alternative-route edges are retained as source coverage, not asserted new direct Lean calls.',
    'actual_direct_producers_proposed': [retrieved[0], retrieved[1], retrieved[2]],
    'same_witness_edge': 'COUNT93 enters106 only through the global Z returned by105, never by separately obtaining another93 or83 witness.',
    'api_dependencies': retrieval, 'topology_status': 'PROPOSED_REQUIRES_SEPARATE_INDEPENDENT_REVIEW',
    'self_topology_validation': False, 'certified_new_Lean_edges': 0, 'proof_credit': False
})

selected = {'weight-matching-and-invariance', 'average', 'phase-gibbs-law'}
for row in regions:
    rid = row['id']
    if rid == 'weight-matching-and-invariance':
        disp = 'Selected changed slice3215–3227: bounded signed duality and F=1 fixed-time invariance; earlier weight matching reused101/102, trailing L² extension excluded.'
    elif rid == 'average':
        disp = 'Gibbs initial averaging inherited105; signed Fubini now identifies the actual clock expectation. No new count resummation.'
    elif rid == 'phase-gibbs-law':
        disp = 'Use103 normalized product law; derive standard-Gaussian momentum-flip invariance internally.'
    elif rid in ['standing-curvature', 'standing-eta']:
        disp = 'Retain original six analytic assumptions exactly; none strengthened.'
    elif rid in ['actual-phase', 'event-convention', 'prescribed', 'simplex']:
        disp = 'Inherited actual105 literal definitions/global witness; no change of jump representative, strict simplex, zero count or fallback.'
    elif rid == 'A3-boundary':
        disp = 'Context/future only: no L² operator or actual Markov semigroup theorem is selected.'
    elif rid == 'source-license':
        disp = 'Retain exact license reference; do not duplicate full primary.'
    else:
        disp = 'Unchanged source producer mechanism already covered by105 inherited graph and coverage; not reproved or recredited in106.'
    row['disposition106'] = disp
coverage = write('source-coverage-delta106.native.json', {
    'kind': 'exhaustive prospective source-region disposition, not compiled106 coverage',
    'primary': primary, 'inherited21_inventory': inputs[OLD + 'source-coverage-delta105.native.json'],
    'all21_slices_rechecked': True, 'regions': regions, 'source_graph_delta': graph,
    'inherited60_nodes': [{'id': n, 'disposition': 'selected bounded target' if n in ['AVG100', 'INV100'] else 'future excluded target' if n in ['L2A3', 'RESTART'] else 'unchanged inherited producer/source-route coverage'} for n in top['effective_graph']['nodes']],
    'new_nodes': newnodes, 'remaining_reds': reds, 'implementation106_exists': False,
    'self_topology_validation': False, 'proof_credit': False
})

recommendation = write('recommendation106.native.json', {
    'kind': 'ONE bounded source-only next-edge recommendation, not an SAU claim',
    'title': 'Actual bounded signed Gibbs duality and fixed-time phase invariance',
    'source': primary, 'primary_first': freeze, 'expected_slots': expected, 'literal_context': context,
    'original_assumptions': assumptions,
    'complete_prospective_statement': [
        'Under exactly the original ambient types and six analytic binders, retain the 37 literal definitions in literal-definition-context106.',
        'There exists ONE Z:E→E→H→ℝ≥0→Ω→H satisfying the exact copied global measurability/live-arc/fallback/parameterwise zero-time contract of105.',
        'For every y,r:E and T:ℝ≥0 let T_ZG(z)=∫w G(Z y r z T w) dP(w), and e_Z(z,w)=Z y r z T w.',
        'MeasurePreserving e_Z ((ν_y).prod P) ν_y.',
        'For every F,G:H→ℝ with Measurable F and Measurable G, and every C_F,C_G:ℝ with 0≤C_F,0≤C_G, (∀z,|Fz|≤C_F),(∀z,|Gz|≤C_G), both z↦Fz*T_ZGz and z↦G(Rz)*T_Z(F∘R)z are Integrable with respect toν_y, and their real integrals are equal.'
    ],
    'quantifier_detail': 'No supplied Z/Q/density/kernel, integrability, finite mass, rate positivity or Gaussian symmetry assumption. Observable hypotheses belong inside the universal observable conclusion, not additional analytic binders. Z exists before all parameters and observables.',
    'proof_route_at_most_seven_steps': [
        'Consume105 once to get the global actual Z, actual endpoint Q probability and J_*Q=Q, retaining the exact witness contract.',
        'Use103 and clock public probability to establish ν/P finite and SFinite; use pinned Gaussian negation and product map for R_*ν=ν.',
        'For arbitrary source-bounded measurable F,G, prove section and product integrability from explicit finite bounds. Joint Z makes T_ZG measurable; norm-integral bound gives |T_ZG|≤C_G.',
        'Transfer f(start,end)=F(start)*G(end) through the actual M and apply signed Fubini to identify ∫f dQ with ∫F*T_ZG dν; repeat for f∘J with the same bounds.',
        'Use J_*Q=Q and real integral_map to derive the bounded signed bilinear identity and the two explicit outer L¹ conclusions.',
        'Set F=1, use P total mass1 and R_*ν=ν; bounded indicator tests identify the actual endpoint pushforward withν. Its measurable map yields MeasurePreserving.',
        'Retain the zero-time, fallback and live-arc contracts from the same Z; document rank0, T0 and inherited n0 handling and stop before L²/restart/semigroup work.'
    ],
    'why_substantive': '105 only supplies nonnegative countable endpoint measure assembly and flipped reversal.106 removes the actual bounded signed averaging and actual Gibbs marginal blocker, with genuine L¹/Fubini and normalization-symmetry obligations; it is not an F=f*g(B) fixed-sector wrapper or a mass corollary.',
    'real_consumers': ['Source final Appendix A.1 bounded bilinear formula and F=1 fixed-time Gibbs stationarity.', 'Future L² contraction/adjoint extension can use invariant actual phase measure and bounded duality, once its own representation/operator contracts are proved.', 'Future actual kernel invariance requires compatible same-Z kernel construction or independently proved witness identification; existing83 cannot be silently substituted.'],
    'edge_cases': {'rank0': 'Standard Gaussian negation and phase product remain valid on the one-point space; no dimension positivity.',
                   'T0': 'The parameterwise P-a.e. initialization and joint measurability suffice for Gibbs averaging; no uniform all-z null set assumed.',
                   'n0': 'No n binder in new final result;105 count assembly already includes the empty tuple/zero-event sector.',
                   'zero_bounds': 'F or G may vanish; no division by bounds or rates.',
                   'jumps': 'Only fixed-time output law is used; no right-continuous pathwise reversal equality.',
                   'noncover': 'Pointwise fallback is retained and inherited actual a.e. laws handle exceptional clock paths.'},
    'source_gap': 'The printed passage suppresses finite signed-integral and normalized momentum symmetry details. Existing105/103/clock and fixed Mathlib can discharge them internally. No missing source assumption identified. Full Markov/L² semantics are not licensed by fixed-time endpoint laws.',
    'readiness': 'Conditional on105 independent exact admission and serialized delivery; source-only recommendation may be reviewed now but does not authorize a new claim or parallel proof.',
    'retrieval': retrieval, 'graph': graph, 'coverage': coverage, 'remaining_reds': reds,
    'proof_credit': False, 'new_header': False, 'new_implementation': False, 'self_topology_validation': False
})

# Preserve only bounded scheduling excerpts because root is integrating105 concurrently.
front = (ROOT / 'website/content/samplewiki_companion_frontiers.json').read_bytes()
handoff = (ROOT / 'docs/companion-papers-handoff.md').read_bytes()
scheduling = write('scheduling-context106.native.json', {
    'kind': 'context only, not mathematical premises or acceptance evidence',
    'frontier_observed_raw_sha256': sha(front),
    'execution_snapshot': json.loads(front)['execution'],
    'handoff_observed_raw_sha256': sha(handoff),
    'handoff_current_section': handoff.decode('utf-8').split('\n## ', 2)[0:2],
    'parent_assignment': '105 science a6060928c393d3efe4c85d4cab2b9af166ab6b37; exact verifier and sole-root integration pending at assignment.104 delivered c4f862780fe019fa63be24026e1e4eef9318fcad.',
    'mutable_context_policy': 'These preserved excerpts are scheduling snapshots only. The full mutable files are deliberately not selected immutable mathematical input references.'
})
run = write('source-preread-run106.native.json', {
    'author': '/root/source_final96', 'mode': 'primary-first source-only next-edge preread',
    'primary_first': freeze, 'expected_slots': expected, 'recommendation': recommendation,
    'graph': graph, 'coverage': coverage, 'retrieval': retrieval, 'scheduling': scheduling,
    'owned_directory': OUT.relative_to(ROOT).as_posix(),
    'independence': {'root_production_writer': True, 'new_implementation_seen': False,
                     'source_graph_creator_self_validated': False, 'new_theorem_claimed': False},
    'new_full_primary_copy': False, 'publication_or_canonical_mutation': False
})
owned = []
for p in sorted(OUT.iterdir()):
    if p.is_file():
        owned.append({'path': p.relative_to(ROOT).as_posix(), 'raw_sha256': sha(p.read_bytes()), 'bytes': p.stat().st_size})
closed = write('closed-RAW-preread106.native.json', {
    'kind': 'immutable source-only106 RAW closure', 'run': run, 'recommendation': recommendation,
    'selected_inputs': list(inputs.values()), 'owned_outputs': owned,
    'no_full_primary_archive': True, 'no_new_Lean_or_header_or_claim': True,
    'topology_review': 'Pending independent reviewer; creator has not validated topology.',
    'closure_self_hash_policy': 'This manifest is externally SHA256-bound; it does not recursively contain its own hash.'
})
print(json.dumps({'recommendation': recommendation, 'graph': graph, 'coverage': coverage, 'run': run, 'closure': closed}, indent=2))
