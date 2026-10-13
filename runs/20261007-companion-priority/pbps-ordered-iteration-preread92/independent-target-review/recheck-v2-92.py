import hashlib
import json
import pathlib
import subprocess
from datetime import datetime, timezone

ROOT = pathlib.Path('E:/Samplinglib')
BASE = ROOT / 'runs/20261007-companion-priority/pbps-ordered-iteration-preread92'
OWN = BASE / 'independent-target-review'
PRIMARY = BASE / 'primary-first'

def read(path):
    return json.loads(path.read_text(encoding='utf-8'))

def digest(data):
    return hashlib.sha256(data).hexdigest()

def bind(path):
    data = path.read_bytes()
    return dict(path=path.as_posix(), raw_sha256=digest(data), bytes=len(data))

def check(row):
    p = pathlib.Path(row['path'])
    if not p.is_absolute():
        p = ROOT / p
    actual = bind(p)
    assert actual['raw_sha256'] == row['raw_sha256'], (str(p), 'hash mismatch')
    assert actual['bytes'] == row['bytes'], (str(p), 'size mismatch')
    return actual

def write_new(name, value):
    p = OWN / name
    with p.open('x', encoding='utf-8', newline='\n') as out:
        if isinstance(value, str):
            out.write(value)
        else:
            json.dump(value, out, ensure_ascii=False, indent=2)
            out.write('\n')
    return p

manifest_path = PRIMARY / 'candidate-v2-closed-RAW92.native.json'
assert bind(manifest_path)['raw_sha256'] == '29baefbf2af4278320cfab1086a322271fd0b988d60cd66ce1fcd64cb6cd971a'
manifest = read(manifest_path)
checked = {}
for m in [manifest, read(OWN / 'closed-RAW92.native.json'), read(PRIMARY / 'closed-RAW92.native.json'), read(PRIMARY / 'candidate-graph-closed-RAW92.native.json')]:
    for row in m.get('inputs', []) + m.get('outputs', []):
        actual = check(row)
        checked[actual['path']] = actual
checked[manifest_path.as_posix()] = bind(manifest_path)

rec = read(PRIMARY / 'recommendation92.v2.native.json')
graph = read(PRIMARY / 'candidate-source-proof-graph92.v2.native.json')
coverage = read(PRIMARY / 'candidate-source-coverage92.v2.native.json')
assert digest(rec['statement'].encode()) == rec['statement_text_sha256']
assert rec['statement'] in (PRIMARY / 'recommendation92.v2.md').read_text(encoding='utf-8')
source = pathlib.Path(rec['primary']['path']).read_bytes()
spans = []
for row in coverage['coverage']:
    span = row['source_region']
    data = source[span['byte_start']:span['byte_end_exclusive']]
    assert digest(data) == span['raw_sha256'], row['id']
    assert len(data) == span['bytes'], row['id']
    spans.append(row['id'])
for regions in [graph['source_regions'], coverage['source_regions']]:
    for key, span in regions.items():
        data = source[span['byte_start']:span['byte_end_exclusive']]
        assert digest(data) == span['raw_sha256'], key

nodes = {node['id']: node for node in graph['nodes']}
assert len(nodes) == len(graph['nodes']) == 29
assert len(graph['edges']) == 57
adj = {n: [] for n in nodes}
indeg = {n: 0 for n in nodes}
for e in graph['edges']:
    assert e['from'] in nodes and e['to'] in nodes
    adj[e['from']].append(e['to'])
    indeg[e['to']] += 1
queue = [n for n, d in indeg.items() if d == 0]
order = []
while queue:
    n = queue.pop()
    order.append(n)
    for nxt in adj[n]:
        indeg[nxt] -= 1
        if indeg[nxt] == 0:
            queue.append(nxt)
