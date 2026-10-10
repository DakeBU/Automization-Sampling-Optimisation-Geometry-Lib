# -*- coding: utf-8 -*-
import pathlib,json,sys
sys.stdout.reconfigure(encoding='utf-8');d=pathlib.Path('E:/Samplinglib/runs/20261007-companion-priority/pbps-outer-gradient-sourcegraph49');g=json.loads((d/'source-proof-graph.json').read_text(encoding='utf-8'));valid={n['id'] for n in g['nodes']};fix=lambda n:'P.typing' if n in ['P.fderiv-context','P.fderiv-context2'] else n
cov=json.loads((d/'source-coverage.json').read_text(encoding='utf-8'))
for row in cov['rows']:row['node_ids']=[fix(n) for n in row['node_ids']];assert all(n in valid for n in row['node_ids'])
for e in g['edges']:e['from_node']=fix(e['from_node']);e['to_node']=fix(e['to_node'])
g['edges']=[e for e in g['edges'] if e['from_node']!=e['to_node']]
inv=json.loads((d/'caller-inventory.json').read_text(encoding='utf-8'));tok=json.loads((d/'selected-token-inventory.json').read_text(encoding='utf-8'));anchor_nodes={}
for n in g['nodes']:
 for a in n.get('primary_anchors',[]):anchor_nodes.setdefault(a,[]).append(n['id'])
for item in inv['entries']+tok['entries']:
 if 'caller_node' in item:item['caller_node']=fix(item['caller_node'])
for item in inv['entries']:
 if item['classification']!='printed-primary-reference':continue
 item['caller_node_ids']=anchor_nodes.get(item['caller_primary_anchor'],[])
 for caller in item['caller_node_ids']:
  for ref in item['resolved_source_nodes']:
   if ref==caller:continue
   consequence=item['source_reference']=='A2.E13' and item['caller_primary_anchor']=='A3.SS1.p3.7'
   g['edges'].append(dict(from_node=caller if consequence else ref,to_node=ref if consequence else caller,relation='printed-source-stated-consequence' if consequence else 'printed-source-reuse',caller=dict(path=item['caller_path'],line1=item['caller_physical_line1'],anchor=item['caller_primary_anchor']),reference=item['source_reference']))
for e in g['edges']:assert e['from_node'] in valid and e['to_node'] in valid,(e['from_node'],e['to_node'])
for f,o in [('source-proof-graph.json',g),('source-coverage.json',cov),('caller-inventory.json',inv),('selected-token-inventory.json',tok)]: (d/f).write_text(json.dumps(o,indent=2,ensure_ascii=False),encoding='utf-8')
print('nodes',len(g['nodes']),'edges',len(g['edges']))
