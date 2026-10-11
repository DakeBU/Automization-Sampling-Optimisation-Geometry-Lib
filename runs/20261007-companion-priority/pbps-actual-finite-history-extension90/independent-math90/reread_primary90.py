from pathlib import Path
from html.parser import HTMLParser
import hashlib,json,datetime
R=Path('E:/Samplinglib');O=Path(__file__).parent
P=R/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'
b=P.read_bytes();assert hashlib.sha256(b).hexdigest()=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
class Parse(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.stack=[];self.nodes={}
 def handle_starttag(self,tag,attrs):
  a=dict(attrs);ident=a.get('id');self.stack.append((tag,ident))
  if ident and ident.startswith('A1'):self.nodes.setdefault(ident,[])
 def handle_startendtag(self,tag,attrs):pass
 def handle_endtag(self,tag):
  for i in range(len(self.stack)-1,-1,-1):
   if self.stack[i][0]==tag:self.stack=self.stack[:i];break
 def handle_data(self,data):
  for _,ident in self.stack:
   if ident in self.nodes:self.nodes[ident].append(data)
x=Parse();x.feed(b.decode('utf8'))
nodes={k:' '.join(' '.join(v).split()) for k,v in x.nodes.items()}
targets=[k for k in nodes if k in ['A1.E1','A1.E2','A1.E7'] or k.startswith('A1.SS2.p') or k in ['A1.SS1.p4','A1.SS1.p5','A1.SS1.p1']]
def put(n,v):
 with (O/n).open('x',encoding='utf8',newline='\n') as f:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
put('.private.primary90.reread-A1-A2.json',{'primary_raw':hashlib.sha256(b).hexdigest(),'spans':{k:nodes[k] for k in targets},'complete_A1_SS1':nodes.get('A1.SS1'),'complete_A1_SS2':nodes.get('A1.SS2')})
put('primary-reread90.chronology.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'primary':{'path':P.relative_to(R).as_posix(),'raw_sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)},'method':'Direct exact primary read and HTMLParser; A1 equations1,2,7, path density context and A2 Borel construction reread before any production90 BODY opened. Prior independently frozen pre90 reconstruction remains reused.','selected_exact_anchor_ids':targets,'production_BODY_read_yet':False,'no_final_decoder_or_source_verdict_read':True,'private_full_extract':'.private.primary90.reread-A1-A2.json'})
for k in targets:
 print(k, nodes[k][:1100])
print('SOURCE_REREAD_BEFORE_BODY_FROZEN')