assert len(order) == 29
old_graph = read(PRIMARY / 'candidate-source-proof-graph92.native.json')
old_edges = {(e['from'], e['to']) for e in old_graph['edges']}
new_edges = {(e['from'], e['to']) for e in graph['edges']}
assert new_edges - old_edges == {('I92', 'M92')}
assert old_edges <= new_edges
assert graph['AND_routes'] == old_graph['AND_routes']
assert graph['OR_routes'] == old_graph['OR_routes']
assert len(spans) == 46
head = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()

findings = [
    {'id': 'P92-1', 'decision': 'resolved', 'finding': 'The statement defines Omega=R^N, the literal infinite product Exp(1) measure, clipped NNReal coordinate clocks with zero-based indexing, and the actual finite stopped recursion. Strictly positive clocks are derived almost surely; no probability, independence, density or good-input provider is added.'},
    {'id': 'P92-2/R92-COUNT', 'decision': 'resolved', 'finding': 'The event is literally the live first-n record prefix with 0<T1<...<Tn<T and E0=Omega. The recommendation, E92, C92-25 and SURV92-to-TERM92 now qualify the counting gloss almost surely and do not equate raw zero-clock input counts pointwise. The original counterexample remains valid and is reproduced accurately in v2.'},
    {'id': 'P92-3', 'decision': 'resolved', 'finding': 'Reflection is expanded with R0=I. Rec is the Borel Sum of NNReal x Phase and Unit, Hist_n is the full Fin(n+1) product, prescribed histories live on the strict simplex subtype, and q is ofReal of the finite nonnegative pre-bounce-rate/segment-survival product. No hidden off-simplex extension is needed.'},
    {'id': 'P92-4', 'decision': 'resolved', 'finding': 'Joint Borel K and q are asserted on R^d x R^d x Phase x Delta_n(T) for fixed V, eta, n, T. No regularity in V or eta or extra parameter-integral conclusion is asserted. The six original analytic assumptions are preserved.'},
    {'id': 'R92-REC-MEAS', 'decision': 'resolved', 'finding': 'I92-to-M92 is the sole new graph edge; it explicitly supplies the actual clock/threshold/record recurrence whose measurability is claimed. The graph stays acyclic.'},
    {'id': 'R92-RESIDUAL-COVERAGE', 'decision': 'resolved', 'finding': 'C92-43 assigns the residual beta-Lipschitz estimate to ENERGY92; C92-44 explicitly excludes full-force recombination as generator background. Both agree with reread fixed-primary S3.SS2.p4.'},
    {'id': 'R92-BOUNCE-COVERAGE', 'decision': 'resolved', 'finding': 'C92-45 explicitly excludes involution from the prefix dependency route; C92-46 assigns zero-normal zero-rate to O92. Both agree with reread fixed-primary A1.SS1.p1. Neither imports reflection continuity.'}
]
decision = {
    'schema_version': 1,
    'reviewer': '/root/independent_math91',
    'utc': datetime.now(timezone.utc).isoformat(),
    'checked_workspace_HEAD': head,
    'decision': 'ACCEPT_TARGET_AND_BOUNDED_SOURCE_CANDIDATE_V2',
    'scope': 'Independent successor recheck of mathematical target and primary-derived candidate topology/coverage only. No exact Lean Statement Seal, implementation, theorem proof, source-to-Lean equivalence or canonical transition is accepted.',
    'inputs': list(checked.values()),
    'immutable_originals': 'All referenced original recommendation/graph/coverage manifests and prior independent review bytes were rehashed against their closed native manifests and remain unchanged. This script creates new owned outputs only.',
    'repairs': findings,
    'unchanged_mathematical_checks': [
        'n=0 uses the singleton mass-one simplex and deterministic initial history even at T=0; n>0,T=0 has empty strict simplex/event.',
        'The finite prefix law permits arbitrary Borel ENNReal tests on the entire ambient tagged history, including infinite values and null-event restriction, with no integrability or positive-event-probability binder.',
        'Each factor is the pre-bounce rate times survival over that elapsed segment. There is no final survival factor and no factorial in the ordered-simplex density.',
        'Zero hazard, stopped records, infinite next wait, rank-zero phase space and raw zero/negative clocks remain totalized consistently. The zero-clock count counterexample is retained, not repaired away.',
        'Preferred absolute-coordinate induction and alternative relative-coordinate transport remain OR routes. Final survival, path/hazard identification, count exhaustiveness and bounded signed assembly remain downstream.',
        'Existing actual-input nonaccumulation78/coverage79 are preserved as historical substrates, not reopened or new prefix hypotheses. Cap/simplex versus mass/Tonelli convergence routes remain alternatives.',
        'The full A7 consumer keeps complete path-functional dependence through PATH92. Path-space sigma algebra, endpoint equivalences and full count/path construction remain future obligations.'
    ],
    'mechanical_checks': {
        'all_manifest_hashes_and_sizes_pass': True,
        'checked_unique_file_count': len(checked),
        'statement_hash_and_markdown_exact_match': True,
        'coverage_dispositions_rehashed': len(spans),
        'all_graph_and_coverage_region_hashes_pass': True,
        'unique_graph_nodes': 29,
        'graph_edges': 57,
        'acyclic_and_all_edge_endpoints_valid': True,
        'old_edges_preserved': True,
        'only_added_edge': ['I92', 'M92'],
        'AND_and_OR_routes_unchanged': True
    },
    'remaining_issues_within_candidate_scope': [],
    'acceptance_boundary': 'Suitable mathematical target and source candidate to inform subsequent exact Statement Seal drafting; any Lean header must still be independently checked against this target. No theorem-completion or whole-A7 credit.',
    'canonical_state_changed': False,
    'production_Lean_changed': False
}
report = write_new('v2-recheck92.native.json', decision)
note = write_new('v2-recheck92.md', '''# Independent target/source-candidate v2 recheck

Accepted within the bounded target and primary-derived source-candidate scope. All seven requested precision/coverage repairs are resolved. The literal product clock law, strict first-n prefix, full tagged histories, finite ENNReal weight and fixed-parameter joint Borel assertion are now explicit. The zero-clock counterexample is preserved with the correct almost-sure counting boundary.

The graph has 29 nodes and 57 edges, remains acyclic, and adds only I92 -> M92. All 46 source dispositions rehash against the fixed primary. The four new dispositions correctly handle residual Lipschitz, force recombination, involution and zero-normal rate. Original native artifacts and independent reviews are unchanged. Preferred and alternative proof routes, existing78/79 substrates and the whole-path A7 consumer remain properly separated.

This accepts no Lean Statement Seal, implementation, proof, canonical transition or full A7 completion. Exact Lean statement review remains a later obligation. See v2-recheck92.native.json for input hashes and findings.
''')
receipt = write_new('v2-recheck92.receipt.json', {
    'command': "C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe -X utf8 runs/20261007-companion-priority/pbps-ordered-iteration-preread92/independent-target-review/recheck-v2-92.py",
    'cwd': ROOT.as_posix(), 'exit_status': 'completed assertions and output generation',
    'checked_HEAD': head, 'report': bind(report), 'script': bind(pathlib.Path(__file__))
})
closed = write_new('v2-recheck-closed-RAW92.native.json', {
    'schema_version': 1, 'closed': True, 'reviewer': '/root/independent_math91',
    'utc': datetime.now(timezone.utc).isoformat(),
    'inputs': list(checked.values()),
    'outputs': [bind(p) for p in [pathlib.Path(__file__), report, note, receipt]],
    'closure': 'New owned v2 review outputs only; predecessor bytes retained. Manifest excludes its own bytes. Acceptance limited to target and source candidate, not a Lean seal or theorem.'
})
print(json.dumps({'decision': decision['decision'], 'report': bind(report), 'closed_manifest': bind(closed), 'checks': decision['mechanical_checks']}, indent=2))
