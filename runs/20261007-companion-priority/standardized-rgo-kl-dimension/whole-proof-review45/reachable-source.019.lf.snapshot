import AutoSamplingTheory.TechnicalLemmas.Analysis.StrongConvexFirstOrder
import AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability

/-!
# Gibbs integrability without a supplied minimizer

A differentiable potential with positive strong-convexity modulus has an
integrable exponential Gibbs weight on finite-dimensional Lebesgue space.
The proof uses the existing first-order lower bound at the fixed point zero,
not an assumed or constructed minimizer. Its Gaussian envelope is obtained
by absorbing the linear term with Young's inequality.

This is a shared normalization prerequisite for the targets in Chen, Chewi,
Lu and Zhang, arXiv:2609.06906v1 Section 6.2.2 and arXiv:2609.06905v1 Section 2.1.
The papers' Hessian-to-`StrongConvexOn` adapter is a separate obligation;
neither their Gibbs initialization nor a sampling theorem is asserted here.
-/

namespace AutoSamplingTheory.TechnicalLemmas.Analysis.StrongConvexGibbsIntegrability

open MeasureTheory
open scoped RealInnerProductSpace

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]

/-- A differentiable strongly convex potential has an integrable Gibbs weight
for canonical volume. Positive modulus is essential to the Gaussian-envelope
argument. No minimizer, gradient field, or normalizer is supplied as an extra
assumption; differentiability supplies the genuine gradient used at zero. -/
theorem integrable_exp_neg_of_strongConvexOn {V : E → ℝ} {m : ℝ}
    (hm : 0 < m) (hV : Differentiable ℝ V)
    (hsc : StrongConvexOn Set.univ m V) :
    Integrable (fun x => Real.exp (-V x)) (volume : Measure E) := by
  let g : E := gradient V 0
  let b : ℝ := V 0 - (m / 2)⁻¹ / 2 * ‖g‖ ^ 2
  have hquad : ∀ x : E, m / 4 * ‖x‖ ^ 2 + b ≤ V x := by
    intro x
    have hfirst : V 0 + inner ℝ g x + m / 2 * ‖x‖ ^ 2 ≤ V x := by
      simpa only [g, sub_zero] using
        StrongConvexFirstOrder.firstOrder_lower_bound_of_strongConvexOn hsc
          (fun z _ => (hV z).hasGradientAt) (x := 0) (y := x)
          (Set.mem_univ _) (Set.mem_univ _)
    have hinner := (abs_le.mp (abs_real_inner_le_norm g x)).1
    have hyoung := two_mul_le_add_mul_sq (a := ‖x‖) (b := ‖g‖)
      (show 0 < m / 2 by positivity)
    dsimp only [b]
    nlinarith
  have hbound := Integrability.integrable_exp_neg_add_mul_norm_sq
    (E := E) (a := m / 4) (b := b) (by positivity)
  refine hbound.mono' ((Real.continuous_exp.comp hV.continuous.neg).aestronglyMeasurable) ?_
  filter_upwards with x
  rw [Real.norm_eq_abs, abs_of_pos (Real.exp_pos _)]
  exact Real.exp_le_exp.mpr (neg_le_neg (hquad x))

end AutoSamplingTheory.TechnicalLemmas.Analysis.StrongConvexGibbsIntegrability
