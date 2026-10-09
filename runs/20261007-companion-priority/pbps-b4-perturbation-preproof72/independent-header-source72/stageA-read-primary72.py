import sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
import pathlib,json,hashlib,re,html,os
from html.parser import HTMLParser
class ReadView(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.parts=[];self.inmath=False
 def handle_starttag(self,tag,attrs):
  if tag=='math':self.inmath=True;self.parts.append(' $'+dict(attrs).get('alttext','')+'$ ')
  elif tag in {'p','div','section','h1','h2','h3','h4','table','tr'} and not self.inmath:self.parts.append('\n')
 def handle_endtag(self,tag):
  if tag=='math':self.inmath=False
 def handle_data(self,data):
  if not self.inmath:self.parts.append(data)
B=pathlib.Path('E:/Samplinglib');O=pathlib.Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def write(n,x):(O/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def pin(p):
 b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');return {'path':p.relative_to(B).as_posix(),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_bytes':len(lf),'LF_sha256':sha(lf)}
primary=B/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html';raw=primary.read_bytes();assert len(raw)==1482128 and sha(raw)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
regions=[('global-assumptions',46982,73369,'e176d6854e56dc575fc8e37556fea086d4bb728f993d2bc23fe5343a5da0766e'),('corrector-sharp-energy-and-consumers-B3',801184,888702,'f5c4686bddcd3dedb2bff2ed6c4399fdb442e9657afda401eb35b391485b9177'),('real-L2-spectral-conventions-D1',1348892,1372364,'b6951c6a9599e243ab960687213a83d322089a2814fb5532eaf1eb656e5e44e9'),('corrector-change-B4-consumer-proof',888702,970152,'860c1410bc5980ac1d736ebbc5952bd1874c23e8c30c11572f9618f816d2d3bc')]
inventory=[];rr=[]
for name,a,z,digest in regions:
 b=raw[a:z];assert sha(b)==digest
 (O/f'stageA.source.{name}.RAW.html').write_bytes(b);(O/f'stageA.source.{name}.LF.html').write_bytes(b.replace(b'\r\n',b'\n'))
 reader=ReadView();reader.feed(b.decode('utf-8'));view=''.join(reader.parts)
 (O/f'stageA.primary-readview.{name}.txt').write_text(view+'\n',encoding='utf-8',newline='\n')
 count=0
 for m in re.finditer(rb'<math\b[^>]*>.*?</math>',b,re.S):
  opening=m.group(0).split(b'>',1)[0]
  attrs={k.decode():html.unescape(v.decode('utf-8')) for k,v in re.findall(rb'([A-Za-z_:][A-Za-z0-9_:.-]*)="([^"]*)"',opening)}
  inventory.append({'ordinal':len(inventory)+1,'region':name,'math_id':attrs.get('id'),'alttext':attrs.get('alttext',''),'RAW_start':a+m.start(),'RAW_end_exclusive':a+m.end(),'region_RAW_start':m.start(),'region_RAW_end_exclusive':m.end(),'RAW_bytes':m.end()-m.start(),'RAW_sha256':sha(m.group(0))});count+=1
 rr.append({'name':name,'RAW_start':a,'RAW_end_exclusive':z,'RAW_bytes':len(b),'RAW_sha256':sha(b),'math_count':count,'snapshot':f'stageA.source.{name}.RAW.html','LF_snapshot':f'stageA.source.{name}.LF.html'})
assert len(inventory)==255 and len({x['math_id'] for x in inventory})==255
write('stageA.primary255.independent-inventory72.json',{'schema':'source72-independent-RAW-math-inventory-v1','primary':pin(primary),'regions':rr,'count':len(inventory),'entries':inventory,'derivation':'Independent regex on exact RAW math elements; alttext is decoded display aid, exact RAW offsets/hashes authoritative.'})
write('stageA.primary-input-manifest72.json',{'schema':'source72-primary-only-input-manifest-v1','actual_pid':os.getpid(),'primary':pin(primary),'regions':rr,'LF_recipe':'ONLY byte CRLF to LF; no trim or other normalization','future72_header_proposal_verdict_BODY_read':False})
for name in ['corrector-sharp-energy-and-consumers-B3','corrector-change-B4-consumer-proof']:
 print('\nPRIMARY REGION '+name+'\n'+(O/f'stageA.primary-readview.{name}.txt').read_text(encoding='utf-8'))
print('\nTARGET B20/B4 MATH IDS AND EXACT ALT TEXT\n')
for x in inventory:
 if x['math_id']=='A2.E20.m1' or x['region']=='corrector-change-B4-consumer-proof':print(json.dumps(x,ensure_ascii=False))
print(json.dumps({'actual_pid':os.getpid(),'status':'PRIMARY_ONLY_4REGIONS_255_REPARSED','counts':rr},ensure_ascii=False,indent=2))
