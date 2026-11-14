from pathlib import Path
from datetime import datetime, timezone
import gzip, hashlib, inspect, json, os, subprocess, sys, tarfile

sys.dont_write_bytecode = True
REPO = Path('/Users/zhouhuanjian/ASTIS-GC')
sys.path.insert(0, str(REPO))
from tools.astis_advance import transition_advance, _replay_advances

BASE = REPO / '.astis/semantic-neutral-20261110/src_62f8c4/sourcev_execution_20261110'
PUB, PRIVATE = BASE / 'public', BASE / 'private'
OUT = PUB / 'preflight'
OUT.mkdir(exist_ok=False)
E = REPO / 'research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-mode-gap-semantic-evidence'
N = REPO / '.astis/semantic-neutral-20261110/module_8d91a6'
ID = 'ASTIS-SA-20261110-GaussianComplexityFixedSpectrumModeGap'
OWNER = 'huanjian_gc_20261110_fixed_spectrum_mode_gap'
VERIFIER = '/root/source_reader_62f8c4'
DECL = 'AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumModeGap.eventual_source_query_mode_gap'
H = lambda b: hashlib.sha256(b).hexdigest()
D = lambda x: H(json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode())

def write(name, value):
    path = OUT / name
    with path.open('x', encoding='utf-8') as f:
        f.write(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def copy(name, source):
    with (OUT / name).open('xb') as f:
        f.write(source.read_bytes())

assert Path(inspect.getfile(transition_advance)).resolve() == REPO / 'tools/astis_advance.py'
assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=REPO).decode().strip() == '348f1f34ada0e9d4f46dfa1a4b1b983ab748bb62'
application = json.loads((E / 'exact-independent-source-review-application.json').read_text())
audit_path = REPO / 'research-wiki/semantic-roundtrip/audits/huanjian-fixed-spectrum-mode-gap.json'
audit = json.loads(audit_path.read_text())
proposal_path = REPO / '.astis/semantic-neutral-20261110/src_62f8c4/phase3/canonical_audit_field_proposal.json'
proposal = json.loads(proposal_path.read_text())
assert all(audit[k] == v for k, v in proposal.items())
assert H(audit_path.read_bytes()) == application['audit_sha256_after']
assert audit['state'] == 'source-reviewed' and audit['source_review']['state'] == 'accepted'
assert audit['source_review']['reviewer'] == VERIFIER
assert audit['publication_binding_sha256'] == '17f6c8d330b1ce2529a881860aa6175821cfeb6dd8b69566c44ac720f8104e18'
copy('accepted-own-audit.raw.json', audit_path)
copy('accepted-source-review-application.json', E / 'exact-independent-source-review-application.json')

layers = []
for path in ['AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumModeGap.lean',
             'Tests/GaussianComplexityFixedSpectrumModeGap.lean',
             'website/content/declaration_lessons/huanjian-fixed-spectrum-mode-gap.json',
             'website/content/publications/huanjian-fixed-spectrum-mode-gap.json']:
    raw = (REPO / path).read_bytes()
    for commit in ['886adb85034f7bcf4e26a24eb648d4adb879219b', 'a2897bb1298d115070485dd271f71ea5db567b86', '348f1f34ada0e9d4f46dfa1a4b1b983ab748bb62']:
        assert subprocess.check_output(['git', 'show', commit + ':' + path], cwd=REPO) == raw
    layers.append({'path': path, 'sha256': H(raw), 'identical_at_math_native_source_and_carrier_layers': True})
write('checked-layer-identities.json', layers)

gate_index = json.loads((E / 'accepted-review-checks/actual-working-layer-gates.json').read_text())
gates = []
for row in gate_index['checks']:
    receipt_path = E / 'accepted-review-checks' / row['receipt']
    raw = receipt_path.read_bytes()
    receipt = json.loads(raw)
    assert H(raw) == row['receipt_sha256'] and receipt['exit_code'] == row['exit_code'] == 0
    gz_path = receipt_path.with_name(row['receipt'].replace('.receipt.json', '.log.gz'))
    decoded = gzip.decompress(gz_path.read_bytes())
    assert H(gz_path.read_bytes()) == row['lossless_gzip_sha256']
    assert H(decoded) == row['original_log_sha256']
    gates.append({**row, 'receipt_path': str(receipt_path.relative_to(REPO)), 'original_log_verified': True})
    print('ACCEPTED_RECEIPT', row['receipt'], 'exit=0')
    print(decoded.decode())
