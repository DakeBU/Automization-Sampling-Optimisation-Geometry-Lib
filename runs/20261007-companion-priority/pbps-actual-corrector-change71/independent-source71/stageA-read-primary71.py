import sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
import pathlib,json,hashlib,os,re,html,html.parser
O=pathlib.Path(__file__).resolve().parent;B=pathlib.Path('E:/Samplinglib');P=B/'runs/20261007-companion-priority/pbps-corrector-change-preproof71';H=P/'independent-header-source71';S=P/'independent-source-first71'
def sha(b):return hashlib.sha256(b).hexdigest()
def write(n,x):(O/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
pins=[]
def pin(p):
 p=pathlib.Path(p);b=p.read_bytes();pins.append({'path':str(p).replace('\\','/'),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_bytes':len(b.replace(b'\r\n',b'\n')),'LF_sha256':sha(b.replace(b'\r\n',b'\n'))});return b
rb=pin(S/'source.regions.json');regions=json.loads(rb);full=pin(pathlib.Path(regions['whole_primary']['path']));assert len(full)==1482128 and sha(full)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
(O/'stageA.source.regions.exactraw.json').write_bytes(rb);(O/'stageA.source.regions.exactraw.json.LF').write_bytes(rb.replace(b'\r\n',b'\n'))
class Text(html.parser.HTMLParser):
 def __init__(self):super().__init__();self.parts=[]
 def handle_data(self,d):self.parts.append(d)
 def handle_starttag(self,t,a):
  if t in ['p','div','section','table','tr','h2','h3','h4']:self.parts.append('\n')
inventory=[]
for q in regions['regions']:
 b=pin(q['RAW']['path']);assert b==full[q['start_byte']:q['end_byte_exclusive']] and sha(b)==q['RAW']['raw_sha256'];name=q['name'];(O/('stageA.source.'+name+'.RAW.html')).write_bytes(b);(O/('stageA.source.'+name+'.LF.html')).write_bytes(b.replace(b'\r\n',b'\n'))
 def replace(m):
  token=m.group(0);tag=token[:token.index(b'>')+1];ident=re.search(rb'\bid="([^"]+)"',tag).group(1).decode();alt=re.search(rb'\balttext="([^"]*)"',tag);latex=html.unescape(alt.group(1).decode()) if alt else ''
  item={'region':name,'math_id':ident,'RAW_region_start':m.start(),'RAW_region_end_exclusive':m.end(),'RAW_full_start':q['start_byte']+m.start(),'RAW_full_end_exclusive':q['start_byte']+m.end(),'math_RAW_bytes':len(token),'math_RAW_sha256':sha(token),'formula_latex':latex};inventory.append(item)
  return html.escape('\n[MATH '+ident+'] '+latex+'\n').encode()
 aid=re.sub(rb'<math\b[^>]*>.*?</math>',replace,b,flags=re.S);t=Text();t.feed(aid.decode());view=''.join(t.parts);view=re.sub(r'\n[ \t]*\n+', '\n\n', view);(O/('stageA.primary-readview.'+name+'.txt')).write_text(view,encoding='utf-8',newline='\n');print('\nREGION',name,'RAWbytes',len(b));print(view)
assert len(inventory)==255,len(inventory)
write('stageA.primary255.reparsed-inventory.json',{'schema':'independent-source71-RAW-reparsed-math-v1','count':len(inventory),'items':inventory,'authority':'Exact RAW bytes; formulas/readviews are display aids only.'})
write('stageA.primary-input-pins.json',{'schema':'independent-source71-primary-only-input-pins-v1','count':len(pins),'LF_recipe':'ONLY CRLF byte pairs to LF; no trim or reserialization','inputs':pins,'current71_BODY_read':False,'new_publication_decoder_root_math_or_source_summary_read':False})
print('actual_PID',os.getpid(),'PASS full primary and four RAW regions255 math exact; no current71 BODY')
