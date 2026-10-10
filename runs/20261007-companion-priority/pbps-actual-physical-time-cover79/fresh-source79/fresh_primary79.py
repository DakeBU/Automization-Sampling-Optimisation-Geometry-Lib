from html.parser import HTMLParser
from pathlib import Path
import re,hashlib
SRC=Path(r'E:/Samplinglib/runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html')
OUT=Path(r'E:/Samplinglib/runs/20261007-companion-priority/pbps-actual-physical-time-cover79/fresh-source79')
class Elem:
 def __init__(self,t,a):self.tag=t;self.attrs=dict(a);self.parts=[]
 def txt(self):
  if self.tag in ('style','script'):return ''
  if self.tag=='math':return self.attrs.get('alttext','')
  return ''.join(x.txt() if isinstance(x,Elem) else x for x in self.parts)
class FreshParser(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.root=Elem('root',[]);self.stack=[self.root];self.items=[]
 def handle_starttag(self,t,a):
  n=Elem(t,a);self.stack[-1].parts.append(n);self.items.append(n)
  if t not in ('area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'):self.stack.append(n)
 def handle_endtag(self,t):
  for j in range(len(self.stack)-1,0,-1):
   if self.stack[j].tag==t:self.stack=self.stack[:j];return
 def handle_data(self,d):self.stack[-1].parts.append(d)
raw=SRC.read_bytes();assert hashlib.sha256(raw).hexdigest()=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
parsed=FreshParser();parsed.feed(raw.decode('utf-8'))
if __name__=='__main__':
 wanted=['S1.p1','S1.E1','S2.SS2.p1.1','S2.E4','S3.E4','S3.E8','S3.E9','alg1','A1.Ex1','A1.Ex2','A1.Ex3','A1.E1','A1.E2','A1.Ex9']
 for n in parsed.items:
  a=n.attrs.get('id','')
  if a in wanted or (n.tag=='p' and a.startswith(('A1.SS1.p1.','A1.SS1.p2.','A1.SS1.p3.'))):print(a,re.sub(r'\s+',' ',n.txt()).strip())
