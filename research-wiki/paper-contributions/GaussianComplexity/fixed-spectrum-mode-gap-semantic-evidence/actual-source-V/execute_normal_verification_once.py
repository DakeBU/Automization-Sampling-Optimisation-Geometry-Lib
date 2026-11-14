from pathlib import Path
from datetime import datetime, timezone
from contextlib import redirect_stdout, redirect_stderr
import hashlib, inspect, io, json, subprocess, sys, traceback

sys.dont_write_bytecode = True
REPO = Path('/Users/zhouhuanjian/ASTIS-GC')
sys.path.insert(0, str(REPO))
from tools.astis_advance import transition_advance, _replay_advances

BASE = REPO / '.astis/semantic-neutral-20261110/src_62f8c4/sourcev_execution_20261110'
PUB, PRIVATE = BASE / 'public', BASE / 'private'
ID = 'ASTIS-SA-20261110-GaussianComplexityFixedSpectrumModeGap'
OWNER = 'huanjian_gc_20261110_fixed_spectrum_mode_gap'
VERIFIER = '/root/source_reader_62f8c4'
LEDGER = REPO / 'runs/substantive_advances.jsonl'
H = lambda b: hashlib.sha256(b).hexdigest()
D = lambda x: H(json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode())
stamp = lambda: datetime.now(timezone.utc).isoformat()
calls = 0
returned = False
error = None
stdout, stderr = io.StringIO(), io.StringIO()

def exclusive_json(path, value):
    with path.open('x', encoding='utf-8') as f:
        f.write(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def journal(event):
    with (PUB / 'normal-api-call-journal.jsonl').open('a', encoding='utf-8') as f:
        f.write(json.dumps({'event': event, 'utc': stamp(), 'actual_transition_API_calls': calls}, sort_keys=True) + '\n')

assert not (PUB / 'normal-api-call-journal.jsonl').exists(), 'Never retry this launcher.'
journal('launcher-started')
try:
    assert Path(inspect.getfile(transition_advance)).resolve() == REPO / 'tools/astis_advance.py'
    assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=REPO).decode().strip() == '348f1f34ada0e9d4f46dfa1a4b1b983ab748bb62'
    contract = json.loads((PUB / 'original-evidence-contract.json').read_text())
    raw_evidence = (PUB / 'original-evidence.raw.json').read_bytes()
    canonical_evidence = (PUB / 'original-evidence.canonical.json').read_bytes()
    evidence = json.loads(raw_evidence)
    assert H(raw_evidence) == contract['original_raw_sha256']
    assert H(canonical_evidence) == contract['original_canonical_sha256'] == D(evidence)
    assert evidence == json.loads(canonical_evidence)
    before = json.loads((PRIVATE / 'before-snapshot.json').read_text())
    for row in before['paths']:
        assert H((REPO / row['path']).read_bytes()) == row['sha256'], 'Protected baseline changed before API.'
    before_raw = LEDGER.read_bytes()
    assert H(before_raw) == before['ledger_raw_sha256'] and before_raw.endswith(b'\n')
    before_records = [json.loads(line) for line in before_raw.splitlines() if line.strip()]
    own_before = _replay_advances(before_records)[ID]
    assert own_before['state'] == 'PROVED_LOCAL' and own_before['owner_id'] == OWNER
    assert evidence['verifier_id'] == VERIFIER != OWNER
    journal('all-read-only-preflight-checks-passed')
    calls += 1
    journal('entering-single-normal-transition-API-call')
    with redirect_stdout(stdout), redirect_stderr(stderr):
        transition_advance(ID, 'VERIFIED', worker_id=VERIFIER,
            modes=['source-review', 'independent-verification'], evidence=evidence)
    returned = True
    journal('single-normal-transition-API-returned-successfully')
except BaseException:
    error = traceback.format_exc()
    journal('launcher-stopped-with-exception-no-retry')
finally:
    with (PRIVATE / 'normal-API.stdout.raw.txt').open('xb') as f: f.write(stdout.getvalue().encode())
    with (PRIVATE / 'normal-API.stderr.raw.txt').open('xb') as f: f.write(stderr.getvalue().encode())
    if error:
        with (PRIVATE / 'normal-launcher-exception.raw.txt').open('x') as f: f.write(error)

# These are post-call reads, never a second API call.
after_raw = LEDGER.read_bytes()
after_records = [json.loads(line) for line in after_raw.splitlines() if line.strip()]
after_state = _replay_advances(after_records)
before = json.loads((PRIVATE / 'before-snapshot.json').read_text())
foreign_after = {k: v for k, v in after_state.items() if k != ID}
foreign_unchanged = foreign_after == before['foreign_advance_states']
suffix = after_raw[before['ledger_raw_bytes']:] if after_raw.startswith(before_raw) else b''
appended = [json.loads(line) for line in suffix.splitlines() if line.strip()]
one_exact_append = (len(appended) == 1 and appended[0]['advance_id'] == ID and
    appended[0]['from_state'] == 'PROVED_LOCAL' and appended[0]['to_state'] == 'VERIFIED' and
    appended[0]['worker_id'] == VERIFIER and appended[0]['evidence'] == evidence)

