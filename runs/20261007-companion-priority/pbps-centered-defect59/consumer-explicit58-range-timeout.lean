import AutoSamplingTheory.ExampleCases.ProximalBPS.CenteredDefectOperator
import Tests.ProximalBPSMacroscopicRange

open MeasureTheory ProbabilityTheory
open scoped ContDiff NNReal ENNReal Topology
namespace Tests.ProximalBPSCenteredDefect
open AutoSamplingTheory.ExampleCases.ProximalBPS
noncomputable section
set_option autoImplicit false
set_option maxHeartbeats 1600000

theorem actual_centered_defect_coercive_and_unit
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ)*‖v‖^2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ)*‖v‖^2)
    (hη : 0 < η) (hβη : (β : ℝ)*η ≤ 1) :
    let μ := (volume : Measure E).tilted (fun x => -V x)
    let J := (μ.prod (stdGaussian E)).map
      (fun p : E × E => (p.1,p.1+Real.sqrt η • p.2))
    let ν := J.snd
    ∃ T : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν,
      IsSelfAdjoint T ∧
      (∀ u : Lp ℝ 2 ν, (T u : E → ℝ) =ᵐ[ν]
        (fun y => ∫ x, u x ∂((volume : Measure E).tilted
          (fun x => -V ((1/2 : ℝ) • (y+x)) - ‖y-x‖^2/(8*η))))) ∧
      ∃ q : Lp ℝ 2 ν,
        (q : E → ℝ) =ᵐ[ν] (fun _ => (1 : ℝ)) ∧
        (∀ u : Lp ℝ 2 ν, inner ℝ q u = ∫ y, u y ∂ν) ∧
        ∃ T0 : ((innerSL ℝ q).ker) →L[ℝ] ((innerSL ℝ q).ker),
          (∀ u : ((innerSL ℝ q).ker), (T0 u : Lp ℝ 2 ν) = T u) ∧
          IsSelfAdjoint T0 ∧ ((1 : ((innerSL ℝ q).ker) →L[ℝ] ((innerSL ℝ q).ker))-T0*T0).IsPositive ∧
          (∀ u : ((innerSL ℝ q).ker),
            ‖T0 u‖ ≤ ((1-(α : ℝ)*η)/(1+(α : ℝ)*η))*‖u‖ ∧
            inner ℝ (((1 : ((innerSL ℝ q).ker) →L[ℝ] ((innerSL ℝ q).ker))-T0*T0) u) u = ‖u‖^2-‖T0 u‖^2 ∧
            (4*(α : ℝ)*η/(1+(α : ℝ)*η)^2)*‖u‖^2 ≤
              inner ℝ (((1 : ((innerSL ℝ q).ker) →L[ℝ] ((innerSL ℝ q).ker))-T0*T0) u) u) ∧
          IsUnit ((1 : ((innerSL ℝ q).ker) →L[ℝ] ((innerSL ℝ q).ker))-T0*T0) := by
  classical
  dsimp only
  let μ := (volume : Measure E).tilted (fun x => -V x)
  let J := (μ.prod (stdGaussian E)).map
    (fun p : E × E => (p.1,p.1+Real.sqrt η • p.2))
  let ν := J.snd
  let P : Lp ℝ 2 J →L[ℝ] Lp ℝ 2 J :=
    (lpMeas ℝ ℝ (MeasurableSpace.comap Prod.snd (inferInstance : MeasurableSpace E))
      2 J).subtypeL ∘L condExpL2 ℝ ℝ measurable_snd.comap_le
  obtain ⟨hμ,hJ,hν,S,hS,hSd,hSc,hSf,hSs,U,hU,hUi,hUs,M,hM,T,hTs,hAll,
    q,hq,hTq,hPair,hH0,hD,hDq,hDef,T0,hT0,hT0s,hT0n,hD0,hD0sub,hDef0⟩ :=
    CenteredDefectOperator.actual_centered_selfadjoint_defect hα hαβ hV hH hη hβη
  letI : IsProbabilityMeasure J := hJ
  letI : IsProbabilityMeasure ν := hν
  let H0 : Submodule ℝ (Lp ℝ 2 ν) := (innerSL ℝ q).ker
  trace "C59_STAGE_00"
  have hLiteral (u : Lp ℝ 2 ν) : (T u : E → ℝ) =ᵐ[ν]
      (fun y => ∫ x, u x ∂((volume : Measure E).tilted
        (fun x => -V ((1/2 : ℝ) • (y+x)) - ‖y-x‖^2/(8*η)))) := by
    filter_upwards [(hAll u).2.2.2.1] with y hy
    exact hy.trans (congrArg (fun m : Measure E => ∫ x, u x ∂m) (hSd y))
  trace "C59_STAGE_01"
  have h58 := ProximalBPSMacroscopicRange.actual_centered_macro_contraction_and_defect_gap
    (E:=E) (V:=V) (α:=α) (β:=β) (η:=η) hα hαβ hV hH hη hβη
  trace "C59_STAGE_01_INSTANTIATED"
  dsimp only at h58
  trace "C59_STAGE_01_LETS_REDUCED"
  obtain ⟨U58,hU58,hUi58,hUs58,hSharp⟩ := h58
  trace "C59_STAGE_02"
  have hSameU : U58=U := LinearIsometry.ext (fun f =>
    Lp.ext ((hU58 f).trans (hU f).symm))
  trace "C59_STAGE_03"
  subst U58
  trace "C59_STAGE_04"
  let hp : MeasurePreserving (Prod.snd : E × E → E) J ν := ⟨measurable_snd,rfl⟩
  trace "C59_STAGE_05"
  let Mc : Lp ℝ 2 ν →ₗᵢ[ℝ] Lp ℝ 2 J := Lp.compMeasurePreservingₗᵢ ℝ Prod.snd hp
  trace "C59_STAGE_06"
  have hSameM : M=Mc := LinearIsometry.ext (fun u =>
    Lp.ext ((hM u).trans (Lp.coeFn_compMeasurePreserving u hp).symm))
  trace "C59_STAGE_07"
  obtain ⟨_,_,hRange,hMean,hCentered⟩ :=
    MacroscopicRange.actual_macroscopic_centered_range hα hαβ hV hH hη hβη
  trace "C59_STAGE_08"
  have hCon (u : H0) : ‖T0 u‖ ≤
      ((1-(α : ℝ)*η)/(1+(α : ℝ)*η))*‖u‖ := by
    have hu : (∫ y, (u : Lp ℝ 2 ν) y ∂ν)=0 := (hH0 _).mp u.property
    have hr : M (u : Lp ℝ 2 ν) ∈ P.toLinearMap.range :=
      ⟨M u,(hAll (u : Lp ℝ 2 ν)).1⟩
    have hc : (∫ p, (M (u : Lp ℝ 2 ν)) p ∂J)=0 := by
      rw [hSameM]
      exact (hMean (u : Lp ℝ 2 ν)).trans hu
    have hn := (hSharp (M u) hr hc).1
    rw [← (hAll (u : Lp ℝ 2 ν)).2.1,M.norm_map] at hn
    simpa only [hT0,Submodule.norm_coe] using hn
  trace "C59_STAGE_09"
  let δ : ℝ := 4*(α : ℝ)*η/(1+(α : ℝ)*η)^2
  have ha0 : 0 < (α : ℝ)*η := mul_pos hα hη
  have ha1 : (α : ℝ)*η ≤ 1 :=
    (mul_le_mul_of_nonneg_right (by exact_mod_cast hαβ) hη.le).trans hβη
  have hd : 0 < 1+(α : ℝ)*η := by positivity
  have hρ : 0 ≤ (1-(α : ℝ)*η)/(1+(α : ℝ)*η) :=
    div_nonneg (sub_nonneg.mpr ha1) hd.le
  have hδ : 0 < δ := by dsimp [δ]; positivity
  trace "C59_STAGE_10"
  have hGap (u : H0) : δ*‖u‖^2 ≤ inner ℝ (((1 : H0 →L[ℝ] H0)-T0*T0) u) u := by
    have hs : ‖T0 u‖^2 ≤ (((1-(α : ℝ)*η)/(1+(α : ℝ)*η))*‖u‖)^2 :=
      (sq_le_sq₀ (norm_nonneg _) (mul_nonneg hρ (norm_nonneg _))).mpr (hCon u)
    have hr : δ = 1-((1-(α : ℝ)*η)/(1+(α : ℝ)*η))^2 := by
      dsimp [δ]
      field_simp [ne_of_gt hd]
      ring
    rw [hDef0,hr]
    nlinarith [hs]
  trace "C59_STAGE_11"
  have hUnit : IsUnit ((1 : H0 →L[ℝ] H0)-T0*T0) := by
    apply ContinuousLinearMap.isUnit_of_forall_le_norm_inner_map
      ((1 : H0 →L[ℝ] H0)-T0*T0) (c:=⟨δ,hδ.le⟩) (by exact hδ)
    intro u
    change ‖u‖^2*δ ≤ ‖inner ℝ (((1 : H0 →L[ℝ] H0)-T0*T0) u) u‖
    rw [Real.norm_eq_abs,abs_of_nonneg (hD0.inner_nonneg_left u),mul_comm]
    exact hGap u
  trace "C59_STAGE_12"
  refine ⟨T,hTs,hLiteral,q,hq,hPair,T0,hT0,hT0s,hD0,?_,hUnit⟩
  intro u
  exact ⟨hCon u,hDef0 u,hGap u⟩

end
end Tests.ProximalBPSCenteredDefect

#print axioms Tests.ProximalBPSCenteredDefect.actual_centered_defect_coercive_and_unit
