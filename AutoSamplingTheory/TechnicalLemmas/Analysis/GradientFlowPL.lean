import Mathlib.Analysis.Calculus.Gradient.Basic
import Mathlib.Analysis.ODE.Gronwall

/-!
# Actual gradient-flow dissipation and PL decay

Chewi, arXiv:2605.07006v1, Section 2, Lemma 2.1 and Corollary 2.6.
The curve is supplied only on a finite forward interval. We derive its objective
dissipation by the chain rule rather than assume a scalar energy identity.
No existence or uniqueness of the flow is asserted.
-/

namespace AutoSamplingTheory.TechnicalLemmas.Analysis.GradientFlowPL

open Set
open scoped RealInnerProductSpace

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E]

/-- Actual gradient dynamics imply energy dissipation and the PL objective rate,
including the initial and final endpoints of a finite nonnegative time interval. -/
theorem dissipation_and_decay {f : E → ℝ} {X : ℝ → E} {z : E} {α T : ℝ}
    (_hα : 0 < α) (_hT : 0 ≤ T) (hf : Differentiable ℝ f)
    (hX : ContinuousOn X (Icc 0 T))
    (hflow : ∀ t ∈ Ico 0 T,
      HasDerivWithinAt X (-gradient f (X t)) (Ici t) t)
    (hz : IsMinOn f univ z)
    (hpl : ∀ x, 2 * α * (f x - f z) ≤ ‖gradient f x‖ ^ 2) :
    (∀ t ∈ Ico 0 T, HasDerivWithinAt (f ∘ X)
      (-‖gradient f (X t)‖ ^ 2) (Ici t) t) ∧
    ∀ t ∈ Icc 0 T, 0 ≤ f (X t) - f z ∧
      f (X t) - f z ≤ (f (X 0) - f z) * Real.exp (-2 * α * t) := by
  have hd : ∀ t ∈ Ico 0 T, HasDerivWithinAt (f ∘ X)
      (-‖gradient f (X t)‖ ^ 2) (Ici t) t := by
    intro t ht
    have hgrad : HasFDerivAt f (InnerProductSpace.toDual ℝ E (gradient f (X t))) (X t) :=
      (hf (X t)).hasGradientAt
    have h := hgrad.comp_hasDerivWithinAt t (hflow t ht)
    simpa only [InnerProductSpace.toDual_apply_apply, inner_neg_right,
      real_inner_self_eq_norm_sq] using h
  refine ⟨hd, ?_⟩
  intro t ht
  refine ⟨sub_nonneg.mpr (hz (mem_univ (X t))), ?_⟩
  have hc : ContinuousOn (fun u => f (X u) - f z) (Icc 0 T) :=
    (hf.continuous.comp_continuousOn hX).sub continuousOn_const
  have hg := le_gronwallBound_of_liminf_deriv_right_le
    (f := fun u => f (X u) - f z) (f' := fun u => -‖gradient f (X u)‖ ^ 2)
    (δ := f (X 0) - f z) (K := -(2 * α)) (ε := 0) hc
    (fun u hu r hr => by
      simpa [Function.comp_def, slope] using
        ((hd u hu).sub_const (f z)).liminf_right_slope_le hr)
    le_rfl
    (fun u _ => by nlinarith [hpl (X u)]) t ht
  simpa [gronwallBound_ε0, sub_zero, neg_mul] using hg

end AutoSamplingTheory.TechnicalLemmas.Analysis.GradientFlowPL
