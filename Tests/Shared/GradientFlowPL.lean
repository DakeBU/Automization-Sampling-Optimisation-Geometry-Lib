import AutoSamplingTheory.TechnicalLemmas.Analysis.GradientFlowPL
import Mathlib.Analysis.Calculus.Deriv.Pow

open AutoSamplingTheory.TechnicalLemmas.Analysis.GradientFlowPL Set

set_option backward.isDefEq.respectTransparency false
set_option backward.isDefEq.respectTransparency.types false

-- A nonstationary actual flow with positive initial gap: f(x)=x²/2, X(t)=exp(-t).
-- The derivative, PL bound and minimizer are proved, rather than supplied.
example (T : ℝ) (hT : 0 ≤ T) :
    (∀ t ∈ Ico 0 T, HasDerivWithinAt (fun s : ℝ => Real.exp (-s) ^ 2 / 2)
      (-Real.exp (-t) ^ 2) (Ici t) t) ∧
    ∀ t ∈ Icc 0 T, 0 ≤ Real.exp (-t) ^ 2 / 2 ∧
      Real.exp (-t) ^ 2 / 2 ≤ 1 / 2 * Real.exp (-2 * t) := by
  let f : ℝ → ℝ := fun x => x ^ 2 / 2
  have hd (x : ℝ) : HasDerivAt f x x := by
    convert ((hasDerivAt_id x).pow 2).div_const 2 using 1 <;>
      first | rfl | (simp only [id_eq]; ring)
  have hg (x : ℝ) : gradient f x = x := (hd x).hasGradientAt'.gradient
  have hm : IsMinOn f univ 0 := by
    intro x _
    dsimp [f]
    nlinarith [sq_nonneg x]
  have hp (x : ℝ) : 2 * 1 * (f x - f 0) ≤ ‖gradient f x‖ ^ 2 := by
    rw [hg]
    simp [f, Real.norm_eq_abs, sq_abs]
    ring_nf
    exact le_rfl
  have hx (t : ℝ) : HasDerivAt (fun s : ℝ => Real.exp (-s))
      (-gradient f (Real.exp (-t))) t := by
    rw [hg]
    simpa using ((hasDerivAt_id t).neg.exp)
  have h := dissipation_and_decay (by norm_num : (0 : ℝ) < 1) hT
    (fun x => (hd x).differentiableAt)
    (Real.continuous_exp.comp continuous_neg).continuousOn
    (fun t _ => (hx t).hasDerivWithinAt) hm hp
  simpa [Function.comp_def, f, hg, Real.norm_eq_abs, sq_abs] using h

-- The actual rate is sharp on the same curve, including t=0.
example (t : ℝ) : Real.exp (-t) ^ 2 / 2 = 1 / 2 * Real.exp (-2 * t) := by
  rw [sq, ← Real.exp_add]
  rw [show -t + -t = -2 * t by ring]
  ring

#print axioms dissipation_and_decay
