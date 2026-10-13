# coding: utf-8
import pathlib,json,re,sys
sys.stdout.reconfigure(encoding='utf-8');o=pathlib.Path('runs/20261007-companion-priority/pbps-macroscopic-energy-sourcegraph50'); ps=json.loads((o/'selected-providers.json').read_text(encoding='utf-8'))['new']; tokens=set()
for p in ps:
 b=(o/(p['snapshot']+'.lf')).read_text(encoding='utf-8')
 for line in b.splitlines():
  line=line.split('--')[0];tokens.update(re.findall(r'[^\W\d]\w*(?:\.[^\W\d]\w*)*',line))
print('TOKENS',len(tokens));print(' '.join(sorted(tokens)))
