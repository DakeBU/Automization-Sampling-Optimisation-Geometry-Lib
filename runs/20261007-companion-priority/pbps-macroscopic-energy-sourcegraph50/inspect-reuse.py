# coding: utf-8
import json,pathlib,sys
sys.stdout.reconfigure(encoding='utf-8');b=pathlib.Path('runs/20261007-companion-priority');o=b/'pbps-outer-gradient-topology-overlay49';g=json.loads((o/'source-proof-graph.after.json').read_text(encoding='utf-8')); a=json.loads((o/'original-primary-balanced-inventory.json.lf').read_text(encoding='utf-8'))['anchors']; print('oldanchors',[(x['id'],x['physical_lines1']) for x in a]);print('edge caller example',next(x for x in g['edges'] if 'caller' in str(x)) )
p=json.loads((o/'selected-providers.after.json').read_text(encoding='utf-8'));print('primitiveheaders',[(x['id'],x['physical_lines1'],x.get('snapshot')) for x in p if x['id'].startswith('api')])
