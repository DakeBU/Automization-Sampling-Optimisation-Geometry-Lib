import AutoSamplingTheory.ExampleCases.ProximalBPS.CenteredDefectOperator
import Mathlib.Analysis.Complex.Basic
open MeasureTheory ProbabilityTheory
open scoped ContDiff NNReal ENNReal Topology
set_option autoImplicit false
set_option maxHeartbeats 1000000
#check (fun
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
    let Λ := J.map (fun p : E × E => (p.2,(2 : ℝ) • p.1-p.2))
    let ι : Lp ℝ 2 ν →L[ℝ] Lp ℂ 2 ν := Complex.ofRealCLM.compLpL 2 ν
    let R : Lp ℂ 2 ν →L[ℝ] Lp ℝ 2 ν := Complex.reCLM.compLpL 2 ν
    let Q : Lp ℂ 2 ν →L[ℝ] Lp ℝ 2 ν := Complex.imCLM.compLpL 2 ν
    let C : Lp ℂ 2 ν →L[ℝ] Lp ℂ 2 ν := Complex.conjCLE.toContinuousLinearMap.compLpL 2 ν
    IsProbabilityMeasure μ ∧ IsProbabilityMeasure J ∧ IsProbabilityMeasure ν ∧
    ∃ S : Kernel E E, IsMarkovKernel S ∧
      (∀ y, S y = (volume : Measure E).tilted
        (fun x => -V ((1/2 : ℝ) • (y+x)) - ‖y-x‖^2/(8*η))) ∧
      Λ.IsCondKernel S ∧ Λ.fst = ν ∧ Λ.snd = ν ∧
      ∃ T : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν,
        IsSelfAdjoint T ∧
        (∀ u : Lp ℝ 2 ν, ‖T u‖ ≤ ‖u‖ ∧
          (T u : E → ℝ) =ᵐ[ν] (fun y => ∫ x, u x ∂S y) ∧
          (∫ y, T u y ∂ν) = ∫ y, u y ∂ν) ∧
        ((1 : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν)-T*T).IsPositive ∧
        (∀ u : Lp ℝ 2 ν, ‖ι u‖ = ‖u‖) ∧
        (∀ g : Lp ℂ 2 ν, C g = g ↔ ∃ u : Lp ℝ 2 ν, ι u = g) ∧
        ∃ Dc : Lp ℂ 2 ν →L[ℂ] Lp ℂ 2 ν,
          Dc.IsPositive ∧
          (∀ g : Lp ℂ 2 ν, Dc g =
            ι (((1 : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν)-T*T) (R g)) +
            Complex.I • ι (((1 : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν)-T*T) (Q g))) ∧
          (∀ u : Lp ℝ 2 ν, Dc (ι u) = ι (((1 : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν)-T*T) u)) ∧
          (∀ g : Lp ℂ 2 ν, C (Dc g) = Dc (C g)) : _)
