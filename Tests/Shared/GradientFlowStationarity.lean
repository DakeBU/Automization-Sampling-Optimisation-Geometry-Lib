import AutoSamplingTheory.TechnicalLemmas.Analysis.GradientFlowStationarity
import Mathlib.Analysis.Calculus.Deriv.Pow

open AutoSamplingTheory.TechnicalLemmas.Analysis.GradientFlowStationarity Set

-- A nonstationary actual trajectory with positive initial gap. The minimum
-- witness and the exact coefficient are both obtained from the public theorem.
example (T : ℝ) (hT : 0 < T) :
    ∃ s ∈ Icc 0 T, IsMinOn (fun u : ℝ => ‖Real.exp (-u)‖) (Icc 0 T) s ∧
      ‖Real.exp (-s)‖ ≤ Real.sqrt (1 / (2 * T)) := by
  let f : ℝ → ℝ := fun x => x ^ 2 / 2
  have hd (x : ℝ) : HasDerivAt f x x := by
    convert ((hasDerivAt_id x).pow 2).div_const 2 using 1 <;>
      first | rfl | (simp only [id_eq]; ring)
  have hg (x : ℝ) : gradient f x = x := (hd x).hasGradientAt'.gradient
  have hf : ContDiff ℝ 1 f := contDiff_id.pow 2 |>.div_const 2
  have hm : IsMinOn f univ 0 := by
    intro x _
    dsimp [f]
    nlinarith [sq_nonneg x]
  have hflow (t : ℝ) : HasDerivAt (fun s : ℝ => Real.exp (-s))
      (-gradient f (Real.exp (-t))) t := by
    rw [hg]
    simpa using (hasDerivAt_id t).neg.exp
  have h := exists_min_norm_le hT hf hm
    (Real.continuous_exp.comp continuous_neg).continuousOn
    (fun t _ => (hflow t).hasDerivWithinAt)
  simp only [hg] at h
  simpa [f, div_div, div_eq_mul_inv, mul_comm] using h

-- Zero initial gap is admissible: no strict gap or PL premise is hidden.
example (T : ℝ) (hT : 0 < T) :
    ∃ s ∈ Icc 0 T, IsMinOn (fun _ : ℝ => (0 : ℝ)) (Icc 0 T) s ∧ (0 : ℝ) ≤ 0 := by
  have h := exists_min_norm_le (f := fun _ : ℝ => (7 : ℝ))
    (X := fun _ : ℝ => (2 : ℝ)) (z := 0) hT contDiff_const
    (by intro x _; change (7 : ℝ) ≤ 7; exact le_rfl) continuousOn_const
    (fun t _ => by simpa using (hasDerivWithinAt_const t (Ici t) (2 : ℝ)))
  simpa using h

#print axioms AutoSamplingTheory.TechnicalLemmas.Analysis.GradientFlowStationarity.exists_min_norm_le
