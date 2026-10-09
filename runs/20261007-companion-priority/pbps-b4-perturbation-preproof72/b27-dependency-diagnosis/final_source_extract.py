from pathlib import Path
import hashlib, html, json, os, re, sys, traceback
ROOT=Path('E:/Samplinglib')
OWN=ROOT/'runs/20261007-companion-priority/pbps-b4-perturbation-preproof72/b27-dependency-diagnosis'
def sha(b):return hashlib.sha256(b).hexdigest()
def plain(s):
 s=re.sub(r'<math\b[^>]*alttext="([^"]*)"[^>]*>.*?</math>',lambda m:' $'+html.unescape(m[1])+'$ ',s,flags=re.S)
 return re.sub(r'\s+',' ',html.unescape(re.sub('<[^>]+>',' ',s))).strip()
def element(raw,ident,tag):
 hit=re.search(rb'<'+tag.encode()+rb'\b[^>]*\bid="'+re.escape(ident.encode())+rb'"[^>]*>',raw)
 assert hit,ident
 depth=0
 for t in re.finditer(rb'</?'+tag.encode()+rb'\b[^>]*>',raw[hit.start():]):
  depth+=-1 if t[0].startswith(b'</') else 1
  if depth==0:
   a=hit.start();z=a+t.end();return a,z,raw[a:z]
 raise AssertionError(ident)
code=0
try:
 pins=json.loads((OWN/'inputs.finite-pins.json').read_text(encoding='utf-8'))
 for p in pins['files']:assert sha((ROOT/p['path']).read_bytes())==p['raw_sha256']
 raw=(ROOT/pins['files'][0]['path']).read_bytes();text=raw.decode('utf-8')
 wanted=['S3.E4.m1','S3.E5.m1','S3.E8.m1','S3.E9.m1','S3.E11.m1','A1.E1.m1','A1.E2.m1','A1.E3.m1','A1.E9.m1','A2.SS1.p1.m1','A2.SS1.p1.m3','A2.E6.m1','A2.E7.m1','A2.Ex27.m1','A2.E27.m1']
 formulas=[]
 for m in re.finditer(rb'<math\b[^>]*\bid="([^"]+)"[^>]*>.*?</math>',raw,re.S):
  ident=m[1].decode()
  if ident in wanted:
   alt=re.search(rb'\balttext="([^"]*)"',m[0])
   formulas.append({'id':ident,'raw_range':[m.start(),m.end()],'raw_bytes':len(m[0]),'raw_sha256':sha(m[0]),'formula_tex':html.unescape(alt[1].decode())})
 blocks=[]
 for ident in ['alg1.4','S3.Thmtheorem1','S3.Thmtheorem2','A1.Thmtheorem1','A1.Thmtheorem2']:
  a,z,b=element(raw,ident,'div')
  blocks.append({'id':ident,'raw_range':[a,z],'raw_bytes':len(b),'raw_sha256':sha(b),'reading_text':plain(b.decode())})
 bib=[]
 for m in re.finditer(rb'<li\b[^>]*>.*?</li>',raw,re.S):
  if b'Davis' in m[0] and (b'ltx_bibitem' in m[0]):
   bib.append({'raw_range':[m.start(),m.end()],'raw_sha256':sha(m[0]),'reading_text':plain(m[0].decode())})
 out={'primary_raw_sha256':sha(raw),'offset_recipe':'zero-based half-open byte ranges into immutable original RAW; no character-offset substitution','formulas':formulas,'blocks':blocks,'nearby_external_citation':bib}
 (OWN/'primary.final-exact-source-anchors.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
 cell=json.loads((ROOT/pins['files'][-1]['path']).read_text(encoding='utf-8'))
 selected={k:cell[k] for k in ['cell_id','source_anchor','target_statement','parents','consumers','reuse_plan','blocked'] if k in cell}
 (OWN/'frontier.reuse-and-open-boundary.json').write_text(json.dumps(selected,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
 print(json.dumps({'actual_pid':os.getpid(),'exit_code':0,'formulas':[(m['id'],m['raw_range']) for m in formulas],'blocks':[(b['id'],b['raw_range']) for b in blocks],'external_citation':bib,'A1_statement':next(b['reading_text'] for b in blocks if b['id']=='A1.Thmtheorem1'),'frontier_reuse':selected},ensure_ascii=True,indent=2))
except BaseException:
 code=1;traceback.print_exc()
finally:
 (OWN/'final-source-extract.terminal.json').write_text(json.dumps({'actual_pid':os.getpid(),'exit_code':code,'argv':sys.argv,'background':False,'input_drift_checks':'all seven exact RAW pins'},indent=2)+'\n',encoding='utf-8',newline='\n')
sys.exit(code)
