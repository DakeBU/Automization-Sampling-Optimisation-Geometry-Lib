from pathlib import Path
r=Path(__file__).parent
assert (r/'root.statement-seal82.json').exists()
header=(r/'header82.proposed.lean').read_text(encoding='utf8')
prefix=header.split('\nend\n',1)[0]
sig=header.split('private def actual_small_time_stochastic_continuity_statement',1)[1].split(' : Prop :=',1)[0]
lets=header.split(' : Prop :=\n',1)[1].split('    ∃ Z :',1)[0]
lets='\n'.join(line[2:] if line.startswith('  ') else line for line in lets.splitlines())
body=(r/'body82.txt').read_text(encoding='utf8')
target=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualSmallTimeContinuity.lean');assert not target.exists()
target.write_text(prefix+'\n\nset_option maxHeartbeats 1600000 in\n/-- Actual PBPS phase-flow defect probability and zero-time stochastic continuity.\nThis source prerequisite asserts no process Markov or full L2 semigroup result. -/\ntheorem actual_small_time_stochastic_continuity'+sig+' :\n    actual_small_time_stochastic_continuity_statement hα hαβ hV hH hη hβη := by\n  classical\n'+lets+'\n'+body+'\nend\nend AutoSamplingTheory.ExampleCases.ProximalBPS.ActualSmallTimeContinuity\n',encoding='utf8',newline='\n')
old=Path('runs/20261007-companion-priority/pbps-actual-physical-time-law81/focused81.py').read_text(encoding='utf8')
(r/'focused82.py').write_text(old.replace('pbps-actual-physical-time-law81','pbps-actual-small-time-continuity82').replace('IdealHalfTurnKernel','ActualSmallTimeContinuity'),encoding='utf8',newline='\n')
