from pathlib import Path
import gzip
import hashlib
import json

ROOT = Path('E:/Samplinglib')
BASE = ROOT / 'runs/20261007-companion-priority/pbps-actual-bounded-gibbs-duality106/next-primary107'
OUT = BASE / 'graph-expansion107'


def ref(p):
    b = p.read_bytes()
    return {'path': p.relative_to(ROOT).as_posix(), 'raw_sha256': hashlib.sha256(b).hexdigest(), 'bytes': len(b)}


def read(p):
    return json.loads(p.read_text(encoding='utf8'))


def put(name, obj):
    p = OUT / name
    assert not p.exists(), p
    p.write_bytes((json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode())
    return ref(p)


original = BASE / 'source-proof-graph-delta107.native.json'
assert ref(original)['raw_sha256'] == '87a64024bfa14dba0b0a6b8764fe08dd9410bb91cb7f95d14a70e5b897550022'
decision = BASE / 'independent-topology107/decision107.native.json'
assert ref(decision)['raw_sha256'] == '80dfd32e4244b66aed9419bc5bd848a682e8d0ba0848d521bc28a9779309b682'
g = read(original)
prior_apis = {a['declaration']: a for a in read(BASE / 'retrieval107.native.json')['api_signatures']}
needed = read(decision)['required_support_leaves']
extra = {
    'MeasureTheory.measurePreserving_fst': ('MeasureTheory/Measure/Prod.lean', 'lemma _root_.MeasureTheory.measurePreserving_fst'),
    'MeasureTheory.MemLp.comp_measurePreserving': ('MeasureTheory/Function/LpSeminorm/Basic.lean', 'theorem MemLp.comp_measurePreserving'),
    'MeasureTheory.MemLp.integrable': ('MeasureTheory/Function/L1Space/Integrable.lean', 'theorem MemLp.integrable {q'),
    'MeasureTheory.ae_ae_of_ae_prod': ('MeasureTheory/Measure/Prod.lean', 'theorem ae_ae_of_ae_prod'),
    'MeasureTheory.indicatorConstLp': ('MeasureTheory/Function/LpSpace/Indicator.lean', 'def indicatorConstLp '),
    'MeasureTheory.indicatorConstLp_coeFn': ('MeasureTheory/Function/LpSpace/Indicator.lean', 'theorem indicatorConstLp_coeFn :'),
}
apis = []
for name in needed + ['MeasureTheory.indicatorConstLp', 'MeasureTheory.indicatorConstLp_coeFn']:
    if name in prior_apis:
        a = dict(prior_apis[name])
        assert ref(ROOT / a['file']['path']) == a['file']
    else:
        tail, needle = extra[name]
        p = ROOT / '.lake/packages/mathlib/Mathlib' / tail
        ls = p.read_text(encoding='utf8').splitlines()
        i = next(i for i, s in enumerate(ls) if needle in s)
        a = {'declaration': name, 'file': ref(p), 'line_start': i + 1,
             'signature_excerpt': '\n'.join(ls[i:i + 6])}
    a['role'] = 'pinned existing Mathlib support; not a newly proved ASTIS theorem'
    apis.append(a)
api_receipt = put('support-api-bindings107.v2.native.json', {'leaves': apis, 'no_new_API_names_inferred': True})

internal = [
    {'id': 'L2-CONSTRUCT107', 'kind': 'required-internal-adapter',
     'meaning': 'Construct Q=B.adjoint composed C and norm≤1 using actual pullback isometries; no assertion about L2 membership of the expectation function is used.'},
    {'id': 'PRODUCT-L1-FUBINI107', 'kind': 'required-internal-adapter',
     'meaning': 'Actual L2 pullback implies product L1 under probability; derive ν-a.e. clock-section integrability and outer L1. Every measurable-set indicator-weighted pullback is product integrable by domination before signed Fubini.'},
    {'id': 'L2-IDENTIFY107', 'kind': 'required-internal-adapter',
     'meaning': 'Pair Q[G] with actual L2 indicators, use adjoint pairing and signed Fubini, then L1 set-integral uniqueness. Only after this a.e. equality infer expectation MemLp and equality of L2 classes.'},
    {'id': 'AE-REP107', 'kind': 'required-internal-adapter',
     'meaning': 'Endpoint measure preservation transports ν-a.e. equality of input representatives to product-a.e.; iterated-a.e. transfer and integral congruence yield ν-a.e. equality of actual clock expectations.'},
]
clock = 'AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws'
groups = [
    {'target': 'BOREL-OP107', 'parents': ['COUNT93', clock, 'MeasureTheory.StronglyMeasurable.integral_prod_right'],
     'mechanism': 'Joint Borel G∘Z gives a jointly Borel literal total integral. Bounded Borel tests additionally have every section integrable and the same bound. No Borel assertion for arbitrary MemLp representatives.'},
    {'target': 'L2-PRODUCT107', 'parents': ['INV100', 'NORM', clock, 'MeasureTheory.measurePreserving_fst', 'MeasureTheory.Lp.compMeasurePreservingₗᵢ'],
     'mechanism': 'Actual endpoint and initial projection preserve ν from ν.prod P; both induce real L2 isometric pullbacks B and C.'},
    {'target': 'L2-CONSTRUCT107', 'parents': ['L2-PRODUCT107', 'ContinuousLinearMap.adjoint'],
     'mechanism': 'Generic complete-Hilbert adjoint construction and operator norm preservation give Q=B†C with norm≤1. This generic adjoint does not assume the future PBPS A.3 identity.'},
    {'target': 'PRODUCT-L1-FUBINI107', 'parents': ['L2-PRODUCT107', 'NORM', clock, 'MeasureTheory.MemLp.comp_measurePreserving', 'MeasureTheory.MemLp.integrable', 'MeasureTheory.Integrable.prod_right_ae', 'MeasureTheory.Integrable.integral_prod_left'],
     'mechanism': 'MemLp input pulled back under actual endpoint is L2, hence L1 for finite product measure. Obtain section-a.e. and outer L1 before proving any L2 property of the expectation; indicator factors bounded by1 preserve product integrability.'},
    {'target': 'L2-IDENTIFY107', 'parents': ['L2-CONSTRUCT107', 'PRODUCT-L1-FUBINI107', 'MeasureTheory.Lp.coeFn_compMeasurePreserving', 'ContinuousLinearMap.adjoint_inner_right', 'MeasureTheory.L2.inner_def', 'MeasureTheory.integral_prod', 'MeasureTheory.indicatorConstLp', 'MeasureTheory.indicatorConstLp_coeFn', 'MeasureTheory.Integrable.ae_eq_of_forall_setIntegral_eq'],
     'mechanism': 'Both Q[G] and actual expectation are L1. Finite-measure set indicators are L2. Adjoint pairing plus signed Fubini identifies all set integrals; L1 uniqueness yields a.e. equality. Therefore, and only therefore, actual expectation is L2 and its class equals Q[G].'},
    {'target': 'AE-REP107', 'parents': ['INV100', 'MeasureTheory.ae_ae_of_ae_prod'],
     'mechanism': 'Measure-preserving endpoint pulls back input null sets, then product-to-iterated-a.e. equality and clock integral congruence establish representative independence. No uniform exceptional set over observables/parameters.'},
    {'target': 'L2-LIFT107', 'parents': ['BOREL-OP107', 'L2-PRODUCT107', 'COUNT93', 'L2-CONSTRUCT107', 'PRODUCT-L1-FUBINI107', 'L2-IDENTIFY107', 'AE-REP107'],
     'mechanism': 'Return same-Z bounded106 contract, genuine identified contraction, square-integral bound and T2 zero identity. Zero-time uses parameterwise clock-a.e. initialization. MemLp test membership remains an observable-domain condition, not a new analytic source premise.'},
]
base_nodes = g['inherited_nodes'] + [x['id'] for x in g['new_nodes']]
base_edges = [(x['source'], x['target']) for x in g['inherited_edges']] + [tuple(x) for x in g['new_edges']]
add_nodes = internal + [{'id': a['declaration'], 'kind': 'pinned-Mathlib-leaf', 'binding': a} for a in apis if a['declaration'] not in base_nodes]
add_edges = []
for group in groups:
    for parent in group['parents']:
        e = (parent, group['target'])
        if e not in base_edges and e not in add_edges:
            add_edges.append(e)
future_edge = ('PHASE-FLIP106', 'L2A3')
if future_edge not in base_edges:
    add_edges.append(future_edge)
overlay = put('ingredient-expansion107.proposal.native.json', {
    'kind': 'append-only source-graph ingredient expansion proposal, not independent admission',
    'author': '/root/source_final96', 'original_graph': ref(original), 'independent_findings': ref(decision),
    'original_recommendation': ref(BASE / 'recommendation107.native.json'), 'original_closure': ref(BASE / 'closed-RAW-preread107.native.json'),
    'changes': 'Add explicit support leaves and construction/L1/identification/AE-transport nodes. Refine107 AND groups. Add one separately labelled future phase-flip incidence. Preserve every original node and edge.',
    'new_nodes': add_nodes, 'new_edges': [{'source': a, 'target': b, 'scope': 'future-A3-only' if (a, b) == future_edge else 'current107'} for a, b in add_edges],
    'refined_AND_groups': groups,
    'future_consumer_correction': {'edge': list(future_edge), 'meaning': 'Distinct R2 isometric pullback needed for future adjoint reversal; not a prerequisite of current107 contraction.', 'consumer_still_red': True},
    'acyclicity_or_topology_admission': 'Pending separate reviewer; creator does not validate',
    'mathematical_statement_change': False, 'new_public_binders': [], 'new_Lean_credit': False})
v2 = put('source-proof-graph-delta107.v2.native.json', {
    'kind': 'effective prospective graph107 v2 proposal', 'base_graph': ref(original), 'overlay': overlay,
    'nodes': [{'id': n, 'kind': 'unchanged-original107'} for n in base_nodes] + add_nodes,
    'edges': [{'source': a, 'target': b, 'scope': 'unchanged-original107'} for a, b in base_edges] + [{'source': a, 'target': b, 'scope': 'future-A3-only' if (a, b) == future_edge else 'current107'} for a, b in add_edges],
    'AND_groups': groups, 'counts': {'nodes': len(base_nodes) + len(add_nodes), 'edges': len(base_edges) + len(add_edges)},
    'original_nodes_edges_all_retained': True, 'future_A3_remains_unproved': True,
    'no_source_binder_or_recommendation_change': True, 'independent_topology_admission': False})
cov = read(BASE / 'source-coverage107.native.json')
coverage = put('source-coverage107.v2-overlay.native.json', {
    'original_coverage': ref(BASE / 'source-coverage107.native.json'), 'v2_graph_proposal': v2,
    'all21_source_regions': cov['all21_regions_rehashed'],
    'source_disposition_change': 'None: same source boundary and same theorem recommendation. Only suppressed analytic support dependencies are exposed.',
    'added_node_dispositions': [{'id': x['id'], 'disposition': 'required current107 analytic support, no new proof credit', 'source_region': 'A3-boundary; weight-matching-and-invariance density sentence'} for x in add_nodes],
    'phase_flip_future_disposition': 'PHASE-FLIP106→L2A3 supplies R2 only for future density/adjoint consumer. It is not counted as a new107 theorem or a premise needed by contraction.',
    'construction_identification_order': ['L2-PRODUCT107', 'L2-CONSTRUCT107 independently of expectation L2', 'PRODUCT-L1-FUBINI107 proves expectation L1 only', 'L2-IDENTIFY107 set-integral uniqueness', 'L2-LIFT107 includes expectation L2 conclusion'],
    'same_witness_unchanged': True, 'MemLp_not_Borel_preserved': True,
    'independent_topology_status': 'pending proposal review', 'compiled107_coverage': False})
inputs = [ref(original), ref(decision), ref(BASE / 'recommendation107.native.json'), ref(BASE / 'source-coverage107.native.json'), ref(BASE / 'closed-RAW-preread107.native.json'), ref(BASE / 'retrieval107.native.json')]
inputs += [a['file'] for a in apis]
inputs = list({x['path']: x for x in inputs}.values())
archives = []
for p in sorted(OUT.iterdir()):
    if p.is_file() and not p.name.endswith('.gz'):
        a = p.with_name(p.name + '.raw.gz')
        assert not a.exists()
        a.write_bytes(gzip.compress(p.read_bytes(), mtime=0))
        assert gzip.decompress(a.read_bytes()) == p.read_bytes()
        archives.append({'raw': ref(p), 'archive': ref(a)})
closure = put('closed-RAW-graph-expansion107.native.json', {
    'proposal': overlay, 'v2_graph': v2, 'coverage': coverage, 'api_bindings': api_receipt,
    'selected_inputs': inputs, 'owned_artifacts': [ref(p) for p in sorted(OUT.iterdir()) if p.is_file()],
    'raw_archives': archives, 'original107_files_untouched': True, 'self_hash_omitted': True,
    'creator_self_admission': False, 'no_source_or_header_or_Lean_change': True})
print(json.dumps({'proposal': overlay, 'v2_graph': v2, 'coverage': coverage, 'closure': closure}, indent=2))
