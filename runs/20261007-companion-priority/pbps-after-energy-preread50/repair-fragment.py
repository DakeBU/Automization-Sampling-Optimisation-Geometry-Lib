# -*- coding: utf-8 -*-
from pathlib import Path
import json,sys
sys.stdout.reconfigure(encoding='utf-8');O=Path('runs/20261007-companion-priority/pbps-after-energy-preread50');p=O/'selected-api-bindings.json';d=json.loads(p.read_text(encoding='utf-8'));(O/'selected-api-bindings.attempt0.json').write_bytes(p.read_bytes())
for x in d:
 if 'physical_lf_lines1' in x and x['id']!='local-reflected-disintegration':
  for suf in ['raw','lf']:
   q=O/(x['id']+'.'+suf);(O/(x['id']+'.attempt0.'+suf)).write_bytes(q.read_bytes())
s=O/'pin-selected.py';(O/'pin-selected.attempt0.py').write_bytes(s.read_bytes());t=s.read_text(encoding='utf-8');assert "b''.join(b.split(b'\\n')[a-1:z])" in t;t=t.replace("b''.join(b.split(b'\\n')[a-1:z])","b'\\n'.join(b.split(b'\\n')[a-1:z])");s.write_text(t,encoding='utf-8')
(O/'fragment-repair-note.json').write_text(json.dumps(dict(issue='Initial selected-API slicing joined LF-split rows without restoring separators; those attempt0 fragments were not contiguous raw source slices.',repair='Retained attempt0 helper/bindings/fragments unchanged, replaced selected slicing with newline join and regenerated current exact selected physical-LF fragments before any proposal or seal.',mathematical_statement_change=False,compiler_used=False,source_coverage_admission=False),indent=2)+'\n',encoding='utf-8')
