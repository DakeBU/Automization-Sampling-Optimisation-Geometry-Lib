# -*- coding: utf-8 -*-
import pathlib,re,html,json,hashlib,sys
sys.stdout.reconfigure(encoding='utf-8');r=pathlib.Path('E:/Samplinglib');d=r/'runs/20261007-companion-priority/pbps-outer-gradient-preread49';p=r/'runs/20261007-companion-priority/next-ready-preread47/primary-pbps.raw.snapshot.html';b=p.read_bytes();lines=b.splitlines(keepends=True);H=lambda b:hashlib.sha256(b).hexdigest();more=[]
for stem,a,z in [('P-U-definitions',3518,3569),('U-unitarity',3571,3636),('compact-reduction-exact',4573,4577)]:
 part=b''.join(lines[a-1:z]);(d/(stem+'.raw.html')).write_bytes(part);(d/(stem+'.lf.html')).write_bytes(part.replace(b'\r\n',b'\n'));more.append(dict(name=stem,path=str(p),span=[a,z],whole_raw_sha256=H(b),whole_lf_sha256=H(b.replace(b'\r\n',b'\n')),fragment_raw_sha256=H(part),fragment_lf_sha256=H(part.replace(b'\r\n',b'\n'))))
 for k,line in enumerate(part.decode().splitlines(),a):
  tx=re.findall(r'<annotation encoding="application/x-tex">(.*?)</annotation>',line)
  if tx:print(k,html.unescape(' ; '.join(tx)))
  elif '<p ' in line:print(k,html.unescape(re.sub(r'<[^>]+>',' ',line))[:1000])
for k,line in enumerate(lines[4565:4896],4566):
 if any(w in line.decode() for w in ['density','closedness','approximation']):print('ROUGH-MENTION',k,html.unescape(re.sub(r'<[^>]+>',' ',line.decode()))[:1500])
(d/'primary-additional-bindings.json').write_text(json.dumps(more,indent=2),encoding='utf-8')
