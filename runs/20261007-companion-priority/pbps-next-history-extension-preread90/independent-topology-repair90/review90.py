import datetime
import hashlib
import json
from pathlib import Path

BASE = Path('E:/Samplinglib')
RUN = BASE / 'runs/20261007-companion-priority/pbps-next-history-extension-preread90'
OUT = RUN / 'independent-topology-repair90'
PACKET = RUN / 'independent-topology90/topology-repair-review-packet90.json'
REVIEWER = '/root/exposition_repair89'

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def info(path):
    raw = path.read_bytes()
    return {'path': str(path), 'sha256': digest(raw), 'bytes': len(raw)}

def write(name, obj):
    (OUT / name).write_bytes((json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))

def diff(a, b, p=''):
    if type(a) is not type(b):
        return [p]
    if isinstance(a, dict):
        assert a.keys() == b.keys()
        return sum((diff(a[k], b[k], p + '/' + k) for k in a), [])
    if isinstance(a, list):
        assert len(a) == len(b)
        return sum((diff(x, y, p + '/' + str(i)) for i, (x, y) in enumerate(zip(a, b))), [])
    return [] if a == b else [p]

assert info(PACKET)['sha256'] == '8081c99c3fd1ef25389897e4ea2da18e1ff7f6f975a08c2b8ad575315d7ead3c'
packet = json.loads(PACKET.read_bytes())
inputs = [{**info(PACKET), 'read_mode': 'content read first'}]
raw_dir = OUT / 'raw-inputs'
raw_dir.mkdir(exist_ok=True)
(raw_dir / 'packet90.private.exactraw.json').write_bytes(PACKET.read_bytes())
paths = {}
for key in ['primary', 'original_graph_snapshot', 'original_coverage_snapshot', 'proposal', 'exact_candidate_graph']:
    entry = packet[key]
    p = Path(entry['path'])
    p = p if p.is_absolute() else BASE / p
    raw = p.read_bytes()
    assert digest(raw) == entry['raw_sha256'] and len(raw) == entry['bytes']
    paths[key] = p
    mode = 'primary anchors read directly before graph/proposal comparison' if key == 'primary' else 'content read after primary-first note'
    if key == 'original_coverage_snapshot':
        mode = 'raw hash, list count, item14 only; no review/acceptance metadata used'
    item = {**info(p), 'read_mode': mode}
    if key != 'primary':
        snapshot = raw_dir / (key + '.private.exactraw.json')
        snapshot.write_bytes(raw)
        item['closed_snapshot'] = str(snapshot)
    else:
        item['private_anchor_extract'] = str(OUT / 'primary-anchors90.private.json')
        item['full_primary_copy_created'] = False
    inputs.append(item)

original = json.loads(paths['original_graph_snapshot'].read_bytes())
candidate = json.loads(paths['exact_candidate_graph'].read_bytes())
proposal = json.loads(paths['proposal'].read_bytes())
expected = ['/nodes/1/claim', '/edges/1/justification']
assert diff(original, candidate) == expected
assert original['nodes'][1]['id'] == candidate['nodes'][1]['id'] == 'S90-A1'
assert original['edges'][1]['source'] == 'S90-A1' and original['edges'][1]['target'] == 'S90-M1'
assert len(proposal['changes']) == 2
raw = paths['original_graph_snapshot'].read_bytes()
for change, pointer in zip(proposal['changes'], expected):
    assert change['json_pointer'] == pointer
    keys = pointer.strip('/').split('/')
    old = original[keys[0]][int(keys[1])][keys[2]]
    new = candidate[keys[0]][int(keys[1])][keys[2]]
    assert old == change['before'] and new == change['after']
    before = json.dumps(old, ensure_ascii=False).encode('utf-8')
    after = json.dumps(new, ensure_ascii=False).encode('utf-8')
    assert raw.count(before) == 1
    raw = raw.replace(before, after)
assert raw == paths['exact_candidate_graph'].read_bytes()

