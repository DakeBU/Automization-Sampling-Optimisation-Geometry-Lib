from pathlib import Path
import re,json,os
p=Path('runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html').read_bytes()
for m in re.finditer(rb'id="(A1\.[^"]+)"',p[533229:575000]):
 id=m.group(1).decode()
 if '.Ex' in id:print(id,533229+m.start())
root=Path('E:/Samplinglib');s=(root/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteJumpRecursion.lean').read_text();h=(root/'runs/20261007-companion-priority/pbps-recursive-preproof76/header76.v3.proposed.lean').read_text()
a=s[s.index('private def '):s.index('set_option maxHeartbeats')].strip();z=h[h.index('private def '):h.index('set_option maxHeartbeats')].strip();print('seal_full_private_exact',a==z)
print('header_tail',h[h.index('set_option maxHeartbeats'):])
print('PID',os.getpid())
