import AutoSamplingTheory.TechnicalLemmas.Measure.L2PullbackRange
import AutoSamplingTheory.ExampleCases.ProximalBPS.GibbsAugmentation
import Mathlib.MeasureTheory.Function.ConditionalExpectation.CondexpL2

/-! Actual PBPS Appendix B macro-space identification. The reverse range and
centered image use genuine measurable factorization, the actual Gaussian-Gibbs
law and pushforward means. This is not a defect square-root/inverse theorem.
Original C2/two Hessian/capped scale are retained; finite real Hilbert/rank zero
is an explicitly disclosed extension. No finite-dimensional assumption on L2. -/

open MeasureTheory ProbabilityTheory
open scoped ContDiff NNReal Topology
namespace AutoSamplingTheory.ExampleCases.ProximalBPS.MacroscopicRange
noncomputable section
set_option autoImplicit false

theorem actual_macroscopic_centered_range
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
    let hp : MeasurePreserving (Prod.snd : E × E → E) J ν :=
      ⟨measurable_snd,rfl⟩
    let M : Lp ℝ 2 ν →ₗᵢ[ℝ] Lp ℝ 2 J :=
      Lp.compMeasurePreservingₗᵢ ℝ Prod.snd hp
    let P : Lp ℝ 2 J →L[ℝ] Lp ℝ 2 J :=
      (lpMeas ℝ ℝ (MeasurableSpace.comap Prod.snd (inferInstance : MeasurableSpace E))
        2 J).subtypeL ∘L condExpL2 ℝ ℝ measurable_snd.comap_le
    IsProbabilityMeasure J ∧ IsProbabilityMeasure ν ∧
      M.toLinearMap.range = P.toLinearMap.range ∧
      (∀ u : Lp ℝ 2 ν, (∫ p, (M u) p ∂J) = ∫ y, u y ∂ν) ∧
      M '' {u : Lp ℝ 2 ν | (∫ y, u y ∂ν)=0} =
        {f : Lp ℝ 2 J | f ∈ P.toLinearMap.range ∧ (∫ p, f p ∂J)=0} := by
  classical
  dsimp only
  let μ := (volume : Measure E).tilted (fun x => -V x)
  let J := (μ.prod (stdGaussian E)).map
    (fun p : E × E => (p.1,p.1+Real.sqrt η • p.2))
  let ν := J.snd
  let hp : MeasurePreserving (Prod.snd : E × E → E) J ν := ⟨measurable_snd,rfl⟩
  let M : Lp ℝ 2 ν →ₗᵢ[ℝ] Lp ℝ 2 J := Lp.compMeasurePreservingₗᵢ ℝ Prod.snd hp
  let S := lpMeas ℝ ℝ (MeasurableSpace.comap Prod.snd
    (inferInstance : MeasurableSpace E)) 2 J
  let P : Lp ℝ 2 J →L[ℝ] Lp ℝ 2 J :=
    S.subtypeL ∘L condExpL2 ℝ ℝ measurable_snd.comap_le
  obtain ⟨_,hJ,_⟩ := GibbsAugmentation.normalized_augmentation_density
    hα hV (fun x v => (hH x v).1) hη
  letI : IsProbabilityMeasure J := hJ
  have hν : IsProbabilityMeasure ν := by infer_instance
  letI : IsProbabilityMeasure ν := hν
  letI : Fact ((MeasurableSpace.comap Prod.snd
    (inferInstance : MeasurableSpace E)) ≤ (inferInstance : MeasurableSpace (E × E))) :=
    ⟨measurable_snd.comap_le⟩
  have hMrange : M.toLinearMap.range = S :=
    AutoSamplingTheory.TechnicalLemmas.Measure.L2PullbackRange.l2_pullback_range_eq_lpMeas hp
  have hPdef : P = S.starProjection := rfl
  have hPrange : P.toLinearMap.range = S := by
    change P.range = S
    rw [hPdef]
    exact S.range_starProjection
  have hRange : M.toLinearMap.range = P.toLinearMap.range := hMrange.trans hPrange.symm
  have hMean (u : Lp ℝ 2 ν) : (∫ p, (M u) p ∂J) = ∫ y, u y ∂ν := by
    calc
      (∫ p, (M u) p ∂J) = ∫ p : E × E, u p.2 ∂J :=
        integral_congr_ae (Lp.coeFn_compMeasurePreserving u hp)
      _ = ∫ y, u y ∂ν :=
        (integral_map measurable_snd.aemeasurable (Lp.aestronglyMeasurable u)).symm
  refine ⟨hJ,hν,hRange,hMean,?_⟩
  ext f
  constructor
  · rintro ⟨u,hu,rfl⟩
    refine ⟨?_,?_⟩
    · rw [← hRange]
      exact ⟨u,rfl⟩
    · rw [hMean]
      exact hu
  · rintro ⟨hf,hfmean⟩
    have hfM : f ∈ M.toLinearMap.range := by rwa [hRange]
    obtain ⟨u,hu⟩ := hfM
    refine ⟨u,?_,hu⟩
    change M u=f at hu
    change (∫ y, u y ∂ν)=0
    rw [← hMean u,hu]
    exact hfmean

end
end AutoSamplingTheory.ExampleCases.ProximalBPS.MacroscopicRange
