import copy
import gzip
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
BASE = ROOT / 'runs/20261007-companion-priority/pbps-actual-l2-flip-duality108/next-primary109'
inputs = {}
OLD = 'MeasureTheory.ae_ae_of_ae_prod'
NEW = 'MeasureTheory.Measure.ae_ae_of_ae_prod'
INNER = 'MeasureTheory.L2.integrable_inner'
IND = 'MeasureTheory.Integrable.indicator'
TARGET = 'MOMENTUM-L1-FUBINI109'


def sha(b):
    return hashlib.sha256(b).hexdigest()


def bind(p):
    b = p.read_bytes()
    x = {'path': p.relative_to(ROOT).as_posix(), 'raw_sha256': sha(b), 'bytes': len(b)}
    inputs[x['path']] = x
    return x


def read(p):
    bind(p)
    return json.loads(p.read_text(encoding='utf-8'))


def emit(name, x):
    p = OUT / name
    assert not p.exists(), p
    p.write_bytes((json.dumps(x, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
    return bind(p)


def normalize(x):
    if isinstance(x, str):
        return x.replace(OLD, NEW)
    if isinstance(x, list):
        return [normalize(v) for v in x]
    if isinstance(x, dict):
        return {normalize(k): normalize(v) for k, v in x.items()}
    return x


def span(p, a, b):
    text = b''.join(p.read_bytes().splitlines(keepends=True)[a - 1:b])
    return {'file': bind(p), 'start': a, 'end': b, 'raw_sha256': sha(text), 'text': text.decode('utf-8')}


freeze = read(OUT / 'primary-first109.native.json')
primary = ROOT / freeze['primary']['path']
assert bind(primary) == freeze['primary']
raw = primary.read_bytes()
for r in freeze['regions']:
    assert sha(raw[r['byte_start']:r['byte_end_exclusive']]) == r['raw_sha256']
original = read(BASE / 'source-proof-graph-delta109.native.json')
retrieval = read(BASE / 'retrieval109.native.json')
coverage = read(BASE / 'source-coverage109.native.json')
bind(BASE / 'closed-RAW-manifest109.native.json')
bind(BASE / 'independent-topology109/decision109.native.json')
header = bind(ROOT / 'runs/20261007-companion-priority/pbps-actual-position-l2-preread109/Header109.lean')
assert header['raw_sha256'] == '927043eaaace6083ec00c750037e4c69f21173595b85646bb9a5a1b63795e31b'
production = ROOT / 'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPositionL2Averaging.lean'
prod_binding = bind(production)
assert prod_binding['raw_sha256'] == '21c6b4e95b729b41f555eecf6a42185ab2f63bff7bcab3f6dc2ab82da171e85e'
mathlib = ROOT / '.lake/packages/mathlib/Mathlib'
api = emit('pinned-api-adapter109.native.json', {
    'kind': 'exact pinned namespace and selected-route API evidence',
    'namespace_correction': {'old': OLD, 'correct': NEW, 'namespace_opening': span(mathlib / 'MeasureTheory/Measure/Prod.lean', 165, 167), 'declaration': span(mathlib / 'MeasureTheory/Measure/Prod.lean', 430, 438), 'namespace_closure': span(mathlib / 'MeasureTheory/Measure/Prod.lean', 850, 852)},
    'selected_integrability_api': {'id': IND, 'evidence': span(mathlib / 'MeasureTheory/Integral/IntegrableOn.lean', 350, 353)},
    'actual_indicator_pairing_adapter': {'id': 'MeasureTheory.L2.inner_indicatorConstLp_one', 'evidence': span(mathlib / 'MeasureTheory/Function/L2Space.lean', 222, 226), 'scope': 'convenience realization of existing indicatorConstLp/L2 pairing node, not an additional mathematical premise'},
    'production_evidence': [span(production, 236, 284), span(production, 333, 345)],
    'actual_route': 'hG.integrable -> hprod; H equals (fst inverse s).indicator G; hprod.indicator proves H integrable before signed integral_prod. No direct L2.integrable_inner invocation in this local block.',
    'no_claim_about_transitive_library_dependencies': True})

graph = normalize(copy.deepcopy(original))
old_group = next(g for g in graph['new_AND_groups'] if g['target'] == TARGET)
old_group = copy.deepcopy(old_group)
common = [p for p in old_group['parents'] if p != INNER]
selected = common + [IND]
mechanism = 'G in L2 on finite actual product gives G in L1; indicator restriction H=(fst inverse s).indicator G is integrable by Integrable.indicator; signed Fubini then supplies indicator-test Gaussian averaging.'
for n in graph['nodes']:
    if n['id'] == TARGET:
        n['meaning'] = mechanism
        n['route_selection'] = 'finite-L1-indicator-restriction'
for n in graph['new_nodes']:
    if n['id'] == TARGET:
        n['meaning'] = mechanism
        n['route_selection'] = 'finite-L1-indicator-restriction'
leaf = {'id': IND, 'kind': 'pinned-Mathlib-api', 'retrieval': api['path']}
assert IND not in {n['id'] for n in graph['nodes']}
graph['nodes'].append(leaf)
graph['new_nodes'].append(leaf)
for collection in ['edges', 'new_edges']:
    hits = [e for e in graph[collection] if e['source'] == INNER and e['target'] == TARGET]
    assert len(hits) == 1
    hits[0]['route_membership'] = 'unselected-L2-inner-alternative-only'
    hits[0]['not_a_current_direct_call'] = True
    graph[collection].append({'source': IND, 'target': TARGET, 'scope': '109-selected-finite-L1-indicator-route', 'mechanism': mechanism, 'route_membership': 'selected'})
for g in graph['new_AND_groups']:
    if g['target'] == TARGET:
        g['parents'] = selected
        g['mechanism'] = mechanism
        g['selection_authority'] = 'conditional_route_groups109; exact mandatory set is selected alternative, not union'
graph['conditional_route_groups109'] = [{
    'target': TARGET, 'selected': 'finite-L1-indicator-restriction',
    'alternatives': [{'id': 'finite-L1-indicator-restriction', 'AND': selected, 'status': 'implemented route proposed for independent admission'}, {'id': 'L2-inner-product-integrability', 'AND': old_group['parents'], 'status': 'retained source-sufficient prospective alternative; not selected, no direct-call claim'}],
    'supersedes_mandatory_group': old_group, 'not_mandatory_union': True,
    'interpretation': 'Shared incoming edges are common premises; only the selected branch-specific input is mandatory. The preserved L2.integrable_inner edge belongs solely to the other branch.'}]
graph['kind'] = 'unadmitted append-only109 namespace and implementation-route adapter proposal'
graph['adapted_from'] = bind(BASE / 'source-proof-graph-delta109.native.json')
graph['counts'] = {'nodes': len(graph['nodes']), 'edges': len(graph['edges']), 'inherited108_nodes': 107, 'inherited108_edges': 196, 'original109_nodes': 122, 'original109_edges': 246, 'adapter_added_nodes': 1, 'adapter_added_edges': 1}
graph['source_and_witness_boundary_unchanged'] = True
graph['creator_does_not_validate_topology'] = True
assert OLD not in json.dumps(graph, ensure_ascii=False)
assert len({n['id'] for n in graph['nodes']}) == len(graph['nodes'])
assert TARGET not in selected
graph_ref = emit('source-proof-graph109.route-adapted.proposal.json', graph)

retrieval_new = normalize(copy.deepcopy(retrieval))
retrieval_new['kind'] = 'prospective109 retrieval normalization and implementation evidence supplement'
retrieval_new['original_retrieval'] = bind(BASE / 'retrieval109.native.json')
retrieval_new['adapter_evidence'] = api
retrieval_new['selected_route'] = mechanism
retrieval_new['unselected_alternative'] = 'L2.integrable_inner is a valid alternative proof ingredient, preserved historically, not a direct invocation in109.'
retrieval_ref = emit('retrieval109.route-adapted.native.json', retrieval_new)
cov = normalize(copy.deepcopy(coverage))
cov['kind'] = 'append-only source coverage adapter proposal; not a final compiled source verdict'
cov['graph'] = graph_ref
cov['original_coverage'] = bind(BASE / 'source-coverage109.native.json')
cov['node_dispositions'].append({'id': IND, 'status': 'exact pinned API used in selected local indicator-integrability route'})
for e in cov['edge_dispositions']:
    if e['source'] == INNER and e['target'] == TARGET:
        e['status'] = 'retained unselected alternative only; not mandatory or a direct implementation call'
cov['edge_dispositions'].append({'source': IND, 'target': TARGET, 'status': 'selected implementation-route proof ingredient, no new source assumption'})
cov['changed_selected_slice'] = {'source_region': 'gaussian-momentum-averaging', 'node': TARGET, 'production_spans': [[240, 259], [261, 284]], 'source_meaning_unchanged': True, 'new_premises': [], 'namespace_projection_span': [340, 342]}
cov['same_witness_scope_unchanged'] = 'One actual108 globalZ/A/J retained; route only establishes already-required Gaussian averaging integrability internally.'
cov['all24_source_regions_unchanged'] = True
cov['selected_proof_obligation'] = mechanism
cov_ref = emit('source-coverage109.route-adapter.native.json', cov)

changed_paths = []


def diff(a, b, path=''):
    if type(a) is not type(b):
        changed_paths.append({'path': path, 'before': a, 'after': b})
    elif isinstance(a, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b:
                changed_paths.append({'path': path + '/' + k, 'before': a.get(k), 'after': b.get(k)})
            else:
                diff(a[k], b[k], path + '/' + k)
    elif isinstance(a, list):
        for i in range(max(len(a), len(b))):
            if i >= len(a) or i >= len(b):
                changed_paths.append({'path': path + '/' + str(i), 'before': a[i] if i < len(a) else None, 'after': b[i] if i < len(b) else None})
            else:
                diff(a[i], b[i], path + '/' + str(i))
    elif a != b:
        changed_paths.append({'path': path, 'before': a, 'after': b})


diff(original, graph)
proposal = emit('route-adapter-proposal109.native.json', {
    'kind': 'source creator proposal requiring separate independent review', 'reviewer_author': '/root/source_final96',
    'primary_first': bind(OUT / 'primary-first109.native.json'), 'original_graph': bind(BASE / 'source-proof-graph-delta109.native.json'), 'proposed_graph': graph_ref,
    'original_retrieval': bind(BASE / 'retrieval109.native.json'), 'proposed_retrieval': retrieval_ref,
    'coverage_overlay': cov_ref, 'pinned_API_evidence': api, 'production': prod_binding, 'sealed_header_unchanged': header,
    'diagnosis': ['Original retrieval/graph namespace omitted Measure; normalize all effectivegraph and retrieval identity occurrences to exact pinned MeasureTheory.Measure.ae_ae_of_ae_prod.', 'Actual indicator integrability is obtained by finite-measure L2-to-L1 and measurable indicator restriction. The old L2 inner-product route is sufficient but not implemented directly.'],
    'mathematical_statement_repair_required': False, 'source_hypothesis_change': False, 'production_change': False,
    'topology_counts': graph['counts'], 'ordinary_graph_policy': 'All original ordinary edges retained, modulo namespace normalization. Add one Integrable.indicator leaf/edge; mark the old inner-product edge as alternative-only. The selected AND excludes it, and conditional OR semantics forbids a mandatory union.',
    'exact_graph_diff': changed_paths,
    'unchanged_boundaries': ['six source assumptions', '37 actual literals', 'same globalZ/A/J', 'Gaussian actual integral representative', 'all24 source slices', 'position self-adjoint contraction only; Markov/semigroup/A2 still red'],
    'no_final_source_verdict_or_topology_self_admission': True})

archive_dir = OUT / 'raw-archives'
archive_dir.mkdir(exist_ok=False)
artifacts = []
archives = []
for p in sorted(OUT.iterdir()):
    if not p.is_file():
        continue
    original_binding = bind(p)
    dst = archive_dir / (p.name + '.gz')
    dst.write_bytes(gzip.compress(p.read_bytes(), mtime=0))
    assert gzip.decompress(dst.read_bytes()) == p.read_bytes()
    artifacts.append(original_binding)
    archives.append({'original': original_binding, 'archive': {'path': dst.relative_to(ROOT).as_posix(), 'raw_sha256': sha(dst.read_bytes()), 'bytes': dst.stat().st_size}})
closure = emit('closed-RAW-route-adapter109.native.json', {'kind': 'immutable source route adapter proposal closure109', 'proposal': proposal, 'inputs': list(inputs.values()), 'artifacts': artifacts, 'archives': archives, 'all_roundtrips_pass': True, 'no_full_primary_archive': True, 'independent_admission_pending': True})
print(json.dumps({'proposal': proposal, 'graph': graph_ref, 'coverage': cov_ref, 'retrieval': retrieval_ref, 'closure': closure, 'counts': graph['counts']}, indent=2))
