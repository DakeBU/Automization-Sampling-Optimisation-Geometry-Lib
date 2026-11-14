import Mathlib

/-! Real matrix exponential estimates for the deterministic step of Tropp's
bounded Bernstein MGF argument (author preprint, Lemma 6.7, pp. 25–26).
The actual Gaussian single-summand consumer has its own original probability law.
-/

open MeasureTheory
open scoped BigOperators Matrix.Norms.L2Operator

noncomputable section

namespace AutoSamplingTheory.TechnicalLemmas.Probability.MatrixBernsteinExponential

private lemma exponential_remainder_integral (k : ℝ) :
    Real.exp k - 1 - k =
      k ^ 2 * ∫ t in (0 : ℝ)..1, (1 - t) * Real.exp (k * t) := by
  have hd : ∀ t : ℝ,
      HasDerivAt (fun u : ℝ => Real.exp (k * u)) (k * Real.exp (k * t)) t := by
    intro t
    exact ((hasDerivAt_const_mul k (x := t)).exp).congr_deriv (mul_comm _ _)
  have hv : ∀ t : ℝ,
      HasDerivAt (fun u : ℝ => k * Real.exp (k * u))
        (k ^ 2 * Real.exp (k * t)) t := by
    intro t
    exact (hd t).const_mul k |>.congr_deriv (by ring)
  have hke : IntervalIntegrable (fun t : ℝ => k * Real.exp (k * t)) volume 0 1 :=
    (by fun_prop : Continuous (fun t : ℝ => k * Real.exp (k * t))).intervalIntegrable _ _
  have he : (∫ t in (0 : ℝ)..1, k * Real.exp (k * t)) = Real.exp k - 1 := by
    simpa only [mul_one, mul_zero, Real.exp_zero] using
      intervalIntegral.integral_eq_sub_of_hasDerivAt (fun t _ => hd t) hke
  have hp := intervalIntegral.integral_mul_deriv_eq_deriv_mul_of_hasDerivAt
    (u := fun t : ℝ => 1 - t) (v := fun t : ℝ => k * Real.exp (k * t))
    (u' := fun _ : ℝ => -1) (v' := fun t : ℝ => k ^ 2 * Real.exp (k * t))
    (a := (0 : ℝ)) (b := 1)
    (by fun_prop) (by fun_prop)
    (fun t _ => ((hasDerivAt_const t (1 : ℝ)).sub (hasDerivAt_id t)).congr_deriv (by ring))
    (fun t _ => hv t)
    ((by fun_prop : Continuous (fun _ : ℝ => (-1 : ℝ))).intervalIntegrable _ _)
    ((by fun_prop : Continuous (fun t : ℝ => k ^ 2 * Real.exp (k * t))).intervalIntegrable _ _)
  have hfactor :
      (∫ t in (0 : ℝ)..1, (1 - t) * (k ^ 2 * Real.exp (k * t))) =
        k ^ 2 * ∫ t in (0 : ℝ)..1, (1 - t) * Real.exp (k * t) := by
    calc
      _ = ∫ t in (0 : ℝ)..1, k ^ 2 * ((1 - t) * Real.exp (k * t)) :=
        intervalIntegral.integral_congr (fun t _ => by ring)
      _ = _ := intervalIntegral.integral_const_mul _ _
  rw [hfactor] at hp
  simp only [sub_self, zero_mul, sub_zero, mul_zero, Real.exp_zero, mul_one, one_mul,
    neg_one_mul, intervalIntegral.integral_neg, he] at hp
  linarith

end AutoSamplingTheory.TechnicalLemmas.Probability.MatrixBernsteinExponential
