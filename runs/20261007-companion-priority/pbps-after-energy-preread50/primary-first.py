# -*- coding: utf-8 -*-
from pathlib import Path
import sys,json,hashlib,re
sys.stdout.reconfigure(encoding='utf-8');R=Path('E:/Samplinglib');O=R/'runs/20261007-companion-priority/pbps-after-energy-preread50';P=R/'runs/20261007-companion-priority/next-ready-preread47/primary-pbps.raw.snapshot.html';b=P.read_bytes();assert hashlib.sha256(b).hexdigest()=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760';rows=b.splitlines(keepends=True);pins=[]
for a,z in [(3714,3735),(3777,3786),(4567,4576),(4646,4665)]:
 f=b''.join(rows[a-1:z]);s='primary-%d-%d'%(a,z);(O/(s+'.raw')).write_bytes(f);(O/(s+'.lf')).write_bytes(f.replace(b'\r\n',b'\n'));pins.append(dict(path=str(P),whole_raw_sha256=hashlib.sha256(b).hexdigest(),whole_lf_sha256=hashlib.sha256(b.replace(b'\r\n',b'\n')).hexdigest(),whole_bytes=len(b),selected_physical_lines1=[a,z],fragment_raw_sha256=hashlib.sha256(f).hexdigest(),fragment_lf_sha256=hashlib.sha256(f.replace(b'\r\n',b'\n')).hexdigest(),raw_snapshot=s+'.raw',lf_snapshot=s+'.lf'));print('\nPRIMARY',a,z);print(re.sub('<[^>]+>',' ',f.decode('utf-8')))
(O/'primary-first.bindings.json').write_text(json.dumps(pins,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
