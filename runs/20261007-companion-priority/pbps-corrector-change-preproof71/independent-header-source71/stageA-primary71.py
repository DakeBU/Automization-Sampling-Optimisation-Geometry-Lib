import sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
import pathlib,json,hashlib,re,html,os,datetime
O=pathlib.Path(__file__).resolve().parent;S=O.parent/'independent-source-first71'
H=lambda b:hashlib.sha256(b).hexdigest()
def J(p):return json.loads(p.read_bytes())
def put(n,x):assert not (O/n).exists();(O/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
inputs=[]
def snap(p,n):
 raw=p.read_bytes();lf=raw.replace(b'\r\n',b'\n');assert not (O/n).exists();(O/n).write_bytes(raw);(O/(n+'.LF')).write_bytes(lf)
 inputs.append({'original_path':str(p),'snapshot':n,'RAW_bytes':len(raw),'RAW_sha256':H(raw),'LF_snapshot':n+'.LF','LF_bytes':len(lf),'LF_sha256':H(lf),'LF_recipe':'replace ONLY CRLF byte pairs with LF','original_mtime_ns':p.stat().st_mtime_ns});return raw
regions=J(S/'source.regions.json');formulas=J(S/'source.formulas.exact.json')
P=pathlib.Path(regions['whole_primary']['path']);primary=snap(P,'primary-pbps.exactraw.snapshot.html')
assert len(primary)==1482128 and H(primary)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
for n in ['source.regions.json','source.formulas.exact.json','source.math.inventory.json','outputs.manifest.json','lease.final.json']:snap(S/n,'source-first71.'+n)
items=[];count_regions=[]
for r in regions['regions']:
 a,z=r['start_byte'],r['end_byte_exclusive'];raw=snap(pathlib.Path(r['RAW']['path']),'source.'+r['name']+'.RAW.html');assert raw==primary[a:z] and H(raw)==r['RAW']['raw_sha256']
 found=[]
 for m in re.finditer(rb'<math\b[^>]*>.*?</math>',raw,re.S):
  tag=m.group();mi=re.search(rb'\bid="([^"]+)"',tag);ma=re.search(rb'\balttext="([^"]*)"',tag);ann=re.search(rb'<annotation\b[^>]*encoding="application/x-tex"[^>]*>(.*?)</annotation>',tag,re.S)
  assert mi and ma and ann;tex=html.unescape(ma.group(1).decode());annotation=html.unescape(ann.group(1).decode());assert tex==annotation
  q={'id':mi.group(1).decode(),'region':r['name'],'source_RAW_range_end_exclusive':[a+m.start(),a+m.end()],'RAW_bytes':len(tag),'RAW_sha256':H(tag),'alttext':tex};items.append(q);found.append(q)
 count_regions.append({'name':r['name'],'source_RAW_range_end_exclusive':[a,z],'math_count':len(found),'RAW_sha256':H(raw)})
for f in formulas['formulas']:
 a,z=f['start_byte'],f['end_byte_exclusive'];assert H(primary[a:z])==f['RAW_sha256'];q=next(q for q in items if q['id']==f['id']);assert q['alttext']==f['alttext'] and q['source_RAW_range_end_exclusive']==[a,z]
oldinventory=J(S/'source.math.inventory.json');assert len(items)==oldinventory['math_count']
put('stageA.independent-RAW-math-inventory.json',{'schema':'prospective-header71-independent-primary-reparse-v1','count':len(items),'regions':count_regions,'items':items,'target_formulas_count':18,'all_target_formulas_exact_primary_match':True,'current71_header_seen':False})
put('stageA.primary-input-manifest.json',{'schema':'prospective-header71-primary-only-exact-inputs-v1','actual_pid':os.getpid(),'inputs':inputs,'input_count':len(inputs),'current71_header_seen':False,'no_prior_header_math_verdict_read':True,'no_decision_run_or_interface_verdict_from_source-first71_read':True,'source-only_formulas_regions_reused_with_independent_RAW_checks':True})
# Bounded exact primary windows, equations protected while stripping HTML for a reading aid.
for name,a,z in [('corrector-definition',818000,828800),('actual-rotation-B21',829000,855000),('B4-corrector-consumer',924800,934000)]:
 raw=primary[a:z];saved=[]
 def token(m):saved.append(html.unescape(re.search(rb'\balttext="([^"]*)"',m.group()).group(1).decode()));return (' MATHPLACEHOLDER'+str(len(saved)-1)+' ').encode()
 protected=re.sub(rb'<math\b[^>]*>.*?</math>',token,raw,flags=re.S);text=html.unescape(re.sub(rb'<[^>]*>',b' ',protected).decode())
 for i,tex in enumerate(saved):text=text.replace('MATHPLACEHOLDER'+str(i),' ['+tex+'] ')
 text=re.sub(r'\s+',' ',text);(O/('stageA.readview.'+name+'.txt')).write_text(text+'\n',encoding='utf-8',newline='\n');print(name+' RAW['+str(a)+','+str(z)+')\n'+text+'\n')
print(json.dumps({'actual_pid':os.getpid(),'regions':len(count_regions),'independent_math_count':len(items),'target_formulas':18,'input_count':len(inputs),'header71_seen':False},ensure_ascii=False))
