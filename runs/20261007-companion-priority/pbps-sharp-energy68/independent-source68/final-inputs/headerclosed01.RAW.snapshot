import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualRootCommutation
open MeasureTheory ProbabilityTheory InnerProductSpace
open scoped RealInnerProductSpace ContDiff NNReal Topology ENNReal
noncomputable section
set_option autoImplicit false
set_option maxHeartbeats 2000000

theorem quadratic_corrector_bound_of_square_identity
    {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℝ H] [CompleteSpace H]
    (K D : H →L[ℝ] H) (hK : IsSelfAdjoint K) (hD : IsSelfAdjoint D)
    (hSquare : (1 : H →L[ℝ] H)+K*K=D*D)
    (c : ℝ) (hc : 0 ≤ c) (hNorm : ‖D‖ ≤ c) (u v : H) :
    |(1/2 : ℝ)*(‖u‖^2-‖v‖^2)-inner ℝ (K u) v| ≤
      (c/2)*(‖u‖^2+‖v‖^2)
