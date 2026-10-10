# -*- coding: utf-8 -*-
from pathlib import Path
import re,json,hashlib,sys
sys.stdout.reconfigure(encoding='utf-8')
R=Path('E:/Samplinglib');O=R/'runs/20261007-companion-priority/next-ready-preread47'
def sha(b):return hashlib.sha256(b).hexdigest()
def lf(b):return b.replace(b'\r\n',b'\n').replace(b'\r',b'\n')
assert json.loads((O/'lease.json').read_text(encoding='utf-8-sig'))['state']=='OPEN'
items=[]
def slice_pin(sid,path,ranges,kind):
 raw=(R/path).read_bytes();rows=raw.splitlines(keepends=True);b=b''.join(b''.join(rows[a-1:z]) for a,z in ranges)
 (O/(sid+'.raw.txt')).write_bytes(b);(O/(sid+'.lf.txt')).write_bytes(lf(b));items.append(dict(id=sid,path=path,kind=kind,physical_ranges=ranges,whole_raw_sha256=sha(raw),raw_sha256=sha(b),lf_sha256=sha(lf(b)),raw_bytes=len(b)))
for sid,path,ranges in [
 ('primary-pbps-standing','runs/20261007-companion-priority/next-ready-preread47/primary-pbps.raw.snapshot.html',[(348,363),(668,695)]),
 ('Poincare-definitions','AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/Poincare.lean',[(13,23),(28,38)]),
 ('gradient-definition','.lake/packages/mathlib/Mathlib/Analysis/Calculus/Gradient/Basic.lean',[(49,53),(82,83)]),
 ('Riesz-type','.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/Dual.lean',[(129,139)]),
 ('L2-context','.lake/packages/mathlib/Mathlib/MeasureTheory/Function/L2Space.lean',[(36,41),(100,105)]),
 ('CLM-integral-context','.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/Bochner/ContinuousLinearMap.lean',[(27,35),(49,49)]),
 ('norm-context','.lake/packages/mathlib/Mathlib/Analysis/Normed/Operator/Basic.lean',[(45,53),(130,130)]),
 ('inner-context','.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/Basic.lean',[(40,47)]),
 ('mathlib-manifest','lake-manifest.json',[(1,14)]),
]:slice_pin(sid,path,ranges,'primary' if sid.startswith('primary') else 'definition-or-ambient-context')
decls=[
 ('memLp-two-sq','.lake/packages/mathlib/Mathlib/MeasureTheory/Function/L2Space.lean','memLp_two_iff_integrable_sq','MeasureTheory.memLp_two_iff_integrable_sq'),
 ('L2-inner','.lake/packages/mathlib/Mathlib/MeasureTheory/Function/L2Space.lean','inner_def','MeasureTheory.L2.inner_def'),
 ('L2-square','.lake/packages/mathlib/Mathlib/MeasureTheory/Function/L2Space.lean','integral_inner_eq_sq_eLpNorm','MeasureTheory.L2.integral_inner_eq_sq_eLpNorm'),
 ('Cauchy-Schwarz','.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/Basic.lean','real_inner_mul_inner_self_le','real_inner_mul_inner_self_le'),
 ('CLM-integral','.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/Bochner/ContinuousLinearMap.lean','integral_apply','ContinuousLinearMap.integral_apply'),
 ('dual-norm-bound','.lake/packages/mathlib/Mathlib/Analysis/Normed/Operator/Basic.lean','opNorm_le_bound','ContinuousLinearMap.opNorm_le_bound'),
 ('bounded-L2','.lake/packages/mathlib/Mathlib/MeasureTheory/Function/LpSeminorm/Basic.lean','MemLp.of_bound','MeasureTheory.MemLp.of_bound'),
 ('covariance-algebra','.lake/packages/mathlib/Mathlib/Probability/Moments/Covariance.lean','covariance_eq_sub','ProbabilityTheory.covariance_eq_sub'),
]
for sid,path,name,qualified in decls:
 raw=(R/path).read_bytes();text=raw.decode('utf-8');matches=list(re.finditer(r'^(?:protected )?(?:theorem|lemma) '+re.escape(name)+r'(?=[\s{(:])',text,re.M));assert len(matches)==1,(sid,len(matches))
 a=matches[0].start();z=text.index(':=',a);header=text[a:z].encode('utf-8');first=text[:a].count('\n')+1;last=text[:z].count('\n')+1
 (O/(sid+'.raw.txt')).write_bytes(header);(O/(sid+'.lf.txt')).write_bytes(lf(header));items.append(dict(id=sid,path=path,kind='public-primitive-header',qualified_name=qualified,physical_ranges=[[first,last]],stop_before_proof=True,whole_raw_sha256=sha(raw),raw_sha256=sha(header),lf_sha256=sha(lf(header)),raw_bytes=len(header)))
 print(qualified,first,last,lf(header).decode('utf-8'))
for slug in ['ASTIS-SW-PBPS-conditional-score','ASTIS-SW-PBPS-conditional-score-variance','ASTIS-SW-PBPS-macroscopic-representative','ASTIS-SW-PBPS-reflection-l2-blocks','ASTIS-SW-SPHMC-proximal-estimator-lipschitz']:
 path='research-wiki/frontier-cells/'+slug+'.json';raw=(R/path).read_bytes();(O/(slug+'.metadata.raw.json')).write_bytes(raw);(O/(slug+'.metadata.lf.json')).write_bytes(lf(raw));items.append(dict(id=slug,path=path,kind='current-DAG-status-metadata-not-proof',raw_sha256=sha(raw),lf_sha256=sha(lf(raw)),raw_bytes=len(raw)))
(O/'primitive-input-bindings.json').write_bytes((json.dumps(items,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
