from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, sys

sys.dont_write_bytecode = True
REPO = Path('/Users/zhouhuanjian/ASTIS-GC')
ROOT = REPO / '.astis/semantic-neutral-20261110/src_62f8c4'
BASE = ROOT / 'frontier_closeout_20261110'
PUB, PRIVATE = BASE / 'public', BASE / 'private'
OLD = ROOT / 'sourcev_execution_20261110'
TARGET_REL = 'research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-fixed-spectrum-mode-gap.json'
TARGET = REPO / TARGET_REL
H = lambda b: hashlib.sha256(b).hexdigest()
D = lambda x: H(json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode())
stamp = lambda: datetime.now(timezone.utc).isoformat()

def write(path, value):
    with path.open('x', encoding='utf-8') as f:
        f.write(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def write_raw(path, raw):
    with path.open('xb') as f: f.write(raw)

assert not (PUB / 'frontier-closeout-result.json').exists(), 'Do not replay the closeout.'
assert H((OLD / 'public/execution-freeze.json').read_bytes()) == 'd92ee6952cf3ae3e40aacb720275df6bbcecf35c42eac59027e220ed3fef9059'
old_result = json.loads((OLD / 'public/normal-verification-execution-result.json').read_text())
assert old_result['actual_normal_transition_API_calls'] == 1 and old_result['after_state'] == 'VERIFIED'
assert old_result['preservation_pass']
old_contract = json.loads((OLD / 'public/original-evidence-contract.json').read_text())
original = json.loads((OLD / 'public/original-evidence.raw.json').read_text())
assert H((OLD / 'public/original-evidence.raw.json').read_bytes()) == old_contract['original_raw_sha256']
assert D(original) == old_contract['original_canonical_sha256']
assert json.loads((OLD / 'public/actual-own-ledger-append.raw.jsonl').read_text())['evidence'] == original

# Preserve the exact entire prior public execution tree; no old output is edited.
old_public_before = {str(p.relative_to(OLD / 'public')): H(p.read_bytes())
    for p in (OLD / 'public').rglob('*') if p.is_file()}
old_private_freeze_before = H((OLD / 'private/PRIVATE-freeze.json').read_bytes())
old_private_manifest_before = H((OLD / 'private/PRIVATE-output-file-manifest.json').read_bytes())
baseline = json.loads((OLD / 'private/after-snapshot.json').read_text())

# Reuse immutable old PRIVATE raw blobs by reference. New private snapshots contain
# the current raw hashes and foreign state values, never public state dumps.
snapshot_before = []
for row in baseline['paths']:
    raw = (REPO / row['path']).read_bytes()
    assert H(raw) == row['sha256'], 'Protected bytes changed before this separate closeout.'
    snapshot_before.append({**row, 'immutable_raw_blob_base': '../sourcev_execution_20261110/private'})
frontier_rows = [x for x in snapshot_before if x['path'].startswith('research-wiki/frontier-cells/')]
foreign_frontier_rows = [x for x in frontier_rows if x['path'] != TARGET_REL]
assert foreign_frontier_rows
before = {'schema': 1, 'observed_utc': stamp(), 'privacy': 'PRIVATE foreign before-state/raw-blob references; do not publish.',
    'paths': snapshot_before, 'foreign_advance_states': baseline['foreign_advance_states'],
    'foreign_advance_states_canonical_sha256': baseline['foreign_advance_states_canonical_sha256'],
    'foreign_frontier_paths': [x['path'] for x in foreign_frontier_rows],
    'old_private_raw_blob_freeze_sha256': old_private_freeze_before,
    'old_private_raw_blob_manifest_sha256': old_private_manifest_before}
write(PRIVATE / 'before-snapshot.json', before)

raw_before = TARGET.read_bytes(); own_before = json.loads(raw_before)
assert own_before['status'] == 'proved_locally'
assert own_before['owner_id'] == 'huanjian_gc_20261110_fixed_spectrum_mode_gap'
assert own_before['advance_id'] == 'ASTIS-SA-20261110-GaussianComplexityFixedSpectrumModeGap'
assert isinstance(own_before['evidence']['independent_verification'], str)
old_string = own_before['evidence']['independent_verification']
new_string = (
    'Independent frontier closeout by original verifier /root/source_reader_62f8c4 under unchanged owner '
    'huanjian_gc_20261110_fixed_spectrum_mode_gap. The bounded uniform finite mode/gap prerequisite and '
    'private actual diagonal-Gaussian Ex23 polynomial-bias component are independently verified. '
    'Accepted raw-first seven-slot/full producer/private Test/provider/source/exposition review: '
    'research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-mode-gap-semantic-evidence/'
    'exact-independent-source-review-application.json; original source phase3 freeze '
    '76cd70cf13096a71f2af28829608b046d5ca8179b2385e69e12c657df7eabeb0. '
    'Separate actual native producer/full Test/kernel and isolated static evidence is archived in '
    'independent-module-native-static-reader-8d91a6.lossless.tar.gz, freeze '
    '3e50cf4ff370eb3a43bb42557c6f8f3dc612f3db11bde66c5700e268dc354a42: checked at '
    'a2897bb1298d115070485dd271f71ea5db567b86, with five unchanged canonical parent objects explicitly reused. '
    'Normal PROVED_LOCAL-to-VERIFIED API call already completed exactly once; public-safe execution freeze '
    '.astis/semantic-neutral-20261110/src_62f8c4/sourcev_execution_20261110/public/execution-freeze.json '
    'SHA256 d92ee6952cf3ae3e40aacb720275df6bbcecf35c42eac59027e220ed3fef9059; exact original ledger append '
    'SHA256 a3d92da48b9edcde420449357f1fdca68793e7a94e1a68a366952794c033e8a3. '
    'Mathematical candidate886adb85034f7bcf4e26a24eb648d4adb879219b, independent native/source candidatea289, '
    'metadata carrier348f1f34ada0e9d4f46dfa1a4b1b983ab748bb62 retain identical Lean/Test/lesson/publication bytes; '
    'no fresh native at348 is claimed. This separate two-field frontier edit makes no advance API call and '
    'is not a post_integration/existing-VERIFIED release. All13 original evidence keys/values and exact '
    'raw/canonical/append outputs remain immutable; a later release may only add post_integration and must '
    'be performed by this original verifier. Earlier pending labels retained elsewhere in this cell are '
    'local/preproof-stage history and are superseded only for this accepted bounded independent verification. '
    'Eight author-side asymptotic intermediates remain sufficient-route variants, not exact emitted outputs. '
    'Concrete tau, shifted events/probabilities, rotated law, algorithm/oracle/TV/cost, main bounds/full source '
    'assembly, latest-main/STAB/global integration, shared site/source-index/graph/public browser delivery, '
    'publication/purification/Exposition Seal and whole-Goal acceptance remain outside this closeout.'
)
text = raw_before.decode()
assert text.count('"status": "proved_locally"') == 1
old_fragment = '"independent_verification": ' + json.dumps(old_string, ensure_ascii=False)
assert text.count(old_fragment) == 1
new_text = text.replace('"status": "proved_locally"', '"status": "independently_verified"', 1)
new_text = new_text.replace(old_fragment, '"independent_verification": ' + json.dumps(new_string, ensure_ascii=False), 1)
raw_after = new_text.encode(); own_after = json.loads(raw_after)
expected = json.loads(raw_before)
expected['status'] = 'independently_verified'
expected['evidence']['independent_verification'] = new_string
assert own_after == expected and isinstance(new_string, str) and new_string.strip()
assert own_after['owner_id'] == own_before['owner_id']
write_raw(PUB / 'own-frontier-before.raw.json', raw_before)
write_raw(PUB / 'own-frontier-after.raw.json', raw_after)
delta = [{'path': '/status', 'old': own_before['status'], 'new': own_after['status']},
    {'path': '/evidence/independent_verification', 'old': old_string, 'new': new_string}]
write(PUB / 'exact-field-delta.json', delta)
write(PUB / 'protocol-inspection.json', {
    'read': ['research-wiki/frontier-cells/README.md', 'tools/astis_frontier_cells.py'],
    'README_status_rule': 'proved_locally → independently_verified; independent verifier records verification evidence',
    'tool_entrypoints': ['check', 'summary'], 'mutating_frontier_API_present': False,
    'method': 'Authorized direct two-field JSON edit; atomic replace of ONLY the owned frontier file.',
    'independent_verification_field_type': 'nonempty string', 'full_gates_or_native_rerun': False})

# Sole canonical mutation in this closeout. The prepared temp is new, inside our
# own private output directory; no other canonical path is touched.
tmp = PRIVATE / 'prepared-owned-frontier-write.tmp'
with tmp.open('xb') as f:
    f.write(raw_after); f.flush(); os.fsync(f.fileno())
assert TARGET.read_bytes() == raw_before
os.replace(tmp, TARGET)
assert TARGET.read_bytes() == raw_after

changed = []
snapshot_after = []
for row in snapshot_before:
    raw = (REPO / row['path']).read_bytes(); sha = H(raw)
    if sha != row['sha256']: changed.append(row['path'])
    if row['path'] == TARGET_REL:
        blob = PRIVATE / 'own-frontier-after.raw.json'
        write_raw(blob, raw)
        snapshot_after.append({'path': row['path'], 'bytes': len(raw), 'sha256': sha, 'blob': blob.name})
    else:
        snapshot_after.append(row)
assert changed == [TARGET_REL]
old_public_after = {str(p.relative_to(OLD / 'public')): H(p.read_bytes())
    for p in (OLD / 'public').rglob('*') if p.is_file()}
assert old_public_before == old_public_after
assert H((OLD / 'private/PRIVATE-freeze.json').read_bytes()) == old_private_freeze_before
assert H((OLD / 'private/PRIVATE-output-file-manifest.json').read_bytes()) == old_private_manifest_before
assert H((OLD / 'public/original-evidence.raw.json').read_bytes()) == old_contract['original_raw_sha256']
assert D(json.loads((OLD / 'public/original-evidence.raw.json').read_text())) == old_contract['original_canonical_sha256']
after = {'schema': 1, 'observed_utc': stamp(), 'privacy': 'PRIVATE foreign after-state/raw-blob references; do not publish.',
    'paths': snapshot_after, 'foreign_advance_states': before['foreign_advance_states'],
    'foreign_advance_states_canonical_sha256': before['foreign_advance_states_canonical_sha256'],
    'foreign_frontier_paths': before['foreign_frontier_paths'], 'only_changed_path': TARGET_REL,
    'old_private_raw_blob_freeze_sha256': old_private_freeze_before,
    'old_private_raw_blob_manifest_sha256': old_private_manifest_before}
write(PRIVATE / 'after-snapshot.json', after)
write(PRIVATE / 'old-sourcev-public-before-after-hashes.json', {'before': old_public_before, 'after': old_public_after})
result = {'schema': 'separate-independent-owned-frontier-closeout-v1', 'observed_utc': stamp(),
    'verifier_id': '/root/source_reader_62f8c4', 'owner_id_unchanged': own_after['owner_id'],
    'only_canonical_path_changed': TARGET_REL, 'old_status': own_before['status'], 'new_status': own_after['status'],
    'old_frontier_raw_sha256': H(raw_before), 'new_frontier_raw_sha256': H(raw_after),
    'exact_field_delta_file': 'exact-field-delta.json', 'exact_field_delta_raw_sha256': H((PUB / 'exact-field-delta.json').read_bytes()),
    'changed_JSON_pointer_count': 2, 'independent_verification_is_nonempty_string': True,
    'normal_advance_API_calls_in_this_closeout': 0, 'total_original_normal_VERIFIED_API_calls_remains': 1,
    'frontier_mutation_API_calls': 0, 'frontier_method': 'authorized direct two-field atomic JSON update; validator has no mutating API',
    'not_existing_VERIFIED_or_post_integration_release': True,
    'original_13_evidence_values_unchanged': True,
    'original_raw_evidence_sha256': old_contract['original_raw_sha256'],
    'original_canonical_evidence_sha256': old_contract['original_canonical_sha256'],
    'old_sourcev_entire_public_output_tree_unchanged': True,
    'old_sourcev_public_output_file_count': len(old_public_before),
    'old_sourcev_private_freeze_and_manifest_unchanged': True,
    'all_ledger_bytes_unchanged': True, 'foreign_advance_state_count_unchanged': len(before['foreign_advance_states']),
    'foreign_advance_states_canonical_sha256': before['foreign_advance_states_canonical_sha256'],
    'foreign_frontier_bytes_and_states_unchanged': True, 'foreign_frontier_file_count': len(foreign_frontier_rows),
    'protected_file_count': len(snapshot_before),
    'nonempty_PBPS_protected_path_count': len(baseline['PBPS_protected_paths']),
    'nonempty_SPHMC_protected_path_count': len(baseline['SPHMC_protected_paths']),
    'private_before_snapshot_raw_sha256': H((PRIVATE / 'before-snapshot.json').read_bytes()),
    'private_after_snapshot_raw_sha256': H((PRIVATE / 'after-snapshot.json').read_bytes()),
    'foreign_raw_snapshots_publicly_exported': False,
    'proof_native_gates_static_site_browser_rerun': False, 'STAB_global_other_frontier_mutation': False,
    'future_original_evidence_contract_unchanged': 'Only original verifier may later add post_integration; preserve every original key/value/raw/canonical/append.',
    'remaining_boundaries': original['truth_boundary']}
write(PUB / 'frontier-closeout-result.json', result)
print(json.dumps({k: result[k] for k in ['only_canonical_path_changed', 'old_status', 'new_status',
    'old_frontier_raw_sha256', 'new_frontier_raw_sha256', 'normal_advance_API_calls_in_this_closeout',
    'changed_JSON_pointer_count', 'foreign_frontier_bytes_and_states_unchanged', 'original_13_evidence_values_unchanged']}, indent=2))