unchanged_keys = [key for key in original if key not in ['nodes', 'edges']]
assert all(original[key] == candidate[key] for key in unchanged_keys)
assert len(original['nodes']) == len(candidate['nodes']) == 7
assert len(original['edges']) == len(candidate['edges']) == 8
assert len(original['AND_junctions']) == len(candidate['AND_junctions']) == 3
coverage = json.loads(paths['original_coverage_snapshot'].read_bytes())
assert len(coverage['items']) == 22
item14 = coverage['items'][13]
assert item14['item'] == 'A.2 Borel hazard/threshold and finite recursive jump times/states'
assert 'S90-M1' in item14['nodes']
for key in ['original_graph', 'unchanged_coverage']:
    e = proposal[key]
    p = BASE / e['path']
    item = info(p)
    assert item['sha256'] == e['raw_sha256'] and item['bytes'] == e['bytes']
    inputs.append({**item, 'read_mode': 'hash only; canonical originals preserved'})

checks = {
    'reviewer_id': REVIEWER,
    'all_packet_input_hashes_and_bytes_match': True,
    'exact_proposal_raw': info(paths['proposal']),
    'exact_candidate_raw': info(paths['exact_candidate_graph']),
    'decoded_difference_pointers': diff(original, candidate),
    'entire_candidate_is_exact_two_string_raw_replacement': True,
    'counts': {'nodes': 7, 'edges': 8, 'AND_junctions': 3, 'coverage_items': 22},
    'all_other_graph_fields_unchanged': True,
    'node_and_edge_identities_memberships_unchanged': True,
    'AND_memberships_unchanged': original['AND_junctions'] == candidate['AND_junctions'],
    'OR_routes_unchanged': original['alternative_sufficient_routes'] == candidate['alternative_sufficient_routes'],
    'source_hypotheses_unchanged': original['source_hypotheses'] == candidate['source_hypotheses'],
    'non_AND_parents_unchanged': original['not_AND_parents'] == candidate['not_AND_parents'],
    'truth_boundary_unchanged': original['truth_boundary'] == candidate['truth_boundary'],
    'coverage_item14_checked': item14,
    'coverage_snapshot_and_canonical_exactraw_match': paths['original_coverage_snapshot'].read_bytes() == (BASE / proposal['unchanged_coverage']['path']).read_bytes(),
    'original_graph_snapshot_and_canonical_exactraw_match': paths['original_graph_snapshot'].read_bytes() == (BASE / proposal['original_graph']['path']).read_bytes(),
    'Lean_or_header_read': False,
    'prior_review_or_acceptance_record_read': False
}
write('checks90.native.json', checks)

