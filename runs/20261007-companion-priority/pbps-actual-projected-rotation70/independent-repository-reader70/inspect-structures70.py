import sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
import pathlib,json,os,subprocess
O=pathlib.Path(__file__).resolve().parent;R=O.parent;B=pathlib.Path('E:/Samplinglib')
print('PID',os.getpid())
for n in ['independent-reader-helper-code70/lease.final.json','independent-source70/lease.final.json','exact-science-verification70/lease.final.json','exact-science-verification70-label-supplement/lease.final.json','anonymous-decoder/lease.json','integration70/visual70/copy-capture.json','integration70/visual70/copy-unit0-copy-and-download.inspect.json','integration70/generator-sideeffects/receipt.json']:
 x=json.loads((R/n).read_bytes());print('\n',n,'keys',list(x))
 for k,v in x.items():
  if isinstance(v,list):print(k,'count',len(v),'first',json.dumps(v[:1],ensure_ascii=False)[:2500])
  elif isinstance(v,dict):print(k,'keys',list(v),'sample',json.dumps(v,ensure_ascii=False)[:1700])
  else:print(k,str(v)[:1400])
lesson=json.loads((B/'website/content/declaration_lessons/pbps-actual-projected-rotation.json').read_bytes())['units'][0]
print('\nLESSON keys',list(lesson));print('proof first',json.dumps(lesson.get('proof',lesson.get('steps')),ensure_ascii=False)[:5000]); print('helpers',lesson.get('helpers'))
for n in ['AutoSamplingTheory/TechnicalLemmas/Registry.lean','conversion-windows/ASTIS-SW-PBPS-2026.md']:
 t=(B/n).read_text(encoding='utf-8');print('\nTEXT',n); print(t[ t.index('localDecl := "AutoSamplingTheory.ExampleCases.ProximalBPS.ActualProjectedRotation')-200:t.index('localDecl := "AutoSamplingTheory.ExampleCases.ProximalBPS.ActualProjectedRotation')+1400] if n.endswith('.lean') else t[:6000])
x=json.loads((B/'_site/data/underlying-lean-graph.json').read_bytes());print('\nGRAPH keys',list(x));print('nodes type',type(x.get('nodes')).__name__);print('nodefirst',str(x.get('nodes',[None])[0])[:1000]);print('edgefirst',str(x.get('edges',[None])[0])[:1000])
for c in [['git','rev-parse','HEAD'],['git','show','--format=fuller','--stat','--oneline','c46af8a55e89419109f654c4553cf527993cbeed'],['git','diff','--name-status','c46af8a55e89419109f654c4553cf527993cbeed','--']]:
 p=subprocess.Popen(c,cwd=B,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=p.communicate();print('\nCMD',c,'PID',p.pid,'EXIT',p.returncode);print(out.decode('utf-8',errors='replace')[:7000]);print(err.decode('utf-8',errors='replace')[:1000]);assert p.returncode==0
