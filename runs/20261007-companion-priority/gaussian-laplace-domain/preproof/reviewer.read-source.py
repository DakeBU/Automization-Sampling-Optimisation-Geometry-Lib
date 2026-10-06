from html.parser import HTMLParser
from pathlib import Path
import hashlib,json
P=Path('runs/20261007-companion-priority/gaussian-laplace-domain/preproof')
class Reader(HTMLParser):
 def __init__(self): super().__init__(); self.math=0; self.out=[]
 def handle_starttag(self,t,a):
  d=dict(a)
  if t=='math': self.math+=1; self.out.append(' ['+d.get('alttext','')+'] ')
  elif not self.math and t in ('p','div','section','h1','h2','h3','h4','tr'): self.out.append('\n'+ ('@'+d['id']+' ' if 'id' in d else ''))
 def handle_endtag(self,t):
  if t=='math': self.math-=1
 def handle_data(self,s):
  if not self.math: self.out.append(s)
r=Reader(); raw=(P/'source-primary.raw.snapshot.html').read_bytes();r.feed(raw.decode());text=''.join(r.out);(P/'reviewer.primary-readable.txt').write_text(text,encoding='utf-8')
print('RAW SHA256',hashlib.sha256(raw).hexdigest());print('TEXT LENGTH',len(text));print(text[:78000])
