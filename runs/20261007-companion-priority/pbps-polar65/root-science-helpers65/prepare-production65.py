from pathlib import Path
import json,hashlib
pre=Path('runs/20261007-companion-priority/pbps-polar-preproof65');r=Path('runs/20261007-companion-priority/pbps-polar65')
seal=json.loads((pre/'root.statement-seal65.json').read_bytes());assert seal['status']=='STATEMENT65_SEALED_NOT_PROVED_NOT_CLAIMED'
for i,q in enumerate(seal['headers']):assert hashlib.sha256((pre/f'header{i}.lean').read_bytes()).hexdigest()==q['raw_sha256']
old=Path('Tests/ProximalBPSCenteredRootOrderInverse.lean').read_text(encoding='utf-8');a=old.index('  classical\n');b=old.index('  have hGramLocal',a);prefix=old[a:b]
prefix=prefix.replace('  letI : InnerProductSpace ℝ HP0 := HP0.innerProductSpace\n','  letI : InnerProductSpace ℝ HP0 := HP0.innerProductSpace\n  letI : CompleteSpace HP0 := (innerSL ℝ qP).isClosed_ker.completeSpace_coe\n')
head=(pre/'header.candidate.lean').read_text(encoding='utf-8').split(':= by')[0]
body=prefix+'''  let Hperp := P.ker
  letI : NormedAddCommGroup Hperp := Hperp.normedAddCommGroup
  letI : InnerProductSpace ℝ Hperp := Hperp.innerProductSpace
  letI : CompleteSpace Hperp := P.isClosed_ker.completeSpace_coe
  let B0 : HP0 →L[ℝ] Hperp :=
    (B ∘L HP0.subtypeL).codRestrict Hperp (by intro f; exact hPB (f : HP))
  have hB0 (f : HP0) : (B0 f : Lp ℝ 2 J)=B (f : HP) := rfl
  let V0 : HP0 →L[ℝ] Hperp := B0 ∘L Inv
  have hGramLocal : B.adjoint ∘L B=ΓP*ΓP := hGram
  have hPosLocal : ΓP.IsPositive := hΓP
  have hVnorm (f : HP0) : ‖V0 f‖=‖f‖ := by
    let g : HP0 := Inv f
    have hg : ΓP0 g=f := congrArg (fun C : HP0 →L[ℝ] HP0 => C f) hRight
    have hb := B.apply_norm_sq_eq_inner_adjoint_right (g : HP)
    have hr := ΓP.apply_norm_sq_eq_inner_adjoint_right (g : HP)
    rw [hGramLocal] at hb
    rw [hPosLocal.isSelfAdjoint.adjoint_eq] at hr
    have hNorm : ‖B (g : HP)‖=‖ΓP (g : HP)‖ :=
      (sq_eq_sq₀ (norm_nonneg _) (norm_nonneg _)).mp (hb.trans hr.symm)
    calc
      ‖V0 f‖=‖B (g : HP)‖ := rfl
      _ = ‖ΓP (g : HP)‖ := hNorm
      _ = ‖ΓP0 g‖ := congrArg (fun z : HP => ‖z‖) (hΓP0 g).symm
      _ = ‖f‖ := congrArg (fun z : HP0 => ‖z‖) hg
  have hFactor : B0=V0 ∘L ΓP0 := by
    ext f
    change B0 f=B0 (Inv (ΓP0 f))
    have hf : Inv (ΓP0 f)=f := congrArg (fun C : HP0 →L[ℝ] HP0 => C f) hLeft
    rw [hf]
  have hVadj : V0.adjoint ∘L V0=(1 : HP0 →L[ℝ] HP0) :=
    (ContinuousLinearMap.norm_map_iff_adjoint_comp_self V0).mp hVnorm
  exact ⟨hμ,hJ,hν,hRange,hPf,S,hS,hSd,hSc,hSf,hSs,e,he,U,hU,hUi,hUs,T,hTs,hAll,
    hAeq,hAs,hAn,hPB,Γ,hΓ,hΓSq,hΓP,hΓPSq,hGram,q,hqa,hTq,hq,hCenter,hΓPq,hγ,
    ΓP0,hΓP0,hPos0,hOrder0,hUnit,Inv,hLeft,hRight,hNormInv,B0,hB0,V0,rfl,
    hFactor,hVadj,hVnorm⟩
'''
p=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/PolarIsometry.lean');assert not p.exists();p.write_text(head+':= by\n'+body+'\nend\nend AutoSamplingTheory.ExampleCases.ProximalBPS.PolarIsometry\n',encoding='utf-8',newline='\n')
testhead=(pre/'test.candidate.lean').read_text(encoding='utf-8').split(':= by')[0].replace('import AutoSamplingTheory.ExampleCases.ProximalBPS.CenteredRootOrderInverse','import AutoSamplingTheory.ExampleCases.ProximalBPS.PolarIsometry')
testprefix=prefix.replace('CenteredRootOrderInverse.actual_centered_root_order_inverse','PolarIsometry.actual_centered_polar_isometry').replace('Inv,hLeft,hRight,hNormInv⟩','Inv,hLeft,hRight,hNormInv,B0,hB0,V0,hVdef,hFactor,hVadj,hVnorm⟩')
testbody=testprefix+'''  let Hperp := P.ker
  letI : NormedAddCommGroup Hperp := Hperp.normedAddCommGroup
  letI : InnerProductSpace ℝ Hperp := Hperp.innerProductSpace
  letI : CompleteSpace Hperp := P.isClosed_ker.completeSpace_coe
  have hBAdj : B0.adjoint=ΓP0 ∘L V0.adjoint := by
    rw [hFactor,ContinuousLinearMap.adjoint_comp,hPos0.isSelfAdjoint.adjoint_eq]
  have hNormV : ‖V0‖ ≤ (1 : ℝ) :=
    ContinuousLinearMap.opNorm_le_bound _ zero_le_one (by intro f; rw [hVnorm f,one_mul])
  have hNormAdj : ‖V0.adjoint‖ ≤ (1 : ℝ) :=
    (ContinuousLinearMap.adjoint.norm_map V0).trans_le hNormV
  refine ⟨hμ,hJ,hν,hRange,hPf,S,hS,hSd,hSc,hSf,hSs,e,he,U,hU,hUi,hUs,T,hTs,hAll,
    hAeq,hAs,hAn,hPB,Γ,hΓ,hΓSq,hΓP,hΓPSq,hGram,q,hqa,hTq,hq,hCenter,hΓPq,hγ,
    ΓP0,hΓP0,hPos0,hOrder0,hUnit,Inv,hLeft,hRight,hNormInv,B0,hB0,V0,hVdef,
    hFactor,hVadj,hVnorm,?_,?_,?_⟩
  · intro g
    exact congrArg (fun C : Hperp →L[ℝ] HP0 => C g) hBAdj
  · intro g
    calc
      ‖V0.adjoint g‖ ≤ ‖V0.adjoint‖*‖g‖ := V0.adjoint.le_opNorm g
      _ ≤ 1*‖g‖ := mul_le_mul_of_nonneg_right hNormAdj (norm_nonneg _)
      _ = ‖g‖ := one_mul _
  · intro g
    have hf : V0.adjoint (V0 (V0.adjoint g))=V0.adjoint g :=
      congrArg (fun C : HP0 →L[ℝ] HP0 => C (V0.adjoint g)) hVadj
    rw [map_sub,hf,sub_self]
'''
p=Path('Tests/ProximalBPSPolarIsometry.lean');assert not p.exists();p.write_text(testhead+':= by\n'+testbody+'\nend\nend Tests.ProximalBPSPolarIsometry\n\n#print axioms AutoSamplingTheory.ExampleCases.ProximalBPS.PolarIsometry.actual_centered_polar_isometry\n#print axioms Tests.ProximalBPSPolarIsometry.genuine_actual_polar_corrector_consumer\n',encoding='utf-8',newline='\n')
print('Wrote actual65 typed polar construction and genuine adjoint-corrector Test from exact sealed headers; compiler acceptance pending.')
