from pathlib import Path
from html.parser import HTMLParser
import hashlib,json,datetime
class Tree(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.root={'tag':'root','attrs':{},'children':[]};self.stack=[self.root];self.ids={}
 def handle_starttag(self,tag,attrs):
  node=dict(tag=tag,attrs=dict(attrs),children=[]);self.stack[-1]['children'].append(node)
  if node['attrs'].get('id'):self.ids[node['attrs']['id']]=node
  if tag not in {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}:self.stack.append(node)
 def handle_endtag(self,tag):
  for i in range(len(self.stack)-1,0,-1):
   if self.stack[i]['tag']==tag:del self.stack[i:];break
 def handle_data(self,data):self.stack[-1]['children'].append(data)
def text(n):return n if isinstance(n,str) else ''.join(text(c) for c in n['children'])
def maths(n):
 if isinstance(n,str):return []
 own=[n['attrs']['alttext']] if 'alttext' in n['attrs'] else []
 return own+[x for c in n['children'] for x in maths(c)]
r=Path(__file__).parent;p=r.parent/'phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html';raw=p.read_bytes()
assert hashlib.sha256(raw).hexdigest()=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
t=Tree();t.feed(raw.decode('utf8'));rows=[]
for anchor in ['S1.p1','S1.E1','S2.SS2.p1','A1.SS1.p1','A1.SS1.p2','A1.E1','A1.E2','A1.E7','A1.SS1.SSS0.Px1.p4']:
 node=t.ids[anchor];row=dict(anchor=anchor,element=node['tag'],formula_alttext=maths(node),private_text=text(node));rows.append(row)
 assert row['private_text'].strip()
 print(anchor,json.dumps(row['formula_alttext'],ensure_ascii=False)[:2400],row['private_text'][:1500] if not row['formula_alttext'] else '')
out=r/'root.primary89.read.private.json';assert not out.exists();out.write_text(json.dumps(dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),primary_RAW_sha256=hashlib.sha256(raw).hexdigest(),selected=rows,purpose='Direct current primary read before any89candidate/header/BODY. Existing tree parser reused without regex fragment truncation.'),ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