snap = []
changes = []
for row in before['paths']:
    raw = (REPO / row['path']).read_bytes(); sha = H(raw)
    blob = PRIVATE / 'blobs' / (sha + '.bin')
    if not blob.exists():
        with blob.open('xb') as f: f.write(raw)
        blob.chmod(0o600)
    snap.append({'path': row['path'], 'bytes': len(raw), 'sha256': sha, 'blob': 'blobs/' + blob.name})
    if sha != row['sha256']: changes.append(row['path'])
after = {'schema': 1, 'observed_utc': stamp(), 'own_advance_id': ID, 'paths': snap,
    'PBPS_protected_paths': before['PBPS_protected_paths'], 'SPHMC_protected_paths': before['SPHMC_protected_paths'],
    'foreign_advance_states': foreign_after, 'foreign_advance_states_canonical_sha256': D(foreign_after),
    'ledger_raw_sha256': H(after_raw), 'ledger_raw_bytes': len(after_raw),
    'advance_ledger_records': len(after_records), 'changed_paths': changes}
exclusive_json(PRIVATE / 'after-snapshot.json', after)
(PRIVATE / 'after-snapshot.json').chmod(0o600)
exclusive_json(PUB / 'own-advance-after.json', after_state[ID])
if one_exact_append:
    with (PUB / 'actual-own-ledger-append.raw.jsonl').open('xb') as f: f.write(suffix)

preserved = (foreign_unchanged and changes == ['runs/substantive_advances.jsonl'] and
    after_raw.startswith(before_raw) and one_exact_append and
    after_state[ID]['state'] == 'VERIFIED' and after_state[ID]['owner_id'] == OWNER)
result = {'schema': 1, 'observed_utc': stamp(), 'advance_id': ID, 'verifier_id': VERIFIER,
    'normal_API_entrypoint': 'tools.astis_advance.transition_advance',
    'actual_normal_transition_API_calls': calls, 'API_returned_successfully': returned,
    'launcher_exception': error is not None, 'launcher_exception_private': error is not None,
    'from_state': 'PROVED_LOCAL', 'after_state': after_state[ID]['state'],
    'exact_original_evidence_appended': one_exact_append,
    'original_evidence_raw_sha256': contract['original_raw_sha256'],
    'original_evidence_canonical_sha256': contract['original_canonical_sha256'],
    'actual_append_raw_sha256': H(suffix) if one_exact_append else None,
    'actual_append_record_canonical_sha256': D(appended[0]) if one_exact_append else None,
    'before_ledger_raw_sha256': before['ledger_raw_sha256'], 'after_ledger_raw_sha256': H(after_raw),
    'prior_ledger_bytes_exact_prefix': after_raw.startswith(before_raw),
    'foreign_advance_states_unchanged': foreign_unchanged, 'foreign_advance_state_count': len(foreign_after),
    'foreign_advance_states_canonical_sha256': D(foreign_after),
    'all_frontier_and_other_protected_bytes_unchanged': changes == ['runs/substantive_advances.jsonl'],
    'protected_file_count': len(snap), 'nonempty_PBPS_protected_path_count': len(before['PBPS_protected_paths']),
    'nonempty_SPHMC_protected_path_count': len(before['SPHMC_protected_paths']),
    'private_before_snapshot_raw_sha256': H((PRIVATE / 'before-snapshot.json').read_bytes()),
    'private_after_snapshot_raw_sha256': H((PRIVATE / 'after-snapshot.json').read_bytes()),
    'preservation_pass': preserved,
    'no_other_cell_frontier_STAB_or_global_state_mutation': preserved,
    'native_proof_static_site_browser_commands_rerun': False,
    'fresh_native_at_carrier348_claimed': False,
    'current_carrier_commit': '348f1f34ada0e9d4f46dfa1a4b1b983ab748bb62',
    'actual_native_and_source_verified_commit': evidence['verified_commit'],
    'remaining_global_site_public_purification_whole_Goal_boundaries': evidence['truth_boundary']}
exclusive_json(PUB / 'normal-verification-execution-result.json', result)
journal('post-call-preservation-checked')
print(json.dumps({k: result[k] for k in ['advance_id', 'actual_normal_transition_API_calls',
    'API_returned_successfully', 'after_state', 'exact_original_evidence_appended', 'preservation_pass']}, indent=2))
if not (calls == 1 and returned and preserved):
    raise SystemExit(1)
