import sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
import pathlib,json,os
O=pathlib.Path(__file__).resolve().parent;R=O.parent;B=pathlib.Path('E:/Samplinglib')
print('PID',os.getpid())
h=(B/'_site/example-cases/samplewiki/companions/proximal-bouncy-particle.html').read_text(encoding='utf-8');i=h.index('Actual PBPS projected reflection rotation and exact pair energy');print(h[i-900:i+300])
i=h.index('data-inline-lean="AutoSamplingTheory.ExampleCases.ProximalBPS.ActualProjectedRotation.actual_projected_rotation_statement"');print('\nHELPER',h[i-150:i+950])
cp=json.loads((R/'integration70/visual70/copy-unit0-copy-and-download.inspect.json').read_bytes());print('DOWNLOAD',[(list(x),x['bytes'],len(x['text'].encode()),x['href']) for x in cp['downloads']]);print('STEP',[list(x) for x in cp['steps']]);print('stepfirst',str(cp['steps'][0])[:1800])
graph=json.loads((B/'_site/data/underlying-lean-graph.json').read_bytes());decl='decl:AutoSamplingTheory.ExampleCases.ProximalBPS.ActualProjectedRotation.actual_projected_rotation';helper='decl:AutoSamplingTheory.ExampleCases.ProximalBPS.ActualProjectedRotation.actual_projected_rotation_statement'
for x in graph['nodes']:
 if x['id'] in [decl,helper,'semantic-audit:ASTIS-RT-20261009-PBPSActualProjectedRotation','cell:ASTIS-SW-PBPS-actual-projected-rotation','frontier:ASTIS-SW-PBPS-actual-projected-rotation']:print('NODE',json.dumps(x,ensure_ascii=False)[:5500])
for x in graph['edges']:
 if decl in [x['source'],x['target']] or helper in [x['source'],x['target']]:print('EDGE',x)
old=B/'runs/20261007-companion-priority/pbps-reflection-intertwining69'
for p in old.glob('**/*receipt*.json'):
 if 'independent-' in str(p) or 'exact-science' in str(p):continue
 if 'site' not in str(p).lower():continue
 try:x=json.loads(p.read_bytes())
 except:continue
 if x.get('exit_code',x.get('EXIT',0))!=0:print('OLD_NEGATIVE',p,x.get('actual_foreground_PID'),x.get('exit_code'),list(x))
