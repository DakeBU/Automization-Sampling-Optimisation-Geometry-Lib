"""Carry the sole real independent VERIFIED append without executing any transition."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, 'tools')
import astis_advance as advance

workspace = Path(__file__).resolve().parent.relative_to(Path.cwd())
evidence = Path('research-wiki/paper-contributions/GaussianComplexity/source-row-independence-semantic-evidence')
phase = evidence / 'normal-verification/ri_src_5ab9'
cell = Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-row-independence.json')
ledger = Path('runs/substantive_advances.jsonl')
target = 'ASTIS-SA-20261112-GaussianComplexitySourceRowIndependence'
sha = lambda b: hashlib.sha256(b).hexdigest()
dump = lambda x: (json.dumps(x, ensure_ascii=False, indent=2) + '\n').encode()
git = lambda *args: subprocess.check_output(['git', *args])

def create(path, raw):
    with path.open('xb') as out:
        out.write(raw)

head = git('rev-parse', 'HEAD').decode().strip()
assert head == 'e5a4eadca4a6208e54cc90b7cb351e664f922cd5'
assert not git('diff', '--cached', '--name-only')
assert set(git('diff', 'HEAD', '--name-only').decode().splitlines()) == {str(cell), str(ledger)}
manifest_raw = (phase / 'portable-manifest.json').read_bytes()
seal_raw = (phase / 'portable-seal.json').read_bytes()
assert sha(manifest_raw) == '39d724afa88e4e0b01ab05d461299690952d602021c948f5a8aa5ed3e7d3f1b9'
assert sha(seal_raw) == '1bc6f515ea09626eb1eaff441fbf031437f02ed674607e449ac3b2a96c7d207c'
manifest, seal = json.loads(manifest_raw), json.loads(seal_raw)
assert manifest['held_metadata_HEAD'] == head
assert manifest['verifier_id'] == seal['verifier_id'] == '/root/row_indep_fresh_source_5ab9'
assert manifest['advance_id'] == seal['advance_id'] == target
assert seal['normal_API_calls'] == 1
assert seal['all_four_original_final_gates_exit0']
assert seal['all_corrected_own_acceptance_and_pre_post_checks_exit0']
assert seal['all_foreign_full_states_discovery_bytes_frontier_files_other_tracked_files_and_prior_source_package_unchanged']
assert len(manifest['entries']) == manifest['listed_original_files'] == 75
for item in manifest['entries']:
    source, destination = Path(item['source']), Path(item['destination'])
    assert not source.is_absolute() and '..' not in source.parts
    assert destination.is_relative_to(phase)
    assert not source.is_symlink() and source.read_bytes() == destination.read_bytes()
    assert not destination.is_absolute() and '..' not in destination.parts
    raw = destination.read_bytes()
    assert not destination.is_symlink() and len(raw) == item['bytes'] and sha(raw) == item['sha256']
portable_files = sorted(p for p in phase.rglob('*') if p.is_file())
expected_files = {Path(x['destination']) for x in manifest['entries']}
expected_files |= {phase / 'portable-manifest.json', phase / 'portable-seal.json'}
assert len(portable_files) == manifest['total_files_including_manifest_and_seal'] == 77
assert set(portable_files) == expected_files
for label in ['normal-api', 'pre-frontier', 'post-frontier', 'pre-preservation-v2', 'post-preservation', 'acceptance-v2']:
    receipt = json.loads((phase / 'receipts' / (label + '.json')).read_bytes())
    assert receipt['exit_code'] == 0
    for kind in ['stdout', 'stderr']:
        item = receipt[kind]
        raw = Path(item['path']).read_bytes()
        assert len(raw) == item['bytes'] and sha(raw) == item['sha256']
for label in ['pre-preservation', 'acceptance-v1']:
    assert json.loads((phase / 'receipts' / (label + '.json')).read_bytes())['exit_code'] == 1
append = (phase / 'actual-VERIFIED-append.original.jsonl').read_bytes()
payload_raw = (phase / 'actual-VERIFIED-evidence.full.json').read_bytes()
assert sha(append) == 'ca03d1d272e159f1f332dcb3ec55a31d4519c32bc637f44cabf22692f5bbdf05'
assert sha(payload_raw) == '72a22ed9cf0a31915d6a3cf7f72ae4792565896db7a3babd957a32f8b4107914'
before, after = git('show', f'{head}:{ledger}'), ledger.read_bytes()
assert after == before + append and len(append.splitlines()) == 1
event, payload = json.loads(append), json.loads(payload_raw)
assert event['advance_id'] == target and event['worker_id'] == '/root/row_indep_fresh_source_5ab9'
assert event['from_state'] == 'PROVED_LOCAL' and event['to_state'] == 'VERIFIED'
assert event['evidence'] == payload
plocal_raw = (evidence / 'actual-PROVED_LOCAL-evidence.full.json').read_bytes()
assert sha(plocal_raw) == '7e5b58b1066292ae3c5ca14534a00f4d86e3c39bd74d241916791f6a613b215e'
plocal = json.loads(plocal_raw)
assert len(plocal) == 20 and all(payload[k] == v for k, v in plocal.items())
assert payload['formalizer_preseal_API_pristine'] is False
assert payload['verified_commit'] == '66e0bb9b748d68816a8443d60696656c9340222f'
assert payload['held_metadata_HEAD'] == head
old = advance._replay_advances([json.loads(x) for x in before.splitlines()])
new = advance._replay_advances([json.loads(x) for x in after.splitlines()])
assert old[target]['state'] == 'PROVED_LOCAL' and new[target]['state'] == 'VERIFIED'
assert {k:v for k,v in old.items() if k != target} == {k:v for k,v in new.items() if k != target}
assert len(old) - 1 == 306
discovery = Path('runs/substantive_discoveries.jsonl')
assert discovery.read_bytes() == git('show', f'{head}:{discovery}')
assert len(advance._replay_discoveries([json.loads(x) for x in discovery.read_bytes().splitlines()])) == 43
expected_cell = json.loads(git('show', f'{head}:{cell}'))
expected_cell['status'] = 'independently_verified'
decision_path = evidence / 'actual-VERIFIED-independent-decision.json'
expected_cell['evidence']['independent_verification'] = str(decision_path)
assert json.loads(cell.read_bytes()) == expected_cell
decision_raw = decision_path.read_bytes()
assert sha(decision_raw) == '9fceb2c439b29782ad79b46269c4c3d88d7f5caa8f924c33b988e10b4ec8a277'
baseline = json.loads((workspace / 'preproof-baseline.private.json').read_bytes())
older = {str(p): sha(p.read_bytes()) for p in cell.parent.rglob('*')
         if p.is_file() and not p.is_symlink() and p != cell}
assert older == baseline['all_existing_frontier_hashes'] and len(older) == 466
for path, raw in [(evidence / 'actual-VERIFIED-append.exact.jsonl', append),
                  (evidence / 'actual-VERIFIED-evidence.full.json', payload_raw)]:
    create(path, raw)
record = {
    'actual_verified_metadata_carrier': head, 'mathematical_native_candidate': payload['verified_commit'],
    'actual_verifier': event['worker_id'], 'advance_id': target,
    'actual_VERIFIED_append_sha256': sha(append), 'actual_full_payload_sha256': sha(payload_raw),
    'original_PLOCAL_raw_bytes_unchanged': True, 'all20_original_PLOCAL_fields_preserved_inline': True,
    'original_ledger_prefix_sha256': sha(before), 'after_ledger_sha256': sha(after),
    'foreign_full_states_preserved': 306, 'all_discovery_states_and_ledger_preserved': 43,
    'older_regular_frontier_files_and_README_preserved': 466,
    'independent_all_other_tracked_files_checked': 130148,
    'portable_original_verification_artifacts': 75, 'total_verification_evidence_files': 77,
    'normal_transition_subprocess_exit_code': 0, 'postcheck_exit_code': 0,
    'whole_frontier_precheck_and_postcheck_exit_codes': [0, 0],
    'normal_transition_calls': 1, 'root_VERIFIED_calls': 0, 'event_replayed': False,
    'formalizer_API_pristine': False,
    'root_custody_v1_rejected_before_writes': 'Assumed manifest original-source path equals portable-copy path; corrected to byte-compare each distinct original and destination. Original script, failed receipt/log and independent successful V remain unchanged. No normal API in either custody script.',
    'verifier_rejected_prechecks': 'Local-main/origin-main confusion and an archive .olean lookup assumption failed before any API. Original v1 scripts/receipts and corrected v2 are retained. One successful normal API was never replayed.',
    'remaining': 'Actual matrix expectation and arbitrary ambient adapters, public aggregate canonicalization, centered variance/concentration, both main bounds and exact oracle/TV/precision/cap/cost adapters, serialized integration, actual desktop/mobile/source-index/graph/copy/download/public delivery and purification.',
}
record_path = evidence / 'actual-original-VERIFIED-custody.json'
create(record_path, dump(record))
files = [*portable_files, decision_path, evidence / 'actual-VERIFIED-append.exact.jsonl',
         evidence / 'actual-VERIFIED-evidence.full.json', record_path, cell, ledger]
assert len(files) == len(set(files))
subprocess.run(['git', 'add', '-f', '--', *map(str, files)], check=True)
assert set(git('diff', '--cached', '--name-only').decode().splitlines()) == set(map(str, files))
subprocess.run(['git', 'diff', '--cached', '--check', '--', str(record_path), str(cell), str(ledger)], check=True)
subprocess.run(['git', 'commit', '-m', 'Carry original independent Gaussian joint-row VERIFIED event'], check=True)
commit = git('rev-parse', 'HEAD').decode().strip()
for path in files:
    assert git('show', f'{commit}:{path}') == path.read_bytes()
assert not git('diff', 'HEAD', '--name-only')
record['immutable_original_VERIFIED_carrier'] = commit
create(workspace / 'actual-original-VERIFIED-commit.json', dump(record))
print(json.dumps(record))
