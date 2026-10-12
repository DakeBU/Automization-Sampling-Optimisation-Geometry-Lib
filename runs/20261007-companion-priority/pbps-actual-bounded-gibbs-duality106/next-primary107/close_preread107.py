from pathlib import Path
import gzip
import hashlib
import json
import re

ROOT = Path('E:/Samplinglib')
RUN = ROOT / 'runs/20261007-companion-priority/pbps-actual-bounded-gibbs-duality106'
OUT = RUN / 'next-primary107'


def sha(b):
    return hashlib.sha256(b).hexdigest()


def ref(p):
    p = ROOT / p if isinstance(p, str) else p
    b = p.read_bytes()
    return {'path': p.relative_to(ROOT).as_posix(), 'raw_sha256': sha(b), 'bytes': len(b)}


def load(p):
    return json.loads(p.read_text(encoding='utf8'))


def put(name, obj):
    p = OUT / name
    assert not p.exists(), p
    p.write_bytes((json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode())
    return ref(p)


primary = load(OUT / 'primary-first107.native.json')
source = ROOT / primary['primary']['path']
assert ref(source) == primary['primary']
for r in primary['source_regions']:
    assert sha(source.read_bytes()[r['byte_start']:r['byte_end_exclusive']]) == r['raw_sha256']
prod = ROOT / 'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualBoundedGibbsDuality.lean'
assert sha(prod.read_bytes()) == '4fad17d78149b7a4a784170309e9de3f70941ef533f90228b0405dee5fc2707d'
s = prod.read_text(encoding='utf8')
prefix = s[s.index('    {E : Type*}'):s.index('      (∀ y xRef : E, ∀ T : ℝ≥0,')]
assert len(re.findall(r'^    let ', prefix, re.M)) == 37
context = put('literal-context107.native.json', {
    'kind': 'Exact universal assumptions, 37 definitions and global-Z contract inherited from106',
    'producer': ref(prod), 'source_lines': [13, 133],
    'literal_LF_text': prefix, 'literal_LF_sha256': sha(prefix.encode()),
    'no_new_Lean_header': True, 'six_original_assumptions': ['hα', 'hαβ', 'hV', 'hH', 'hη', 'hβη'],
    'test_membership_not_source_assumption': 'MemLp G 2 (nu y) classifies a quantified observable. It does not assume a property of the process or potential.'})

mathlib = '.lake/packages/mathlib/Mathlib/'
api_specs = [
    ('MeasureTheory.StronglyMeasurable.integral_prod_right', 'MeasureTheory/Integral/Prod.lean', 'theorem MeasureTheory.StronglyMeasurable.integral_prod_right ', 'Borel expectation after composing real Borel G with the same jointly measurable Z; SFinite actual clock derived from probability.'),
    ('MeasureTheory.Integrable.prod_right_ae', 'MeasureTheory/Integral/Prod.lean', 'theorem Integrable.prod_right_ae ', 'Actual section integrability from product L1.'),
    ('MeasureTheory.Integrable.integral_prod_left', 'MeasureTheory/Integral/Prod.lean', 'theorem Integrable.integral_prod_left ', 'A.e. expectation is integrable over initial phase.'),
    ('MeasureTheory.integral_prod', 'MeasureTheory/Integral/Prod.lean', 'theorem integral_prod ', 'Signed Fubini for representative identification, with product integrability proved.'),
    ('MeasureTheory.Lp.compMeasurePreservingₗᵢ', 'MeasureTheory/Function/LpSpace/Basic.lean', 'def compMeasurePreservingₗᵢ ', 'Isometric pullback under actual endpoint and initial projection.'),
    ('MeasureTheory.Lp.coeFn_compMeasurePreserving', 'MeasureTheory/Function/LpSpace/Basic.lean', 'theorem coeFn_compMeasurePreserving ', 'Representative is the pullback a.e., not pointwise.'),
    ('ContinuousLinearMap.adjoint', 'Analysis/InnerProductSpace/Adjoint.lean', 'def adjoint : (E →L[𝕜] F)', 'Bounded Hilbert averaging as adjoint of initial projection pullback; adjoint is an isometry on operator spaces.'),
    ('ContinuousLinearMap.adjoint_inner_right', 'Analysis/InnerProductSpace/Adjoint.lean', 'theorem adjoint_inner_right ', 'Indicator pairing identifies actual expectation.'),
    ('MeasureTheory.L2.inner_def', 'MeasureTheory/Function/L2Space.lean', 'theorem inner_def ', 'Pairing equals integral of products.'),
    ('MeasureTheory.memLp_two_iff_integrable_sq', 'MeasureTheory/Function/L2Space.lean', 'theorem memLp_two_iff_integrable_sq ', 'Optional explicit square-integral expression of contraction.'),
    ('MeasureTheory.Integrable.ae_eq_of_forall_setIntegral_eq', 'MeasureTheory/Function/AEEqOfIntegral.lean', 'theorem Integrable.ae_eq_of_forall_setIntegral_eq ', 'L1 equality against measurable finite sets identifies the averaging representative.'),
    ('MeasureTheory.Lp.simpleFunc.denseRange', 'MeasureTheory/Function/SimpleFuncDenseLp.lean', 'protected theorem denseRange (hp_ne_top', 'Future A.3 density consumer only; not needed to construct current candidate.'),
]
apis = []
for name, tail, needle, use in api_specs:
    p = ROOT / (mathlib + tail)
    ls = p.read_text(encoding='utf8').splitlines()
    i = next(i for i, x in enumerate(ls) if needle in x)
    apis.append({'declaration': name, 'file': ref(p), 'line_start': i + 1,
                 'signature_excerpt': '\n'.join(ls[i:i + 6]), 'use': use,
                 'status': 'pinned source inspected; no new compilation or theorem credit'})

local_paths = [
    'AutoSamplingTheory/TechnicalLemmas/Measure/L2Expectation.lean',
    'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualOuterBoundedL2Continuity.lean',
    'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPhaseTransitionKernel.lean',
    'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPhaseNormalization.lean',
    'AutoSamplingTheory/TechnicalLemmas/Probability/UnitExponentialProduct.lean',
    'research-wiki/retrieval-index/astis-lean-arsenal-module-graph.json',
    'research-wiki/external-lean-libraries/mathlib.md',
    'research-wiki/external-lean-libraries/lean-stat-learning-theory.md',
]
cells = []
for p in sorted((ROOT / 'research-wiki/frontier-cells').glob('*PBPS*.json')):
    if any(k in p.stem.lower() for k in ['l2', 'kernel', 'duality', 'restart', 'semigroup', 'small-time']):
        x = load(p)
        cells.append({'input': ref(p), 'status': x.get('status'), 'cell': p.stem,
                      'duplicate_decision': 'Existing bounded small-time/kernel/reflection domains do not construct the actual106 same-witness all-L2 contraction.'})
retrieval = put('retrieval107.native.json', {
    'toolchain': ref(ROOT / 'lean-toolchain'), 'manifest': ref(ROOT / 'lake-manifest.json'),
    'fixed_Mathlib_revision': 'db584cd6d46c92f209a44c0f1c829460d327499d', 'api_signatures': apis,
    'local_inputs': [ref(p) for p in local_paths], 'active_cell_screen': cells,
    'local_reuse_findings': [
        'L2Expectation.expectation_apply_eq_integral supplies constant-one expectation functional, not product averaging or actual transition lift. Do not duplicate it or cite it as the missing lift.',
        'ActualOuterBoundedL2Continuity proves bounded continuous test small-time convergence for a separately existential Z. Its all-L2 operator/contraction remains red. Same-witness alignment is required before a strong-continuity consumer.',
        'ActualPhaseTransitionKernel produces a probability kernel for a separately existential Z. Probability-fiber kernel status does not prove restart or semigroup; do not consume its witness interchangeably with106.',
        'Actual106 plus actual normalization103 and actual clock probability suffice for the selected fixed-time lift; no external port needed.'
    ],
    'compatible_catalog_scope': 'Searched local arsenal/retrieval and external-library cards first. Fixed Mathlib already supplies Hilbert pullbacks/adjoints, Fubini and a.e. uniqueness. No SLT/ATLAS/OAI statement selected, ported or credited.',
    'diagnostics': [
        'Initial capsule printing failed under GBK; rerun with PYTHONIOENCODING=utf-8 succeeded and exact stdout snapshot retained.',
        'Screening guesses ProximalBPS/L2Expectation, Probability/L2Expectation and Mathlib/Probability/Kernel/Lp did not exist. Correct local file is TechnicalLemmas/Measure/L2Expectation; no guessed API adopted.',
        'Windows rg wildcard-as-path failed; corrected to directory plus glob. No duplicate-absence conclusion rests on failed search.'
    ]})

route = [
    'Consume106 once to obtain one actual global Z with all inherited pointwise arc/fallback and parameterwise clock-a.e. zero-time clauses, actual endpoint measure preservation and bounded duality. Derive nu and P probability using103 and UnitExponentialProduct; retain the same Z in every conclusion.',
    'For each Borel G, jointly measurable G(Z(y,r,z,T,w)) has a strongly measurable clock integral by fixed-Mathlib product-integral measurability. For bounded G derive every section integrable and the unchanged bound C; no integrability premise is supplied.',
    'For fixed y,r,T, let mu=nu_y.prod P, Fst(z,w)=z and End(z,w)=Z(y,r,z,T,w). Both preserve their measures. Form real L2 isometric pullbacks B=f↦f∘Fst and C=f↦f∘End using the exact Mathlib API.',
    'Define the bounded lift internally as B.adjoint composed with C. Its norm is at most1 from the isometries and adjoint norm preservation. This is a construction choice, never a public supplied operator.',
    'For any G with MemLp G 2 nu_y, pullback gives product L2 and hence L1; Fubini gives clock-section integrability for nu_y-a.e. z and outer L1. Pair B.adjoint(C[G]) against measurable-set indicators, use signed Fubini and L2.inner_def, then L1 set-integral uniqueness to identify it a.e. with op G.',
    'Transport a.e. changes in G via actual endpoint measure preservation and Fubini. Thus op respects L2 equivalence classes, belongs to L2, and represents this same contraction. Derive the square-integral inequality and the zero-time operator identity from the inherited parameterwise clock-a.e. zero-time clause.',
    'Return the exact same-witness106 bounded-duality/invariance contract together with Borel expectation and the actual L2 lift. Future A.3 may then combine bounded duality with simple-function density; do not assert that extension, strong continuity or a semigroup in this packet.'
]
recommendation = put('recommendation107.native.json', {
    'kind': 'one prospective source-backed mathematical edge; not a claim, header or proof',
    'title': 'Actual fixed-time Gibbs L2 expectation contraction',
    'source': primary['primary'], 'source_anchor': 'Appendix A.1 A.3 at3000-3014 and density extension at3226-3227; fixed-time contraction component of item(ii), not its semigroup/continuity component.',
    'frozen_primary_first': ref(OUT / 'primary-first107.native.json'), 'literal_context': context,
    'expected_semantic_slots': primary['expected_slots'],
    'complete_prospective_statement': [
        'Preserve exactly the ambient finite-dimensional real Hilbert Borel structure, six analytic conditions, 37 literal definitions and global existential Z contract in literal-context107.native.json. Preserve all106 same-Z endpoint-preservation and bounded-duality conclusions as inherited outputs, so the later density consumer cannot accidentally combine different existential witnesses.',
        'For every Borel G:H→R, the literal total clock expectation A_G(y,r,z,T)=integral G(Z y r z T w) dP(w) is jointly Borel in ((y,r),z,T). For every C≥0 with |G|≤C, every clock section is integrable and |A_G|≤C everywhere.',
        'For every y,r there exists a family T2 indexed by T:NNReal of continuous real linear maps Lp R 2 (nu y)→Lp R 2 (nu y). No continuity or measurability of this operator-valued family is asserted. For every T, ||T2 T||≤1.',
        'For every T and every G:H→R with hG:MemLp G 2 (nu y), derive: for nu_y-a.e. z, w↦G(Z y r z T w) is P-integrable; hOp:MemLp (A_G y r · T) 2 (nu y); (T2 T)(hG.toLp G)=hOp.toLp(A_G y r · T). Equivalently its chosen representative equals the actual clock expectation nu_y-a.e. Membership and equality are outputs, not assumptions about the process.',
        'For the same G, integral |A_G|^2 dnu_y ≤ integral |G|^2 dnu_y, and T2 0 is the identity. The bound1 is exact, independent of y,r,T,dimension or curvature constants. A.e. representative independence follows; no pointwise equality for arbitrary L2 representatives is required.'
    ],
    'actual_direct_producers': [
        'AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBoundedGibbsDuality.actual_bounded_gibbs_duality',
        'AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhaseNormalization.actual_phase_gibbs_normalization',
        'AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws'],
    'why_substantive': 'Constructs and identifies an actual operator on L2 equivalence classes, proves contraction and a.e. section integrability for unbounded L2 observables. These are absent from bounded106 and not a restatement or bounded-test wrapper.',
    'real_consumer': 'Canonical L2A3: combine the retained same-Z AVG100 bounded duality with this contraction and PHASE-FLIP106 isometric pullback, extend by simple-function density to T2.adjoint=R2 composed T2 composed R2. This consumer is future, not newly certified.',
    'route_at_most_seven_steps': route, 'retrieval': retrieval,
    'readiness': 'Dependency-ready analytically after exact106 admission and delivery. At snapshot106 is PROVED_LOCAL with final source review closed; no integration/completion inferred.',
    'source_gap': 'The printed density sentence suppresses construction of a representative-independent bounded L2 operator. The selected target fills that analytic obligation from actual stationarity, probability, Hilbert pullbacks and Fubini, without adding source premises.',
    'edge_cases': {'rank_zero': 'Allowed: actual Gibbs/clock laws and pullbacks remain meaningful.', 'time_zero': 'T2 0=id uses fixed-parameter clock-a.e. Z0=z plus Fubini; no common null set over uncountably many parameters.', 'unbounded_L2': 'Section integrability only nu-a.e.; total Bochner convention is not used as fake pointwise integrability.', 'null_representatives': 'Same-L2 input gives same-L2 output; pointwise output agreement for all initial states is false in general and excluded.', 'zero_rates_and_empty_counts': 'Handled by inherited actual Z construction, no count restriction or new event convention.'},
    'remaining_reds': ['L2A3 adjoint identity itself', 'same-witness identification with older small-time/transition-kernel witnesses', 'strong continuity for all L2', 'restart and actual Markov property', 'Chapman-Kolmogorov and semigroup law', 'momentum-averaged selfadjoint position operator', 'hypocoercivity, simulation errors, expected costs, main results and composition'],
    'no_topology_self_validation': True, 'new_Lean_credit': False})

base = load(RUN / 'final-source106/compiled-source-coverage106.native.json')
nodes = [x['id'] for x in base['node_dispositions']]
new_nodes = [
    {'id': 'BOREL-OP107', 'meaning': 'Joint Borel actual clock expectation and bounded-section integrability under the same global Z.'},
    {'id': 'L2-PRODUCT107', 'meaning': 'Same actual endpoint and initial projection induce L2 isometric pullbacks on nu_y.prod P.'},
    {'id': 'L2-LIFT107', 'meaning': 'Actual continuous linear L2 contraction, all-L2 expectation representative and zero-time identity.'}]
clock = 'AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws'
new_edges = [['COUNT93', 'BOREL-OP107'], [clock, 'BOREL-OP107'], ['INV100', 'L2-PRODUCT107'], ['NORM', 'L2-PRODUCT107'], [clock, 'L2-PRODUCT107'], ['BOREL-OP107', 'L2-LIFT107'], ['L2-PRODUCT107', 'L2-LIFT107'], ['COUNT93', 'L2-LIFT107'], ['L2-LIFT107', 'L2A3']]
graph = put('source-proof-graph-delta107.native.json', {
    'kind': 'prospective graph delta; independently review before seal', 'author': '/root/source_final96',
    'base_graph': ref(RUN / 'source-graph106.effective.json'), 'base_compiled_coverage': ref(RUN / 'final-source106/compiled-source-coverage106.native.json'),
    'base_independent_overlay_admission': ref(RUN / 'independent-whole-math106/route-topology106/route-topology-admission106.native.json'),
    'inherited_nodes': nodes, 'inherited_edges': [{'source': x['source'], 'target': x['target']} for x in base['edge_dispositions']],
    'new_nodes': new_nodes, 'new_edges': new_edges, 'counts_if_admitted': {'nodes': 65, 'edges': 132},
    'AND_groups': [
        {'target': 'BOREL-OP107', 'parents': ['COUNT93', clock], 'mechanism': 'Joint measurable same-Z contract projects from106; actual probability clock supplies SFinite and bounded integration.'},
        {'target': 'L2-PRODUCT107', 'parents': ['INV100', 'NORM', clock], 'mechanism': 'Endpoint stationarity and actual probability products give endpoint/fst measure preservation; form isometric pullbacks.'},
        {'target': 'L2-LIFT107', 'parents': ['BOREL-OP107', 'L2-PRODUCT107', 'COUNT93'], 'mechanism': 'Adjoint averaging, Fubini and set-indicator uniqueness establish representative and contraction; COUNT93 same-Z zero-time projection supplies T2 zero identity.'}],
    'future_consumer': {'target': 'L2A3', 'new_parent': 'L2-LIFT107', 'other_obligations': 'Retain inherited AVG100 and PHASE-FLIP106 dependencies; bounded simple-function density and bilinear extension remain unproved. No A3 acceptance from this graph.'},
    'source_binders_vs_edges': 'Six analytic source conditions only. All measurability/probability/measure-preservation/L2 bounds/representatives are dependencies or internal conclusions, never new source hypotheses.',
    'same_witness': 'COUNT93/INV100/AVG100 interfaces here all project from one106 invocation. Independent existential older83/84 witnesses are not freely substituted.',
    'canonical_identity_policy': 'Reuse TIME97, AVG100, INV100, NORM, COUNT93, L2A3 and RESTART; no duplicate alias nodes.',
    'topology_validation': 'Pending independent reviewer; creator does not self-admit', 'new_proof_credit': False})

regions = []
for r in primary['source_regions']:
    r = dict(r)
    if r['id'] == 'A3-boundary':
        disp = 'Selected strict prerequisite for fixed-time real L2 operator construction. Adjoint A3, strong continuity, semigroup and position averaging remain red; heuristic generator calculations are excluded.'
    elif r['id'] == 'weight-matching-and-invariance':
        disp = '3226-3227 density extension motivates the selected L2 domain/contraction bridge. Earlier weighted matching and bounded duality reused through106; no new finite-sector proof.'
    elif r['id'] in ['standing-curvature', 'standing-eta']:
        disp = 'Retain original six conditions literally; proof inputs are not extra public binders.'
    elif r['id'] == 'source-license':
        disp = 'Pinned arXiv nonexclusive-distribution license; reference existing primary, no new whole-primary archive.'
    else:
        disp = 'Unchanged inherited106 source mechanism/actual definition. Exact existing coverage reused, no new theorem credit.'
    r['disposition107'] = disp
    regions.append(r)
coverage = put('source-coverage107.native.json', {
    'source': primary['primary'], 'all21_regions_rehashed': regions,
    'inherited_coverage': ref(RUN / 'final-source106/compiled-source-coverage106.native.json'), 'graph_delta': graph,
    'node_dispositions': [{'id': n, 'status': ('future consumer; still red' if n == 'L2A3' else 'independent restart boundary; still red' if n == 'RESTART' else 'inherited exact106 coverage unchanged')} for n in nodes] + [{'id': n['id'], 'status': 'selected prospective obligation, no implementation or proof'} for n in new_nodes],
    'source_route': 'ASTIS analytic completion of suppressed L2 domain step; Hilbert adjoint averaging is equivalent to conditional expectation/Jensen. No generator-domain exponentiation or restart assumed.',
    'compiled107_coverage': False, 'independent_topology_admission': False})

run = put('source-preread-run107.native.json', {
    'author': '/root/source_final96', 'recommendation': recommendation, 'coverage': coverage, 'graph': graph,
    'source_first': ref(OUT / 'primary-first107.native.json'), 'read_only_production': ref(prod),
    'current_scheduling_snapshots': [ref(OUT / n) for n in ['capsule107.exactraw.snapshot.json', 'handoff107.exactraw.snapshot.md', 'frontiers107.exactraw.snapshot.json']],
    'mutable_context_policy': 'Exact snapshot bytes preserved; future scheduling changes do not alter mathematical evidence.',
    'no_new_header_or_proof': True, 'no_new_claim_or_seal': True, 'no_shared_mutation': True,
    'no_source_graph_self_validation': True, 'readiness_conditional_on106_delivery': True})
inputs = [ref(source), ref(prod), ref(RUN / 'source-graph106.effective.json'), ref(RUN / 'final-source106/compiled-source-coverage106.native.json'), ref(RUN / 'independent-whole-math106/route-topology106/route-topology-admission106.native.json'), ref(ROOT / 'lean-toolchain'), ref(ROOT / 'lake-manifest.json')]
inputs += [ref(p) for p in local_paths] + [a['file'] for a in apis] + [c['input'] for c in cells]
inputs = list({x['path']: x for x in inputs}.values())
archives = []
for p in sorted(OUT.iterdir()):
    if p.is_file() and not p.name.endswith('.gz'):
        a = p.with_name(p.name + '.raw.gz')
        assert not a.exists()
        a.write_bytes(gzip.compress(p.read_bytes(), mtime=0))
        assert gzip.decompress(a.read_bytes()) == p.read_bytes()
        archives.append({'raw': ref(p), 'archive': ref(a)})
closure = put('closed-RAW-preread107.native.json', {
    'kind': 'immutable source-only107 closure; no mathematical acceptance', 'recommendation': recommendation,
    'run': run, 'selected_inputs': inputs, 'owned_artifacts': [ref(p) for p in sorted(OUT.iterdir()) if p.is_file()],
    'original_RAW_archives': archives, 'no_full_primary_archive': True,
    'self_hash_omitted': True, 'topology_pending_independent_review': True})
print(json.dumps({'recommendation': recommendation, 'graph': graph, 'coverage': coverage, 'closure': closure}, indent=2))
