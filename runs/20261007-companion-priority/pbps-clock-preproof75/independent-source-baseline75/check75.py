from pathlib import Path
from html.parser import HTMLParser
from collections import Counter
import json,hashlib,re,os,sys,base64
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path('E:/Samplinglib');OWN=Path(__file__).resolve().parent
def load(p):return json.loads(p.read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()
def canonical(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def verify_pin(e):
 b=(ROOT/e['path']).read_bytes();assert len(b)==e['RAW_bytes'] and sha(b)==e['RAW_sha256'] and sha(b.replace(b'\r\n',b'\n'))==e['LF_sha256'],e['path']
class Visible(HTMLParser):
 def __init__(self,s,lo):
  super().__init__(convert_charrefs=False);self.s=s;self.lo=lo;self.stack=[];self.data=[];self.offsets=[0]
  for m in re.finditer('\n',s):self.offsets.append(m.end())
  self.feed(s)
 def handle_starttag(self,t,a):
  if t not in ('br','img','meta','link','hr','wbr','input','source','col'):self.stack.append(t)
 def handle_endtag(self,t):
  for i in range(len(self.stack)-1,-1,-1):
   if self.stack[i]==t:self.stack=self.stack[:i];return
 def handle_data(self,d):
  if not d.strip() or any(t in self.stack for t in ('math','script','style')):return
  l,c=self.getpos();o=self.offsets[l-1]+c;b=self.lo+len(self.s[:o].encode());self.data.append((b,b+len(d.encode()),d.strip()))
def main():
 inv=load(OWN/'source-coverage-inventory75.json');graph=load(OWN/'source-proof-graph75.json');ex=load(OWN/'source-first.expectations75.json');im=load(OWN/'inputs.manifest75.json')
 assert len(inv['items'])==137 and inv['classifications']=={'NODE':77,'EXCLUDED':60} and inv['math_count']==89 and inv['block_count']==48
 primary=ROOT/im['inputs'][0]['path'];raw=primary.read_bytes();assert sha(raw)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
 for e in im['inputs']:
  verify_pin(e)
  if 'snapshot'in e:
   verify_pin(e['snapshot']);assert (ROOT/e['path']).read_bytes()==(ROOT/e['snapshot']['path']).read_bytes()
 for r in inv['regions']:
  verify_pin(r['RAW']);a,b=r['RAW_range'];assert raw[a:b]==(ROOT/r['RAW']['path']).read_bytes()
 for r in inv['items']:
  a,b=r['RAW_range'];chunk=raw[a:b];assert len(chunk)==r['RAW_bytes'] and sha(chunk)==r['RAW_sha256'] and sha(chunk.replace(b'\r\n',b'\n'))==r['LF_sha256']
  assert r['classification'] in ('NODE','EXCLUDED') and r['reason']
 nodes={x['id']:x for x in graph['nodes']};assert len(nodes)==32 and len(graph['edges'])==67
 incoming=Counter();children={x:[]for x in nodes}
 for e in graph['edges']:
  assert e['producer'] in nodes and e['consumer'] in nodes;incoming[e['consumer']]+=1;children[e['producer']].append(e['consumer'])
 todo=[x for x in nodes if not incoming[x]];seen=[]
 while todo:
  x=todo.pop();seen.append(x)
  for y in children[x]:
   incoming[y]-=1
   if not incoming[y]:todo.append(y)
 assert len(seen)==32,'source graph must be acyclic'
 for x in nodes.values():
  for a in x['source_anchors']:
   lo,hi=a['RAW_range'];assert sha(raw[lo:hi])==a['RAW_sha256'];assert ('id="'+a['id']+'"').encode() in raw[lo:hi]
 assert len(ex['original_callers'])==6 and len(ex['future_header_obligations'])==32 and len(ex['source_evidence_vs_completion']['internal_bridge_nodes'])==13 and ex['source_before_75_header_body']
 parts=load(OWN/'source-RAW-partition75.json')['partitions'];uncovered=[]
 for part in parts:
  a,b=part['RAW_range'];cursor=a
  for q in part['partition']:
   lo,hi=q['RAW_range'];assert lo==cursor and hi>lo and sha(raw[lo:hi])==q['RAW_sha256'];cursor=hi
  assert cursor==b
  visible=Visible(raw[a:b].decode(),a)
  rows=[r for r in inv['items'] if r['region_id']==part['region_id']]
  for lo,hi,t in visible.data:
   if not any(r['RAW_range'][0]<=lo and r['RAW_range'][1]>=hi for r in rows):uncovered.append({'region_id':part['region_id'],'RAW_range':[lo,hi],'text':t})
 allowed={'(3.4)','(3.5)','(3.6)','(3.7)','(3.8)','(3.9)','(A.1)','(A.2)','(A.3)','(i)','(ii)','(iii)','(1.1)'}
 assert all(q['text']in allowed for q in uncovered),uncovered
 if (OWN/'lease.final.json').exists():
  lease=load(OWN/'lease.final.json');assert lease['status']=='CLOSED_LAST'
  actual=sorted(x.relative_to(ROOT).as_posix()for x in OWN.rglob('*')if x.is_file())
  assert len(actual)==lease['owned_count'] and set(actual)==set(e['path']for e in lease['all_owned_outputs_except_only_self'])|{(OWN/'lease.final.json').relative_to(ROOT).as_posix()}
  for e in lease['all_owned_outputs_except_only_self']:verify_pin(e)
  manifest=load(OWN/'whole-owned.manifest75.json');verify_pin(lease['whole_owned_manifest'])
  for e in manifest['files']:verify_pin(e)
  run=load(OWN/'run75.json');given=run.pop('run_sha256');assert sha(canonical(run))==given==lease['whole_logical_run_sha256']
  named=load(OWN/'complete-named-RAW-payload75.json');verify_pin(lease['complete_named_RAW_payload'])
  for e in named['named_payloads']:
   b=base64.b64decode(e['complete_RAW_base64'],validate=True);assert b==(ROOT/e['pin']['path']).read_bytes();verify_pin(e['pin'])
  assert all(x.stat().st_mtime_ns<=(OWN/'lease.final.json').stat().st_mtime_ns for x in OWN.rglob('*')if x.is_file())
  status={'status':'POSTCLOSE_READ_ONLY_PASS','owned_files':len(actual),'lease_members':len(lease['all_owned_outputs_except_only_self']),'manifest_members':len(manifest['files']),'whole_logical_run_sha256':given,'lease_RAW_sha256':sha((OWN/'lease.final.json').read_bytes()),'postclose_owned_writes':0}
 else:status={'status':'OPEN_PRE_CLOSE_VERIFICATION_PASS'}
 print(json.dumps({'actual_PID':os.getpid(),'actual_EXIT':0,**status,'input_count':len(im['inputs']),'source_items':137,'NODE':77,'EXCLUDED':60,'source_graph':[32,67],'future_obligations':32,'internal_bridges':13,'structural_visible_labels_outside_semantic_rows':uncovered,'candidate_header_or_BODY_read':False},ensure_ascii=False,sort_keys=True))
if __name__=='__main__':main()
