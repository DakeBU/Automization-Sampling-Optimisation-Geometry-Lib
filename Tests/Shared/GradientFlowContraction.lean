import AutoSamplingTheory.TechnicalLemmas.Analysis.GradientFlowContraction
import Mathlib.Analysis.Calculus.Deriv.Pow

open AutoSamplingTheory.TechnicalLemmas.Analysis.GradientFlowContraction Set

set_option backward.isDefEq.respectTransparency false
set_option backward.isDefEq.respectTransparency.types false

-- Two distinct nonstationary solutions of f(x)=x²/2. All ODE and convexity
-- premises are derived, and arbitrary initial positions include coincident flows.
example (a b T : ℝ) (hT : 0 ≤ T) :
    ∀ t ∈ Icc 0 T, ‖b * Real.exp (-t) - a * Real.exp (-t)‖ ≤
      Real.exp (-t) * ‖b - a‖ := by
  let f : ℝ → ℝ := fun x => x ^ 2 / 2
  have hd (x : ℝ) : HasDerivAt f x x := by
    convert ((hasDerivAt_id x).pow 2).div_const 2 using 1 <;>
      first | rfl | (simp only [id_eq]; ring)
  have hg (x : ℝ) : gradient f x = x := (hd x).hasGradientAt'.gradient
  have hsc : StrongConvexOn univ 1 f := by
    rw [strongConvexOn_iff_convex]
    have he : (fun x : ℝ => f x - 1 / 2 * ‖x‖ ^ 2) = fun _ => 0 := by
      funext x
      simp only [f, Real.norm_eq_abs, sq_abs]
      ring
    rw [he]
    exact convexOn_const (0 : ℝ) convex_univ
  have hflow (c t : ℝ) : HasDerivAt (fun s : ℝ => c * Real.exp (-s))
      (-gradient f (c * Real.exp (-t))) t := by
    rw [hg]
    simpa using ((hasDerivAt_id t).neg.exp.const_mul c)
  have h := norm_sub_le (by norm_num : (0 : ℝ) ≤ 1) hT
    (fun x => (hd x).differentiableAt) hsc
    ((Real.continuous_exp.comp continuous_neg).const_mul a).continuousOn
    ((Real.continuous_exp.comp continuous_neg).const_mul b).continuousOn
    (fun t _ => (hflow a t).hasDerivWithinAt)
    (fun t _ => (hflow b t).hasDerivWithinAt)
  simpa using h

-- The rate is exact, not just a zero-initial-distance check.
example (a b t : ℝ) : ‖b * Real.exp (-t) - a * Real.exp (-t)‖ =
    Real.exp (-t) * ‖b - a‖ := by
  rw [← sub_mul, norm_mul, Real.norm_of_nonneg (Real.exp_pos _).le, mul_comm]

-- Zero curvature: constant objective, distinct stationary trajectories.
example (a b T : ℝ) (hT : 0 ≤ T) :
    ∀ t ∈ Icc 0 T, ‖b - a‖ ≤ ‖b - a‖ := by
  have hg (x : ℝ) : gradient (fun _ : ℝ => (0 : ℝ)) x = 0 :=
    (hasDerivAt_const x (0 : ℝ)).hasGradientAt'.gradient
  have hsc : StrongConvexOn univ 0 (fun _ : ℝ => (0 : ℝ)) := by
    rw [strongConvexOn_iff_convex]
    simpa using convexOn_const (c := (0 : ℝ)) (convex_univ : Convex ℝ (univ : Set ℝ))
  have h := norm_sub_le (le_refl (0 : ℝ)) hT (differentiable_const (0 : ℝ)) hsc
    (X := fun _ => a) (Y := fun _ => b) continuousOn_const continuousOn_const
    (fun t _ => by simpa [hg] using (hasDerivAt_const t a).hasDerivWithinAt)
    (fun t _ => by simpa [hg] using (hasDerivAt_const t b).hasDerivWithinAt)
  simpa using h

#print axioms norm_sub_le
