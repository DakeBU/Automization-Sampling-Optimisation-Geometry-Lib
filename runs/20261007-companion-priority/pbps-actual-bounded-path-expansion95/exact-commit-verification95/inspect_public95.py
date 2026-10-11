import pathlib,json,re,hashlib
R=pathlib.Path('E:/Samplinglib');O=pathlib.Path(__file__).resolve().parent;B=O.parent
paths=['website/content/declaration_lessons/pbps-actual-bounded-path-expansion.json','website/content/publications/pbps-actual-bounded-path-expansion.json','research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261011-PBPSActualBoundedPathExpansion.json','research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-bounded-path-expansion.json',str(B/'claim.json'),'runs/20261007-companion-priority/pbps-bounded-path-expansion-preread95/root.statement-seal95.json']
results=[]
def walk(v,f,p):
 if isinstance(v,dict):
  for k,x in v.items():walk(x,f+'.'+k,p)
 elif isinstance(v,list):
  for i,x in enumerate(v):walk(x,f+'['+str(i)+']',p)
 elif isinstance(v,str) and re.search(r'[A-Za-z]:[/\\]',v):results.append({'file':p,'field':f,'value':v})
for p in paths:walk(json.loads((R/p).read_bytes()),'',p)
(O/'portability-inventory.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for r in results:print(r['file'],r['field'],r['value'][:180])
lesson=json.loads((R/paths[0]).read_bytes())['units'][0]
regions=[];module=(R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualBoundedPathExpansion.lean').read_bytes();lines=module.decode().splitlines(keepends=True)
for i,s in enumerate(lesson['steps']):
 rg=s['lean_source_region'];code=''.join(lines[rg['start_line']-1:rg['end_line']]);assert code==s['lean'];assert hashlib.sha256(code.encode()).hexdigest()==rg['exact_code_raw_sha256'];assert hashlib.sha256(module).hexdigest()==rg['source_raw_sha256'];regions.append({'step':i+1,'region':rg});print(i+1,s['text'],s['formula'])
(O/'exposition-regions95.json').write_text(json.dumps(regions,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
