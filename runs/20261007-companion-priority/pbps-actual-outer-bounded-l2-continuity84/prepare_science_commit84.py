from pathlib import Path
r=Path(__file__).parent
s=Path('runs/20261007-companion-priority/pbps-actual-bounded-test-continuity83/commit_science83.py').read_text(encoding='utf8')
for a,b in [
 ('pbps-bounded-test-preread83','pbps-outer-bounded-l2-preread84'),('root.source83.adoption','root.source84.adoption'),('root.math83.adoption','root.math84.adoption'),('post-fetch83.workspace-RAW.corrected','pre-fetch84.workspace-RAW'),('immutable-whitespace-archives83','immutable-whitespace-archives84'),('ActualBoundedTestContinuity.lean','ActualOuterBoundedL2Continuity.lean'),('ASTIS-SW-PBPS-actual-bounded-test-continuity','ASTIS-SW-PBPS-actual-outer-bounded-l2-continuity'),('ASTIS-RT-20261010-PBPSActualBoundedTestContinuity','ASTIS-RT-20261011-PBPSActualOuterBoundedL2Continuity'),('pbps-actual-bounded-test-continuity.json','pbps-actual-outer-bounded-l2-continuity.json'),('science-staging83','science-staging84'),('science-stage-whitespace83','science-stage-whitespace84'),('Prove actual PBPS bounded-test clock integrability and expectation continuity','Prove actual PBPS bounded-test outer square-integral continuity')]:
 assert a in s,a;s=s.replace(a,b)
p=r/'commit_science84.py';assert not p.exists();p.write_text(s,encoding='utf8',newline='\n')
