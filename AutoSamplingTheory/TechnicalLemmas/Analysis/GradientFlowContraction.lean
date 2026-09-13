import AutoSamplingTheory.TechnicalLemmas.Analysis.StrongConvexFirstOrder
import Mathlib.Analysis.InnerProductSpace.Calculus
import Mathlib.Analysis.ODE.Gronwall

/-!
# Contraction of two actual gradient flows

Chewi, arXiv:2605.07006v1, Theorem 2.2. Derive the squared separation
inequality from the supplied gradient ODEs and existing gradient monotonicity.
Only forward right derivatives before the terminal time are required.
-/

namespace AutoSamplingTheory.TechnicalLemmas.Analysis.GradientFlowContraction

open Set
open scoped RealInnerProductSpace

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E]

/-- Two supplied gradient trajectories contract on every finite forward interval.
Zero curvature gives nonexpansiveness; positive curvature gives exponential decay.
No existence of a trajectory or of a minimizer is asserted. -/
theorem norm_sub_le {f : E → ℝ} {X Y : ℝ → E} {α T : ℝ}
    (_hα : 0 ≤ α) (_hT : 0 ≤ T) (hf : Differentiable ℝ f)
    (hsc : StrongConvexOn univ α f)
    (hX : ContinuousOn X (Icc 0 T)) (hY : ContinuousOn Y (Icc 0 T))
    (hx : ∀ t ∈ Ico 0 T, HasDerivWithinAt X (-gradient f (X t)) (Ici t) t)
    (hy : ∀ t ∈ Ico 0 T, HasDerivWithinAt Y (-gradient f (Y t)) (Ici t) t) :
    ∀ t ∈ Icc 0 T, ‖Y t - X t‖ ≤ Real.exp (-α * t) * ‖Y 0 - X 0‖ := by
  have hd (t : ℝ) (ht : t ∈ Ico 0 T) :
      HasDerivWithinAt (fun u => ‖Y u - X u‖ ^ 2)
        (-2 * inner ℝ (gradient f (Y t) - gradient f (X t)) (Y t - X t))
        (Ici t) t := by
    have h := ((hy t ht).sub (hx t ht)).norm_sq
    simp only [Pi.sub_apply] at h
    rw [show -gradient f (Y t) - -gradient f (X t) =
      -(gradient f (Y t) - gradient f (X t)) by abel,
      inner_neg_right, real_inner_comm] at h
    convert h using 1; ring
  intro t ht
  have hg := le_gronwallBound_of_liminf_deriv_right_le
    (f := fun u => ‖Y u - X u‖ ^ 2)
    (f' := fun u => -2 * inner ℝ (gradient f (Y u) - gradient f (X u)) (Y u - X u))
    (δ := ‖Y 0 - X 0‖ ^ 2) (K := -(2 * α)) (ε := 0)
    ((hY.sub hX).norm.pow 2)
    (fun u hu r hr => by simpa [slope] using (hd u hu).liminf_right_slope_le hr)
    le_rfl (fun u _ => by
      have hm := StrongConvexFirstOrder.gradient_inner_lower_bound_of_strongConvexOn
        hsc (fun z _ => (hf z).hasGradientAt) (mem_univ (X u)) (mem_univ (Y u))
      nlinarith) t ht
  have hs : ‖Y t - X t‖ ^ 2 ≤ (Real.exp (-α * t) * ‖Y 0 - X 0‖) ^ 2 := by
    rw [mul_pow, show Real.exp (-α * t) ^ 2 = Real.exp (-(2 * α) * t) by
      rw [sq, ← Real.exp_add]; congr 1; ring, mul_comm]
    simpa only [gronwallBound_ε0, sub_zero] using hg
  exact (sq_le_sq₀ (norm_nonneg _) (mul_nonneg (Real.exp_pos _).le (norm_nonneg _))).mp hs

end AutoSamplingTheory.TechnicalLemmas.Analysis.GradientFlowContraction
