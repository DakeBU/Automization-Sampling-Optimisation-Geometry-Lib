"""Inspect exact current renderer output, without claiming browser validation."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib,json,sys
sys.path.insert(0,str(Path.cwd()/'website/scripts'))
import declaration_lessons as dl
r=Path(__file__).parent
lesson=json.loads(Path('website/content/declaration_lessons/pbps-actual-finite-history-tail-law.json').read_bytes())['units'][0]
text=dl.render_unit(lesson,'lessons/pbps-actual-finite-history-tail-law.html')
p=r/'reader-candidate87.html';assert not p.exists();p.write_text(text,encoding='utf8',newline='\n')
class Inspect(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.details=[];self.code=None;self.codes=[];self.events=[];self.steps=0
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='details':
   self.details.append(a)
   if a.get('data-inline-lean'):self.events.append(('lean',a['data-inline-lean'],a.get('class','')))
  if 'proof-roadmap' in a.get('class','').split():self.events.append(('roadmap','',''))
  if 'proof-reader-step' in a.get('class','').split():self.steps+=1
  if tag=='code':assert self.code is None;self.code=[]
 def handle_endtag(self,tag):
  if tag=='code' and self.code is not None:self.codes.append(''.join(self.code));self.code=None
 def handle_data(self,data):
  if self.code is not None:self.code.append(data)
i=Inspect();i.feed(text);decl=lesson['declaration'];spec=decl+'_statement'
assert i.steps==6 and all('open' not in d for d in i.details)
assert i.events[:3]==[('lean',decl,'inline-lean inline-lean-statement'),('lean',spec,'inline-lean inline-lean-proof'),('roadmap','','')]
assert sum(e[1]==spec for e in i.events)==1
for step in lesson['steps']:assert any(step['lean'].strip()==code.strip() for code in i.codes),step['title']
receipt=dict(status='PASS_LOCAL_RENDERER_HTML_CONTENT_ONLY',candidate=p.as_posix(),candidate_RAW_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),lesson_RAW_sha256=hashlib.sha256(Path('website/content/declaration_lessons/pbps-actual-finite-history-tail-law.json').read_bytes()).hexdigest(),initially_folded_details=len(i.details),exact_BODY_regions=6,literal_Prop_sibling_adjacent=True,visual_inspection=False,browser_interactivity=False,canonical_site_build=False,VERIFIED=False)
out=r/'reader-candidate87.receipt.json';assert not out.exists();out.write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf8',newline='\n');print(json.dumps(receipt))
