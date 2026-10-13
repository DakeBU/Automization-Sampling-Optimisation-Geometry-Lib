from pathlib import Path
from html.parser import HTMLParser
import hashlib,json,re
R=Path('E:/Samplinglib');D=R/'runs/20261007-companion-priority/pbps-path-law-preread86'
p=R/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'
assert hashlib.sha256(p.read_bytes()).hexdigest()=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
ids=['S1.E1','S2.SS2.p1.1','A1.E1','A1.E2','A1.Ex1','A1.Ex2','A1.Ex3','A1.SS1.p2.1','A1.SS1.SSS0.Px1.p4.2','A1.E7']
class Parser(HTMLParser):
 def __init__(self): super().__init__();self.stack=[];self.out={};self.math=0
 def handle_starttag(self,t,attrs):
  a=dict(attrs);i=a.get('id');self.stack.append((t,i))
  if i in ids:self.out[i]=[]
  if t=='math':
   if self.math==0:
    for _,k in self.stack:
     if k in self.out:self.out[k].append(a.get('alttext',''))
   self.math+=1
  if t in ['br','wbr','img','meta','link','input','hr','source']:self.stack.pop()
 def handle_endtag(self,t):
  if t=='math':self.math=max(0,self.math-1)
  for j in range(len(self.stack)-1,-1,-1):
   if self.stack[j][0]==t:del self.stack[j:];break
 def handle_data(self,s):
  if self.math==0:
   for _,k in self.stack:
    if k in self.out:self.out[k].append(s)
z=Parser();z.feed(p.read_text(encoding='utf-8'));texts={i:' '.join(' '.join(z.out[i]).split()) for i in ids}
(D/'root.primary-anchor-read86.private.json').write_text(json.dumps(texts,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for i,v in texts.items():print(i+': '+v)
