import sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
import pathlib,json,re,html,hashlib,os,datetime
O=pathlib.Path(__file__).resolve().parent
raw=(O/'primary-pbps.exactraw.snapshot.html').read_bytes()
H=lambda b:hashlib.sha256(b).hexdigest()
regions=json.loads((O/'stageA.primary419.reparsed-inventory.json').read_bytes())['regions']
records=[]
for r in regions:
 a,z=r['RAW_range_end_exclusive']; part=raw[a:z]
 def math_repl(m):
  b=m.group(); i=re.search(rb'\bid="([^"]+)"',b).group(1).decode(); t=html.unescape(re.search(rb'\balttext="([^"]*)"',b).group(1).decode('utf-8'))
  return ('\nMATH '+i+' RAW['+str(a+m.start())+','+str(a+m.end())+') '+t+'\n').encode('utf-8')
 v=re.sub(rb'<math\b[^>]*>.*?</math>',math_repl,part,flags=re.S)
 v=re.sub(rb'</(?:p|div|section|h[1-6]|tr|table|figure|li)>',b'\n',v)
 v=re.sub(rb'<[^>]*>',b'',v)
 text=html.unescape(v.decode('utf-8'))
 text=re.sub(r'\n[ \t]*\n+', '\n\n',text)
 name='stageA.primary-readview.'+r['name']+'.txt'
 (O/name).write_text(text,encoding='utf-8',newline='\n')
 records.append({'name':name,'source_RAW_range_end_exclusive':[a,z],'source_RAW_sha256':H(part),'view_RAW_sha256':H((O/name).read_bytes()),'view_is_attributed_parser_aid_not_primary':True,'formula_bytes_authority':'original exact RAW math tags; alttext crosschecked with annotation TeX'})
report={'schema':'source70-stageA-attributed-primary-readviews-v1','actual_pid':os.getpid(),'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'views':records,'current70_BODY_read':False}
(O/'stageA.primary-readviews.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
for name in sys.argv[1:]:
 p=O/('stageA.primary-readview.'+name+'.txt'); print('READVIEW '+name+'\n'+p.read_text(encoding='utf-8'))
