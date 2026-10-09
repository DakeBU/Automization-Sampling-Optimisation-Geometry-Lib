import sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
import pathlib,re,html,json,os
O=pathlib.Path(__file__).resolve().parent;primary=(O/'primary-pbps.exactraw.snapshot.html').read_bytes()
for name,a,z in [('corrector-definition',818000,828800),('actual-rotation-B21',829000,855000),('B4-corrector-consumer',924800,934000)]:
 a=primary.rfind(b'<p ',0,a);end=primary.find(b'</p>',z);z=end+4 if end>=0 else z
 raw=primary[a:z];saved=[]
 def token(m):saved.append(html.unescape(re.search(rb'\balttext="([^"]*)"',m.group()).group(1).decode()));return (' MATHPLACEHOLDER'+str(len(saved)-1)+' ').encode()
 protected=re.sub(rb'<math\b[^>]*>.*?</math>',token,raw,flags=re.S);text=html.unescape(re.sub(rb'<[^>]*>',b' ',protected).decode())
 text=re.sub(r'MATHPLACEHOLDER(\d+)',lambda m:' ['+saved[int(m[1])]+'] ',text)
 text=re.sub(r'\s+',' ',text);assert 'MATHPLACEHOLDER' not in text
 (O/('stageA.readview-v2.'+name+'.txt')).write_text(text+'\n',encoding='utf-8',newline='\n');print(name+' RAW['+str(a)+','+str(z)+')\n'+text+'\n')
print(json.dumps({'actual_pid':os.getpid(),'v1_retired':'derived reading aid had numeric placeholder prefix collision; RAW inputs/formula reparse unaffected; v2 uses single regex replacement','current_header_seen':False}))
