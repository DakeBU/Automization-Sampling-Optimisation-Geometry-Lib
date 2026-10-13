from pathlib import Path
import hashlib
import json
import datetime

ROOT = Path('E:/Samplinglib')
OUT = ROOT / 'runs/20261007-companion-priority/pbps-actual-normalized-endpoint104/next-primary105'
B = 'runs/20261007-companion-priority/'
PRIMARY = B + 'phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'
COVER104 = B + 'pbps-actual-phase-normalization103/next-primary104/source-coverage-delta104.native.json'
GRAPH104 = B + 'pbps-actual-phase-normalization103/next-primary104/source-proof-graph-delta104.native.json'
TOPO104 = B + 'pbps-normalized-endpoint-preread104/independent-header-math104/topology-binding-check104.native.json'
ADMISSION104 = B + 'pbps-normalized-endpoint-preread104/independent-header-math104/source-topology-admission104.native.json'
COMPILED104 = B + 'pbps-actual-normalized-endpoint104/final-source104/compiled-source-coverage104.native.json'
P93 = 'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteCountPath.lean'
P95 = 'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualBoundedPathExpansion.lean'
P103 = 'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPhaseNormalization.lean'
P104 = 'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualNormalizedEndpointSector.lean'
CLOCK = 'AutoSamplingTheory/TechnicalLemmas/Probability/UnitExponentialProduct.lean'
M = '.lake/packages/mathlib/Mathlib/MeasureTheory/'


def sha(b):
    return hashlib.sha256(b).hexdigest()


def binding(path):
    p = ROOT / path
    b = p.read_bytes()
    return {'path': path, 'raw_sha256': sha(b), 'bytes': len(b)}


