import sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
import json,pathlib,os
O=pathlib.Path(__file__).resolve().parent;R=O.parent;B=pathlib.Path('E:/Samplinglib')
l=json.loads((B/'website/content/declaration_lessons/pbps-actual-projected-rotation.json').read_bytes())['units'][0];c=json.loads((R/'integration70/visual70/copy-unit0-copy-and-download.inspect.json').read_bytes());print('PID',os.getpid())
for key in ['lean_statement','lean_proof']:print(key,type(l[key]).__name__,repr(l[key])[:1800])
for i,q in enumerate(c['panels']):print('panel',i,len(q['code']),repr(q['code'][:200]),repr(q['code'][-120:]))
print('moduleline133-145',repr((B/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualProjectedRotation.lean').read_text(encoding='utf-8').splitlines()[132:145]))
