import AutoSamplingTheory.ExampleCases.ProximalBPS.SourceMeanGradientDomain
import AutoSamplingTheory.ExampleCases.ProximalBPS.L2MacroscopicMean
import Mathlib.Analysis.Normed.Operator.Extend

open MeasureTheory ProbabilityTheory InnerProductSpace
open scoped RealInnerProductSpace ContDiff NNReal Topology
namespace AutoSamplingTheory.ExampleCases.ProximalBPS.RoughMeanGradient
noncomputable section
set_option autoImplicit false
set_option maxHeartbeats 1600000

theorem actual_rough_mean_gradient
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
    let S := fun y : E => (volume : Measure E).tilted
      (fun x => -V ((1/2 : ℝ) • (y+x)) - ‖y-x‖^2/(8*η))
    IsProbabilityMeasure ν ∧
      ∃ G : Lp ℝ 2 ν →ₗ.[ℝ] Lp E 2 ν,
        Dense (G.domain : Set (Lp ℝ 2 ν)) ∧ G.IsClosable ∧ G.closure.IsClosed ∧
        (∀ (u : Lp ℝ 2 ν) (v : Lp E 2 ν), (u,v) ∈ G.graph ↔
          ∃ φ : E → ℝ, ContDiff ℝ ∞ φ ∧ HasCompactSupport φ ∧
            u =ᵐ[ν] φ ∧ v =ᵐ[ν] gradient φ) ∧
        ∃ T : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν,
          ∃ K : Lp ℝ 2 ν →L[ℝ] Lp E 2 ν,
            ∀ u : Lp ℝ 2 ν,
              (T u,K u) ∈ G.closure.graph ∧ ‖T u‖ ≤ ‖u‖ ∧
              (T u : E → ℝ) =ᵐ[ν] (fun y => ∫ x, u x ∂S y) ∧
              (∀ᵐ y ∂ν, Integrable (u : E → ℝ) (S y) ∧
                Integrable (fun x => (u x)^2) (S y)) ∧
              η*‖K u‖^2 ≤
                (1-(α : ℝ)*η)^2/(4*(1+(α : ℝ)*η)) * (‖u‖^2-‖T u‖^2) ∧
              4*η*‖K u‖^2 ≤ ‖u‖^2-‖T u‖^2 