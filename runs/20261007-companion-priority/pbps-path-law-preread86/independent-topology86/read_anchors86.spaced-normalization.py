from pathlib import Path
from html.parser import HTMLParser
import json,hashlib,datetime
R=Path("E:/Samplinglib");B=R/"runs/20261007-companion-priority/pbps-path-law-preread86";O=Path(__file__).parent
i=json.loads((B/"source-inventory86.json").read_text("utf-8"));wanted={x["source_id"] for x in i["anchors"]};raw=(R/i["primary"]["path"]).read_bytes()
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
  if ident in wanted:
   self.active.append(dict(id=ident,depth=len(self.stack),chunks=[]))
 def handle_data(self,d):
  if not self.math:
   for e in self.active:e['chunks'].append(d)
 def handle_endtag(self,t):
  if t not in self.stack:return
  depth=len(self.stack)-self.stack[::-1].index(t)
  for e in self.active[:]:
   if e['depth']>=depth:
    text=' '.join(' '.join(e['chunks']).split());self.records.append(dict(id=e['id'],text=text,normalized_text_sha256=hashlib.sha256(text.encode()).hexdigest()));self.active.remove(e)
  self.stack=self.stack[:depth-1]
  if t=='math':self.math=max(0,self.math-1)

p=Read();p.feed(raw.decode("utf-8"));got={x["id"]:x for x in p.records};used={s for x in i["items"] for s in x["source_ids"]}
rows=[]
for a in i["anchors"]:
 x=got.get(a["source_id"]);rows.append(dict(source_id=a["source_id"],present=x is not None,hash_matches=x is not None and x["normalized_text_sha256"]==a["normalized_anchor_sha256"],mapped_to_inventory_item=a["source_id"] in used,text=x["text"] if x else None,actual_normalized_sha256=x["normalized_text_sha256"] if x else None))
with (O/"anchor-readback86.spaced-normalization.json").open("x",encoding="utf-8",newline="\n") as f:json.dump(dict(created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),primary_raw_sha256=hashlib.sha256(raw).hexdigest(),rows=rows),f,ensure_ascii=False,indent=2);f.write("\n")
print("ROWS",len(rows),"MISMATCH",[x["source_id"] for x in rows if not x["hash_matches"]],"UNMAPPED",[x["source_id"] for x in rows if not x["mapped_to_inventory_item"]])
for x in rows:print(x["source_id"],x["text"])
