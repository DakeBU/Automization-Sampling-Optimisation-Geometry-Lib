import datetime
import hashlib
import json
from pathlib import Path

BASE = Path('E:/Samplinglib')
RUN = BASE / 'runs/20261007-companion-priority/pbps-actual-finite-history-extension90'
OUT = RUN / 'independent-exposition-repair90'
PACKET = RUN / 'independent-math90/exposition-repair-review-packet90.json'
REVIEWER = '/root/exposition_repair89'

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def info(path):
    raw = path.read_bytes()
    return {'path': str(path), 'sha256': digest(raw), 'bytes': len(raw)}

def write(name, data):
    (OUT / name).write_bytes((json.dumps(data, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))

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

assert info(PACKET)['sha256'] == '84959316f5b01cbe08663c8555ecfcc1623fdf1466f8f80cfe053db90c2707b0'
packet = json.loads(PACKET.read_bytes())
assert (OUT / 'source-first90.native.json').exists()
source_first = json.loads((OUT / 'source-first90.native.json').read_bytes())
assert source_first['phase'] == 'PRIMARY_FIRST_BEFORE_ORIGINAL_CANDIDATE_MATHEMATICAL_COMPARISON'
raw_dir = OUT / 'raw-inputs'
raw_dir.mkdir(exist_ok=True)
(raw_dir / 'packet90.private.exactraw.json').write_bytes(PACKET.read_bytes())
inputs = [{**info(PACKET), 'read_mode': 'packet read first', 'closed_snapshot': str(raw_dir / 'packet90.private.exactraw.json')}]
entries = [(key, packet[key]) for key in ['primary', 'original_module', 'statement_seal', 'original_lesson', 'original_publication', 'original_publication_freeze', 'proposal']]
entries += [('candidate_' + str(i), entry) for i, entry in enumerate(packet['candidates'])]
paths = {}
for key, entry in entries:
    path = BASE / entry['path']
    raw = path.read_bytes()
    assert digest(raw) == entry['raw_sha256'] and len(raw) == entry['bytes']
    paths[key] = path
    mode = 'mathematical content read after primary-first note'
    if key in ['statement_seal', 'original_publication_freeze']:
        mode = 'hash-only; not parsed or used as prior decision evidence'
    if key == 'primary':
        mode = 'bounded source anchors read directly before original/candidate comparison'
    item = {**info(path), 'read_mode': mode}
    if key != 'primary':
        snapshot = raw_dir / (key + '.private.exactraw' + path.suffix)
        snapshot.write_bytes(raw)
        item['closed_snapshot'] = str(snapshot)
    else:
        item['private_anchor_extract'] = str(OUT / 'primary-anchors90.private.json')
        item['full_primary_copy_created'] = False
    inputs.append(item)

proposal = json.loads(paths['proposal'].read_bytes())
assert proposal['proposer_id'] != REVIEWER
assert len(proposal['changes']) == 2
pointers = ['/units/0/steps/0/formula', '/items/0/formulae/0/tex']
assert packet['pointers'] == pointers
records = []
objects = {}
for i, key in enumerate(['original_lesson', 'original_publication']):
    original_raw = paths[key].read_bytes()
    candidate_raw = paths['candidate_' + str(i)].read_bytes()
    original = json.loads(original_raw)
    candidate = json.loads(candidate_raw)
    change = proposal['changes'][i]
    assert change['pointer'] == pointers[i]
    assert differences(original, candidate) == [pointers[i]]
    before = json.dumps(change['before'], ensure_ascii=False).encode('utf-8')
    after = json.dumps(change['after'], ensure_ascii=False).encode('utf-8')
    assert original_raw.count(before) == 1
    assert original_raw.replace(before, after) == candidate_raw
    assert len(candidate_raw) - len(original_raw) == 6
    records.append({'pointer': pointers[i], 'exact_single_json_string_raw_replacement': True, 'decoded_differences': differences(original, candidate), 'added_bytes': 6, 'original': info(paths[key]), 'candidate': info(paths['candidate_' + str(i)])})
    objects[key] = original
    objects['candidate_' + str(i)] = candidate

original_lesson = objects['original_lesson']
candidate_lesson = objects['candidate_0']
original_publication = objects['original_publication']
candidate_publication = objects['candidate_1']
assert original_lesson['units'][0]['statement'] == original_publication['items'][0]['statement']
assert candidate_lesson['units'][0]['statement'] == original_lesson['units'][0]['statement']
assert candidate_publication['items'][0]['statement'] == original_publication['items'][0]['statement']
assert proposal['changes'][0]['after'] == proposal['changes'][1]['after']
assert proposal['changes'][0]['before'] == proposal['changes'][1]['before']
assert r'T+\max\{s,0\}' in proposal['changes'][0]['after']
assert r'S_r\Phi_s z' in proposal['changes'][0]['after']
assert r'\ s>0,' not in proposal['changes'][0]['after']
module_raw = paths['original_module'].read_bytes()
lines = module_raw.splitlines(keepends=True)
regions = []
for number, step in enumerate(candidate_lesson['units'][0]['steps'], 1):
    region = step['lean_source_region']
    raw = b''.join(lines[region['start_line'] - 1:region['end_line']])
    assert raw == step['lean'].encode('utf-8')
    assert digest(raw) == region['exact_code_raw_sha256']
    regions.append({'step': number, 'start_line': region['start_line'], 'end_line': region['end_line'], 'sha256': digest(raw), 'bytes': len(raw), 'exact_adjacent_Lean': True})

write('checks90.native.json', {
    'reviewer_id': REVIEWER,
    'all_supplied_raw_hashes_and_bytes_match': True,
    'exact_deltas': records,
    'same_after_formula_in_lesson_and_publication': True,
    'all_other_decoded_fields_and_raw_bytes_preserved': True,
    'statement_and_source_conditions_preserved': True,
    'publication_statement_equals_lesson_statement': True,
    'exact_adjacent_Lean_regions': regions,
    'append_definition_line_regions': [[76, 81], [173, 178], [218, 223]],
    'guarded_actual_identification_line_region': [299, 317],
    'statement_seal_and_publication_freeze': 'supplied originals hash-checked only and left unchanged',
    'neutral_decoder': 'not supplied in this clean packet; no decoder or prior blind/source/mathematical verdict was read or modified',
    'compilation_or_prior_semantic_verdict_used_as_proof': False,
    'Lean_build_performed': False,
    'canonical_mutation_performed': False
})

decision = {
    'decision': 'ACCEPT_EXACT_TWO_FIELD_EXPOSITION90_REPAIR',
    'reviewer_id': REVIEWER,
    'distinct_from_proposer77_root_formalizer_and_source_graph_creator87': True,
    'exact_proposal': info(paths['proposal']),
    'accepted_lesson_candidate': info(paths['candidate_0']),
    'accepted_publication_candidate': info(paths['candidate_1']),
    'accepted_pointers': pointers,
    'native_independent_findings': [
        'The supplied total append has domain Hist_n times real time and matches on the last record tag, not on positivity of s. Its live cumulative-time coordinate is T + Real.toNNReal(s), whose real value is T + max(s,0); its state coordinate uses the unclipped real harmonic flow Phi_s. The formal statement (76-81), proof-change statement (173-178) and local definition (218-223) agree.',
        'The original displayed live case is restricted to s>0, leaving live histories at s=0 and s<0 without a case even though the unchanged prose and Lean define a total map. The proposed removal of that side condition and replacement T+s by T+max(s,0) precisely fills this exposition gap.',
        'For s>0, max(s,0)=s, so the proposed formula reduces to the primary finite update T+s and reflection after Phi_s. The primary A.1 threshold construction has nonnegative waits, stops on infinity and A.7 uses strict positive ordered event times. The actual finite density support retains 0<s<d(h). Thus no negative-time source dynamics or unrestricted next-history law is introduced.',
        'At s=0 the live time stays T and the state is S_r(Phi_0(z)); at s<0 the live time again stays T while the state remains S_r(Phi_s(z)). These are exactly the already specified auxiliary totalizations. The proposed formula does not change Phi_s into Phi_max(s,0), insert a positivity branch, or change the stopped output.',
        'Fin.snoc preserves every old record and the paired lift keeps s itself. Both are unchanged in the displayed formula and literal definitions. The stopped case remains stopped for every real s.',
        'Each candidate file is exactly its supplied original raw file with one occurrence of the stated JSON-encoded formula string replaced. Only the two permitted pointers change, each by six bytes; statement, assumptions, source attribution, guards, boundaries, proof text and all embedded Lean remain identical. All six embedded BODY regions match the exact supplied module raw bytes.',
        'No current compilation, prior semantic/source verdict or neutral decoder verdict was used as mathematical proof. Seal and publication-freeze originals were hash-checked only. The overlay neither changes nor authorizes changes to those artifacts, Lean or the neutral decoder.'
    ],
    'required_repairs': [],
    'scope_limits': ['Independent acceptance covers only the exact two-field exposition repair.', 'No whole-theorem proof credit, source-fidelity admission, VERIFIED transition, main integration, purification, paper or Goal completion is granted.', 'Only the assigned independent review directory was written; no canonical application occurred.'],
    'primary_first_note': str(OUT / 'source-first90.native.json'),
    'frozen_before_return': True,
    'completed_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()
}
write('decision90.native.json', decision)

write('chronology90.native.json', {
    'reviewer_id': REVIEWER,
    'chronology_type': 'native observed tool sequence; exact times only where observed',
    'events': [
        {'order': 1, 'action': 'Read exact clean packet and verify its SHA256.'},
        {'order': 2, 'action': 'Hash primary, seven original/proposal inputs and two candidates without mathematical comparison. Directly read bounded pinned-primary fixed flow, threshold, finite update/stop and strict ordered-event support. Save .private. extracts and source-first note.', 'source_first_note_observed_utc': '2026-10-11T00:22:48.102309+00:00'},
        {'order': 3, 'action': 'Read proposal and compare literal module append definitions, real Phi argument and guarded actual recursion identification; no previous acceptance/source/blind verdicts or unlisted files opened.'},
        {'order': 4, 'action': 'Read original lesson statement/first step and proposed formulas; compare publication statement/formula. Recursively check exactly two permitted pointers, exact raw replacements and all six adjacent Lean regions.', 'checks_observed_utc': '2026-10-11T00:23:52.551547+00:00'},
        {'order': 5, 'action': 'Write native decision/checks/chronology and closed RAW manifest; freeze artifact bytes, validate closure and mark owned files read-only before return.'}
    ],
    'no_full_primary_copy': True,
    'long_primary_extracts_private': True,
    'no_canonical_or_independent_math90_mutations': True,
    'freeze_contract': 'After manifest finalization only read-only validation and file attribute changes are permitted; no review artifact bytes will change before return.',
    'finished_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()
})

artifacts = [info(path) for path in sorted(OUT.rglob('*')) if path.is_file() and path.name != 'closed-raw-manifest90.json']
write('closed-raw-manifest90.json', {
    'reviewer_id': REVIEWER,
    'algorithm': 'SHA256 of exact raw file bytes',
    'closure': 'All supplied input files and all produced artifact files are SHA256/byte identified. Full primary remains at its supplied pinned location; private bounded extracts are hashed. This manifest excludes only itself to avoid circular hashing; its digest and bytes are returned externally.',
    'inputs': inputs,
    'artifacts': artifacts,
    'excluded_self': str(OUT / 'closed-raw-manifest90.json'),
    'frozen': True
})
for name in ['decision90.native.json', 'checks90.native.json', 'chronology90.native.json', 'source-first90.native.json', 'closed-raw-manifest90.json']:
    print(json.dumps(info(OUT / name)))
