import AutoSamplingTheory.TechnicalLemmas.Analysis.GradientFlowLastIterate
import Mathlib.Analysis.Calculus.Deriv.Pow

open AutoSamplingTheory.TechnicalLemmas.Analysis.GradientFlowLastIterate Set

-- A genuine nonstationary quadratic trajectory tests all three conclusions,
-- including the closed-time Lyapunov statement when the horizon equals zero.
example (T : ℝ) (hT : 0 ≤ T) :
    AntitoneOn (fun t => t ^ 2 * ‖Real.exp (-t)‖ ^ 2 +
      2 * t * (Real.exp (-t) ^ 2 / 2) + ‖Real.exp (-t)‖ ^ 2) (Icc 0 T) ∧
    ∀ t ∈ Ioc 0 T, ‖Real.exp (-t)‖ ^ 2 ≤ 1 / t ^ 2 ∧
      Real.exp (-t) ^ 2 / 2 ≤ 1 / (4 * t) := by
  let f : ℝ → ℝ := fun x => x ^ 2 / 2
  have hd (x : ℝ) : HasDerivAt f x x := by
    convert ((hasDerivAt_id x).pow 2).div_const 2 using 1 <;>
      first | rfl | (simp only [id_eq]; ring)
  have hg (x : ℝ) : gradient f x = x := (hd x).hasGradientAt'.gradient
  have hf : ContDiff ℝ 2 f := contDiff_id.pow 2 |>.div_const 2
  have hc : ConvexOn ℝ univ f := by
    have h := ConvexOn.smul (by norm_num : 0 ≤ (1 / 2 : ℝ))
      ((by decide : Even (2 : ℕ)).convexOn_pow (𝕜 := ℝ))
    simpa [f, smul_eq_mul, div_eq_mul_inv, mul_comm] using h
  have hm : IsMinOn f univ 0 := by
    intro x _
    dsimp [f]
    nlinarith [sq_nonneg x]
  have hflow (t : ℝ) : HasDerivAt (fun s : ℝ => Real.exp (-s))
      (-gradient f (Real.exp (-t))) t := by
    rw [hg]
    simpa using (hasDerivAt_id t).neg.exp
  have h := lyapunov_and_rates hT hf hc hm
    (Real.continuous_exp.comp continuous_neg).continuousOn
    (fun t _ => (hflow t).hasDerivWithinAt)
  simp only [hg] at h
  simpa [f] using h

#print axioms AutoSamplingTheory.TechnicalLemmas.Analysis.GradientFlowLastIterate.lyapunov_and_rates
