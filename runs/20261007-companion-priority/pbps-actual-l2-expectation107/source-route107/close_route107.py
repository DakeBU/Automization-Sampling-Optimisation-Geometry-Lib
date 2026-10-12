from pathlib import Path
import gzip
import hashlib
import json

ROOT = Path('E:/Samplinglib')
RUN = ROOT / 'runs/20261007-companion-priority/pbps-actual-l2-expectation107'
OUT = RUN / 'source-route107'
SRC = ROOT / 'runs/20261007-companion-priority/pbps-actual-bounded-gibbs-duality106/next-primary107'
PRE = ROOT / 'runs/20261007-companion-priority/pbps-actual-l2-expectation-preread107'


def ref(p):
    b = p.read_bytes()
    return {'path': p.relative_to(ROOT).as_posix(), 'raw_sha256': hashlib.sha256(b).hexdigest(), 'bytes': len(b)}


def load(p):
    return json.loads(p.read_text(encoding='utf8'))


def put(name, x):
    p = OUT / name
    assert not p.exists(), p
    p.write_bytes((json.dumps(x, ensure_ascii=False, indent=2) + '\n').encode())
    return ref(p)


prod = ROOT / 'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualL2Expectation.lean'
assert ref(prod)['raw_sha256'] == '4c35e0b71362bec3563e3d07c9f122d6b7ca4cae604f7a88aad397d2a028f4d6'
s = prod.read_text(encoding='utf8')
assert len(s.splitlines()) == 345
assert 'ae_ae_of_ae_prod' not in s
header = PRE / 'Header107.lean'
h = header.read_text(encoding='utf8')
start = '    {E : Type*}'
assert s[s.index(start):s.index('\nset_option maxHeartbeats')].strip() == h[h.index(start):h.index('#check candidate')].strip()
graph_path = SRC / 'graph-expansion107/source-proof-graph-delta107.v2.native.json'
graph = load(graph_path)
assert graph['counts'] == {'nodes': 85, 'edges': 160}
assert not any(e['source'] == 'L2-IDENTIFY107' and e['target'] == 'AE-REP107' for e in graph['edges'])
original_group = next(x for x in graph['AND_groups'] if x['target'] == 'AE-REP107')
assert original_group['parents'] == ['INV100', 'MeasureTheory.ae_ae_of_ae_prod']
math = RUN / 'independent-whole-math107/whole-math-decision107.native.json'
assert load(math)['decision'] == 'ACCEPT_WHOLE_MATHEMATICS_AND_EXACT_SEALED_KERNEL'
lines = prod.read_bytes().splitlines(keepends=True)


def span(lo, hi, meaning):
    b = b''.join(lines[lo - 1:hi])
    return {'line_start': lo, 'line_end': hi, 'raw_sha256': hashlib.sha256(b).hexdigest(), 'meaning': meaning}


spans = [
    span(183, 215, 'hpair_core constructs one A=B.adjoint composed C, with norm bound and pairing, before all L2 f,g.'),
    span(216, 227, 'haverage_core quantifies one A before every G and hG; its universal conclusion is the key route invariant.'),
    span(228, 235, 'Actual pullback L2 implies product L1; both expectation and A[G] are L1 before set-integral uniqueness.'),
    span(236, 268, 'heq: chosen representative of A[G] equals literal clock expectation a.e., using indicator pairing and signed Fubini.'),
    span(269, 272, 'MemLp.ae_eq transports membership; Lp.ext and coeFn_toLp identify the actual expectation L2 class with A[G].'),
    span(311, 319, 'Instantiate universal haverage_core at same actual Z and endpoint stationarity from106; choose family before observables.'),
    span(332, 341, 'For every G,hG export section AE-integrability, actual hOp and class equality; derive square contraction.')
]
apis = []
specs = [
    ('MeasureTheory.MemLp.ae_eq', 'MeasureTheory/Function/LpSeminorm/Basic.lean', 'theorem MemLp.ae_eq ', 'direct code269'),
    ('MeasureTheory.MemLp.coeFn_toLp', 'MeasureTheory/Function/LpSpace/Basic.lean', 'theorem coeFn_toLp ', 'direct code242,272'),
    ('MeasureTheory.Lp.ext', 'MeasureTheory/Function/LpSpace/Basic.lean', 'theorem ext {f g : Lp', 'direct code271'),
    ('MeasureTheory.MemLp.toLp_congr', 'MeasureTheory/Function/LpSpace/Basic.lean', 'theorem toLp_congr ', 'source-route explanation of same input class; not claimed directly invoked'),
]
for name, tail, needle, role in specs:
    p = ROOT / '.lake/packages/mathlib/Mathlib' / tail
    ls = p.read_text(encoding='utf8').splitlines()
    i = next(i for i, l in enumerate(ls) if needle in l)
    apis.append({'declaration': name, 'file': ref(p), 'line_start': i + 1,
                 'signature_excerpt': '\n'.join(ls[i:i + 5]), 'role': role})

