from pathlib import Path
from html.parser import HTMLParser
import json,hashlib,datetime
root=Path('E:/Samplinglib'); out=Path(__file__).resolve().parent
primary=root/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'
raw=primary.read_bytes(); digest=hashlib.sha256(raw).hexdigest()
assert digest=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
lines=raw.splitlines(keepends=True)
ranges=[('license',257,261),('standing',349,361),('eta',613,616),('center',1486,1492),('flow-and-clock',2859,2911),('density-iteration-A7',3147,3173),('joint-Borel-A2',3325,3338)]
class Read(HTMLParser):
 def __init__(self):super().__init__();self.text=[];self.math=[]
 def handle_data(self,d):self.text.append(d)
 def handle_starttag(self,t,a):
  a=dict(a)
  if t=='math' and 'alttext' in a:self.math.append(a['alttext'])
spans=[]
for anchor,start,end in ranges:
 block=b''.join(lines[start-1:end]); p=Read();p.feed(block.decode())
 span=dict(anchor=anchor,raw_line_start=start,raw_line_end=end,byte_start_zero_based=sum(map(len,lines[:start-1])),byte_end_exclusive=sum(map(len,lines[:end])),raw_span_sha256=hashlib.sha256(block).hexdigest(),raw_html=block.decode(),readable_text=' '.join(' '.join(p.text).split()),math_alttext=p.math)
 spans.append(span)
 print(anchor,span['readable_text'])
 print('FORMULAE',json.dumps(p.math,ensure_ascii=False))
private=out/'primary89.direct-read.private.json';assert not private.exists()
private.write_text(json.dumps(dict(source=str(primary),source_raw_sha256=digest,spans=spans),ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
chron=out/'chronology.source-first89.native.jsonl';assert not chron.exists()
chron.write_text(json.dumps(dict(event='DIRECT_PRIMARY_READ_BEFORE_ANY89_CANDIDATE_OR_TOPOLOGY_COMPARISON',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),source_path=str(primary),source_raw_sha256=digest,private_extract_path=str(private),private_extract_raw_sha256=hashlib.sha256(private.read_bytes()).hexdigest(),candidate89_read=False,header89_read=False,BODY89_read=False,graph89_existed_before_this_read=False),ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
