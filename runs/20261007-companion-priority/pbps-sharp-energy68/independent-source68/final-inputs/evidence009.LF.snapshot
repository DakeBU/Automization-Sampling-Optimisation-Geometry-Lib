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

def save(name, value):
    (OUT / name).write_bytes((json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode('utf-8'))

def read(name):
    return json.loads((OUT / name).read_bytes())

manifest = read('raw_input_manifest.json')
input_checks = []
for name, row in manifest['inputs'].items():
    original = BASE / name
    raw = original.read_bytes()
    assert sha(raw) == row['raw_sha256'] and len(raw) == row['bytes']
    assert original.stat().st_mtime_ns == row['mtime_ns']
    assert (OUT / row['raw_snapshot']).read_bytes() == raw
    assert (OUT / row['lf_snapshot']).read_bytes() == raw.replace(b'\r\n', b'\n')
    input_checks.append({'input': name, 'raw_exact': True, 'crlf_to_lf_only_exact': True, 'original_mtime_unchanged': True})
assert (BASE / 'lease.json').read_bytes() == (BASE / 'initial-lease.raw.snapshot.json').read_bytes()
assert json.loads((BASE / 'lease.json').read_bytes())['status'] == 'OPEN'
terminal = read('terminal_build.json')
assert terminal['actual_process_completed'] is True and terminal['exit_code'] == 0
payload = read('reconstruction_payload.json')
packet_records = {}
for packet_id, record in payload['reconstructions'].items():
    packet = json.loads((BASE / record['input_filename']).read_bytes())
    assert packet_id == packet['packet_id']
    assert record['lean_statement_literal'] == packet['lean']['statement']
    assert record['lean_statement_literal'] in record['reconstructed_theorem_text']
    raw_text = record['reconstructed_theorem_text'].encode('utf-8')
    assert sha(raw_text) == record['reconstructed_text_sha256']
    assert (OUT / record['named_reconstruction_file']).read_bytes() == raw_text
    assert list(record['seven_slot_coverage'].keys()) == sorted(SLOTS)
    assert all(isinstance(record[slot], str) and record[slot].strip() for slot in SLOTS)
    assert all(record['seven_slot_coverage'][slot]['status'] == 'covered' for slot in SLOTS)
    assert all(clause['status'] == 'retained' for clause in record['clause_coverage'])
    assert record['source_text_visible'] is False
    assert record['source_identity_visible'] is False
    assert record['compiler_started'] is False
    packet_records[packet_id] = {
        'packet_filename': record['input_filename'],
        'statement_sha256': record['lean_statement_sha256'],
        'reconstruction_file': record['named_reconstruction_file'],
        'reconstruction_raw_sha256': record['reconstructed_text_sha256'],
        'seven_slots': {slot: record[slot] for slot in SLOTS},
        'clause_coverage': record['clause_coverage']
    }
run = {
    'schema_version': 1,
    'task': 'independent-source-blind-semantic-reconstruction',
    'decoder': payload['decoder'],
    'allowed_input_count': 4,
    'allowed_inputs': sorted(manifest['inputs']),
    'packet_count': len(packet_records),
    'packet_records': packet_records,
    'raw_input_manifest_sha256': sha((OUT / 'raw_input_manifest.json').read_bytes()),
    'finite_pin_mappings_sha256': sha((OUT / 'finite_pin_mappings.json').read_bytes()),
    'actual_build_terminal_receipt_sha256': sha((OUT / 'terminal_build.json').read_bytes()),
    'reconstruction_payload_path': 'reconstruction_payload.json',
    'source_text_visible': False,
    'source_identity_visible': False,
    'compiler_started': False,
    'hash_rule': 'SHA256 of UTF-8 JSON with ensure_ascii=false, sort_keys=true, separators=(comma,colon), after removing ONLY the top-level run_sha256 key; no other field is removed or normalized.',
    'parent_lease_preserved_open': True,
    'semantic_scope': 'Supplied neutral Lean statements and approved definition contexts only; no source comparison or proof verification.',
    'finalizer_process_id': os.getpid(),
    'finalizer_parent_process_id': os.getppid()
}
run_hash = sha(canon(run))
run['run_sha256'] = run_hash
save('final_run.json', run)
payload['decoder_run_sha256'] = run_hash
for record in payload['reconstructions'].values():
    record['decoder_run_sha256'] = run_hash
save('reconstruction_payload.json', payload)
read_run = read('final_run.json')
found = read_run.pop('run_sha256')
assert found == run_hash == sha(canon(read_run))
assert read('reconstruction_payload.json')['decoder_run_sha256'] == run_hash
save('finalizer_results.json', {
    'status': 'PASS',
    'logical_run_sha256': run_hash,
    'logical_run_rule_removes_only_top_run_sha256': True,
    'packet_count': len(packet_records),
    'seven_slots_per_packet_checked': 7,
    'complete_literal_statements_retained': True,
    'named_text_raw_bytes_checked': True,
    'all_input_checks': input_checks,
    'parent_lease_open_and_raw_unchanged': True,
    'source_text_visible': False,
    'source_identity_visible': False,
    'compiler_started': False,
    'remaining_uncertainty': 'Statement reconstruction only; no source fidelity verdict, independent proof, compiler result, or VERIFIED transition.'
})
save('finalizer_process.json', {
    'process_id': os.getpid(), 'parent_process_id': os.getppid(),
    'completed_work_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'action': 'finalize logical run, bind decoder run hash, verify exact bytes and seven-slot coverage',
    'compiler_started': False
})
print(json.dumps({'status': 'FINALIZER_DONE', 'process_id': os.getpid(), 'parent_process_id': os.getppid(), 'run_sha256': run_hash}, sort_keys=True))
