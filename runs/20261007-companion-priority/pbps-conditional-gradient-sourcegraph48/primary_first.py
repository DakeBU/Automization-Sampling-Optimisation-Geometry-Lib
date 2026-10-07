# -*- coding: utf-8 -*-
from pathlib import Path
import json,hashlib,datetime,re,html,sys
sys.stdout.reconfigure(encoding='utf-8')
R=Path('E:/Samplinglib');O=R/'runs/20261007-companion-priority/pbps-conditional-gradient-sourcegraph48'
def sha(b):return hashlib.sha256(b).hexdigest()
def lf(b):return b.replace(b'\r\n',b'\n').replace(b'\r',b'\n')
lease=json.loads((O/'lease.json').read_text(encoding='utf-8-sig'));assert lease['state']=='OPEN'
(O/'lease.open.raw.snapshot.json').write_bytes((O/'lease.json').read_bytes())
prior=R/'runs/20261007-companion-priority/next-ready-preread47'
pins=[]
for name in ['sourcecontract.json','input-bindings.json','source-detail.json']:
 b=(prior/name).read_bytes();(O/('prior47-'+name)).write_bytes(b);pins.append(dict(path=str(prior/name).replace('\\','/'),raw_sha256=sha(b),lf_sha256=sha(lf(b))))
p=prior/'primary-pbps.raw.snapshot.html';raw=p.read_bytes();assert sha(raw)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
rows=raw.splitlines(keepends=True)
ranges=[(348,363),(615,652),(668,695),(4566,4653)]
for a,b in ranges:
 fragment=b''.join(rows[a-1:b]);name='primary-%d-%d'%(a,b);(O/(name+'.raw.html')).write_bytes(fragment);(O/(name+'.lf.html')).write_bytes(lf(fragment))
 pins.append(dict(id=name,path=str(p).replace('\\','/'),whole_raw_sha256=sha(raw),whole_lf_sha256=sha(lf(raw)),physical_ranges=[[a,b]],fragment_raw_sha256=sha(fragment),fragment_lf_sha256=sha(lf(fragment)),raw_bytes=len(fragment)))
 text=fragment.decode('utf-8');text=re.sub(r'<math\b[^>]*alttext="([^"]*)"[^>]*>.*?</math>',lambda m:' '+html.unescape(m.group(1))+' ',text,flags=re.S);text=html.unescape(re.sub('<[^>]+>',' ',text));print('PRIMARY',a,b,re.sub(r'\s+',' ',text))
contract=dict(schema_version=1,stage='48 actual source-before-target record',actor='gaussian_noncompact_preread_42',created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),own_lease_opened_before_reads=lease['opened_at_utc'],primary='arxiv:2609.06905v1',pins=pins,candidate_text_read=False,implementation_read=False,compiler_used=False,prior_exposure='Historical41 metadata/decoder-binding original_text, shared32snippet,44metadata,46provider snippets and47current45status/path metadata were explicitly recorded earlier; not fresh blind.',source_boundary='Pointwise A3.Ex7 only; source C.2 formula/integrated bound and subsection C.2 halfturn are outside target.')
(O/'source-before-target.contract.json').write_bytes((json.dumps(contract,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
(O/'primary-input-bindings.json').write_bytes((json.dumps(pins,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
