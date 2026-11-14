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
evidence = Path('research-wiki/paper-contributions/GaussianComplexity/source-row-law-semantic-evidence')
audit_path = Path('research-wiki/semantic-roundtrip/audits/huanjian-gaussian-source-row-law.json')
cell_path = Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-row-law.json')
phase = Path('.astis/semantic-neutral-20261112/rl_src_3dd4')
sha = lambda raw: hashlib.sha256(raw).hexdigest()
dump = lambda obj: (json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode()
git = lambda *args: subprocess.check_output(['git', *args])


def create(path, raw):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as out:
        out.write(raw)


expected = json.loads((workspace / 'expected-source-originals.json').read_bytes())
head = git('rev-parse', 'HEAD').decode().strip()
assert head == 'd0654e9bbed44ab852fc44598560799949d8bd12'
assert set(git('diff', 'HEAD', '--name-only').decode().splitlines()) == {str(audit_path)}
assert not git('diff', '--cached', '--name-only')
ledger = Path('runs/substantive_advances.jsonl')
before_ledger = ledger.read_bytes()
discovery_path = Path('runs/substantive_discoveries.jsonl')
before_discoveries = discovery_path.read_bytes()
baseline = json.loads((workspace / 'preproof-baseline.private.json').read_bytes())
states = advance._replay_advances([json.loads(x) for x in before_ledger.splitlines()])
assert states.pop('ASTIS-SA-20261112-GaussianComplexitySourceRowLaw')['state'] == 'EXPLORING'
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
    assert source.is_relative_to(phase) and destination.is_relative_to(evidence / 'source-review/rl_src_3dd4')
    raw = source.read_bytes()
    assert not source.is_symlink() and len(raw) == item['bytes'] and sha(raw) == item['sha256']
    if destination.exists():
        assert not destination.is_symlink() and destination.read_bytes() == raw
    files.append((destination, raw))
assert len(files) == manifest['originals_count'] == expected['entry_count']
overlay_raw = (phase / expected['overlay_name']).read_bytes()
assert sha(overlay_raw) == expected['overlay_sha256']
overlay = json.loads(overlay_raw)
fields = {'state', 'semantic_slots', 'deltas', 'verdict', 'source_review', 'repairs'}
assert set(overlay) == fields
assert overlay['state'] == overlay['source_review']['state'] == 'accepted'
assert overlay['verdict'] == 'equivalent-after-elaboration'
assert overlay['deltas'] == overlay['repairs'] == []
assert overlay['source_review']['reviewer'] == '/root/row_law_fresh_source_3dd4'
assert overlay['source_review']['reviewer_packet_sha256'] == '57526c79133302068b87c1de935502e1ea9f64d5cb96aaa8ef7c16ee338fea40'
assert overlay['source_review']['review_run_sha256'] == expected['report_sha256']
assert sha((phase / expected['report_name']).read_bytes()) == expected['report_sha256']
before_audit = audit_path.read_bytes()
audit = json.loads(before_audit)
assert audit['publication_binding_sha256'] == 'f86fb828622e7c5c6e34ae2cb49dc1a6428d94701d36d7bb81a523861d48e419'
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
self_copy = evidence / 'source-review/rl_src_3dd4/portable-originals-manifest.json'
assert self_copy.is_relative_to(evidence / 'source-review/rl_src_3dd4')
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
cell['reader_contract']['status'] = 'Independent source content and whole-module proof review accepted. Six exact adjacent Lean folds and the full source export include the complete private145-line same-experiment consumer. Native/static evidence is handled separately; actual desktop/mobile/source-index/graph delivery remains pending.'
cell['source_proof_coverage'] = {
    'inventory_archive': str(evidence / 'preproof-source-types-topology-local-build.original-files.tar.gz'),
    'inventory_member': '.astis/semantic-neutral-20261112/rl_sg_6a90/bounded_inventory.json',
    'reviewed_nodes': 'Independent raw, type-only and distinct topology freezes, then fresh whole-module and anti-anchored source review.',
    'excluded_with_reason': 'All145 bounded source atoms retain19NODE and126EXCLUDED dispositions with196 locators. Narrow row marginals do not cover source joint-row independence.',
    'source_gaps': 'Bounded row-measurability/pushforward, actual exponential integrability/mean transport, strict tails, finite union and measurable closed complement are compiled and source-reviewed. Joint-row independence, arbitrary extended-ambient transfer and matrix-expectation adapters remain open.',
    'alternative_routes': [], 'exact_source_and_Lean_map': str(evidence / 'source-lean-map.draft.json'),
}
cell['proof_digestion'] = {
    'existing_substrate': [*cell['parents'], 'measurePreserving_eval', 'measurePreserving_pi', 'integral_map', 'meas_ge_le_lintegral_div'],
    'bookkeeping': ['Literal coordinate and finite-product measure-map composition', 'Euclidean row wrapping', 'Noninjective exponential integral transport', 'Exact cutoff calibration and ENNReal complement arithmetic'],
    'new_reusable': [],
    'new_topology': 'The source-experiment marginal adapter is materially consumed with the canonical exponential node to prove the actual simultaneous cutoff event under the same product law.',
}
cell['purification'] = {
    'status': 'pending', 'dead_code_audit': 'Strict final focused probe checks all4 new declarations reachable; fresh whole-import native closure acceptance pending.',
    'duplicate_semantics_audit': 'Reuse the canonical exponential moment; no new public moment or individual-tail wrapper.',
    'canonicalization': 'Source-specific literal coordinate-row law with a real same-experiment cutoff consumer.',
    'compressed_spine_delta': 'Gaussian coordinate/product projection to row law, then moment transport, Markov and finite union.',
    'reader_default_view': 'Compact row-law and cutoff statements with six source-ordered folded formula/Lean steps.',
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
subprocess.run(['git', 'commit', '-m', 'Attach independent Gaussian row-law source decoding and full module review'], check=True)
commit = git('rev-parse', 'HEAD').decode().strip()
for path in paths:
    assert git('show', f'{commit}:{path}') == path.read_bytes()
assert not git('diff', 'HEAD', '--name-only')
record['source_review_metadata_commit'] = commit
create(workspace / 'actual-independent-source-review-commit.json', dump(record))
print(json.dumps(record))
