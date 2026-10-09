from pathlib import Path
import hashlib,json
pre=Path('runs/20261007-companion-priority/pbps-ambient-adjoint-preproof66')
r=Path('runs/20261007-companion-priority/pbps-ambient-adjoint66')
assert json.loads((r/'claim.json').read_bytes())['advance_id']=='ASTIS-SA-20261009-PBPSAmbientAdjointCorrector'
parent=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/PolarIsometry.lean').read_text(encoding='utf-8')
begin=parent.index('  classical\n',parent.index(':= by'))
end=parent.index('  let B0 : HP0',begin)
setup=parent[begin:end].replace('AutoSamplingTheory.ExampleCases.ProximalBPS.CenteredRootOrderInverse.actual_centered_root_order_inverse','AutoSamplingTheory.ExampleCases.ProximalBPS.PolarIsometry.actual_centered_polar_isometry')
setup=setup.replace('Inv,hLeft,hRight,hNormInv⟩','Inv,hLeft,hRight,hNormInv,B0,hB0,V0,hVdef,hFactor,hVadj,hVnorm⟩')
body=setup+'''  change HP0 →L[ℝ] Hperp at B0 V0
  change HP0 →L[ℝ] HP0 at ΓP0 Inv
  letI : IsProbabilityMeasure J := hJ
  letI : IsProbabilityMeasure ν := hν
  let C : Lp ℝ 2 J →L[ℝ] HP := condExpL2 ℝ ℝ (μ:=J) measurable_snd.comap_le
  have hPself (g k : Lp ℝ 2 J) : inner ℝ (P g) k=inner ℝ g (P k) :=
    inner_condExpL2_left_eq_right measurable_snd.comap_le
  have hPid (g : Lp ℝ 2 J) : P (P g)=P g := hPf (C g)
  let R : Lp ℝ 2 J →L[ℝ] Hperp :=
    ((1 : Lp ℝ 2 J →L[ℝ] Lp ℝ 2 J)-P).codRestrict Hperp (by
      intro g
      change P (g-P g)=0
      rw [map_sub,hPid,sub_self])
  have hR (g : Lp ℝ 2 J) : (R g : Lp ℝ 2 J)=g-P g := rfl
  have hRself (g : Hperp) : R (g : Lp ℝ 2 J)=g := by
    apply Subtype.ext
    change (g : Lp ℝ 2 J)-P g=g
    rw [show P (g : Lp ℝ 2 J)=0 from g.property,sub_zero]
  have hGramLocal : B.adjoint ∘L B=ΓP*ΓP := hGram
  have hRootq : ΓP qP=0 := hΓPq
  have hBq : B qP=0 := by
    have hn := B.apply_norm_sq_eq_inner_adjoint_right qP
    rw [hGramLocal] at hn
    have hz : (ΓP*ΓP) qP=0 := by
      change ΓP (ΓP qP)=0
      rw [hRootq,map_zero]
    rw [hz,inner_zero_right] at hn
    exact norm_eq_zero.mp (sq_eq_zero_iff.mp hn)
  have hBCenter (g : Lp ℝ 2 J) : B.adjoint g ∈ HP0 := by
    change inner ℝ qP (B.adjoint g)=0
    rw [B.adjoint_inner_right,hBq,inner_zero_left]
  have hAmbient (g : Lp ℝ 2 J) :
      B.adjoint g=HP0.subtypeL (B0.adjoint (R g)) := by
    let b : HP0 := ⟨B.adjoint g,hBCenter g⟩
    have heq : b=B0.adjoint (R g) := by
      apply ext_inner_left ℝ
      intro u
      change inner ℝ (u : HP) (B.adjoint g)=inner ℝ u (B0.adjoint (R g))
      rw [B.adjoint_inner_right,B0.adjoint_inner_right]
      change inner ℝ (B (u : HP)) g=inner ℝ (B0 u : Lp ℝ 2 J) (R g : Lp ℝ 2 J)
      rw [hB0,hR,inner_sub_right]
      have ho : inner ℝ (B (u : HP)) (P g)=0 := by
        rw [← hPself,hPB,inner_zero_left]
      rw [ho,sub_zero]
    exact congrArg (fun z : HP0 => HP0.subtypeL z) heq
  have hPosLocal : ΓP0.IsPositive := hPos0
  have hBAdj : B0.adjoint=ΓP0 ∘L V0.adjoint := by
    calc
      B0.adjoint = (V0 ∘L ΓP0).adjoint :=
        congrArg (fun D : HP0 →L[ℝ] Hperp => D.adjoint) hFactor
      _ = ΓP0.adjoint ∘L V0.adjoint := ContinuousLinearMap.adjoint_comp V0 ΓP0
      _ = ΓP0 ∘L V0.adjoint :=
        congrArg (fun D : HP0 →L[ℝ] HP0 => D ∘L V0.adjoint)
          hPosLocal.isSelfAdjoint.adjoint_eq
  have hNormV : ‖V0‖ ≤ (1 : ℝ) :=
    ContinuousLinearMap.opNorm_le_bound _ zero_le_one (by intro u; rw [hVnorm u,one_mul])
  have hNormAdj : ‖V0.adjoint‖ ≤ (1 : ℝ) :=
    (ContinuousLinearMap.adjoint.norm_map V0).trans_le hNormV
  have hVcontract (g : Hperp) : ‖V0.adjoint g‖≤‖g‖ := by
    calc
      ‖V0.adjoint g‖ ≤ ‖V0.adjoint‖*‖g‖ := V0.adjoint.le_opNorm g
      _ ≤ 1*‖g‖ := mul_le_mul_of_nonneg_right hNormAdj (norm_nonneg _)
      _ = ‖g‖ := one_mul _
  let hp : MeasurePreserving (Prod.snd : E × E → E) J ν := ⟨measurable_snd,rfl⟩
  let M : Lp ℝ 2 ν →ₗᵢ[ℝ] Lp ℝ 2 J := Lp.compMeasurePreservingₗᵢ ℝ Prod.snd hp
  have hqOne : (qP : Lp ℝ 2 J)=
      AutoSamplingTheory.TechnicalLemmas.Measure.L2Expectation.one J := by
    rw [show (qP : Lp ℝ 2 J)=M q from he q]
    apply Lp.ext
    have hqaPull : (fun z : E × E => q z.2)=ᵐ[J] (fun _ => (1 : ℝ)) :=
      hp.quasiMeasurePreserving.ae hqa
    exact (Lp.coeFn_compMeasurePreserving q hp).trans
      (hqaPull.trans (Lp.coeFn_const (p:=(2 : ℝ≥0∞)) (μ:=J) (c:=(1 : ℝ))).symm)
  have hqIntegral (g : Lp ℝ 2 J) : inner ℝ (qP : Lp ℝ 2 J) g=∫ z, g z ∂J := by
    rw [hqOne]
    exact AutoSamplingTheory.TechnicalLemmas.Measure.L2Expectation.inner_one_eq_integral J g
  have hPq : P (qP : Lp ℝ 2 J)=qP := hPf qP
  refine ⟨hμ,hJ,hν,hRange,hPf,S,hS,hSd,hSc,hSf,hSs,e,he,U,hU,hUi,hUs,T,hTs,hAll,
    hAeq,hAs,hAn,hPB,Γ,hΓ,hΓSq,hΓP,hΓPSq,hGram,q,hqa,hTq,hq,hCenter,hΓPq,hγ,
    ΓP0,hΓP0,hPos0,hOrder0,hUnit,Inv,hLeft,hRight,hNormInv,B0,hB0,V0,hVdef,
    hFactor,hVadj,hVnorm,R,hR,hAmbient,?_⟩
  intro f hf
  have hCf : C f ∈ HP0 := by
    change inner ℝ qP (C f)=0
    change inner ℝ (qP : Lp ℝ 2 J) (P f)=0
    rw [← hPself,hPq,hqIntegral,hf]
  let fP : HP0 := ⟨C f,hCf⟩
  refine ⟨fP,rfl,?_,?_,?_,hVcontract (R f)⟩
  · calc
      B.adjoint (R f : Lp ℝ 2 J)=HP0.subtypeL (B0.adjoint (R (R f))) := hAmbient _
      _ = HP0.subtypeL (B0.adjoint (R f)) := congrArg
        (fun z : Hperp => HP0.subtypeL (B0.adjoint z)) (hRself (R f))
      _ = HP0.subtypeL (ΓP0 (V0.adjoint (R f))) :=
        congrArg (fun z : HP0 => HP0.subtypeL z)
          (congrArg (fun D : Hperp →L[ℝ] HP0 => D (R f)) hBAdj)
  · exact hΓP0 _
  · have hn := HP.norm_sq_eq_add_norm_sq_starProjection f
    have hProj : HP.starProjection=P := rfl
    rw [hProj,HP.starProjection_orthogonal_val] at hn
    change ‖f‖^2=‖(C f : Lp ℝ 2 J)‖^2+‖f-P f‖^2 at hn
    exact hn
'''
candidate=(pre/'header.candidate.lean').read_text(encoding='utf-8')
assert candidate.count('  ASTIS_UNIMPLEMENTED_BODY66\n')==1
p=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/AmbientAdjointCorrector.lean');assert not p.exists()
p.write_text(candidate.replace('  ASTIS_UNIMPLEMENTED_BODY66\n',body),encoding='utf-8',newline='\n')
print('Production66 first implementation written; exact sealed header preserved; compilation unrun.')
