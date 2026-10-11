import copy
import datetime
import hashlib
import json
from pathlib import Path

BASE = Path('E:/Samplinglib')
RUN = BASE / 'runs/20261007-companion-priority/pbps-ordered-history-iteration-preread91'
OUT = RUN / 'independent-topology-repair91'
PACKET = RUN / 'independent-topology91/topology-route-repair91.packet.json'
REVIEWER = '/root/exposition_repair89'

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def info(path):
    raw = path.read_bytes()
    return {'path': str(path), 'sha256': sha(raw), 'bytes': len(raw)}

def write(name, obj):
    (OUT / name).write_bytes((json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))

assert info(OUT / 'source-first91.native.json')['sha256'] == 'f128840dcdf525d85d4d518c2b38a4a0b706b086664f46d644afcb7c4a57618e'
assert info(OUT / 'source-first91.raw-manifest.json')['sha256'] == '8deb9d360e42e3d092f3439b8f15f5f44c9d71743ecb65a952d998ae27d1404a'
assert info(PACKET)['sha256'] == 'bd26878996306f97c1153b1986ea26b4ae294d1f467b59ec30fb4f8c4b5f43eb'
packet = json.loads(PACKET.read_bytes())
raw_dir = OUT / 'raw-inputs'
raw_dir.mkdir(exist_ok=True)
(raw_dir / 'repair-packet91.private.exactraw.json').write_bytes(PACKET.read_bytes())
inputs = [{**info(PACKET), 'read_mode': 'clean packet after frozen primary-first reasoning', 'closed_snapshot': str(raw_dir / 'repair-packet91.private.exactraw.json')}]
paths = {}
for key, e in packet.items():
    if not isinstance(e, dict) or 'path' not in e or 'raw_sha256' not in e:
        continue
    p = BASE / e['path']
    raw = p.read_bytes()
    assert sha(raw) == e['raw_sha256'] and len(raw) == e['bytes']
    paths[key] = p
    mode = 'content after frozen primary-first reasoning'
    if key == 'primary':
        mode = 'direct primary first, before packet/graph/overlay; later raw span checks'
    if key == 'inherited_global_inventory':
        mode = 'hash-only; no earlier verdict used'
    if key == 'inherited_global_graph':
        mode = 'only E86-63 content used, other global verdict/status claims not used'
    eout = {**info(p), 'read_mode': mode}
    if key != 'primary':
        snapshot = raw_dir / (key + '.private.exactraw.json')
        snapshot.write_bytes(raw)
        eout['closed_snapshot'] = str(snapshot)
    else:
        eout['private_anchor_extract'] = str(OUT / 'primary-anchors91.private.json')
        eout['full_primary_copy_created'] = False
    inputs.append(eout)

provenance = RUN / 'independent-topology91/closed-RAW-manifest91.second-half.json'
assert info(provenance)['sha256'] == '9c260798f83dd9fc159090c6eae2b62524a4eb40621e38b806cf0fc5069859d4'
inputs.append({**info(provenance), 'read_mode': 'hash-only provenance; not parsed or used as verdict'})

primary = paths['primary'].read_bytes()
span_metadata = json.loads(paths['primary_spans'].read_bytes())
span_checks = []
for span in span_metadata['spans']:
    raw = primary[span['byte_start_zero_based']:span['byte_end_exclusive']]
    assert sha(raw) == span['raw_span_sha256']
    span_checks.append({'anchor': span.get('anchor', span.get('label')), 'sha256': sha(raw), 'bytes': len(raw), 'match': True})

original = json.loads(paths['original_graph'].read_bytes())
successor = json.loads(paths['exact_proposed_successor'].read_bytes())
proposal = json.loads(paths['exact_proposal'].read_bytes())
assert proposal['proposer_id'] == '/root/exact_verify77'
assert original['creator'] == '/root/fresh_source87'
assert REVIEWER not in [proposal['proposer_id'], original['creator'], '/root']
expected_ops = [('replace', '/AND_junctions/5/route'), ('add', '/AND_junctions/-'), ('add', '/OR_routes/-')]
assert [(e['op'], e['path']) for e in proposal['operations']] == expected_ops
computed = copy.deepcopy(original)
for op in proposal['operations']:
    keys = op['path'].strip('/').split('/')
    target = computed
    for key in keys[:-1]:
        target = target[int(key)] if isinstance(target, list) else target[key]
    key = keys[-1]
    if op['op'] == 'replace':
        assert target[key] == op['before']
        target[key] = op['value']
    else:
        assert key == '-' and isinstance(target, list)
        target.append(op['value'])
