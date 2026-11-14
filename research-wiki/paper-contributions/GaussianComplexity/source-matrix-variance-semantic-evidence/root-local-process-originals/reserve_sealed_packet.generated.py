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
evidence = paper / 'source-matrix-variance-semantic-evidence'
seal_path = paper / 'source-matrix-variance-statement-seal.json'
cell_path = Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-matrix-variance.json')
ledger = Path('runs/substantive_advances.jsonl')
advance_id = 'ASTIS-SA-20261112-GaussianComplexitySourceMatrixVariance'
owner = 'huanjian_gc_20261112_source_matrix_variance'
sha = lambda b: hashlib.sha256(b).hexdigest()
dump = lambda obj: (json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode()
git = lambda *args: subprocess.check_output(['git', *args])


def create(path, raw):
    with path.open('xb') as out:
        out.write(raw)


head = git('rev-parse', 'HEAD').decode().strip()
expected = json.loads((workspace / 'expected-reservation-baseline.json').read_bytes())
assert head == expected['head']
assert not git('diff', 'HEAD', '--name-only') and not git('diff', '--cached', '--name-only')
seal_raw = seal_path.read_bytes()
assert sha(seal_raw) == '5f905cafe6035238cebdedd4f841e87b703e741b4c8aa204471d89e4c07e8a14'
seal = json.loads(seal_raw)
P, T = [seal[k]['planned_file'] for k in ('producer', 'actual_private_consumer')]
assert not Path(P).exists() and not Path(T).exists() and not cell_path.exists()
ledger_raw = ledger.read_bytes()
assert sha(ledger_raw) == expected['ledger_sha256']
states = advance._replay_advances([json.loads(x) for x in ledger_raw.splitlines()])
assert len(states) == 308 and advance_id not in states
assert states['ASTIS-SA-20261112-GaussianComplexitySourceMatrixMean']['state'] == 'VERIFIED'
older = {str(p): sha(p.read_bytes()) for p in cell_path.parent.rglob('*')
         if p.is_file() and not p.is_symlink()}
assert len(older) == 468
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
    'Samplinglib/ASTIS prior canonical Gaussian row law, radial fourth moment matrix and weighted cosine coefficient bound are compiled and known from the prior accepted packets. Actual matrix means are independently VERIFIED. Their exact identities are reused; prior proof/API exposure is disclosed.',
    'Samplinglib/ASTIS old private canonical-row uncentered aggregate remains immutable history. The new packet concerns literal physical rows on the actual original product law, then genuine centered/cosine-weighted operator-norm variance conclusions. No duplicate canonical public radial/frame lemma credit.',
    'Mathlib exact standard definition and actual-instance prints cover ordinary finite matrix multiplication, full PosSemidef, integrability/Bochner meaning and L2Operator norm/completeness. New-target generic matrix variance/PSD-to-norm API retrieval is pending exact source graph/topology admission; no new target implementation yet.',
]

