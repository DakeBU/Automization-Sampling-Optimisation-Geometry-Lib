# -*- coding: utf-8 -*-
from pathlib import Path
import json,sys,hashlib
sys.stdout.reconfigure(encoding='utf-8');R=Path('E:/Samplinglib');O=R/'runs/20261007-companion-priority/pbps-after-energy-preread50';pins=[]
def pin(p,id,b):
 whole=p.read_bytes();(O/(id+'.raw')).write_bytes(b);(O/(id+'.lf')).write_bytes(b.replace(b'\r\n',b'\n'));pins.append(dict(id=id,path=str(p),whole_raw_sha256=hashlib.sha256(whole).hexdigest(),whole_lf_sha256=hashlib.sha256(whole.replace(b'\r\n',b'\n')).hexdigest(),whole_bytes=len(whole),fragment_raw_sha256=hashlib.sha256(b).hexdigest(),fragment_lf_sha256=hashlib.sha256(b.replace(b'\r\n',b'\n')).hexdigest(),raw_snapshot=id+'.raw',lf_snapshot=id+'.lf'))
for id,rel in [('reflection','AutoSamplingTheory/ExampleCases/ProximalBPS/ReflectionL2.lean'),('representative','AutoSamplingTheory/ExampleCases/ProximalBPS/MacroscopicRepresentative.lean')]:
 p=R/rel;b=p.read_bytes();a=b.index(b'theorem ');z=b.index(b':= by',a);f=b[a:z];pin(p,'public-'+id,f);print('\nPUBLIC',id);print(f.decode('utf-8'))
for id,rel in [('reflection-cell','research-wiki/frontier-cells/ASTIS-SW-PBPS-reflection-l2-blocks.json'),('representative-cell','research-wiki/frontier-cells/ASTIS-SW-PBPS-macroscopic-representative.json'),('weighted-cell','research-wiki/frontier-cells/ASTIS-SW-PBPS-weighted-gradient.json'),('gradient-distribution-cell','research-wiki/frontier-cells/ASTIS-SW-PBPS-gradient-distributional.json')]:
 p=R/rel;b=p.read_bytes();pin(p,id,b);d=json.loads(b);print('\nCELL',id,json.dumps({k:d[k] for k in ['id','cell_id','status','source_contract','reuse_plan','open_obligations','residual_obligations','next_delta','dependencies'] if k in d},ensure_ascii=False))
p=R/'website/content/samplewiki_companion_frontiers.json';b=p.read_bytes();pin(p,'frontier-execution-provider',b);d=json.loads(b);print('\nEXECUTION',json.dumps(d['execution'],ensure_ascii=False))
for id,rel in [('measure-card','research-wiki/sampling-sde-library/cards/AutoSamplingTheory.TechnicalLemmas.Measure.md'),('functional-card','research-wiki/sampling-sde-library/cards/AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.md'),('probability-card','research-wiki/sampling-sde-library/cards/AutoSamplingTheory.TechnicalLemmas.Probability.md')]:
 p=R/rel;b=p.read_bytes();pin(p,id,b);print('\nCARD',id);print(b.decode('utf-8')[:4200])
(O/'api-input-bindings.initial.json').write_text(json.dumps(pins,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
