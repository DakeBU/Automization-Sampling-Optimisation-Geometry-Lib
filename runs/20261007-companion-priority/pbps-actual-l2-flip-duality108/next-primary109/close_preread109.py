import copy
import gzip
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
RUN = OUT.parent
BASE = ROOT / 'runs/20261007-companion-priority/pbps-actual-l2-expectation107/next-primary108'
inputs = {}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def bind(p):
    p = Path(p)
    if not p.is_absolute():
        p = ROOT / p
    b = p.read_bytes()
    result = {'path': p.relative_to(ROOT).as_posix(), 'raw_sha256': sha(b), 'bytes': len(b)}
    inputs[result['path']] = result
    return result


def read(p):
    bind(p)
    return json.loads(Path(p).read_text(encoding='utf-8'))


def emit(name, value):
    p = OUT / name
    assert not p.exists(), p
    p.write_bytes((json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
    return bind(p)


primary = read(OUT / 'primary-first109.native.json')
source = ROOT / primary['primary']['path']
assert bind(source) == primary['primary']
raw = source.read_bytes()
for region in primary['regions']:
    assert sha(raw[region['byte_start']:region['byte_end_exclusive']]) == region['raw_sha256']
base_path = BASE / 'route-policy-repair108/source-proof-graph-delta108.v2.native.json'
base = read(base_path)
admission = bind(BASE / 'independent-topology108/v2-admission/admission108.v2.native.json')
producer = ROOT / 'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualL2FlipDuality.lean'
producer_binding = bind(producer)
assert producer_binding['raw_sha256'] == '2358ce3e7a74b5d1ebdf857be873588db3ffdefd08239b7f2df37bf6b72349cd'
producer_lines = producer.read_bytes().splitlines(keepends=True)
for name in ['compiled-source-coverage108.native.json', 'closed-RAW-final-source108.native.json']:
    bind(RUN / 'final-source108' / name)
for p in OUT.glob('*.context.*'):
    bind(p)
bind(ROOT / 'lean-toolchain')
bind(ROOT / 'lake-manifest.json')

api_specs = [
    ('MeasureTheory.measurePreserving_fst', 'MeasureTheory/Measure/Prod.lean', 258, 260),
    ('MeasureTheory.ae_ae_of_ae_prod', 'MeasureTheory/Measure/Prod.lean', 433, 438),
    ('MeasureTheory.Lp.compMeasurePreservingₗᵢ', 'MeasureTheory/Function/LpSpace/Basic.lean', 632, 635),
    ('MeasureTheory.Lp.coeFn_compMeasurePreserving', 'MeasureTheory/Function/LpSpace/Basic.lean', 572, 574),
    ('MeasureTheory.MemLp.coeFn_toLp', 'MeasureTheory/Function/LpSpace/Basic.lean', 111, 113),
    ('MeasureTheory.Lp.ext', 'MeasureTheory/Function/LpSpace/Basic.lean', 146, 149),
    ('MeasureTheory.MemLp.integrable', 'MeasureTheory/Function/L1Space/Integrable.lean', 659, 665),
    ('MeasureTheory.Integrable.prod_right_ae', 'MeasureTheory/Integral/Prod.lean', 250, 254),
    ('MeasureTheory.Integrable.integral_prod_left', 'MeasureTheory/Integral/Prod.lean', 335, 340),
    ('MeasureTheory.integral_prod', 'MeasureTheory/Integral/Prod.lean', 444, 450),
    ('MeasureTheory.Integrable.ae_eq_of_forall_setIntegral_eq', 'MeasureTheory/Function/AEEqOfIntegral.lean', 364, 369),
    ('MeasureTheory.indicatorConstLp', 'MeasureTheory/Function/LpSpace/Indicator.lean', 98, 105),
    ('MeasureTheory.indicatorConstLp_coeFn', 'MeasureTheory/Function/LpSpace/Indicator.lean', 115, 122),
    ('MeasureTheory.MemLp.ae_eq', 'MeasureTheory/Function/LpSeminorm/Basic.lean', 489, 492),
    ('MeasureTheory.L2.inner_def', 'MeasureTheory/Function/L2Space.lean', 137, 138),
    ('MeasureTheory.L2.integrable_inner', 'MeasureTheory/Function/L2Space.lean', 172, 175),
    ('MeasureTheory.isZeroOrProbabilityMeasure_tilted', 'MeasureTheory/Measure/Tilted.lean', 138, 146),
    ('ProbabilityTheory.isProbabilityMeasure_stdGaussian', 'Probability/Distributions/Gaussian/Multivariate.lean', 72, 75),
    ('ContinuousLinearMap.adjoint', 'Analysis/InnerProductSpace/Adjoint.lean', 114, 116),
    ('ContinuousLinearMap.adjoint_inner_right', 'Analysis/InnerProductSpace/Adjoint.lean', 127, 128),
    ('ContinuousLinearMap.adjoint_adjoint', 'Analysis/InnerProductSpace/Adjoint.lean', 132, 133),
    ('ContinuousLinearMap.adjoint_comp', 'Analysis/InnerProductSpace/Adjoint.lean', 138, 141),
    ('LinearIsometry.adjoint_comp_self', 'Analysis/InnerProductSpace/Adjoint.lean', 1062, 1066),
    ('ContinuousLinearMap.opNorm_comp_le', 'Analysis/Normed/Operator/Basic.lean', 395, 399),
    ('LinearIsometry.norm_toContinuousLinearMap_le', 'Analysis/Normed/Operator/Basic.lean', 492, 495),
    ('LinearIsometry.inner_map_map', 'Analysis/InnerProductSpace/LinearMap.lean', 115, 118),
]
apis = []
for ident, filename, start, end in api_specs:
    p = ROOT / '.lake/packages/mathlib/Mathlib' / filename
    b = p.read_bytes()
    excerpt = b''.join(b.splitlines(keepends=True)[start - 1:end])
    apis.append({'id': ident, 'file': bind(p), 'line_start': start, 'line_end': end,
                 'span_raw_sha256': sha(excerpt), 'text': excerpt.decode('utf-8'),
                 'status': 'pinned API inspected; prospective use, not a new compiled ASTIS edge'})
local_specs = [
    ('AutoSamplingTheory/TechnicalLemmas/Measure/L2PullbackRange.lean', 'Pullback range/comap measurable classes; no actual Gaussian adjoint integral identification.'),
    ('AutoSamplingTheory/TechnicalLemmas/Measure/L2Expectation.lean', 'Scalar expectation functional; not the fiberwise position average.'),
    ('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualCorrectorChange.lean', 'Different joint law/snd projection; no matching position-first pi times gamma provider.'),
    ('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualOuterBoundedL2Continuity.lean', 'Own existential Z and bounded continuous tests; cannot substitute for the SAME108 L2 family. Future strong-continuity route requires alignment and density.'),
    ('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPhaseTransitionKernel.lean', 'Own existential Z and kernel laws; same-witness identification with108 is unproved, so not a producer for109.'),
    ('AutoSamplingTheory/ExampleCases/ProximalBPS/IdealHalfTurnKernel.lean', 'Actual independent-reference/half-turn kernel is a future consumer after alignment; do not identify its separately existential Z automatically.'),
    ('Libraries/frontloaded-shared-spine.json', 'Shared background screened; no matching actual continuous phase Gaussian averaging theorem.'),
    ('research-wiki/external-lean-libraries/lean-stat-learning-theory.md', 'Pinned external catalog d0f506f0a695018265dccb33bcb05e2f5ca1c876, Lean4.32 versus local4.33; not callable. Product slicing APIs already present in pinned Mathlib; no port proposed.'),
]
locals_found = [{'file': bind(ROOT / p), 'disposition': d} for p, d in local_specs]
retrieval = emit('retrieval109.native.json', {
    'kind': 'bounded local and pinned API retrieval109', 'apis': apis, 'local_and_compatible_screen': locals_found,
    'direct_process_producer': producer_binding,
    'private_api_policy': 'No private/mangled producer. Prior107 haverage_core is only a mathematical pattern, not a callable declaration.',
    'scheduling': 'Captured handoff/execution lag behind current108 cell; current cell and accepted108 exact producer are authoritative for this recommendation. Readiness still conditional on completed108 delivery.',
    'no_external_certificate_or_port_claim': True})

assumptions = [
    '0 < (alpha : Real)', 'alpha <= beta', 'ContDiff Real 2 V',
    'forall x v, alpha*norm(v)^2 <= (fderiv Real (fderiv Real V) x v) v and (fderiv Real (fderiv Real V) x v) v <= beta*norm(v)^2',
    '0 < eta', '(beta : Real)*eta <= 1']
conclusions = [
    'Retain ONE global actual Z and every108 conclusion, including measurability, live-arc/fallback contract and parameterwise P-AE Z0. For each y,r retain the SAME family A_T and hR/J supplied by108; all109 clauses live in that existential scope.',
    'Let pi_y=volume.tilted(fun x => -Vy y x), gamma=stdGaussian E, nu_y=pi_y.prod gamma. Derive hfst:MeasurePreserving Prod.fst nu_y pi_y. Define B=Lp.compMeasurePreserving_li Real Prod.fst hfst, M=B.toContinuousLinearMap.adjoint. B has its literal representative f(x), norm(B)<=1, norm(M)<=1 and M.comp B=id.',
    'For every G:H->Real and hG:MemLp G 2 nu_y, pi_y-AE x the gamma section G(x,.) is integrable. With gbar(x)=integral p,G(x,p) dgamma, obtain hbar:MemLp gbar 2 pi_y and M(hG.toLp G)=hbar.toLp gbar. This is for arbitrary MemLp representatives, not only Borel bounded ones.',
    'For every f:L2(pi_y), J(B f)=B f; as continuous linear maps M.comp J=M. All lift/flip representative equalities are AE, never pointwise at arbitrary quotient representatives.',
    'Define K_T=M.comp((A_T).comp B.toContinuousLinearMap), for every nonnegative T. Prove (K_T).adjoint=K_T, norm(K_T)<=1, and K_0=id.',
    'For every f:E->Real, hf:MemLp f 2 pi_y, and T:NNReal, let kTf(x)=integral p,(integral w,f((Z y r (x,p) T w).1) dP) dgamma. Prove pi_y-AE x, gamma-AE p the inner clock section is P-integrable; pi_y-AE x the outer integrand is gamma-integrable; obtain hk:MemLp kTf 2 pi_y and K_T(hf.toLp f)=hk.toLp kTf. The gamma outer / P inner order is literal; no exchange is silently assumed.'
]
interface = emit('actual-interface109.native.json', {
    'kind': 'precise prospective mathematical boundary; no Lean header', 'producer': producer_binding,
    'public_declaration': 'AutoSamplingTheory.ExampleCases.ProximalBPS.ActualL2FlipDuality.actual_l2_flip_duality',
    'literal_statement_span': {'start': 14, 'end': 171, 'raw_sha256': sha(b''.join(producer_lines[13:171]))},
    'public_binders_span': {'start': 175, 'end': 183, 'raw_sha256': sha(b''.join(producer_lines[174:183]))},
    'ambient': 'E real finite-dimensional Hilbert space with Borel measurable structure; V:E->Real, alpha beta:NNReal, eta:Real; H=E times E position first; Omega=Nat->Real.',
    'original_six_assumptions': assumptions,
    'literal_definition_contract': 'Retain all37 algorithm/measure definitions of108 verbatim, including its actual P, epsilon, history guard A, R, Vy, nu. Retain globalZ and all108 outputs. Operator family A is locally scoped separately from history guard A; proposed K is position operator, not inherited algorithm K. Use distinct Lean identifiers when authoring.',
    'exact_energy': 'Vy(y,x)=V(x)+norm(x-y)^2/(2*eta); gamma is the probability stdGaussian E, with no density normalization multiplied into the averaging integral.',
    'conclusions': conclusions,
    'quantifier_order': 'six assumptions ->37 actual literals ->exists globalZ with all108 contract ->forall y r ->exists SAME A with all108 outputs ->derived hfst,B,M ->allG Gaussian identification and flip absorption ->literal K ->forallT and allf representative/contraction/selfadjoint claims',
    'no_new_binders': ['no supplied normalizer/minimizer', 'no supplied integrability or positivity', 'no arbitrary Z,A,B,M,K', 'no probability/provider assumption', 'no extra smoothness or dimension positivity'],
    'edge_cases': ['rank0 uses same standard Gaussian and L2 constructions; no division by dimension', 'T=0 from same A0 and B*B=id', 'y and r unrestricted', 'arbitrary MemLp representatives yield parameterwise AE statements; no uniform null set', 'jump times and fallback retain108 contract; no path reversal assertion'],
    'definition_technicality': 'Finite/SFinite pi follows from tilted zero-or-probability; gamma is probability. This suffices for lift and Fubini, so no separate103 normalizer invocation is required.'})

route = [
    'Invoke actual108 once and keep its globalZ, same A, same canonical J and every inherited contract; derive pi/gamma finite-product instances internally.',
    'Construct position lift B with measurePreserving_fst and Lp.compMeasurePreserving_li. Set M=B*. Get contraction and B*B=id from LinearIsometry.norm_toContinuousLinearMap_le, adjoint isometry and LinearIsometry.adjoint_comp_self.',
    'For arbitrary G in MemLp2, use MemLp.integrable, Integrable.prod_right_ae and integral_prod_left to obtain section/average L1. Pair M[G] against indicatorConstLp(s,1); adjoint_inner_right, L2.inner_def, L2.integrable_inner and integral_prod identify all measurable-set integrals. Integrable.ae_eq_of_forall_setIntegral_eq gives the literal Gaussian average representative; MemLp.ae_eq transports L2 membership.',
    'Use the actual J/B AE representatives, Lp.ext and R(x,p).1=x to prove J B=B. J is self-adjoint from its isometry and involution (inner_map_map/adjoint uniqueness); take adjoints to prove M J=M.',
    'Define K=M A B. Expand adjoint_comp and use108 A*=J A J plus absorption to obtain K*=K. opNorm_comp_le gives norm<=1, and A0/B*B give K0=id.',
    'Apply same108 expectation identification to f composed with Prod.fst, using MemLp.comp_measurePreserving. Slice its AE clock-integrability with ae_ae_of_ae_prod; apply step3 to its MemLp opG to obtain the literal outer Gaussian integral, outer integrability, and K representative.',
    'Retain exact six assumptions, all-time indexing and parameterwise AE scope; expose actual position expectation as the future A2 independent-reference averaging input, without claiming Markovness or reference integration.'
]
reds = ['Markov positivity and constant preservation of K', 'strong continuity on all phase or position L2', 'semigroup/restart/kernel identity', 'independent reference averaging at T=pi and joint parameter integral/quotient identification', 'identification with the separately existential IdealHalfTurnKernel witness', 'complex L2 extension', 'hypocoercive convergence and query cost', 'whole A1/A2/paper/Goal completion']
recommendation = emit('recommendation109.native.json', {
    'kind': 'one prospective source-backed substantive edge', 'recommended_boundary': 'actual Gaussian momentum averaging and fixed-reference position L2 self-adjoint contraction',
    'primary_first': bind(OUT / 'primary-first109.native.json'), 'interface': interface, 'retrieval': retrieval,
    'source_anchors': ['A.1(iii), original A3-boundary', 'A.1 final Gaussian-momentum-averaging lines3246-3259', 'A.2 lines3265-3287 future consumer only'],
    'source_license': primary['source_license'], 'seven_step_route': route,
    'substantive_delta': 'Build and identify the actual Gaussian adjoint averaging for every MemLp representative, then identify its same-process nested clock action and prove position self-adjoint contraction. Abstract B*AB algebra alone would be too small; it is not the proposed SAU.',
    'why_dependency_ready': '108 supplies actual same-witness A/J and full realL2 flip identity. Pinned Mathlib supplies product Fubini, quotient/pullback and adjoint APIs. No smaller mathematical prerequisite or new public hypothesis was found.',
    'why_not_strong_continuity_next': 'Source proof separates the preceding strong-continuity paragraph from the final algebraic averaging paragraph. Existing bounded-continuity theorem uses a separately existential Z and needs alignment/dense extension; it is not a prerequisite to this averaging edge.',
    'direct_producers': [producer_binding], 'same_witness': 'Exactly one108 process/operator producer; never combine existentialZ or A selected by different theorem calls.',
    'actual_consumer': 'A.2 independent-reference half-turn operator needs the fixed-reference actual position operator and its self-adjoint L2 action;109 supplies that ingredient, while reference averaging, Markovness and kernel witness alignment remain explicit future obligations.',
    'source_gap': 'Source suppresses Gaussian-average L2 representative/Fubini/adjoint identification. Complete it internally using the listed APIs, without integrability binders. Source also asserts Markovness, which this deliberately bounded candidate leaves red.',
    'remaining_red_boundaries': reds, 'expected_semantic_slots': primary['expected_semantic_slots'],
    'readiness': 'conditional on108 complete independent admission/integration/delivery;108 source/math acceptance is not delivery',
    'no_header_proof_claim_or_second_active_SAU': True, 'no_creator_topology_admission': True})

graph = copy.deepcopy(base)
old_ids = {n['id'] for n in graph['nodes']}
new_nodes = []
for a in apis:
    if a['id'] not in old_ids:
        new_nodes.append({'id': a['id'], 'kind': 'pinned-Mathlib-api', 'retrieval': retrieval['path']})
        old_ids.add(a['id'])
meanings = {
    'MOMENTUM-LIFT109': 'Actual hfst and position lift B; M=B*; contraction and B*B=id.',
    'MOMENTUM-L1-FUBINI109': 'Finite product L2-to-L1, Gaussian sections/average L1 and indicator-weighted signed Fubini; no input integrability premise.',
    'MOMENTUM-IDENTIFY109': 'M[G] equals the class of the literal Gaussian integral for every MemLp representative, with AE integrable sections.',
    'FLIP-ABSORB109': 'Same108 J fixes position lift; J*=J, and M J=M.',
    'POSITION-OP109': 'Literal K=M A B is self-adjoint contraction with K0=id.',
    'POSITION-REP109': 'Same108 Z/A produces K as Gaussian-outer clock-inner actual position expectation, with both section-integrability obligations.',
    'POSITION-AVG109': 'Selected109 actual Gaussian averaging/position operator package; not full Markov or A2.'}
new_nodes += [{'id': k, 'kind': 'prospective109-obligation', 'meaning': v, 'status': 'unproved'} for k, v in meanings.items()]
groups = [
    ('MOMENTUM-LIFT109', ['MeasureTheory.measurePreserving_fst', 'ProbabilityTheory.isProbabilityMeasure_stdGaussian', 'MeasureTheory.isZeroOrProbabilityMeasure_tilted', 'MeasureTheory.Lp.compMeasurePreservingₗᵢ', 'MeasureTheory.Lp.coeFn_compMeasurePreserving', 'ContinuousLinearMap.adjoint', 'LinearIsometry.adjoint_comp_self', 'LinearIsometry.norm_toContinuousLinearMap_le']),
    ('MOMENTUM-L1-FUBINI109', ['MOMENTUM-LIFT109', 'MeasureTheory.MemLp.integrable', 'MeasureTheory.Integrable.prod_right_ae', 'MeasureTheory.Integrable.integral_prod_left', 'MeasureTheory.integral_prod', 'MeasureTheory.L2.integrable_inner', 'MeasureTheory.indicatorConstLp', 'MeasureTheory.indicatorConstLp_coeFn']),
    ('MOMENTUM-IDENTIFY109', ['MOMENTUM-LIFT109', 'MOMENTUM-L1-FUBINI109', 'ContinuousLinearMap.adjoint_inner_right', 'MeasureTheory.L2.inner_def', 'MeasureTheory.Integrable.ae_eq_of_forall_setIntegral_eq', 'MeasureTheory.MemLp.ae_eq', 'MeasureTheory.MemLp.coeFn_toLp', 'MeasureTheory.Lp.ext']),
    ('FLIP-ABSORB109', ['FLIP-L2-108', 'MOMENTUM-LIFT109', 'LinearIsometry.inner_map_map', 'ContinuousLinearMap.adjoint_inner_left', 'ContinuousLinearMap.adjoint_comp', 'ContinuousLinearMap.adjoint_adjoint', 'MeasureTheory.Lp.ext']),
    ('POSITION-OP109', ['L2A3', 'L2-LIFT107', 'FLIP-ABSORB109', 'MOMENTUM-LIFT109', 'ContinuousLinearMap.adjoint_comp', 'ContinuousLinearMap.adjoint_adjoint', 'ContinuousLinearMap.opNorm_comp_le']),
    ('POSITION-REP109', ['POSITION-OP109', 'MOMENTUM-IDENTIFY109', 'L2-IDENTIFY107', 'AE-REP107', 'MeasureTheory.MemLp.comp_measurePreserving', 'MeasureTheory.ae_ae_of_ae_prod', 'MeasureTheory.MemLp.coeFn_toLp', 'MeasureTheory.Lp.ext']),
    ('POSITION-AVG109', ['MOMENTUM-IDENTIFY109', 'FLIP-ABSORB109', 'POSITION-OP109', 'POSITION-REP109'])]
new_groups = [{'target': t, 'parents': ps, 'mechanism': meanings[t], 'source_scope': 'gaussian-momentum-averaging'} for t, ps in groups]
new_edges = [{'source': p, 'target': g['target'], 'scope': 'prospective109-selected-adjoint-averaging', 'mechanism': g['mechanism']} for g in new_groups for p in g['parents']]
graph = {
    'kind': 'unadmitted prospective109 effective graph proposal', 'base_graph': bind(base_path), 'base_independent_admission': admission,
    'nodes': base['nodes'] + new_nodes, 'edges': base['edges'] + new_edges,
    'new_nodes': new_nodes, 'new_edges': new_edges, 'new_AND_groups': new_groups,
    'inherited_route_logic': {k: base[k] for k in ['inherited_route_logic', 'new_AND_groups', 'OR_route_policy', 'inherited_L2A3_coarse_edges']},
    'OR_route_policy': {'target': 'POSITION-AVG109', 'selected': 'actual-adjoint-Gaussian-identification', 'alternatives': [{'id': 'actual-adjoint-Gaussian-identification', 'AND': ['MOMENTUM-IDENTIFY109', 'FLIP-ABSORB109', 'POSITION-OP109', 'POSITION-REP109']}], 'not_mandatory_union': True},
    'same_witness_constraint': 'L2A3,FLIP-L2-108,L2-LIFT107,L2-IDENTIFY107,AE-REP107 are retained projections of ONE actual108 invocation and SAME globalZ/A, not separately invoked producers.',
    'actual_direct_producers_planned': [producer_binding], 'future_consumer_not_a_current_prerequisite': 'A2 reference average at T=pi; Markov and independent-reference integration remain red.',
    'creator_does_not_validate_topology': True, 'no_header_or_implementation_or_claim': True}
graph['counts'] = {'nodes': len(graph['nodes']), 'edges': len(graph['edges']), 'inherited_nodes': len(base['nodes']), 'inherited_edges': len(base['edges']), 'new_nodes': len(new_nodes), 'new_edges': len(new_edges)}
assert len({n['id'] for n in graph['nodes']}) == len(graph['nodes'])
for g in new_groups:
    assert g['target'] not in g['parents']
assert 'POSITION-AVG109' not in graph['OR_route_policy']['alternatives'][0]['AND']
graph_binding = emit('source-proof-graph-delta109.native.json', graph)
regions = []
for r in primary['regions']:
    r = dict(r)
    if r['id'] == 'gaussian-momentum-averaging':
        r.update(disposition='selected substantive109 slice; Markov clause explicitly excluded', nodes=list(meanings))
    elif r['id'] == 'strong-continuity-after-A3':
        r.update(disposition='independent future red edge, not an averaging prerequisite', nodes=[])
    elif r['id'] == 'averaged-halfturn-consumer':
        r.update(disposition='future real consumer; no A2/kernel/reversibility completion credit', nodes=['POSITION-AVG109'])
    elif r['id'] in ['standing-curvature', 'standing-eta', 'target-position-energy', 'phase-gibbs-law', 'source-license']:
        r.update(disposition='unchanged source assumptions/actual laws/license retained', nodes=['MOMENTUM-LIFT109'])
    elif r['id'] == 'A3-boundary':
        r.update(disposition='108 full realL2 flip result reused;109 selects only actual momentum averaging self-adjoint/contraction part; other proposition clauses unchanged/red', nodes=['L2A3', 'POSITION-AVG109'])
    else:
        r.update(disposition='unchanged inherited108 source route; no new proof credit and no changed path conventions', nodes=[])
    regions.append(r)
coverage = emit('source-coverage109.native.json', {
    'kind': 'prospective exhaustive source-region and graph disposition, not compiled coverage', 'graph': graph_binding,
    'regions': regions, 'source_regions_count': len(regions), 'inherited_regions': 21, 'new_regions': 3,
    'inherited_coverage': bind(RUN / 'final-source108/compiled-source-coverage108.native.json'),
    'node_dispositions': [{'id': n['id'], 'status': ('inherited unchanged; status/compiled correspondence remains in108 coverage, including red boundaries' if n['id'] in {x['id'] for x in base['nodes']} else ('prospective unproved109 obligation' if n['id'] in meanings else 'pinned API inspected; no new ASTIS theorem credit'))} for n in graph['nodes']],
    'edge_dispositions': [{'source': e['source'], 'target': e['target'], 'status': 'inherited unchanged' if i < len(base['edges']) else 'prospective proof ingredient dependency; not an extra source binder'} for i, e in enumerate(graph['edges'])],
    'proof_ingredients_are_not_public_assumptions': True, 'all_new_nodes_have_meaning_or_retrieval': True,
    'same_witness': graph['same_witness_constraint'], 'remaining_red_boundaries': reds,
    'independent_topology_admission_required': True})
emit('source-preread-run109.native.json', {
    'kind': 'closed source-only preread109', 'reviewer': '/root/source_final96', 'source_creator_not_topology_validator': True,
    'reading_order': ['fixed original primary and frozen24region/7slot record', 'exact accepted108 interface and current context snapshots', 'local, pinned Mathlib and compatible catalog retrieval', 'one bounded candidate/interface/graph/coverage'],
    'recommendation': recommendation, 'interface': interface, 'retrieval': retrieval, 'graph': graph_binding, 'coverage': coverage,
    'future_implementation_seen': False, 'production_or_shared_files_written': False, 'new_full_primary_archive': False,
    'diagnostic': 'A read-only inspection initially used platform-default GBK and raised UnicodeDecodeError; retried explicit UTF-8. No input/output mutation or semantic effect.',
    'readiness': '108 complete delivery required before scheduling109; no new SAU claim/Statement Seal/proof/Goal/state transition',
    'independent_admission': 'required for this graph; not issued by creator'})

artifacts = []
archives = []
archive_dir = OUT / 'raw-archives'
archive_dir.mkdir(exist_ok=False)
for p in sorted(OUT.iterdir()):
    if not p.is_file():
        continue
    b = p.read_bytes()
    artifact = bind(p)
    artifacts.append(artifact)
    dest = archive_dir / (p.name + '.gz')
    dest.write_bytes(gzip.compress(b, mtime=0))
    assert gzip.decompress(dest.read_bytes()) == b
    archives.append({'original': artifact, 'archive': {'path': dest.relative_to(ROOT).as_posix(), 'raw_sha256': sha(dest.read_bytes()), 'bytes': dest.stat().st_size}})
manifest = emit('closed-RAW-manifest109.native.json', {
    'kind': 'immutable prospective109 RAW closure', 'artifacts': artifacts, 'inputs': list(inputs.values()), 'archives': archives,
    'primary_archive_policy': 'Pinned existing primary referenced by exact RAW and24slice hashes; no full-primary archive created.',
    'all_archive_roundtrips_pass': True, 'readiness_conditional_on108_delivery': True, 'no_proof_or_topology_admission': True})
print(json.dumps({'recommendation': recommendation, 'interface': interface, 'retrieval': retrieval, 'graph': graph_binding, 'coverage': coverage, 'closure': manifest, 'counts': graph['counts']}, indent=2))
