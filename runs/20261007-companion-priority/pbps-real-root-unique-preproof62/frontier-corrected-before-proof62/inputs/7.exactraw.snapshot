import AutoSamplingTheory.ExampleCases.ProximalBPS.RealDefectRoot
open MeasureTheory ProbabilityTheory
open scoped ContDiff NNReal ENNReal Topology
set_option autoImplicit false
set_option maxHeartbeats 1000000
#check (fun
    {Ω : Type*} [MeasurableSpace Ω] (μ : Measure Ω)
    (A B : Lp ℝ 2 μ →L[ℝ] Lp ℝ 2 μ)
    (hA : A.IsPositive) (hB : B.IsPositive) (hSq : A*A=B*B) =>
    A=B
 : _)