def write(name, value):
    p = OUT / name
    assert not p.exists(), 'Do not overwrite closed native evidence: ' + name
    p.write_bytes((json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf8'))
    return binding(p.relative_to(ROOT).as_posix())


def excerpt(path, lo, hi):
    lines = (ROOT / path).read_bytes().splitlines(keepends=True)
    b = b''.join(lines[lo - 1:hi])
    return dict(binding(path), line_start=lo, line_end=hi,
                byte_start=sum(map(len, lines[:lo - 1])), raw_span_sha256=sha(b),
                text=b.decode('utf8'))


primary = binding(PRIMARY)
assert primary['raw_sha256'] == 'd81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
raw = (ROOT / PRIMARY).read_bytes()
regions = json.loads((ROOT / COVER104).read_text(encoding='utf8'))['regions']
for region in regions:
    assert sha(raw[region['byte_start']:region['byte_end_exclusive']]) == region['raw_sha256']
assert len(regions) == 21
assert binding(P104)['raw_sha256'] == 'c2a980f6397528f818120ca6163bf9b286f5c2ef5d4c730d9608267271b03074'
stamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
exclusions = [
    'No theorem/header/Statement Seal/SAU claim or Lean implementation105 exists in this packet.',
    'No pointwise reversal of right-continuous paths at jumps; only endpoint-pair measure reversal.',
    'No sector probability-one assertion; sector subprobability follows only after the actual count/probability argument.',
    'No supplied process, density, joint-count measurability, integrability, normalizer or rate-positivity hypothesis.',
    'No bounded signed bilinear theorem, phase marginal invariance, semigroup/Markov/restart theorem, L2 extension or cost result is claimed.',
    'No full-paper, integration, browser, stabilization, purification or Goal-completion credit.'
]
assumptions = [
    'E is a finite-dimensional real inner-product space, with its Borel measurable structure; rank zero is allowed.',
    'V : E -> real; alpha,beta : nonnegative real; eta : real.',
    'hAlpha: 0 < alpha.',
    'hAlphaBeta: alpha <= beta.',
    'hV: V is C2.',
    'hH: for every x,v, alpha*norm(v)^2 <= D2V(x)[v,v] <= beta*norm(v)^2 (one paired binder).',
    'hEta: 0 < eta.',
    'hBetaEta: beta*eta <= 1.'
]
source_first = write('primary-first-reconstruction105.native.json', {
    'kind': 'independent primary-first prospective reconstruction', 'author': '/root/source_final96',
    'frozen_at_utc': stamp, 'primary': primary, 'source_version': 'arXiv:2609.06905v1',
    'source_license': 'arXiv perpetual non-exclusive distribution; lines257-258; existing local snapshot referenced only.',
    'read_order': 'Original A7/averaging/A8/Tonelli/signed-invariance paragraph first; then actual93/95/103/104 interfaces and pinned Mathlib. No future105 implementation exists or was inspected.',
    'prior_involvement': 'Author reconstructed earlier source graphs and reviewed104; earlier semantic verdict payloads are not decision inputs. Existing graph topology admission is independently authored.',
    'source_reconstruction': [
        'A7 first expands the actual path law at a fixed initial phase into all finite event counts.',
        'The source then integrates the initial phase against the normalized Gibbs phase measure before applying fixed-count reversal.',
        'Nonnegative Tonelli is the mechanism that permits countable assembly under the initial measure. The fixed-initial energy bound is not a uniform Gibbs domination theorem.',
        'Signed bounded bilinear duality and marginal invariance occur after this nonnegative assembly and remain separate consumer boundaries.'
    ],
    'original_assumptions': assumptions, 'all21_source_slices_rehashed': True,
    'changed_slice': ['A7', 'average', 'weight-matching-and-invariance:3210-3215'],
    'no_new_full_primary_copy': True, 'proof_credit': False, 'exclusions': exclusions
})

definitions = write('literal-definition-context105.native.json', {
    'kind': 'existing actual interface definition context, not a new Lean header',
    'actual93_literal_context': excerpt(P93, 1851, 1982),
    'actual93_full_public_contract_location': dict(binding(P93), private_statement_lines=[1851, 2001], public_declaration_line=2005),
    'actual104_literal_endpoint_sector_context': excerpt(P104, 31, 98),
    'convention': 'Reuse exact actual93 recursion, clocks, count selector, prescribed Gamma and rho. Reconcile identically specified Gamma/rho/m in104 by unfolding ordinary literal definitions; never call private mangled declarations.',
    'new_mathematical_notation': {
        'H': 'E x E, position first and momentum second',
        'Omega': 'Nat -> real, product Borel sigma algebra',
        'P': 'Measure.infinitePi (fun _ : Nat => expMeasure (1 : real))',
        'R': 'R(x,p)=(x,-p)',
        'Vy': 'Vy(y,x)=V(x)+norm(x-y)^2/(2*eta)',
        'nu': 'nu_y=((volume : Measure E).tilted (fun x => -Vy(y,x))).prod (ProbabilityTheory.stdGaussian E)',
        'Delta': 'Delta(n,T)={t:Fin n->real | StrictMono(Fin.cons 0 t) and forall i,t(i)<T}; coordinates are zero-based, hence 0<t(0)<...<t(n-1)<T.',
        'm': 'm(n,T)=Measure.comap Subtype.val (volume : Measure (Fin n -> real)); Prefix(n,T) is the Delta subtype.',
        'rho': 'Exact actual93/104 ENNReal q times terminal survival weight, not a freely supplied density and not replaced by a real density.',
        'B': 'B_n(z,t)=(z,Gamma(y,r,z,n,T,t)(<T,le_rfl>))',
        'sigma': 'sigma_n=(nu_y.prod m(n,T)).withDensity (fun (z,t) => rho(y,r,z,n,T,t))',
        'L': 'L_n=Measure.map B_n sigma_n, a measure on H x H',
        'M': 'M_Z(z,w)=(z,Z(y,r,z,T,w))',
        'Q': 'Q(y,r,T)=Measure.map M_Z (nu_y.prod P)',
        'J': 'J(z0,zT)=(R(zT),R(z0))'
    },
    'actual_Z_contract': [
        'Exists one Z:E->E->H->NNReal->Omega->H before forall y,r,T.',
        'Jointly measurable in ((y,r),z,s,w), with the exact actual93 product association.',
        'For all y,r,z,w,s,n,a: w in I(y,r,z,s,n) and record(y,r,z,epsilon(w),n)=live(a) imply Z(y,r,z,s,w)=Phi(y,r,(s-a.time : NNReal),a.phase).',
        'If no such I sector exists at s, Z(y,r,z,s,w)=z.',
        'For every y,r,z, Z(y,r,z,0,w)=z for P-almost every w.'
    ],
    'no_arbitrary_provider_binder': True
})

slots = {
    'objects': 'Actual stopped exponential-clock PBPS witness Z, actual prescribed Gamma/rho, conditional Gibbs position times standard Gaussian, and the endpoint pair law Q.',
    'domains': 'Finite-dimensional real E (rank0 allowed), H=E x E, Omega=Nat->real, n:Nat, T:NNReal, strict Prefix(n,T); measures on H x H in initial/terminal order.',
    'quantifiers': 'Original six analytic binders; exists one global measurable actual Z with arc/fallback/zero properties; for every y,r:E and T:NNReal, the three endpoint-law conclusions. Count n is summed over all Nat, with no cap.',
    'assumptions': 'Only the original six analytic assumptions plus ambient typeclass structure. Clock probability, normalizability, count disjointness, measurable sector integrals and all measures are proved/defined internally.',
    'conclusion': 'Q=Measure.sum(fun n=>L_n) AND IsProbabilityMeasure Q AND MeasurePreserving J Q Q.',
    'scopes': 'One actual normalized countable endpoint-law assembly edge. Equality is equality of measures, and reversal is endpoint-pair measure preservation. No pathwise jump reversal or process/Markov invariance theorem.',
    'constant_dependencies': 'Exact sqrt(eta) dynamics/rate, expMeasure rate1, eta quadratic coefficient1/(2eta), momentum1/2, standard Gaussian, no new constants or uniform energy/rate bounds. r is arbitrary and fixed inside each endpoint law.'
}
expected = write('expected-semantic-slots105.native.json', {'kind': 'prospective source-only seven slots', 'primary_first': source_first, 'semantic_slots': slots, 'proof_credit': False})

apis = [
    (M + 'Measure/Prod.lean', "Measurable.lintegral_prod_right'", 123, 'Joint measurable nonnegative integrand; SFinite measure integrated out. Derives initial-phase measurability of each sector integral.'),
    (M + 'Measure/Prod.lean', 'MeasureTheory.lintegral_prod', 1006, 'Tonelli for AEMeasurable nonnegative product integrand with SFinite second measure; no signed integrability.'),
    (M + 'Integral/Lebesgue/Add.lean', 'MeasureTheory.lintegral_tsum', 360, 'Countable family of AEMeasurable ENNReal functions; no domination assumption.'),
    (M + 'Integral/Lebesgue/Basic.lean', 'MeasureTheory.lintegral_iUnion', 584, 'Measurable pairwise-disjoint count fibers; their union is all Omega since N is Nat-valued.'),
    (M + 'Integral/Lebesgue/Basic.lean', 'MeasureTheory.lintegral_sum_measure', 443, 'Integral over Measure.sum equals countable sum, without finite total mass premise.'),
    (M + 'Integral/Lebesgue/Basic.lean', 'MeasureTheory.Measure.ext_of_lintegral', 571, 'Equality on every measurable ENNReal test identifies measures.'),
    (M + 'Measure/AEMeasurable.lean', 'MeasureTheory.Measure.map_sum', 434, 'Requires AEMeasurable J for the sum measure; literal J is globally measurable.'),
    (M + 'Measure/Typeclasses/Probability.lean', 'MeasureTheory.Measure.isProbabilityMeasure_map', 124, 'AEMeasurable actual endpoint map and probability source product.'),
    (M + 'Measure/WithDensity.lean', 'MeasureTheory.lintegral_withDensity_eq_lintegral_mul', 398, 'Measurable density and test; exact ENNReal factor order can be commuted.'),
    (M + 'Integral/Lebesgue/Map.lean', 'MeasureTheory.lintegral_map', 27, 'Measurable endpoint map and measurable test.'),
    (M + 'Measure/Restrict.lean', 'map_comap_subtype_coe', 950, 'Global declaration; measurable strict simplex maps comap to restricted volume.'),
    (M + 'Measure/Typeclasses/SFinite.lean', 'MeasureTheory.SigmaFinite.of_map', 660, 'Recovers sigma-finiteness of actual simplex comap from its sigma-finite mapped measure.')
]
retrieval = write('retrieval105.native.json', {
    'kind': 'local and fixed-Mathlib API retrieval; no proof execution',
    'selected_actual_public_producers': [
        dict(binding(P93), declaration='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteCountPath.actual_finite_count_path_law', use='One jointly measurable actual Z and actual prescribed Gamma/rho; fixed-count ENNReal test identity and measurable Nat count; single producer witness throughout.'),
        dict(binding(P103), declaration='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhaseNormalization.actual_phase_gibbs_normalization', use='Actual nu_y probability by the exported normalized-density/product identification.'),
        dict(binding(P104), declaration='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualNormalizedEndpointSector.actual_normalized_endpoint_sector_reversal', use='For each n, J preserves the literal normalized endpoint sector L_n.'),
        dict(binding(CLOCK), declaration='AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws', use='Actual infinite Exp(1) product is probability; no supplied clock-law premise.')
    ],
    'actual95_comparison': dict(binding(P95), declaration='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBoundedPathExpansion.actual_bounded_path_functional_expansion', source='A7', finding='Full bounded signed path expansion and absolute summability already hold at fixed initial phase. Initial-phase integration of the series is not itself exported. For105 the nonnegative count law93 supplies the needed stronger measure-level route directly, without a second existential Z alignment or a fabricated95 dependency.'),
    'mass_candidate_rejected_as_separate_SAU': '93 already proves integral rho dm=P{N=n}<=1 at fixed initial phase. Averaging against the actual probability nu gives sector subprobability directly; this is an ingredient/corollary rather than the next substantive independent SAU.',
    'local_search': 'Searched ProximalBPS and shared probability/measure APIs for countable endpoint law, Measure.sum, map_sum and lintegral_iUnion. No existing actual normalized countable endpoint-law theorem found; actual104 is fixed n only.',
    'compatible_external_catalog': dict(binding('research-wiki/external-lean-libraries/README.md'), decision='Pinned local Mathlib already supplies all required generic operations. No external theorem import, port, floating upstream retrieval or private mangled API proposed.'),
    'mathlib_toolchain': [binding('lean-toolchain'), binding('lake-manifest.json')],
    'apis': [dict(binding(p), declaration=n, line=line, contract=contract) for p, n, line, contract in apis],
    'namespace_checks': 'Measurable.lintegral_prod_right\' and map_comap_subtype_coe are root declarations; Measure.map_sum is inside MeasureTheory.Measure. Names checked in pinned files, not inferred from prose.',
    'new_compilation': False
})

route = [
    'Extract the single actual93 Z with joint measurability, arc/fallback/zero characterization, joint Gamma/rho and fixed-count nonnegative test identity. Keep all coordinates literal.',
    'Use actual103 and UnitExponentialProduct to derive nu_y and P probability internally; the joint Z makes M_Z measurable, hence Q is probability.',
    'For fixed n,T derive sigma-finiteness of the strict-simplex comap, and joint measurability of f(z,Gamma(z,t)(T))*rho(z,t). Apply Measurable.lintegral_prod_right\' for the initial-phase sector integral.',
    'For each fixed z, partition Omega by the measurable disjoint fibers {N(T)=n}, whose union is univ. Apply actual93 with F(history,path)=f(z,path(T)) and lintegral_iUnion to get the countable nonnegative endpoint expansion.',
    'Integrate that identity against nu_y. Use lintegral_tsum and product Tonelli, then exact map/withDensity integral identities, to identify the right side with integral f against sum L_n. Measure.ext_of_lintegral gives Q=sum L_n.',
    'Use actual104 separately for every n to obtain MeasurePreserving J L_n L_n. J is the same literal globally measurable flipped swap for all n.',
    'Apply Measure.map_sum and each sector map equality; rewrite using Q=sum L_n and package the assembly, probability and endpoint-pair reversal for the same actual Z.'
]
recommendation = write('recommendation105.native.json', {
    'kind': 'one bounded source-only next-edge recommendation', 'selected_edge': 'actual normalized countable endpoint-pair law assembly and reversal',
    'primary_first': source_first, 'expected_slots': expected, 'literal_definition_context': definitions, 'retrieval': retrieval,
    'complete_statement_conditions': assumptions, 'statement': slots['quantifiers'] + ' Conclusion: ' + slots['conclusion'],
    'actual_process_identification': 'All five Z clauses in literal-definition-context are retained: existential global witness, joint measurability, actual arc formula, fallback, and a.e. zero-time initialization. An arbitrary Z binder or merely existential reversible law would not meet the source target.',
    'why_one_substantive_edge': 'Identifies the actual Gibbs-initialized clock process law with the countable sum of previously reversed sectors. Probability is obtained from the actual initial/clock product, and sector reversal then transfers to that same law. This removes the countable-assembly blocker rather than wrapping104 with a test function or proving only a short averaged mass bound.',
    'internal_not_public_assumptions': ['Joint endpoint/density measurability', 'Measurable count fibers at each initial phase', 'Measurable initial-phase sector integrals', 'Sigma-finite actual simplex measure', 'Probability of nu_y and P', 'Exact literal alignment of93/104 sector definitions', 'Countable exchange and countable map identity'],
    'joint_count_measurability': 'No joint-in-z measurability of N is assumed or needed: use its fixed-z measurable fibers first, then the jointly measurable Gamma/rho sector integral. Joint Z supplies the measurable left side.',
    'real_consumer': 'Future AVG100 bounded bilinear endpoint duality can integrate f(z0,zT)=F(z0)G(zT) against this actual probability law. Only after that or a separate marginal argument may actual phase invariance be asserted. No T_t Markov kernel is silently introduced.',
    'route_at_most_seven_steps': route,
    'edge_cases': {
        'n0': 'Prefix(0,T) is a singleton; empty event product=1. The n0 sector is included literally, never discarded.',
        'T0': 'Positive-count strict simplexes are empty. Zero-time actual initialization is a.e.; Q is the diagonal pushforward of nu, and the selected identities retain T=0.',
        'rank0': 'E may have rank0; standard Gaussian and Gibbs laws are the singleton probabilities. No positive-dimension binder.',
        'zero_rate': 'No positivity of rate; zero-gradient reflection convention and infinite first wait are retained. Absorbing stopped records and default count/path values on null bad events remain literal.',
        'jump_endpoints': '93 null event-time facts support actual count-sector equality. No equality of reversed right-continuous paths at every time is inferred.',
        'infinite_ENNReal_tests': 'Measure extensionality may use arbitrary measurable ENNReal tests, even unbounded; positive Tonelli suffices. Source bounded positive tests are included, and bounded signed integrability is a later consequence of probability, not an assumption.'
    },
    'precise_source_gap': 'The prose passes from fixed-initial A7 to averaging and termwise reversal. Formal completion needs joint measurable actual endpoint/density, measurable parameter integrals, and countable nonnegative exchange. Its fixed-initial energy-dependent rate bound does not authorize a uniform initial-phase signed dominating function. Existing93 plus Tonelli resolves this gap without new public hypotheses.',
    'readiness': 'Mathematically dependency-ready conditional on exact admission and delivery of104 by the owner. This packet does not assert104 integration completion or schedule/claim105.',
    'exclusions': exclusions, 'proof_credit': False, 'self_topology_validation': False
})

clock_id = 'AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws'
new_nodes = [
    {'id': 'COUNT93', 'kind': 'existing-public-projection', 'content': 'Same actual93 witness: jointly measurable actual Z and Gamma, fixed-count ENNReal test law, measurable Nat count and exact mass. Distinct from PATH93 interpolation and MEASDENS93 rho measurability.'},
    {'id': 'SECTOR-INTEGRAL-MEAS105', 'kind': 'required-adapter', 'content': 'Joint endpoint-test times actual density and sigma-finite simplex yield measurable initial-phase sector integrals.'},
    {'id': 'ASSEMBLY105', 'kind': 'selected-internal-edge', 'content': 'Pointwise count partition plus initial-phase Tonelli identifies actual Q with sum L_n.'},
    {'id': 'ENDPOINT-LAW105', 'kind': 'selected-public-edge', 'content': 'Same actual countable endpoint law Q is probability, equals sum L_n, and is preserved by J.'},
    {'id': clock_id, 'kind': 'existing-public-producer', 'content': 'Actual infinite Exp(1) product probability; no mathematical proof credit105.'}
]
groups = [
    {'target': 'COUNT93', 'parents': ['H99', 'D99'], 'mechanism': 'Project existing actual93 public theorem, with all six original assumptions and literal recursion.'},
    {'target': 'SECTOR-INTEGRAL-MEAS105', 'parents': ['COUNT93', 'MEASDENS93', 'D99'], 'mechanism': 'COUNT93 supplies actual joint Gamma, not merely path interpolation; MEASDENS93 supplies rho. Measurable simplex/SFinite and Measurable.lintegral_prod_right\' are local fixed-Mathlib ingredients.'},
    {'target': 'ASSEMBLY105', 'parents': ['COUNT93', 'SECTOR-INTEGRAL-MEAS105', 'NORM', 'D99'], 'mechanism': 'Actual clock count law plus normalized initial measure, fixed-z count union, then Tonelli and lintegral_tsum. No joint-count premise.'},
    {'target': 'ENDPOINT-LAW105', 'parents': ['ASSEMBLY105', 'ENDPAIR104', 'COUNT93', 'NORM', clock_id], 'mechanism': 'Probability from actual measurable product pushforward; reversal from map_sum of actual104 sectors. Same Z in all clauses.'}
]
edges = [{'source': p, 'target': g['target'], 'logic': 'AND', 'certified_Lean_edge': False} for g in groups for p in g['parents']]
graph = write('source-proof-graph-delta105.native.json', {
    'kind': 'source-first prospective graph delta', 'author': '/root/source_final96',
    'base_source_graph104': binding(GRAPH104), 'independent_base_topology_binding': binding(TOPO104), 'independent_base_topology_admission': binding(ADMISSION104),
    'inherited_compiled_coverage': binding(COMPILED104), 'inherited_count': {'nodes': 55, 'edges': 96},
    'new_nodes': new_nodes, 'AND_dependency_groups': groups, 'producer_edges': edges,
    'future_consumer_edges': [{'source': 'ENDPOINT-LAW105', 'target': 'AVG100', 'kind': 'future-needed-input', 'certified_Lean_edge': False}],
    'stable_identity_policy': 'Retain all55 base identities and96 edges. TIME97 remains canonical; RHO97 remains an alias. NORM has no102 dependency. A795 is existing fixed-initial signed expansion and is not invented as a direct105 parent. AVG100 retains the larger signed averaging boundary; the new actual countable law is its strict prerequisite, not completion of AVG100.',
    'public_projection_bindings': {'COUNT93': binding(P93), 'ENDPAIR104': binding(P104), 'NORM': binding(P103), clock_id: binding(CLOCK)},
    'api_dependencies': retrieval, 'topology_status': 'proposed, requires separately independent validation',
    'self_topology_validation': False, 'certified_Lean_edges_added': 0, 'proof_credit': False
})

dispositions = {
    'standing-curvature': 'Retain original hAlpha,hAlphaBeta,hV,hH; no extra source binder.',
    'standing-eta': 'Retain hEta,hBetaEta; no new time restriction.',
    'target-position-energy': 'Reuse exact Vy and normalized position Gibbs from103.',
    'phase-gibbs-law': 'Reuse103 product identification and probability; normalizer is not supplied.',
    'actual-phase': 'Reuse actual93 flow/bounce/rate/clock recursion; no new dynamical proof.',
    'event-convention': 'Retain actual93 post-event representative, incoming-state density and null event-endpoint facts; no pointwise path reversal.',
    'shifted-energy-distinction': 'Inherited shifted energy is not confused with target Gibbs energy; no new proof or domination claim.',
    'A3-boundary': 'L2 adjoint/generator/semigroup extension remains red and outside105.',
    'A4': 'Inherited through104; not re-proved.',
    'elementary-reversal': 'Inherited through104 endpoint-sector preservation; not pathwise-all-times reversal.',
    'A5': 'Inherited rate-product matching through104; no extra rate positivity.',
    'A6': 'Inherited through104, no new Jacobian claim.',
    'simplex': 'All counts including0 and T=0 use actual strict simplex/comap; local measurable/SFinite adapter required.',
    'prescribed': 'Actual93 Gamma and rho are reused jointly measurably and matched to104 literals.',
    'A7': 'Selected actual count law and nonnegative endpoint-test assembly under Gibbs initialization. Existing95 full signed fixed-initial expansion is recorded, not re-proved.',
    'average': 'Selected initial-phase integration and countable Tonelli exchange; energy-dependent bound is not assumed uniform in initial phase.',
    'A8': 'Reuse104 fixed-count endpoint flipped-swap, then transfer over countable sum. All-time jumpwise path equality excluded.',
    'unweighted-transform': 'Inherited97/104 transform; no new endpoint-time theorem.',
    'integrated-A4': 'Inherited98/101/104 weight normalization route; no new energy theorem.',
    'weight-matching-and-invariance': '3210-3215: selected countable nonnegative assembly and reversal. 3216-3222: signed bounded bilinear consumer remains red. 3224-3227: marginal invariance and L2 completion remain red.',
    'source-license': 'Existing pinned source referenced; no new full primary copy/archive.'
}
covered = []
for r in regions:
    row = {k: v for k, v in r.items() if not k.startswith('disposition')}
    row['disposition105'] = dispositions[r['id']]
    covered.append(row)
coverage = write('source-coverage-delta105.native.json', {
    'kind': 'exhaustive source-only region disposition', 'primary': primary,
    'inherited21_inventory': binding(COVER104), 'all21_slices_rechecked': True,
    'regions': covered, 'source_graph_delta': graph,
    'changed_required_slice': ['COUNT93', 'SECTOR-INTEGRAL-MEAS105', 'ASSEMBLY105', 'ENDPOINT-LAW105'],
    'all_inherited_nodes_policy': 'Every unchanged55-node source identity remains bound to compiled104 coverage. No new credit for inherited mechanics; future red AVG100/INV100/L2A3/RESTART remain red.',
    'implementation_coverage': 'Not applicable: no105 Lean declaration/header exists.',
    'remaining_reds': ['AVG100 bounded signed endpoint bilinear identity', 'INV100 actual phase marginal invariance', 'L2A3', 'RESTART/Markov/semigroup', 'cost and full-paper claims'],
    'self_topology_validation': False, 'proof_credit': False
})

# Preserve bounded scheduling context as text/JSON, not a mutable input binding.
handoff_path = 'docs/companion-papers-handoff.md'
handoff_lines = (ROOT / handoff_path).read_text(encoding='utf8').splitlines()
start = next(i for i, l in enumerate(handoff_lines) if l.startswith('## Actual normalized PBPS endpoint-pair sector reversal'))
end = next((i for i in range(start + 1, len(handoff_lines)) if handoff_lines[i].startswith('## ')), len(handoff_lines))
context = write('scheduling-context105.native.json', {
    'kind': 'bounded scheduling context only, never theorem evidence',
    'execution': json.loads((ROOT / 'website/content/samplewiki_companion_frontiers.json').read_text(encoding='utf8'))['execution'],
    'handoff_section': '\n'.join(handoff_lines[start:end]),
    'handoff_section_line_start': start + 1, 'handoff_section_line_end': end,
    'observed_full_file_raw_hashes_context_only': [binding(handoff_path), binding('website/content/samplewiki_companion_frontiers.json')],
    'snapshot_policy': 'The owned extracted context is immutable. Full scheduling files are mutable and are not selected mathematical input bindings or required closure-recovery inputs.',
    'authorization': 'Only prospective105 source recommendation; owner continues serialized104 integration.'
})
inputs = [PRIMARY, COVER104, GRAPH104, TOPO104, ADMISSION104, COMPILED104, P93, P95, P103, P104, CLOCK,
          'lean-toolchain', 'lake-manifest.json', 'research-wiki/external-lean-libraries/README.md']
inputs += [a[0] for a in apis]
inputs = sorted(set(inputs))
run = write('source-preread-run105.native.json', {
    'kind': 'native bounded independent source-only preread run', 'reviewer': '/root/source_final96',
    'primary_first': source_first, 'recommendation': recommendation, 'coverage': coverage, 'graph': graph,
    'expected_slots': expected, 'definition_context': definitions, 'retrieval': retrieval, 'scheduling_context': context,
    'selected_inputs': [binding(p) for p in inputs], 'status': 'RECOMMEND_ONE_ACTUAL_COUNTABLE_ENDPOINT_ASSEMBLY_EDGE',
    'new_proof_or_header': False, 'source_graph_self_validation': False, 'shared_writes': False,
    'remaining_gate': 'Separate prospective topology/header reviews and104 delivery are owner-controlled; no105 proof credit.'
})
owned = [binding(p.relative_to(ROOT).as_posix()) for p in sorted(OUT.iterdir()) if p.is_file()]
closure = write('closed-RAW-preread105.native.json', {
    'kind': 'immutable RAW closure', 'reviewer': '/root/source_final96', 'run': run,
    'selected_inputs': [binding(p) for p in inputs], 'owned_artifacts': owned,
    'self_manifest_excluded': True, 'primary_snapshot_referenced_not_copied': True,
    'source_graph_self_validation': False, 'proof_credit': False
})
print(json.dumps({'recommendation': recommendation, 'graph': graph, 'coverage': coverage, 'run': run, 'closure': closure}, indent=2))
