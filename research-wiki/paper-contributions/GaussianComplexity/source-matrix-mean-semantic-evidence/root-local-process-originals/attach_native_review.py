"""Carry exact independent native/static originals; preserve native-credit scope."""
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
phase = Path('.astis/semantic-neutral-20261112/mm_native_4a62')
destination = evidence / 'native-review/mm_native_4a62'
cell_path = Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-matrix-mean.json')
candidate = '5fb1440f771bdae77ad31f27b2275447fe3e89e5'
target = 'ASTIS-SA-20261112-GaussianComplexitySourceMatrixMean'
sha = lambda b: hashlib.sha256(b).hexdigest()
dump = lambda x: (json.dumps(x, ensure_ascii=False, indent=2) + '\n').encode()
git = lambda *args: subprocess.check_output(['git', *args])

def create(path, raw):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as out:
        out.write(raw)

def stream_sha(path):
    digest = hashlib.sha256()
    length = 0
    with path.open('rb') as source:
        while block := source.read(4 * 1024 * 1024):
            length += len(block)
            digest.update(block)
    return length, digest.hexdigest()

head = git('rev-parse', 'HEAD').decode().strip()
local_commit = json.loads((workspace / 'actual-local-proof-commit.json').read_bytes())
assert head == local_commit['local_proof_commit']
assert not git('diff', 'HEAD', '--name-only') and not git('diff', '--cached', '--name-only')
ledger = Path('runs/substantive_advances.jsonl')
before = ledger.read_bytes()
discovery = Path('runs/substantive_discoveries.jsonl')
before_discovery = discovery.read_bytes()
baseline = json.loads((workspace / 'preproof-baseline.private.json').read_bytes())
states = advance._replay_advances([json.loads(x) for x in before.splitlines()])
assert states.pop(target)['state'] == 'PROVED_LOCAL'
assert states == baseline['all_foreign_states'] and len(states) == 307
for name, digest in baseline['all_existing_frontier_hashes'].items():
    assert sha(Path(name).read_bytes()) == digest
report_raw = (phase / 'report.json').read_bytes()
manifest_raw = (phase / 'portable-manifest.json').read_bytes()
archive_path = phase / 'mm_native_4a62-portable.tar.gz'
archive_raw = archive_path.read_bytes()
assert sha(report_raw) == '82efcb654cdbd8e65e11dc17a5136d3c516b8730a92bcdc36416aaaf13f9a65e'
assert sha(manifest_raw) == '64372485bbcdff58200981201e649733e09673505d1a8cc2fa51dffde8cc2860'
assert sha(archive_raw) == '9b49a45ad0f09673ef7303956731962af7d14e7b826cdc1ea01489be890bf293'
assert sha((phase / 'final-seal.json').read_bytes()) == '20925d457c9aefeb71aff1199e96196369437891b1ac0285a62bcf65ddafe5cf'
report, manifest = json.loads(report_raw), json.loads(manifest_raw)
assert report['candidate'] == manifest['candidate'] == candidate
assert report['verdict'] == 'PASS_WITH_EXPLICIT_BOUNDED_SCOPE'
assert report['source_fidelity_verdict'] is None
native = report['native']
assert native['fresh_ASTIS_module_count'] == 7 and native['fresh_compile_exit_codes'] == [0] * 7
assert native['whole_module_constant_count'] == 39 and native['whole_module_all_full_types_and_bodies_read']
assert native['whole_module_all_closed'] and native['starting_ASTIS_olean_count'] == 0
assert native['no_ASTIS_cached_olean_copied_or_reachable']
assert (native['new_owned_count'], native['new_handwritten_roots'], native['new_generated_reachable']) == (3, 2, 1)
assert native['full_seven_module_root_reachable_constants'] == 32
assert native['retained_old_generated_outside_root_closure'] == 7
assert set(native['allowed_axioms_only']) == {'propext', 'Classical.choice', 'Quot.sound'}
assert native['root_original_probe_replayed_exit0']
assert len(native['sealed_literal_kernel_applications']) == 2
assert all(x['sealed_literal_kernel_application'] and not x['raw_expr_structurally_equal']
           for x in native['sealed_literal_kernel_applications'])
draft = json.loads((evidence / 'publication-draft-record.json').read_bytes())
assert {k: sorted(v) for k, v in native['actual_immediate_ASTIS_parents'].items()} == {
    k: sorted(v) for k, v in draft['actual_public_ASTIS_parents'].items()}
