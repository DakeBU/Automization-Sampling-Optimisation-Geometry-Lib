import json
from pathlib import Path
R=Path('E:/Samplinglib');P=R/'runs/20261007-companion-priority/pbps-sharp-energy68'
for s in ['hilbert-sharp-quadratic-corrector-bound','pbps-sharp-corrector-energy']:
 for sub in ['publications','declaration_lessons']:
  x=json.loads((R/f'website/content/{sub}/{s}.json').read_text(encoding='utf-8'))
  if sub=='declaration_lessons':
   u=x['units'][0];print(s,'LEAN_STATEMENT',len(u['lean_statement']));print(u['lean_statement'])
  else:print('PUB '+s,json.dumps(x,ensure_ascii=False,indent=2))
