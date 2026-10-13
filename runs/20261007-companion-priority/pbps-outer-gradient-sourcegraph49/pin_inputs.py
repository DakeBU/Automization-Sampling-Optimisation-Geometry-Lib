# -*- coding: utf-8 -*-
import pathlib,json,hashlib,re,sys
sys.stdout.reconfigure(encoding='utf-8');r=pathlib.Path('E:/Samplinglib');d=r/'runs/20261007-companion-priority/pbps-outer-gradient-sourcegraph49';H=lambda b:hashlib.sha256(b).hexdigest();inp=[];sel=[]
def pin(path,name,a=None,z=None,fragment=None,kind='metadata'):
 p=r/path;b=p.read_bytes();lf=b.replace(b'\r\n',b'\n'); part=b if fragment is None else fragment
 if a is not None and fragment is None:part=b''.join(b.splitlines(keepends=True)[a-1:z])
 (d/(name+'.raw')).write_bytes(part);(d/(name+'.lf')).write_bytes(part.replace(b'\r\n',b'\n'))
 rec=dict(id=name,path=str(p),kind=kind,whole_raw_sha256=H(b),whole_lf_sha256=H(lf),whole_bytes=len(b),fragment_raw_sha256=H(part),fragment_lf_sha256=H(part.replace(b'\r\n',b'\n')),fragment_bytes=len(part),snapshot=name)
 if a is not None:rec['physical_lines1']=[a,z]
 inp.append(rec);return rec
for name,path in [('target','runs/20261007-companion-priority/pbps-outer-gradient-preproof49/prospective-statement.txt'),('proposal','runs/20261007-companion-priority/pbps-outer-gradient-preproof49/root.statement-proposal.json'),('phase-primary-contract','runs/20261007-companion-priority/phase-pbps-primary-preread49/primary.contract.json'),('phase-primary-lease','runs/20261007-companion-priority/phase-pbps-primary-preread49/reviewer.primary.lease.json'),('historical-preread-contract','runs/20261007-companion-priority/pbps-outer-gradient-preread49/sourcecontract.json'),('historical-preread-detail','runs/20261007-companion-priority/pbps-outer-gradient-preread49/source-detail.md'),('historical-preread-lease','runs/20261007-companion-priority/pbps-outer-gradient-preread49/lease.json')]:pin(path,name,kind='target' if name=='target' else 'chronology-and-public-metadata')
assert inp[0]['fragment_lf_sha256']=='f37b4a07e62e16d22f4ecbc1fba9c38fd80d42f947011b38ded7c5153e0bea1d'
for name in ['phase-primary-lease','historical-preread-lease']:
 o=json.loads((d/(name+'.raw')).read_bytes().decode('utf-8-sig'));print(name,o)
# Exact current three opaque public producers, no parent body semantic reads.
for mod,decl in [('ConditionalGradientVariance','reflected_conditional_gradient_variance'),('GibbsAugmentation','normalized_augmentation_density'),('GaussianReflection','reflection_preserves_augmentation')]:
 path='AutoSamplingTheory/ExampleCases/ProximalBPS/'+mod+'.lean';b=(r/path).read_bytes();m=re.search(rb'^theorem\s+'+decl.encode()+rb'\b',b,re.M);a=m.start();z=b.index(b':= by',a);part=b[a:z];start=b[:a].count(b'\n')+1;end=b[:z].count(b'\n')+1;rec=pin(path,'parent-'+mod, start,end,part,'opaque-verified-public-header');rec['header_end_before_proof']=True;rec['declaration']='AutoSamplingTheory.ExampleCases.ProximalBPS.'+mod+'.'+decl;sel.append(rec)
# Check exact primitive public contracts; let-free selected declarations end before proof :=.
api=[('Kernel/Disintegration/Basic','class IsCondKernel','P.disintegration',58,59),('Kernel/Disintegration/Basic','lemma disintegrate','P.disintegrate',63,63),('Kernel/Composition/IntegralCompProd','lemma integrable_compProd_iff','P.fubini-domain',461,466),('Kernel/Composition/IntegralCompProd','lemma integral_compProd','P.fubini',469,473),('Kernel/MeasurableIntegral','theorem StronglyMeasurable.integral_kernel','P.kernel-meas',56,57),('Kernel/MeasurableIntegral','theorem StronglyMeasurable.integral_kernel_prod_right','P.kernel-prod-meas',79,81)]
for file,decl,key,a,z in api:
 path='.lake/packages/mathlib/Mathlib/Probability/'+file+'.lean';b=(r/path).read_bytes();part=b''.join(b.splitlines(keepends=True)[a-1:z]); assert decl.encode() in part
 if b':=' in part and 'class' not in decl:part=part[:part.index(b':=')]
 sel.append(pin(path,'api-'+key,a,z,part,'primitive-public-contract'))
other=[('Analysis/Calculus/FDeriv/Measurable','theorem measurable_fderiv','P.fderiv-meas',380,380),('MeasureTheory/Function/L1Space/Integrable','theorem Integrable.mono_nonneg','P.domination',91,95),('MeasureTheory/Integral/Bochner/Basic','lemma integral_mono_ae','P.integral-order',627,629),('MeasureTheory/Integral/Bochner/Basic','theorem integral_map','P.map-integral',1043,1045),('MeasureTheory/Function/LpSeminorm/Basic','theorem MemLp.of_bound','P.bounded-Lp',549,551),('MeasureTheory/Function/L2Space','theorem memLp_two_iff_integrable_sq_norm','P.gradient-L2',45,47),('Probability/Moments/Variance','lemma variance_eq_integral','P.var-integral',155,156),('Probability/Moments/Variance','theorem variance_eq_sub','P.var-sub',224,226),('MeasureTheory/Measure/Tilted','lemma isProbabilityMeasure_tilted','P.tilt-prob',126,127)]
for file,decl,key,a,z in other:
 path='.lake/packages/mathlib/Mathlib/'+file+'.lean';b=(r/path).read_bytes();part=b''.join(b.splitlines(keepends=True)[a-1:z]);assert decl.encode() in part,(key,part)
 if b':=' in part:part=part[:part.index(b':=')]
 sel.append(pin(path,'api-'+key,a,z,part,'primitive-public-contract'))
for key,path,a,z in [('D.variance','AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/Poincare.lean',28,29),('D.gradient','.lake/packages/mathlib/Mathlib/Analysis/Calculus/Gradient/Basic.lean',82,83),('D.tilt','.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Tilted.lean',42,43),('P.fderiv-context','.lake/packages/mathlib/Mathlib/Analysis/Calculus/FDeriv/Measurable.lean',104,109),('P.fderiv-context2','.lake/packages/mathlib/Mathlib/Analysis/Calculus/FDeriv/Measurable.lean',358,370),('P.markov','.lake/packages/mathlib/Mathlib/Probability/Kernel/Defs.lean',145,147),('P.markov-instance','.lake/packages/mathlib/Mathlib/Probability/Kernel/Defs.lean',211,213)]:sel.append(pin(path,'selected-'+key,a,z,kind='definition-or-typing-contract'))
(d/'input-bindings.json').write_text(json.dumps(inp,indent=2),encoding='utf-8');(d/'selected-providers.json').write_text(json.dumps(sel,indent=2),encoding='utf-8');print('selected providers',len(sel),'inputs',len(inp))
