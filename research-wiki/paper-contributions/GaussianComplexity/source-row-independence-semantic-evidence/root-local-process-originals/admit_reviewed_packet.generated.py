"""Perform one normal intake after exact independent source/type/topology review."""
from pathlib import Path
import hashlib
import json
import stat
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
sha = lambda raw: hashlib.sha256(raw).hexdigest()
dump = lambda value: (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode()


def create(path, raw):
    with path.open('xb') as out:
        out.write(raw)


def git(*args):
    return subprocess.check_output(['git', *args])


def replay(raw):
    return advance._replay_advances([json.loads(line) for line in raw.splitlines()])


review_path = workspace / 'reviewed-preproof-inputs.json'
review = json.loads(review_path.read_bytes())
assert review['source_type_verdict'] == 'accepted'
assert review['independent_topology_verdict'] == 'accepted'
assert review['remaining_statement_or_source_topology_blockers'] == []
assert review['formalizer_API_pristine'] is False
for item in review['independent_originals']:
    raw = Path(item['path']).read_bytes()
    assert sha(raw) == item['sha256'] and len(raw) == item['bytes'], item['path']
seal_raw = seal_path.read_bytes()
assert sha(seal_raw) == '88a55849ce9e13a9a04edff6aac13ce32d4370712b1b7a422fba0d570ff0b25e'
assert review['statement_seal_sha256'] == sha(seal_raw)
seal = json.loads(seal_raw)
baseline = json.loads((workspace / 'preproof-baseline.private.json').read_bytes())
assert git('rev-parse', 'HEAD').decode().strip() == baseline['head']
assert not git('diff', 'HEAD', '--name-only') and not git('diff', '--cached', '--name-only')
assert git('ls-files', '--stage').decode() == baseline['tracked_git_index']
before = ledger.read_bytes()
assert len(before) == baseline['ledger_bytes'] and sha(before) == baseline['ledger_sha256']
states = replay(before)
assert states == baseline['all_foreign_states'] and advance_id not in states
for name, digest in baseline['all_existing_frontier_hashes'].items():
    assert sha(Path(name).read_bytes()) == digest, name
producer, consumer = [seal[key]['planned_file'] for key in ('producer', 'actual_private_consumer')]
assert not Path(producer).exists() and not Path(consumer).exists()
cell_before = cell_path.read_bytes()
assert sha(cell_before) == 'be03871e5c86378721ab9bde584ff06cb5ee3ed43310f70d921a98646d05441e'
cell = json.loads(cell_before)
assert cell['status'] == 'claimed' and cell['owner_id'] == owner
assert not frontiers.validate_cells(frontiers.load_cells())
known = set(json.loads(Path('.astis/huanjian-gc-source-row-law-20261112/intake-controls.private.json').read_bytes()))
known.update(str(path) for path in Path('runs').iterdir())
known.add('website/content/samplewiki_companion_frontiers.json')
for name in ('control', 'queues', 'runtime', 'harness', 'state', 'locks'):
    root = Path('.astis') / name
    if root.is_dir() and not root.is_symlink():
        known.update(str(path) for path in root.rglob('*'))
for path in Path('.astis').iterdir():
    if any(word in path.name.lower() for word in ('queue', 'control', 'goal', 'steer', 'execution')):
        known.add(str(path))
known.update(raw.decode() for raw in git('ls-files', '--others', '--exclude-standard', '-z').split(b'\0') if raw)
controls = {}
for name in sorted(known):
    path = Path(name)
    if path in (ledger, cell_path, seal_path) or path.is_relative_to(evidence) or name.startswith('.atlas-upstream/'):
        continue
    if path.exists():
        info = path.lstat()
        if stat.S_ISREG(info.st_mode) and info.st_size < 100_000_000:
            controls[name] = sha(path.read_bytes())
create(workspace / 'intake-controls.private.json', dump(controls))
record = {
    'kind': 'Prover readback of independent mathematical source/type/topology judgments',
    'statement_seal_sha256': sha(seal_raw), 'reserved_cell_sha256': sha(cell_before),
    'independent_review_readback': review,
    'prover_source_VERIFIED_calls': 0,
    'boundary': 'Independent source/type/topology acceptance only; explicit internal/applicability ports remain unproved. Actual joint-row/Yi independence proof, source verification, integration and publication remain open.',
}
record_path = evidence / 'preproof-source-admission.json'
record_raw = dump(record)
create(record_path, record_raw)
proposal = advance.AdvanceProposal(
    advance_id=advance_id, task_id='ASTIS-SW-GAUSSIAN-COMPLEXITY-2026',
    goal='Prove full joint independence of actual physical Gaussian rows under the literal source column-product experiment and consume it in measurability and independence of the exact Ex107 truncated matrices.',
    source_anchor=cell['source_anchor'], theorem_delta=seal['producer']['signature'],
    truth_boundary=seal['scope_boundary'], created_by=owner,
    dag_inputs=(cell['source_anchor'], 'Literal standard-Gaussian column-product law, actual physical coordinate rows and exact Ex107 Yi. Coordinate-basis/product-law alignment, full joint independence, actual truncated-matrix measurability and independence under the same mu are internal proof obligations. Marginals alone do not supply independence; no law/independence/measurability certificate input.'),
    proposed_files=tuple(path for path in cell['owned_files'] if not path.endswith('/')),
    focused_checks=('lake env lean ' + producer, 'lake build Tests.GaussianComplexityFixedSpectrumSourceRowIndependence'),
    modes=('source-reading', 'proof-design', 'compiler-diagnosis'), priority=50,
    frontier_cell=cell_path.stem, target_declarations=(seal['producer']['name'],),
)
proposal.validate()
create(workspace / 'normal-intake-attempted.once.json', dump({
    'advance_id': advance_id, 'before_ledger_sha256': sha(before),
    'independent_math_review_record_sha256': sha(record_raw), 'no_replay': True,
}))
event_evidence = {
    'independent_topology': {'file': str(record_path), 'sha256': sha(record_raw)},
    'statement_seal_sha256': sha(seal_raw), 'truth_boundary': seal['scope_boundary'],
    'formalizer_API_pristine': False,
}
advance.propose_advance(proposal)
advance.transition_advance(advance_id, 'CLAIMED', worker_id=owner, evidence=event_evidence)
advance.transition_advance(advance_id, 'EXPLORING', worker_id=owner, evidence=event_evidence)
after = ledger.read_bytes()
assert after.startswith(before)
append = after[len(before):]
events = [json.loads(line) for line in append.splitlines()]
assert len(events) == 3 and all(event['advance_id'] == advance_id for event in events)
assert [event.get('state', event.get('to_state')) for event in events] == ['PROPOSED', 'CLAIMED', 'EXPLORING']
now = replay(after)
assert now.pop(advance_id)['state'] == 'EXPLORING' and now == states
assert git('diff', 'HEAD', '--name-only').decode().splitlines() == [str(ledger)]
for name, digest in baseline['all_existing_frontier_hashes'].items():
    assert sha(Path(name).read_bytes()) == digest, name
for name, digest in controls.items():
    assert sha(Path(name).read_bytes()) == digest, name
assert cell_path.read_bytes() == cell_before
cell['evidence']['preproof_source_admission'] = event_evidence['independent_topology']
cell['evidence']['normal_API_calls'] = 3
cell['evidence']['target_proof_calls'] = 0
cell['statement_seal']['status'] = 'EXACT_TYPES_AND_DEFINITIONS;INDEPENDENT_SOURCE_TOPOLOGY_ACCEPTED;UNPROVED'
cell['reservation_only'] = 'Normal ledger records EXPLORING under the named owner.'
cell_path.write_bytes(dump(cell))
create(evidence / 'normal-EXPLORING-append.exact.jsonl', append)
summary = {
    'state': 'EXPLORING', 'append_sha256': sha(append), 'actual_normal_API_calls': 3,
    'foreign_full_states_preserved': len(states),
    'older_frontier_files_preserved': len(baseline['all_existing_frontier_hashes']),
    'foreign_controls_preserved': len(controls), 'target_proof_or_sourceV': False,
    'baseline_commit': baseline['head'],
}
create(evidence / 'normal-intake-preservation.json', dump(summary))
assert not frontiers.validate_cells(frontiers.load_cells())
print(json.dumps(summary))
