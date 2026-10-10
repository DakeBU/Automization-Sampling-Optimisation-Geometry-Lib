import json
from pathlib import Path
P=Path('E:/Samplinglib');R=P/'runs/20261007-companion-priority/pbps-sharp-energy68'
for name in ['publication-plan.json','conceptual-mirror-audit68.json','compiler-diagnosis68/parent-projection-route.json','compiler-diagnosis68/atomic-existential-route.json','compiler-diagnosis68/atomic-global-route.json','compiler-diagnosis68/local-global-proof-route.json','compiler-diagnosis68/redundant-ring-repair.json','compiler-diagnosis68/test-atomic-route.json','compiler-diagnosis68/test-local-global-proof-route.json']:
 x=json.loads((R/name).read_text(encoding='utf-8'));print('\nFILE '+name)
 if name=='publication-plan.json':
  print(json.dumps({k:v for k,v in x.items() if k not in ['private_literal_statements','statements','headers','literal_statements']},ensure_ascii=False,indent=2)[:12000])
 else:print(json.dumps(x,ensure_ascii=False,indent=2))
for sub in ['publications','declaration_lessons']:
 for name in ['hilbert-sharp-quadratic-corrector-bound','pbps-sharp-corrector-energy']:
  f=P/f'website/content/{sub}/{name}.json';x=json.loads(f.read_text(encoding='utf-8'));print('\nFILE '+str(f))
  def trim(v):
   if isinstance(v,dict):return {k:('[RAW full Lean retained, '+str(len(q))+' characters]' if k in ['lean','lean_code','lean_statement','lean_proof','statement_lean','definition','expanded_header'] and isinstance(q,str) and len(q)>1500 else trim(q)) for k,q in v.items()}
   if isinstance(v,list):return [trim(q) for q in v]
   return v
  print(json.dumps(trim(x),ensure_ascii=False,indent=2))
