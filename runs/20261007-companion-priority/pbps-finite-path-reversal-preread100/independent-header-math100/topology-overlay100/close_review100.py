import hashlib, json
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path('E:/Samplinglib')
OWN = Path(__file__).resolve().parent
PRE = 'runs/20261007-companion-priority/pbps-finite-path-reversal-preread100/'
OLD = PRE + 'independent-header-math100/'
SRC = 'runs/20261007-companion-priority/pbps-actual-prescribed-state-reversal99/next-primary100/'

def read(p):
    return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))

def raw(p):
    b = (ROOT / p).read_bytes()
    return dict(path=p, raw_sha256=hashlib.sha256(b).hexdigest(), bytes=len(b))

checked = {}
def check(r):
    actual = raw(r['path'])
    assert actual['raw_sha256'] == r['raw_sha256'], (r, actual)
    if 'bytes' in r:
        assert actual['bytes'] == r['bytes'], (r, actual)
    checked[r['path']] = actual
    return actual

def close_inputs(p, expected=None):
    r = raw(p)
    if expected:
        assert r['raw_sha256'] == expected
    checked[p] = r
    doc = read(p)
    for k in ['inputs', 'outputs', 'files']:
        for item in doc.get(k, []):
            check(item)
    return doc

close_inputs(OLD + 'closed-RAW-original100.native.json', '9bf92e608fde7c1cae5561787ef7a87c7b04e5181edfbaa1efba7a5068bf4767')
close_inputs(OLD + 'api-name-erratum100/closed-RAW-erratum100.native.json')
close_inputs(SRC + 'graph-refinement100/closed-RAW-overlay100.native.json', 'b0584e155afbab5d4c247d8cc7d22bcc2e2e397c8e9502acd0bd91c1eb68a2f3')
overlay_path = SRC + 'graph-refinement100/source-graph-overlay100.native.json'
overlay = read(overlay_path)
assert raw(overlay_path)['raw_sha256'] == '10e3a03424bb0fcf0df371bb23986a2d58250c5fc9456887025c238b64fbff33'
check(overlay['base'])
check(overlay['unchanged_header'])
delta = read(overlay['base']['path'])
for k in ['inherits_exact', 'unchanged_inventory', 'unchanged_coverage99']:
    check(delta[k])
graph = read(delta['inherits_exact']['path'])
assert len(overlay['changes']) == 3
rho, gap, arc = overlay['changes']
assert rho['id'] == 'RHO99' and rho['not_implied_by_states_alone']
assert gap['target'] == 'GAPS99-adapter' and gap['sources'] == ['D99', 'RHO99']
assert {(e['from'],e['to']) for e in gap['edges']} == {('D99','GAPS99-adapter'),('RHO99','GAPS99-adapter')}
assert arc['id'] == 'OPENARC100' and not arc['endpoint_derivation']['new_parent_or_premise']
check(rho['producer'])
check(arc['existing_path_producer'])
assert len(delta['source_coverage_delta']) == 21
nodes = {n['id'] for n in graph['nodes']} | set(delta['new_required_slice']) | {'RHO99'}
edges = {(e['from'],e['to']) for e in graph['edges']} | {tuple(e) for e in delta['delta_edges']} | {(e['from'],e['to']) for e in gap['edges']}
assert all(a in nodes and b in nodes for a,b in edges)
todo = set(nodes)
order = []
while todo:
    ready = sorted(n for n in todo if not any(b == n and a in todo for a,b in edges))
    assert ready, 'cycle in inherited graph plus delta and overlay'
    order += ready
    todo.difference_update(ready)

