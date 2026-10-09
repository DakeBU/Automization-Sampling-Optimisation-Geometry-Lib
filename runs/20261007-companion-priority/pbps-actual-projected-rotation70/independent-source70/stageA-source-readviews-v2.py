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
 a,z=r['RAW_range_end_exclusive']; part=raw[a:z]; formulas={}
 def math_repl(m):
  b=m.group(); i=re.search(rb'\bid="([^"]+)"',b).group(1).decode(); t=html.unescape(re.search(rb'\balttext="([^"]*)"',b).group(1).decode('utf-8'))
  token='ASTISRAWFORMULATOKEN'+str(len(formulas))+'ENDTOKEN'
  formulas[token]='\nMATH '+i+' RAW['+str(a+m.start())+','+str(a+m.end())+') '+t+'\n'
  return token.encode('ascii')
 v=re.sub(rb'<math\b[^>]*>.*?</math>',math_repl,part,flags=re.S)
 v=re.sub(rb'</(?:p|div|section|h[1-6]|tr|table|figure|li)>',b'\n',v)
 v=re.sub(rb'<[^>]*>',b'',v)
 text=html.unescape(v.decode('utf-8'))
 for token,formula in formulas.items():
  assert text.count(token)==1
  text=text.replace(token,formula)
 text=re.sub(r'\n[ \t]*\n+', '\n\n',text)
 name='stageA.primary-readview-v2.'+r['name']+'.txt'
 (O/name).write_text(text,encoding='utf-8',newline='\n')
 records.append({'name':name,'source_RAW_range_end_exclusive':[a,z],'source_RAW_sha256':H(part),'view_RAW_sha256':H((O/name).read_bytes()),'math_count':len(formulas),'view_is_attributed_parser_aid_not_primary':True,'formula_preservation':'Math placeholders protected from HTML tag stripping; RAW alttext and annotation agreement separately verified'})
report={'schema':'source70-stageA-attributed-primary-readviews-v2','actual_pid':os.getpid(),'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'views':records,'supersedes_view_v1_only':True,'v1_limitation':'HTML tag removal after inserting TeX may swallow source less-than inequalities; v1 aids retired and retained, RAW and inventory unchanged.','current70_BODY_read':False}
(O/'stageA.primary-readviews-v2.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
for name in sys.argv[1:]:
 p=O/('stageA.primary-readview-v2.'+name+'.txt'); print('READVIEW V2 '+name+'\n'+p.read_text(encoding='utf-8'))
