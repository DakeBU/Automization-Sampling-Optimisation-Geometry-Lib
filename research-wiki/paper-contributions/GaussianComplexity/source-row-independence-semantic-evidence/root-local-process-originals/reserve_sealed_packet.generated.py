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
evidence = paper / 'source-row-independence-semantic-evidence'
seal_path = paper / 'source-row-independence-statement-seal.json'
cell_path = Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-row-independence.json')
ledger = Path('runs/substantive_advances.jsonl')
advance_id = 'ASTIS-SA-20261112-GaussianComplexitySourceRowIndependence'
owner = 'huanjian_gc_20261112_source_row_independence'
sha = lambda b: hashlib.sha256(b).hexdigest()
dump = lambda obj: (json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode()
git = lambda *args: subprocess.check_output(['git', *args])


def create(path, raw):
    with path.open('xb') as out:
        out.write(raw)


head = git('rev-parse', 'HEAD').decode().strip()
assert head == '6ef180f7495ef79e1f70bac7909036fc6f7f73bc'
assert not git('diff', 'HEAD', '--name-only') and not git('diff', '--cached', '--name-only')
seal_raw = seal_path.read_bytes()
assert sha(seal_raw) == '88a55849ce9e13a9a04edff6aac13ce32d4370712b1b7a422fba0d570ff0b25e'
seal = json.loads(seal_raw)
P, T = [seal[k]['planned_file'] for k in ('producer', 'actual_private_consumer')]
assert not Path(P).exists() and not Path(T).exists() and not cell_path.exists()
ledger_raw = ledger.read_bytes()
assert sha(ledger_raw) == '138bad640d592e268d0c770a91cf113237920c9d79e4115ce13593924565dda3'
states = advance._replay_advances([json.loads(x) for x in ledger_raw.splitlines()])
assert len(states) == 306 and advance_id not in states
assert states['ASTIS-SA-20261112-GaussianComplexitySourceRowLaw']['state'] == 'VERIFIED'
older = {str(p): sha(p.read_bytes()) for p in cell_path.parent.rglob('*')
         if p.is_file() and not p.is_symlink()}
assert len(older) == 466
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
    'Samplinglib exact canonical FixedSpectrumSourceRowLaw.actual_source_row_marginal_law is compiled and known from the previous packet, including row measurability; its whole code/API exposure is disclosed. It does not prove joint independence.',
    'Mathlib literal iIndepFun and its kernel/finite-intersection meanings, product measurable structures, finite product Gaussian law and real-entry matrix definitions were audited with actual current prints/instances. New proof API retrieval waits for source/type/topology acceptance and normal intake.',
    'Bounded GaussianComplexity Row filename inventory found existing TruncatedRowMoment and SourceRowLaw; the proposed SourceRowIndependence production/test files do not exist. No new independence proof implementation has been attempted.',
]

slug = 'huanjian-gaussian-source-row-independence.json'
cell.update({
    'cell_id': cell_path.stem, 'title': 'Original Gaussian row joint independence and actual truncated-matrix independence',
    'source_anchor': 'arXiv2610.20492v1 C.2 p1 joint independence and p12 first sentence/Ex107 actual independent truncated matrices; standing integer query range',
    'target_statement': seal['producer']['signature'] + '\nPrivate actual consumer\n' + seal['actual_private_consumer']['signature'],
    'status': 'claimed', 'owner_id': owner, 'advance_id': advance_id,
    'reservation_only': 'Exact-type reservation, normal ledger intake has not occurred.',
    'parents': [], 'consumers': [seal['actual_private_consumer']['name']],
    'shared_floor_audit': {'searched': searches, 'classification': 'adapt', 'decision': 'new_route_local',
                           'canonical_declaration': seal['producer']['name'], 'canonical_shared_cell': ''},
    'reuse_plan': {'searched_existing': searches, 'reused_declarations': [],
                  'planned_existing_parents': [seal['shared_floor_audit']['known_existing_node']],
                  'new_shared_declarations': [], 'known_consumers': [],
                  'planned_consumers': [seal['actual_private_consumer']['name']],
                  'no_duplicate_wrapper': True,
                  'decision_reason': 'The existing marginal-law node is canonical. Complement it with full independence of the literal physical-row family and consume that result in actual source Yi measurability/independence; no duplicate marginal theorem or independence certificate input.'},
    'source_detail_audit': {
        'primary_edition': 'arXiv2610.20492v1 raw SHA ' + seal['source']['raw_sha256'],
        'primary_anchor': 'C.2 p1 and p12 first sentence/Ex107, with literal grid and cutoff definitions',
        'detail_status': 'omitted',
        'gap': 'Source omits the product-coordinate regrouping/full joint independence and measurable truncated-matrix composition details. These need actual internal proofs; marginals alone do not supply independence.',
        'consulted': [{'source': 'Pinned original source and literal canonical definitions',
                       'anchor': 'C.2 row experiment/Ex107 and actual iIndepFun/kernel/product/matrix-entry meanings',
                       'hypothesis_adapter': 'All rows and Yi use one actual product experiment. Establish full row independence and derive measurability/independence of literal Yi internally, q=0 included; no law, Gram/norm, tau/kappa or independence certificate input.'}],
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
cell['reader_contract']['status'] = 'Prospective exact joint-independence statement and actual Yi consumer; formula explanation and adjacent Lean follow actual proof.'
cell['graph_contribution']['focus_targets'] = [seal['producer']['name']]
cell['graph_contribution']['visual_review'] = 'Preliminary raw reading and newly sealed exact types only; formal graph/type/topology review pending. Actual compiled independence/consumer edges require the new proof.'
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
