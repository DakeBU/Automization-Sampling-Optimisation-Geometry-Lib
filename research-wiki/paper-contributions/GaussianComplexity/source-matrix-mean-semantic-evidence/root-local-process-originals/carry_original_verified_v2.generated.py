"""Carry the independent actor's one original VERIFIED event; never invoke a transition."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import tarfile

sys.dont_write_bytecode = True
sys.path.insert(0, 'tools')
import astis_advance as advance

workspace = Path(__file__).resolve().parent.relative_to(Path.cwd())
evidence = Path('research-wiki/paper-contributions/GaussianComplexity/source-matrix-mean-semantic-evidence')
phase = evidence / 'normal-verification/mm_src_8c31'
cell = Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-matrix-mean.json')
ledger = Path('runs/substantive_advances.jsonl')
target = 'ASTIS-SA-20261112-GaussianComplexitySourceMatrixMean'
sha = lambda b: hashlib.sha256(b).hexdigest()
dump = lambda x: (json.dumps(x, ensure_ascii=False, indent=2) + '\n').encode()
git = lambda *args: subprocess.check_output(['git', *args])

def create(path, raw):
    with path.open('xb') as out:
        out.write(raw)

head = git('rev-parse', 'HEAD').decode().strip()
assert head == '94116ada2dad7de1d31ca9c67189ee734a72ed16'
assert not git('diff', '--cached', '--name-only')
assert set(git('diff', 'HEAD', '--name-only').decode().splitlines()) == {str(cell), str(ledger)}
manifest_raw = (phase / 'portable-manifest.json').read_bytes()
seal_raw = (phase / 'final-seal.json').read_bytes()
assert sha(manifest_raw) == 'dd4342190989beb66ae1d1c4635b699cd51137989a2eda69be1277ec407c3a79'
assert sha(seal_raw) == 'd72e38fdca4453e922d2d708a9dded26282efeb7f0a502fff66b1f566d14d972'
manifest, seal = json.loads(manifest_raw), json.loads(seal_raw)
assert manifest['held_metadata_HEAD'] == seal['held_metadata_HEAD'] == head
assert manifest['actor'] == seal['actor'] == '/root/mm_fresh_source_8c31'
assert seal['advance_id'] == target and seal['actual_normal_VERIFIED']
assert seal['normal_API_calls'] == 1
for key in ['normal_API_exit', 'pre_frontier_exit', 'post_frontier_exit', 'precheck_exit', 'postcheck_exit']:
    assert seal[key] == 0
assert seal['source_v1_v2_original_bytes_preserved']
assert len(manifest['entries']) == manifest['payload_file_count'] == manifest['exact_count'] == 133
for item in manifest['entries']:
    source, destination = Path(item['source']), Path(item['destination'])
    assert not source.is_absolute() and '..' not in source.parts
    assert destination.is_relative_to(phase) and not destination.is_absolute() and '..' not in destination.parts
    raw = destination.read_bytes()
    assert not source.is_symlink() and not destination.is_symlink()
    assert source.read_bytes() == raw and len(raw) == item['bytes'] and sha(raw) == item['sha256']
portable_files = sorted(p for p in phase.rglob('*') if p.is_file())
archive_path = phase / 'mm_src_8c31-normal-verification-portable.tar.gz'
expected_files = {Path(x['destination']) for x in manifest['entries']}
expected_files |= {phase / 'portable-manifest.json', phase / 'final-seal.json', archive_path}
assert len(portable_files) == seal['physical_directory_file_count_with_manifest_archive_seal'] == 136
assert set(portable_files) == expected_files
for item in seal['raw_hashes'].values():
    raw = Path(item['path']).read_bytes()
    assert len(raw) == item['bytes'] and sha(raw) == item['sha256']
with tarfile.open(archive_path, 'r:gz') as tar:
    members = tar.getmembers()
    assert len(members) == seal['archive_member_count'] == 134
    assert {x.name for x in members} == {str(p.relative_to(phase)) for p in expected_files - {archive_path, phase / 'final-seal.json'}}
    for member in members:
        assert member.isfile() and tar.extractfile(member).read() == (phase / member.name).read_bytes()
for label in ['normal-VERIFIED-API-original-v2', 'pre-frontier-v1', 'post-frontier-v1',
              'precheck-wrapper-v1', 'actual-outcome-and-cell-v1', 'postcheck-wrapper-v1']:
    receipt = json.loads((phase / (label + '.receipt.json')).read_bytes())
    assert receipt['exit_code'] == 0
    for kind in ['stdout', 'stderr']:
        assert sha((phase / (label + '.' + kind)).read_bytes()) == receipt[kind + '_sha256']
append = (phase / 'actual-VERIFIED-append.exact.jsonl').read_bytes()
payload_raw = (phase / 'actual-VERIFIED-evidence.full.json').read_bytes()
before, after = git('show', f'{head}:{ledger}'), ledger.read_bytes()
assert after == before + append and len(append.splitlines()) == 1
event, payload = json.loads(append), json.loads(payload_raw)
assert event['advance_id'] == target and event['worker_id'] == '/root/mm_fresh_source_8c31'
assert event['from_state'] == 'PROVED_LOCAL' and event['to_state'] == 'VERIFIED'
assert event['evidence'] == payload
plocal_raw = (evidence / 'actual-PROVED_LOCAL-evidence.full.json').read_bytes()
assert sha(plocal_raw) == '917c02437299ae4b3848bc0fa01affa46afa3b3c74ee5d0a472c701bccb8e291'
plocal = json.loads(plocal_raw)
assert len(plocal) == 20 and len(payload) == 30 and all(payload[k] == v for k, v in plocal.items())
assert payload['formalizer_preseal_API_pristine'] is False
assert payload['verified_commit'] == '5fb1440f771bdae77ad31f27b2275447fe3e89e5'
assert payload['verification_metadata_HEAD'] == head
old = advance._replay_advances([json.loads(x) for x in before.splitlines()])
new = advance._replay_advances([json.loads(x) for x in after.splitlines()])
assert old[target]['state'] == 'PROVED_LOCAL' and new[target]['state'] == 'VERIFIED'
assert {k:v for k,v in old.items() if k != target} == {k:v for k,v in new.items() if k != target}
assert len(old) - 1 == 307
discovery = Path('runs/substantive_discoveries.jsonl')
assert discovery.read_bytes() == git('show', f'{head}:{discovery}')
assert len(advance._replay_discoveries([json.loads(x) for x in discovery.read_bytes().splitlines()])) == 43
expected_cell = json.loads(git('show', f'{head}:{cell}'))
expected_cell['status'] = 'independently_verified'
decision_path = evidence / 'actual-VERIFIED-independent-decision.json'
expected_cell['evidence']['independent_verification'] = str(decision_path)
assert json.loads(cell.read_bytes()) == expected_cell
assert decision_path.read_bytes() == (phase / decision_path.name).read_bytes()
baseline = json.loads((workspace / 'preproof-baseline.private.json').read_bytes())
older = {str(p): sha(p.read_bytes()) for p in cell.parent.rglob('*')
         if p.is_file() and not p.is_symlink() and p != cell}
assert older == baseline['all_existing_frontier_hashes'] and len(older) == 467
for path, raw in [(evidence / 'actual-VERIFIED-append.exact.jsonl', append),
                  (evidence / 'actual-VERIFIED-evidence.full.json', payload_raw)]:
    create(path, raw)
record = {
    'actual_verified_metadata_carrier': head, 'mathematical_native_candidate': payload['verified_commit'],
    'actual_verifier': event['worker_id'], 'advance_id': target,
    'actual_VERIFIED_append_sha256': sha(append), 'actual_full_payload_sha256': sha(payload_raw),
    'original_PLOCAL_raw_bytes_unchanged': True, 'all20_original_PLOCAL_fields_preserved_inline': True,
    'original_ledger_prefix_sha256': sha(before), 'after_ledger_sha256': sha(after),
    'foreign_full_states_preserved': 307, 'all_discovery_states_and_ledger_preserved': 43,
    'older_regular_frontier_files_and_README_preserved': 467,
    'independent_tracked_inventory': 130418, 'other_tracked_bytes_preserved': 130416,
    'portable_original_verification_payloads': 133, 'portable_archive_members': 134, 'total_verification_evidence_files': 136,
    'normal_transition_subprocess_exit_code': 0, 'postcheck_exit_code': 0,
    'whole_frontier_precheck_and_postcheck_exit_codes': [0, 0],
    'normal_transition_calls': 1, 'root_VERIFIED_calls': 0, 'event_replayed': False,
    'formalizer_API_pristine': False, 'normal_verifier_failures': [],
    'root_custody_v1_failure_before_writes': 'Assumed R7 payload held_metadata_HEAD key; actual R8 original uses verification_metadata_HEAD. Corrected only the root check after actual ledger readback confirmed one VERIFIED and no custody writes. Original payload and sole normal API unchanged.',
    'history_preserved': 'Pfirst0; T1/1/0; strict0; source v1 field-schema rejection and independent v2 metadata correction, native preparer/probe failures and all original labels retained. No successful transition replay.',
    'remaining': 'Actual centered variance/concentration and arbitrary ambient adapters, public aggregate canonicalization, both main bounds and exact oracle/TV/precision/cap/cost adapters, serialized integration, actual desktop/mobile/source-index/graph/copy/download/public delivery and purification.',
}
record_path = evidence / 'actual-original-VERIFIED-custody.json'
create(record_path, dump(record))
files = [*portable_files, decision_path, evidence / 'actual-VERIFIED-append.exact.jsonl',
         evidence / 'actual-VERIFIED-evidence.full.json', record_path, cell, ledger]
assert len(files) == len(set(files))
subprocess.run(['git', 'add', '-f', '--', *map(str, files)], check=True)
assert set(git('diff', '--cached', '--name-only').decode().splitlines()) == set(map(str, files))
subprocess.run(['git', 'diff', '--cached', '--check', '--', str(record_path), str(cell), str(ledger)], check=True)
subprocess.run(['git', 'commit', '-m', 'Carry sole independent VERIFIED event for actual Gaussian matrix means'], check=True)
commit = git('rev-parse', 'HEAD').decode().strip()
for path in files:
    assert git('show', f'{commit}:{path}') == path.read_bytes()
assert not git('diff', 'HEAD', '--name-only')
record['immutable_original_VERIFIED_carrier'] = commit
create(workspace / 'actual-original-VERIFIED-commit.json', dump(record))
print(json.dumps(record))
