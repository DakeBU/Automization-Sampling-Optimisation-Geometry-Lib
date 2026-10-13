import os,json,hashlib,datetime,re
from pathlib import Path
from html.parser import HTMLParser
O=Path('E:/Samplinglib/runs/20261007-companion-priority/pbps-polar65/independent-source65');S=Path('E:/Samplinglib/runs/20261007-companion-priority/pbps-polar-preproof65/independent-primary65');P=Path('E:/Samplinglib/runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html')
def sha(b):return hashlib.sha256(b).hexdigest()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def write(n,v):(O/n).write_bytes((json.dumps(v,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode())
write('lease.open.json',{'schema':'source65-owned-lease-v1','status':'OPEN','owner':'/root/independent_source64','owned_root':O.as_posix(),'opened_utc':now(),'actual_create_pid':os.getpid(),'scope':'This NEW owned folder only; no closed/canonical/Git/ledger/Lean mutation','candidate_seen':False})
start=now();pins={'source-proof-graph.json':'d2df300e034f799bc30dba724e4595682310f76c567e83316603a3a372e7f5f8','source-coverage-inventory.json':'605a1e7e3a4d583198d147a5207316cb62febb66ca0b9651e6372595728ffc45','source-inputs.json':'9529d76492ab43ea2d5ecae02fc6e5881b7cd57256d16ea88d4e0843960e62cb','residual-next-header.json':'89c0e89b915577ae94b52c781356fdb130533438c4bf4d53688d2ee70751986f','lease.final.json':'484c7e4eb3ce900d957de8a35590399d2593158344f7d5b2565901e53232abbf'};refs=[]
for n,h in pins.items():
 b=(S/n).read_bytes();assert sha(b)==h;(O/('primary-first.'+n)).write_bytes(b);refs.append({'name':n,'source_path':(S/n).as_posix(),'snapshot':'primary-first.'+n,'RAW_sha256':h,'RAW_bytes':len(b),'LF_sha256':sha(b.replace(b'\r\n',b'\n').replace(b'\r',b'\n'))})
i=json.loads((S/'source-inputs.json').read_text(encoding='utf-8'));c=json.loads((S/'source-coverage-inventory.json').read_text(encoding='utf-8'));raw=P.read_bytes();assert sha(raw)==i['primary_raw_sha256']=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760';assert c['math_count']==len(c['math_items'])==280 and c['missing_alttext_count']==c['annotation_mismatch_count']==0
class Render(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.out=[];self.depth=0
 def handle_starttag(self,t,a):
  if t=='math':self.depth+=1;self.out.append(dict(a).get('alttext','MISSING'));return
  if not self.depth and t in ['p','div','table','li','h1','h2','h3','h4']:self.out.append('\n')
 def handle_endtag(self,t):
  if t=='math':self.depth-=1;return
  if not self.depth and t in ['p','div','table','li','h1','h2','h3','h4']:self.out.append('\n')
 def handle_data(self,s):
  if not self.depth:self.out.append(s)
for x in i['regions']:
 a,b=x['source_raw_byte_range'];blob=raw[a:b];assert blob==(S/(x['name']+'.raw.html')).read_bytes() and sha(blob)==x['raw_sha256'];lf=blob.replace(b'\r\n',b'\n').replace(b'\r',b'\n');(O/(x['name']+'.raw.html')).write_bytes(blob);(O/(x['name']+'.LF.html')).write_bytes(lf);r=Render();r.feed(blob.decode());txt=re.sub(r'\n\s*\n+','\n\n',''.join(r.out)).strip()+'\n';(O/(x['name']+'.rendered.txt')).write_bytes(txt.encode());refs.append({'name':x['name'],'source_path':P.as_posix(),'snapshot':x['name']+'.raw.html','LF_snapshot':x['name']+'.LF.html','source_RAW_byte_range':[a,b],'RAW_sha256':sha(blob),'LF_sha256':sha(lf),'RAW_bytes':len(blob),'math_count':x['math_count']});print('\nPRIMARY ONLY '+x['name']+' '+str([a,b])+'\n'+txt)
write('primary-first-seal.json',{'schema':'source65-primary-first-seal-v1','source_read_start_utc':start,'source_read_end_utc':now(),'candidate_seen_before_this_seal':False,'source_independent_of_Lean_topology':True,'source_RAW_sha256':sha(raw),'frozen_primary65_graph_RAW_sha256':pins['source-proof-graph.json'],'frozen_primary65_inventory_RAW_sha256':pins['source-coverage-inventory.json'],'source_math_items':280,'missing_alttext':0,'annotation_mismatch':0,'source_bindings':refs,'reused_before_any_future65_candidate':'Closed primary65 graph/inventory were frozen before header65; current reread precedes all current source65 candidate/decoder/proof inputs.'});print('\nSOURCE GRAPH\n'+(S/'source-proof-graph.json').read_text(encoding='utf-8'))
