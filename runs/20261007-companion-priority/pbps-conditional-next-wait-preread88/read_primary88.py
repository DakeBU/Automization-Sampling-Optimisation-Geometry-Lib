from pathlib import Path
from html import unescape
import re,json,hashlib,datetime
r=Path(__file__).parent
p=r.parent/'phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'
b=p.read_bytes();assert hashlib.sha256(b).hexdigest()=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
s=b.decode('utf8');rows=[]
for anchor in ['A1.E1','A1.E2','A1.E7','A1.SS1.SSS0.Px1.p4']:
 token='id="'+anchor+'"';start=s.index(token);end=s.find(' id="',start+len(token))
 if end<0:end=min(len(s),start+20000)
 text=s[start:end]
 formulas=[unescape(x) for x in re.findall(r'alttext="([^"]*)"',text)]
 rows.append(dict(anchor=anchor,start_character=start,end_character=end,formula_alttext=formulas,private_raw_fragment=text))
out=r/'root.primary88.read.private.json';assert not out.exists();out.write_text(json.dumps(dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),primary=str(p),primary_RAW_sha256=hashlib.sha256(b).hexdigest(),selected=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
for row in rows:print(row['anchor'],json.dumps(row['formula_alttext'],ensure_ascii=False)[:3000])
