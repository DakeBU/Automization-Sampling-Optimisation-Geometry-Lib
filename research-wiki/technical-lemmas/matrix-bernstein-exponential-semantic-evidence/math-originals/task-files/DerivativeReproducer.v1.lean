import Mathlib
set_option autoImplicit false
open scoped Matrix.Norms.L2Operator
example (k t : ℝ) :
    HasDerivAt (fun u : ℝ => Real.exp (k * u)) (k * Real.exp (k * t)) t :=
  ((hasDerivAt_const_mul k (x := t)).exp).congr_deriv (mul_comm _ _)
example (k t : ℝ) :
    HasDerivAt (fun u : ℝ => k * Real.exp (k * u))
      (k ^ 2 * Real.exp (k * t)) t := by
  have h : HasDerivAt (fun u : ℝ => Real.exp (k * u)) (k * Real.exp (k * t)) t :=
    ((hasDerivAt_const_mul k (x := t)).exp).congr_deriv (mul_comm _ _)
  exact (h.const_mul k).congr_deriv (by ring)
example (t : ℝ) : HasDerivAt (fun u : ℝ => 1 - u) (-1) t :=
  ((hasDerivAt_const t (1 : ℝ)).sub (hasDerivAt_id t)).congr_deriv (by ring)