static = report['static_reader']
assert static['source_ordered_proof_folds'] == 6
assert static['full_T_source_lines'] == 158 and static['private_L17_anchor']
assert static['all_exact_source_bytes_formulae_and_progressive_authored_data_checked']
assert static['true_materialized_download_filebytes'] and static['bounded_theme_and_empty_status_inputs']
assert report['byte_and_history']['original_archive_members_rehashed'] == 218
assert (report['byte_and_history']['source_spans'], report['byte_and_history']['Lean_spans']) == (27, 30)
assert report['receipts']['total'] == 109
assert len(manifest['payload']) == manifest['payload_file_count'] == 440
with tarfile.open(archive_path, 'r:gz') as archive:
    members = archive.getmembers()
    expected = {x['path'] for x in manifest['payload']} | {'portable-manifest.json'}
    assert len(members) == len(expected) == 441 and {x.name for x in members} == expected
    for member in members:
        relative = Path(member.name)
        assert member.isfile() and not relative.is_absolute() and '..' not in relative.parts
    assert archive.extractfile('portable-manifest.json').read() == manifest_raw
    for item in manifest['payload']:
        relative = Path(item['path'])
        assert not relative.is_absolute() and '..' not in relative.parts
        raw = (phase / relative).read_bytes()
        assert len(raw) == item['bytes'] and sha(raw) == item['sha256']
        assert archive.extractfile(item['path']).read() == raw
receipt_paths = [Path(x['path']) for x in manifest['payload']
                 if x['path'].startswith('receipts/') and x['path'].endswith('.receipt.json')]
assert len(receipt_paths) == 109
for path in receipt_paths:
    receipt = json.loads((phase / path).read_bytes())
    for kind in ['stdout', 'stderr']:
        item = receipt[kind]
        raw = (phase / item['path']).read_bytes()
        assert len(raw) == item['bytes'] and sha(raw) == item['sha256']
large = report['large_local_dump']
assert large['portable'] is False
assert stream_sha(phase / large['path']) == (large['bytes'], large['sha256'])
binding_raw = (phase / 'relevant-input-binding.json').read_bytes()
assert sha(binding_raw) == '2eb375336a679d9682215d53aa2336d8e93b5afcea71615515cff785aa8df556'
binding = json.loads(binding_raw)
assert binding['candidate'] == binding['native_compile_credit_only_for'] == candidate
assert len(binding['repository_inputs']) == 50
comparisons = []
for item in binding['repository_inputs']:
    path = Path(item['repository_relative_path'])
    raw = path.read_bytes()
    assert len(raw) == item['bytes'] and sha(raw) == item['sha256']
    if path.parts[0] == '.astis':
        tracked = False
    else:
        assert git('show', f'{candidate}:{path}') == raw and git('show', f'{head}:{path}') == raw
        tracked = True
    comparisons.append({**item, 'candidate_and_metadata_git_bytes_compared': tracked,
                        'pinned_local_input_only': not tracked})
assert sum(x['candidate_and_metadata_git_bytes_compared'] for x in comparisons) == 48
binary = binding['native_binary']
assert stream_sha(Path(binary['path'])) == (binary['bytes'], binary['sha256'])
package_checks = []
for package in binding['actual_package_pins']:
    path = Path('.lake/packages') / package['name']
    actual = subprocess.check_output(['git', '-C', str(path), 'rev-parse', 'HEAD']).decode().strip()
    clean = not subprocess.check_output(['git', '-C', str(path), 'status', '--porcelain=v1', '--untracked-files=all'])
    assert actual == package['expected'] == package['actual'] and clean
    package_checks.append({'name': package['name'], 'revision': actual, 'clean_including_untracked': clean})
assert len(package_checks) == 9
comparison_path = destination / 'metadata-carrier-byte-comparison.json'
create(comparison_path, dump({
    'compiled_candidate': candidate, 'later_metadata_HEAD': head,
    'new_native_compile_claimed_for_metadata_HEAD': False,
    'unchanged_relevant_inputs': comparisons, 'actual_packages_rechecked': package_checks,
    'actual_binary_and_pinned_local_probe_and_raw_source_hashes_rechecked': True,
    'local_large_body_dump_stream_rehashed_without_export': large,
}))
names = ['report.json', 'report.md', 'portable-manifest.json', 'mm_native_4a62-portable.tar.gz',
         'REPRODUCE.md', 'relevant-input-binding.json', 'final-seal.json', 'portable-archive-rehash.json']
