import os,sys,json,hashlib,datetime,re,subprocess,traceback,html
from html.parser import HTMLParser
from pathlib import Path
ROOT=Path('E:/Samplinglib');O=ROOT/'runs/20261007-companion-priority/pbps-corrector-change-preproof71/independent-source-first71';PRI=ROOT/'runs/20261007-companion-priority/pbps-reflection-rotation-preproof69/independent-primary69';PRIMARY=ROOT/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html';ACTOR='/root/exact_science63'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):return json.loads(Path(p).read_bytes())
def get(n):return read(O/n)
def save(n,v):
 assert not(O/'lease.final.json').exists();p=O/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((json.dumps(v,sort_keys=True,ensure_ascii=False,indent=2)+'\n').encode())
def pin(p):
 p=Path(p);b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');return dict(path=p.as_posix(),raw_bytes=len(b),raw_sha256=sha(b),lf_bytes=len(lf),lf_sha256=sha(lf))
def checkpin(q):assert pin(q['path'])==q,('RAW/LF mismatch',q['path'])
def logical(d):return sha(json.dumps({k:v for k,v in d.items() if k!='run_sha256'},sort_keys=True,ensure_ascii=False,separators=(',',':')).encode())
def stable():
 for q in get('inputs.manifest.json')['inputs']:checkpin(q['original'])
class Readable(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.math=False;self.parts=[]
 def handle_starttag(self,tag,attrs):
  if tag=='math':self.math=True;self.parts.append(' [ '+dict(attrs).get('alttext','')+' ] ')
  elif not self.math and tag in ['p','div','section','h2','h3','h4','table','tr']:self.parts.append('\n')
 def handle_endtag(self,tag):
  if tag=='math':self.math=False
 def handle_data(self,data):
  if not self.math:self.parts.append(data)
def extract():
 O.mkdir(parents=True,exist_ok=True);save('lease.open.json',dict(status='OPEN',actor=ACTOR,actual_PID=os.getpid(),utc=now(),owned_scope=O.as_posix(),scope='Independent source-first P15/P16/P17/B4 extraction; no proof search, SAU, canonical/Git/ledger writes.'))
 save('visibility-declaration.json',dict(actor=ACTOR,prior_visibility='Previously reviewed70 proposed expanded header as independent mathematics/type reviewer. This extraction is NOT source-blind or a new anti-anchored final source verdict.',current_order='Fixed primary RAW and independently frozen pre69 source DAG first; seal source expectations BEFORE any current70 sealed header/interface read.',no70BODY_read=True,no69_native_review_copy_or_reaudit=True,Lean_proof_search=False,VERIFIED=False))
 regionmap=read(PRI/'source-input-regions.json');graph=read(PRI/'source-proof-graph.json');raw=PRIMARY.read_bytes();assert sha(raw)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'==regionmap['whole_primary']['RAW_sha256'];assert len(raw)==1482128;assert len(graph['nodes'])==22 and len(graph['edges'])==49 and pin(PRI/'source-proof-graph.json')['raw_sha256']=='1b464d9452b722abbaa6e274872366d8771780f96bc263dfeeb86322c2e88b8c'
 inputs=[]
 for i,p in enumerate([PRIMARY,PRI/'source-input-regions.json',PRI/'source-proof-graph.json']):
  row=dict(original=pin(p),authority='Fixed2609.06905v1 exact primary or pre69 independent22-node49-edge source-only graph. No theorem proof certificate.')
  if p!=PRIMARY:
   for kind,b in [('RAW',p.read_bytes()),('LF',p.read_bytes().replace(b'\r\n',b'\n'))]:
    q=O/f'inputs/{i:02}.{kind}.snapshot';q.parent.mkdir(exist_ok=True);q.write_bytes(b);row[kind+'_snapshot']=pin(q)
  else:row['storage']='Whole immutable source pinned without duplicate; bounded exact RAW regions stored below.'
  inputs.append(row)
 save('inputs.manifest.json',dict(input_count=len(inputs),inputs=inputs,LF_recipe='Replace ONLY CRLF with LF; preserve bare CR/encoding/all other bytes. RAW authoritative.',finite_historical_maps=[],source_only=True,no_69_native_payload_consumed=True))
 selected=['global-assumptions','corrector-sharp-energy-and-consumers-B3','real-L2-spectral-conventions-D1','corrector-change-B4-consumer-proof'];regions=[];math=[]
 for n in selected:
  q=next(x for x in regionmap['regions'] if x['name']==n);a,b=q['source_RAW_range_end_exclusive'];part=raw[a:b];assert sha(part)==q['RAW_sha256'] and len(part)==q['RAW_bytes'];rp=O/f'source/{n}.RAW.html';lp=O/f'source/{n}.LF.html';rp.parent.mkdir(exist_ok=True);rp.write_bytes(part);lp.write_bytes(part.replace(b'\r\n',b'\n'));regions.append(dict(name=n,start_byte=a,end_byte_exclusive=b,RAW=pin(rp),LF=pin(lp),whole_primary_RAW_sha256=sha(raw)))
  for match in re.finditer(rb'<math\b[^>]*>.*?</math>',part,re.S):
   block=match.group();opening=block[:block.index(b'>')+1];ident=re.search(rb'\bid="([^"]+)"',opening).group(1).decode();alt=re.search(rb'\balttext="([^"]*)"',opening);assert ident;math.append(dict(id=ident,region=n,start_byte=a+match.start(),end_byte_exclusive=a+match.end(),RAW_bytes=len(block),RAW_sha256=sha(block),alttext=html.unescape(alt.group(1).decode()) if alt else ''))
  parser=Readable();parser.feed(part.decode());plain=''.join(parser.parts);(O/f'source/{n}.readable.txt').write_bytes(plain.encode())
 save('source.regions.json',dict(whole_primary=pin(PRIMARY),source_id='arXiv:2609.06905v1',region_count=len(regions),regions=regions,RAW_offsets_end_exclusive=True,rendered_readable_text='Derived display aid only; exact source authority is RAW bytes, never soup reserialization.'))
 save('source.math.inventory.json',dict(math_count=len(math),items=math,coverage_boundary='Only four named bounded primary regions. Every selected math element is inventoried; no whole-paper coverage claim.'))
 print(json.dumps(dict(status='EXTRACTED_FIXED_PRIMARY',actual_PID=os.getpid(),regions=len(regions),math_items=len(math))))
if __name__=='__main__':
 try:globals()[sys.argv[1]]()
 except Exception as e:
  if not(O/'lease.final.json').exists():save((sys.argv[2] if len(sys.argv)>2 else sys.argv[1])+'.failure.json',dict(actual_PID=os.getpid(),utc=now(),error=repr(e),traceback=traceback.format_exc()))
  raise
