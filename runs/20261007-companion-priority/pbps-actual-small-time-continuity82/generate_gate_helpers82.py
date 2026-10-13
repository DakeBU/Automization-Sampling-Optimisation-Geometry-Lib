from pathlib import Path
r=Path(__file__).parent;old=Path('runs/20261007-companion-priority/pbps-actual-physical-time-law81')
for name in ['run_gates','refresh_graph','inspect_reader_html']:
 s=(old/(name+'81.py')).read_text(encoding='utf8')
 s=s.replace('pbps-actual-physical-time-law81','pbps-actual-small-time-continuity82').replace('IdealHalfTurnKernel','ActualSmallTimeContinuity').replace('pbps-ideal-half-turn-kernel','pbps-actual-small-time-continuity').replace('ideal-half-turn-kernel','actual-small-time-continuity').replace('integration81','integration82').replace('SAU81','SAU82').replace('claim81','claim82').replace('reader-html81','reader-html82').replace('7b7906944cafaea3bb6b8c289a599dc3a6bf6f51','4502b48d0319bf35110511aa8c98f0190db3623f')
 p=r/(name+'82.py');assert not p.exists();p.write_text(s,encoding='utf8',newline='\n')
