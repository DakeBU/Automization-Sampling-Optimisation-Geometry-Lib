import AutoSamplingTheory.TechnicalLemmas.Analysis.StrongConvexFirstOrder
import Mathlib.Analysis.InnerProductSpace.Calculus
import Mathlib.Analysis.ODE.Gronwall

/-!
# Objective rate for a convex gradient flow

Chewi, arXiv:2605.07006v1, Theorem 2.4. The finite real-valued rate needs
positive observation time. The zero-curvature coefficient is written explicitly.
The flow and its minimizer are supplied; no well-posedness is asserted.
-/

namespace AutoSamplingTheory.TechnicalLemmas.Analysis.GradientFlowValue

open Set
open scoped RealInnerProductSpace

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E]

/-- The objective gap along an actual convex gradient trajectory, including the
zero-curvature rate, at every positive time of a supplied forward interval. -/
theorem value_le {f : E → ℝ} {X : ℝ → E} {z : E} {α T : ℝ}
    (hα : 0 ≤ α) (_hT : 0 ≤ T) (hf : Differentiable ℝ f)
    (hsc : StrongConvexOn univ α f) (hz : IsMinOn f univ z)
    (hX : ContinuousOn X (Icc 0 T))
    (hflow : ∀ t ∈ Ico 0 T, HasDerivWithinAt X (-gradient f (X t)) (Ici t) t) :
    ∀ t ∈ Ioc 0 T, 0 ≤ f (X t) - f z ∧
      f (X t) - f z ≤ if α = 0 then ‖X 0 - z‖ ^ 2 / (2 * t)
        else α / (2 * (Real.exp (α * t) - 1)) * ‖X 0 - z‖ ^ 2 := by
  have hd (u : ℝ) (hu : u ∈ Ico 0 T) :
      HasDerivWithinAt (fun s => f (X s)) (-‖gradient f (X u)‖ ^ 2) (Ici u) u := by
    have hgrad : HasFDerivAt f (InnerProductSpace.toDual ℝ E (gradient f (X u))) (X u) :=
      (hf (X u)).hasGradientAt
    simpa only [Function.comp_def, InnerProductSpace.toDual_apply_apply,
      inner_neg_right, real_inner_self_eq_norm_sq] using
      hgrad.comp_hasDerivWithinAt u (hflow u hu)
  have hmono : AntitoneOn (fun s => f (X s)) (Icc 0 T) := by
    intro a ha b hb hab
    have hc := (hf.continuous.comp_continuousOn hX).mono
      (show Icc a b ⊆ Icc 0 T from fun u hu => ⟨ha.1.trans hu.1, hu.2.trans hb.2⟩)
    have hg := le_gronwallBound_of_liminf_deriv_right_le
      (f' := fun u => -‖gradient f (X u)‖ ^ 2) (δ := f (X a)) (K := 0) (ε := 0) hc
      (fun u hu r hr => by
        simpa [slope] using (hd u ⟨ha.1.trans hu.1, hu.2.trans_le hb.2⟩).liminf_right_slope_le hr)
      le_rfl (fun u _ => by nlinarith [sq_nonneg ‖gradient f (X u)‖]) b ⟨hab, le_rfl⟩
    simpa [gronwallBound_K0] using hg
  have hdist (u : ℝ) (hu : u ∈ Ico 0 T) :
      HasDerivWithinAt (fun s => ‖X s - z‖ ^ 2)
        (-2 * inner ℝ (gradient f (X u)) (X u - z)) (Ici u) u := by
    have h := ((hflow u hu).sub_const z).norm_sq
    simp only [inner_neg_right, real_inner_comm] at h
    convert h using 1; ring
  intro t ht
  refine ⟨sub_nonneg.mpr (hz (mem_univ _)), ?_⟩
  have hbound := le_gronwallBound_of_liminf_deriv_right_le
    (f := fun s => ‖X s - z‖ ^ 2)
    (f' := fun u => -2 * inner ℝ (gradient f (X u)) (X u - z))
    (δ := ‖X 0 - z‖ ^ 2) (K := -α) (ε := -2 * (f (X t) - f z))
    (((hX.sub continuousOn_const).norm.pow 2).mono
      (show Icc 0 t ⊆ Icc 0 T from fun u hu => ⟨hu.1, hu.2.trans ht.2⟩))
    (fun u hu r hr => by
      simpa [slope] using (hdist u ⟨hu.1, hu.2.trans_le ht.2⟩).liminf_right_slope_le hr)
    le_rfl (fun u hu => by
      have hs := StrongConvexFirstOrder.firstOrder_lower_bound_of_strongConvexOn
        hsc (fun x _ => (hf x).hasGradientAt) (mem_univ (X u)) (mem_univ z)
      rw [show z - X u = -(X u - z) by abel, inner_neg_right, norm_neg] at hs
      have hm := hmono ⟨hu.1, hu.2.le.trans ht.2⟩ ⟨ht.1.le, ht.2⟩ hu.2.le
      nlinarith) t ⟨ht.1.le, le_rfl⟩
  have hn := (sq_nonneg ‖X t - z‖).trans hbound
  by_cases ha : α = 0
  · simp only [ha, neg_zero, gronwallBound_K0, sub_zero] at hn ⊢
    apply (le_div_iff₀ (mul_pos (by norm_num) ht.1)).mpr
    nlinarith
  · rw [if_neg ha]
    have hap : 0 < α := lt_of_le_of_ne hα (Ne.symm ha)
    rw [gronwallBound_of_K_ne_0 (neg_ne_zero.mpr ha), sub_zero] at hn
    have hmul := mul_nonneg hn hap.le
    have heq : (‖X 0 - z‖ ^ 2 * Real.exp (-α * t) +
        (-2 * (f (X t) - f z)) / -α * (Real.exp (-α * t) - 1)) * α =
        α * ‖X 0 - z‖ ^ 2 * Real.exp (-α * t) +
          2 * (f (X t) - f z) * (Real.exp (-α * t) - 1) := by
      field_simp
    rw [heq] at hmul
    have he : Real.exp (-α * t) * Real.exp (α * t) = 1 := by
      rw [← Real.exp_add, show -α * t + α * t = 0 by ring, Real.exp_zero]
    have hp := mul_nonneg hmul (Real.exp_pos (α * t)).le
    have hcancel : (α * ‖X 0 - z‖ ^ 2 * Real.exp (-α * t) +
        2 * (f (X t) - f z) * (Real.exp (-α * t) - 1)) * Real.exp (α * t) =
        α * ‖X 0 - z‖ ^ 2 - 2 * (f (X t) - f z) * (Real.exp (α * t) - 1) := by
      calc
        _ = α * ‖X 0 - z‖ ^ 2 * (Real.exp (-α * t) * Real.exp (α * t)) +
          2 * (f (X t) - f z) * (Real.exp (-α * t) * Real.exp (α * t)) -
          2 * (f (X t) - f z) * Real.exp (α * t) := by ring
        _ = _ := by rw [he]; ring
    rw [hcancel] at hp
    rw [div_mul_eq_mul_div]
    apply (le_div_iff₀ (mul_pos (by norm_num) (sub_pos.mpr (Real.one_lt_exp_iff.mpr
      (mul_pos hap ht.1))))).mpr
    nlinarith

end AutoSamplingTheory.TechnicalLemmas.Analysis.GradientFlowValue
