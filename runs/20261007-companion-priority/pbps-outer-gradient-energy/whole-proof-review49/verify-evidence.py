# -*- coding: utf-8 -*-
from pathlib import Path
import hashlib,json,sys
sys.stdout.reconfigure(encoding='utf-8');R=Path('E:/Samplinglib');O=R/'runs/20261007-companion-priority/pbps-outer-gradient-energy/whole-proof-review49'
s=(R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ConditionalGradientEnergy.lean').read_text(encoding='utf-8');a=s.index('theorem reflected_conditional_gradient_energy');z=s.index(' := by',a);header=s[a:z]+'\n';sealed=(R/'runs/20261007-companion-priority/pbps-outer-gradient-preproof49/prospective-statement.txt').read_text(encoding='utf-8');assert header==sealed
(O/'statement-match.json').write_text(json.dumps(dict(exact_lf_header_equal=True,lf_bytes=len(header.encode('utf-8')),lf_sha256=hashlib.sha256(header.encode('utf-8')).hexdigest(),extraction='From public theorem keyword through conclusion, excluding final space := by; append exact sealed newline. Private helper is separate, not a public premise.'),indent=2)+'\n',encoding='utf-8')
log=(R/'runs/20261007-companion-priority/pbps-outer-gradient-energy/tests.1.log').read_text(encoding='utf-8');assert 'Build completed successfully (3888 jobs).' in log
for f in ['production.2.compiler.lease.json','tests.1.compiler.lease.json']:
 d=json.loads((R/'runs/20261007-companion-priority/pbps-outer-gradient-energy'/f).read_text(encoding='utf-8'));print(f,json.dumps(d))
# Bind current primary only; no need replay source graph/admission/publication or blind reviewer.
p=R/'runs/20261007-companion-priority/next-ready-preread47/primary-pbps.raw.snapshot.html';b=p.read_bytes();assert hashlib.sha256(b).hexdigest()=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760';selected=[]
for a,z in [(4654,4665),(3714,3735),(3777,3786),(4574,4576)]:
 f=b''.join(b.splitlines(keepends=True)[a-1:z]);n='primary-%d-%d'%(a,z);(O/(n+'.raw')).write_bytes(f);(O/(n+'.lf')).write_bytes(f.replace(b'\r\n',b'\n'));selected.append(dict(physical_lines1=[a,z],raw_sha256=hashlib.sha256(f).hexdigest(),lf_sha256=hashlib.sha256(f.replace(b'\r\n',b'\n')).hexdigest(),raw_snapshot=n+'.raw',lf_snapshot=n+'.lf'))
(O/'primary-bindings.json').write_text(json.dumps(dict(path=str(p),whole_raw_sha256=hashlib.sha256(b).hexdigest(),whole_lf_sha256=hashlib.sha256(b.replace(b'\r\n',b'\n')).hexdigest(),whole_bytes=len(b),selected_source_fragments=selected,scope='Source truth boundary confirmation only; not topology self-review, primary already read before49candidate in original preread'),indent=2)+'\n',encoding='utf-8')
print('EXACT HEADER MATCH',len(header.encode('utf-8')))