decision = {
  'kind': 'independent-base-plus-overlay-topology-admission100',
  'utc': datetime.now(timezone.utc).isoformat(),
  'reviewer': '/root/exact_verifier96',
  'decision': 'ACCEPT_BASE_PLUS_NARROW_OVERLAY_TOPOLOGY_AND_COVERAGE',
  'review_mode': 'Nonblind independent validation of source_final96 graph. Original mathematical reconstruction preceded reading the source100 delta; overlay review knowingly addresses the two recorded findings. No claim of a second blind reconstruction.',
  'overlay': raw(overlay_path),
  'base': raw(overlay['base']['path']),
  'inherited_graph': raw(delta['inherits_exact']['path']),
  'header': raw(PRE + 'Header100.lean'),
  'original_negative': raw(OLD + 'source-topology-original100.native.json'),
  'original_header_acceptance': raw(OLD + 'header-math-decision100.native.json'),
  'api_name_erratum': raw(OLD + 'api-name-erratum100/erratum100.native.json'),
  'findings_closed': [
    {'id':'GAPS100-inputs', 'status':'resolved', 'reason':'RHO99 is the coordinate projection of the existing public actual99 theorem, sharing its single existential rho with STATES99. D99 and RHO99 jointly supply the locally derived grid-gap adapter. This neither invokes the private99 helper nor assumes a second reversal map.'},
    {'id':'endpoint-scope', 'status':'resolved', 'reason':'OPENARC100 now includes the off-event closed horizon. At zero, actual93 initial arc yields barGamma(0)=R A and gamma(T)=A. At T, actual93 last arc and the second actual99 pair at last yield barGamma(T)=R post(0)=R z; actual93 gives gamma(0)=z. Strict tuple bounds exclude events at both endpoints.'}
  ],
  'mathematical_audit': {
    'interior':'For reverse active arc j and k=n-j, complemented grids give d-v=T-s-b_k. STATES99 supplies barPost_j=R(Phi_d post_k); flow group and R Phi reversal give Phi_v barPost_j=R(Phi_(d-v) post_k). PATH93 identifies both actual Gamma values. Excluding event times is essential for the right-continuous convention.',
    'zero_cases':'n=0 retains one arc; T=0,n=0 retains the coincident endpoint and zero integrals; T=0,n>0 has empty strict simplex. Rank zero, zero normals and zero rates need no added exclusion.',
    'integral_bridge':'Finite event range is volume-null; the off-event equality gives AE equality on the interval. Actual94 forward interval integrability on the reversed input, AE congruence, reflection composition and interval symmetry discharge both integrability exports. Time substitution s -> T-s gives the positive-orientation integral equality.',
    'correct_94_api':'AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPrescribedPathDensity.actual_prescribed_path_density_rewrite',
    'same_witness':'RHO99 and STATES99 are sibling projections from one existing producer application; the projection node is not a fresh theorem hypothesis or an inference from states alone.',
    'graph_interpretation':'Inherited graph is retained by reference; the required100 adapter is explicit and separately named. The historical GAPS99 route remains historical source topology, not permission to call a private helper. Existing public producers discharge the selected slice under the unchanged six assumptions.'
  },
  'mechanical_validation': {'all_bound_RAWs_match':True,'checked_distinct_files':len(checked),'union_graph_acyclic':True,'union_nodes':len(nodes),'union_edges':len(edges),'topological_order':order,'source_regions_unchanged':21,'original19source_ids_retained_by_unchanged_inventory':True},
  'coverage':'The overlay adds no source region and changes no disposition. Original21-region audit and exact inherited99 inventory are reused by unchanged RAW. Only the selected off-event and survival-integral components of A7/A8 are admitted prospectively; weighted sectors, averaging, invariance and later analysis remain outside this header.',
  'type_validation':'Original independent fresh Header100 type-only PASS reused by exact unchanged Header RAW and immutable receipt; a graph-only correction does not warrant duplicate elaboration.',
  'preservation': {'original_review_and_negative_unchanged':True,'append_only_api_erratum_preserved':True,'header_and_six_assumptions_unchanged':True,'production_and_shared_records_unmodified':True},
  'no_Lean_proof_credit':True, 'no_statement_seal_or_claim':True, 'no_VERIFIED_transition':True
}
def write(name, obj):
    p = OWN / name
    assert not p.exists(), p
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n', encoding='utf-8', newline='\n')
    return raw(p.relative_to(ROOT).as_posix())

receipt = write('source-topology-admission100.native.json', decision)
manifest = write('closed-RAW-topology-admission100.native.json', {
    'kind':'closed-independent-topology-overlay-review100',
    'inputs':list(checked.values()),
    'files':[receipt, raw(Path(__file__).resolve().relative_to(ROOT).as_posix())],
    'closed':True, 'hash_algorithm':'SHA256 exact raw bytes', 'self_hash_intentionally_omitted':True
})
print(json.dumps({'decision':receipt,'manifest':manifest}, indent=2))
