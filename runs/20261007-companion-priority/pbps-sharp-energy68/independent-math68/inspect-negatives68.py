import json
from pathlib import Path
R=Path('E:/Samplinglib/runs/20261007-companion-priority/pbps-sharp-energy68');f=R/'compiler-diagnosis68/diagnostics-removed.json';x=json.loads(f.read_text(encoding='utf-8'))
def bounded(v):
 if isinstance(v,dict):return {k:bounded(q) for k,q in v.items()}
 if isinstance(v,list):return [bounded(q) for q in v]
 if isinstance(v,str) and len(v)>500:return dict(string_length=len(v),prefix=v[:180],tail=v[-120:])
 return v
print(json.dumps(bounded(x),ensure_ascii=False,indent=2))
