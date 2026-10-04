import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.BoundedStoppedItoMean

namespace AutoSamplingTheory.Tests.BoundedStoppedItoMean

open MeasureTheory
open AutoSamplingTheory.TechnicalLemmas.StochasticProcesses
open BoundedStoppedItoMean BrownianMotion ItoIntegralProcess ProgressiveL2 StoppingTime
open scoped NNReal

noncomputable section

variable {Omega : Type*} {m : MeasurableSpace Omega}
  {filtration : Filtration ℝ≥0 m} {mu : Measure Omega} {T : ℝ≥0}
  {B : ℝ≥0 → Omega → ℝ}

#check itoIntegralProcess_at_boundedStopping_integrable
#check integral_itoIntegralProcess_at_boundedStopping_eq_zero

example [IsFiniteMeasure mu]
    (eta : ProgressiveL2Integrand filtration mu T) (hT : 0 < T)
    (tau : Omega → ℝ≥0)
    (htau : IsChewiStoppingTime filtration
      (fun omega => (tau omega : WithTop ℝ≥0)))
    (htauT : ∀ omega, tau omega ≤ T)
    (hB : IsBrownianMotionWithFiltration B filtration mu)
    (hUsual : SatisfiesUsualConditions filtration mu) :
    Integrable
        (fun omega => itoIntegralProcess eta hT hB hUsual (tau omega) omega) mu ∧
      ∫ omega, itoIntegralProcess eta hT hB hUsual (tau omega) omega ∂mu = 0 := by
  exact ⟨itoIntegralProcess_at_boundedStopping_integrable
      eta hT tau htau htauT hB hUsual,
    integral_itoIntegralProcess_at_boundedStopping_eq_zero
      eta hT tau htau htauT hB hUsual⟩

end
end AutoSamplingTheory.Tests.BoundedStoppedItoMean
