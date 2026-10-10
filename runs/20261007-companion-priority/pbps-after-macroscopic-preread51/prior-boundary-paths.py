# coding: utf-8
import pathlib,json,sys
sys.stdout.reconfigure(encoding='utf-8');b=pathlib.Path('runs/20261007-companion-priority/pbps-after-energy-preread50')
for n in ['weighted-public-bindings.json','selected-api-bindings.json']:
 x=json.loads((b/n).read_text(encoding='utf-8-sig'));print(n,type(x).__name__)
 if isinstance(x,list):
  for r in x:print(r.get('path'),r.get('declaration'),r.get('physical_lines1',r.get('physical_lines')))
 else:print(list(x))
