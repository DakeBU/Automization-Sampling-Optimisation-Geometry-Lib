import sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
import pathlib,json,hashlib,re,html,os,importlib.util
B=pathlib.Path('E:/Samplinglib');O=pathlib.Path(__file__).resolve().parent;raw=(B/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html').read_bytes()
def sha(b):return hashlib.sha256(b).hexdigest()
def write(n,x):(O/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
targets=json.loads((O/'stageA.primary255.independent-inventory72.json').read_bytes())['entries']
for x in targets:
 if x['math_id']=='A2.E20.m1' or re.match(r'A2\.(Ex(2[3-9]|3[0-6])|E2[78])\.',x['math_id']):print(json.dumps(x,ensure_ascii=False))
print('\nEXACT SUPPLEMENTARY B1/B2 MATH ELEMENTS\n')
items=[]
for m in re.finditer(rb'<math\b[^>]*>.*?</math>',raw,re.S):
 opening=m.group(0).split(b'>',1)[0];attrs={k.decode():html.unescape(v.decode('utf-8')) for k,v in re.findall(rb'([A-Za-z_:][A-Za-z0-9_:.-]*)="([^"]*)"',opening)};mid=attrs.get('id','')
 if re.match(r'A2\.(E[3-7]|E1[2-6])\.',mid) or mid.startswith('A2.SS1.p1.m') or mid.startswith('A2.SS2.p6.m'):
  x={'math_id':mid,'alttext':attrs.get('alttext',''),'RAW_start':m.start(),'RAW_end_exclusive':m.end(),'RAW_bytes':m.end()-m.start(),'RAW_sha256':sha(m.group(0))};items.append(x);(O/f'stageA.supplement.{mid}.RAW.html').write_bytes(m.group(0));(O/f'stageA.supplement.{mid}.LF.html').write_bytes(m.group(0).replace(b'\r\n',b'\n'));print(json.dumps(x,ensure_ascii=False))
write('stageA.supplementary-discovery72.json',{'schema':'source72-exact-primary-supplement-discovery-v1','actual_pid':os.getpid(),'items':items,'count':len(items),'role':'Finite exact primary elements for retained operator definitions and actual K/H input adapters; final selection/classification independently frozen later. No proposed72 header read.'})
paras=[]
for mid in ['A2.SS1.p1.1','A2.SS1.p1.2','A2.SS1.p1.3','A2.SS1.p1.4','A2.SS1.p1.5','A2.SS2.p6.1']:
 m=re.search(rb'<p\b[^>]*id="'+mid.encode()+rb'"[^>]*>.*?</p>',raw,re.S)
 if m:
  b=m.group(0);paras.append({'id':mid,'RAW_start':m.start(),'RAW_end_exclusive':m.end(),'RAW_sha256':sha(b),'RAW_bytes':len(b)});(O/f'stageA.supplement-paragraph.{mid}.RAW.html').write_bytes(b);(O/f'stageA.supplement-paragraph.{mid}.LF.html').write_bytes(b.replace(b'\r\n',b'\n'))
  # display aid only, exact bytes remain authoritative
  s=b.decode();s=re.sub(r'<math\b[^>]*alttext="([^"]*)"[^>]*>.*?</math>',lambda q:' $'+html.unescape(q[1])+'$ ',s,flags=re.S);s=html.unescape(re.sub(r'<[^>]*>','',s));print('\nSUPPLEMENT PARAGRAPH '+mid+'\n'+s)
write('stageA.supplementary-prose-anchors72.json',{'schema':'source72-exact-supplement-prose-v1','items':paras,'count':len(paras)})
write('stageA.negative-inline-observer72.json',{'status':'retained_process_observer_negative','command_kind':'bounded read-only inline primary-target inventory print','tool_exit_code':1,'actual_child_PID':'not captured; no invented PID','error':'SyntaxError unmatched closing parenthesis in inline print; no source data or owned mathematical artifact modified','corrected_by':'this foreground named script','no_mathematical_failure':True})
