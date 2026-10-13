# -*- coding: utf-8 -*-
from pathlib import Path
import json,hashlib,sys
sys.stdout.reconfigure(encoding='utf-8')
R=Path('E:/Samplinglib');D=R/'runs/20261007-companion-priority/pbps-outer-gradient-energy';O=D/'whole-proof-review49'
def sha(b):return hashlib.sha256(b).hexdigest()
def lf(b):return b.replace(b'\r\n',b'\n')
f=json.loads((D/'math-freeze.json').read_text(encoding='utf-8'));pins=[]
for i,x in enumerate(f['inputs']):
 b=(R/x['path']).read_bytes();assert sha(b)==x['raw_sha256'],x['path'];assert sha(lf(b))==x['lf_sha256'];assert len(b)==x['bytes']
 stem='input-%02d'%i;(O/(stem+'.raw')).write_bytes(b);(O/(stem+'.lf')).write_bytes(lf(b));pins.append(dict(x,id=stem,raw_snapshot=stem+'.raw',lf_snapshot=stem+'.lf'))
b=(D/'math-freeze.json').read_bytes();(O/'math-freeze.raw.json').write_bytes(b);(O/'math-freeze.lf.json').write_bytes(lf(b));pins.append(dict(path=str(D/'math-freeze.json'),raw_sha256=sha(b),lf_sha256=sha(lf(b)),bytes=len(b),raw_snapshot='math-freeze.raw.json',lf_snapshot='math-freeze.lf.json'))
(O/'input-bindings.json').write_text(json.dumps(pins,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('PINNED',len(f['inputs']),'FROZEN INPUTS, base',f['checked_base_commit'])
for name in ['AutoSamplingTheory/ExampleCases/ProximalBPS/ConditionalGradientEnergy.lean','Tests/ProximalBPSConditionalGradientEnergy.lean','runs/20261007-companion-priority/pbps-outer-gradient-energy/claim.json','runs/20261007-companion-priority/pbps-outer-gradient-energy/production.2.status.json','runs/20261007-companion-priority/pbps-outer-gradient-energy/tests.1.status.json']:
 print('\nFILE',name)
 for n,line in enumerate((R/name).read_text(encoding='utf-8').splitlines(),1): print('%03d %s'%(n,line))
