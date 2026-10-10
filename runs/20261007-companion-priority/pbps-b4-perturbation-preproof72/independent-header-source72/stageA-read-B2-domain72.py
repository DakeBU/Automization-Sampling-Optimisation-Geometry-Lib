import sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
import pathlib,json,hashlib,re,html,os
B=pathlib.Path('E:/Samplinglib');O=pathlib.Path(__file__).resolve().parent;raw=(B/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html').read_bytes()
def sha(b):return hashlib.sha256(b).hexdigest()
items=[]
for m in re.finditer(rb'<math\b[^>]*>.*?</math>',raw,re.S):
 attrs={k.decode():html.unescape(v.decode('utf-8')) for k,v in re.findall(rb'([A-Za-z_:][A-Za-z0-9_:.-]*)="([^"]*)"',m.group(0).split(b'>',1)[0])};mid=attrs.get('id','')
 if mid.startswith(('A2.SS2.p1.','A2.Thmtheorem1.p1.','A2.SS2.p2.','A2.SS2.p3.','A2.SS2.p4.')):
  x={'math_id':mid,'alttext':attrs.get('alttext',''),'RAW_start':m.start(),'RAW_end_exclusive':m.end(),'RAW_bytes':m.end()-m.start(),'RAW_sha256':sha(m.group(0)),'supplement_region':'B2-centered-domain'};items.append(x);(O/f'stageA.supplement.{mid}.RAW.html').write_bytes(m.group(0));(O/f'stageA.supplement.{mid}.LF.html').write_bytes(m.group(0).replace(b'\r\n',b'\n'));print(json.dumps(x,ensure_ascii=False))
paras=[]
for m in re.finditer(rb'<p\b[^>]*id="(A2\.(?:SS2\.p[1-4]|Thmtheorem1\.p1)\.[^"]+)"[^>]*>.*?</p>',raw,re.S):
 b=m.group(0);mid=m[1].decode();paras.append({'id':mid,'RAW_start':m.start(),'RAW_end_exclusive':m.end(),'RAW_bytes':len(b),'RAW_sha256':sha(b)});(O/f'stageA.supplement-paragraph.{mid}.RAW.html').write_bytes(b);(O/f'stageA.supplement-paragraph.{mid}.LF.html').write_bytes(b.replace(b'\r\n',b'\n'));s=b.decode();s=re.sub(r'<math\b[^>]*alttext="([^"]*)"[^>]*>.*?</math>',lambda q:' $'+html.unescape(q[1])+'$ ',s,flags=re.S);print('\n'+html.unescape(re.sub(r'<[^>]*>','',s)))
(O/'stageA.supplement-B2-domain.inventory72.json').write_text(json.dumps({'schema':'source72-centered-domain-exact-supplement-v1','actual_pid':os.getpid(),'entries':items,'count':len(items),'prose':paras,'scope':'Source hypotheses and SAME centered positive-root/polar interpretation only; excludes B2 sharp-energy proof/other sourceplan judgments.'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
