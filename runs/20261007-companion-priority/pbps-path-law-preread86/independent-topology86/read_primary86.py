from pathlib import Path
from html.parser import HTMLParser
import datetime,hashlib,json
R=Path('E:/Samplinglib');O=Path(__file__).parent;P=R/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'
raw=P.read_bytes();assert hashlib.sha256(raw).hexdigest()=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
class Read(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.stack=[];self.active=[];self.records=[];self.math=0
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if t in ['meta','link','img','br','hr','input','wbr','source']:return
  self.stack.append(t)
  if t=='math':
   self.math+=1
   if self.math==1:
    for e in self.active:e['chunks'].append(' '+a.get('alttext','')+' ')
  ident=a.get('id','');classes=a.get('class','').split()
  if (ident.startswith('A1') and any(k in classes for k in ['ltx_para','ltx_equation','ltx_theorem','ltx_title'])) or ident in ['S1.p1.1','S1.E1','S2.SS2.p1.1']:
   self.active.append(dict(id=ident,depth=len(self.stack),chunks=[]))
 def handle_data(self,d):
  if not self.math:
   for e in self.active:e['chunks'].append(d)
 def handle_endtag(self,t):
  if t not in self.stack:return
  depth=len(self.stack)-self.stack[::-1].index(t)
  for e in self.active[:]:
   if e['depth']>=depth:
    text=' '.join(''.join(e['chunks']).split());self.records.append(dict(id=e['id'],text=text,normalized_text_sha256=hashlib.sha256(text.encode()).hexdigest()));self.active.remove(e)
  self.stack=self.stack[:depth-1]
  if t=='math':self.math=max(0,self.math-1)
p=Read();p.feed(raw.decode('utf8'))
with (O/'primary-first86.json').open('x',encoding='utf8',newline='\n') as f:json.dump(dict(reviewer_id='/root/exact_verify77',created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),primary=dict(path=P.relative_to(R).as_posix(),RAW_sha256=hashlib.sha256(raw).hexdigest(),RAW_bytes=len(raw)),extractor_artifacts_read=False,Lean_BODY_read=False,regions=p.records),f,ensure_ascii=False,indent=2);f.write('\n')
with (O/'reader-setup-diagnosis86.json').open('x',encoding='utf8',newline='\n') as f:json.dump(dict(status='READER_SETUP_ONLY',observed_exit=1,observed_error="ModuleNotFoundError: No module named 'bs4'",action='Used standard-library HTMLParser in immutable read_primary86.py; no source bytes modified or dependency installed.',native_full_trace_file_claimed=False),f,indent=2);f.write('\n')
print('PRIMARY-FIRST REGIONS',len(p.records))
for e in p.records:print(e['id'],e['text'])
