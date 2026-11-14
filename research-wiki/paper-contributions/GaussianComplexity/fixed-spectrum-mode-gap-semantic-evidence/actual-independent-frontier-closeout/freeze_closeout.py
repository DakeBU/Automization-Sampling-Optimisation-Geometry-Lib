from pathlib import Path
from datetime import datetime, timezone
import hashlib, json

BASE = Path('/Users/zhouhuanjian/ASTIS-GC/.astis/semantic-neutral-20261110/src_62f8c4/frontier_closeout_20261110')
PUB, PRIVATE = BASE / 'public', BASE / 'private'
H = lambda b: hashlib.sha256(b).hexdigest()

def write(path, value):
    with path.open('x', encoding='utf-8') as f:
        f.write(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

r = json.loads((PUB / 'frontier-closeout-result.json').read_text())
assert r['normal_advance_API_calls_in_this_closeout'] == 0
assert r['total_original_normal_VERIFIED_API_calls_remains'] == 1
assert r['changed_JSON_pointer_count'] == 2
assert r['foreign_frontier_bytes_and_states_unchanged'] and r['all_ledger_bytes_unchanged']
assert r['original_13_evidence_values_unchanged'] and r['old_sourcev_entire_public_output_tree_unchanged']
assert H((PUB / 'own-frontier-before.raw.json').read_bytes()) == r['old_frontier_raw_sha256']
assert H((PUB / 'own-frontier-after.raw.json').read_bytes()) == r['new_frontier_raw_sha256']
assert Path('/Users/zhouhuanjian/ASTIS-GC', r['only_canonical_path_changed']).read_bytes() == (PUB / 'own-frontier-after.raw.json').read_bytes()
private_files = [{'file': str(p.relative_to(PRIVATE)), 'bytes': p.stat().st_size, 'sha256': H(p.read_bytes())}
    for p in sorted(PRIVATE.rglob('*')) if p.is_file()]
private_freeze = {'schema': 'PRIVATE-separate-frontier-closeout-snapshots-v1',
    'privacy': 'PRIVATE foreign state/raw-blob references. Do not publish or package these snapshots.',
    'files': private_files,
    'prior_immutable_private_raw_blob_freeze_sha256': '869a2f40af3eeca72df303688619136a9c848e6cb6276c35d9f2a822706bf69c',
    'original_private_blob_store_modified': False}
write(PRIVATE / 'PRIVATE-freeze.json', private_freeze)
private_sha = H((PRIVATE / 'PRIVATE-freeze.json').read_bytes())
files = [{'file': str(p.relative_to(PUB)), 'bytes': p.stat().st_size, 'sha256': H(p.read_bytes())}
    for p in sorted(PUB.rglob('*')) if p.is_file()]
manifest = {'schema': 'public-safe-frontier-closeout-output-file-manifest-v1', 'public_safe': True,
    'files': files, 'private_foreign_raw_snapshots_excluded': True,
    'private_snapshot_freeze_raw_sha256': private_sha,
    'only_canonical_path_changed': r['only_canonical_path_changed'],
    'old_frontier_raw_sha256': r['old_frontier_raw_sha256'], 'new_frontier_raw_sha256': r['new_frontier_raw_sha256'],
    'exact_two_field_delta_raw_sha256': r['exact_field_delta_raw_sha256']}
write(PUB / 'output-file-manifest.json', manifest)
freeze = {'schema': 'separate-independent-owned-frontier-closeout-freeze-v1',
    'created_utc': datetime.now(timezone.utc).isoformat(),
    'verifier_id': r['verifier_id'], 'owner_id_unchanged': r['owner_id_unchanged'],
    'only_canonical_path_changed': r['only_canonical_path_changed'],
    'old_status': r['old_status'], 'new_status': r['new_status'],
    'old_frontier_raw_sha256': r['old_frontier_raw_sha256'], 'new_frontier_raw_sha256': r['new_frontier_raw_sha256'],
    'exact_two_field_delta_raw_sha256': r['exact_field_delta_raw_sha256'],
    'execution_result_raw_sha256': H((PUB / 'frontier-closeout-result.json').read_bytes()),
    'output_file_manifest_raw_sha256': H((PUB / 'output-file-manifest.json').read_bytes()),
    'private_snapshot_freeze_raw_sha256': private_sha,
    'normal_advance_API_calls_in_this_closeout': 0, 'original_normal_VERIFIED_API_calls_total_unchanged': 1,
    'all_foreign_frontier_bytes_states_and_all_ledgers_unchanged': True,
    'original_13_evidence_values_and_old_sourceV_outputs_freeze_append_unchanged': True,
    'not_existing_VERIFIED_or_post_integration_release': True,
    'proof_native_gates_site_browser_or_global_STAB_mutation': False,
    'original_only_post_integration_future_release_contract_unchanged': True,
    'remaining_boundaries': r['remaining_boundaries']}
write(PUB / 'frontier-closeout-freeze.json', freeze)
with (PUB / 'SHA256SUMS').open('x') as f:
    for p in sorted(PUB.rglob('*')):
        if p.is_file() and p.name != 'SHA256SUMS':
            f.write(H(p.read_bytes()) + '  ' + str(p.relative_to(PUB)) + '\n')
print('FROZEN SEPARATE FRONTIER CLOSEOUT')
for name in ['own-frontier-before.raw.json', 'own-frontier-after.raw.json', 'exact-field-delta.json',
             'frontier-closeout-result.json', 'output-file-manifest.json', 'frontier-closeout-freeze.json', 'SHA256SUMS']:
    print(H((PUB / name).read_bytes()), name)
