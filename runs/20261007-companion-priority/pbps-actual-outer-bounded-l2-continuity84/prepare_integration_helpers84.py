from pathlib import Path
r=Path(__file__).parent;old=r.parent/'pbps-actual-bounded-test-continuity83'
files=['run_gates83.py','refresh_graph83.py','render_svg83.js','record_svg_view83.py','inspect_reader_html83.py','commit_integration83.py']
common=[('pbps-actual-bounded-test-continuity83','pbps-actual-outer-bounded-l2-continuity84'),('pbps-bounded-test-preread83','pbps-outer-bounded-l2-preread84'),('integration83','integration84'),('pbps-actual-bounded-test-continuity','pbps-actual-outer-bounded-l2-continuity'),('ActualBoundedTestContinuity','ActualOuterBoundedL2Continuity'),('SAU83','SAU84'),('actual83 branch','actual84 branch'),('actual bounded-test clock expectation theorem','actual bounded-test outer square-integral theorem'),('post-fetch83.workspace-RAW.corrected.json','pre-fetch84.workspace-RAW.json'),('immutable-whitespace-archives83','immutable-whitespace-archives84'),('immutable-integration-log-archives83','immutable-integration-log-archives84'),('staged-scope83','staged-scope84'),('Integrate verified actual PBPS bounded-test expectation and reader evidence','Integrate verified actual PBPS bounded-test outer square integral and reader evidence'),('481d8f1bca0dd1b3219ef7b8c0f882583f6316b4','5f29b2a3b5a95d7ee9f8e166ba833857ef0845e2')]
for name in files:
 s=(old/name).read_text(encoding='utf8')
 for a,b in common:s=s.replace(a,b)
 if name=='commit_integration83.py':
  a=s.index("if (r/'next-source84.readiness.json').exists():")
  b=s.index('\nfor offset in range',a)
  s=s[:a]+s[b:]
 p=r/name.replace('83.','84.');assert not p.exists();p.write_text(s,encoding='utf8',newline='\n')
print('Deferred helpers prepared; none executed, independent VERIFIED remains prerequisite')
