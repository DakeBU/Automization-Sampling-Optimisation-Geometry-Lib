from pathlib import Path
from html.parser import HTMLParser
import json,hashlib,collections
P=Path('runs/20261007-companion-priority/gaussian-laplace-domain/preproof'); raw=(P/'source-primary.raw.snapshot.html').read_bytes(); text=raw.decode('utf8');graph=json.loads((P/'source-proof-graph.independent.json').read_text(encoding='utf8'))
lines=text.splitlines(keepends=True); offsets=[0]
for ln in lines:offsets.append(offsets[-1]+len(ln))
class Inventory(HTMLParser):
 def __init__(self):super().__init__();self.stack=[];self.spans={};self.section_ids=[]
 def pos(self):l,c=self.getpos();return offsets[l-1]+c
 def handle_starttag(self,t,a):
  d=dict(a); i=d.get('id'); start=self.pos()
  if i and (i=='S4.SS1' or any(x[1]=='S4.SS1' for x in self.stack)):self.section_ids.append(i)
  if t not in ('area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'):self.stack.append((t,i,start))
  elif i:self.spans[i]=(start,start+len(self.get_starttag_text()))
 def handle_startendtag(self,t,a):
  d=dict(a);i=d.get('id');start=self.pos()
  if i:self.spans[i]=(start,start+len(self.get_starttag_text()))
 def handle_endtag(self,t):
  end=text.index('>',self.pos())+1
  for k in range(len(self.stack)-1,-1,-1):
   if self.stack[k][0]==t:
    _,i,start=self.stack[k]
    if i:self.spans[i]=(start,end)
    del self.stack[k:];break
r=Inventory();r.feed(text)
h=lambda b:hashlib.sha256(b).hexdigest()
records=[];fail=[]
for x in graph['source_inventory']:
 i=x['source_item_id'];a,b=r.spans[i];bs=len(text[:a].encode('utf8'));be=len(text[:b].encode('utf8'));frag=raw[bs:be];ok=bs==x['byte_start'] and be==x['byte_end_exclusive'] and h(frag)==x['raw_fragment_sha256']
 if not ok:fail.append(i)
 q=P/('reviewer.reviewedraw.source-item.'+i+'.html')
 with q.open('xb') as f:f.write(frag)
 records.append({'id':i,'byte_start':bs,'byte_end_exclusive':be,'raw_sha256':h(frag),'snapshot_path':str(q).replace('\\','/'),'matches_author_inventory':ok,'disposition_review':x['disposition'],'nodes':x['node_ids'],'reason_reviewed':x['coverage_or_exclusion_reason']})
ids=[x['source_item_id'] for x in graph['source_inventory']]; result={'section_ids_independently_extracted':r.section_ids,'section_count':len(r.section_ids),'missing_section_ids':list(set(r.section_ids)-set(ids)),'extra_context_ids':list(set(ids)-set(r.section_ids)),'total_count':len(ids),'duplicate_ids':[i for i,n in collections.Counter(ids).items() if n>1],'raw_span_failures':fail,'records':records}
with (P/'reviewer.inventory-raw-check.json').open('x',encoding='utf8') as f:json.dump(result,f,indent=2);f.write('\n')
for name in ['statement-proposal.json','source-proof-graph.independent.json','source-topology-review.json']:
 q=P/('reviewer.reviewedraw.'+name)
 with q.open('xb') as f:f.write((P/name).read_bytes())
print(json.dumps({k:v for k,v in result.items() if k not in ['records','section_ids_independently_extracted']},indent=2))
