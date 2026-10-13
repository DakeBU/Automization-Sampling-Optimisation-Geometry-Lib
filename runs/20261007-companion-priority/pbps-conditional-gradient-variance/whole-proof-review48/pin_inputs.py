# -*- coding: utf-8 -*-
import pathlib, hashlib, json, datetime, re
root=pathlib.Path('E:/Samplinglib'); out=root/'runs/20261007-companion-priority/pbps-conditional-gradient-variance/whole-proof-review48'
sysfiles=['AutoSamplingTheory/ExampleCases/ProximalBPS/ConditionalGradientVariance.lean','AutoSamplingTheory/ExampleCases/ProximalBPS/ConditionalScore.lean','AutoSamplingTheory/ExampleCases/ProximalBPS/ConditionalScoreVariance.lean','AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/Poincare.lean','runs/20261007-companion-priority/pbps-conditional-gradient-variance/claim.json','runs/20261007-companion-priority/pbps-conditional-gradient-variance/focused.1.lean','runs/20261007-companion-priority/pbps-conditional-gradient-variance/focused.1.log','runs/20261007-companion-priority/pbps-conditional-gradient-variance/focused.1.status.json','runs/20261007-companion-priority/pbps-conditional-gradient-preproof48/prospective-statement.txt','runs/20261007-companion-priority/pbps-conditional-gradient-preproof48/statement-seals.accepted.json']
H=lambda b:hashlib.sha256(b).hexdigest(); bindings=[]
for i,p in enumerate(sysfiles):
 b=(root/p).read_bytes(); lf=b.replace(b'\r\n',b'\n'); stem='input.%02d'%i
 (out/(stem+'.raw')).write_bytes(b); (out/(stem+'.lf')).write_bytes(lf)
 bindings.append(dict(path=p,raw_bytes=len(b),raw_sha256=H(b),lf_bytes=len(lf),lf_sha256=H(lf),snapshot=stem))
(out/'input-bindings.json').write_text(json.dumps(bindings,indent=2),encoding='utf-8')
prod=(root/sysfiles[0]).read_bytes(); snap=(root/sysfiles[5]).read_bytes(); status=json.loads((root/sysfiles[7]).read_text(encoding='utf-8-sig'))
assert prod==snap and H(prod)==status['source_raw_sha256']
assert status['exit_code']==0 and H((root/sysfiles[6]).read_bytes())==status['log_raw_sha256']
s=prod.decode('utf-8').replace('\r\n','\n'); a=s.index('theorem reflected_conditional_gradient_variance'); z=s.index(' := by',a)
header=s[a:z]; target=(root/sysfiles[8]).read_text(encoding='utf-8-sig').replace('\r\n','\n').strip()
(out/'production-header.txt').write_bytes((header+'\n').encode())
# Exact statement whitespace-normalized comparison only; immutable bytes remain separately pinned.
assert re.sub(r'\s+',' ',header).strip()==re.sub(r'\s+',' ',target).strip()
# Source-level reachable local import graph, not elaborated declaration dependency or axiom closure.
seen={}; queue=[sysfiles[0]]; findings=[]
while queue:
 p=queue.pop()
 if p in seen:continue
 b=(root/p).read_bytes(); t=b.decode('utf-8-sig'); imps=re.findall(r'^import (\S+)',t,re.M); seen[p]=dict(raw_sha256=H(b),lf_sha256=H(b.replace(b'\r\n',b'\n')),imports=imps)
 for k,line in enumerate(t.splitlines(),1):
  if re.search(r'\b(sorry|admit|axiom)\b|Prop\s*:=\s*True|:=\s*trivial',line):findings.append(dict(path=p,line=k,text=line))
 for m in imps:
  q=m.replace('.','/')+'.lean'
  if m.startswith('AutoSamplingTheory.') and (root/q).is_file():queue.append(q)
(out/'reachable-local-imports.json').write_text(json.dumps(seen,indent=2),encoding='utf-8')
(out/'fake-closure-lexical-findings.json').write_text(json.dumps(findings,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps(dict(frozen_production_matches_focused1=True,statement_normalized_matches_seal=True,local_imports=len(seen),lexical_hits=len(findings),findings=findings),ensure_ascii=True))
