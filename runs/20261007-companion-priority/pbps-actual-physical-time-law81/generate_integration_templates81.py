from pathlib import Path
old=Path('runs/20261007-companion-priority/pbps-actual-physical-time-measurability80');new=Path('runs/20261007-companion-priority/pbps-actual-physical-time-law81')
for name in ['run_gates80.py','refresh_graph80.py']:
 s=(old/name).read_text(encoding='utf8')
 for a,b in [('pbps-actual-physical-time-measurability80','pbps-actual-physical-time-law81'),('ASTIS-SW-PBPS-actual-physical-time-measurability','ASTIS-SW-PBPS-ideal-half-turn-kernel'),('ActualPhysicalTimeMeasurability','IdealHalfTurnKernel'),('integration80','integration81'),('SAU80','SAU81'),('bdc743c8022ef5e682f38ecac2f8e5a9815ff3de','7b7906944cafaea3bb6b8c289a599dc3a6bf6f51')]:s=s.replace(a,b)
 p=new/name.replace('80','81');assert not p.exists();p.write_text(s,encoding='utf8',newline='\n')
print('Prepared existing pure graph/gate wrappers for81; not executed, canonical tools unchanged')
