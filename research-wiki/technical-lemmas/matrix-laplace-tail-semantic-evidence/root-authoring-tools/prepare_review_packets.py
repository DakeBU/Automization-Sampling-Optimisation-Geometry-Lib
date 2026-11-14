from pathlib import Path
import json, subprocess, hashlib
r=Path.cwd(); w=r/'.astis/huanjian-gc-matrix-laplace-20261114'
cmd=['python3','tools/astis_publication.py','review-context','--item','huanjian-matrix-laplace-tail','--declaration','AutoSamplingTheory.TechnicalLemmas.Probability.MatrixLaplaceTail.max_eigenvalue_tail_le_iInf_trace_exp']
raw=subprocess.check_output(cmd)
(w/'publication-context.v1.json').write_bytes(raw)
ctx=json.loads(raw)
p=r/'research-wiki/semantic-roundtrip/audits/huanjian-matrix-laplace-tail.json'
a=json.loads(p.read_text())
a['publication_binding_sha256']=ctx['publication_binding_sha256']
a['publication_context']=ctx['publication_context']
p.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n')
custom=w/'private-consumer-audit.registry.json'
reg=json.loads(custom.read_text()); t=reg['audits'][0]
t['publication_binding_sha256']=ctx['publication_binding_sha256']
t['publication_context']=ctx['publication_context']
t['private_module_context']={'file':'Tests/GaussianComplexityLaplaceTail.lean',
 'commit':'1d1103af694b9663a72b0d610004ed85c7c6b527',
 'sha256':hashlib.sha256((r/'Tests/GaussianComplexityLaplaceTail.lean').read_bytes()).hexdigest(),
 'text':(r/'Tests/GaussianComplexityLaplaceTail.lean').read_text()}
custom.write_text(json.dumps(reg,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'binding_sha256':ctx['publication_binding_sha256'],'context_file':str((w/'publication-context.v1.json').relative_to(r))}))
