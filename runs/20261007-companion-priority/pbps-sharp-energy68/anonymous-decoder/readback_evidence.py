import datetime
import hashlib
import json
import os
from pathlib import Path

BASE = Path(r'E:/Samplinglib/.astis/decoder-68')
OUT = BASE / 'independent'
SLOTS = ['objects', 'domains', 'quantifiers', 'assumptions', 'conclusion', 'scopes', 'constant_dependencies']

def sha(b):
    return hashlib.sha256(b).hexdigest()

def canon(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')

def read(name):
    return json.loads((OUT / name).read_bytes())

def save(name, value):
    (OUT / name).write_bytes((json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode('utf-8'))

manifest = read('raw_input_manifest.json')
for name,row in manifest['inputs'].items():
    path = BASE / name
    raw = path.read_bytes()
    assert sha(raw) == row['raw_sha256']
    assert len(raw) == row['bytes'] and path.stat().st_mtime_ns == row['mtime_ns']
    assert (OUT / row['raw_snapshot']).read_bytes() == raw
    assert (OUT / row['lf_snapshot']).read_bytes() == raw.replace(b'\r\n', b'\n')
assert (BASE / 'lease.json').read_bytes() == (BASE / 'initial-lease.raw.snapshot.json').read_bytes()
assert json.loads((BASE / 'lease.json').read_bytes())['status'] == 'OPEN'
run = read('final_run.json')
claimed_run = run.pop('run_sha256')
assert sha(canon(run)) == claimed_run
payload = read('reconstruction_payload.json')
assert payload['decoder_run_sha256'] == claimed_run
records = []
for packet_id, record in payload['reconstructions'].items():
    packet = json.loads((BASE / record['input_filename']).read_bytes())
    assert packet_id == packet['packet_id']
    assert record['lean_statement_literal'] == packet['lean']['statement']
    raw = (OUT / record['named_reconstruction_file']).read_bytes()
    assert raw == record['reconstructed_theorem_text'].encode('utf-8')
    assert sha(raw) == record['reconstructed_text_sha256']
    assert record['decoder_run_sha256'] == claimed_run
    assert all(record[slot].strip() and record['seven_slot_coverage'][slot]['status'] == 'covered' for slot in SLOTS)
    assert record['source_text_visible'] is False and record['source_identity_visible'] is False and record['compiler_started'] is False
    assert run['packet_records'][packet_id]['seven_slots'] == {slot: record[slot] for slot in SLOTS}
    assert run['packet_records'][packet_id]['clause_coverage'] == record['clause_coverage']
    records.append({'packet_id': packet_id, 'named_reconstruction_file': record['named_reconstruction_file'], 'raw_sha256': sha(raw), 'seven_slot_count': 7, 'clause_coverage_count': len(record['clause_coverage'])})
for name in ['terminal_build.json','terminal_finalizer.json']:
    t = read(name)
    assert t['actual_process_completed'] is True and t['exit_code'] == 0 and t['exit_status'] == 'EXIT0'
    assert isinstance(t['process_id'], int) and t['process_id'] > 0
for obj in [payload,run,read('lease.json')]:
    assert obj['source_text_visible'] is False and obj['source_identity_visible'] is False and obj['compiler_started'] is False
save('readback_results.json', {
    'status': 'PASS',
    'process_id': os.getpid(), 'parent_process_id': os.getppid(),
    'logical_run_sha256': claimed_run,
    'logical_run_removal_rule': 'ONLY top-level run_sha256 removed',
    'raw_input_manifest_sha256': sha((OUT / 'raw_input_manifest.json').read_bytes()),
    'reconstruction_payload_raw_sha256': sha((OUT / 'reconstruction_payload.json').read_bytes()),
    'records': records,
    'parent_lease_open_unchanged_raw_and_mtime': True,
    'snapshots_raw_and_crlf_to_lf_only_exact': True,
    'source_text_visible': False, 'source_identity_visible': False, 'compiler_started': False,
    'source_fidelity_verdict': 'not assessed',
    'verified_transition': False
})
save('readback_process.json', {
    'process_id': os.getpid(), 'parent_process_id': os.getppid(),
    'completed_work_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'action': 'fresh readback of all allowed input snapshots, logical run, complete reconstructions and actual completed stage receipts',
    'compiler_started': False
})
print(json.dumps({'status': 'READBACK_DONE', 'process_id': os.getpid(), 'parent_process_id': os.getppid(), 'logical_run_sha256': claimed_run}, sort_keys=True))
