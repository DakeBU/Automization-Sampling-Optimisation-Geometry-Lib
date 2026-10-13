# -*- coding: utf-8 -*-
import pathlib,json,hashlib,re,sys
sys.stdout.reconfigure(encoding='utf-8')
r=pathlib.Path('E:/Samplinglib'); d=r/'runs/20261007-companion-priority/pbps-conditional-gradient-variance/whole-proof-review48'; H=lambda b:hashlib.sha256(b).hexdigest()
closure=json.loads((d/'reachable-local-imports.json').read_text()); sd=d/'reachable-snapshots';sd.mkdir(exist_ok=True)
for i,(p,v) in enumerate(sorted(closure.items())):
 b=(r/p).read_bytes();assert H(b)==v['raw_sha256'];(sd/('%03d.raw'%i)).write_bytes(b);(sd/('%03d.lf'%i)).write_bytes(b.replace(b'\r\n',b'\n'));v['snapshot']='reachable-snapshots/%03d'%i
(d/'reachable-local-imports.json').write_text(json.dumps(closure,indent=2),encoding='utf-8')
api=[('Mathlib/Probability/Moments/Covariance.lean',38,67),('Mathlib/MeasureTheory/Function/L2Space.lean',38,56),('Mathlib/MeasureTheory/Function/L2Space.lean',125,142),('Mathlib/Analysis/Calculus/Gradient/Basic.lean',278,299),('Mathlib/MeasureTheory/Integral/Bochner/ContinuousLinearMap.lean',64,81),('Mathlib/Probability/Kernel/Defs.lean',143,147),('Mathlib/Probability/Kernel/Defs.lean',211,213),('Mathlib/Analysis/InnerProductSpace/Basic.lean',277,286)]
bind=[]
for i,(p,a,z) in enumerate(api):
 full=r/'.lake/packages/mathlib'/p;b=full.read_bytes();lines=b.splitlines(keepends=True);part=b''.join(lines[a-1:z]);stem='api.%02d'%i;(d/(stem+'.raw')).write_bytes(part);(d/(stem+'.lf')).write_bytes(part.replace(b'\r\n',b'\n'))
 bind.append(dict(path=str(full),span=[a,z],whole_raw_sha256=H(b),whole_lf_sha256=H(b.replace(b'\r\n',b'\n')),fragment_raw_sha256=H(part),fragment_lf_sha256=H(part.replace(b'\r\n',b'\n')),snapshot=stem))
(d/'api-bindings.json').write_text(json.dumps(bind,indent=2),encoding='utf-8')
t=(r/'AutoSamplingTheory/ExampleCases/ProximalBPS/ConditionalGradientVariance.lean').read_text(encoding='utf-8');
for i,l in enumerate(t.splitlines(),1):
 if any(s in l for s in ['have hSS','subst S','let : IsMarkov','have hf2','have hYc2','have hY2','have hpair','have hcs','have hcov','have hnorm','have hbound','by_cases hz','have hp','mul_le_mul_iff_right']):print(i,l.strip())
