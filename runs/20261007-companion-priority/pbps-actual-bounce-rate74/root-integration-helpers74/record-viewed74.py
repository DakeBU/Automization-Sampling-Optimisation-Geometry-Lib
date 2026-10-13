from pathlib import Path
import hashlib,json,os
r=Path('runs/20261007-companion-priority/pbps-actual-bounce-rate74');folders=[Path('.astis/pbps-bounce74/visual74-cdp'),Path('.astis/pbps-bounce74/visual74-copy')]
paths=[p for d in folders for p in sorted(d.glob('*.png'))];assert len(paths)==10
rows=[]
for p in paths:
 b=p.read_bytes();rows.append(dict(path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=hashlib.sha256(b).hexdigest()))
out=r/'root.viewed-captures74.json';assert not out.exists()
out.write_text(json.dumps(dict(status='ROOT_ACTUALLY_VIEWED_TEN_CURRENT_CAPTURES',actual_root_PID=os.getpid(),viewed_by_root=True,images=rows,scope='One statement/seven BODY formula steps/actual branch plus isolated copy/download page. Layout and math inspected; bounded dense graph/plain notation debt remains; no full Exposition Seal or live claim.',full_Exposition_Seal=False,PURIFIED=False,Goal_complete=False),indent=2)+'\n',encoding='utf8',newline='\n')
print('PASS74 root actual ten-PNG visual inspection recorded; no whole-reader or theorem credit.')