assert computed == successor
assert (json.dumps(computed, ensure_ascii=False, indent=2) + '\n').encode('utf-8') == paths['exact_proposed_successor'].read_bytes()
unchanged = [key for key in original if key not in ['AND_junctions', 'OR_routes']]
assert all(original[key] == successor[key] for key in unchanged)
assert original['AND_junctions'][:5] == successor['AND_junctions'][:5]
assert original['AND_junctions'][5]['target'] == successor['AND_junctions'][5]['target'] == 'S91-A7'
assert original['AND_junctions'][5]['parents'] == successor['AND_junctions'][5]['parents'] == ['S91-F', 'S91-P', 'S91-AC']
assert original['OR_routes'] == successor['OR_routes'][:-1]
assert successor['AND_junctions'][-1]['parents'] == ['S91-F', 'S91-P']
assert successor['OR_routes'][-1]['not_both_AND'] is True
nodes = {node['id']: node for node in successor['nodes']}
for node in ['S91-J', 'S91-F', 'S91-P', 'S91-AC', 'S91-A7', 'S91-ALG', 'S91-PATH']:
    assert nodes[node]['status'].startswith('OPEN')
assert nodes['S91-B']['status'] == 'OPEN_IF_ENDPOINT_EQUALITY_ASSERTED_NOT91_PARENT'
edgepairs = {(edge['from'], edge['to']) for edge in successor['edges']}
for parent in successor['AND_junctions'][-1]['parents']:
    assert (parent, 'S91-A7') in edgepairs

global_graph = json.loads(paths['inherited_global_graph'].read_bytes())
def find_edge(value):
    if isinstance(value, dict):
        if value.get('id') == 'E86-63':
            return value
        for v in value.values():
            hit = find_edge(v)
            if hit:
                return hit
    if isinstance(value, list):
        for v in value:
            hit = find_edge(v)
            if hit:
                return hit
    return None
retained_edge = find_edge(global_graph)
assert retained_edge == proposal['global_retained_route']
assert retained_edge['classification'] == 'SUFFICIENT_SUMMABILITY_ROUTE'
coverage = json.loads(paths['unchanged_coverage'].read_bytes())
assert len(coverage['coverage']) == 27
assert not coverage['uncovered_local_items']
relevant_coverage = [item for item in coverage['coverage'] if item['id'] in ['C18', 'C20', 'C21', 'C25']]
candidate = json.loads(paths['unchanged_candidate'].read_bytes())
assert candidate['status'] == 'PROPOSAL_ONLY_NO_CLAIM_HEADER_SEAL_PROOF'
assert candidate['preferred_parent'] == 'actual_finite_history_extension90'
assert candidate['cases']['endpoint'].startswith('Both sides are strict')

write('checks91.native.json', {
    'reviewer_id': REVIEWER,
    'primary_first_reasoning_frozen_sha256': 'f128840dcdf525d85d4d518c2b38a4a0b706b086664f46d644afcb7c4a57618e',
    'all_packet_raw_inputs_match': True,
    'primary_span_raw_checks': span_checks,
    'exact_operations': proposal['operations'],
    'computed_successor_equals_exact_supplied_successor': True,
    'serialized_entire_successor_exact_raw_match': True,
    'only_three_operations_change_graph': True,
    'counts': {'nodes': len(successor['nodes']), 'edges': len(successor['edges']), 'old_AND_junctions': len(original['AND_junctions']), 'new_AND_junctions': len(successor['AND_junctions']), 'old_OR_routes': len(original['OR_routes']), 'new_OR_routes': len(successor['OR_routes']), 'coverage': len(coverage['coverage'])},
    'all_other_top_level_fields_unchanged': unchanged,
    'all_node_claims_and_statuses_unchanged': True,
    'all_edges_unchanged': True,
    'six_source_hypotheses_unchanged': len(successor['source_hypotheses']) == 6,
    'inherited_E86_63_exact': retained_edge,
    'relevant_retained_coverage': relevant_coverage,
    'candidate_scope_unchanged': 'Only graph file is changed by the exact operations; separately supplied candidate remains proposal-only with strict endpoint and finite coordinate boundary.',
    'no91_header_Seal_BODY_or_implementation_read': True,
    'no_prior_acceptance_verdict_read_or_used': True,
    'canonical_application': False
})

