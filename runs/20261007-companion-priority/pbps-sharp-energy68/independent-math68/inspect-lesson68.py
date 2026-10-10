import json,sys
from pathlib import Path
R=Path('E:/Samplinglib');s=sys.argv[1];f=R/('website/content/declaration_lessons/'+s+'.json');x=json.loads(f.read_text(encoding='utf-8'))
for u in x['units']:
 print(json.dumps({k:v for k,v in u.items() if k not in ['steps','lean_statement','statement']},ensure_ascii=False,indent=2))
 print('STATEMENT '+u['statement'])
 for i,q in enumerate(u['steps']):print(json.dumps(dict(step=i+1,**{k:v for k,v in q.items() if k!='lean'}),ensure_ascii=False))