write('accepted-metadata-gates.json', {'scope': gate_index['scope'], 'rows': gates,
    'actual_metadata_gate_count': 4, 'application_receipt_is_separate': True, 'rerun_here': False})

freeze_raw = (N / 'freeze.json').read_bytes()
assert H(freeze_raw) == application['native_module_freeze_sha256'] == '3e50cf4ff370eb3a43bb42557c6f8f3dc612f3db11bde66c5700e268dc354a42'
native_freeze = json.loads(freeze_raw)
for row in native_freeze['artifacts']:
    raw = (N / row['path']).read_bytes()
    assert H(raw) == row['sha256'] and len(raw) == row['bytes']
native_receipts = []
for name in ['isolated-producer', 'isolated-Test', 'isolated-kernel-audit', 'static-lesson-v2']:
    rp = N / (name + '.receipt.json')
    receipt = json.loads(rp.read_text())
    assert receipt['exit_code'] == 0
    # The corrected static-v2 receipt binds the existing static stdout filename.
    logstem = 'static-lesson' if name == 'static-lesson-v2' else name
    assert H((N / (logstem + '.stdout.log')).read_bytes()) == receipt['stdout_sha256']
    assert H((N / (logstem + '.stderr.log')).read_bytes()) == receipt['stderr_sha256']
    native_receipts.append({'path': str(rp.relative_to(REPO)), 'raw_sha256': H(rp.read_bytes()), **receipt})
reuse = json.loads((N / 'canonical-reuse.json').read_text())
assert len(reuse['objects']) == 5 and all(not x['fresh_run_claim'] and x['historical_exit_code'] == 0 for x in reuse['objects'])
for row in reuse['objects']:
    assert H((REPO / row['source']).read_bytes()) == row['current_source_sha256']
copy('native-freeze.json', N / 'freeze.json')
copy('native-kernel-inventory.json', N / 'kernel-inventory.json')
copy('native-report.json', N / 'check-report.json')
copy('native-canonical-reuse.json', N / 'canonical-reuse.json')
write('native-actual-receipts.json', {'checked_commit': native_freeze['candidate_commit'], 'receipts': native_receipts,
    'fresh_runs_by_this_verifier': False, 'fresh_native_at_carrier_claimed': False,
    'canonical_parent_objects_reused_not_fresh': 5})

archive_rows = []
for key, local_base in [('source_archive', REPO / '.astis/semantic-neutral-20261110/src_62f8c4/phase3'), ('native_module_archive', N)]:
    row = application[key]
    raw = (REPO / row['path']).read_bytes()
    assert H(raw) == row['sha256'] and len(raw) == row['bytes']
    with tarfile.open(REPO / row['path'], 'r:gz') as archive:
        members = [m for m in archive.getmembers() if m.isfile()]
        for m in members:
            assert not Path(m.name).is_absolute() and '..' not in Path(m.name).parts
            assert archive.extractfile(m).read() == (local_base / m.name).read_bytes()
    archive_rows.append({**row, 'files_exactly_equal_to_original_freeze': len(members)})
write('archive-losslessness.json', archive_rows)

ledger_path = REPO / 'runs/substantive_advances.jsonl'
ledger_raw = ledger_path.read_bytes()
assert ledger_raw.endswith(b'\n')
records = [json.loads(line) for line in ledger_raw.splitlines() if line.strip()]
state = _replay_advances(records)
own = state[ID]
assert own['state'] == 'PROVED_LOCAL' and own['owner_id'] == OWNER
assert own['publication_declarations'] == [DECL] and own['schema_version'] >= 4
assert VERIFIER != OWNER
write('own-advance-before.json', own)

# PRIVATE content-addressed raw snapshots; no foreign record/path/value is printed.
private_blobs = PRIVATE / 'blobs'
private_blobs.mkdir(mode=0o700, exist_ok=False)
paths = set()
for relative in ['runs/substantive_advances.jsonl', 'runs/substantive_discoveries.jsonl', 'research-wiki/semantic-roundtrip/registry.json']:
    if (REPO / relative).is_file(): paths.add(relative)
for directory in ['research-wiki/frontier-cells', 'research-wiki/semantic-roundtrip/audits']:
    paths.update(str(x.relative_to(REPO)) for x in (REPO / directory).rglob('*') if x.is_file())
