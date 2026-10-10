from pathlib import Path
import json

old=Path('.astis/pbps-root-commutation67/foreground67.py').read_text(encoding='utf-8')
dest=Path('.astis/pbps-sharp-energy68');dest.mkdir(exist_ok=True)
p=dest/'foreground68.py';assert not p.exists()
start=old.index('names = [');end=old.index('inputs = ',start)
names=['lean-toolchain','lake-manifest.json',
       'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualRootCommutation.lean',
       'Tests/ProximalBPSActualRootCommutation.lean',
       'runs/20261007-companion-priority/pbps-root-commutation67/root.exact-verification67.adoption.json',
       'runs/20261007-companion-priority/pbps-sharp-energy-preproof68/root.statement-seal68.json',
       'AutoSamplingTheory/TechnicalLemmas/Analysis/HilbertCorrectorBound.lean',
       'AutoSamplingTheory/ExampleCases/ProximalBPS/SharpCorrectorEnergy.lean',
       'Tests/ProximalBPSSharpCorrectorEnergy.lean',
       'research-wiki/frontier-cells/ASTIS-SHARED-hilbert-corrector-square-bound.json',
       'research-wiki/frontier-cells/ASTIS-SW-PBPS-sharp-corrector-energy.json']
text=old[:start]+'names = '+repr(names)+'\n'+old[end:]
text=text.replace("out = root / 'runs/20261007-companion-priority/pbps-root-commutation67' / label",
                  "out = root / 'runs/20261007-companion-priority/pbps-sharp-energy68' / label")
p.write_text(text,encoding='utf-8',newline='\n')
print('Prepared bounded foreground68 wrapper; no canonical files, SAU or proofs written.')
