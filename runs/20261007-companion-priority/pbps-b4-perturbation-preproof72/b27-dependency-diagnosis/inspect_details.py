from pathlib import Path
import hashlib, html, json, os, re, sys, traceback
ROOT=Path('E:/Samplinglib')
OWN=ROOT/'runs/20261007-companion-priority/pbps-b4-perturbation-preproof72/b27-dependency-diagnosis'
def sha(b):return hashlib.sha256(b).hexdigest()
def plain(s):
 s=re.sub(r'<math\b[^>]*alttext="([^"]*)"[^>]*>.*?</math>',lambda m:' $'+html.unescape(m[1])+'$ ',s,flags=re.S)
 return re.sub(r'\s+',' ',html.unescape(re.sub('<[^>]+>',' ',s))).strip()
code=0
try:
 pins=json.loads((OWN/'inputs.finite-pins.json').read_text(encoding='utf-8'))
 for p in pins['files']:
  assert sha((ROOT/p['path']).read_bytes())==p['raw_sha256']
 raw=(ROOT/pins['files'][0]['path']).read_bytes()
 text=raw.decode('utf-8')
 views=[]
 for label,a,z in [('algorithm-and-proposition32',195000,292500),('appendix-A-construction-and-joint-operator',545000,670000),('B1-actual-kernel-and-block',708167,758371),('B4-actual-residual-and-B27',891000,907500)]:
  views.append({'label':label,'raw_range':[a,z],'text':plain(raw[a:z].decode('utf-8',errors='replace'))})
 (OWN/'primary.bounded-readviews.json').write_text(json.dumps(views,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
 items=[]
 for m in re.finditer(r'<math\b(?P<attrs>[^>]*)>.*?</math>',text,re.S):
  attrs=m['attrs']; ident=re.search(r'\bid="([^"]+)"',attrs); alt=re.search(r'\balttext="([^"]*)"',attrs)
  if ident and alt and (ident[1] in ['A1.E9.m1','A2.E6.m1','A2.E7.m1','A2.Ex27.m1','A2.E27.m1']):
   a=len(text[:m.start()].encode()); b=m[0].encode()
   items.append({'id':ident[1],'raw_range':[a,a+len(b)],'raw_bytes':len(b),'raw_sha256':sha(b),'formula_tex':html.unescape(alt[1])})
 tags=[]
 for m in re.finditer(r'<(?:section|div|figure)\b[^>]*id="([^"]+)"[^>]*>',text):
  a=len(text[:m.start()].encode())
  if 195000<=a<=292500 or 545000<=a<=670000:
   if any(t in m[0] for t in ['ltx_theorem','ltx_proof','ltx_figure','ltx_listing','ltx_section','ltx_subsection']):tags.append({'id':m[1],'raw_offset':a,'tag':m[0]})
 (OWN/'primary.exact-anchors.json').write_text(json.dumps({'fixed_primary_sha256':sha(raw),'math':items,'structure_tags':tags},ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
 cell=json.loads((ROOT/pins['files'][-1]['path']).read_text(encoding='utf-8'))
 selected={k:v for k,v in cell.items() if k in ['cell_id','schema_version','title','source_detail_audit','parent_cells','dag_parents','target_declarations','proof_obligations','remaining_boundary','remaining_truth_boundary','source_anchors','source_ids','current_status','status']}
 (OWN/'frontier.bounded-reuse-fields.json').write_text(json.dumps(selected,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
 print(json.dumps({'actual_pid':os.getpid(),'exit_code':0,'views':[(v['label'],len(v['text'])) for v in views],'source_math_ids':[i['id'] for i in items],'source_structure':tags,'frontier_keys':list(cell),'selected_frontier_keys':list(selected)},ensure_ascii=True,indent=2))
except BaseException:
 code=1;traceback.print_exc()
finally:
 (OWN/'inspect-details.terminal.json').write_text(json.dumps({'actual_pid':os.getpid(),'exit_code':code,'argv':sys.argv,'background':False,'input_drift_checks':'all seven exact RAW pins'},indent=2)+'\n',encoding='utf-8',newline='\n')
sys.exit(code)
