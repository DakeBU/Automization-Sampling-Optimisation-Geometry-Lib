from pathlib import Path
from html.parser import HTMLParser
import json,hashlib,datetime
root=Path('E:/Samplinglib');out=Path(__file__).resolve().parent
p=root/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'
b=p.read_bytes();assert hashlib.sha256(b).hexdigest()=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
lines=b.splitlines(keepends=True)
class Read(HTMLParser):
 def __init__(self):super().__init__();self.text=[];self.math=[]
 def handle_data(self,d):self.text.append(d)
 def handle_starttag(self,t,a):
  a=dict(a)
  if t=='math' and a.get('alttext'):self.math.append(a['alttext'])
spans=[]
for anchor,lo,hi in [('license',257,261),('standing',349,361),('eta',613,616),('center',1486,1492),('actual-clock-A1-E1-E2',2859,2911),('density-iteration-A1-E7',3147,3173),('joint-Borel-A2',3325,3338)]:
 chunk=b''.join(lines[lo-1:hi]);r=Read();r.feed(chunk.decode())
 s=dict(anchor=anchor,raw_line_start=lo,raw_line_end=hi,byte_start_zero_based=sum(map(len,lines[:lo-1])),byte_end_exclusive=sum(map(len,lines[:hi])),raw_span_sha256=hashlib.sha256(chunk).hexdigest(),raw_html=chunk.decode(),readable_text=' '.join(' '.join(r.text).split()),math_alttext=r.math)
 spans.append(s);print(anchor,s['readable_text']);print('FORMULAE',json.dumps(r.math,ensure_ascii=False))
private=out/'primary89.final-preread.private.json';assert not private.exists();private.write_text(json.dumps(dict(source=str(p),source_raw_sha256=hashlib.sha256(b).hexdigest(),spans=spans),ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
chron=out/'chronology.final-source89.native.jsonl';assert not chron.exists();chron.write_text(json.dumps(dict(event='DIRECT_PRIMARY89_REREAD_BEFORE_PRODUCTION_BODY_LESSON_DECODER_OR_REVIEW_PACKET',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),source_path=str(p),source_raw_sha256=hashlib.sha256(b).hexdigest(),private_extract_path=str(private),private_extract_raw_sha256=hashlib.sha256(private.read_bytes()).hexdigest(),production_BODY89_read=False,lesson89_read=False,blind_reconstruction89_read=False,mathematical_acceptance89_read=False,prior_fidelity_decision_contents_read_in_this_final_phase=False,prior_prospective_V2_header_review_known=True),ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
