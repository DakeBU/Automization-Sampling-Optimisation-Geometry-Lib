import sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
import pathlib,json,hashlib,re,html,os
B=pathlib.Path('E:/Samplinglib');O=pathlib.Path(__file__).resolve().parent;raw=(B/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html').read_bytes()
def sha(b):return hashlib.sha256(b).hexdigest()
def write(n,x):(O/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
a=raw.index(b'<section id="A2.SS1"');z=raw.index(b'<section id="A2.SS2"',a);b=raw[a:z]
(O/'stageA.supplement-B1-framework.RAW.html').write_bytes(b);(O/'stageA.supplement-B1-framework.LF.html').write_bytes(b.replace(b'\r\n',b'\n'))
entries=[]
for m in re.finditer(rb'<math\b[^>]*>.*?</math>',b,re.S):
 attrs={k.decode():html.unescape(v.decode('utf-8')) for k,v in re.findall(rb'([A-Za-z_:][A-Za-z0-9_:.-]*)="([^"]*)"',m.group(0).split(b'>',1)[0])};entries.append({'math_id':attrs['id'],'alttext':attrs.get('alttext',''),'RAW_start':a+m.start(),'RAW_end_exclusive':a+m.end(),'RAW_bytes':m.end()-m.start(),'RAW_sha256':sha(m.group(0)),'supplement_region':'B1-framework'})
write('stageA.supplement-B1-framework.inventory72.json',{'schema':'source72-bounded-B1-supplement-inventory-v1','actual_pid':os.getpid(),'RAW_start':a,'RAW_end_exclusive':z,'RAW_bytes':len(b),'RAW_sha256':sha(b),'count':len(entries),'entries':entries,'reason':'Exact original Markov kernel, conditional expectation, half-turn H, block compression and K=B7 adapters are necessary to prevent arbitrary perturbation vectors from acquiring actual-update semantics.'})
s=b.decode();s=re.sub(r'<math\b[^>]*alttext="([^"]*)"[^>]*>.*?</math>',lambda q:' $'+html.unescape(q[1])+'$ ',s,flags=re.S);s=html.unescape(re.sub(r'<[^>]*>','',s))
(O/'stageA.supplement-B1-framework.readview.txt').write_text(s,encoding='utf-8',newline='\n');print(s)
write('stageA.negative-PowerShell-parser-observer72.json',{'status':'retained_process_observer_negative','tool_exit_code':1,'actual_child_PID':'No child executed: PowerShell parse failure','error':'Complex inline Python regex quoting triggered PowerShell ParserError; replaced by this named foreground helper.','source_or_candidate_changed':False,'source_read_scope':'Fixed primary only; no72candidate/header/sourceplan opened'})
print(json.dumps({'actual_pid':os.getpid(),'count':len(entries),'range':[a,z],'RAW_sha256':sha(b)},indent=2))
