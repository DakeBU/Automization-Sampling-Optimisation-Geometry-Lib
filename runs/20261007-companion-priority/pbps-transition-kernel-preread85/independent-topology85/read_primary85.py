from pathlib import Path
from html.parser import HTMLParser
import hashlib,json,datetime
R=Path('E:/Samplinglib');O=Path(__file__).parent
P=R/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html';raw=P.read_bytes();assert hashlib.sha256(raw).hexdigest()=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
class Text(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.stack=[];self.ids={};self.math=0
 def append(self,d):
  for tag,i in self.stack:
   if i:self.ids[i].append(d)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs);i=a.get('id')
  if tag=='math':self.append(a.get('alttext',''));self.math+=1
  self.stack.append((tag,i))
  if i:self.ids[i]=[]
  if tag in ['meta','link','img','br','hr','input','source','wbr']:self.stack.pop()
 def handle_endtag(self,tag):
  if tag=='math':self.math-=1
  for k in range(len(self.stack)-1,-1,-1):
   if self.stack[k][0]==tag:self.stack=self.stack[:k];break
 def handle_data(self,d):
  if not self.math:self.append(d)
p=Text();p.feed(raw.decode('utf8'));texts={i:' '.join(' '.join(x).split()) for i,x in p.ids.items()}
selected={i:t for i,t in texts.items() if i.startswith('A1.SS1') or i in ['S1.E1','S1.E2','S1.E3'] or i.startswith('S2.SS2') or i.startswith('alg1')}
out=dict(created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),reviewer_id='/root/exact_verify77',primary=dict(path=P.relative_to(R).as_posix(),RAW_sha256=hashlib.sha256(raw).hexdigest(),RAW_bytes=len(raw)),source_first=True,inventory_graph_candidate_not_read=True,selection='Direct primary whole AppendixA.1 and conditional/Gaussian augmentation Section2.2; normalized MathML alttext parser, not extractor content.',elements=selected)
with (O/'independent-primary-first-read85.json').open('x',encoding='utf8') as f:json.dump(out,f,ensure_ascii=False,indent=2);f.write('\n')
for i in ['A1.SS1.p1.1','A1.SS1.p2.2','A1.Ex9','A1.SS1.SSS0.Px1.p4.2','A1.SS1.SSS0.Px1.p4.3','A1.SS1.SSS0.Px1.p5.1','A1.SS1.SSS0.Px1.p5.2','A1.SS1.SSS0.Px1.p5.3','A1.SS1.SSS0.Px1.p6.1','A1.SS1.SSS0.Px1.p6.2']:
 print(i,texts.get(i,'NO DIRECT ID'))
for i,t in texts.items():
 if i.startswith('S2.SS2') and '.p' in i:print(i,t)
