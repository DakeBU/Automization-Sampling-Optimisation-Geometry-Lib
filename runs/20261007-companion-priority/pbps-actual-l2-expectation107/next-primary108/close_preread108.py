from pathlib import Path
import hashlib
import json
import gzip

ROOT = Path('E:/Samplinglib')
RUN = ROOT / 'runs/20261007-companion-priority/pbps-actual-l2-expectation107'
OUT = RUN / 'next-primary108'


def binding(p):
    p = Path(p)
    if not p.is_absolute():
        p = ROOT / p
    b = p.read_bytes()
    return {'path': p.relative_to(ROOT).as_posix(), 'raw_sha256': hashlib.sha256(b).hexdigest(), 'bytes': len(b)}


def read(p):
    return json.loads(Path(p).read_text(encoding='utf-8'))


def write(name, obj):
    p = OUT / name
    assert not p.exists(), p
    p.write_bytes((json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
    return binding(p)


primary = read(OUT / 'primary-first108.native.json')
basepath = RUN / 'source-graph107.effective.json'
base = read(basepath)
production = ROOT / 'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualL2Expectation.lean'
assert binding(production)['raw_sha256'] == '4c35e0b71362bec3563e3d07c9f122d6b7ca4cae604f7a88aad397d2a028f4d6'
lines = production.read_bytes().splitlines(keepends=True)
context = write('actual-interface108.native.json', {
    'producer': binding(production),
    'public_declaration': 'AutoSamplingTheory.ExampleCases.ProximalBPS.ActualL2Expectation.actual_l2_expectation_contraction',
    'literal_definition_interval': [25, 125],
    'literal_definition_count': 37,
    'literal_definition_raw_sha256': hashlib.sha256(b''.join(lines[24:125])).hexdigest(),
    'full_literal_contract_interval': [14, 164],
    'full_literal_contract_raw_sha256': hashlib.sha256(b''.join(lines[13:164])).hexdigest(),
    'global_witness_contract': {
        'Z_quantifier': 'one existential Z before all y,r,z,time,noise and observables',
        'joint_measurability': [126, 128], 'live_arc': [129, 132],
        'fallback': [133, 134], 'parameterwise_ae_zero': [135, 135],
        'endpoint_invariance_and_bounded_signed_duality': [136, 148],
        'joint_borel_expectation_and_bounded_sections': [149, 155],
        'same_Z_L2_family_and_universal_representatives': [156, 164]
    },
    'transfer_rule': 'Destructure107 once. Carry its Z and, for each y,r, its A family and ALL existing conclusions. Establish the new adjoint identity for this very A using its universal representative equation and the bounded duality for this very Z. Never invoke105 or106 independently to obtain another existential path.',
    'no_private_API': True,
    'readiness': '107 science 2b657840a2f21c5d8001c83e4625a1ab13ef70ba; exact admission/integration/delivery was pending at assignment. Scheduling108 remains conditional on delivery.'
})

M = '.lake/packages/mathlib/Mathlib/'
specs = [
    ('MeasureTheory.isZeroOrProbabilityMeasure_tilted', 'MeasureTheory/Measure/Tilted.lean', 138, 146),
    ('ProbabilityTheory.stdGaussian_map', 'Probability/Distributions/Gaussian/Multivariate.lean', 128, 135),
    ('MeasureTheory.Measure.map_prod_map', 'MeasureTheory/Measure/Prod.lean', 833, 842),
    ('MeasureTheory.Lp.compMeasurePreservingₗᵢ', 'MeasureTheory/Function/LpSpace/Basic.lean', 630, 635),
    ('MeasureTheory.Lp.coeFn_compMeasurePreserving', 'MeasureTheory/Function/LpSpace/Basic.lean', 572, 574),
    ('MeasureTheory.Lp.compMeasurePreserving_comp', 'MeasureTheory/Function/LpSpace/Basic.lean', 597, 602),
    ('MeasureTheory.Lp.compMeasurePreserving_id', 'MeasureTheory/Function/LpSpace/Basic.lean', 589, 592),
    ('MeasureTheory.MemLp.coeFn_toLp', 'MeasureTheory/Function/LpSpace/Basic.lean', 111, 113),
    ('MeasureTheory.Lp.simpleFunc.toSimpleFunc', 'MeasureTheory/Function/SimpleFuncDenseLp.lean', 497, 499),
    ('MeasureTheory.Lp.simpleFunc.measurable', 'MeasureTheory/Function/SimpleFuncDenseLp.lean', 501, 505),
    ('MeasureTheory.Lp.simpleFunc.memLp', 'MeasureTheory/Function/SimpleFuncDenseLp.lean', 525, 527),
    ('MeasureTheory.Lp.simpleFunc.toLp_toSimpleFunc', 'MeasureTheory/Function/SimpleFuncDenseLp.lean', 529, 531),
    ('MeasureTheory.SimpleFunc.exists_forall_norm_le', 'MeasureTheory/Function/SimpleFuncDenseLp.lean', 255, 256),
    ('MeasureTheory.Lp.simpleFunc.denseRange', 'MeasureTheory/Function/SimpleFuncDenseLp.lean', 671, 673),
    ('DenseRange.induction_on₂', 'Topology/DenseEmbedding.lean', 364, 367),
    ('continuous_inner', 'Analysis/InnerProductSpace/Continuous.lean', 63, 66),
    ('MeasureTheory.L2.inner_def', 'MeasureTheory/Function/L2Space.lean', 137, 138),
    ('MeasureTheory.L2.integrable_inner', 'MeasureTheory/Function/L2Space.lean', 172, 175),
    ('LinearIsometry.inner_map_map', 'Analysis/InnerProductSpace/LinearMap.lean', 115, 118),
    ('ContinuousLinearMap.adjoint_inner_left', 'Analysis/InnerProductSpace/Adjoint.lean', 123, 124),
    ('ext_inner_left', 'Analysis/InnerProductSpace/Basic.lean', 322, 324)
]
apis = []
for name, file, a, b in specs:
    p = ROOT / (M + file)
    raw = b''.join(p.read_bytes().splitlines(keepends=True)[a-1:b])
    apis.append({'id': name, 'file': binding(p), 'line_start': a, 'line_end': b,
                 'span_raw_sha256': hashlib.sha256(raw).hexdigest(),
                 'signature_excerpt': raw.decode('utf-8')})
screen = [
    ('AutoSamplingTheory/TechnicalLemmas/Measure/L2Expectation.lean', 'Scalar expectation-pairing API; not the actual PBPS A3 extension. Do not replace actual107 quotient operator by an unrelated abstract lift.'),
    ('AutoSamplingTheory/TechnicalLemmas/Probability/KernelReversibility.lean', 'Atomic singleton balance implies kernel reversibility; wrong state/transition contract for continuous phase momentum-flip adjoint.'),
    ('AutoSamplingTheory/TechnicalLemmas/Probability/KernelTransport.lean', 'Existing kernel map/comap invariant transport, not same-witness PBPS L2 adjoint.'),
    ('Libraries/frontloaded-shared-spine.json', 'Finite reversible Dirichlet/dissipation floor screened; no substitute for actual continuous phase same-Z bridge.'),
    ('research-wiki/external-lean-libraries/lean-stat-learning-theory.md', 'Pinned compatibility catalog d0f506f0a695018265dccb33bcb05e2f5ca1c876 targets Lean4.32.0 and is external-reference only. Fixed Mathlib supplies density/pullback APIs; no upstream port selected or credited.')
]
retrieval = write('retrieval108.native.json', {
    'pinned_manifest': binding(ROOT / 'lake-manifest.json'),
    'pinned_toolchain': binding(ROOT / 'lean-toolchain'),
    'mathlib_revision': 'db584cd6d46c92f209a44c0f1c829460d327499d',
    'apis': apis,
    'local_compatible_catalog_screen': [{'input': binding(ROOT / p), 'disposition': d} for p, d in screen],
    'search_boundary': 'Bounded local and pinned Mathlib retrieval; no network upstream theorem imported, no comprehensive all-library absence claim.',
    'finite_measure_detail': 'map_prod_map requires SFinite each factor. Tilted measure is zero-or-probability by existing Mathlib instance, hence finite/SFinite; stdGaussian is probability. No public finiteness assumption and no extra103 producer is required for the chosen flip construction. Actual107 already concerns the genuine normalized law.',
    'density_detail': 'Lp.simpleFunc representatives are measurable, bounded and already MemLp. Use their own memLp field, not a false inference that arbitrary bounded functions are L2 on an unspecified measure.',
    'diagnostics': ['First inventory read omitted encoding and failed under GBK; repeated explicitly UTF8 succeeded. No output acceptance based on failed read.', 'A PowerShell rg wildcard path failed; exact Tilted.lean was located and inspected.']
})

route = [
    'Invoke actual107 once; retain its global Z, all path/clock/invariance/bounded-duality/Borel conclusions, and its same A family with universal MemLp representative equation.',
    'Prove actual R preserves nu_y using Gaussian negation and product-map identity (finite-factor instances from tilted/stdGaussian); define J_y as the canonical Lp pullback linear isometry. R squared=id gives J_y squared=id and inner-product preservation.',
    'Take two Lp.simpleFunc classes and their measurable finite-range representatives F,G. Obtain nonnegative global bounds by enlarging the finite-range norm bounds; use the representatives own MemLp witnesses. Pullback preserves MemLp and agrees almost everywhere with composition by R.',
    'Apply inherited107 bounded signed duality to F,G, and its universal representative equation to G and F composed R. Use L2.inner_def, coeFn_toLp and pullback AE identities to derive inner(f,A_T g)=inner(J_y g,A_T(J_y f)) on the dense simple-function pair.',
    'Both sides are continuous functions on the product real Hilbert space since A_T and J_y are continuous linear. Extend the equality to all f,g by Lp.simpleFunc.denseRange and DenseRange.induction_on₂. L2.integrable_inner handles the resulting products; no signed integrability premise is inserted.',
    'Use J_y isometry/involution to move the flip across the inner product, then adjoint_inner_left and inner extensionality to obtain A_T.adjoint=J_y.toContinuousLinearMap.comp(A_T.comp J_y.toContinuousLinearMap).',
    'Return the SAME witnesses and all107 outputs plus the canonical flip representation/involution and full real-L2 adjoint identity for every nonnegative T. Check T=0 and rank0 directly against identity/involution; stop before semigroup, strong continuity or momentum-averaged kernel construction.'
]
recommendation = write('recommendation108.native.json', {
    'kind': 'one prospective source-backed mathematical edge, not a claim or header',
    'target_canonical_node': 'L2A3',
    'title': 'Actual real-L2 momentum-flip adjoint identity for the same107 clock expectation',
    'source': primary['primary'],
    'anchors': ['A1.E3 / lines3000-3014', 'A1.Ex21 / lines3210-3227', 'phase law Eq3.1 / lines1411-1422'],
    'license': primary['source_license'],
    'expected_semantic_slots': primary['expected_semantic_slots'],
    'complete_prospective_boundary': {
        'ambient': 'E real finite-dimensional inner-product space with its Borel measurable structure; V:E->R; alpha,beta:NNReal; eta:R. Rank0 included.',
        'only_six_analytic_assumptions': ['0<(alpha:R)', 'alpha<=beta', 'ContDiff R 2 V', 'forall x v, alpha*norm(v)^2 <= (fderiv R (fderiv R V) x v) v <= beta*norm(v)^2', '0<eta', '(beta:R)*eta<=1'],
        'literal_context': context,
        'retain_unchanged': 'All37 literal definitions and the entire107 global witness contract (including joint Borel expectation and inherited bounded signed duality). No arbitrary supplied path, law, transition kernel or CLM.',
        'quantifier_placement': 'After the37 literal definitions, exists ONE Z with all107 global outputs; for every y,r exists ONE A indexed by T with ALL107 family conclusions AND the following additional flip/adjoint package. The A used in new conclusion is the same existential family, not a second A.',
        'additional_package': 'Exists hR:MeasurePreserving R (nu y) (nu y); let J_y := Lp.compMeasurePreserving_linearIsometry R hR on Lp R 2 (nu y). For every f, J_y f agrees nu_y-a.e. with z |-> f(R z) and J_y(J_y f)=f. For every T:NNReal, (A T).adjoint = J_y.toContinuousLinearMap.comp((A T).comp J_y.toContinuousLinearMap).',
        'hR_is_output_not_binder': True,
        'J_parameter_dependence': 'The displayed existential proof may occur under y,r for convenient preservation of107 quantifiers; J is literally pullback by the fixed R on nu_y and is proof-independent, hence independent of r and T. A stronger forall y exists J then forall r exists A arrangement is equivalent if same-Z family is retained.',
        'representative_sense': 'For arbitrary L2 classes only almost-everywhere representatives; arbitrary MemLp expectation identity remains exactly107. No common null set across all y,r,T or all representatives is claimed.',
        'constants': 'Contraction1 and A0=id inherited, all real T>=0, original eta cap inclusive. No new constants.'
    },
    'selected_route_steps': route,
    'why_substantive': 'Closes the currently red all-real-L2 adjoint identity, not a bounded-test restatement or wrapper. Enables later momentum-averaged position self-adjointness and provides a true operator relation for future analytic consumers.',
    'real_future_consumers': ['Source A.1 final Gaussian momentum averaging: Pi_p A_T Pi_p* self-adjoint, after actual averaging maps/identities are proved.', 'Future source hypocoercive operator analysis can consume actual A3 together with independently proved domain/continuity/semigroup results.'],
    'no_smaller_prerequisite_required_as_separate_SAU': 'Flip-isometry, dense representatives and the two-variable continuity extension are bounded internal dependencies supported by pinned APIs. No identified missing source assumption forces a preceding SAU.',
    'readiness': 'Candidate only; requires independent topology/header review and completed107 delivery before scheduling.',
    'remaining_red': ['Markov/restart and semigroup law for this SAME Z/A', 'strong continuity of A_T', 'identification with separately constructed83 or other kernel witness', 'complex-L2 extension', 'actual momentum-averaged position operator construction/self-adjointness', 'hypocoercivity/convergence', 'implementation errors, expected-query costs, actual-input composition and full-paper completion'],
    'edge_cases': ['rank0 gives one-point phase; pullback identity still meaningful, no positive dimension premise', 'T=0 inherited A0=id and J squared=id gives A3', 'zero normal or event boundaries are already covered by literal total path/bounce conventions, no continuity of bounce required', 'no event-count n binder introduced; inherited empty sectors/time0 retained'],
    'source_gap': 'The source compresses the density extension into one sentence. This packet expands that analytic step without assuming its conclusion. Source calls process operators Markov, but the selected A3 identity does not use or assert an unproved semigroup/restart contract.'
})

nodes = list(base['nodes'])
edges = list(base['edges'])
ids = {n['id'] for n in nodes}
new_nodes = []
for api in apis:
    if api['id'] not in ids:
        n = {'id': api['id'], 'kind': 'pinned-Mathlib-leaf', 'binding': api}
        nodes.append(n)
        new_nodes.append(n)
        ids.add(api['id'])
meanings = {
    'FLIP-L2-108': 'Canonical Lp pullback of actual phase R; isometry, representative formula and involution; same actual nu_y.',
    'SIMPLE-REP108': 'Dense L2 simple classes with measurable bounded MemLp representatives and their exact toLp identifications.',
    'BOUNDED-PAIR108': 'Same107 Z/A bounded signed duality converted to L2 pairings on simple representatives.',
    'FULL-PAIR108': 'Continuous two-variable extension to all real L2 classes, with L2 product integrability.'
}
for name, meaning in meanings.items():
    assert name not in ids
    n = {'id': name, 'kind': 'required-internal-adapter', 'meaning': meaning, 'status': 'unproved prospective108'}
    nodes.append(n)
    new_nodes.append(n)
    ids.add(name)
groups = [
    ('PHASE-FLIP106', ['MeasureTheory.isZeroOrProbabilityMeasure_tilted', 'ProbabilityTheory.stdGaussian_map', 'MeasureTheory.Measure.map_prod_map'], 'existing canonical flip fact reconstructed internally from the literal law; not a call to private106 hR'),
    ('FLIP-L2-108', ['PHASE-FLIP106', 'MeasureTheory.Lp.compMeasurePreservingₗᵢ', 'MeasureTheory.Lp.coeFn_compMeasurePreserving', 'MeasureTheory.Lp.compMeasurePreserving_comp', 'MeasureTheory.Lp.compMeasurePreserving_id', 'LinearIsometry.inner_map_map'], 'actual R involution, pullback AE and isometry'),
    ('SIMPLE-REP108', ['MeasureTheory.Lp.simpleFunc.toSimpleFunc', 'MeasureTheory.Lp.simpleFunc.measurable', 'MeasureTheory.Lp.simpleFunc.memLp', 'MeasureTheory.Lp.simpleFunc.toLp_toSimpleFunc', 'MeasureTheory.SimpleFunc.exists_forall_norm_le', 'MeasureTheory.Lp.simpleFunc.denseRange'], 'finite-range representatives plus density'),
    ('BOUNDED-PAIR108', ['AVG100', 'L2-IDENTIFY107', 'AE-REP107', 'SIMPLE-REP108', 'FLIP-L2-108', 'MeasureTheory.MemLp.comp_measurePreserving', 'MeasureTheory.MemLp.coeFn_toLp', 'MeasureTheory.L2.inner_def'], 'all same-witness107 projections, bounded duality and representative identification'),
    ('FULL-PAIR108', ['BOUNDED-PAIR108', 'L2-LIFT107', 'FLIP-L2-108', 'SIMPLE-REP108', 'DenseRange.induction_on₂', 'continuous_inner', 'MeasureTheory.L2.integrable_inner'], 'closed equality locus on product Hilbert space'),
    ('L2A3', ['FULL-PAIR108', 'FLIP-L2-108', 'ContinuousLinearMap.adjoint', 'ContinuousLinearMap.adjoint_inner_left', 'ext_inner_left'], 'adjoint uniqueness with flip involution/isometry; canonical target retained')
]
added_edges = []
for target, parents, mechanism in groups:
    for parent in parents:
        assert parent in ids and target in ids
        e = {'source': parent, 'target': target, 'scope': 'prospective108-selected-density-route', 'mechanism': mechanism}
        if not any(x['source'] == parent and x['target'] == target for x in edges):
            edges.append(e)
            added_edges.append(e)
graph = write('source-proof-graph-delta108.native.json', {
    'kind': 'unadmitted append-only prospective108 graph refinement',
    'base_graph': binding(basepath), 'nodes': nodes, 'edges': edges,
    'new_nodes': new_nodes, 'new_edges': added_edges,
    'counts': {'base_nodes': len(base['nodes']), 'base_edges': len(base['edges']), 'nodes': len(nodes), 'edges': len(edges)},
    'inherited_route_logic': {k: base[k] for k in ['AND_groups', 'superseded_single_route_AND_groups', 'AND_route_alternatives', 'OR_semantics']},
    'new_AND_groups': [{'target': t, 'parents': ps, 'mechanism': m} for t, ps, m in groups],
    'OR_route_policy': {'target': 'L2A3', 'selected': 'dense-simple-two-variable-extension', 'alternatives': [
        {'id': 'dense-simple-two-variable-extension', 'AND': [t for t, _, _ in groups], 'status': 'selected prospective route'},
        {'id': 'bounded-truncation-L2-limit', 'status': 'unselected mathematical alternative, no API claim or graph admission', 'obligations': ['measurable truncation', 'L2 convergence', 'pullback convergence', 'continuity of both pairings']}
    ], 'not_mandatory_union': True},
    'same_witness_constraint': {'nodes': ['AVG100', 'INV100', 'L2-LIFT107', 'L2-IDENTIFY107', 'AE-REP107'], 'producer': context, 'rule': 'All current108 process facts projected from ONE invocation of107. Historical graph ancestors do not authorize choosing a fresh105/106 path.'},
    'inherited_L2A3_coarse_edges': 'Retained as ancestry/dependency summaries, not removed or reinterpreted as theorem credit. Selected fine route expands them; INV100 is already internal to107 L2 lift rather than a new direct108 process producer.',
    'actual_direct_producers_planned': ['AutoSamplingTheory.ExampleCases.ProximalBPS.ActualL2Expectation.actual_l2_expectation_contraction'],
    'creator_does_not_validate_topology': True,
    'no_header_or_implementation_or_claim': True
})

dispositions = []
for region in primary['regions']:
    rid = region['id']
    if rid == 'A3-boundary':
        disposition = 'Selected EqA3 fixed-time real-L2 identity; surrounding semigroup/strong-continuity/averaged-kernel consequences excluded; heuristic generator exponentiation not used.'
    elif rid == 'weight-matching-and-invariance':
        disposition = 'Selected bounded duality and explicit density-extension sentence; bounded duality inherited from107 same Z, density extension is new108 obligation.'
    elif rid in ['phase-gibbs-law', 'target-position-energy']:
        disposition = 'Literal actual law and energy identify phase-flip pullback; normalization inherited, no new Gibbs theorem credit.'
    elif rid in ['standing-curvature', 'standing-eta']:
        disposition = 'All six original analytic source assumptions retained unchanged.'
    elif rid == 'source-license':
        disposition = 'Attribution/license retained; reference original local primary only.'
    else:
        disposition = 'Unchanged inherited actual-path/sector/averaging ancestor through107. No reproof or extra source credit in108; total event/zero conventions retained.'
    dispositions.append(dict(region, disposition=disposition))
coverage = write('source-coverage108.native.json', {
    'kind': 'prospective source coverage, not compiled coverage',
    'primary': primary['primary'], 'regions': dispositions,
    'graph': graph,
    'node_dispositions': [{'id': n['id'], 'disposition': 'new internal/API route obligation, no proof credit' if n in new_nodes else ('selected canonical target remains red until108 proved' if n['id'] == 'L2A3' else 'inherited node retained with original107 status and route alternatives')} for n in nodes],
    'edge_dispositions': [{'source': e['source'], 'target': e['target'], 'disposition': 'prospective selected108 dependency' if e in added_edges else 'unchanged inherited107 edge; no new completion credit'} for e in edges],
    'selected_proof_obligations': route,
    'future_consumers_are_future': True,
    'independent_topology_admission': 'required, not performed by source creator'
})
run = write('source-preread-run108.native.json', {
    'owner': '/root/source_final96', 'mode': 'source-only prospective108',
    'primary_first': binding(OUT / 'primary-first108.native.json'),
    'recommendation': recommendation, 'retrieval': retrieval, 'actual_interface': context,
    'graph': graph, 'coverage': coverage,
    'semantic_decision': 'RECOMMEND_ONE_BOUNDED_REAL_L2_A3_EDGE_CONDITIONAL_ON_107_DELIVERY',
    'not_a_source_fidelity_or_topology_admission': True,
    'no_production_header_seal_claim_shared_state_changes': True,
    'primary_reconstructed_before_retrieval': True,
    'prior107_involvement_acknowledged': True,
    'not_108_implementation': True
})
inputs = [primary['primary'], binding(basepath), binding(production), binding(ROOT / 'lake-manifest.json'), binding(ROOT / 'lean-toolchain')]
inputs.extend(a['file'] for a in apis)
inputs.extend(binding(ROOT / p) for p, _ in screen)
unique = {x['path']: x for x in inputs}
artifacts = [binding(p) for p in sorted(OUT.iterdir()) if p.is_file() and p.suffix != '.gz']
archives = []
for a in artifacts:
    p = ROOT / a['path']
    z = p.with_name(p.name + '.raw.gz')
    assert not z.exists()
    z.write_bytes(gzip.compress(p.read_bytes(), mtime=0))
    assert gzip.decompress(z.read_bytes()) == p.read_bytes()
    archives.append({'original': a, 'archive': binding(z), 'recovered_raw_sha256': a['raw_sha256']})
closure = write('closed-RAW-manifest108.native.json', {
    'kind': 'immutable native source-only108 closure', 'inputs': list(unique.values()),
    'artifacts': artifacts, 'archives': archives, 'run': run,
    'source_license_no_full_primary_copy': True,
    'topology_admission': False, 'theorem_credit': False,
    'mutable_context_snapshots': 'Scheduling inputs preserved as exact context snapshots. They are not mathematical assumptions or theorem evidence.'
})
print(json.dumps({'recommendation': recommendation, 'graph': graph, 'coverage': coverage, 'run': run, 'closure': closure}, indent=2))
