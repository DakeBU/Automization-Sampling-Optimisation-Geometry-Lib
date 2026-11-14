"""Carry the independent source actor's original report and complete audit overlay."""
from pathlib import Path
import copy
import hashlib
import json
import subprocess
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, 'tools')
import astis_semantic_roundtrip as semantic
import astis_publication as publication
import astis_advance as advance

workspace = Path(__file__).resolve().parent.relative_to(Path.cwd())
evidence = Path('research-wiki/paper-contributions/GaussianComplexity/source-matrix-mean-semantic-evidence')
audit_path = Path('research-wiki/semantic-roundtrip/audits/huanjian-gaussian-source-matrix-mean.json')
cell_path = Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-matrix-mean.json')
phase = Path('.astis/semantic-neutral-20261112/mm_src_8c31')
sha = lambda raw: hashlib.sha256(raw).hexdigest()
dump = lambda obj: (json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode()
git = lambda *args: subprocess.check_output(['git', *args])


def create(path, raw):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as out:
        out.write(raw)


expected = json.loads((workspace / 'expected-source-originals.json').read_bytes())
head = git('rev-parse', 'HEAD').decode().strip()
assert head == '5fb1440f771bdae77ad31f27b2275447fe3e89e5'
assert not git('diff', 'HEAD', '--name-only')
assert not git('diff', '--cached', '--name-only')
ledger = Path('runs/substantive_advances.jsonl')
before_ledger = ledger.read_bytes()
discovery_path = Path('runs/substantive_discoveries.jsonl')
before_discoveries = discovery_path.read_bytes()
baseline = json.loads((workspace / 'preproof-baseline.private.json').read_bytes())
states = advance._replay_advances([json.loads(x) for x in before_ledger.splitlines()])
assert states.pop('ASTIS-SA-20261112-GaussianComplexitySourceMatrixMean')['state'] == 'EXPLORING'
assert states == baseline['all_foreign_states']
for name, digest in baseline['all_existing_frontier_hashes'].items():
    assert sha(Path(name).read_bytes()) == digest, name
manifest_path = phase / expected['manifest_name']
manifest_raw = manifest_path.read_bytes()
assert sha(manifest_raw) == expected['manifest_sha256']
manifest = json.loads(manifest_raw)
files = []
for item in manifest['entries']:
    source, destination = Path(item['source']), Path(item['destination'])
    assert not source.is_absolute() and '..' not in source.parts and source.resolve().is_relative_to(Path.cwd())
    assert destination.is_relative_to(evidence / 'source-review/mm_src_8c31')
    assert not destination.is_absolute() and '..' not in destination.parts
    raw = source.read_bytes()
    assert not source.is_symlink() and len(raw) == item['bytes'] and sha(raw) == item['sha256']
    if destination.exists():
        assert not destination.is_symlink() and destination.read_bytes() == raw
    files.append((destination, raw))
assert len(files) == manifest['exact_count'] == expected['entry_count']
overlay_raw = (phase / expected['overlay_name']).read_bytes()
assert sha(overlay_raw) == expected['overlay_sha256']
overlay = json.loads(overlay_raw)
fields = {'state', 'semantic_slots', 'deltas', 'verdict', 'source_review', 'repairs'}
assert set(overlay) == fields
assert overlay['state'] == 'source-reviewed' and overlay['source_review']['state'] == 'accepted'
assert overlay['verdict'] == 'equivalent-after-elaboration'
assert overlay['deltas'] == overlay['repairs'] == []
assert overlay['source_review']['reviewer'] == '/root/mm_fresh_source_8c31'
assert overlay['source_review']['reviewer_packet_sha256'] == '0d8f3df6fc7d9e27bfb4c31c24f5cd87a20fd4d35f3adc365c59e8e40eb9c226'
assert overlay['source_review']['review_run_sha256'] == expected['report_sha256']
assert sha((phase / expected['report_name']).read_bytes()) == expected['report_sha256']
before_audit = audit_path.read_bytes()
audit = json.loads(before_audit)
assert audit['publication_binding_sha256'] == 'c0e0e354793ad6c2901a23c28c58d1bae8a63bf682d8645ce6e555d2d96df834'
candidate_registry = copy.deepcopy(semantic.load_registry())
matches = [a for a in candidate_registry['audits'] if a['id'] == audit['id']]
assert len(matches) == 1
matches[0].update(overlay)
errors = semantic.validate_registry(candidate_registry)
assert not errors, errors
create(workspace / 'audit-before-source-overlay.original.json', before_audit)
for path, raw in files:
    if not path.exists():
        create(path, raw)
self_copy = Path(manifest['manifest_destination'])
assert self_copy.is_relative_to(evidence / 'source-review/mm_src_8c31')
if self_copy.exists():
    assert not self_copy.is_symlink() and self_copy.read_bytes() == manifest_raw
else:
    create(self_copy, manifest_raw)
manifest_copy = evidence / 'independent-source-review-portable-custody.original.json'
create(manifest_copy, manifest_raw)
audit.update(overlay)
audit_path.write_bytes(dump(audit))
publication.inputs.cache_clear()
publication.load.cache_clear()
publication.check_advance([audit['lean']['declaration']], reviewed=True)
cell = json.loads(cell_path.read_bytes())
assert cell['status'] == 'claimed' and cell['evidence']['independent_verification'] == ''
cell['evidence']['independent_source_review'] = {
    'report': overlay['source_review']['run_artifact'],
    'report_sha256': overlay['source_review']['review_run_sha256'],
    'overlay_sha256': sha(overlay_raw), 'custody_manifest': str(manifest_copy),
    'reviewed_publication_binding_sha256': audit['publication_binding_sha256'],
}
cell['reader_contract']['status'] = 'Independent source content and whole-module proof review accepted. Six exact adjacent Lean folds and the full source export include the complete private158-line actual sum-integral consumer. Native/static evidence is handled separately; actual desktop/mobile/source-index/graph delivery remains pending.'
cell['source_proof_coverage'] = {
    'inventory_archive': str(evidence / 'preproof-source-types-topology-local-build.original-files.tar.gz'),
    'inventory_member': '.astis/semantic-neutral-20261112/mm_sg_61c4/raw-freeze-v1/atomic-inventory.json',
    'reviewed_nodes': 'Independent raw, type-only and distinct topology freezes, then fresh whole-module and anti-anchored source review.',
    'excluded_with_reason': 'All79 bounded atoms retain44NODE and35EXCLUDED dispositions. Distinct topology challenge checked62nodes/94edges and463locator occurrences, including both formal roots and separate source correspondence endpoints. Canonical row/moment/frame identities retain their existing credit.',
    'source_gaps': 'Actual row-law and retained scalar/matrix moment applicability, actual matrix integrability, selected CLM expectation route, literal frame and actual finite integral exchange are compiled and independently source-reviewed. The entrywise OR route is unselected, not an extra requirement. Arbitrary ambient transfer, public aggregate canonicalization, centered variance/concentration and main bounds remain open.',
    'alternative_routes': [], 'exact_source_and_Lean_map': str(evidence / 'source-lean-map.draft.json'),
}

cell['proof_digestion'] = {
    'existing_substrate': [*cell['parents'], 'MeasurePreserving.integrable_comp_of_integrable', 'integral_map',
                           'ContinuousLinearMap.integrable_comp', 'ContinuousLinearMap.integral_comp_comm',
                           'Matrix.kroneckerBilinear', 'Matrix.one_kronecker_one', 'integrable_finsetSum', 'integral_finsetSum', 'integral_smul'],
    'bookkeeping': ['Literal same-experiment row pushforward and noninjective moment transport',
                    'Fixed Gaussian-first tensor CLM and exact closed-cutoff image',
                    'Exact half-grid/frame application and paired-identity normalization',
                    'Actual finite-sum integrability and Bochner/scalar exchange'],
    'new_reusable': [],
    'new_topology': 'Same canonical row-law and truncated moment yield actual Yi integrability/means, materially consumed with the same cosine-frame node in both actual finite-sum expectation identities.',
}
cell['purification'] = {
    'status': 'pending', 'dead_code_audit': 'Strict exact probe checks2 handwritten roots and1 emitted internal helper closed/reachable with standard axioms. Independent full fresh native closure remains separate.',
    'duplicate_semantics_audit': 'One canonical existing row-law, radial moment and frame node each reused. The old private canonical-row matrix application remains immutable history without duplicate public credit.',
    'canonicalization': 'Source-specific actual original-experiment matrix means with a real two-sum Bochner expectation consumer.',
    'compressed_spine_delta': 'Exact row pushforward and retained moment -> fixed tensor CLM -> actual Yi means -> source cosine tensor sums -> actual finite-sum integrals.',
    'reader_default_view': 'Compact individual means with six source-ordered formula/Lean folds and the complete158-line private source at L17.',
}
cell_path.write_bytes(dump(cell))
record = {
    'kind': 'Exact independent source review attachment', 'mathematical_candidate': head,
    'reviewer': overlay['source_review']['reviewer'],
    'original_math_report_sha256': overlay['source_review']['review_run_sha256'],
    'original_complete_overlay_sha256': sha(overlay_raw),
    'original_portable_manifest_sha256': sha(manifest_raw), 'portable_originals_copied': len(files),
    'projected_audit_fields': sorted(fields), 'actual_core_schema_validation_errors': 0,
    'source_reviewed_publication_gate': 'Actual check_advance reviewed=True passed.',
    'Lean_code_source_map_publication_and_decoder_unchanged': True,
    'normal_VERIFIED_calls': 0, 'normal_PROVED_LOCAL_calls': 0,
    'actual_browser_integration_and_purification': 'HOLD',
}
record_path = evidence / 'actual-independent-source-review-attachment.json'
create(record_path, dump(record))
assert ledger.read_bytes() == before_ledger and discovery_path.read_bytes() == before_discoveries
for name, digest in baseline['all_existing_frontier_hashes'].items():
    assert sha(Path(name).read_bytes()) == digest
paths = [audit_path, cell_path, *sorted(p for p in evidence.rglob('*') if p.is_file())]
assert len(paths) == len(set(paths))
expected_changes = set()
for path in paths:
    prior = subprocess.run(['git', 'show', f'{head}:{path}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if prior.returncode or prior.stdout != path.read_bytes():
        expected_changes.add(str(path))
subprocess.run(['git', 'add', '-f', '--', *map(str, paths)], check=True)
assert set(git('diff', '--cached', '--name-only').decode().splitlines()) == expected_changes
subprocess.run(['git', 'diff', '--cached', '--check', '--', str(audit_path), str(cell_path), str(record_path)], check=True)
subprocess.run(['git', 'commit', '-m', 'Attach independent actual Gaussian matrix-mean source and reader review'], check=True)
commit = git('rev-parse', 'HEAD').decode().strip()
for path in paths:
    assert git('show', f'{commit}:{path}') == path.read_bytes()
assert not git('diff', 'HEAD', '--name-only')
record['source_review_metadata_commit'] = commit
create(workspace / 'actual-independent-source-review-commit.json', dump(record))
print(json.dumps(record))