slug = 'huanjian-gaussian-source-matrix-variance.json'
cell.update({
    'cell_id': cell_path.stem, 'title': 'Actual original-experiment truncated matrix means and two mean sums',
    'source_anchor': 'arXiv2610.20492v1 C.2 p12 actual Yi first moments and Ex110 two mean sums, using original p1 experiment and Fact C5; standing integer query range',
    'target_statement': seal['producer']['signature'] + '\nPrivate actual consumer\n' + seal['actual_private_consumer']['signature'],
    'status': 'claimed', 'owner_id': owner, 'advance_id': advance_id,
    'reservation_only': 'Exact-type reservation, normal ledger intake has not occurred.',
    'parents': [], 'consumers': [seal['actual_private_consumer']['name']],
    'shared_floor_audit': {'searched': searches, 'classification': 'adapt', 'decision': 'new_route_local',
                           'canonical_declaration': seal['producer']['name'], 'canonical_shared_cell': ''},
    'reuse_plan': {'searched_existing': searches, 'reused_declarations': [],
                  'planned_existing_parents': seal['shared_floor_audit']['known_canonical_nodes'],
                  'new_shared_declarations': [], 'known_consumers': [],
                  'planned_consumers': [seal['actual_private_consumer']['name']],
                  'no_duplicate_wrapper': True,
                  'decision_reason': 'Use the same canonical row law and truncated radial moment to derive actual Yi integrability and means under the original product law; consume these exact means with the existing cosine frame in both actual finite-sum integrals. No duplicated public radial/marginal theorem or supplied mean certificate.'},
    'source_detail_audit': {
        'primary_edition': 'arXiv2610.20492v1 raw SHA ' + seal['source']['raw_sha256'],
        'primary_anchor': 'C.2 p1,p10,p12 Ex107/108/110 and exact Fact C5 feature sums',
        'detail_status': 'omitted',
        'gap': 'Source suppresses actual row-law applicability, Bochner integrability/transport, tensor/scalar image commutation, finite integral exchange and exact cosine-frame assembly. All remain internal proof obligations, not theorem binders.',
        'consulted': [{'source': 'Pinned original source and literal canonical definitions',
                       'anchor': 'C.2 actual matrix means/two expectation sums and literal Bochner/indicator/Kronecker/operator-norm meanings',
                       'hypothesis_adapter': 'All actual Yi use one product experiment and source closed cutoff. Derive their integrability/means and finite-sum exchange internally, q=0 retained; no row-law/moment/integrability/Gram/mean/tau/kappa certificate input. Joint independence is separate existing credit and unnecessary for means.'}],
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
cell['reader_contract']['status'] = 'Sealed exact actual Yi means and both actual sum integrals; formula proof and exact adjacent folded Lean await real proof.'
cell['graph_contribution']['focus_targets'] = [seal['producer']['name']]
cell['graph_contribution']['visual_review'] = 'Independent raw reading and newly sealed exact types only; formal source graph/type/topology admission pending. Actual compiled mean/consumer edges require real new proofs.'

cell['title'] = 'Actual Gaussian matrix squared moments and centered variance operator bounds'
cell['source_anchor'] = 'arXiv2610.20492v1 C.2 p13 Z definition; p14 Ex113/114 and centered/cosine-weighted variance comparisons; original p1/p10/Ex107 experiment and exact Fact C5 features. Bernstein p15 excluded.'
cell['reuse_plan']['decision_reason'] = 'Use existing canonical row-law, radial-fourth and weighted-frame results to obtain actual uncentered squared moments; consume them in actual centered and cosine-weighted centered integrability and operator-norm bounds. Any missing multi-route generic lemma must receive one shared canonical cell before its proof; never add a variance/PSD/norm certificate as a binder.'
cell['source_detail_audit'].update({
    'primary_anchor': 'C.2 p1,p10,Ex107,p13,p14,Ex113/114 and Fact C5; all p15 excluded',
    'gap': 'Actual-law transport, squared integrability, Hermitian/PSD facts, centered Bochner variance identity, weighted comparison and PSD domination to actual L2 operator norm all require internal proofs. A source omission is not an extra theorem hypothesis.',
    'consulted': [{'source': 'Pinned original source and literal canonical definitions', 'anchor': 'Actual closed-cutoff Yi, actual mean/Z and p14 centered/cos² comparisons', 'hypothesis_adapter': 'Same original independent-column product experiment and exact midpoint features; sole range2q+1<d including q0. Every integrability, positivity, moment/Gram/norm estimate is derived internally.'}],
})
cell['reader_contract']['status'] = 'Exact uncentered PSD and two genuine centered operator-norm targets sealed; readable formula proof and adjacent initially folded exact Lean await real proof.'
cell['graph_contribution']['visual_review'] = 'Own raw source freezes and exact sealed types; independent type/graph/topology admission pending. No compiled variance edge or runtime reader evidence yet.'

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
