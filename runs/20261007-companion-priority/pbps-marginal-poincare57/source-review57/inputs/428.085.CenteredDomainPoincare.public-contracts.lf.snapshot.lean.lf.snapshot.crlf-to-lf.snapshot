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
    let μ := (volume : Measure E).tilted (fun x => -W x)
    ∀ (D : Lp ℝ 2 μ →ₗ.[ℝ] Lp E 2 μ), D.IsClosable →
      (∀ (a : Lp ℝ 2 μ) (G : Lp E 2 μ), (a,G) ∈ D.graph ↔
        ∃ φ : E → ℝ, ContDiff ℝ ∞ φ ∧ HasCompactSupport φ ∧
          a =ᵐ[μ] φ ∧ G =ᵐ[μ] gradient φ) →
      ∀ z : D.closure.domain, (∫ x, (z : Lp ℝ 2 μ) x ∂μ)=0 →
        m*‖(z : Lp ℝ 2 μ)‖^2 ≤ ‖D.closure z‖^2 