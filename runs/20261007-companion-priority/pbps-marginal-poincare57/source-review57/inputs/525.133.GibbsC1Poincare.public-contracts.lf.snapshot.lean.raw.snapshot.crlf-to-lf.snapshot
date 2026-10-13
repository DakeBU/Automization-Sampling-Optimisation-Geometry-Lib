import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.CenteredDomainPoincare
import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.WeightedC1GradientDomain
import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare
set_option autoImplicit false
noncomputable section
open Filter InnerProductSpace MeasureTheory
open scoped Topology RealInnerProductSpace ContDiff
namespace AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GibbsC1Poincare

theorem gibbs_c1_variance_poincare
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    (W : E → ℝ) (hW : ContDiff ℝ 2 W)
    (hI : Integrable (fun x => Real.exp (-W x)))
    (hZ : 0 < ∫ x, Real.exp (-W x))
    (m M : ℝ) (hm : 0 < m) (hmM : m ≤ M)
    (hlower : ∀ x a, m*‖a‖^2 ≤ fderiv ℝ (fderiv ℝ W) x a a)
    (hupper : ∀ x a, fderiv ℝ (fderiv ℝ W) x a a ≤ M*‖a‖^2) :
    let μ := (volume : Measure E).tilted (fun x => -W x)
    ∀ f : E → ℝ, ContDiff ℝ 1 f → MemLp f 2 μ → MemLp (gradient f) 2 μ →
      AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare.Admissible μ f ∧
      m*AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare.variance μ f ≤
        AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare.dirichletEnergy μ f 