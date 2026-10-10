import AutoSamplingTheory.ExampleCases.ProximalBPS.L2MacroscopicMean
import Mathlib.MeasureTheory.Function.FactorsThrough
open MeasureTheory ProbabilityTheory
open scoped ContDiff NNReal Topology
set_option autoImplicit false

#check fun
    {X Y : Type*} [MeasurableSpace X] [MeasurableSpace Y]
    {μ : Measure X} {ν : Measure Y} {f : X → Y}
    (hf : MeasurePreserving f μ ν) =>
    (Lp.compMeasurePreservingₗᵢ ℝ f hf).toLinearMap.range =
      lpMeas ℝ ℝ (MeasurableSpace.comap f (inferInstance : MeasurableSpace Y)) 2 μ

#check fun
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ)*‖v‖^2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ)*‖v‖^2)
    (hη : 0 < η) (hβη : (β : ℝ)*η ≤ 1) =>
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
        {f : Lp ℝ 2 J | f ∈ P.toLinearMap.range ∧ (∫ p, f p ∂J)=0}

