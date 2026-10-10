# -*- coding: utf-8 -*-
from pathlib import Path
import json,sys
sys.stdout.reconfigure(encoding='utf-8')
p=Path('runs/20261007-companion-priority/pbps-outer-gradient-sourcegraph49')
for name in ['source-proof-graph.json','source-coverage.json','caller-inventory.json','selected-token-inventory.json','input-bindings.json','selected-providers.json']:
 d=json.loads((p/name).read_text(encoding='utf-8')); print(name, type(d).__name__)
 if isinstance(d,dict):
  print([(k,len(v) if isinstance(v,(list,dict)) else v) for k,v in d.items() if k not in ['nodes','edges','entries','rows','bindings','providers']]);print('KEYS',list(d))
  for k in ['nodes','edges','entries','rows','bindings','providers']:
   if k in d: print(k,repr(d[k][0]) if isinstance(d[k],list) and d[k] else '')
 else: print(len(d),repr(d[0]))
r=json.loads(Path('runs/20261007-companion-priority/pbps-outer-gradient-source-topology-review49/direct-call.checks.json').read_text(encoding='utf-8')); print('MISSING',repr(r['missing_public_contract_references']))
print('FILES',[x.name for x in p.iterdir() if 'fderiv-context2' in x.name])
print((p/'schema-and-boundary.md').read_text(encoding='utf-8'))
