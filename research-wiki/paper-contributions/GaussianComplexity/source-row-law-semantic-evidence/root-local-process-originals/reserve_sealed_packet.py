"""Reserve the exact source-experiment target, preserving every prior state."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, 'tools')
import astis_advance as advance
import astis_frontier_cells as frontiers

workspace = Path(__file__).resolve().parent.relative_to(Path.cwd())
paper = Path('research-wiki/paper-contributions/GaussianComplexity')
evidence = paper / 'source-row-law-semantic-evidence'
seal_path = paper / 'source-row-law-statement-seal.json'
cell_path = Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-row-law.json')
ledger = Path('runs/substantive_advances.jsonl')
advance_id = 'ASTIS-SA-20261112-GaussianComplexitySourceRowLaw'
owner = 'huanjian_gc_20261112_source_row_law'
sha = lambda b: hashlib.sha256(b).hexdigest()
dump = lambda obj: (json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode()
git = lambda *args: subprocess.check_output(['git', *args])


def create(path, raw):
    with path.open('xb') as out:
        out.write(raw)


head = git('rev-parse', 'HEAD').decode().strip()
assert head == '60a86f45ca29cd5cae96e59e8b14975674f59df9'
assert not git('diff', 'HEAD', '--name-only') and not git('diff', '--cached', '--name-only')
seal_raw = seal_path.read_bytes()
assert sha(seal_raw) == 'f9476ec7454a0927d3a1068226ad635b464d9b5d631f4992421d4b3b39b70ec3'
seal = json.loads(seal_raw)
P, T = [seal[k]['planned_file'] for k in ('producer', 'actual_private_consumer')]
assert not Path(P).exists() and not Path(T).exists() and not cell_path.exists()
ledger_raw = ledger.read_bytes()
assert sha(ledger_raw) == '2d07278f66962c1f106c5f498d8d970e3aedc7d9e5ca27715da0c5c3483d4112'
states = advance._replay_advances([json.loads(x) for x in ledger_raw.splitlines()])
assert len(states) == 305 and advance_id not in states
assert states['ASTIS-SA-20261112-GaussianComplexityWeightedCosineFrame']['state'] == 'VERIFIED'
older = {str(p): sha(p.read_bytes()) for p in cell_path.parent.rglob('*')
         if p.is_file() and not p.is_symlink()}
assert len(older) == 465
create(workspace / 'preproof-baseline.private.json', dump({
    'head': head, 'ledger_bytes': len(ledger_raw), 'ledger_sha256': sha(ledger_raw),
    'all_foreign_states': states, 'all_existing_frontier_hashes': older,
    'tracked_git_index': git('ls-files', '--stage').decode(),
    'scope': 'Private complete preservation state, never export the foreign replay or tracked-index inventory.',
}))
discovery_raw = Path('runs/substantive_discoveries.jsonl').read_bytes()
discoveries = advance._replay_discoveries([json.loads(x) for x in discovery_raw.splitlines()])
assert len(discoveries) == 43
create(workspace / 'preproof-discoveries.private.json', dump({
    'ledger_sha256': sha(discovery_raw), 'ledger_bytes': len(discovery_raw),
    'full_states': discoveries, 'scope': 'Private complete preservation guard, never export full foreign states.',
}))
template = Path('.astis/huanjian-gc-weighted-cosine-frame-20261112/reserved-cell.description-attempt1.original.json')
cell = json.loads(template.read_bytes())
searches = [
    'Samplinglib canonical StdGaussianRadialExponential.integrable_exp_norm_sq_div_three_and_integral_stdGaussian signature: both exponential integrability and exact mean are already compiled and will be reused by the consumer.',
    'Mathlib literal standard Gaussian, Euclidean coordinate wrapper, finite product measure, product measurable space and MeasurePreserving output fields were audited; actual product-probability and factor sigma-finite instances synthesized.',
    'No existing GaussianComplexity RowLaw module found by bounded filename lookup. New target proof APIs and implementation remain untouched pending independent type/topology acceptance and normal intake.',
]
slug = 'huanjian-gaussian-source-row-law.json'
cell.update({
    'cell_id': cell_path.stem, 'title': 'Original Gaussian column-experiment row laws and global good cutoff event',
    'source_anchor': 'arXiv2610.20492v1 C.2 p1 row construction and p10 Ex104/Ex105 with the printed probability0.999, under the standing integer query range',
    'target_statement': seal['producer']['signature'] + '\nPrivate actual consumer\n' + seal['actual_private_consumer']['signature'],
    'status': 'claimed', 'owner_id': owner, 'advance_id': advance_id,
    'reservation_only': 'Exact-type reservation, normal ledger intake has not occurred.',
    'parents': [], 'consumers': [seal['actual_private_consumer']['name']],
    'shared_floor_audit': {'searched': searches, 'classification': 'adapt', 'decision': 'new_route_local',
                           'canonical_declaration': seal['producer']['name'], 'canonical_shared_cell': ''},
    'reuse_plan': {'searched_existing': searches, 'reused_declarations': [],
                  'planned_existing_parents': [seal['shared_floor_audit']['existing_canonical_consumer_parent']],
                  'new_shared_declarations': [], 'known_consumers': [],
                  'planned_consumers': [seal['actual_private_consumer']['name']],
                  'no_duplicate_wrapper': True,
                  'decision_reason': 'The source-specific coordinate row map has a fixed original column-product law. Prove its actual measurable Gaussian marginal transport and consume it in the same experiment global truncation event, reusing the canonical exponential moment.'},
    'source_detail_audit': {
        'primary_edition': 'arXiv2610.20492v1 raw SHA ' + seal['source']['raw_sha256'],
        'primary_anchor': 'C.2 p1 and p10 Ex104/Ex105',
        'detail_status': 'omitted',
        'gap': 'Source row-law identification, canonical product realization, measurability, exponential-moment/tail transport, finite union and closed good-event complement need internal formal proofs.',
        'consulted': [{'source': 'Pinned original source and literal canonical definitions',
                       'anchor': 'C.2 row experiment, actual Measure.pi and MeasurePreserving meanings',
                       'hypothesis_adapter': 'All rows use one concrete tuple of independent standard Gaussian columns. Derive marginal laws and tails internally, retain q=0, add no tau-smallness or law certificate.'}],
        'fidelity_boundary': seal['scope_boundary'],
    },
    'statement_seal': {'status': seal['state'], 'file': str(seal_path), 'sha256': sha(seal_raw),
                       'signature_sha256': seal['producer']['signature_sha256'],
                       'private_consumer_signature_sha256': seal['actual_private_consumer']['signature_sha256']},
    'evidence': {'actual_literal_formation': seal['actual_statement_formation'],
                 'actual_definition_meaning': seal['actual_definition_meaning'],
                 'new_target_proof_attempts': 0, 'formalizer_API_pristine': False},
    'owned_files': [P, T, str(seal_path), str(cell_path), str(evidence) + '/',
                    'website/content/declaration_lessons/' + slug, 'website/content/publications/' + slug,
                    'research-wiki/semantic-roundtrip/audits/' + slug],
    'truth_boundary': seal['scope_boundary'], 'conceptual_mirror_audit': {'status': 'pending'},
})
cell['reader_contract']['status'] = 'Prospective original experiment statement, source formula steps and exact adjacent Lean after actual proof.'
cell['graph_contribution']['focus_targets'] = [seal['producer']['name']]
cell['graph_contribution']['visual_review'] = 'Independent raw source and exact types only. Actual compiled law/consumer edges require the new proof.'
create(cell_path, dump(cell))
errors = frontiers.validate_cells(frontiers.load_cells())
assert not errors, errors
assert ledger.read_bytes() == ledger_raw
assert Path('runs/substantive_discoveries.jsonl').read_bytes() == discovery_raw
for name, digest in older.items():
    assert sha(Path(name).read_bytes()) == digest, name
summary = {
    'baseline_commit': head, 'exact_seal_sha256': sha(seal_raw),
    'cell': str(cell_path), 'cell_sha256': sha(cell_path.read_bytes()),
    'foreign_full_states_guarded': len(states), 'older_frontier_files_guarded': len(older),
    'discovery_states_guarded': len(discoveries), 'normal_API_and_proof_calls': 0,
    'independent_topology_acceptance': 'pending',
}
create(workspace / 'actual-seal-and-reservation-summary.json', dump(summary))
print(json.dumps(summary))