mechanism = [
    'The actual haverage_core chooses A before G,hG. For every input representative it proves A([G])=[opG], with output MemLp proved by heq, not supplied.',
    'If G and H represent the same L2 class, [G]=[H]. Applying the same function A gives A([G])=A([H]). Universal identification then gives [opG]=[opH]. Hence their expectation functions agree nu-a.e. through their toLp representative identities.',
    'This implication uses universal class identification already proved at216-272 and exported for the same actual Z at311-341. No additional separately named cross-representative theorem or explicit ae_ae_of_ae_prod call is present; the route is a structural consequence of the compiled universal interface.',
    'The existing measure-preserving endpoint and Fubini ingredients remain transitive dependencies of L2-IDENTIFY107. The selected alternative does not remove or bypass them; it avoids a second iterated-a.e. transport proof specifically for representative independence.',
    'No pointwise agreement for arbitrary L2 representatives, common null set over parameters or observables, or pointwise Borel status of arbitrary MemLp G is asserted.'
]
proposal = put('quotient-identification107.proposal.native.json', {
    'kind': 'minimal append-only compiled-route source graph overlay proposal',
    'creator': '/root/source_final96', 'primary_first': ref(OUT / 'primary-first-route107.native.json'),
    'base_graph': ref(graph_path), 'base_independent_admission': ref(SRC / 'independent-topology107/v2-admission/admission107.v2.native.json'),
    'production': ref(prod), 'original_header': ref(header), 'whole_math_evidence': ref(math),
    'new_nodes': [], 'new_edges': [['L2-IDENTIFY107', 'AE-REP107']], 'removed_nodes': [], 'removed_edges': [],
    'refined_node_meaning': {'id': 'AE-REP107', 'meaning': 'Actual expectation depends only on the input real L2 equivalence class; equal input classes give equal output classes and hence nu-a.e. equal expectations. Mechanisms are the explicit OR alternatives below.', 'old_mechanism_preserved_in': 'planned-iterated-ae-transport107'},
    'AND_route_alternatives': {'AE-REP107': [
        {'route_id': 'planned-iterated-ae-transport107', 'status': 'retained original planned route; not asserted to be directly executed by current implementation', 'parents': original_group['parents'], 'mechanism': original_group['mechanism']},
        {'route_id': 'universal-quotient-identification107', 'status': 'selected compiled route proposal; independent admission pending', 'parents': ['L2-IDENTIFY107'], 'mechanism': mechanism, 'evidence': spans[1:5], 'ordinary_quotient_support': apis}
    ]},
    'OR_semantics': 'Either complete AND route supplies AE-REP107. Do not require the union of both route parent sets as one AND group. Retain the original edges for the unselected alternative.',
    'counts_if_admitted': {'nodes': 85, 'edges': 161, 'source_regions': 21},
    'unchanged_groups': 'All other v2 groups, including construction before identification, L1/Fubini support, final L2-LIFT107 aggregate, and future PHASE-FLIP106→L2A3 remain unchanged.',
    'statement_repair_required': False, 'source_hypothesis_change': False, 'public_header_change': False,
    'classification': 'Implementation-route/topology coverage refinement. A graph overlay is required for truthful selected-route evidence; no mathematical theorem repair.',
    'no_topology_self_admission': True, 'no_final_source_verdict': True, 'no_new_Lean_credit': True})
