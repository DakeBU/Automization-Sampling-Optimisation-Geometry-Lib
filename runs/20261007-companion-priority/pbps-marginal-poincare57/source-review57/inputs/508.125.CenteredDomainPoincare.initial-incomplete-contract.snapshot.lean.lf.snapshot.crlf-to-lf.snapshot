import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.CenteredGibbsResolventLimit
import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GlobalWeightedResolventCoercivity
set_option autoImplicit false
noncomputable section
open Filter InnerProductSpace MeasureTheory
open scoped Topology RealInnerProductSpace ContDiff
namespace AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.CenteredDomainPoincare

theorem gibbs_centered_domain_poincare
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    (W : E → ℝ) (hW : ContDiff ℝ 2 W)
    (hI : Integrable (fun x => Real.exp (-W x)))
    (hZ : 0 < ∫ x, Real.exp (-W x))
    (m M : ℝ) (hm : 0 < m) (hmM : m ≤ M)
    (hlower : ∀ x a, m*‖a‖^2 ≤ fderiv ℝ (fderiv ℝ W) x a a)
    (hupper : ∀ x a, fderiv ℝ (fderiv ℝ W) x a a ≤ M*‖a‖^2) :
    let μ 