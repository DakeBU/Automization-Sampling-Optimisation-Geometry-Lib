"""Finish prepared integration under the existing sole four-paper lane."""
from pathlib import Path
import json
import sys
sys.path.insert(0, str(Path.cwd() / 'tools'))
import astis_advance as advance
run = Path('runs/20261007-companion-priority/pbps-unit-exponential-product77')
out = run / 'integration77'
lanes = [s for s in advance.current_advances().values() if s['state'] == 'STABILIZING']
assert len(lanes) == 1
lane = lanes[0]
assert lane['advance_id'] == 'ASTIS-SA-20261005-SPHMCImplementedPhaseKernel'
assert lane['latest_evidence']['integration_owner'] == 'companion_root_20261005'
assert advance.current_advances()['ASTIS-SA-20261010-UnitExponentialProduct']['state'] == 'VERIFIED'
scope = {
    'owned': [x['path'] for x in json.loads((out / 'owned-before.json').read_bytes())],
    'science_commit': '4f88383540a865aea304c63c40de5a699ea61611',
    'sole_stabilization_owner': lane['advance_id'],
    'integration_actor': lane['latest_evidence']['integration_owner'],
    'mathematical_state': 'VERIFIED', 'aggregate': 'pending', 'visual': 'pending',
    'lane_diagnosis': 'Initial attempt to open a second lane rejected before any ledger transition. Prepared import/Registry/Tests/docs changes are adopted into the existing branch lane; no old state reset and no second stabilization owner.',
    'Goal_complete': False,
}
assert not (out / 'integration-scope.json').exists()
(out / 'integration-scope.json').write_text(json.dumps(scope, indent=2) + '\n', encoding='utf8')
print('Preserved existing sole stabilization lane; SAU77 remains VERIFIED pending shared integration acceptance.')
