from pathlib import Path
from html.parser import HTMLParser
import hashlib,json,re,datetime
R=Path('E:/Samplinglib');O=R/'runs/20261007-companion-priority/pbps-actual-small-time-continuity82/header-review82'
S=R/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html';raw=S.read_bytes();assert hashlib.sha256(raw).hexdigest()=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
class Parser(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.stack=[];self.nodes=[];self.math=0
 def handle_starttag(self,tag,attrs):
  at=dict(attrs);n=dict(tag=tag,id=at.get('id'),text=[]);self.stack.append(n)
  if tag=='math':
   if self.math==0:
    for q in self.stack:q['text'].append(at.get('alttext',''))
   self.math+=1
  if tag in {'br','hr','img','meta','link','input','source','wbr','area','base','col','embed','param','track'}:self.handle_endtag(tag)
 def handle_endtag(self,tag):
  if tag=='math':self.math=max(0,self.math-1)
  found=next((i for i in range(len(self.stack)-1,-1,-1) if self.stack[i]['tag']==tag),None)
  if found is None:return
  ended=self.stack[found:];self.stack=self.stack[:found]
  for n in ended:
   if n['id']:self.nodes.append(dict(id=n['id'],tag=n['tag'],text=re.sub(r'\s+',' ',' '.join(n['text'])).strip()))
 def handle_data(self,data):
  if not self.math:
   for q in self.stack:q['text'].append(data)
p=Parser();p.feed(raw.decode('utf8'))
ids={'S1.E1','S2.SS2.p1.1','S3.Thmtheorem1','A1.SS2.p3.1','A1.SS2.p4.1'}
selected=[n for n in p.nodes if n['id'] in ids or (n['id'].startswith('A1.') and (n['id'].startswith('A1.SS1') or n['id'] in {'A1.Ex22','A1.Ex9','A1.Ex10','A1.Ex11','A1.Ex12','A1.Ex13','A1.Ex14','A1.Ex15','A1.Ex16','A1.Ex17','A1.Ex18','A1.Ex19','A1.Ex20','A1.Ex21','A1.Ex23','A1.E4','A1.E5','A1.E6','A1.E7','A1.E8','A1.EGx4'}) and n['tag'] in {'p','table'})]
for n in selected:n['text_utf8_sha256']=hashlib.sha256(n['text'].encode()).hexdigest()
out=dict(status='PRIMARY_REREAD_BEFORE_EXTRACTOR_INVENTORY_GRAPH',created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),reviewer='/root/exact_verify77',source=dict(path=S.relative_to(R).as_posix(),RAW_sha256=hashlib.sha256(raw).hexdigest(),RAW_bytes=len(raw)),parser='Own stdlib HTMLParser; use math alttext once and skip MathML/TeX annotation duplicates. No extractor scripts/rationale/verdict consulted.',regions=selected)
with (O/'independent-primary-readback82.json').open('x',encoding='utf8',newline='\n') as f:json.dump(out,f,ensure_ascii=False,indent=2);f.write('\n')
for n in selected:print(n['id'],n['text'])
