from html.parser import HTMLParser
from pathlib import Path
import json,re,hashlib
SRC=Path(r'E:/Samplinglib/runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html')
OUT=Path(r'E:/Samplinglib/runs/20261007-companion-priority/pbps-actual-nonaccumulation78/fresh-source78')
class Node:
 def __init__(self,tag,attrs,parent=None):self.tag=tag; self.attrs=dict(attrs);self.parent=parent;self.children=[]
 def text(self):
  if self.tag in ('script','style'):return ''
  if self.tag=='math':return self.attrs.get('alttext','')
  return ''.join(c.text() if isinstance(c,Node) else c for c in self.children)
class Parser(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.root=Node('root',[]);self.stack=[self.root];self.nodes=[]
 def handle_starttag(self,t,a):
  n=Node(t,a,self.stack[-1]);self.stack[-1].children.append(n);self.nodes.append(n)
  if t not in ('area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'):self.stack.append(n)
 def handle_endtag(self,t):
  for i in range(len(self.stack)-1,0,-1):
   if self.stack[i].tag==t:self.stack=self.stack[:i];break
 def handle_data(self,d):self.stack[-1].children.append(d)
p=Parser();raw=SRC.read_bytes();p.feed(raw.decode('utf-8'))
if __name__=='__main__':
 print('SHA256',hashlib.sha256(raw).hexdigest())
 for n in p.nodes:
  id=n.attrs.get('id','');cl=n.attrs.get('class','');tx=re.sub(r'\s+',' ',n.text()).strip()
  if n.tag in ('h1','h2','h3','h4') or (id and ('A1' in id or 'Ex' in id or 'alg' in id.lower())) or (n.tag=='p' and re.search(r'non.explos|strong law|well.defined|smooth|Lipschitz|Assumption|exponential',tx,re.I)):
   print(id,n.tag,tx[:12000])
