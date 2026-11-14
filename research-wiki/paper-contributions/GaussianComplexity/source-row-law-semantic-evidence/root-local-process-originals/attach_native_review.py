"""Verify and carry exact independent native/static originals, with compile-credit scope."""
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
evidence = Path('research-wiki/paper-contributions/GaussianComplexity/source-row-law-semantic-evidence')
phase = Path('.astis/semantic-neutral-20261112/rl_native_52e9')
destination = evidence / 'native-review/rl_native_52e9'
cell_path = Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-row-law.json')
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
assert states.pop('ASTIS-SA-20261112-GaussianComplexitySourceRowLaw')['state'] == 'PROVED_LOCAL'
assert states == baseline['all_foreign_states']
for path, digest in baseline['all_existing_frontier_hashes'].items():
    assert sha(Path(path).read_bytes()) == digest, path
report_raw = (phase / 'report.original.json').read_bytes()
manifest_raw = (phase / 'portable-manifest.json').read_bytes()
archive_raw = (phase / 'portable-evidence.tar.gz').read_bytes()
assert sha(report_raw) == '74edceb44614716afc5bd13f090e322547b46b25129ccb3c7ebbddd0bfae9125'
assert sha(manifest_raw) == '3efa0e70017f1cde3cdf57b513a603955a1edfe45883332683fecae3a33e4caf'
assert sha(archive_raw) == '3e20649c6649f1ea283af7d43ecf9d4f9ebca0bb6a4343cc9911b9146cd7b049'
report, manifest = json.loads(report_raw), json.loads(manifest_raw)
candidate = 'd0654e9bbed44ab852fc44598560799949d8bd12'
assert report['checked_commit'] == manifest['checked_commit'] == candidate
assert report['compile_credit_only_for_checked_commit']
assert report['native']['module_owned_total'] == 18
assert report['native']['new_owned_total'] == 4 and report['native']['all_new_owned_reachable']
assert report['native']['new_handwritten'] == report['native']['new_generated'] == 2
assert report['native']['producer_ASTIS_parents'] == []
assert report['native']['consumer_ASTIS_parents'] == json.loads((evidence / 'publication-draft-record.json').read_bytes())['actual_public_ASTIS_parents']['_private.Tests.GaussianComplexityFixedSpectrumSourceRowLaw.0.AutoSamplingTheory.Tests.GaussianComplexityFixedSpectrumSourceRowLaw.actual_original_all_good_cutoff_probability']
assert report['native']['all_module_owned_types_bodies_closed_and_axioms_checked']
assert report['statement_seal']['both_author_exact_and_independent_literal_kernel_applications_passed']
assert report['static_reader']['all_details_initially_closed']
assert report['static_reader']['consumer_exact_full_module_lines'] == 145
assert len(report['static_reader']['six_steps']) == 6
assert set(report['native']['allowed_axioms']) == {'propext', 'Classical.choice', 'Quot.sound'}
assert len(manifest['files']) == 333
archive_prefix = manifest['root_name'] + '/'
with tarfile.open(phase / 'portable-evidence.tar.gz', 'r:gz') as archive:
    members = archive.getmembers()
    assert len(members) == 334
    expected = {archive_prefix + item['path'] for item in manifest['files']} | {archive_prefix + 'portable-manifest.json'}
    assert {m.name for m in members} == expected
    for member in members:
        relative = Path(member.name)
        assert member.isfile() and not relative.is_absolute() and '..' not in relative.parts
    assert archive.extractfile(archive_prefix + 'portable-manifest.json').read() == manifest_raw
    for item in manifest['files']:
        relative = Path(item['path'])
        assert not relative.is_absolute() and '..' not in relative.parts
        raw = (phase / relative).read_bytes()
        assert len(raw) == item['bytes'] and sha(raw) == item['sha256']
        assert archive.extractfile(archive_prefix + item['path']).read() == raw
full_dump = report['native']['full_dump']
full_dump_raw = (phase / full_dump['path']).read_bytes()
assert len(full_dump_raw) == full_dump['bytes'] and sha(full_dump_raw) == full_dump['sha256']
binding = json.loads((phase / 'relevant-input-binding.json').read_bytes())
assert binding['compile_candidate_only'] == candidate and not binding['later_carrier_compilation_claimed']
inputs = binding['tracked_relevant_input_hashes']
assert len(inputs) == 29
for item in inputs:
    path = Path(item['path'])
    raw = path.read_bytes()
    assert sha(raw) == item['sha256']
    assert git('show', f'{head}:{path}') == raw and git('show', f'{candidate}:{path}') == raw
comparison = {
    'compiled_candidate': candidate, 'later_metadata_HEAD': head,
    'new_native_compile_claimed_for_metadata_HEAD': False,
    'unchanged_relevant_inputs': inputs,
}
names = [
    'report.original.json', 'report.original.md', 'portable-manifest.json', 'portable-evidence.tar.gz',
    'REPRODUCE.md', 'relevant-input-binding.json', 'evidence-seal.json',
]
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
    'report': str(destination / 'report.original.json'), 'report_sha256': sha(report_raw),
    'compiled_candidate': candidate, 'metadata_carrier_byte_comparison_head': head,
    'original_portable_manifest': str(destination / 'portable-manifest.json'),
    'original_raw_execution_archive': str(destination / 'portable-evidence.tar.gz'),
    'normal_VERIFIED_transition_performed': False,
}
cell['statement_seal']['status'] = 'EXACT_UNCHANGED_TYPES_COMPILED;INDEPENDENT_SOURCE_AND_FRESH_NATIVE_COMPLETE;API_NONPRISTINE_DISCLOSED'
cell['reader_contract']['status'] = 'Independent source content and six exact closed production static folds accepted, with full private L14/145-line source export and original blank separators retained. Actual desktop/mobile/MathJax, full source-index/graph/copy/download/public delivery and purification remain HOLD.'
cell['purification']['dead_code_audit'] = 'All4 new declarations reachable, standard axioms only. Full5-module native closure checked18 owned declarations. Eight older authored RadonNikodym declarations are outside this consumer closure and remain unchanged; this is not a global dead-code judgment. No older generated unreachable auxiliaries. Post-merge purification pending.'
cell['purification']['canonicalization'] = 'One source-specific row-law node materially reused by its actual cutoff consumer; same existing canonical exponential moment reused. No new public tail/moment wrapper.'
cell_path.write_bytes(dump(cell))
record = {
    'mathematical_native_candidate': candidate, 'PLOCAL_carrier': head,
    'source_metadata_commit': local_commit['reviewed_metadata_commit'],
    'native_reviewer': report['reviewer'], 'original_report_sha256': sha(report_raw),
    'original_manifest_sha256': sha(manifest_raw), 'original_archive_sha256': sha(archive_raw),
    'exact_archive_members_verified': 334, 'selected_direct_originals_carried': len(copies),
    'full_native_owned_constants': 18, 'new_packet_owned_namespaces': 4,
    'new_handwritten_roots': 2, 'new_generated_reachable': 2,
    'older_authored_declarations_outside_consumer_closure_retained': 8,
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
subprocess.run(['git', 'commit', '-m', 'Carry independent Gaussian row-law native closure and static reader acceptance'], check=True)
commit = git('rev-parse', 'HEAD').decode().strip()
for path in paths:
    assert git('show', f'{commit}:{path}') == path.read_bytes()
assert not git('diff', 'HEAD', '--name-only')
record['native_review_metadata_commit'] = commit
create(workspace / 'actual-independent-native-review-commit.json', dump(record))
print(json.dumps(record))
