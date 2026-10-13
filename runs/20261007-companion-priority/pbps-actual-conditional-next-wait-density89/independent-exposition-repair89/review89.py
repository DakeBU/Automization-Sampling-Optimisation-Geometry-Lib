import datetime
import hashlib
import json
from pathlib import Path

BASE = Path('E:/Samplinglib')
RUN = BASE / 'runs/20261007-companion-priority/pbps-actual-conditional-next-wait-density89'
OUT = RUN / 'independent-exposition-repair89'
PACKET = RUN / 'independent-math89/exposition-repair-review-packet89.json'
EXPECTED_PACKET = '7d7290f4ea779020a51f1e14a9c07e582c1a41f06dc2e97b092599209f6a7869'

def digest(data):
    return hashlib.sha256(data).hexdigest()

def info(path):
    raw = path.read_bytes()
    return {'path': str(path), 'sha256': digest(raw), 'bytes': len(raw)}

def write(name, obj):
    (OUT / name).write_bytes((json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))

def differences(a, b, pointer=''):
    if type(a) is not type(b):
        return [pointer]
    if isinstance(a, dict):
        assert a.keys() == b.keys()
        return sum((differences(a[k], b[k], pointer + '/' + k) for k in a), [])
    if isinstance(a, list):
        assert len(a) == len(b)
        return sum((differences(x, y, pointer + '/' + str(i)) for i, (x, y) in enumerate(zip(a, b))), [])
    return [] if a == b else [pointer]

packet_raw = PACKET.read_bytes()
assert digest(packet_raw) == EXPECTED_PACKET
packet = json.loads(packet_raw)
raw_dir = OUT / 'raw-inputs'
raw_dir.mkdir(exist_ok=True)
(raw_dir / 'packet89.exactraw.json').write_bytes(packet_raw)
inputs = []
for i, expected in enumerate(packet['inputs'] + packet['original_snapshots']):
    path = BASE / expected['path']
    raw = path.read_bytes()
    assert digest(raw) == expected['sha256'] and len(raw) == expected['bytes']
    snapshot = raw_dir / (str(i) + '-' + path.name)
    snapshot.write_bytes(raw)
    inputs.append({**info(path), 'read_mode': 'content-read', 'closed_snapshot': str(snapshot)})

overlay = json.loads((BASE / packet['inputs'][3]['path']).read_bytes())
old_raw = (BASE / packet['original_snapshots'][0]['path']).read_bytes()
new_raw = (BASE / packet['inputs'][4]['path']).read_bytes()
old, new = json.loads(old_raw), json.loads(new_raw)
changes = overlay['changes']
assert len(changes) == 1
change = changes[0]
pointer = '/units/0/steps/1/formula'
assert change['json_pointer'] == pointer
assert differences(old, new) == [pointer]
assert old['units'][0]['steps'][1]['formula'] == change['before']
assert new['units'][0]['steps'][1]['formula'] == change['after']
before = json.dumps(change['before'], ensure_ascii=False).encode()
after = json.dumps(change['after'], ensure_ascii=False).encode()
assert old_raw.count(before) == 1 and old_raw.replace(before, after) == new_raw

lean_path = BASE / packet['inputs'][2]['path']
lean_raw = lean_path.read_bytes()
lines = lean_raw.splitlines(keepends=True)
regions = []
for step, item in enumerate(new['units'][0]['steps'], 1):
    region = item['lean_source_region']
    raw = b''.join(lines[region['start_line'] - 1:region['end_line']])
    assert raw == item['lean'].encode()
    assert digest(raw) == region['exact_code_raw_sha256']
    regions.append({'step': step, 'start_line': region['start_line'], 'end_line': region['end_line'], 'raw_sha256': digest(raw), 'bytes': len(raw), 'exact_embedded_lean_match': True})

seal_path = RUN / 'root.statement-seal89.json'
seal = info(seal_path)
assert seal['sha256'] == overlay['unchanged']['statement_seal_sha256']
inputs.append({**seal, 'read_mode': 'hash-only; not parsed or used as prior verdict evidence'})
primary_path = OUT / 'primary2609.06905v1.direct.html'
primary = info(primary_path)
assert primary['sha256'] == 'd81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
assert primary['bytes'] == 1482128
inputs.append({**primary, 'read_mode': 'direct pinned-version source; web read before candidate, local HTML read later', 'url': 'https://arxiv.org/html/2609.06905v1'})

checks = {
    'reviewer_id': '/root/exposition_repair89',
    'all_packet_raw_inputs_and_snapshots_match': True,
    'packet_sha256': EXPECTED_PACKET,
    'decoded_difference_pointers': differences(old, new),
    'raw_entire_candidate_equals_single_exact_field_replacement': True,
    'removed_bytes': len(old_raw) - len(new_raw),
    'before': change['before'], 'after': change['after'],
    'exact_adjacent_lean_regions': regions,
    'canonical_lesson_still_original': (BASE / packet['inputs'][0]['path']).read_bytes() == old_raw,
    'canonical_publication_equals_original_snapshot': (BASE / packet['inputs'][1]['path']).read_bytes() == (BASE / packet['original_snapshots'][1]['path']).read_bytes(),
    'statement_seal_hash_only_match': True,
    'lean_build_performed': False,
    'lean_build_reason': 'No Lean change; this independently reviews one exposition field only and grants no compilation or whole-theorem proof credit.'
}
write('checks89.native.json', checks)

