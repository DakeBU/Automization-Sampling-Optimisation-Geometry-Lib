from pathlib import Path
from datetime import datetime, timezone
import hashlib, json

BASE = Path('/Users/zhouhuanjian/ASTIS-GC/.astis/semantic-neutral-20261110/src_62f8c4/sourcev_execution_20261110')
PUB, PRIVATE = BASE / 'public', BASE / 'private'
H = lambda b: hashlib.sha256(b).hexdigest()
D = lambda x: H(json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode())

def write_exclusive(path, value):
    with path.open('x', encoding='utf-8') as f:
        f.write(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

result = json.loads((PUB / 'normal-verification-execution-result.json').read_text())
contract = json.loads((PUB / 'original-evidence-contract.json').read_text())
original = json.loads((PUB / 'original-evidence.raw.json').read_text())
assert H((PUB / 'original-evidence.raw.json').read_bytes()) == contract['original_raw_sha256']
assert H((PUB / 'original-evidence.canonical.json').read_bytes()) == contract['original_canonical_sha256'] == D(original)
assert result['actual_normal_transition_API_calls'] == 1 and result['API_returned_successfully'] and result['preservation_pass']
append_raw = (PUB / 'actual-own-ledger-append.raw.jsonl').read_bytes()
append = json.loads(append_raw)
assert append['evidence'] == original
assert H(append_raw) == result['actual_append_raw_sha256']
journal = [json.loads(x) for x in (PUB / 'normal-api-call-journal.jsonl').read_text().splitlines()]
assert sum(x['event'] == 'entering-single-normal-transition-API-call' for x in journal) == 1
assert sum(x['event'] == 'single-normal-transition-API-returned-successfully' for x in journal) == 1
binding = {'schema': 'immutable-original-evidence-and-append-binding-v1',
    'original_raw_evidence_sha256': contract['original_raw_sha256'],
    'original_canonical_evidence_sha256': contract['original_canonical_sha256'],
    'original_contract_raw_sha256': H((PUB / 'original-evidence-contract.json').read_bytes()),
    'original_top_level_keys': contract['original_top_level_keys'], 'original_top_level_key_count': 13,
    'actual_append_raw_sha256': H(append_raw), 'actual_append_record_canonical_sha256': D(append),
    'actual_api_call_count': 1, 'all_original_keys_and_values_match_actual_append': True,
    'future_release_only_added_key': 'post_integration',
    'future_release_actor_required': '/root/source_reader_62f8c4',
    'future_extension_check': "set(later)==set(original)|{'post_integration'} and all(later[k]==original[k] for k in original)",
    'future_extension_original_canonical_digest_check': "canonical_sha256({k:later[k] for k in original}) == '9b6b102bd38e87dbd3864dafa89c57d9026c22d40e5cc60df4cc834cc455275b'",
    'raw_original_and_exact_append_must_also_be_preserved': True}
write_exclusive(PUB / 'original-evidence-contract-binding.json', binding)

# Private foreign raw content is frozen separately and never enters public file manifests.
private_files = []
for path in sorted(x for x in PRIVATE.rglob('*') if x.is_file()):
    raw = path.read_bytes(); sha = H(raw)
    if path.parent.name == 'blobs': assert path.stem == sha
    private_files.append({'file': str(path.relative_to(PRIVATE)), 'bytes': len(raw), 'sha256': sha})
private_manifest = {'schema': 'PRIVATE-foreign-raw-before-after-snapshot-manifest-v1',
    'privacy': 'PRIVATE. Do not publish, package, source-index or place in a public evidence archive.',
    'files': private_files, 'file_count': len(private_files),
    'raw_before_snapshot_sha256': result['private_before_snapshot_raw_sha256'],
    'raw_after_snapshot_sha256': result['private_after_snapshot_raw_sha256'],
    'public_safe_execution_result_sha256': H((PUB / 'normal-verification-execution-result.json').read_bytes())}
write_exclusive(PRIVATE / 'PRIVATE-output-file-manifest.json', private_manifest)
private_freeze = {'schema': 'PRIVATE-snapshot-freeze-v1',
    'created_utc': datetime.now(timezone.utc).isoformat(),
    'privacy': 'PRIVATE foreign raw snapshots; public receipts carry only this digest and aggregate preservation facts.',
    'private_output_manifest_raw_sha256': H((PRIVATE / 'PRIVATE-output-file-manifest.json').read_bytes()),
    'private_file_count_before_manifests': len(private_files),
    'foreign_states_unchanged': True, 'frontier_and_protected_bytes_unchanged': True,
    'normal_api_calls': 1}
write_exclusive(PRIVATE / 'PRIVATE-freeze.json', private_freeze)
private_freeze_sha = H((PRIVATE / 'PRIVATE-freeze.json').read_bytes())

public_files = []
for path in sorted(x for x in PUB.rglob('*') if x.is_file()):
    raw = path.read_bytes()
    public_files.append({'file': str(path.relative_to(PUB)), 'bytes': len(raw), 'sha256': H(raw)})
manifest = {'schema': 'public-safe-normal-verification-output-file-manifest-v1',
    'public_safe': True, 'files': public_files,
    'private_raw_snapshots_excluded': True, 'private_snapshot_freeze_raw_sha256': private_freeze_sha,
    'actual_normal_transition_API_calls': 1, 'actual_launcher_exit_code': 0,
    'original_raw_evidence_sha256': contract['original_raw_sha256'],
    'original_canonical_evidence_sha256': contract['original_canonical_sha256'],
    'exact_actual_append_raw_sha256': result['actual_append_raw_sha256']}
write_exclusive(PUB / 'output-file-manifest.json', manifest)
freeze = {'schema': 'original-independent-normal-VERIFIED-execution-freeze-v1',
    'created_utc': datetime.now(timezone.utc).isoformat(),
    'advance_id': result['advance_id'], 'verifier_id': result['verifier_id'],
    'owner_id': 'huanjian_gc_20261110_fixed_spectrum_mode_gap',
    'from_state': 'PROVED_LOCAL', 'to_state': 'VERIFIED',
    'actual_normal_transition_API_calls': 1, 'actual_launcher_exit_code': 0,
    'output_file_manifest_raw_sha256': H((PUB / 'output-file-manifest.json').read_bytes()),
    'execution_result_raw_sha256': H((PUB / 'normal-verification-execution-result.json').read_bytes()),
    'original_evidence_contract_binding_raw_sha256': H((PUB / 'original-evidence-contract-binding.json').read_bytes()),
    'original_raw_evidence_sha256': contract['original_raw_sha256'],
    'original_canonical_evidence_sha256': contract['original_canonical_sha256'],
    'actual_append_raw_sha256': result['actual_append_raw_sha256'],
    'private_snapshot_freeze_raw_sha256': private_freeze_sha,
    'foreign_and_frontier_and_PBPS_SPHMC_preservation_pass': True,
    'foreign_state_count': 292, 'protected_file_count': 90428,
    'nonempty_PBPS_protected_path_count': 88823, 'nonempty_SPHMC_protected_path_count': 594,
    'native_and_source_checked_commit': 'a2897bb1298d115070485dd271f71ea5db567b86',
    'metadata_evidence_carrier_commit': '348f1f34ada0e9d4f46dfa1a4b1b983ab748bb62',
    'fresh_native_at_carrier_claimed': False, 'proof_native_static_site_browser_commands_rerun': False,
    'STAB_or_global_or_other_cell_mutation': False,
    'remaining_boundaries': result['remaining_global_site_public_purification_whole_Goal_boundaries'],
    'later_existing_V_release_rule': 'Only original verifier /root/source_reader_62f8c4 may later add post_integration; every original evidence key/value and exact raw/canonical original files and append must be retained.'}
write_exclusive(PUB / 'execution-freeze.json', freeze)
all_public = sorted(x for x in PUB.rglob('*') if x.is_file())
with (PUB / 'SHA256SUMS').open('x') as f:
    f.write(''.join(H(x.read_bytes()) + '  ' + str(x.relative_to(PUB)) + '\n' for x in all_public))
print('FROZEN PUBLIC-SAFE EXECUTION; PRIVATE RAW SNAPSHOTS EXCLUDED')
for name in ['original-evidence.raw.json', 'original-evidence.canonical.json', 'actual-own-ledger-append.raw.jsonl',
             'original-evidence-contract-binding.json', 'normal-verification-execution-result.json',
             'output-file-manifest.json', 'execution-freeze.json', 'SHA256SUMS']:
    print(H((PUB / name).read_bytes()), name)
print('PRIVATE freeze digest only', private_freeze_sha)
