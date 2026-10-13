import datetime
import hashlib
import json
import os
from pathlib import Path

BASE = Path(r'E:/Samplinglib/.astis/decoder-68')
OUT = BASE / 'independent'

def sha(b):
    return hashlib.sha256(b).hexdigest()

def canon(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')

def read(name):
    return json.loads((OUT / name).read_bytes())

def save(name, value):
    (OUT / name).write_bytes((json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode('utf-8'))

def rows(names):
    result = []
    for name in sorted(names):
        path = OUT / name
        raw = path.read_bytes()
        st = path.stat()
        result.append({'path': name, 'bytes': len(raw), 'raw_sha256': sha(raw), 'mtime_ns': st.st_mtime_ns})
    return result

def exact_readback(records):
    for row in records:
        path = OUT / row['path']
        raw = path.read_bytes()
        assert len(raw) == row['bytes'] and sha(raw) == row['raw_sha256']
        assert path.stat().st_mtime_ns == row['mtime_ns']

base_names = [
    'build_evidence.py', 'finalize_evidence.py', 'readback_evidence.py', 'close_evidence.py',
    'raw_input_manifest.json', 'finite_pin_mappings.json', 'reconstruction_payload.json',
    'build_process.json', 'terminal_build.json', 'final_run.json',
    'finalizer_results.json', 'finalizer_process.json', 'terminal_finalizer.json',
    'readback_results.json', 'readback_process.json', 'terminal_readback.json',
    'reconstructions/packet0.complete-reconstruction.txt',
    'reconstructions/packet1.complete-reconstruction.txt',
]
for name in ['packet0.json','packet1.json','lease.json','initial-lease.raw.snapshot.json']:
    base_names.extend(['snapshots/' + name + '.raw.snapshot', 'snapshots/' + name + '.lf.snapshot'])

assert read('lease.json')['status'] == 'OPEN'
assert read('finalizer_results.json')['status'] == 'PASS'
assert read('readback_results.json')['status'] == 'PASS'
terminals = []
for name in ['terminal_build.json','terminal_finalizer.json','terminal_readback.json']:
    t = read(name)
    assert t['actual_process_completed'] is True and t['exit_code'] == 0 and t['exit_status'] == 'EXIT0'
    assert t['process_id'] > 0 and t['parent_process_id'] == t['shell_process_id']
    terminals.append({'receipt_file': name, 'receipt_raw_sha256': sha((OUT / name).read_bytes()), **t})
save('terminal_manifest.json', {
    'completed_stage_count': len(terminals), 'actual_completed_stage_receipts': terminals,
    'final_closing_process_id': os.getpid(), 'final_closing_parent_process_id': os.getppid(),
    'final_closing_exit_evidence_location': 'Authoritative exec_command return and stdout; no owned file is written after the CLOSED_LAST lease.',
    'compiler_started': False
})
self_rows = rows(base_names + ['terminal_manifest.json'])
exact_readback(self_rows)
save('self_manifest.json', {
    'schema_version': 1, 'finite_file_count': len(self_rows), 'files': self_rows,
    'finite_rows_sha256': sha(canon(self_rows)),
    'exclusions': ['self_manifest.json','closure_readback_results.json','closure_manifest.json','lease.json'],
    'exclusion_reason': 'No cyclic self-hashes; these manifest and lease bytes are bound by the next manifest and final lease.',
    'source_text_visible': False, 'source_identity_visible': False, 'compiler_started': False
})
manifest = read('raw_input_manifest.json')
for name,row in manifest['inputs'].items():
    path = BASE / name
    raw = path.read_bytes()
    assert sha(raw) == row['raw_sha256'] and len(raw) == row['bytes']
    assert path.stat().st_mtime_ns == row['mtime_ns']
assert (BASE / 'lease.json').read_bytes() == (BASE / 'initial-lease.raw.snapshot.json').read_bytes()
assert json.loads((BASE / 'lease.json').read_bytes())['status'] == 'OPEN'
run = read('final_run.json')
logical = dict(run)
logical.pop('run_sha256')
assert sha(canon(logical)) == run['run_sha256']
payload = read('reconstruction_payload.json')
assert payload['decoder_run_sha256'] == run['run_sha256']
assert all(obj['source_text_visible'] is False and obj['source_identity_visible'] is False and obj['compiler_started'] is False for obj in [run,payload,read('lease.json')])
save('closure_readback_results.json', {
    'status': 'PASS', 'process_id': os.getpid(), 'parent_process_id': os.getppid(),
    'self_manifest_raw_sha256': sha((OUT / 'self_manifest.json').read_bytes()),
    'self_manifest_rows_count': len(self_rows), 'self_manifest_rows_exact_hash_size_mtime_readback': True,
    'parent_lease_open_unchanged_raw_and_mtime': True,
    'logical_run_sha256_verified_removing_only_top_run_sha256': run['run_sha256'],
    'source_text_visible': False, 'source_identity_visible': False, 'compiler_started': False,
    'remaining_uncertainty': 'Semantic reconstruction from supplied statements/context only; source fidelity and independent proof validity unassessed.'
})
closure_names = base_names + ['terminal_manifest.json','self_manifest.json','closure_readback_results.json']
closure_rows = rows(closure_names)
exact_readback(closure_rows)
save('closure_manifest.json', {
    'schema_version': 1, 'finite_file_count': len(closure_rows), 'files': closure_rows,
    'finite_rows_sha256': sha(canon(closure_rows)),
    'normalization_for_rows_hash': 'UTF-8 JSON list; ensure_ascii=false; sort_keys=true; separators=(comma,colon). File hashes use exact RAW bytes. mtimes are integer nanoseconds.',
    'excluded_self': 'closure_manifest.json', 'excluded_mutable_final_lease': 'lease.json',
    'closure_manifest_itself_bound_by_final_lease': True
})

# This readback is the final finite readback before the last owned write.
final_names = closure_names + ['closure_manifest.json']
final_rows = rows(final_names)
actual_names = sorted(str(p.relative_to(OUT)).replace('\\','/') for p in OUT.rglob('*') if p.is_file())
assert actual_names == sorted(final_names + ['lease.json'])
exact_readback(final_rows)
assert read('closure_manifest.json')['files'] == closure_rows
for name,row in manifest['inputs'].items():
    path = BASE / name
    raw = path.read_bytes()
    assert sha(raw) == row['raw_sha256'] and len(raw) == row['bytes']
    assert path.stat().st_mtime_ns == row['mtime_ns']
assert json.loads((BASE / 'lease.json').read_bytes())['status'] == 'OPEN'
assert (BASE / 'lease.json').read_bytes() == (BASE / 'initial-lease.raw.snapshot.json').read_bytes()
closure_hash = sha(canon(final_rows))
lease = {
    'status': 'CLOSED_LAST',
    'allowed_inputs': ['packet0.json','packet1.json','lease.json','initial-lease.raw.snapshot.json'],
    'source_text_visible': False, 'source_identity_visible': False, 'compiler_started': False,
    'parent_lease_open_and_unchanged': True,
    'parent_lease_raw_sha256': manifest['inputs']['lease.json']['raw_sha256'],
    'initial_parent_lease_raw_sha256': manifest['inputs']['initial-lease.raw.snapshot.json']['raw_sha256'],
    'whole_logical_run_sha256': run['run_sha256'],
    'reconstruction_payload_raw_sha256': sha((OUT / 'reconstruction_payload.json').read_bytes()),
    'named_reconstructions': {pid: {'path': rec['named_reconstruction_file'], 'raw_sha256': rec['reconstructed_text_sha256']} for pid,rec in payload['reconstructions'].items()},
    'raw_input_manifest_raw_sha256': sha((OUT / 'raw_input_manifest.json').read_bytes()),
    'closure_manifest_raw_sha256': sha((OUT / 'closure_manifest.json').read_bytes()),
    'closure_manifest_file_count_excluding_itself_and_lease': len(closure_rows),
    'closure_count': len(final_rows),
    'closure_count_scope': 'All immutable owned files including closure_manifest.json; excludes final lease.json only.',
    'closure_sha256': closure_hash,
    'closure_hash_rule': 'SHA256 canonical JSON list of sorted path,bytes,raw_sha256,mtime_ns rows; includes closure_manifest.json and excludes lease.json only.',
    'immutable_file_rows': final_rows,
    'total_owned_file_count_including_lease': len(final_rows) + 1,
    'exact_finite_count_hash_size_mtime_readback_before_close': True,
    'actual_completed_terminal_pids': [t['process_id'] for t in terminals],
    'actual_completed_terminal_shell_pids': [t['shell_process_id'] for t in terminals],
    'actual_completed_terminal_exit_statuses': [t['exit_status'] for t in terminals],
    'last_writer_process_id': os.getpid(), 'last_writer_parent_process_id': os.getppid(),
    'last_writer_exit_evidence': 'Authoritative exec_command stdout/exit code; no owned writes follow this lease.',
    'closed_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'last_owned_write': 'lease.json',
    'source_fidelity_verdict': 'not assessed', 'verified_transition': False,
    'remaining_uncertainty': 'No source text/identity or compiler was consulted. Reconstruction does not certify source fidelity, proof correctness, or VERIFIED.'
}
save('lease.json', lease)

# Read-only after the CLOSED_LAST write: emit hashes to the terminal only.
lease_raw = (OUT / 'lease.json').read_bytes()
assert json.loads(lease_raw)['status'] == 'CLOSED_LAST'
print(json.dumps({
    'status': 'CLOSED_LAST',
    'last_writer_process_id': os.getpid(), 'last_writer_parent_process_id': os.getppid(),
    'whole_logical_run_sha256': run['run_sha256'],
    'complete_reconstruction_payload_raw_sha256': lease['reconstruction_payload_raw_sha256'],
    'named_reconstructions': lease['named_reconstructions'],
    'separate_raw_input_manifest_sha256': lease['raw_input_manifest_raw_sha256'],
    'closure_count': len(final_rows), 'closure_sha256': closure_hash,
    'closure_manifest_raw_sha256': lease['closure_manifest_raw_sha256'],
    'lease_raw_sha256': sha(lease_raw),
    'actual_completed_terminal_pids': lease['actual_completed_terminal_pids'],
    'actual_completed_terminal_exit_statuses': lease['actual_completed_terminal_exit_statuses'],
    'parent_lease_status': 'OPEN', 'parent_lease_unchanged': True,
    'source_text_visible': False, 'source_identity_visible': False, 'compiler_started': False,
    'exit_evidence': 'Actual closing process exit status is supplied by exec_command after this stdout.'
}, sort_keys=True))
