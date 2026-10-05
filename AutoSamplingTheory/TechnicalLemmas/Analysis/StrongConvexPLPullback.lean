import AutoSamplingTheory.TechnicalLemmas.Analysis.StrongConvexFirstOrder
import Mathlib.Analysis.InnerProductSpace.Adjoint
import Mathlib.Analysis.Calculus.FDeriv.Comp

/-!
# A numerical PL inequality after nonlinear reparametrization

Chewi arXiv:2605.07006v1 Exercise 2.3, with the attained-minimum convention
from Section 2. The derivative maps from the parameter space to the objective
space; the source's transposed Jacobian is its adjoint. We prove the numerical
inequality for differentiable maps on complete real Hilbert spaces, including
the degenerate zero lower bound. This does not assert continuous differentiability
of the composite, uniqueness of a minimizing preimage, or convexity of the composite.
-/

namespace AutoSamplingTheory.TechnicalLemmas.Analysis.StrongConvexPLPullback

open Set
open scoped RealInnerProductSpace

variable {E F : Type*}
  [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E]
  [NormedAddCommGroup F] [InnerProductSpace ℝ F] [CompleteSpace F]

set_option backward.isDefEq.respectTransparency false in
/-- Surjectivity lifts the attained minimum, and the adjoint derivative's
coercivity transports strongly convex gap control to the actual composite gradient. -/
theorem exists_minimizer_and_pl {f : F → ℝ} {g : E → F} {α σ : ℝ} {z : F}
    (hα : 0 < α) (hσ : 0 ≤ σ) (hsc : StrongConvexOn univ α f)
    (hf : Differentiable ℝ f) (hg : Differentiable ℝ g)
    (hsurj : Function.Surjective g) (hz : IsMinOn f univ z)
    (hjac : ∀ x v, σ * ‖v‖ ^ 2 ≤
      inner ℝ v ((fderiv ℝ g x) ((fderiv ℝ g x).adjoint v))) :
    ∃ xstar, g xstar = z ∧ IsMinOn (f ∘ g) univ xstar ∧
      ∀ x, 2 * (α * σ) * ((f ∘ g) x - (f ∘ g) xstar) ≤
        ‖gradient (f ∘ g) x‖ ^ 2 := by
  obtain ⟨xstar, hxstar⟩ := hsurj z
  refine ⟨xstar, hxstar, ?_, ?_⟩
  · intro x _
    simpa [Function.comp_def, hxstar] using hz (mem_univ (g x))
  · intro x
    have hfirst := StrongConvexFirstOrder.firstOrder_lower_bound_of_strongConvexOn
      hsc (fun y _ => (hf y).hasGradientAt) (mem_univ (g x)) (mem_univ z)
    have hcs := real_inner_le_norm (gradient f (g x)) (g x - z)
    have hbase : 2 * α * (f (g x) - f z) ≤ ‖gradient f (g x)‖ ^ 2 := by
      rw [← neg_sub (g x) z, inner_neg_right, norm_neg] at hfirst
      nlinarith [sq_nonneg (‖gradient f (g x)‖ - α * ‖g x - z‖)]
    have hchain : HasGradientAt (f ∘ g)
        ((fderiv ℝ g x).adjoint (gradient f (g x))) x := by
      apply hasGradientAt_iff_hasFDerivAt.mpr
      have hc := (hf (g x)).hasGradientAt.hasFDerivAt.comp x (hg x).hasFDerivAt
      have heq : (InnerProductSpace.toDual ℝ F (gradient f (g x))).comp (fderiv ℝ g x) =
          InnerProductSpace.toDual ℝ E ((fderiv ℝ g x).adjoint (gradient f (g x))) := by
        ext v
        simp [InnerProductSpace.toDual_apply_apply, ContinuousLinearMap.adjoint_inner_left]
      rw [heq] at hc
      exact hc
    have hcoerc := hjac x (gradient f (g x))
    rw [← ContinuousLinearMap.adjoint_inner_left, real_inner_self_eq_norm_sq] at hcoerc
    have hmul := mul_le_mul_of_nonneg_left hbase hσ
    rw [hchain.gradient]
    dsimp only [Function.comp_def]
    rw [hxstar]
    nlinarith

end AutoSamplingTheory.TechnicalLemmas.Analysis.StrongConvexPLPullback
