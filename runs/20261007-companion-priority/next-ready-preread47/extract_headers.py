# -*- coding: utf-8 -*-
from pathlib import Path
import re,json,hashlib,sys
sys.stdout.reconfigure(encoding='utf-8')
R=Path('E:/Samplinglib');O=R/'runs/20261007-companion-priority/next-ready-preread47'
assert json.loads((O/'lease.json').read_text(encoding='utf-8-sig'))['state']=='OPEN'
def sha(x):return hashlib.sha256(x).hexdigest()
apis=[]
for sid,file,name in [
 ('score','AutoSamplingTheory/ExampleCases/ProximalBPS/ConditionalScore.lean','reflected_conditional_covariance'),
 ('variance','AutoSamplingTheory/ExampleCases/ProximalBPS/ConditionalScoreVariance.lean','conditional_centered_domain_and_score_variance'),
 ('macro','AutoSamplingTheory/ExampleCases/ProximalBPS/MacroscopicRepresentative.lean','macroscopic_reflection_smooth_representative'),
 ('reflection','AutoSamplingTheory/ExampleCases/ProximalBPS/ReflectionL2.lean','actual_reflection_block_identities'),
]:
 raw=(R/file).read_bytes();text=raw.decode('utf-8');m=re.search(r'^theorem '+re.escape(name)+r'\b',text,re.M);assert m,(file,name)
 a=m.start();proof=re.search(r':=\s*by\b',text[a:]);assert proof,(file,name)
 b=a+proof.start();first=text[:a].count('\n')+1;last=text[:b].count('\n')+1;header=text[a:b].encode('utf-8');lf=header.replace(b'\r\n',b'\n')
 for suffix in ['raw','lf']:
  p=O/(sid+'.public.'+suffix+'.txt')
  if p.exists() and not (O/(sid+'.truncated-first-coloneq.'+suffix+'.txt')).exists():p.rename(O/(sid+'.truncated-first-coloneq.'+suffix+'.txt'))
 (O/(sid+'.public.raw.txt')).write_bytes(header);(O/(sid+'.public.lf.txt')).write_bytes(lf)
 apis.append(dict(id=sid,path=file,declaration=name,raw_sha256=sha(header),lf_sha256=sha(lf),whole_raw_sha256=sha(raw),whole_lf_sha256=sha(raw.replace(b'\r\n',b'\n')),physical_span=[first,last],proof_body_read=False))
 print(sid,first,last,lf.decode('utf-8'))
(O/'public-input-bindings.json').write_bytes((json.dumps(apis,indent=2)+'\n').encode())
