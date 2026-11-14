"""Repair only a metadata envelope; preserve the actual PL evidence unchanged."""
from pathlib import Path
import json
import hashlib
import copy

R = Path('/Users/zhouhuanjian/ASTIS-GC')
E = R / 'research-wiki/technical-lemmas/matrix-bernstein-mgf-semantic-evidence'
C = R / 'research-wiki/frontier-cells/ASTIS-SHARED-MATRIX-BERNSTEIN-MGF.json'
pl_path = E / 'PROVED_LOCAL-evidence.full.json'
pl_bytes = pl_path.read_bytes()
pl = json.loads(pl_bytes)
cell = json.loads(C.read_text())
assert cell['status'] == 'proved_locally'
assert cell['evidence']['focused_checks'] == pl['focused_checks']
cell['evidence']['focused_checks_bundle'] = copy.deepcopy(pl['focused_checks'])
checks = []
for row in pl['focused_checks']['ROOT_actual']:
    p = R / row['file']
    raw = p.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == row['sha256']
    receipt = json.loads(raw)
    assert receipt['exit_code'] == 0
    checks.append({**row, 'command': receipt['command']})
assert len(checks) == 2
cell['evidence']['focused_checks'] = checks
cell['evidence']['metadata_envelope_repair'] = 'Initial pre-V frontier check correctly rejected a dictionary copied from the richer PL focused_checks bundle where the frontier schema requires a list. Actual ROOT receipt records are now the list; the complete bundle and original PL bytes remain unchanged. No check or proof was rerun or fabricated by this envelope repair.'
C.write_text(json.dumps(cell, ensure_ascii=False, indent=2) + '\n')
assert pl_path.read_bytes() == pl_bytes
print(json.dumps({'repair': 'frontier focused_checks dict-to-actual-receipt-list only', 'actual_receipts': len(checks), 'PL_24field_original_unchanged': True, 'Lean_or_API_calls': 0}))
