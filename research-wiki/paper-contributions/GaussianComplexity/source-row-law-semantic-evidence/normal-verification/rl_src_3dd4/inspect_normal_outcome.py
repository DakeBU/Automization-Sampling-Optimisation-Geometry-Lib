import json,pathlib,sys
ROOT=pathlib.Path('/Users/zhouhuanjian/ASTIS-GC');sys.path.insert(0,str(ROOT))
from tools import astis_advance as a
T='ASTIS-SA-20261112-GaussianComplexitySourceRowLaw';rows=[json.loads(x) for x in (ROOT/'runs/substantive_advances.jsonl').read_text().splitlines() if x.strip()];s=a._replay_advances(rows)[T]
v=[r for r in rows if r.get('advance_id')==T and r.get('to_state')=='VERIFIED'];print(json.dumps({'target':T,'actual_state':s['state'],'actual_VERIFIED_events':len(v),'retry_policy':'never replay a successful append','inspection_reason':'Rejected original precheck count assertion before any normal transition call'},indent=2));assert s['state']=='PROVED_LOCAL' and len(v)==0
