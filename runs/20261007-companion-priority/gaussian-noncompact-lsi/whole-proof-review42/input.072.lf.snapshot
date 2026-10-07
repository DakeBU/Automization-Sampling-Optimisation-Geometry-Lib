import AutoSamplingTheory.TechnicalLemmas.Analysis.ConvexityC2

/-!
# One-sided smoothness equivalences

Chewi, Lectures on Optimization, arXiv:2605.07006v1, Definition 1.12
and Proposition 1.13. Apply the signed lower-bound interfaces to -f.
The complete-space and signed-parameter scope is an explicit generalization.
No convexity or Lipschitz-gradient conclusion is asserted.
-/

namespace AutoSamplingTheory.TechnicalLemmas.Analysis.SmoothnessEquivalences

open Set
open scoped RealInnerProductSpace

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E]

/-- The global quadratic upper model is equivalent to a one-sided gradient
bound. The parameter is allowed to be signed. -/
theorem upper_model_iff_gradient_upper {f : E → ℝ} {β : ℝ}
    (hf : ContDiff ℝ 1 f) :
    (∀ x y, f y ≤ f x + inner ℝ (gradient f x) (y - x) + β / 2 * ‖y - x‖ ^ 2) ↔
    ∀ x y, inner ℝ (gradient f y - gradient f x) (y - x) ≤ β * ‖y - x‖ ^ 2 := by
  have hg (x : E) : gradient (fun z => -f z) x = -gradient f x := by
    simp [gradient]
  constructor
  · intro h x y
    have hxy := h x y
    have hyx := h y x
    rw [show x - y = -(y - x) by abel, inner_neg_right, norm_neg] at hyx
    rw [inner_sub_left]
    linarith
  · intro h
    have hn : StrongConvexOn (univ : Set E) (-β) (fun z => -f z) :=
      ConvexityC1.strongConvexOn_univ_of_gradient_mono_integral hf.neg (by
        intro x y
        rw [hg, hg, inner_sub_left, inner_neg_left, inner_neg_left]
        have hxy := h x y
        rw [inner_sub_left] at hxy
        linarith)
    intro x y
    have hl := StrongConvexFirstOrder.firstOrder_lower_bound_of_strongConvexOn hn
      (fun z _ => (hf.neg.differentiable_one z).hasGradientAt) (mem_univ x) (mem_univ y)
    rw [hg, inner_neg_left] at hl
    linarith

/-- With genuine C² regularity the same upper model is equivalent to the
Hessian diagonal upper bound, without assuming convexity. -/
theorem upper_model_iff_fderiv2_upper {f : E → ℝ} {β : ℝ}
    (hf : ContDiff ℝ 2 f) :
    (∀ x y, f y ≤ f x + inner ℝ (gradient f x) (y - x) + β / 2 * ‖y - x‖ ^ 2) ↔
    ∀ x v, (fderiv ℝ (fderiv ℝ f) x v) v ≤ β * ‖v‖ ^ 2 := by
  have hg (x : E) : gradient (fun z => -f z) x = -gradient f x := by
    simp [gradient]
  have hH (x v : E) :
      (fderiv ℝ (fderiv ℝ (fun z => -f z)) x v) v =
        -(fderiv ℝ (fderiv ℝ f) x v) v := by
    rw [show fderiv ℝ (fun z => -f z) = -fderiv ℝ f by
      funext z; exact fderiv_fun_neg]
    rw [fderiv_neg]
    rfl
  rw [upper_model_iff_gradient_upper (hf.of_le (by norm_num))]
  have h := ConvexityC2.gradient_mono_iff_fderiv2_lower (m := -β) hf.neg
  simp only [hg, inner_sub_left, inner_neg_left, hH] at h
  constructor
  · intro hu x v
    have hl := h.mp (by
      intro x y
      have hxy := hu x y
      rw [inner_sub_left] at hxy
      linarith) x v
    linarith
  · intro hu x y
    have hl := h.mpr (by intro x v; have hv := hu x v; linarith) x y
    rw [inner_sub_left]
    linarith

end AutoSamplingTheory.TechnicalLemmas.Analysis.SmoothnessEquivalences
