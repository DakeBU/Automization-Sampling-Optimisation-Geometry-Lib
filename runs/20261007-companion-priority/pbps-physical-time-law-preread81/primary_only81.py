from pathlib import Path
from html.parser import HTMLParser
import hashlib,re
SRC=Path('E:/Samplinglib/runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html')
class Element:
 def __init__(self,tag,attrs):self.tag=tag;self.attrs=dict(attrs);self.content=[]
 def text(self):
  if self.tag in ('script','style'):return ''
  if self.tag=='math':return self.attrs.get('alttext','')
  return ''.join(x.text() if isinstance(x,Element) else x for x in self.content)
class Primary81(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.root=Element('root',[]);self.stack=[self.root];self.elements=[]
 def handle_starttag(self,tag,attrs):
  n=Element(tag,attrs);self.stack[-1].content.append(n);self.elements.append(n)
  if tag not in ('area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'):self.stack.append(n)
 def handle_endtag(self,tag):
  for i in range(len(self.stack)-1,0,-1):
   if self.stack[i].tag==tag:self.stack=self.stack[:i];return
 def handle_data(self,s):self.stack[-1].content.append(s)
raw=SRC.read_bytes();assert hashlib.sha256(raw).hexdigest()=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
tree=Primary81();tree.feed(raw.decode('utf-8'))
if __name__=='__main__':
 for n in tree.elements:
  ident=n.attrs.get('id','')
  if (ident.startswith(('S2.SS2.','S3.','A1.SS1.')) and n.tag in ('p','table')) or ident in ('license-tr','S1.p1','S1.E1','S2.E4','S2.E5','S2.E6','S2.E7','S2.E8','alg1') or ident.startswith('A1.Ex'):
   print(ident,re.sub(r'\s+',' ',n.text()).strip())
