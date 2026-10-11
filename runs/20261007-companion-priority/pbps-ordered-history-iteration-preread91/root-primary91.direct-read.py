from pathlib import Path
from html.parser import HTMLParser
import hashlib,json
r=Path(__file__).parent
primary=Path('runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html')
raw=primary.read_bytes();sha=lambda b:hashlib.sha256(b).hexdigest()
assert sha(raw)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
inventory=json.loads((r/'independent-source-first91/source-inventory91.primary-first.native.json').read_bytes())
class Text(HTMLParser):
 def __init__(self):super().__init__();self.math=0;self.parts=[]
 def handle_starttag(self,tag,attrs):
  if tag=='math':
   self.math+=1;self.parts.append('$'+dict(attrs).get('alttext','')+'$')
  elif tag in ('p','tr','div'):self.parts.append('\n')
 def handle_endtag(self,tag):
  if tag=='math':self.math-=1
 def handle_data(self,data):
  if not self.math:self.parts.append(data)
items=[]
for span in inventory['spans']:
 if span['id'] not in ['P91-V','P91-A7']:continue
 b=raw[span['byte_start']:span['byte_end_exclusive']]
 assert sha(b)==span['raw_sha256'] and len(b)==span['bytes']
 p=Text();p.feed(b.decode('utf8'));text=''.join(p.parts)
 items.append(dict(span=span,decoded_primary_text=text))
 print(span['id'],text)
out=r/'.private.root-primary91.exact-A7.json';assert not out.exists()
out.write_text(json.dumps(dict(primary_raw_sha256=sha(raw),purpose='Owner direct exact primary read before any91 header/Seal/BODY; private long text excluded from public archives.',items=items),ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
