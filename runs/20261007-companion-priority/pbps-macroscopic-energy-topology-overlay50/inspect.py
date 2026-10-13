# coding: utf-8
import pathlib,json,sys
sys.stdout.reconfigure(encoding='utf-8');b=pathlib.Path('runs/20261007-companion-priority');o=b/'pbps-macroscopic-energy-sourcegraph50';c=json.loads((o/'caller-inventory.json').read_text(encoding='utf-8'));t=json.loads((o/'selected-token-inventory.json').read_text(encoding='utf-8'));g=json.loads((o/'source-proof-graph.json').read_text(encoding='utf-8'));p=json.loads((o/'selected-providers.json').read_text(encoding='utf-8'))
for i in [384,457]:
 r=c['entries'][i];print('CALL',i,r)
 print('TOKENS',[(n,x) for n,x in enumerate(t['entries']) if x.get('caller_start_utf8_byte0')==r['caller_start_utf8_byte0'] and x.get('caller_path')==r['caller_path']])
 print('EDGES',[(n,x) for n,x in enumerate(g['edges']) if x.get('caller',{}).get('byte_interval0')==[r['caller_start_utf8_byte0'],r['caller_end_utf8_byte0_exclusive']] and x.get('caller',{}).get('path')==r['caller_path']])
print('provider keys',p.keys())
review=json.loads((b/'pbps-macroscopic-energy-topology-review50/source-topology-review.json').read_text(encoding='utf-8'));print('reviewkeys',list(review));print(str(review.get('blockers',review.get('negative',{})))[:1800])
