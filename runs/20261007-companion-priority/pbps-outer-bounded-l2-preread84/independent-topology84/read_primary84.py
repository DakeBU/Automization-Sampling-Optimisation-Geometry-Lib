from pathlib import Path
from html.parser import HTMLParser
import hashlib,json,datetime
R=Path('E:/Samplinglib');O=Path(__file__).parent
P=R/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'
raw=P.read_bytes();assert hashlib.sha256(raw).hexdigest()=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
class Parser(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.stack=[];self.elements={}
 def handle_starttag(self,tag,attrs):
  a=dict(attrs);i=a.get('id');self.stack.append((tag,i))
  if i:self.elements[i]={'tag':tag,'attrs':a,'text':[]}
  if tag in ['meta','link','img','br','hr','input','source','wbr']:self.stack.pop()
 def handle_endtag(self,tag):
  for k in range(len(self.stack)-1,-1,-1):
   if self.stack[k][0]==tag:self.stack=self.stack[:k];break
 def handle_data(self,data):
  for tag,i in self.stack:
   if i:self.elements[i]['text'].append(data)
p=Parser();p.feed(raw.decode('utf8'))
for e in p.elements.values():e['text']=' '.join(' '.join(e['text']).split())
selected={i:e for i,e in p.elements.items() if i.startswith('A1.SS1') or i in ['S1.E1','S1.E2','S1.E3'] or 'algorithm' in e['attrs'].get('class','')}
out={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'primary_RAW_sha256':hashlib.sha256(raw).hexdigest(),'reviewer':'/root/exact_verify77','source_first':True,'inventory_graph_candidate_not_read':True,'selection':'Whole AppendixA.1 + source conditional/kernel equations and algorithms; selected directly from primary ids, not frozen84 graph.','elements':selected}
with (O/'independent-primary-read84.json').open('x',encoding='utf8') as f:json.dump(out,f,ensure_ascii=False,indent=2);f.write('\n')
for i,e in p.elements.items():
 if e['tag'] in ['h2','h3','h4'] or 'algorithm' in e['attrs'].get('class',''):print(i,e['text'])
for i in ['A1.SS1.SSS0.Px1.p6.1','A1.SS1.SSS0.Px1.p6.2','A1.Ex22']:
 print('\nSOURCE',i,'\n',p.elements.get(i))
