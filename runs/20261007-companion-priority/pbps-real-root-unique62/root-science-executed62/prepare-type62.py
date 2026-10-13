from pathlib import Path
r=Path('runs/20261007-companion-priority/pbps-real-root-unique-preproof62')
imports='''import AutoSamplingTheory.ExampleCases.ProximalBPS.RealDefectRoot
open MeasureTheory ProbabilityTheory
open scoped ContDiff NNReal ENNReal Topology
set_option autoImplicit false
set_option maxHeartbeats 1000000
'''
for i in range(2):
 s=(r/f'header{i}.lean').read_text(encoding='utf-8');name=s.splitlines()[0].split()[1];expr=s.replace('theorem '+name,'fun',1).replace(' :\n',' =>\n',1)
 p=r/f'elab{i}.lean';assert not p.exists();p.write_text(imports+'#check ('+expr+' : _)\n',encoding='utf-8',newline='\n')
source=Path('.astis/pbps-real-defect-root61/proof-gate61.py').read_text(encoding='utf-8')
source=source.replace('pbps-real-defect-root-preproof61','pbps-real-root-unique-preproof62')
start=source.index("math=['");end=source.index(';inputs=',start)
names=['AutoSamplingTheory/TechnicalLemmas/Measure/L2RealComplexOperator.lean','AutoSamplingTheory/TechnicalLemmas/Measure/L2RealSquareRoot.lean','AutoSamplingTheory/ExampleCases/ProximalBPS/RealDefectRoot.lean','lean-toolchain','lake-manifest.json',str(r/'header0.lean'),str(r/'header1.lean'),str(r/'elab0.lean'),str(r/'elab1.lean'),str(r/'statement-candidate.json')]
source=source[:start]+'math='+repr(names)+source[end:]
p=Path('.astis/pbps-real-root-unique62/preproof-gate62.py');assert not p.exists();p.write_text(source,encoding='utf-8',newline='\n')
print('Prepared exact62 type-only probes/foreground observer. No62proof or claim.')
