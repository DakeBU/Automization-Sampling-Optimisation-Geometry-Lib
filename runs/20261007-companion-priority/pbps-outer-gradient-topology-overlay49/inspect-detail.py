# -*- coding: utf-8 -*-
import json,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');p=Path('runs/20261007-companion-priority/pbps-outer-gradient-sourcegraph49')
g=json.loads((p/'source-proof-graph.json').read_text(encoding='utf-8'))
for i in [244,252,253,254]: print('EDGE',i,json.dumps(g['edges'][i],ensure_ascii=False))
for file,key in [('caller-inventory.json','entries'),('selected-token-inventory.json','entries')]:
 d=json.loads((p/file).read_text(encoding='utf-8'))
 for i,e in enumerate(d[key]):
  if e.get('caller_selected_provider')=='selected-P.fderiv-context2' and e.get('caller_physical_line1')==364: print(file,i,json.dumps(e,ensure_ascii=False))
for e in g['nodes']:
 if e['id'] in ['P.typing','P.fderiv','S.compact','R.rough','R.operator','P.integral','P.map','P.prob','P.mathlib-variance']: print('NODE',json.dumps(e,ensure_ascii=False))
for x in json.loads((p/'selected-providers.json').read_text(encoding='utf-8')):
 if x['id'] in ['additional-P.mean-bound','additional-P.map-prob','additional-P.compact-bound','api-P.var-sub','parent-context-GibbsAugmentation','parent-context-GaussianReflection','selected-P.fderiv-context2']: print('PROVIDER',json.dumps(x,ensure_ascii=False))
