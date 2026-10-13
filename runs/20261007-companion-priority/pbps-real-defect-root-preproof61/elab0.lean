import AutoSamplingTheory.ExampleCases.ProximalBPS.DefectComplexLift
import Mathlib.Analysis.CStarAlgebra.ContinuousFunctionalCalculus.Order
open MeasureTheory ProbabilityTheory
open scoped ContDiff NNReal ENNReal Topology
set_option autoImplicit false
set_option maxHeartbeats 1000000
#check (fun
    {Ω : Type*} [MeasurableSpace Ω] (μ : Measure Ω)
    (D : Lp ℝ 2 μ →L[ℝ] Lp ℝ 2 μ) (hD : D.IsPositive) =>
    ∃ Γ : Lp ℝ 2 μ →L[ℝ] Lp ℝ 2 μ,
      Γ.IsPositive ∧ Γ*Γ = D ∧
      ∀ u : Lp ℝ 2 μ, ‖Γ u‖^2 = inner ℝ (D u) u : _)
