import AutoSamplingTheory.TechnicalLemmas.Analysis.GradientFlowValue
import Mathlib.Analysis.Calculus.Deriv.Pow

open AutoSamplingTheory.TechnicalLemmas.Analysis.GradientFlowValue Set

set_option backward.isDefEq.respectTransparency false
set_option backward.isDefEq.respectTransparency.types false

-- One nonstationary actual quadratic flow exercises every curvature alpha in
-- [0,1], in particular both branches alpha=0 and alpha=1 with positive gap.
example (α T : ℝ) (hα : 0 ≤ α) (ha : α ≤ 1) (hT : 0 ≤ T) :
    ∀ t ∈ Ioc 0 T, 0 ≤ Real.exp (-t) ^ 2 / 2 ∧
      Real.exp (-t) ^ 2 / 2 ≤ if α = 0 then 1 / (2 * t)
        else α / (2 * (Real.exp (α * t) - 1)) := by
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
  have hm : IsMinOn f univ 0 := by
    intro x _
    dsimp [f]
    nlinarith [sq_nonneg x]
  have hflow (t : ℝ) : HasDerivAt (fun s : ℝ => Real.exp (-s))
      (-gradient f (Real.exp (-t))) t := by
    rw [hg]
    simpa using (hasDerivAt_id t).neg.exp
  have h := value_le hα hT (fun x => (hd x).differentiableAt)
    (hsc.mono ha) hm (Real.continuous_exp.comp continuous_neg).continuousOn
    (fun t _ => (hflow t).hasDerivWithinAt)
  simpa [f] using h

-- Endpoint source-gap witness: the displayed quotient with Lean's total /0
-- would falsely force the positive initial gap of that flow to vanish.
example : ¬ ((1 : ℝ) / 2 ≤ 1 / (2 * (Real.exp (1 * 0) - 1)) * ‖(1 : ℝ) - 0‖ ^ 2) := by
  norm_num

#print axioms AutoSamplingTheory.TechnicalLemmas.Analysis.GradientFlowValue.value_le
