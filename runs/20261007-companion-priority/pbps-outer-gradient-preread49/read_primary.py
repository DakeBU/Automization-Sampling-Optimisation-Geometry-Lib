# -*- coding: utf-8 -*-
import pathlib, re,sys,hashlib,json
sys.stdout.reconfigure(encoding='utf-8')
r=pathlib.Path('E:/Samplinglib');d=r/'runs/20261007-companion-priority/pbps-outer-gradient-preread49';p=r/'runs/20261007-companion-priority/next-ready-preread47/primary-pbps.raw.snapshot.html';b=p.read_bytes();H=lambda b:hashlib.sha256(b).hexdigest();assert H(b)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760';lines=b.splitlines(keepends=True)
for name,a,z in [('outer-C2',4644,4679),('B13-search-region',3750,3890)]:
 part=b''.join(lines[a-1:z]);(d/(name+'.raw.html')).write_bytes(part);(d/(name+'.lf.html')).write_bytes(part.replace(b'\r\n',b'\n'));print(name,a,z);print(part.decode('utf-8'))
