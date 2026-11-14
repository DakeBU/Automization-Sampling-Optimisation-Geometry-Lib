"""One normal shared-interface local-proof transition; no root VERIFIED."""
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

W = Path(__file__).resolve().parent.relative_to(Path.cwd())
E = Path('research-wiki/technical-lemmas/real-matrix-positive-integral-semantic-evidence')
C = Path('research-wiki/frontier-cells/ASTIS-SHARED-REAL-MATRIX-POSITIVE-INTEGRAL.json')
ledger = Path('runs/substantive_advances.jsonl')
target = 'ASTIS-SA-20261112-RealMatrixPositiveIntegral'
owner = 'huanjian_20261112_real_matrix_positive_integral'
sha = lambda raw: hashlib.sha256(raw).hexdigest()
dump = lambda obj: (json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode()
git = lambda *args: subprocess.check_output(['git', *args])
def create(path, raw):
    with path.open('xb') as out:
        out.write(raw)

head = git('rev-parse', 'HEAD').decode().strip()
source = json.loads((W/'actual-independent-source-review-commit.json').read_bytes())
assert head == source['source_review_metadata_commit']
assert not git('diff', 'HEAD', '--name-only') and not git('diff', '--cached', '--name-only')
candidate = json.loads((W/'actual-immutable-math-candidate.json').read_bytes())
math_commit = candidate['mathematical_candidate']
assert math_commit == '9964c33c4599f85d27dc8687e8bd6fdb5c44ff49'
seal = json.loads((W/'statement-seal-v1.json').read_bytes())
draft = json.loads((E/'coupled-publication-draft-record.json').read_bytes())
for key in ('producer', 'actual_consumer'):
    item = draft[key]
    p = Path(item['file'])
    assert sha(p.read_bytes()) == item['file_sha256']
    assert git('show', f'{math_commit}:{p}') == p.read_bytes()
before = ledger.read_bytes()
states = advance._replay_advances([json.loads(x) for x in before.splitlines()])
assert states[target]['state'] == 'EXPLORING' and states[target]['owner_id'] == owner
b = json.loads((W/'candidate-boundary-v3.private.json').read_bytes())
assert {k:v for k,v in states.items() if k != target} == b['all_foreign_states']
for p, digest in b['all_existing_frontier_hashes'].items():
    assert sha(Path(p).read_bytes()) == digest, p
discovery_raw = Path('runs/substantive_discoveries.jsonl').read_bytes()
dg = json.loads((W/'preproof-discoveries.private.json').read_bytes())
assert sha(discovery_raw) == dg['ledger_sha256']
assert advance._replay_discoveries([json.loads(x) for x in discovery_raw.splitlines()]) == dg['full_states']
cell = json.loads(C.read_bytes())
assert cell['status'] == 'claimed' and cell['evidence']['independent_verification'] == ''
assert cell['conceptual_mirror_audit']['status'] == 'none-found'
checks = [draft['producer_build'], draft['consumer_first_build'], draft['build'], draft['kernel']]
for item in checks:
    p = Path(item['path'])
    r = json.loads(p.read_bytes())
    assert sha(p.read_bytes()) == item['sha256'] and r['exit_code'] == 0
    assert sha(Path(r['log']).read_bytes()) == item['log_sha256'] == r['log_sha256']
names = [draft[k]['declaration'] for k in ('producer', 'actual_consumer')]
publication.check_advance(names, reviewed=True)
assert not frontier.validate_cells(frontier.load_cells())
boundary = 'One generic real-matrix probability expectation positivity interface, materially consumed by the actual uncentered source moment bound. No centered/weighted proof credit in this immutable packet; subsequent R9 draft is outside this SAU. Independent native verification, original-owner serialized integration, root/site/graph/reader publication and purification remain separate.'
result = {
    'result_kind': 'reusable-interface', 'theorem_delta': seal['producer']['signature'],
    'lean_files': [draft['producer']['file'], draft['actual_consumer']['file'], 'Tests/RealMatrixPositiveIntegral.lean'],
    'lean_declarations': [names[0]], 'publication_declarations': [names[0]],
    'focused_checks': checks, 'truth_boundary': boundary,
    'mathematical_candidate': math_commit, 'source_review_metadata_commit': head,
    'actual_compiled_parent_edges': draft['actual_public_ASTIS_parents'],
    'actual_material_consumer': {k:draft['actual_consumer'][k] for k in ('declaration', 'file', 'file_sha256', 'publication_binding_sha256')},
    'publication_binding_sha256': draft['producer']['publication_binding_sha256'],
    'independent_source_review': cell['evidence']['independent_source_review'],
    'conceptual_mirror_audit': cell['conceptual_mirror_audit'],
    'owned_theorems': draft['owned_mathematics'],
    'kernel_type_check': 'Both literal complete Props accepted by actual kernel proof-value applications. S has generic universes and raw Expr equality true; P monomorphic raw Expr equality false. All4 new declarations closed/reachable, standard axioms only. Actual empty matrix index and q0 checks compiled.',
    'formalizer_preseal_API_pristine': False, 'preseal_exposure': seal.get('preseal_exposure', {}),
    'proof_iteration': {
        'producer_initial_build_failures': 1, 'consumer_initial_build_failures': 0,
        'strict_kernel_probe_failures': 0,
        'diagnosis': 'Missing existing Mathlib Real StarOrderedRing instance import on first S attempt; exact prior source and receipt retained. Added only the provider import, unchanged target/route. Actual P compiled first attempt.',
        'independent_reader_correction': 'P unqualified variance wording corrected to its exact uncentered squared-moment PSD scope. Both source review inputs and all old prose/audit/anti packets retained.',
        'source_types_changed': False,
    },
    'reader_boundary': cell['reader_contract']['status'],
}
create(W/'local-proof-transition-attempted.once.json', dump({
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
now = advance._replay_advances([json.loads(x) for x in after.splitlines()])
assert now[target]['state'] == 'PROVED_LOCAL'
assert {k:v for k,v in now.items() if k != target} == b['all_foreign_states']
cell['status'] = 'proved_locally'
cell['truth_boundary'] = boundary
cell.pop('reservation_only', None)
cell['statement_seal']['status'] = 'EXACT_UNCHANGED_TYPES_COMPILED;INDEPENDENT_SOURCE_ACCEPTED;FINAL_NATIVE_VERIFICATION_PENDING'
cell['evidence']['focused_checks'] = checks
cell['evidence']['actual_PROVED_LOCAL_append_sha256'] = sha(append)
cell['learning_contract']['failure_class'] = 'IMPLEMENTATION_FAILED'
C.write_bytes(dump(cell))
assert not frontier.validate_cells(frontier.load_cells())
create(E/'actual-PROVED_LOCAL-append.exact.jsonl', append)
create(E/'actual-PROVED_LOCAL-evidence.full.json', dump(result))
for p, digest in b['all_existing_frontier_hashes'].items():
    assert sha(Path(p).read_bytes()) == digest, p
assert Path('runs/substantive_discoveries.jsonl').read_bytes() == discovery_raw
assert set(git('diff', 'HEAD', '--name-only').decode().splitlines()) == {str(C), str(ledger)}
print(json.dumps({'state': 'PROVED_LOCAL', 'math_candidate': math_commit,
    'source_metadata_commit': head, 'append_sha256': sha(append),
    'full_original_payload_sha256': sha(dump(result)), 'foreign_full_states_preserved': len(states)-1,
    'older_frontiers_preserved_since_qualified_boundary': len(b['all_existing_frontier_hashes']),
    'root_VERIFIED_calls': 0}))
