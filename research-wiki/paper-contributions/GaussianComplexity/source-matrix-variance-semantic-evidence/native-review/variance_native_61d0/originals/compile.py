from runner import *
p=json.loads((OUT/'preparation.json').read_text());c=Path(p['candidate']);lib=c/'empty-astis-output'
results=[]
for i,m in enumerate(p['order']):
 f=m.replace('.','/')+'.lean';o=lib/(m.replace('.','/')+'.olean');o.parent.mkdir(parents=True,exist_ok=True)
 dep=run(f'deps-{i:02d}',[p['lean'],'--deps',f],c,p['env']).decode()
 deps=dep.splitlines();actual=[]
 for x in deps:
  if '/AutoSamplingTheory/' in x or '/Tests/' in x:
   assert x.startswith(str(lib)+'/' ),x
   actual.append(x[len(str(lib))+1:].removesuffix('.olean').replace('/','.'))
 expected=[x for x in p['sources'][i]['imports'] if x.startswith(('AutoSamplingTheory.','Tests.'))]
 assert sorted(actual)==sorted(expected),(m,actual,expected)
 run(f'compile-{i:02d}',[p['lean'],'-o',o,f],c,p['env'])
 results.append({'module':m,'direct_astis_deps':actual,'olean_bytes':o.stat().st_size,'olean_sha256':sha(o.read_bytes())})
(OUT/'compile-results.json').write_text(json.dumps(results,indent=2))