first = load(OUT / 'primary-first-route107.native.json')
coverage = put('source-route-coverage107.proposal.native.json', {
    'primary': first['primary'], 'all21_source_regions': first['source_regions'],
    'base_v2_coverage': ref(SRC / 'graph-expansion107/source-coverage107.v2-overlay.native.json'),
    'overlay_proposal': proposal, 'production': ref(prod), 'selected_spans': spans,
    'exact_changed_dispositions': [
        {'node': 'AE-REP107', 'before': 'Representative independence described only by explicit iterated-a.e. transport.', 'after': 'Same mathematical node, OR between retained transport route and selected universal quotient-identification consequence.'},
        {'node': 'L2-IDENTIFY107', 'before': 'Supplies representative identity and expectation MemLp to L2-LIFT107.', 'after': 'Same proved identity additionally supplies AE-REP107 through universal quantification over arbitrary MemLp G with one operator fixed first.'},
        {'node': 'MeasureTheory.ae_ae_of_ae_prod', 'before': 'Planned explicit AE-REP107 support.', 'after': 'Retained support of unselected alternative; no direct call claimed for current whole module.'}
    ],
    'source_region_changes': 'No primary bytes/ranges or source obligations change. A3-boundary and final density sentence still require well-defined L2 classes but do not mandate this specific route. All other19 region dispositions unchanged; both affected anchors retain their original scope.',
    'future_boundaries': 'No A.3 adjoint identity, strong continuity, restart, Markov/semigroup, costs, full-paper or reader/browser admission.',
    'coverage_scope': 'Only the changed route incidence and adjacent exact implementation spans; final exhaustive module/source/exposition coverage will follow a fresh canonical reviewer packet.',
    'source_graph_creator_not_independent_admitter': True})
run = put('source-route-run107.native.json', {
    'creator': '/root/source_final96', 'proposal': proposal, 'coverage': coverage,
    'primary_first': ref(OUT / 'primary-first-route107.native.json'),
    'current_header_statement_matches_production': True, 'direct_ae_ae_of_ae_prod_call_found': False,
    'raw_production_lines': 345, 'mathematical_repair': False,
    'topology_admission': 'pending separate reviewer', 'no_shared_mutation': True})
inputs = [prod, header, graph_path, math, SRC / 'graph-expansion107/source-coverage107.v2-overlay.native.json', SRC / 'independent-topology107/v2-admission/admission107.v2.native.json', ROOT / first['primary']['path']]
inputs += [ROOT / x['file']['path'] for x in apis]
inputs = list({str(p): p for p in inputs}.values())
archives = []
for p in sorted(OUT.iterdir()):
    if p.is_file() and not p.name.endswith('.gz'):
        a = p.with_name(p.name + '.raw.gz')
        assert not a.exists()
        a.write_bytes(gzip.compress(p.read_bytes(), mtime=0))
        assert gzip.decompress(a.read_bytes()) == p.read_bytes()
        archives.append({'raw': ref(p), 'archive': ref(a)})
closure = put('closed-RAW-source-route107.native.json', {
    'proposal': proposal, 'coverage': coverage, 'run': run, 'selected_inputs': [ref(p) for p in inputs],
    'owned_artifacts': [ref(p) for p in sorted(OUT.iterdir()) if p.is_file()], 'raw_archives': archives,
    'no_full_primary_archive': True, 'self_hash_omitted': True,
    'no_topology_self_admission': True, 'no_final_source_acceptance': True})
print(json.dumps({'proposal': proposal, 'coverage': coverage, 'run': run, 'closure': closure}, indent=2))
