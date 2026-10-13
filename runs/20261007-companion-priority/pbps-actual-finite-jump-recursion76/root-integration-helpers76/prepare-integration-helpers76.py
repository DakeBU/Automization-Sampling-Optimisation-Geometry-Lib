from pathlib import Path
import ast,json,re
old=Path('.astis/pbps-clock75');new=Path('.astis/pbps-recursion76')
def adapt(s):
 for a,b in [('pbps-actual-hazard-clock75','pbps-actual-finite-jump-recursion76'),('pbps-clock75','pbps-recursion76'),('ActualHazardClock.actual_integrated_hazard_clock_laws','ActualFiniteJumpRecursion.actual_fixed_reference_finite_jump_recursion'),('ActualHazardClock','ActualFiniteJumpRecursion'),('actual-hazard-clock','actual-finite-jump-recursion')]:s=s.replace(a,b)
 return re.sub(r'75(?![0-9a-f])','76',s)
names=['inspect-cdp75.mjs','inspect-copy75.mjs','final-gates75.py','reuse-regression75.py','prepare-generated-scope75.py','refresh-affected-module-graph75.py','small-gates75.py','run-integration75.py','commit-integration75.py','github-integration75.py','adopt-exact75.py']
for name in names:
 s=adapt((old/name).read_text(encoding='utf8'));dest=new/name.replace('75.','76.')
 if name=='github-integration75.py':
  s=s.replace('526a6af98cf0380032a3aed52da01c5304de3bb8','54620175c56e7db191bcebe7bb010edda1744894').replace('Prove actual PBPS flow, bounce and first hazard clock','Prove actual finite PBPS jump recursion and uniform spacing')
 if name=='adopt-exact75.py':s=s.replace('fresh_direct_Lean_math76_PID18716_exact_RAW_reused=True','fresh_direct_Lean_math76_PID28496_exact_RAW_reused=True')
 if dest.suffix=='.py':ast.parse(s)
 assert not dest.exists(),dest
 dest.write_text(s,encoding='utf8',newline='\n')
print('Prepared current-target integration helpers only; no canonical changes, checks or admission.')
