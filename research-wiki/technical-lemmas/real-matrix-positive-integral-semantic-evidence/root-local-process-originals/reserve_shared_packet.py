"""Name the single shared cell before recording the route-local dependency decision."""
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
cell_path = Path('research-wiki/frontier-cells/ASTIS-SHARED-REAL-MATRIX-POSITIVE-INTEGRAL.json')
route_path = Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-matrix-variance.json')
seal_path = Path('research-wiki/technical-lemmas/real-matrix-positive-integral-statement-seal.json')
evidence = Path('research-wiki/technical-lemmas/real-matrix-positive-integral-semantic-evidence')
ledger = Path('runs/substantive_advances.jsonl')
target = 'ASTIS-SA-20261112-RealMatrixPositiveIntegral'
owner = 'huanjian_20261112_real_matrix_positive_integral'
sha = lambda raw: hashlib.sha256(raw).hexdigest()
dump = lambda value: (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode()
git = lambda *args: subprocess.check_output(['git', *args])

def create(path, raw):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as out:
        out.write(raw)

head = git('rev-parse', 'HEAD').decode().strip()
assert head == '441d54ee96a6182374d2df3bf4d2fb096d5b7e14'
assert not git('diff', '--cached', '--name-only')
assert git('diff', 'HEAD', '--name-only').decode().splitlines() == [str(ledger)]
seal_raw = seal_path.read_bytes()
assert sha(seal_raw) == 'a5179ed392ef8e55ab470a3a98ebd542e35301f51472e9cdd7bc168a88bafa26'
seal = json.loads(seal_raw)
route_before = route_path.read_bytes()
route = json.loads(route_before)
assert route['advance_id'] == 'ASTIS-SA-20261112-GaussianComplexitySourceMatrixVariance'
assert route['shared_floor_audit']['decision'] == 'new_route_local'
ledger_raw = ledger.read_bytes()
states = advance._replay_advances([json.loads(x) for x in ledger_raw.splitlines()])
assert len(states) == 309 and target not in states
assert states[route['advance_id']]['state'] == 'EXPLORING'
assert not cell_path.exists() and not Path(seal['producer']['planned_file']).exists()
cell = json.loads(route_before)
cell.update({
    'cell_id': cell_path.stem, 'route': 'shared', 'mode': 'faithfulPaper',
    'title': 'Shared Bochner expectation positivity for finite real matrices',
    'source_anchor': 'ASTIS-authored general background for arXiv2610.20492v1 C.2 p14 Ex115/118/120 PSD integration; pinned Mathlib Convex.integral_mem and full finite Matrix.PosSemidef definitions. Not a printed general paper theorem.',
    'target_statement': seal['producer']['signature'] + '\nUnchanged actual source consumer\n' + seal['actual_consumer']['signature'],
    'status': 'claimed', 'owner_id': owner, 'advance_id': target,
    'reservation_only': 'Exact shared-type reservation; normal ledger intake pending independent authored-background type/topology acceptance.',
    'parents': [], 'consumers': seal['shared_floor_audit']['actual_consumers'],
    'shared_floor_audit': {'searched': seal['shared_floor_audit']['searched'], 'classification': 'adapt', 'decision': 'new_canonical_shared', 'canonical_declaration': seal['producer']['name'], 'canonical_shared_cell': cell_path.stem},
    'reuse_plan': {'searched_existing': seal['shared_floor_audit']['searched'], 'reused_declarations': [], 'new_shared_declarations': [seal['producer']['name']], 'known_consumers': [], 'planned_consumers': seal['shared_floor_audit']['actual_consumers'], 'no_duplicate_wrapper': True, 'decision_reason': seal['shared_floor_audit']['decision_reason']},
    'source_detail_audit': {'primary_edition': 'Pinned arXiv2610.20492v1 and Mathlibdb584cd6d46c92f209a44c0f1c829460d327499d', 'primary_anchor': 'p14 omitted PSD expectation applications; Mathlib Analysis/Convex/Integral.lean', 'detail_status': 'omitted', 'gap': 'The paper does not state the arbitrary-function background theorem. This explicit authored expansion proves closed/convex full PSD cone applicability internally; the source consumer must establish integrability and AE positivity internally.', 'consulted': [{'source': 'ASTIS-authored reusable expansion with pinned source application and canonical Mathlib integral provider', 'anchor': 'Ex115/118/120 PSD expectations', 'hypothesis_adapter': 'Arbitrary-f probability/integrability/AE-PSD are genuine generic background conditions. No such condition is added to the original literal Gaussian source statement.'}], 'fidelity_boundary': seal['scope_boundary']},
    'statement_seal': {'status': seal['state'], 'file': str(seal_path), 'sha256': sha(seal_raw), 'signature_sha256': seal['producer']['signature_sha256'], 'actual_consumer_signature_sha256': seal['actual_consumer']['signature_sha256']},
    'evidence': {'actual_literal_formation': seal['actual_statement_formation'], 'actual_generic_instances_in_formation': seal['actual_statement_formation'], 'new_shared_target_proof_attempts': 0, 'formalizer_API_pristine': False},
    'owned_files': [seal['producer']['planned_file'], 'Tests/RealMatrixPositiveIntegral.lean', str(cell_path), str(seal_path), str(evidence) + '/', 'website/content/declaration_lessons/huanjian-real-matrix-positive-integral.json', 'website/content/publications/huanjian-real-matrix-positive-integral.json', 'research-wiki/semantic-roundtrip/audits/huanjian-real-matrix-positive-integral.json'],
    'truth_boundary': seal['scope_boundary'], 'conceptual_mirror_audit': {'status': 'pending'},
})
cell['reader_contract']['status'] = 'Sealed explicitly authored background statement and unchanged literal Gaussian consumer; proof and exact folded Lean pending.'
cell['graph_contribution']['focus_targets'] = [seal['producer']['name']]
cell['graph_contribution']['visual_review'] = 'One new shared candidate node; no compiled call or source theorem credit before actual proof. Exact known consumers planned, independent type/topology pending.'
# The shared cell must exist before changing the route-local decision.
create(cell_path, dump(cell))
create(Path('.astis/huanjian-gc-source-matrix-variance-20261112/cell-before-shared-canonical-dependency.original.json'), route_before)
route['shared_floor_audit']['decision'] = 'new_canonical_shared'
route['shared_floor_audit']['canonical_shared_cell'] = cell_path.stem
route['reuse_plan']['planned_shared_cell'] = cell_path.stem
route['reuse_plan']['new_shared_declarations'] = [seal['producer']['name']]
route['reuse_plan']['decision_reason'] += ' Actual floor search found a reusable positivity-integral applicability bridge with uncentered and centered consumers; one shared cell is named before its proof. Generic integrability/AE-PSD contracts never enter this source theorem.'
route['evidence']['shared_background_dependency_pending'] = {'cell': cell_path.stem, 'seal': str(seal_path), 'seal_sha256': sha(seal_raw), 'new_compiled_parent_claimed': False}
route_path.write_bytes(dump(route))
assert not frontiers.validate_cells(frontiers.load_cells())
assert ledger.read_bytes() == ledger_raw
older = {str(p): sha(p.read_bytes()) for p in cell_path.parent.rglob('*') if p.is_file() and not p.is_symlink() and p != cell_path}
assert len(older) == 469
create(workspace / 'preproof-baseline.private.json', dump({'head': head, 'ledger_bytes': len(ledger_raw), 'ledger_sha256': sha(ledger_raw), 'all_foreign_states': states, 'all_existing_frontier_hashes': older, 'tracked_git_index': git('ls-files', '--stage').decode(), 'preexisting_tracked_diff_names': [str(ledger)], 'preexisting_R9_intake_prefix_is_authorized_and_not_replayed': True, 'scope': 'Private complete preservation guard only; no full foreign/control snapshot export.'}))
discovery_raw = Path('runs/substantive_discoveries.jsonl').read_bytes()
discoveries = advance._replay_discoveries([json.loads(x) for x in discovery_raw.splitlines()])
assert len(discoveries) == 43
create(workspace / 'preproof-discoveries.private.json', dump({'ledger_sha256': sha(discovery_raw), 'ledger_bytes': len(discovery_raw), 'full_states': discoveries, 'scope': 'Private complete preservation guard only.'}))
record = {'shared_cell': str(cell_path), 'shared_cell_sha256': sha(cell_path.read_bytes()), 'shared_seal_sha256': sha(seal_raw), 'source_consumer_cell': str(route_path), 'source_consumer_cell_before_sha256': sha(route_before), 'source_consumer_cell_after_sha256': sha(route_path.read_bytes()), 'source_seal_unchanged': route['statement_seal']['sha256'], 'source_statement_unchanged': True, 'only_planned_dependency_no_compiled_edge': True, 'normal_shared_API_calls': 0, 'foreign_full_states_guarded': len(states), 'older_regular_frontier_guarded': len(older), 'discovery_full_states_and_bytes_guarded': len(discoveries), 'preexisting_R9_EXPLORING_prefix_sha256': sha(ledger_raw)}
create(workspace / 'actual-seal-and-reservation-summary.json', dump(record))
print(json.dumps(record))
