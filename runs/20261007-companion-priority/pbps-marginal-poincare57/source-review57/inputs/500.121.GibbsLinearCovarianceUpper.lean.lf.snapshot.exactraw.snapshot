import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GibbsC1Poincare
import Mathlib.Probability.Moments.CovarianceBilin

/-! Actual isotropic covariance upper from the original closed-gradient Poincare
producer. The observable is the genuine linear functional, its gradient is the
constant direction, and normalized Dirichlet energy is exactly its squared norm.
Actual vectorL2 is explicit in this canonical interface because Mathlib's
covarianceBilin is totalized outside that domain. The source SPHMC consumer must
produce this moment internally. BOTH curvature bounds are explicit; no full
anisotropic Brascamp-Lieb or sampler/main claim. -/

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
    ∀ a : E, ProbabilityTheory.covarianceBilin μ a a ≤ ‖a‖^2/m := by
  let μ := (volume : Measure E).tilted (fun x => -W x)
  let : IsProbabilityMeasure μ := isProbabilityMeasure_tilted hI
  dsimp only
  intro a
  let f : E → ℝ := fun x => inner ℝ a x
  have hf : ContDiff ℝ 1 f := (innerSL ℝ a).contDiff
  have hp : MemLp f 2 μ := hX.const_inner a
  have hgrad : gradient f = fun _ => a := by
    funext x
    apply (toDual ℝ E).injective
    rw [toDual_gradient]
    exact (innerSL ℝ a).fderiv
  have hq : MemLp (gradient f) 2 μ := hgrad ▸ memLp_const a
  obtain ⟨_, hb⟩ := GibbsC1Poincare.gibbs_c1_variance_poincare
    W hW hI hZ m M hm hmM hlower hupper f hf hp hq
  have henergy : Poincare.dirichletEnergy μ f = ‖a‖^2 := by
    simp only [Poincare.dirichletEnergy, hgrad]
    simp
  rw [henergy] at hb
  have hcov : covarianceBilin μ a a = Poincare.variance μ f := by
    rw [covarianceBilin_self hX a, variance_eq_integral hp.aemeasurable]
    rfl
  rw [hcov]
  exact (le_div_iff₀ hm).2 (by simpa only [mul_comm] using hb)

end
end AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GibbsLinearCovarianceUpper
