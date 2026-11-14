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
evidence = Path('research-wiki/paper-contributions/GaussianComplexity/source-row-independence-semantic-evidence')
audit_path = Path('research-wiki/semantic-roundtrip/audits/huanjian-gaussian-source-row-independence.json')
cell_path = Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-row-independence.json')
phase = Path('.astis/semantic-neutral-20261112/ri_src_5ab9')
sha = lambda raw: hashlib.sha256(raw).hexdigest()
dump = lambda obj: (json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode()
git = lambda *args: subprocess.check_output(['git', *args])


def create(path, raw):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as out:
        out.write(raw)


expected = json.loads((workspace / 'expected-source-originals.json').read_bytes())
head = git('rev-parse', 'HEAD').decode().strip()
assert head == '66e0bb9b748d68816a8443d60696656c9340222f'
assert not git('diff', 'HEAD', '--name-only')
assert not git('diff', '--cached', '--name-only')
ledger = Path('runs/substantive_advances.jsonl')
before_ledger = ledger.read_bytes()
discovery_path = Path('runs/substantive_discoveries.jsonl')
before_discoveries = discovery_path.read_bytes()
baseline = json.loads((workspace / 'preproof-baseline.private.json').read_bytes())
states = advance._replay_advances([json.loads(x) for x in before_ledger.splitlines()])
assert states.pop('ASTIS-SA-20261112-GaussianComplexitySourceRowIndependence')['state'] == 'EXPLORING'
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
    assert destination.is_relative_to(evidence / 'source-review/ri_src_5ab9')
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
assert overlay['source_review']['reviewer'] == '/root/row_indep_fresh_source_5ab9'
assert overlay['source_review']['reviewer_packet_sha256'] == '51f818cce1189763710d937ce87ef07808c728984c5f93f7da4279054b037210'
assert overlay['source_review']['review_run_sha256'] == expected['report_sha256']
assert sha((phase / expected['report_name']).read_bytes()) == expected['report_sha256']
before_audit = audit_path.read_bytes()
audit = json.loads(before_audit)
assert audit['publication_binding_sha256'] == 'd90576df8ae217ca7cb9ce631cdca049780f3a706510afbe2f72a71dd1c03829'
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
assert self_copy.is_relative_to(evidence / 'source-review/ri_src_5ab9')
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
cell['reader_contract']['status'] = 'Independent source content and whole-module proof review accepted. Six exact adjacent Lean folds and the full source export include the complete private81-line actual matrix consumer. Native/static evidence is handled separately; actual desktop/mobile/source-index/graph delivery remains pending.'
cell['source_proof_coverage'] = {
    'inventory_archive': str(evidence / 'preproof-source-types-topology-local-build.original-files.tar.gz'),
    'inventory_member': '.astis/semantic-neutral-20261112/ri_sg_78c2/raw-freeze-v1/inventory.json',
    'reviewed_nodes': 'Independent raw, type-only and distinct topology freezes, then fresh whole-module and anti-anchored source review.',
    'excluded_with_reason': 'All83 bounded atoms retain17NODE and66EXCLUDED dispositions. Distinct topology challenge checked all30nodes/33edges and472locator occurrences. Marginal-law source context remains separate canonical credit.',
    'source_gaps': 'All10 bounded coordinate-product/regrouping/full-row-independence and actual-Y/measurability/image-independence ports are compiled and independently source-reviewed. Arbitrary ambient transfer, matrix-expectation adapters, centered variance/concentration and main bounds remain open.',
    'alternative_routes': [], 'exact_source_and_Lean_map': str(evidence / 'source-lean-map.draft.json'),
}

cell['proof_digestion'] = {
    'existing_substrate': [*cell['parents'], 'map_pi_eq_stdGaussian', 'measurePreserving_pi',
                           'Measure.infinitePi_map_curry_symm', 'measurePreserving_piCongrLeft',
                           'Measure.infinitePi_map_curry', 'iIndepFun_iff_map_fun_eq_pi_map', 'iIndepFun.comp'],
    'bookkeeping': ['Full physical-coordinate Gaussian product identification', 'Flatten/swap/regroup of the same finite scalar array',
                    'Euclidean row wrapping and exact joint product transport', 'Actual finite-entry closed-cutoff polynomial measurability and composition'],
    'new_reusable': [],
    'new_topology': 'Existing canonical row law plus full joint coordinate regrouping yields actual row independence, materially consumed by the exact source truncated-matrix measurable images.',
}
cell['purification'] = {
    'status': 'pending', 'dead_code_audit': 'Strict focused probe checks both handwritten roots reachable, with no generated owned helper; full native transitive closure review pending.',
    'duplicate_semantics_audit': 'Reuse the same canonical row-law node and Mathlib product/independence declarations. No second marginal-law proof or public matrix wrapper.',
    'canonicalization': 'Source-specific full-row independence with actual Ex107 matrix-independence consumer.',
    'compressed_spine_delta': 'Full Gaussian coordinate product, finite regrouping and joint-law independence, then separate measurable nonlinear images.',
    'reader_default_view': 'Compact independence conclusions with six source-ordered formula/Lean folds and full81-line private source export.',
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
subprocess.run(['git', 'commit', '-m', 'Attach independent Gaussian joint-row independence source and module review'], check=True)
commit = git('rev-parse', 'HEAD').decode().strip()
for path in paths:
    assert git('show', f'{commit}:{path}') == path.read_bytes()
assert not git('diff', 'HEAD', '--name-only')
record['source_review_metadata_commit'] = commit
create(workspace / 'actual-independent-source-review-commit.json', dump(record))
print(json.dumps(record))
