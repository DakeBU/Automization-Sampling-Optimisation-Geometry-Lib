import Mathlib

/-! Real matrix exponential estimates for the deterministic step of Tropp's
bounded Bernstein MGF argument (author preprint, Lemma 6.7, pp. 25–26).
The actual Gaussian single-summand consumer has its own original probability law.
-/

open MeasureTheory
open scoped BigOperators Matrix.Norms.L2Operator

noncomputable section

universe u

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

private def remainderKernel (k : ℝ) : ℝ :=
  ∫ t in (0 : ℝ)..1, (1 - t) * Real.exp (k * t)

private lemma remainderKernel_monotone : Monotone remainderKernel := by
  intro x y hxy
  unfold remainderKernel
  apply intervalIntegral.integral_mono_on zero_le_one
    ((by fun_prop : Continuous (fun t : ℝ => (1 - t) * Real.exp (x * t))).intervalIntegrable _ _)
    ((by fun_prop : Continuous (fun t : ℝ => (1 - t) * Real.exp (y * t))).intervalIntegrable _ _)
  intro t ht
  exact mul_le_mul_of_nonneg_left
    (Real.exp_le_exp.mpr (mul_le_mul_of_nonneg_right hxy ht.1)) (sub_nonneg.mpr ht.2)

private lemma remainderKernel_zero : remainderKernel 0 = 1 / 2 := by
  simp only [remainderKernel, zero_mul, Real.exp_zero, mul_one]
  rw [intervalIntegral.integral_sub]
  · norm_num [intervalIntegral.integral_const, integral_id]
  · exact continuous_const.intervalIntegrable _ _
  · exact continuous_id.intervalIntegrable _ _

private def bernsteinRemainder (s x : ℝ) : ℝ :=
  if x = 0 then s ^ 2 / 2 else (Real.exp (s * x) - s * x - 1) / x ^ 2

private lemma bernsteinRemainder_eq_kernel (s x : ℝ) :
    bernsteinRemainder s x = s ^ 2 * remainderKernel (s * x) := by
  by_cases hx : x = 0
  · subst x
    simp [bernsteinRemainder, remainderKernel_zero, div_eq_mul_inv]
  · rw [bernsteinRemainder, if_neg hx]
    apply (div_eq_iff (pow_ne_zero 2 hx)).2
    calc
      Real.exp (s * x) - s * x - 1 = Real.exp (s * x) - 1 - s * x := by ring
      _ = (s * x) ^ 2 * remainderKernel (s * x) := exponential_remainder_integral _
      _ = (s ^ 2 * remainderKernel (s * x)) * x ^ 2 := by ring

private lemma bernsteinRemainder_monotone {s : ℝ} (hs : 0 < s) :
    Monotone (bernsteinRemainder s) := by
  intro x y hxy
  rw [bernsteinRemainder_eq_kernel, bernsteinRemainder_eq_kernel]
  exact mul_le_mul_of_nonneg_left
    (remainderKernel_monotone (mul_le_mul_of_nonneg_left hxy hs.le)) (sq_nonneg s)

private lemma bernsteinRemainder_mul_sq (s x : ℝ) :
    bernsteinRemainder s x * x ^ 2 = Real.exp (s * x) - s * x - 1 := by
  by_cases hx : x = 0
  · subst x
    simp [bernsteinRemainder]
  · rw [bernsteinRemainder, if_neg hx]
    field_simp

private lemma bernstein_scalar_bound {s : ℝ} (hs : 0 < s) {x : ℝ} (hx : x ≤ 1) :
    Real.exp (s * x) ≤ 1 + s * x + (Real.exp s - s - 1) * x ^ 2 := by
  have hone : bernsteinRemainder s 1 = Real.exp s - s - 1 := by
    simp [bernsteinRemainder]
  have h := mul_le_mul_of_nonneg_right (bernsteinRemainder_monotone hs hx) (sq_nonneg x)
  rw [bernsteinRemainder_mul_sq, hone] at h
  linarith

open scoped MatrixOrder in
/-- The deterministic real-matrix inequality in the proof of Tropp's Lemma 6.7.
The upper spectral cap is one-sided; negative eigenvalues are unrestricted. -/
theorem bernstein_exponential_quadratic_bound
    {ι : Type u} [Fintype ι] [DecidableEq ι] [Nonempty ι]
    (A : Matrix ι ι ℝ) (hA : A.IsHermitian)
    (hA_le : (1 - A).PosSemidef) {s : ℝ} (hs : 0 < s) :
    ((1 : Matrix ι ι ℝ) + s • A + (Real.exp s - s - 1) • (A * A) -
      NormedSpace.exp (s • A)).PosSemidef := by
  have hSA : IsSelfAdjoint A := hA.isSelfAdjoint
  have hle : A ≤ 1 := Matrix.le_iff.mpr hA_le
  have hspec : ∀ x ∈ spectrum ℝ A, x ≤ 1 :=
    (CFC.le_one_iff (R := ℝ) A hSA).mp hle
  have hfc : cfc (fun x : ℝ => Real.exp (s * x)) A ≤
      cfc (fun x : ℝ => 1 + s * x + (Real.exp s - s - 1) * (x * x)) A := by
    apply cfc_mono
    intro x hx
    simpa only [pow_two] using bernstein_scalar_bound hs (hspec x hx)
  have hleft : cfc (fun x : ℝ => Real.exp (s * x)) A = NormedSpace.exp (s • A) := by
    calc
      _ = cfc Real.exp (s • A) := cfc_comp_const_mul s Real.exp A (by fun_prop) hSA
      _ = _ := CFC.real_exp_eq_normedSpace_exp ((IsSelfAdjoint.all s).smul hSA)
  have hright :
      cfc (fun x : ℝ => 1 + s * x + (Real.exp s - s - 1) * (x * x)) A =
        (1 : Matrix ι ι ℝ) + s • A + (Real.exp s - s - 1) • (A * A) := by
    rw [cfc_add (a := A) (fun x : ℝ => 1 + s * x)
        (fun x : ℝ => (Real.exp s - s - 1) * (x * x)) (by fun_prop) (by fun_prop),
      cfc_add (a := A) (fun _ : ℝ => 1) (fun x : ℝ => s * x) (by fun_prop) (by fun_prop),
      cfc_const (R := ℝ) 1 A hSA,
      cfc_const_mul_id s A hSA,
      cfc_const_mul (Real.exp s - s - 1) (fun x : ℝ => x * x) A (by fun_prop),
      cfc_mul (fun x : ℝ => x) (fun x : ℝ => x) A (by fun_prop) (by fun_prop),
      cfc_id' ℝ A hSA, map_one]
  exact Matrix.le_iff.mp (by simpa only [hleft, hright] using hfc)

end AutoSamplingTheory.TechnicalLemmas.Probability.MatrixBernsteinExponential
