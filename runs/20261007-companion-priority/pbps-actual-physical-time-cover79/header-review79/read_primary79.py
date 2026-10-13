from pathlib import Path
from html.parser import HTMLParser
import re,json,hashlib,datetime
R=Path('E:/Samplinglib');O=R/'runs/20261007-companion-priority/pbps-actual-physical-time-cover79/header-review79';O.mkdir(parents=True,exist_ok=True)
P=R/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'
b=P.read_bytes();assert hashlib.sha256(b).hexdigest()=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760';s=b.decode()
class Text(HTMLParser):
 def __init__(self):super().__init__();self.parts=[];self.math=False
 def handle_starttag(self,t,a):
  if t=='math':self.parts.append(' '+dict(a).get('alttext','')+' ');self.math=True
  if t in ['p','div','section','table']:self.parts.append('\n')
 def handle_endtag(self,t):
  if t=='math':self.math=False
 def handle_data(self,d):
  if not self.math:self.parts.append(d)
def subtree(anchor):
 m=re.search(r'<([a-zA-Z0-9]+)\b[^>]*\bid="'+re.escape(anchor)+r'"[^>]*>',s);assert m,anchor
 start=m.start();tag=m.group(1);depth=0
 for q in re.finditer(r'<(/?)'+re.escape(tag)+r'\b[^>]*>',s[start:]):
  depth+=-1 if q.group(1) else 1
  if depth==0:return s[start:start+q.end()]
 raise ValueError(anchor)
entries=[]
for a in ['S1.p1.1','S1.E1','S2.SS2','S3.SS2','A1.SS1']:
 raw=subtree(a);t=Text();t.feed(raw);name=a.replace('.','_')
 for suffix,data in [('.raw.html',raw.encode()),('.text.txt',''.join(t.parts).encode())]:
  p=O/(name+suffix);assert not p.exists();p.write_bytes(data)
 entries.append(dict(anchor=a,raw_sha256=hashlib.sha256(raw.encode()).hexdigest()))
(O/'primary-first-read79.json').write_text(json.dumps(dict(reviewer='/root/exact_verify77',created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),primary_raw_sha256=hashlib.sha256(b).hexdigest(),regions=entries,header_or_extractor_read_before_extraction=False),indent=2)+'\n',encoding='utf-8')
print('Independent primary excerpts frozen; candidate/extractor not read.')
