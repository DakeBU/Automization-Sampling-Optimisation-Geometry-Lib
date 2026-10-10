from pathlib import Path
from html.parser import HTMLParser
import hashlib,json,datetime
R=Path('E:/Samplinglib');O=Path(__file__).parent;B=O.parent
raw=(R/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html').read_bytes()
assert hashlib.sha256(raw).hexdigest()=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
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
p=Text();p.feed(raw.decode('utf8'));inv=json.loads((B/'source_inventory84.json').read_text(encoding='utf8'));rows=[]
for a in inv['source_anchor_coverage']:
 i=a['source_id'];assert i in p.ids
 t=' '.join(' '.join(p.ids[i]).split());h=hashlib.sha256(t.encode()).hexdigest()
 rows.append(dict(source_id=i,independent_normalized_text=t,independent_normalized_sha256=h,frozen_normalized_sha256=a['normalized_anchor_sha256'],normalized_hash_equal=h==a['normalized_anchor_sha256']))
with (O/'independent-26-anchor-readback84.json').open('x',encoding='utf8') as f:json.dump(dict(created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),primary_RAW_sha256=hashlib.sha256(raw).hexdigest(),authority='Exact primary RAW; normalized hashes are parser recipes, not independent mathematical certificates.',anchors=rows),f,ensure_ascii=False,indent=2);f.write('\n')
for e in rows:print(e['source_id'],'MATCH' if e['normalized_hash_equal'] else 'PARSER-DIFFERENCE',e['independent_normalized_text'])
