from pathlib import Path
from html.parser import HTMLParser
import hashlib,json,re,datetime
out=Path(r'E:/Samplinglib/runs/20261007-companion-priority/pbps-centered-root-preproof64/independent-primary64')
src=Path(r'E:/Samplinglib/runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html')
raw=src.read_bytes(); expected='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
assert hashlib.sha256(raw).hexdigest()==expected
s=raw.decode('utf8'); lines=[0]
for m in re.finditer('\n',s):lines.append(m.end())
class Index(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.stack=[];self.nodes={};self.heads=[]
 def location(self):ln,col=self.getpos();return lines[ln-1]+col
 def handle_starttag(self,tag,attrs):
  at=dict(attrs);pos=self.location();entry={'tag':tag,'id':at.get('id'),'start_char':pos,'class':at.get('class','')}
  if tag not in ['meta','link','img','br','hr','input','source','wbr']:self.stack.append(entry)
  if tag in ['h1','h2','h3','h4','h5']:self.heads.append(entry)
 def handle_endtag(self,tag):
  for j in range(len(self.stack)-1,-1,-1):
   if self.stack[j]['tag']==tag:
    pos=self.location();end=s.find('>',pos)+1
    for entry in self.stack[j:]:
     entry['end_char']=end
     if entry['id']:self.nodes[entry['id']]=entry
    del self.stack[j:];break
p=Index();p.feed(s)
class Readable(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.bits=[];self.mathdepth=0
 def handle_starttag(self,tag,attrs):
  at=dict(attrs)
  if tag=='math':self.bits.append('`'+at.get('alttext','[MATH WITHOUT ALTTEXT]')+'`');self.mathdepth+=1
  elif self.mathdepth:return
  elif tag in ['p','div','table','tr','h1','h2','h3','h4','h5','br','li']:self.bits.append('\n')
 def handle_endtag(self,tag):
  if tag=='math':self.mathdepth-=1
  elif not self.mathdepth and tag in ['p','div','table','tr','h1','h2','h3','h4','h5','li']:self.bits.append('\n')
 def handle_data(self,d):
  if not self.mathdepth:self.bits.append(d)
 def text(self):return re.sub(r'\n[ \t]*\n(?:[ \t]*\n)*','\n\n',''.join(self.bits)).strip()
def readable(t):q=Readable();q.feed(t);return q.text()
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
lease={'schema':1,'owner':'/root/preproof_centered64','owned_directory':str(out),'state':'OPEN','opened_utc':now,'allowed_actions':['primary-source-preread','owned-evidence-writing','bounded-read-only-API-inspection'],'forbidden_actions':['Lean-authoring','compile','canonical-ledger-or-cell-or-site-or-Git-mutation','theorem-review-without-frozen-header']}
(out/'owned-lease.json').write_text(json.dumps(lease,indent=2)+'\n',encoding='utf8')
(out/'source-index.json').write_text(json.dumps({'source':str(src),'raw_sha256':expected,'bytes':len(raw),'nodes':p.nodes},indent=2)+'\n',encoding='utf8')
heads=[{'text':readable(s[e['start_char']:e['end_char']]),'container':next((n['id'] for n in p.nodes.values() if n['start_char']<e['start_char'] and n['end_char']>=e['end_char'] and n['tag'] in ['section','div']),None),'start_char':e['start_char']} for e in p.heads]
(out/'primary-preread-open-receipt.json').write_text(json.dumps({'source':str(src),'expected_raw_sha256':expected,'observed_raw_sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'actual_read_utc':now,'role':'independent-primary-preread','source_first':True,'candidate_or_old_Lean_or_verdict_read':False,'parser':'stdlib HTMLParser; math alttext preserved'},indent=2)+'\n',encoding='utf8')
print(json.dumps(heads,ensure_ascii=False,indent=2))
for id,e in p.nodes.items():
 if e['class'].startswith('ltx_equation'):
  t=readable(s[e['start_char']:e['end_char']])
  if re.search(r'\((?:B\.1[0-6]|C\.[1-4]|D\.1|2\.[67]|1\.1)\)',t):print(id,t[:1300])

