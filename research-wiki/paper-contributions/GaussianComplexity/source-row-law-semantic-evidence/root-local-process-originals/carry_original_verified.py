"""Carry the sole independent normal event and exact originals, without replay."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, 'tools')
import astis_advance as advance

workspace = Path(__file__).resolve().parent.relative_to(Path.cwd())
evidence = Path('research-wiki/paper-contributions/GaussianComplexity/source-row-law-semantic-evidence')
phase = evidence / 'normal-verification/rl_src_3dd4'
cell = Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-row-law.json')
ledger = Path('runs/substantive_advances.jsonl')
target = 'ASTIS-SA-20261112-GaussianComplexitySourceRowLaw'
sha = lambda raw: hashlib.sha256(raw).hexdigest()
dump = lambda obj: (json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode()
git = lambda *args: subprocess.check_output(['git', *args])
head = git('rev-parse', 'HEAD').decode().strip()
assert head == '2c57883183937fdef1578a2b33e4ea892af2c694'
assert not git('diff', '--cached', '--name-only')
assert set(git('diff', 'HEAD', '--name-only').decode().splitlines()) == {str(cell), str(ledger)}
manifest_raw = (phase / 'portable-manifest.json').read_bytes()
seal_raw = (phase / 'evidence-seal.json').read_bytes()
assert sha(manifest_raw) == 'fc8f8acd893be5e133d860d4922d08631f928158cb78eab0d2984834d05db743'
assert sha(seal_raw) == '529173894e5171984cd51535af48732fafe95a971a69400351cdf0af375a14dc'
manifest, seal = json.loads(manifest_raw), json.loads(seal_raw)
assert manifest['held_metadata_carrier'] == seal['held_metadata_HEAD'] == head
assert seal['normal_API_calls'] == 1 and seal['normal_API_exit'] == 0
assert seal['post_preservation_result'] == 'pass' and seal['frontier_pre_and_post_exit_codes'] == [0, 0]
assert len(manifest['files']) == manifest['original_file_count'] == 121
for item in manifest['files']:
    relative = Path(item['path'])
    assert not relative.is_absolute() and '..' not in relative.parts
    path = phase / relative
    raw = path.read_bytes()
    assert not path.is_symlink() and Path(item['source']) == path
    assert len(raw) == item['bytes'] and sha(raw) == item['sha256']
for item in seal['packaging_completion_receipt_and_streams']:
    raw = (phase / item['path']).read_bytes()
    assert len(raw) == item['bytes'] and sha(raw) == item['sha256']
portable_files = sorted(p for p in phase.rglob('*') if p.is_file())
assert len(portable_files) == 126
expected_files = {phase / item['path'] for item in manifest['files']}
expected_files |= {phase / 'portable-manifest.json', phase / 'evidence-seal.json'}
expected_files |= {phase / item['path'] for item in seal['packaging_completion_receipt_and_streams']}
assert set(portable_files) == expected_files and all(not p.is_symlink() for p in portable_files)
append = (phase / 'actual-VERIFIED-append.original.jsonl').read_bytes()
payload_raw = (phase / 'actual-VERIFIED-evidence.full.json').read_bytes()
assert sha(append) == 'f665dec771c757f8d2dba21c5b5c0b746d42387789c1beb224aad31c26aa164c'
assert sha(payload_raw) == '3f0f484f9424d7b63ba04fbb492855075c9f5940c6a496c3cb589d025c75dd8d'
before, after = git('show', f'{head}:{ledger}'), ledger.read_bytes()
assert after == before + append and len(append.splitlines()) == 1
event, payload = json.loads(append), json.loads(payload_raw)
assert event['advance_id'] == target and event['worker_id'] == '/root/row_law_fresh_source_3dd4'
assert event['from_state'] == 'PROVED_LOCAL' and event['to_state'] == 'VERIFIED'
assert event['evidence'] == payload
plocal_raw = (evidence / 'actual-PROVED_LOCAL-evidence.full.json').read_bytes()
assert sha(plocal_raw) == '253c50d3918d7b679792a0644eb9162ec08b4420629bfc6e568efd6ac8b86c28'
plocal = json.loads(plocal_raw)
assert len(plocal) == 20 and all(payload[key] == value for key, value in plocal.items())
assert payload['formalizer_preseal_API_pristine'] is False
assert payload['verified_commit'] == 'd0654e9bbed44ab852fc44598560799949d8bd12'
assert payload['held_metadata_carrier'] == head
old = advance._replay_advances([json.loads(x) for x in before.splitlines()])
new = advance._replay_advances([json.loads(x) for x in after.splitlines()])
assert old[target]['state'] == 'PROVED_LOCAL' and new[target]['state'] == 'VERIFIED'
assert {k:v for k,v in old.items() if k != target} == {k:v for k,v in new.items() if k != target}
assert len(old) - 1 == 305
discoveries = Path('runs/substantive_discoveries.jsonl')
assert discoveries.read_bytes() == git('show', f'{head}:{discoveries}')
assert len(advance._replay_discoveries([json.loads(x) for x in discoveries.read_bytes().splitlines()])) == 43
expected = json.loads(git('show', f'{head}:{cell}'))
expected['status'] = 'independently_verified'
decision_path = evidence / 'actual-VERIFIED-independent-decision.json'
expected['evidence']['independent_verification'] = str(decision_path)
assert json.loads(cell.read_bytes()) == expected
decision_raw = decision_path.read_bytes()
assert sha(decision_raw) == '68b42a6371921e1b325b9b1161942706e98431c3b4409b42b7a47ac52c1de524'
assert decision_raw == (phase / 'decision.original.json').read_bytes()
baseline = json.loads((workspace / 'preproof-baseline.private.json').read_bytes())
older = {str(p): sha(p.read_bytes()) for p in cell.parent.rglob('*')
         if p.is_file() and not p.is_symlink() and p != cell}
assert older == baseline['all_existing_frontier_hashes'] and len(older) == 465
for path, raw in [(evidence / 'actual-VERIFIED-append.exact.jsonl', append),
                  (evidence / 'actual-VERIFIED-evidence.full.json', payload_raw)]:
    with path.open('xb') as out:
        out.write(raw)
record = {
    'actual_verified_metadata_carrier': head, 'mathematical_native_candidate': payload['verified_commit'],
    'actual_verifier': event['worker_id'], 'advance_id': target,
    'actual_VERIFIED_append_sha256': sha(append), 'actual_full_payload_sha256': sha(payload_raw),
    'original_PLOCAL_raw_bytes_unchanged': True, 'all20_original_PLOCAL_fields_preserved_inline': True,
    'original_ledger_prefix_sha256': sha(before), 'after_ledger_sha256': sha(after),
    'foreign_full_states_preserved': 305, 'all_discovery_states_and_ledger_preserved': 43,
    'older_regular_frontier_files_and_README_preserved': 465,
    'independent_all_other_tracked_files_checked': 129882,
    'portable_original_verification_artifacts': 121, 'total_verification_evidence_files': 126,
    'normal_transition_subprocess_exit_code': 0, 'postcheck_exit_code': 0,
    'whole_frontier_precheck_and_postcheck_exit_codes': [0, 0],
    'normal_transition_calls': 1, 'root_VERIFIED_calls': 0, 'event_replayed': False,
    'formalizer_API_pristine': False,
    'verifier_failure': 'The initial count precheck failed before any API call; actual zero-V outcome inspected. Versioned count correction retained. Final single normal API, post-frontier and one preservation readback passed.',
    'remaining': 'Joint-row independence, ambient and matrix-expectation adapters, centered variance/concentration, both main bounds and exact oracle/TV/precision/cap/cost adapters, serialized integration, actual desktop/mobile/source-index/graph/copy/download/public delivery and purification.',
}
record_path = evidence / 'actual-original-VERIFIED-custody.json'
with record_path.open('xb') as out:
    out.write(dump(record))
files = [*portable_files, decision_path, evidence / 'actual-VERIFIED-append.exact.jsonl',
         evidence / 'actual-VERIFIED-evidence.full.json', record_path, cell, ledger]
assert len(files) == len(set(files))
subprocess.run(['git', 'add', '-f', '--', *map(str, files)], check=True)
assert set(git('diff', '--cached', '--name-only').decode().splitlines()) == set(map(str, files))
subprocess.run(['git', 'diff', '--cached', '--check', '--', str(record_path), str(cell), str(ledger)], check=True)
subprocess.run(['git', 'commit', '-m', 'Carry original independent Gaussian row-law VERIFIED event'], check=True)
commit = git('rev-parse', 'HEAD').decode().strip()
for path in files:
    assert git('show', f'{commit}:{path}') == path.read_bytes()
assert not git('diff', 'HEAD', '--name-only')
record['immutable_original_VERIFIED_carrier'] = commit
with (workspace / 'actual-original-VERIFIED-commit.json').open('xb') as out:
    out.write(dump(record))
print(json.dumps(record))
