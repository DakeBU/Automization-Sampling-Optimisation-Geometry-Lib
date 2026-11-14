"""Use the frontier schema's string locator; keep full structured V evidence."""
from pathlib import Path
import json

R = Path('/Users/zhouhuanjian/ASTIS-GC')
C = R / 'research-wiki/frontier-cells/ASTIS-SHARED-MATRIX-BERNSTEIN-MGF.json'
cell = json.loads(C.read_text())
e = cell['evidence']
assert cell['status'] == 'independently_verified'
assert e['independent_verification'] == e['actual_normal_VERIFIED']
locator = e['actual_normal_VERIFIED']['payload']['file']
assert (R / locator).is_file()
e['independent_verification'] = locator
e['verification_locator_schema_repair'] = 'The current frontier schema requires a nonempty string locator in independent_verification; the full unchanged structured record remains actual_normal_VERIFIED. The rejected dictionary envelope and actual gate failure are preserved. This changes no independent verdict, API event, theorem, proof or evidence original.'
C.write_text(json.dumps(cell, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'independent_verification_locator': locator, 'full_structured_evidence_preserved': True, 'API_or_proof_calls': 0}))