write('decision91.native.json', {
    'decision': 'ACCEPT_EXACT_THREE_OPERATION_ROUTE_INDEXED_TOPOLOGY_OVERLAY91',
    'reviewer_id': REVIEWER,
    'distinct_from_proposer77_creator87_and_root': True,
    'exact_proposal': info(paths['exact_proposal']),
    'exact_accepted_successor': info(paths['exact_proposed_successor']),
    'original_graph': info(paths['original_graph']),
    'primary_first_reasoning': info(OUT / 'source-first91.native.json'),
    'native_independent_findings': [
        'The original local graph has only one A7 junction, labelled full A7 with parents F, P and AC. That presentation makes the cap/simplex-specific AC obligatory for every displayed local A7 route, despite the valid alternative preserved by inherited global E86-63 and independently reconstructed before this overlay was read.',
        'For the printed route, the nonnegative survival factor is at most one and the finite preserved-energy cap M bounds the n rate factors. For |Psi|<=B, simplex volume t^n/n! bounds the absolute n contribution by B*(M*t)^n/n!, giving a summable majorant. This remains a valid route; summability alone does not identify the actual count/path law.',
        'For the alternative, F must establish each exact finite-count nonnegative factor law, including final survival and segment-to-path hazard algebra, and P must establish the exhaustive AE actual count/path partition with Borel path tests and all chosen endpoint conventions. Once these OPEN obligations are proved, let q_n be the identified event measures. Then sum mass(q_n)=sum P(E_n)=1 follows from the actual probability partition, without assuming full A7.',
        'Tonelli then gives sum integral |Psi| dq_n=E|Psi(actual_path)|<=B, so sum |integral Psi dq_n|<=B. Applying the nonnegative identity to positive and negative parts gives the bounded signed A7 expectation identity. This is noncircular because exact finite-count identities and actual partition, rather than full A7 or a supplied normalization premise, provide mass one.',
        'The separate cap/simplex estimate is unnecessary at the final alternative assembly junction. This does not remove any cap dependency from the already established upstream nonexplosion proof or erase the printed source route. The partition route also avoids requiring an integrable exp(M(z0)*t) envelope when subsequently averaging uniformly bounded tests over an initial probability law.',
        'The three operations are exact and sufficient: relabel the existing cap-specific junction as one sufficient route; add an F-and-P alternative junction; and add the explicit A7 OR entry. The entire supplied successor equals the original with those exact operations, including exact serialized raw bytes. Existing source nodes, dependency edges, statuses, six binders, earlier routes, coverage and bounded91 coordinate target are unchanged.',
        'Ordered finite induction, final survival/hazard algebra, actual prescribed-path observables, endpoint resolution and exhaustive count/path compatibility remain OPEN. The conditional boundary node remains required only when endpoint conventions are equated; no finite-atom or physical-time restart premise is introduced. Survival88 remains a future final-factor parent, not a parent of the bounded91 density target.',
        'The fixed-primary printed convergence sentence is distinguished from the source-implicit ASTIS partition alternative. The overlay records sufficient-route bookkeeping and grants no source theorem implementation, local proof closure or full A7 result.'
    ],
    'required_repairs': [],
    'scope_limits': ['Acceptance covers only the exact proposer77 route-indexed overlay.', 'This does not replace a whole topology/coverage review of the graph or candidate, and does not approve a91 header, Statement Seal, SAU claim or BODY.', 'No VERIFIED, canonical integration, whole-paper or Goal completion credit is granted.', 'Only the assigned review directory was written; original and canonical inputs remain unchanged.'],
    'source_data_not_published': True,
    'full_primary_copy_created': False,
    'frozen_before_return': True,
    'completed_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()
})

write('chronology91.native.json', {
    'reviewer_id': REVIEWER,
    'events': [
        {'order': 1, 'action': 'Read primary Appendix A1/A2 and exact A7 directly before any graph/proposal; independently reconstruct sufficient cap/simplex and finite-count partition routes.', 'observed_utc': '2026-10-11T01:26:56.311367+00:00'},
        {'order': 2, 'action': 'Save and freeze source-first91.native.json and preparation manifest before root supplied exact overlay packet; report those hashes to root.'},
        {'order': 3, 'action': 'Receive exact clean packet/proposal/successor/provenance hashes; read packet and hash all exact raw inputs.'},
        {'order': 4, 'action': 'Read proposal, original graph and unchanged bounded candidate; inspect only inherited global E86-63. No older acceptance decisions or predecessor reconstruction files opened.', 'observed_utc': '2026-10-11T01:29:00.706180+00:00'},
        {'order': 5, 'action': 'Apply all three operations in memory and compare complete exact successor bytes; inspect relevant coverage and primary span metadata. Hash second-half manifest only for provenance.', 'observed_utc': '2026-10-11T01:29:35.914705+00:00'},
        {'order': 6, 'action': 'Write native independent decision/checks/run and final closed RAW manifest. Validate closure and mark owned outputs read-only before return; retain frozen source-first notes unchanged.'}
    ],
    'no_canonical_application': True,
    'no91_header_Seal_claim_or_BODY_read': True,
    'private_source_extracts_only': True,
    'finished_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()
})

artifacts = [info(p) for p in sorted(OUT.rglob('*')) if p.is_file() and p.name != 'closed-raw-manifest91.json']
write('closed-raw-manifest91.json', {
    'reviewer_id': REVIEWER,
    'algorithm': 'SHA256 exact raw bytes',
    'closure': 'All exact consulted input files and all owned artifacts are byte/hash identified. Previous primary-first frozen artifacts remain unchanged and are included. Full primary stays at supplied path, with private bounded extracts only. Manifest excludes only itself; external return identifies its exact digest/bytes.',
    'inputs': inputs,
    'artifacts': artifacts,
    'excluded_self': str(OUT / 'closed-raw-manifest91.json'),
    'frozen': True
})
for name in ['decision91.native.json', 'checks91.native.json', 'chronology91.native.json', 'closed-raw-manifest91.json']:
    print(json.dumps(info(OUT / name)))
