from pathlib import Path
src=Path('.astis/pbps-bounce74/foreground74.py').read_text(encoding='utf8')
src=src.replace('pbps-actual-bounce-rate74','pbps-actual-hazard-clock75').replace('pbps-bounce-rate-preproof74','pbps-clock-preproof75').replace('ActualBounceRate.lean','ActualHazardClock.lean').replace('ASTIS-SW-PBPS-actual-bounce-rate.json','ASTIS-SW-PBPS-actual-hazard-clock.json').replace("'header74.proposed.lean','root.statement-seal74.json','root.header-reviews74.adoption.json'","'header75.v2.proposed.lean','root.statement-seal75.json','root.header-reviews75.adoption.json'")
src=src.replace("'AutoSamplingTheory/TechnicalLemmas/Analysis/QuadraticRegularization.lean'","'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHarmonicFlow.lean','AutoSamplingTheory/ExampleCases/ProximalBPS/ActualBounceRate.lean'")
p=Path('.astis/pbps-clock75/foreground75.py');assert not p.exists();p.write_text(src,encoding='utf8',newline='\n')
