# -*- coding: utf-8 -*-
from pathlib import Path
import sys,json,re,hashlib
sys.stdout.reconfigure(encoding='utf-8')
R=Path('E:/Samplinglib');O=R/'runs/20261007-companion-priority/pbps-outer-gradient-energy/whole-proof-review49'
def sha(b):return hashlib.sha256(b).hexdigest()
def lf(b):return b.replace(b'\r\n',b'\n')
def write(n,v):(O/n).write_bytes((json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
api_specs=[('bochner', 'MeasureTheory/Integral/Bochner/Basic.lean',[(202,202),(261,264),(620,630),(966,967),(1032,1033)]),('variance','Probability/Moments/Variance.lean',[(151,156),(224,226)]),('disintegration','Probability/Kernel/Disintegration/Basic.lean',[(56,63)]),('prod','MeasureTheory/Measure/Prod.lean',[(1209,1210)]),('fubini','Probability/Kernel/Composition/IntegralCompProd.lean',[(469,472)]),('Lp-bound','MeasureTheory/Function/LpSeminorm/Basic.lean',[(549,551)]),('L2','MeasureTheory/Function/L2Space.lean',[(42,47)]),('kernel-mean','Probability/Kernel/MeasurableIntegral.lean',[(50,57)]),('tilt','MeasureTheory/Measure/Tilted.lean',[(42,43),(126,127)]),('map-prob','MeasureTheory/Measure/Typeclasses/Probability.lean',[(124,125)]),('grad','Analysis/Calculus/Gradient/Basic.lean',[(82,83)]),('fderiv-meas','Analysis/Calculus/FDeriv/Measurable.lean',[(106,109),(358,359),(370,370),(379,380)]),('domination','MeasureTheory/Function/L1Space/Integrable.lean',[(91,95)]),('compact-bound-generated','Topology/Order/Compact.lean',[(338,348)])]
api=[]
for id,rel,ranges in api_specs:
 p=R/'.lake/packages/mathlib/Mathlib'/rel;b=p.read_bytes();lines=b.splitlines(keepends=True);frags=[]
 for k,(a,z) in enumerate(ranges):
  f=b''.join(lines[a-1:z]);stem='api-'+id+'-'+str(k);(O/(stem+'.raw')).write_bytes(f);(O/(stem+'.lf')).write_bytes(lf(f));frags.append(dict(physical_lines1=[a,z],byte_interval0=[len(b''.join(lines[:a-1])),len(b''.join(lines[:z]))],raw_sha256=sha(f),lf_sha256=sha(lf(f)),raw_snapshot=stem+'.raw',lf_snapshot=stem+'.lf'))
 api.append(dict(id=id,path=str(p),whole_raw_sha256=sha(b),whole_lf_sha256=sha(lf(b)),whole_bytes=len(b),selected_fragments=frags,semantic_scope='Exact relevant contracts/definitions or generator context; compiled Mathlib internals trusted, not independently recompiled here'))
write('mathlib-api-bindings.json',api)
# Compare the original sourcegraph provider pins; current review is not graph self-admission.
old=json.loads((R/'runs/20261007-companion-priority/pbps-outer-gradient-sourcegraph49/selected-providers.json').read_text(encoding='utf-8'));matching=[]
for x in old:
 b=Path(x['path']).read_bytes();assert sha(b)==x['whole_raw_sha256'] and sha(lf(b))==x['whole_lf_sha256'],x['id'];matching.append(dict(id=x['id'],path=x['path'],current_raw_sha256=sha(b),current_lf_sha256=sha(lf(b)),unchanged=True))
write('unchanged-parent-api-checks.json',matching)
# Static import-reachable ASTIS scan; does not claim an exported kernel declaration graph.
root='AutoSamplingTheory.ExampleCases.ProximalBPS.ConditionalGradientEnergy';todo=[root];seen={};hits=[]
pattern=re.compile(r'\b(sorry|admit|sorryAx)\b|^\s*(?:unsafe\s+)?axiom\s|Prop\s*:=\s*True|:=\s*trivial',re.M)
while todo:
 module=todo.pop()
 if module in seen:continue
 p=R/(module.replace('.','/')+'.lean');b=p.read_bytes();s=b.decode('utf-8');im=re.findall(r'(?m)^\s*(?:public\s+)?import\s+(\S+)',s)
 seen[module]=dict(module=module,path=str(p),raw_sha256=sha(b),lf_sha256=sha(lf(b)),imports=im,inspection_scope='automated imports/forbidden-token scan; semantic expansion only new file and explicitly reviewed direct parents')
 for m in pattern.finditer(s):hits.append(dict(module=module,path=str(p),physical_line1=s[:m.start()].count('\n')+1,text=s[m.start():m.end()],line=s.splitlines()[s[:m.start()].count('\n')]))
 todo += [x for x in im if x.startswith('AutoSamplingTheory.')]
write('astis-import-reachability.json',dict(scope='Bounded transitive ASTIS import closure of target; module scan is not exact proof-term declaration extraction',root=root,module_count=len(seen),modules=list(seen.values()),raw_forbidden_hits=hits))
print('ASTIS_MODULES',len(seen),'HITS',json.dumps(hits,ensure_ascii=False))
# Exact frozen public header, all new declaration bodies and test axiom output.
s=(R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ConditionalGradientEnergy.lean').read_text(encoding='utf-8');header=s[s.index('theorem reflected_conditional_gradient_energy'):s.index(' := by',s.index('theorem reflected_conditional_gradient_energy'))]
sealed=(R/'runs/20261007-companion-priority/pbps-outer-gradient-preproof49/prospective-statement.txt').read_text(encoding='utf-8')
# The prospective file includes := by marker? Print exact lengths before choosing literal comparison.
print('HEADER',len(header.encode('utf-8')),'SEALED',len(sealed.encode('utf-8')),'SEALED_END',repr(sealed[-30:]))
print('GENERATED COMPACT', '\n'.join((R/'.lake/packages/mathlib/Mathlib/Topology/Order/Compact.lean').read_text(encoding='utf-8').splitlines()[337:349]))
log=(R/'runs/20261007-companion-priority/pbps-outer-gradient-energy/tests.1.log').read_text(encoding='utf-8');axioms=[]
for m in re.finditer(r"'([^']+)' depends on axioms: \[([^]]*)\]",log,re.S):
 ax=[a.strip() for a in m.group(2).split(',')];assert sorted(ax)==sorted(['propext','Classical.choice','Quot.sound']);axioms.append(dict(declaration=m.group(1),axioms=ax,physical_log_line1=log[:m.start()].count('\n')+1))
assert len(axioms)==3;write('axiom-evidence.json',dict(reused_compiler_log=True,reviewer_compiler_used=False,log_path='runs/20261007-companion-priority/pbps-outer-gradient-energy/tests.1.log',declarations=axioms,sorryAx_present=False,scope='Actual target and two test closures; includes transitively reachable proof terms in those compiled declarations'))
