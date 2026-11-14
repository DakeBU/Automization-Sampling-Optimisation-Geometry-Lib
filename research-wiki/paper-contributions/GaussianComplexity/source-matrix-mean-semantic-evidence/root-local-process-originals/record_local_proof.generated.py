"""Append one normal local proof transition, retaining its full exact payload."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, 'tools')
import astis_advance as advance
import astis_frontier_cells as frontier
import astis_publication as publication

workspace = Path(__file__).resolve().parent.relative_to(Path.cwd())
evidence = Path('research-wiki/paper-contributions/GaussianComplexity/source-matrix-mean-semantic-evidence')
cell_path = Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-matrix-mean.json')
ledger = Path('runs/substantive_advances.jsonl')
target = 'ASTIS-SA-20261112-GaussianComplexitySourceMatrixMean'
owner = 'huanjian_gc_20261112_source_matrix_mean'
sha = lambda raw: hashlib.sha256(raw).hexdigest()
dump = lambda value: (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode()
git = lambda *args: subprocess.check_output(['git', *args])


def create(path, raw):
    with path.open('xb') as out:
        out.write(raw)


head = git('rev-parse', 'HEAD').decode().strip()
source_commit = json.loads((workspace / 'actual-independent-source-review-commit.json').read_bytes())
assert head == source_commit['source_review_metadata_commit']
assert not git('diff', 'HEAD', '--name-only') and not git('diff', '--cached', '--name-only')
candidate = json.loads((workspace / 'actual-immutable-math-candidate.json').read_bytes())
math_commit = candidate['mathematical_candidate']
assert math_commit == '5fb1440f771bdae77ad31f27b2275447fe3e89e5'
seal = json.loads((workspace / 'statement-seal-v1.json').read_bytes())
draft = json.loads((evidence / 'publication-draft-record.json').read_bytes())
P, T = [Path(seal[key]['planned_file']) for key in ('producer', 'actual_private_consumer')]
assert sha(P.read_bytes()) == draft['producer_sha256']
assert sha(T.read_bytes()) == draft['private_consumer_sha256']
for path in (P, T):
    assert git('show', f'{math_commit}:{path}') == path.read_bytes()
before = ledger.read_bytes()
states = advance._replay_advances([json.loads(line) for line in before.splitlines()])
assert states[target]['state'] == 'EXPLORING' and states[target]['owner_id'] == owner
baseline = json.loads((workspace / 'preproof-baseline.private.json').read_bytes())
assert {key:value for key,value in states.items() if key != target} == baseline['all_foreign_states']
for path, digest in baseline['all_existing_frontier_hashes'].items():
    assert sha(Path(path).read_bytes()) == digest
discovery_bytes = Path('runs/substantive_discoveries.jsonl').read_bytes()
discovery_guard = json.loads((workspace / 'preproof-discoveries.private.json').read_bytes())
assert sha(discovery_bytes) == discovery_guard['ledger_sha256']
assert advance._replay_discoveries([json.loads(x) for x in discovery_bytes.splitlines()]) == discovery_guard['full_states']
cell = json.loads(cell_path.read_bytes())
assert cell['status'] == 'claimed' and cell['evidence']['independent_verification'] == ''
assert cell['conceptual_mirror_audit']['status'] == 'none-found'
assert all(item['identity_and_status_preserved'] for item in cell['conceptual_mirror_audit']['existing_validated_mirrors'])
checks = [draft['build'], draft['kernel']]
for item in checks:
    path = Path(item['path'])
    receipt = json.loads(path.read_bytes())
    assert sha(path.read_bytes()) == item['sha256'] and receipt['exit_code'] == 0
    assert sha(Path(receipt['log']).read_bytes()) == item['log_sha256'] == receipt['log_sha256']
name = seal['producer']['name']
publication.check_advance([name], reviewed=True)
assert not frontier.validate_cells(frontier.load_cells())
boundary = seal['scope_boundary']
result = {
    'result_kind': 'theorem-edge', 'theorem_delta': seal['producer']['signature'],
    'lean_files': [str(P), str(T)], 'lean_declarations': [name], 'publication_declarations': [name],
    'focused_checks': checks, 'truth_boundary': boundary,
    'mathematical_candidate': math_commit, 'source_review_metadata_commit': head,
    'actual_compiled_parent_edges': draft['actual_public_ASTIS_parents'],
    'actual_private_consumer': seal['actual_private_consumer']['signature'],
    'publication_binding_sha256': draft['publication_binding_sha256'],
    'independent_source_review': cell['evidence']['independent_source_review'],
    'conceptual_mirror_audit': cell['conceptual_mirror_audit'],
    'owned_theorems': {'handwritten': 2, 'generated_reachable_internal': 1},
    'kernel_type_check': 'Both exact literal Props accepted by actual kernel applications, monomorphic; raw Expr equality false. Two handwritten roots and one emitted internal helper are all closed and reachable with standard axioms only.',
    'formalizer_preseal_API_pristine': False, 'preseal_exposure': seal['preseal_exposure'],
    'proof_iteration': {
        'diagnoses': str(evidence / 'local-attempt-diagnoses.json'),
        'producer_initial_failures': 0, 'consumer_initial_build_failures': 2,
        'initial_strict_kernel_failure': None,
        'recovery': 'Actual consumer proof-local Matrix annotation and implicit Finset.smul_sum argument failures diagnosed; final v3 and the unchanged strict probe passed. Producer passed first attempt; exact sealed types unchanged.',
        'final_build': draft['build'], 'final_kernel': draft['kernel'], 'source_types_changed': False,
    },
    'reader_boundary': cell['reader_contract']['status'],
}
create(workspace / 'local-proof-transition-attempted.once.json', dump({
    'advance_id': target, 'before_ledger_sha256': sha(before), 'math_candidate': math_commit,
    'metadata_commit': head, 'from_state': 'EXPLORING', 'to_state': 'PROVED_LOCAL',
}))
advance.transition_advance(target, 'PROVED_LOCAL', worker_id=owner, evidence=result)
after = ledger.read_bytes()
assert after.startswith(before)
append = after[len(before):]
assert len(append.splitlines()) == 1
event = json.loads(append)
assert event['advance_id'] == target and event['worker_id'] == owner
assert event['to_state'] == 'PROVED_LOCAL' and event['evidence'] == result
now = advance._replay_advances([json.loads(line) for line in after.splitlines()])
assert now[target]['state'] == 'PROVED_LOCAL'
assert {key:value for key,value in states.items() if key != target} == {key:value for key,value in now.items() if key != target}
cell['status'] = 'proved_locally'
cell['truth_boundary'] = boundary
cell.pop('reservation_only', None)
cell['statement_seal']['status'] = 'EXACT_UNCHANGED_TYPES_COMPILED;INDEPENDENT_SOURCE_ACCEPTED;FINAL_NATIVE_VERIFICATION_PENDING'
cell['evidence']['focused_checks'] = checks
cell['evidence']['actual_PROVED_LOCAL_append_sha256'] = sha(append)
cell['learning_contract']['failure_class'] = 'IMPLEMENTATION_FAILED'
cell['learning_contract']['salvage'] = {
    'required': True, 'status': 'completed',
    'reason': 'Control-plane reservation label and exploratory API lookup failures retained. Producer compiled first attempt; two consumer elaboration/API errors fixed without changing the exact statement or mathematical route. Final v3 and original strict kernel probe passed. All failed source versions/streams retained; no discarded mathematical fragment.',
    'promoted_fragments': [name], 'discarded_fragments': [],
}
cell_path.write_bytes(dump(cell))
assert not frontier.validate_cells(frontier.load_cells())
create(evidence / 'actual-PROVED_LOCAL-append.exact.jsonl', append)
create(evidence / 'actual-PROVED_LOCAL-evidence.full.json', dump(result))
for path, digest in baseline['all_existing_frontier_hashes'].items():
    assert sha(Path(path).read_bytes()) == digest
assert Path('runs/substantive_discoveries.jsonl').read_bytes() == discovery_bytes
assert set(git('diff', 'HEAD', '--name-only').decode().splitlines()) == {str(cell_path), str(ledger)}
print(json.dumps({
    'state': 'PROVED_LOCAL', 'math_candidate': math_commit, 'source_metadata_commit': head,
    'append_sha256': sha(append), 'full_original_payload_sha256': sha(dump(result)),
    'foreign_full_states_preserved': len(states) - 1,
    'older_frontier_regular_files_preserved': len(baseline['all_existing_frontier_hashes']),
    'root_VERIFIED_calls': 0, 'formalizer_API_pristine': False,
}))
