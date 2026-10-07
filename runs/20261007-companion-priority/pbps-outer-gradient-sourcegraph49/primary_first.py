# -*- coding: utf-8 -*-
import pathlib,json,hashlib,datetime,sys,re,html
sys.stdout.reconfigure(encoding='utf-8');r=pathlib.Path('E:/Samplinglib');d=r/'runs/20261007-companion-priority/pbps-outer-gradient-sourcegraph49';p=r/'runs/20261007-companion-priority/next-ready-preread47/primary-pbps.raw.snapshot.html';b=p.read_bytes();H=lambda b:hashlib.sha256(b).hexdigest();assert H(b)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760';lines=b.splitlines(keepends=True);ranges=[('standing',348,360),('actual-law',615,647),('B8B9',3714,3735),('B13-residual',3761,3786),('compact-scope',4573,4576),('Ex7-parent',4644,4653),('outerC2',4654,4665)]
for n,a,z in ranges:
 part=b''.join(lines[a-1:z]);(d/(n+'.raw.html')).write_bytes(part);(d/(n+'.lf.html')).write_bytes(part.replace(b'\r\n',b'\n'));print(n,a,z)
 for k,line in enumerate(part.decode().splitlines(),a):
  tex=re.findall(r'<annotation encoding="application/x-tex">(.*?)</annotation>',line)
  if tex:print(k,html.unescape(' ; '.join(tex)))
contract=dict(status='SOURCE_READ_BEFORE_PROSPECTIVE49_CANDIDATE',recorded_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),primary_path=str(p),primary_raw_sha256=H(b),primary_lf_sha256=H(b.replace(b'\r\n',b'\n')),selected_ranges=ranges,known48proof_exposure=True,implementation49_exists=False,prospective49_not_yet_read=True,preread49_contract_sha256=H((r/'runs/20261007-companion-priority/pbps-outer-gradient-preread49/sourcecontract.json').read_bytes()))
(d/'source-before-candidate.contract.json').write_text(json.dumps(contract,indent=2),encoding='utf-8')