decision = {
    'decision': 'ACCEPT_EXACT_TWO_FIELD_SOURCE_TOPOLOGY_SCOPE_OVERLAY',
    'reviewer_id': REVIEWER,
    'distinct_from_graph_creator': REVIEWER != original['creator'],
    'distinct_from_proposer': REVIEWER != proposal['proposer_id'],
    'distinct_from_root_formalizer': REVIEWER != '/root',
    'proposal': info(paths['proposal']),
    'original_graph': info(paths['original_graph_snapshot']),
    'accepted_candidate_graph': info(paths['exact_candidate_graph']),
    'accepted_pointers': expected,
    'native_source_mathematical_findings': [
        'The existing S90-M1 target includes both a Borel abstract history/wait append and actual next-history measurability. Flow/reflection and finite tuple operations establish the former, but cannot by themselves establish Borel dependence of the actual next wait, which is selected by the integrated-hazard threshold crossing.',
        'Primary Appendix A.2 explicitly supplies Borel integrated hazard, threshold-crossing times and finite recursive jump times/post-jump states. Combining that paragraph with the finite branch and stopped recursion in A.1(A.1)-(A.2), finite prefix/tag constructions gives the source-backed finite stopped-history input. This uses no nonexplosion limit or physical-time restart theorem.',
        'Expanding the existing S90-A1 node and its existing edge to S90-M1 records this omitted scope. Both changes are necessary for a coherent node/edge pair: changing the node alone leaves the edge justification incomplete; changing only the edge names a proof ingredient absent from its producer node.',
        'The candidate is exactly the original graph with the two stated strings replaced. There are no added nodes, edges, AND parents, public premises, hypotheses, OR-route changes, coverage changes or target-boundary changes. Coverage item14 already records the same A.2 ingredient as supporting S90-M1.',
        'The phrase derived internally or consumed from exact verified producers is a proof obligation, not an added theorem premise or a claim of present compilation. The actual next-history measurability conclusion remains an OPEN target ingredient; the expanded source ingredient does not certify its implementation.',
        'The existing89 strict joint-measure transport route remains sufficient once the unchanged Borel append and guarded actual-recursion identity are supplied. Density-law transport is not being used as a substitute for actual finite-history Borel derivation. The direct87/86 calculation remains an alternative, without additional AND dependencies.',
        'Neither a separate no-finite-atom result nor survival88 becomes a prerequisite. Strict positivity/finite cutoff and the finite source update suffice for this extension; full ordered-time iteration and final survival/count assembly remain outside90.'
    ],
    'required_repairs': [],
    'canonical_application_performed': False,
    'scope_limits': ['Approval is only of this exact dependency-scope repair, not a whole-graph topology/coverage admission.', 'No90 theorem header, Lean BODY, SAU verification, source-fidelity completion, VERIFIED transition, paper completion or Goal completion is approved.', 'No canonical input, coverage, graph or original snapshot was modified.'],
    'source_first_note': str(OUT / 'source-first90.native.json'),
    'completed_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()
}
write('decision90.native.json', decision)

chronology = {
    'reviewer_id': REVIEWER,
    'chronology_type': 'native observed sequence with exact times only where observed',
    'events': [
        {'order': 1, 'action': 'Read exact supplied packet; verify packet SHA256.'},
        {'order': 2, 'action': 'Hash all five packet raw inputs without reading graph/proposal content, then read fixed local primary A1.E1, A1.E2, A1.E7 and A1.SS2 Borel paragraph.', 'observed_utc': '2026-10-10T23:53:27.623380+00:00'},
        {'order': 3, 'action': 'Read strict simplex immediately preceding A1.E7; save private source-anchor extract and native source-first note before candidate comparison.', 'observed_utc': '2026-10-10T23:53:46.845256+00:00'},
        {'order': 4, 'action': 'Read proposal, original graph snapshot and exact candidate. Do not follow global graph/inventory references or prior review metadata.'},
        {'order': 5, 'action': 'Compute recursive exact two-field diff and raw replacement equality. Hash canonical original graph/coverage only. Inspect only original coverage list count and item14 for the stated Borel ingredient.', 'observed_utc': '2026-10-10T23:54:09.069652+00:00'},
        {'order': 6, 'action': 'Write native independent decision/checks/run record and closed RAW manifest only inside assigned review directory.'}
    ],
    'no_prior_verdicts_relied_on': True,
    'no90_header_or_Lean_read': True,
    'source_extract_policy': 'Only targeted excerpts saved, with .private. filenames; no full primary copy created.',
    'finished_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()
}
write('chronology90.native.json', chronology)

artifacts = [info(p) for p in sorted(OUT.rglob('*')) if p.is_file() and p.name != 'closed-raw-manifest90.json']
write('closed-raw-manifest90.json', {
    'reviewer_id': REVIEWER,
    'algorithm': 'SHA256 of exact file bytes',
    'closure': 'Every consulted raw file is identified; targeted primary extracts are private, full primary remains at the exact supplied path. Every output except this self-referential manifest is hashed. Manifest digest and bytes are returned externally.',
    'inputs': inputs,
    'artifacts': artifacts,
    'excluded_self': str(OUT / 'closed-raw-manifest90.json')
})
for name in ['decision90.native.json', 'checks90.native.json', 'chronology90.native.json', 'closed-raw-manifest90.json']:
    print(json.dumps(info(OUT / name)))
