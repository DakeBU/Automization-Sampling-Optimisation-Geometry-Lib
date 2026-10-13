# coding: utf-8
import pathlib,json,sys
sys.stdout.reconfigure(encoding='utf-8');b=pathlib.Path('runs/20261007-companion-priority');o=b/'pbps-outer-gradient-topology-overlay49'
g=json.loads((o/'source-proof-graph.after.json').read_text());print('graph keys',list(g));print('nodes',len(g['nodes']),'edges',len(g['edges']));print('node0',g['nodes'][0]);print('edge0',g['edges'][0]);
for n in g['nodes']: print(n['id'],n.get('kind'),n.get('label'),str(n.get('source_refs',[]))[:160])
p=json.loads((o/'selected-providers.after.json').read_text());print('provider example',p[0]);print('provider ids',[x['id'] for x in p]);
