import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GibbsC1Poincare
import Mathlib.Probability.Moments.CovarianceBilin
namespace AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GibbsLinearCovarianceUpper
open MeasureTheory ProbabilityTheory InnerProductSpace
open scoped RealInnerProductSpace
noncomputable section
set_option autoImplicit false
set_option backward.isDefEq.respectTransparency false

theorem gibbs_linear_covariance_upper
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E] [CompleteSpace E]
    (W : E → ℝ) (hW : ContDiff ℝ 2 W)
    (hI : Integrable (fun x => Real.exp (-W x)))
    (hZ : 0 < ∫ x, Real.exp (-W x))
    (m M : ℝ) (hm : 0 < m) (hmM : m ≤ M)
    (hlower : ∀ x a, m*‖a‖^2 ≤ fderiv ℝ (fderiv ℝ W) x a a)
    (hupper : ∀ x a, fderiv ℝ (fderiv ℝ W) x a a ≤ M*‖a‖^2)
    (hX : MemLp id 2 ((volume : Measure E).tilted (fun x => -W x))) :
    let μ := (volume : Measure E).tilted (fun x => -W x)
    ∀ a : E, ProbabilityTheory.covarianceBilin μ a a ≤ ‖a‖^2/m 