from pathlib import Path
import json
r=Path(__file__).parent
assert json.loads((r/'root.statement-seal84.json').read_bytes())['proof_BODY_created'] is False
h=(r/'header84.reviewed.lean').read_text(encoding='utf8')
h=h[:h.index('\nend\n')]
h=h.replace('Prospective exact statement84 only; no theorem proof or admission.','Actual PBPS bounded-test outer square-integral continuity.')
p=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualOuterBoundedL2Continuity.lean');assert not p.exists()
p.write_text(h+'\n\n'+(r/'body84.lean.txt').read_text(encoding='utf8')+'\nend\nend AutoSamplingTheory.ExampleCases.ProximalBPS.ActualOuterBoundedL2Continuity\n',encoding='utf8',newline='\n')
