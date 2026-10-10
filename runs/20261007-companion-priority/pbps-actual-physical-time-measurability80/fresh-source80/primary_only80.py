from pathlib import Path
from html.parser import HTMLParser
import hashlib,re
SRC=Path(r'E:/Samplinglib/runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html')
OUT=Path(r'E:/Samplinglib/runs/20261007-companion-priority/pbps-actual-physical-time-measurability80/fresh-source80')
class SourceElement:
 def __init__(self,tag,attrs):self.tag=tag;self.attrs=dict(attrs);self.content=[]
 def text(self):
  if self.tag in ('script','style'):return ''
  if self.tag=='math':return self.attrs.get('alttext','')
  return ''.join(x.text() if isinstance(x,SourceElement) else x for x in self.content)
class PrimaryOnly80(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.root=SourceElement('root',[]);self.stack=[self.root];self.elements=[]
 def handle_starttag(self,tag,attrs):
  n=SourceElement(tag,attrs);self.stack[-1].content.append(n);self.elements.append(n)
  if tag not in ('area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'):self.stack.append(n)
 def handle_endtag(self,tag):
  for i in range(len(self.stack)-1,0,-1):
   if self.stack[i].tag==tag:self.stack=self.stack[:i];return
 def handle_data(self,s):self.stack[-1].content.append(s)
raw=SRC.read_bytes();assert hashlib.sha256(raw).hexdigest()=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
source=PrimaryOnly80();source.feed(raw.decode('utf-8'))
if __name__=='__main__':
 ids=['license-tr','S1.p1','S2.SS2.p1.1','S2.E4','S3.E4','alg1','S3.Thmtheorem1.p1.1','A1.Ex1','A1.Ex2','A1.Ex3','A1.E1','A1.E2','A1.Ex4','A1.Ex5','A1.Ex6','A1.Ex7','A1.Ex8','A1.Ex9','A1.SS1.SSS0.Px1.p4.4']
 for n in source.elements:
  ident=n.attrs.get('id','')
  if ident in ids or (n.tag=='p' and ident.startswith(('A1.SS1.p1.','A1.SS1.p2.','A1.SS1.p3.'))):print(ident,re.sub(r'\s+',' ',n.text()).strip())
