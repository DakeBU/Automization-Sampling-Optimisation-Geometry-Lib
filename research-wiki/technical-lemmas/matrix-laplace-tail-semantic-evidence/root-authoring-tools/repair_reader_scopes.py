from pathlib import Path
import json, subprocess
r=Path.cwd();w=r/'.astis/huanjian-gc-matrix-laplace-20261114'
p=r/'website/content/declaration_lessons/huanjian-matrix-laplace-tail.json'
before=p.read_bytes();(w/'lesson.authored-v1.before-source-scope-repair.json').write_bytes(before)
x=json.loads(before); ss=x['units'][0]['sources']
scopes={
'AutoSamplingTheory/TechnicalLemmas/Probability/MatrixLaplaceTail.lean':'Exact complete public probability-tail theorem, with its matrix and measure semantics.',
'Tests/GaussianComplexityLaplaceTail.lean':'Associated private original-Gaussian four-family consumer; no separate public node.',
'A3.Ex85':'Literal feature vectors and row coordinates used in the private consumer.',
'A3.SS2.p1.2':'Original unconditional product-Gaussian row experiment.',
'A3.SS2.p4.1':'Physical-row midpoint angles used in the cosine weights and feature vectors.',
'A3.SS2.p10.1':'Exact cutoff threshold L and physical-row squared norm.',
'A3.Ex107':'Inclusive own-row truncated rank-one Kronecker definition.',
'A3.SS2.p13.1':'Actual unconditional centering Zi=Yi−EYi.',
'A3.Ex112':'Previously compiled source radius and actual-mean norm bounds, reused internally.',
'A3.Ex121':'Source strict norm tail context; the complete two-sided norm/union bridge remains deferred.',
'A3.SS2.p15.2':'Cosine-weighted concentration context; the full Bernstein MGF/tail estimate remains deferred.'}
for s in ss:
    if 'scope' in s: continue
    key=s.get('path') or s['url'].split('#')[-1]
    s['scope']=scopes[key]
p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
script=(w/'prepare_reader_preview.py').read_text()
assert script.count("new=w/'reader-preview-v1'")==1
(w/'prepare_reader_preview.v2.py').write_text(script.replace("new=w/'reader-preview-v1'","new=w/'reader-preview-v2'"))
subprocess.run(['python3',str(w/'prepare_reader_preview.v2.py')],check=True)
subprocess.run(['python3',str(w/'prepare_review_packets.py')],check=True)
