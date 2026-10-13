from pathlib import Path
import subprocess,json,hashlib
r=Path('runs/20261007-companion-priority/pbps-ambient-adjoint66');out=r/'reuse-retrieval66';out.mkdir(exist_ok=False)
queries=[
 ('canonical-substrate','actual_centered_polar_isometry|hGramLocal|hVnorm', ['AutoSamplingTheory/ExampleCases/ProximalBPS/PolarIsometry.lean','Tests/ProximalBPSPolarIsometry.lean']),
 ('conditional-projection','def condExpL2|inner_condExpL2_left_eq_right|inner_condExpL2_eq_inner_fun',['.lake/packages/mathlib/Mathlib/MeasureTheory/Function/ConditionalExpectation/CondexpL2.lean']),
 ('projection-geometry','starProjection_inner_eq_zero|norm_sq_eq_add_norm_sq_starProjection|starProjection_orthogonal_val',['.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/Projection/Basic.lean']),
 ('adjoint-pairing','theorem adjoint_inner_left|theorem adjoint_inner_right|norm_map_iff_adjoint_comp_self',['.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/Adjoint.lean']),
 ('expectation-transport','inner_one_eq_integral|theorem coeFn_compMeasurePreserving|theorem ae ',['AutoSamplingTheory/TechnicalLemmas/Measure/L2Expectation.lean','.lake/packages/mathlib/Mathlib/MeasureTheory/Function/LpSpace/Basic.lean','.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/QuasiMeasurePreserving.lean']),
 ('existing-cell-owner','ambient-adjoint|actual-polar-isometry',['research-wiki/frontier-cells'])]
rows=[]
for label,pattern,paths in queries:
 cmd=['rg','-n',pattern]+paths
 if label=='existing-cell-owner':cmd+=['-g','*.json']
 p=subprocess.run(cmd,capture_output=True);assert p.returncode==0,(label,p.returncode)
 f=out/(label+'.stdout.exactraw.txt');f.write_bytes(p.stdout)
 rows.append(dict(label=label,command=cmd,exit_code=p.returncode,stdout_path=f.as_posix(),raw_sha256=hashlib.sha256(p.stdout).hexdigest()))
(out/'retrieval.json').write_text(json.dumps(dict(status='LOCAL_AND_PINNED_MATHLIB_RETRIEVAL',queries=rows,mathlib_commit='db584cd6d46c92f209a44c0f1c829460d327499d',decision='Reuse SAME65 actual data,root,inverse,polar. Minimal domain adapter/centered input only; no external theorem or duplicate generic floor.'),indent=2)+'\n',encoding='utf-8',newline='\n')
print('Exact Samplinglib/pinned Mathlib retrieval retained; one66 owner and existing source consumers.')
