# -*- coding: utf-8 -*-
from pathlib import Path
import sys,json
sys.stdout.reconfigure(encoding='utf-8')
p=Path('runs/20261007-companion-priority/next-ready-preread47/primary-pbps.raw.snapshot.html'); print(p.read_text(encoding='utf-8').splitlines()[4573])
d=Path('runs/20261007-companion-priority/pbps-outer-gradient-sourcegraph49')
print((d/'selected-P.fderiv-context2.raw').read_text(encoding='utf-8'))
for n in ['additional-P.mean-bound','additional-P.map-prob','additional-P.compact-bound','api-P.var-sub','parent-context-GibbsAugmentation','parent-context-GaussianReflection']:
 print(n,(d/(n+'.raw')).read_text(encoding='utf-8'))
