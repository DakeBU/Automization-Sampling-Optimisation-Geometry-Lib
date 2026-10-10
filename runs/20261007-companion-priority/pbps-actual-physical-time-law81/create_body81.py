from pathlib import Path
r=Path('runs/20261007-companion-priority/pbps-actual-physical-time-law81')
header=(r/'header81.proposed.lean').read_text(encoding='utf8')
prefix=header.split('\nend\n',1)[0]
sig=header.split('private def ideal_half_turn_returned_position_kernel_statement',1)[1].split(' : Prop :=',1)[0]
lets=header.split(' : Prop :=\n',1)[1].split('    ∃ Z :',1)[0]
lets='\n'.join(line[2:] if line.startswith('  ') else line for line in lets.splitlines())
body=(r/'body81.txt').read_text(encoding='utf8')
target=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/IdealHalfTurnKernel.lean')
assert not target.exists()
target.write_text(prefix+'\n\nset_option maxHeartbeats 1600000 in\n/-- Ideal exact-reference PBPS returned law at pi. Kernel mass and initialization\nare derived; no phase Markov property, invariance, implementation or cost claim. -/\ntheorem ideal_half_turn_returned_position_kernel'+sig+' :\n    ideal_half_turn_returned_position_kernel_statement hα hαβ hV hH hη hβη := by\n  classical\n'+lets+'\n'+body+'\nend\nend AutoSamplingTheory.ExampleCases.ProximalBPS.IdealHalfTurnKernel\n',encoding='utf8',newline='\n')
