"""Reuse terminal gate utilities with explicit identities; execute none here."""
from pathlib import Path
r=Path(__file__).parent;old=r.parent/'pbps-actual-outer-bounded-l2-continuity84'
pairs=[('pbps-actual-outer-bounded-l2-continuity84','pbps-actual-phase-transition-kernel85'),('integration84','integration85'),('ASTIS-SW-PBPS-actual-outer-bounded-l2-continuity','ASTIS-SW-PBPS-actual-phase-transition-kernel'),('pbps-actual-outer-bounded-l2-continuity','pbps-actual-phase-transition-kernel'),('ActualOuterBoundedL2Continuity','ActualPhaseTransitionKernel')]
for name in ['run_gates84.py','refresh_graph84.py','render_svg84.js','record_svg_view84.py','inspect_reader_html84.py']:
 s=(old/name).read_text(encoding='utf8')
 for a,b in pairs:s=s.replace(a,b)
 if name=='run_gates84.py':
  s=s.replace('SAU84','SAU85').replace('5f29b2a3b5a95d7ee9f8e166ba833857ef0845e2','f145260bd7470ae06d8839fb6d6b158141ce5754')
  assert '"--cell", "ASTIS-SW-PBPS-actual-phase-transition-kernel"' in s
 if name=='inspect_reader_html84.py':
  s=s.replace("== 8","== 6").replace("'exact_step_Lean_regions': 8","'exact_step_Lean_regions': 6").replace('eight exact adjacent','six exact adjacent')
 if name=='record_svg_view84.py':
  s=s.replace('Precise actual84 branch separately generated and checked.','New actual85 declaration is checked in the reference graph; name-scanned references remain incomplete signals. Kernel-audited actual proof dependencies are separately certified.')
 assert 'ASTIS-SW-PBPS-actual-outer-bounded-l2-continuity' not in s
 p=r/name.replace('84.','85.');assert not p.exists();p.write_text(s,encoding='utf8',newline='\n')
print('Five deferred terminal/render/HTML utilities prepared with exact85 target; no shared mutation')
