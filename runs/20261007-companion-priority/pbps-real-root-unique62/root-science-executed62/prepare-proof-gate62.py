from pathlib import Path
import json
s=Path('.astis/pbps-real-root-unique62/preproof-gate62.py').read_text(encoding='utf-8');start=s.index('math=[');end=s.index(';inputs=',start)
pre=Path('runs/20261007-companion-priority/pbps-real-root-unique-preproof62');r=Path('runs/20261007-companion-priority/pbps-real-root-unique62');c=json.loads((r/'claim.json').read_bytes())
inputs=c['proposed_files']+['AutoSamplingTheory/TechnicalLemmas/Measure/L2RealComplexOperator.lean','AutoSamplingTheory/ExampleCases/ProximalBPS/RealDefectRoot.lean','lean-toolchain','lake-manifest.json']+[str(pre/n) for n in ['header0.lean','header1.lean','root.statement-seal62.json']]
s=s[:start]+'math='+repr(inputs)+s[end:];s=s.replace("out=root/'runs/20261007-companion-priority/pbps-real-root-unique-preproof62'/label","out=root/'runs/20261007-companion-priority/pbps-real-root-unique62'/label")
Path('.astis/pbps-real-root-unique62/proof-gate62.py').write_text(s,encoding='utf-8',newline='\n');print('Prepared focused62 proof observer with exact3 new sources/parents/sealed headers pinned before compiler spawn.')
