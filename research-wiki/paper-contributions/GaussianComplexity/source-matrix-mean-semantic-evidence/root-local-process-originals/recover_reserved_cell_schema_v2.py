"""Repair only library-search provenance labels on the new, unadmitted cell."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, 'tools')
import astis_frontier_cells as frontier
import astis_advance as advance

workspace = Path(__file__).resolve().parent.relative_to(Path.cwd())
cell_path = Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-matrix-mean.json')
sha = lambda b: hashlib.sha256(b).hexdigest()
dump = lambda x: (json.dumps(x, ensure_ascii=False, indent=2) + '\n').encode()
raw = cell_path.read_bytes()
cell = json.loads(raw)
baseline = json.loads((workspace / 'preproof-baseline.private.json').read_bytes())
ledger = Path('runs/substantive_advances.jsonl')
assert sha(ledger.read_bytes()) == baseline['ledger_sha256']
assert advance.current_advances() == baseline['all_foreign_states']
assert not subprocess.check_output(['git', 'diff', 'HEAD', '--name-only'])
assert cell['reservation_only'] and cell['status'] == 'claimed'
assert cell['advance_id'] not in advance.current_advances()
with (workspace / 'reserved-cell.description-attempt1.original.json').open('xb') as out:
    out.write(raw)
searches = list(cell['shared_floor_audit']['searched'])
searches[0] = 'Samplinglib: ' + searches[0]
searches[2] = 'Mathlib: ' + searches[2]
cell['shared_floor_audit']['searched'] = searches
cell['reuse_plan']['searched_existing'] = searches
cell['evidence']['reservation_schema_diagnosis'] = {
    'class': 'IMPLEMENTATION_FAILED', 'scope': 'New unadmitted control-plane description only',
    'reason': 'Schema requires explicit Samplinglib and Mathlib search provenance labels. Actual known canonical-source inspection and standard-definition lookups were already recorded; only those literal library names were omitted.',
    'original_cell': str(workspace / 'reserved-cell.description-attempt1.original.json'),
    'original_sha256': sha(raw), 'new_target_proof_attempts': 0, 'normal_API_calls': 0,
    'mathematical_signature_or_source_change': False,
}
cell_path.write_bytes(dump(cell))
assert not frontier.validate_cells(frontier.load_cells())
for name, digest in baseline['all_existing_frontier_hashes'].items():
    assert sha(Path(name).read_bytes()) == digest
summary = {
    'baseline_commit': baseline['head'], 'exact_seal_sha256': cell['statement_seal']['sha256'],
    'cell': str(cell_path), 'cell_sha256': sha(cell_path.read_bytes()),
    'foreign_full_states_guarded': len(baseline['all_foreign_states']),
    'older_frontier_files_guarded': len(baseline['all_existing_frontier_hashes']),
    'discovery_states_guarded': 43, 'normal_API_and_proof_calls': 0,
    'independent_topology_acceptance': 'pending',
    'recovery': 'Only explicit library provenance labels added; original unadmitted cell/failed receipt retained.',
}
with (workspace / 'actual-seal-and-reservation-summary.json').open('xb') as out:
    out.write(dump(summary))
print(json.dumps(summary))