copies = [(destination / name, (phase / name).read_bytes()) for name in names]
for path, raw in copies:
    create(path, raw)
owner_path = evidence / 'last-formal-main-original-owner-observation.json'
create(owner_path, (workspace / 'latest-original-owner-after-math-candidate.json').read_bytes())
cell = json.loads(cell_path.read_bytes())
assert cell['status'] == 'proved_locally' and cell['evidence']['independent_verification'] == ''
cell['evidence']['independent_native_review'] = {
    'report': str(destination / 'report.json'), 'report_sha256': sha(report_raw),
    'compiled_candidate': candidate, 'metadata_carrier_byte_comparison_head': head,
    'original_portable_manifest': str(destination / 'portable-manifest.json'),
    'original_raw_execution_archive': str(destination / 'mm_native_4a62-portable.tar.gz'),
    'normal_VERIFIED_transition_performed': False,
}
cell['statement_seal']['status'] = 'EXACT_UNCHANGED_TYPES_COMPILED;INDEPENDENT_SOURCE_AND_FRESH_NATIVE_COMPLETE;API_NONPRISTINE_DISCLOSED'
cell['reader_contract']['status'] = 'Independent source and complete module review plus six exact closed production static folds accepted; full private158-line source at L17. Native theme is bounded and minimal. Actual desktop/mobile/MathJax/global source-index/graph/copy/download interaction and public delivery, serialized integration and purification remain HOLD.'
cell['purification']['dead_code_audit'] = 'All3 new declarations (2 handwritten,1 generated) reachable, standard axioms only. Full7-module fresh native closure checks39 complete types/bodies;32 root-reachable and7 older GridAlias generated helpers outside this root retained unchanged. No global dead-code or post-merge purification claim.'
cell['purification']['canonicalization'] = 'Same row-law and truncated-row-moment producer nodes and same cosine-frame consumer node are shared canonical declarations. Old private canonical-row matrix application is outside this native import closure and gains no new credit.'
cell_path.write_bytes(dump(cell))
record = {
    'mathematical_native_candidate': candidate, 'PLOCAL_carrier': head,
    'source_metadata_commit': local_commit['reviewed_metadata_commit'],
    'native_reviewer': '/root/mm_native_4a62', 'original_report_sha256': sha(report_raw),
    'original_manifest_sha256': sha(manifest_raw), 'original_archive_sha256': sha(archive_raw),
    'exact_archive_members_verified': 441, 'selected_direct_originals_carried': len(copies),
    'full_native_owned_constants': 39, 'new_packet_owned_namespaces': 3,
    'new_handwritten_roots': 2, 'new_generated_reachable': 1,
    'older_GridAlias_generated_outside_root_closure_retained': 7,
    'formalizer_API_pristine': False, 'all_original_PLOCAL_evidence_unchanged': True,
    'foreign_full_states_preserved': len(states),
    'older_frontier_regular_files_preserved': len(baseline['all_existing_frontier_hashes']),
    'normal_VERIFIED_calls_by_root': 0, 'full_reader_integration_and_purification': 'HOLD',
}
record_path = evidence / 'actual-independent-native-review-attachment.json'
create(record_path, dump(record))
assert ledger.read_bytes() == before and discovery.read_bytes() == before_discovery
paths = [cell_path, owner_path, comparison_path, record_path, *[p for p, _ in copies]]
subprocess.run(['git', 'add', '-f', '--', *map(str, paths)], check=True)
assert set(git('diff', '--cached', '--name-only').decode().splitlines()) == set(map(str, paths))
subprocess.run(['git', 'diff', '--cached', '--check', '--', str(cell_path), str(record_path)], check=True)
subprocess.run(['git', 'commit', '-m', 'Carry independent actual matrix-mean native closure and static reader evidence'], check=True)
commit = git('rev-parse', 'HEAD').decode().strip()
for path in paths:
    assert git('show', f'{commit}:{path}') == path.read_bytes()
assert not git('diff', 'HEAD', '--name-only')
record['native_review_metadata_commit'] = commit
create(workspace / 'actual-independent-native-review-commit.json', dump(record))
print(json.dumps(record))