git_paths = subprocess.check_output(['git', 'ls-files', '--cached', '--others', '--exclude-standard', '-z'], cwd=REPO).decode().split('\0')
pbps = sorted({x for x in git_paths if x and 'pbps' in x.lower() and (REPO / x).is_file()})
sphmc = sorted({x for x in git_paths if x and 'sphmc' in x.lower() and (REPO / x).is_file()})
assert pbps and sphmc
paths.update(pbps); paths.update(sphmc)
paths.update(x for x in git_paths if x and ('frontier' in x.lower()) and (REPO / x).is_file())
snap = []
for relative in sorted(paths):
    raw = (REPO / relative).read_bytes(); sha = H(raw)
    blob = private_blobs / (sha + '.bin')
    if not blob.exists():
        with blob.open('xb') as f: f.write(raw)
        blob.chmod(0o600)
    snap.append({'path': relative, 'bytes': len(raw), 'sha256': sha, 'blob': 'blobs/' + blob.name})
foreign = {k: v for k, v in state.items() if k != ID}
before = {'schema': 1, 'observed_utc': datetime.now(timezone.utc).isoformat(), 'own_advance_id': ID,
    'paths': snap, 'PBPS_protected_paths': pbps, 'SPHMC_protected_paths': sphmc,
    'foreign_advance_states': foreign, 'foreign_advance_states_canonical_sha256': D(foreign),
    'ledger_raw_sha256': H(ledger_raw), 'ledger_raw_bytes': len(ledger_raw),
    'advance_ledger_records': len(records), 'all_frontier_bytes_protected': True}
with (PRIVATE / 'before-snapshot.json').open('x') as f: f.write(json.dumps(before, ensure_ascii=False, indent=2) + '\n')
(PRIVATE / 'before-snapshot.json').chmod(0o600)
report = {'status': 'READY_FOR_ONE_NORMAL_API_TRANSITION', 'observed_utc': before['observed_utc'],
    'target_advance_id': ID, 'owner_id': OWNER, 'verifier_id': VERIFIER, 'from_state': own['state'],
    'current_carrier_commit': '348f1f34ada0e9d4f46dfa1a4b1b983ab748bb62',
    'actual_native_and_source_checked_commit': 'a2897bb1298d115070485dd271f71ea5db567b86',
    'mathematical_candidate_commit': '886adb85034f7bcf4e26a24eb648d4adb879219b',
    'all_four_relevant_files_identical_across_layers': True,
    'accepted_audit_raw_sha256': H(audit_path.read_bytes()), 'accepted_audit_canonical_sha256': D(audit),
    'exact_five_fields_match_original_proposal': True,
    'publication_binding_sha256': audit['publication_binding_sha256'],
    'native_module_freeze_sha256': H(freeze_raw), 'native_archive_all_files_lossless': True,
    'metadata_gates_at_a289_accepted_review_working_layer_passed': 4,
    'normal_transition_entrypoint': 'tools.astis_advance.transition_advance',
    'normal_transition_entrypoint_source': str(Path(inspect.getfile(transition_advance)).relative_to(REPO)),
    'normal_transition_api_calls_so_far': 0, 'normal_transition_launcher_invoked_so_far': False,
    'read_only_preflight_failures_retained': 2,
    'protected_file_count': len(snap), 'foreign_advance_state_count': len(foreign),
    'nonempty_PBPS_protected_path_count': len(pbps), 'nonempty_SPHMC_protected_path_count': len(sphmc),
    'private_before_manifest_raw_sha256': H((PRIVATE / 'before-snapshot.json').read_bytes()),
    'foreign_states_canonical_sha256': D(foreign),
    'frontiers_STAB_global_changes_authorized': False,
    'remaining_boundary': 'Only bounded local prerequisite plus private actual-law Ex23 component. Global latest-main integration, site/source-index/graph/public browser delivery, publication/purification/Exposition Seal, complete source theorem and whole Goal remain unaccepted.'}
write('preflight-report.json', report)
print(json.dumps({k: report[k] for k in ['status', 'normal_transition_api_calls_so_far', 'protected_file_count', 'foreign_advance_state_count', 'nonempty_PBPS_protected_path_count', 'nonempty_SPHMC_protected_path_count']}, indent=2))