chronology = {
    'reviewer_id': '/root/exposition_repair89',
    'chronology_type': 'native observed tool-call sequence; exact times supplied only when observed',
    'events': [
        {'order': 1, 'action': 'Read exact supplied packet and verify its SHA256.'},
        {'order': 2, 'action': 'Hash all seven explicitly listed raw inputs/snapshots without reading candidate content; read current publication for source URL. Embedded references to prior acceptance were incidental and not followed or relied on.'},
        {'order': 3, 'action': 'Read pinned primary directly using web open/find/open: arXiv2609.06905v1 Appendix A.1 (A.1), (A.2), strict ordered simplex and (A.7); Appendix A.2 joint Borel recursion. This preceded candidate/exposition comparison.'},
        {'order': 4, 'action': 'Capture primary HTML directly into owned directory, then read proposed overlay and Lean BODY lines 250-370.', 'primary_capture_observed_utc': '2026-10-10T23:20:27.1310299Z'},
        {'order': 5, 'action': 'Compute recursive JSON diff. First lesson display failed at Windows GBK output encoding; rerun with UTF-8 only, without changing any input.'},
        {'order': 6, 'action': 'Read proposed lesson statement and all six steps; verify exact adjacent code regions, one raw-byte replacement and seal hash-only. Read raw primary local A.1/A.2 excerpts.', 'checks_observed_utc': '2026-10-10T23:21:09.911817+00:00'},
        {'order': 7, 'action': 'First artifact script execution reached writing checks but local Python rejected pathlib.write_text(newline=). Change only the owned script to UTF-8 write_bytes and rerun; no review input changed.'},
        {'order': 8, 'action': 'Write independent native decision/checks/chronology and closed RAW manifest within the owned directory.'}
    ],
    'excluded_evidence': ['No root history was inherited.', 'No earlier mathematical/source review or acceptance record was searched or opened.', 'Current publication metadata containing prior verdict claims was not used as evidence.', 'No source-proof graph, coverage decision, reviewed adapter, or earlier BODY decision was opened.'],
    'finished_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()
}
write('chronology89.native.json', chronology)

decision = {
    'decision': 'ACCEPT_EXACT_ONE_FIELD_EXPOSITION_REPAIR',
    'reviewer_id': '/root/exposition_repair89',
    'distinct_from_proposer': overlay['proposer_id'] == '/root/exact_verify77',
    'distinct_from_author_root': True,
    'proposal': info(BASE / packet['inputs'][3]['path']),
    'original_lesson': info(BASE / packet['original_snapshots'][0]['path']),
    'accepted_proposed_lesson': info(BASE / packet['inputs'][4]['path']),
    'accepted_json_pointer': pointer,
    'native_findings': [
        'The candidate differs from the original in exactly the specified formula string. The entire raw file is the original raw file with exactly one JSON-encoded string replacement; all other fields, including theorem statement, assumptions, source attribution, boundaries, Lean excerpts and region metadata, are unchanged.',
        'In step 2, lines 279-280 define nu as the product measure with density D; lines 299-304 establish joint measurability of D; lines 305-306 identify K(h) with volume.withDensity(D(h)). Both remaining displayed formulas therefore belong beside this region.',
        'The removed K(h,R)<=1 clause is established in step 4, lines 359-365, using hK and the strict fiber pushforward law proved in step 3. Line 366 constructs IsFiniteKernel with uniform bound 1. The unchanged step-4 formula displays precisely that event-probability equality and bound beside this code.',
        'The theorem statement and publication retain the kernel mass conclusion. Removing its premature duplicate from the step-2 formula neither weakens the theorem nor creates any source premise, endpoint equivalence, normalization or finite-wait guarantee.',
        'Direct primary reading shows the stopped independent exponential-threshold recursion, strict ordered-time domain and jump-rate/survival factors, followed by joint Borel recursion. The one-field overlay changes no source interpretation or attributed completion boundary.',
        'All six embedded Lean regions are exact contiguous raw extracts of the supplied production module, including the two required comparison regions 259-306 and 359-366.'
    ],
    'required_repairs': [],
    'canonical_application_performed': False,
    'scope_limits': ['Independent acceptance is solely for this exact one-field exposition overlay.', 'No independent whole-theorem proof credit, source-fidelity acceptance, VERIFIED transition, purification, paper completion or Goal completion is granted.', 'No Lean, Statement Seal, canonical lesson or canonical publication was modified.'],
    'evidence_files': ['checks89.native.json', 'chronology89.native.json', 'closed-raw-manifest89.json'],
    'completed_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()
}
write('decision89.native.json', decision)

artifacts = [info(path) for path in sorted(OUT.rglob('*')) if path.is_file() and path.name != 'closed-raw-manifest89.json']
write('closed-raw-manifest89.json', {
    'reviewer_id': '/root/exposition_repair89',
    'algorithm': 'SHA256 of exact file bytes',
    'closure': 'All consulted local raw inputs and direct primary capture are identified; all review artifacts except this self-referential manifest are hashed. Manifest SHA256 and bytes are returned externally.',
    'inputs': [{'path': str(PACKET), 'sha256': EXPECTED_PACKET, 'bytes': len(packet_raw), 'closed_snapshot': str(raw_dir / 'packet89.exactraw.json')}] + inputs,
    'artifacts': artifacts,
    'excluded_self': str(OUT / 'closed-raw-manifest89.json')
})
for name in ['decision89.native.json', 'checks89.native.json', 'chronology89.native.json', 'closed-raw-manifest89.json']:
    print(json.dumps(info(OUT / name)))
