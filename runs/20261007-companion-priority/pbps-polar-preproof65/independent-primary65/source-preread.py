import os,json,hashlib,re,html,datetime
from pathlib import Path
from html.parser import HTMLParser
O=Path('E:/Samplinglib/runs/20261007-companion-priority/pbps-polar-preproof65/independent-primary65')
P=Path('E:/Samplinglib/runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html')
H='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def write(n,v):
 b=(json.dumps(v,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode();(O/n).write_bytes(b);return sha(b)
if not (O/'lease.open.json').exists():write('lease.open.json',{'schema':'primary65-owned-lease-v1','status':'OPEN','owner':'/root/independent_source64','owned_root':O.as_posix(),'opened_utc':now(),'create_pid':os.getpid(),'write_scope':'this new owned folder only','forbidden_scopes':['independent-source64','independent-auxiliary-overlay64','canonical','Git','ledger'],'future65_candidate_inputs_seen':False})
start=now();raw=P.read_bytes();assert sha(raw)==H
# Exact section starts and next section starts delimit literal byte regions.
def pos(s):
 k=raw.find(s.encode());assert k>=0,s;return k
spec=[('source-assumptions','<section id="S1"','<section id="S2"'),('joint-law-step','<section id="S2.SS2"','<section id="S2.SS3"'),('operator-blocks-B1','<section id="A2.SS1"','<section id="A2.SS2"'),('root-polar-B2','<section id="A2.SS2"','<section id="A2.SS3"'),('corrector-first-consumer','<section id="A2.SS3"','<div id="A2.SS3.p5"'),('spectral-background-D1','<section id="A4.SS1"','<section id="A4.SS2"')]
# Read-only source parsing records every literal math tag; annotations are evidence only.
class Render(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.out=[];self.depth=0
 def handle_starttag(self,t,a):
  if t=='math':self.depth+=1;self.out.append(dict(a).get('alttext','[MISSING ALTTEXT]'));return
  if self.depth:return
  if t in ['p','h1','h2','h3','h4','div','table','tr','li']:self.out.append('\n')
 def handle_endtag(self,t):
  if t=='math':self.depth-=1;return
  if not self.depth and t in ['p','h1','h2','h3','h4','div','table','tr','li']:self.out.append('\n')
 def handle_data(self,s):
  if not self.depth:self.out.append(s)
regions=[];maths=[];payload=bytearray();mapping=[]
for name,a,b in spec:
 st=pos(a);en=pos(b);blob=raw[st:en];txt=blob.decode('utf-8');readstart=now();r=Render();r.feed(txt);rendered=re.sub(r'\n\s*\n+','\n\n',''.join(r.out)).strip()+'\n';(O/(name+'.raw.html')).write_bytes(blob);lf=blob.replace(b'\r\n',b'\n').replace(b'\r',b'\n');(O/(name+'.lf.html')).write_bytes(lf);(O/(name+'.rendered.txt')).write_bytes(rendered.encode('utf-8'))
 items=[]
 for m in re.finditer(rb'<math\b[^>]*>.*?</math>',blob,re.S):
  full=m.group();op=full[:full.find(b'>')+1].decode();alt=re.search(r'\balttext="([^"]*)"',op);annotation=re.search(rb'<annotation\b[^>]*encoding="application/x-tex"[^>]*>(.*?)</annotation>',full,re.S)
  av=html.unescape(alt.group(1)) if alt else None;ann=html.unescape(annotation.group(1).decode()) if annotation else None
  prev=blob[:m.start()];ids=list(re.finditer(rb'\bid="([^"]+)"',prev));near=ids[-1].group(1).decode() if ids else None
  item={'index':len(maths),'region':name,'source_nearest_id':near,'raw_byte_start':st+m.start(),'raw_byte_end_exclusive':st+m.end(),'raw_math_sha256':sha(full),'alttext':av,'annotation_tex':ann,'alttext_present':bool(alt),'annotation_present':bool(annotation),'annotation_exactly_matches_alttext':None if not annotation or not alt else ann==av,'classification':'source-global-hypotheses' if name in ['source-assumptions','joint-law-step'] else 'spectral-convention' if name=='spectral-background-D1' else 'next-corrector-consumer-only' if name=='corrector-first-consumer' else 'operator-block-prerequisite' if name=='operator-blocks-B1' else 'root-to-polar-and-downstream-boundary'}
  maths.append(item);items.append(item['index'])
 offset=len(payload);head=json.dumps({'name':name,'source_raw_range':[st,en],'bytes':len(blob),'sha256':sha(blob)},sort_keys=True,separators=(',',':')).encode()+b'\n';payload.extend(head);bodypos=len(payload);payload.extend(blob);payload.extend(b'\n')
 mapping.append({'name':name,'header_byte_start':offset,'body_byte_start':bodypos,'body_byte_end_exclusive':bodypos+len(blob),'source_byte_range':[st,en],'raw_sha256':sha(blob),'lf_sha256':sha(lf),'raw_snapshot':name+'.raw.html','lf_snapshot':name+'.lf.html','rendered_snapshot':name+'.rendered.txt'})
 regions.append({'name':name,'source_raw_byte_range':[st,en],'raw_bytes':len(blob),'raw_sha256':sha(blob),'lf_bytes':len(lf),'lf_sha256':sha(lf),'math_indices':items,'math_count':len(items),'read_start_utc':readstart,'read_end_utc':now()})
 print('\nSOURCE REGION '+name+' '+str([st,en])+'\n'+rendered[:(15000 if name in ['operator-blocks-B1','root-polar-B2','corrector-first-consumer'] else 7000)])
(O/'complete-source-inputs.named.raw.payload').write_bytes(payload)
write('source-inputs.json',{'schema':'primary65-source-inputs-v1','primary_path':P.as_posix(),'primary_raw_sha256':H,'primary_raw_bytes':len(raw),'source_only_read_start_utc':start,'source_only_read_end_utc':now(),'prior_read_record':{'tool_chunk':'7d93e8','exit_code':0,'utc':'2026-10-09T05:12:34.276162+00:00','regions':['A2.SS1','A2.SS2','A2.SS3'],'future65_inputs_seen':False},'regions':regions,'named_raw_input_payload':{'filename':'complete-source-inputs.named.raw.payload','bytes':len(payload),'sha256':sha(payload),'format':'each named JSON header LF then exact raw region bytes LF','segment_map':mapping},'source_primary_reuse':{'original_primary_first_source_proof_graph_sha256':'f4e62204a025c69b97a7baaeee685f084877ca03d76db6a336e9f50b5865e7e8','original_primary_first_source_coverage_inventory_sha256':'141c1e94552951795cc58b97538797bd31ea69c1935f3c9b91c484862c14467e','original_primary_first_stage_seal_sha256':'e6d3ca80b214839da7b450919e1a3e75de772140118e5bf2d34f8e0fac5f3a81','reuse_kind':'identity and already-read source-only topology; no closed folder opened; target-specific graph reconstructed from exact primary again','timing':'Original primary-first stage precedes all64 candidate exposure. New target reread times above.'}})
write('source-coverage-inventory.json',{'schema':'primary65-literal-source-coverage-v1','regions':regions,'math_count':len(maths),'missing_alttext_count':sum(not x['alttext_present'] for x in maths),'missing_annotation_count':sum(not x['annotation_present'] for x in maths),'annotation_mismatch_count':sum(x['annotation_exactly_matches_alttext'] is False for x in maths),'math_items':maths,'coverage_scope':'All literal math tags in six selected source regions. First corrector consumer prefix only; later B3 equations outside prefix excluded from target.'})
