# coding: utf-8
import json,pathlib,sys
sys.stdout.reconfigure(encoding='utf-8')
b=pathlib.Path('runs/20261007-companion-priority'); o=b/'pbps-outer-gradient-topology-overlay49'
for name in ['source-graph.after.json','source-coverage.after.json','caller-inventory.after.json','selected-token-inventory.after.json','original-selected-providers.json.lf','original-primary-balanced-inventory.json.lf']:
 p=o/name
 if not p.exists(): print('missing',name);continue
 x=json.loads(p.read_text(encoding='utf-8-sig'));print(name,type(x).__name__, list(x)[:16] if isinstance(x,dict) else len(x))
 if isinstance(x,dict):
  for k,v in x.items():
   if isinstance(v,list): print('LIST',k,len(v),str(v[:1])[:2500])
 print()
p=b/'next-ready-preread47/primary-pbps.raw.snapshot.html'; lines=p.read_text(encoding='utf-8').splitlines()
for n in range(3507,3639):
 s=lines[n-1]
 if 'id=' in s: print(n,s[:220])
