"""Carry independent native originals after exact custody and held-input comparison."""
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
evidence = Path('research-wiki/paper-contributions/GaussianComplexity/source-row-independence-semantic-evidence')
phase = Path('.astis/semantic-neutral-20261112/ri_native_74b8')
destination = evidence / 'native-review/ri_native_74b8'
cell_path = Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-row-independence.json')
candidate = '66e0bb9b748d68816a8443d60696656c9340222f'
target = 'ASTIS-SA-20261112-GaussianComplexitySourceRowIndependence'
sha = lambda b: hashlib.sha256(b).hexdigest()
dump = lambda obj: (json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode()
git = lambda *args: subprocess.check_output(['git', *args])

def create(path, raw):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as out:
        out.write(raw)

head = git('rev-parse', 'HEAD').decode().strip()
local_commit = json.loads((workspace / 'actual-local-proof-commit.json').read_bytes())
assert head == local_commit['local_proof_commit']
assert not git('diff', 'HEAD', '--name-only') and not git('diff', '--cached', '--name-only')
ledger = Path('runs/substantive_advances.jsonl')
before = ledger.read_bytes()
discovery_path = Path('runs/substantive_discoveries.jsonl')
before_discoveries = discovery_path.read_bytes()
baseline = json.loads((workspace / 'preproof-baseline.private.json').read_bytes())
states = advance._replay_advances([json.loads(x) for x in before.splitlines()])
assert states.pop(target)['state'] == 'PROVED_LOCAL'
assert states == baseline['all_foreign_states']
for path, digest in baseline['all_existing_frontier_hashes'].items():
    assert sha(Path(path).read_bytes()) == digest, path
report_raw = (phase / 'report.json').read_bytes()
manifest_raw = (phase / 'portable-manifest.json').read_bytes()
archive_raw = (phase / 'portable-evidence.tar.gz').read_bytes()
assert sha(report_raw) == '75f6730c5d105217b3ab0d4b6c73c079fcef9b4592b2cf3d8d01ec123cc46419'
assert sha(manifest_raw) == '782536c48c83e179b096a1cf63f57e5f3648c158b480d222fa014c4b68cdda41'
assert sha(archive_raw) == '2f878e68fd733379d6ac055e8a32111c13d3f782efda4bd41a1dc2382f0ed709'
report, manifest = json.loads(report_raw), json.loads(manifest_raw)
assert report['compile_candidate_only'] == manifest['compile_candidate'] == candidate
assert report['verdict'] == 'ACCEPT_BOUNDED_NATIVE_WHOLE_MODULE_STATIC'
assert not report['source_fidelity_grant'] and not report['ledger_transition_or_permission_grant']
native = report['native']
assert native['fresh_module_builds'] == native['all_owned_declarations'] == 3
assert native['new_handwritten'] == 2 and native['new_generated'] == 0
assert native['all_owned_reachable'] and native['native_type_body_closed']
assert set(native['standard_axioms_only']) == {'propext', 'Classical.choice', 'Quot.sound'}
assert native['exact_author_probe_pass'] and native['separate_seal_literal_kernel_applications_pass']
assert native['no_ASTIS_cached_oleans_copied_or_reachable']
draft = json.loads((evidence / 'publication-draft-record.json').read_bytes())
assert native['parents'] == draft['actual_public_ASTIS_parents']
static = report['static']
assert static['complete_private_export_lines'] == 81 and static['private_link_line'] == 11
assert static['original_blank_separator_line'] == 60
assert len(static['six_exact_closed_steps']) == 6
assert all(x['initially_closed'] and x['exact_adjacent_formula_and_Lean'] for x in static['six_exact_closed_steps'])
assert static['coordinate_span_checks'] == 47 and static['original_archive_members_all_reread'] == 204
assert len(manifest['members']) == manifest['member_count_excluding_this_manifest'] == 460
assert manifest['receipt_count'] == len(manifest['receipts']) == 106
assert manifest['receipts_all_streams_rehashed']
with tarfile.open(phase / 'portable-evidence.tar.gz', 'r:gz') as archive:
    members = archive.getmembers()
    expected = {x['path'] for x in manifest['members']} | {'portable-manifest.json'}
    assert len(members) == len(expected) == 461
    assert {m.name for m in members} == expected
    assert sum(m.size for m in members) == 4395888
    for member in members:
        relative = Path(member.name)
        assert member.isfile() and not relative.is_absolute() and '..' not in relative.parts
    assert archive.extractfile('portable-manifest.json').read() == manifest_raw
    for item in manifest['members']:
        relative = Path(item['path'])
        assert not relative.is_absolute() and '..' not in relative.parts
        raw = (phase / relative).read_bytes()
        assert len(raw) == item['bytes'] and sha(raw) == item['sha256']
        assert archive.extractfile(item['path']).read() == raw
for item in manifest['receipts']:
    receipt = json.loads((phase / item['path']).read_bytes())
    assert receipt['exit_code'] == item['exit_code']
    for stream in ('stdout', 'stderr'):
        original = receipt[stream]
        raw = (phase / original['path']).read_bytes()
        assert len(raw) == original['bytes'] and sha(raw) == original['sha256']
full_dump = native['full_native_dump']
full_dump_raw = (phase / full_dump['path']).read_bytes()
assert len(full_dump_raw) == full_dump['bytes'] and sha(full_dump_raw) == full_dump['sha256']
binding_raw = (phase / 'relevant-input-binding.json').read_bytes()
assert sha(binding_raw) == report['final_binding']['sha256']
binding = json.loads(binding_raw)
assert binding['compile_candidate_only'] == candidate and not binding['later_carrier_compilation_claimed']
inputs = binding['tracked_relevant_input_hashes']
assert len(inputs) == report['final_binding']['tracked_input_count'] == 45
for item in inputs:
    path = Path(item['path'])
    raw = path.read_bytes()
    assert len(raw) == item['bytes'] and sha(raw) == item['sha256']
    assert git('show', f'{head}:{path}') == raw and git('show', f'{candidate}:{path}') == raw
for item in (binding['private_author_probe'], binding['source_raw'], binding['native_binary']):
    path = Path(item.get('path', item.get('origin')))
    assert sha(path.read_bytes()) == item['sha256']
package_checks = []
for package in json.loads(Path('lake-manifest.json').read_bytes())['packages']:
    path = Path('.lake/packages') / package['name']
    actual = subprocess.check_output(['git', '-C', str(path), 'rev-parse', 'HEAD']).decode().strip()
    clean = not subprocess.check_output(['git', '-C', str(path), 'status', '--porcelain=v1', '--untracked-files=all'])
    assert actual == package['rev'] and clean
    package_checks.append({'name': package['name'], 'rev': actual, 'clean_including_untracked': clean})
assert len(package_checks) == 9
comparison = {
    'compiled_candidate': candidate, 'later_metadata_HEAD': head,
    'new_native_compile_claimed_for_metadata_HEAD': False,
    'unchanged_relevant_inputs': inputs, 'actual_packages_rechecked': package_checks,
    'actual_binary_and_original_author_probe_and_raw_source_hashes_rechecked': True,
}
names = ['report.json', 'report.md', 'portable-manifest.json', 'portable-evidence.tar.gz',
         'REPRODUCE.md', 'relevant-input-binding.json', 'evidence-seal.json']
copies = [(destination / name, (phase / name).read_bytes()) for name in names]
for path, raw in copies:
    create(path, raw)
comparison_path = destination / 'metadata-carrier-byte-comparison.json'
create(comparison_path, dump(comparison))
owner_path = evidence / 'last-formal-main-original-owner-observation.json'
create(owner_path, (workspace / 'latest-original-owner-after-math-candidate.json').read_bytes())
cell = json.loads(cell_path.read_bytes())
assert cell['status'] == 'proved_locally' and cell['evidence']['independent_verification'] == ''
cell['evidence']['independent_native_review'] = {
    'report': str(destination / 'report.json'), 'report_sha256': sha(report_raw),
    'compiled_candidate': candidate, 'metadata_carrier_byte_comparison_head': head,
    'original_portable_manifest': str(destination / 'portable-manifest.json'),
    'original_raw_execution_archive': str(destination / 'portable-evidence.tar.gz'),
    'normal_VERIFIED_transition_performed': False,
}
cell['statement_seal']['status'] = 'EXACT_UNCHANGED_TYPES_COMPILED;INDEPENDENT_SOURCE_AND_FRESH_NATIVE_COMPLETE;API_NONPRISTINE_DISCLOSED'
cell['reader_contract']['status'] = 'Independent source review and six exact closed production static folds accepted, with the full private L11/81-line source and original blank T60 retained. Actual desktop/mobile/MathJax, global source-index/graph/copy/download delivery, serialized integration and purification remain HOLD.'
cell['purification']['dead_code_audit'] = 'All2 new handwritten declarations reachable, zero new generated helpers, standard axioms only. Full3-module native closure checks3 owned declarations. No global dead-code or post-merge purification claim.'
cell['purification']['canonicalization'] = 'One actual-row full-independence node, using the same existing canonical row-law node, materially consumed by the original closed-cutoff matrix images. No duplicate marginal law or public matrix wrapper.'
cell_path.write_bytes(dump(cell))
record = {
    'mathematical_native_candidate': candidate, 'PLOCAL_carrier': head,
    'source_metadata_commit': local_commit['reviewed_metadata_commit'],
    'native_reviewer': '/root/row_indep_native_74b8', 'original_report_sha256': sha(report_raw),
    'original_manifest_sha256': sha(manifest_raw), 'original_archive_sha256': sha(archive_raw),
    'exact_archive_members_verified': 461, 'selected_direct_originals_carried': len(copies),
    'full_native_owned_constants': 3, 'new_packet_owned_namespaces': 2,
    'new_handwritten_roots': 2, 'new_generated_reachable': 0,
    'formalizer_API_pristine': False, 'all_original_PLOCAL_evidence_unchanged': True,
    'foreign_full_states_preserved': len(states),
    'older_frontier_regular_files_preserved': len(baseline['all_existing_frontier_hashes']),
    'normal_VERIFIED_calls_by_root': 0, 'full_reader_integration_and_purification': 'HOLD',
}
record_path = evidence / 'actual-independent-native-review-attachment.json'
create(record_path, dump(record))
assert ledger.read_bytes() == before and discovery_path.read_bytes() == before_discoveries
paths = [cell_path, owner_path, comparison_path, record_path, *[p for p, _ in copies]]
subprocess.run(['git', 'add', '-f', '--', *map(str, paths)], check=True)
assert set(git('diff', '--cached', '--name-only').decode().splitlines()) == set(map(str, paths))
subprocess.run(['git', 'diff', '--cached', '--check', '--', str(cell_path), str(record_path)], check=True)
subprocess.run(['git', 'commit', '-m', 'Carry independent Gaussian joint-row native and static review'], check=True)
commit = git('rev-parse', 'HEAD').decode().strip()
for path in paths:
    assert git('show', f'{commit}:{path}') == path.read_bytes()
assert not git('diff', 'HEAD', '--name-only')
record['native_review_metadata_commit'] = commit
create(workspace / 'actual-independent-native-review-commit.json', dump(record))
print(json.dumps(record))
