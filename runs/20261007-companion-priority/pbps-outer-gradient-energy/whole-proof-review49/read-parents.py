# -*- coding: utf-8 -*-
from pathlib import Path
import sys
sys.stdout.reconfigure(encoding='utf-8');r=Path('E:/Samplinglib')
for file in ['AutoSamplingTheory/ExampleCases/ProximalBPS/GibbsAugmentation.lean','AutoSamplingTheory/ExampleCases/ProximalBPS/GaussianReflection.lean','AutoSamplingTheory/ExampleCases/ProximalBPS/ConditionalGradientVariance.lean','AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/Poincare.lean','runs/20261007-companion-priority/pbps-outer-gradient-energy/mathlib-ready-leaf.md','runs/20261007-companion-priority/pbps-outer-gradient-energy/production.2.log']:
 print('\nFILE',file)
 for n,line in enumerate((r/file).read_text(encoding='utf-8').splitlines(),1): print('%03d %s'%(n,line))
file='runs/20261007-companion-priority/pbps-outer-gradient-energy/tests.1.log';ls=(r/file).read_text(encoding='utf-8').splitlines();print('\nTESTS LOG LAST30');print('\n'.join(ls[-30:]))
