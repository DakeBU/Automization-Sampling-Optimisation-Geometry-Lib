from pathlib import Path
import ast,os
root=Path('E:/Samplinglib')
old=root/'runs/20261007-companion-priority/pbps-actual-bounce-rate74/exact-science-verification74/verify74.py'
own=Path(__file__).parent
source=old.read_text(encoding='utf-8');lines=source.splitlines(keepends=True)
names={'now','sha','canon','load','read','write','path','pin','check','git','state','differences','recheck','process','gates','transition','transition_readback','allowned','finalize','readback','close_probe','close','postclose','launch'}
prefix=source[:source.index('def now():')]
parts=[prefix]+[''.join(lines[n.lineno-1:n.end_lineno])+'\n' for n in ast.parse(source).body if isinstance(n,ast.FunctionDef) and n.name in names]
text=''.join(parts).replace('pbps-actual-bounce-rate74','pbps-actual-hazard-clock75').replace('ActualBounceRate','ActualHazardClock').replace('actual-bounce-rate','actual-hazard-clock').replace('PBPSActualBounceRate','PBPSActualHazardClock').replace('actual_bounce_rate_energy_laws','actual_integrated_hazard_clock_laws').replace('exact-science-verification74','exact-science-verification75').replace('SCI74','SCI75').replace('r74/','r75/').replace('19204','18716').replace('52720','21324').replace('d556a7550f0395d149720da6478bfdfff98368a7','51d3a65f65b189b0afaaf91a248f8c2f58162ef2').replace('e91f9b3acfeea172c33053b28d88b7fea6e61e9d','526a6af98cf0380032a3aed52da01c5304de3bb8')
(own/'verify75.py').write_text(text,encoding='utf-8',newline='\n')
print('Prepared bounded SCI75 helper from immutable74 utility/closure definitions only; actualPID',os.getpid())
