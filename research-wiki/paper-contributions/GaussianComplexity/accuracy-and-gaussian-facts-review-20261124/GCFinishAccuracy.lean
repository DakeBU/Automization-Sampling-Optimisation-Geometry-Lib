import GC41Asymptotic
import Mathlib.Analysis.SpecialFunctions.Log.Deriv

/-! The accuracy limitation of the Section 4.4 separating test. -/
open MeasureTheory ProbabilityTheory
noncomputable section
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumTargetEvent

/-- The two-sided Bernstein expression displayed after Fact C.6.
Its variance and radius are the explicit values used in the paper. -/
def bernsteinCertificate (d q : ℕ) (u : ℝ) : ℝ :=
  let r := (q : ℝ) + 1
  let L := 2*r + 3*Real.log (1000*(d : ℝ))
  let v := 2*r*(r+2)/(d : ℝ)
  let R := 2*r*(L+1)/(d : ℝ)
  2*r^2 * Real.exp (-(u^2)/(2*(v+R*u/3)))

/-- Even a certificate below one requires a deviation exceeding the reciprocal
square root of the dimension. This concerns the displayed bound on the tail. -/
theorem bernstein_certificate_floor {d q : ℕ} (hd : 0 < d) {u : ℝ} (hu : 0 ≤ u)
    (hc : bernsteinCertificate d q u < 1) : 1/Real.sqrt (d : ℝ) < u := by
  have hd' : (1 : ℝ) ≤ d := by exact_mod_cast hd
  let r := (q : ℝ)+1
  let L := 2*r+3*Real.log (1000*(d : ℝ))
  let v := 2*r*(r+2)/(d : ℝ)
  let R := 2*r*(L+1)/(d : ℝ)
  have hr : 1 ≤ r := by dsimp [r]; linarith [show 0 ≤ (q : ℝ) by positivity]
  have hv : 1/(d : ℝ) ≤ v := by
    apply div_le_div_of_nonneg_right _ (by positivity)
    nlinarith [sq_nonneg r]
  have hL : 0 ≤ L := by
    dsimp [L]
    have := Real.log_nonneg (show (1:ℝ) ≤ 1000*d by linarith)
    linarith
  have hR : 0 ≤ R := by dsimp [R]; positivity
  have hv0 : 0 < v := lt_of_lt_of_le (by positivity) hv
  change 2*r^2 * Real.exp (-(u^2)/(2*(v+R*u/3))) < 1 at hc
  by_contra! h
  have hs : 0 < Real.sqrt (d : ℝ) := by positivity
  have hsq := pow_le_pow_left₀ hu h 2
  rw [div_pow, one_pow, Real.sq_sqrt (by positivity)] at hsq
  have hratio : -(1/2 : ℝ) ≤ -(u^2)/(2*(v+R*u/3)) := by
    apply (le_div_iff₀ (by positivity)).2
    nlinarith [mul_nonneg hR hu]
  have hexp : 1/2 ≤ Real.exp (-(u^2)/(2*(v+R*u/3))) := by
    have := Real.add_one_le_exp (-(1/2 : ℝ))
    linarith [Real.exp_le_exp.mpr hratio]
  have hr2 : 2 ≤ 2*r^2 := by nlinarith [sq_nonneg (r-1)]
  linarith [mul_le_mul hr2 hexp (by norm_num : (0:ℝ) ≤ 1/2) (by positivity : 0 ≤ 2*r^2)]

/-- The exact finite-grid means give the upper signal bound for every allowed mode.
The extra gap in Lemma 4.5 is needed for the companion lower estimate. -/
theorem mode_bias_upper {d : ℕ} (hd : 2 ≤ d) {κ : ℝ} (hk : 2 ≤ κ) {n : ℕ}
    (hn : 1 ≤ n) (hnd : n < d) :
    |∫ x, cosineForm n x ∂diagonalLaw d κ| / (∫ x, ‖x‖^2 ∂diagonalLaw d κ)
      ≤ Real.exp (-2*(n : ℝ)/Real.sqrt κ) := by
  let s := Real.sqrt κ
  let r := (s-1)/(s+1)
  have hs : 1 < s := by
    dsimp [s]
    exact (Real.lt_sqrt (by norm_num)).2 (by linarith)
  have hr : 0 < r := div_pos (by linarith) (by linarith)
  have hr' : r < 1 := (div_lt_one (by linarith : 0 < s+1)).2 (by linarith)
  have hx : 1/s < 1 := (div_lt_one (by linarith)).2 hs
  have hl := Real.sum_range_le_log_div (show 0 ≤ 1/s by positivity) hx 1
  have heq : (1+1/s)/(1-1/s) = r⁻¹ := by
    dsimp [r]; field_simp
  rw [heq,Real.log_inv] at hl
  norm_num at hl
  have hpow : r^n ≤ Real.exp (-2*(n:ℝ)/s) := by
    rw [← Real.exp_log hr, ← Real.exp_nat_mul]
    apply Real.exp_le_exp.mpr
    have hlog : Real.log r ≤ -(2/s) := by rw [div_eq_mul_inv]; linarith
    calc
      _ ≤ (n : ℝ) * -(2/s) := mul_le_mul_of_nonneg_left hlog (Nat.cast_nonneg _)
      _ = _ := by ring
  have h := FixedSpectrumExactMeans.actual_diagonal_gaussian_exact_means hd hk n hn hnd
  let M := ∫ x, ‖x‖^2 ∂diagonalLaw d κ
  let b := ∫ x, cosineForm n x ∂diagonalLaw d κ
  have hM : M = ((d : ℝ)/s)*((1-r^(2*d))/(1+r^(2*d))) := h.2.2.1
  have hb : (-1 : ℝ)^n*b = ((d : ℝ)/s)*((r^n-r^(2*d-n))/(1+r^(2*d))) := h.2.2.2
  have hd0 : 0 < (d : ℝ)/s := div_pos (by exact_mod_cast (show 0 < d by omega)) (by linarith)
  have hden : 0 < 1+r^(2*d) := by positivity
  have hden' : 0 < 1-r^(2*d) := sub_pos.mpr (pow_lt_one₀ hr.le hr' (by omega))
  have hindex : n+2*(d-n)=2*d-n := by omega
  change |b|/M ≤ _
  apply le_trans _ hpow
  have hfactor : r^n-r^(2*d-n) = r^n*(1-r^(2*(d-n))) := by
    rw [← hindex,pow_add]; ring
  have htail : 0 ≤ 1-r^(2*(d-n)) := sub_nonneg.mpr (pow_le_one₀ hr.le hr'.le)
  have hmean : 0 < M := hM ▸ mul_pos hd0 (div_pos hden' hden)
  have hsign : 0 ≤ (-1 : ℝ)^n*b := by
    rw [hb,hfactor]
    positivity
  have habs : |b| = (-1 : ℝ)^n*b := by
    rw [← abs_of_nonneg hsign, abs_mul, abs_neg_one_pow, one_mul]
  rw [habs, div_le_iff₀ hmean, hb, hM]
  change (d : ℝ)/s*((r^n-r^(2*d-n))/(1+r^(2*d))) ≤ _
  rw [hfactor]
  have horder := pow_le_pow_of_le_one hr.le hr'.le (show 2*(d-n) ≤ 2*d by omega)
  calc
    _ ≤ (d : ℝ)/s*((r^n*(1-r^(2*d)))/(1+r^(2*d))) := by gcongr
    _ = _ := by ring

/-- A threshold separating the algorithmic uniform bound from the actual target
mean using the stated Bernstein certificate forces a budget independent of ε. -/
theorem accuracy_certificate_query_ceiling {d q : ℕ} (hn : 2*q+1 < d)
    {κ : ℝ} (hk : 2 ≤ κ) {u a t : ℝ} (hu : 0 ≤ u)
    (hcert : bernsteinCertificate d q u < 1) (hua : u ≤ a) (hat : a ≤ t)
    (ht : t < |∫ x, cosineForm (2*q+1) x ∂diagonalLaw d κ| /
      (∫ x, ‖x‖^2 ∂diagonalLaw d κ)) :
    1/Real.sqrt (d : ℝ) < a ∧ (q : ℝ) < Real.sqrt κ * Real.log (d : ℝ) / 8 := by
  have hd : 0 < (d : ℝ) := by exact_mod_cast (show 0 < d by omega)
  have hs : 0 < Real.sqrt κ := Real.sqrt_pos.mpr (by linarith)
  have hf := lt_of_lt_of_le (bernstein_certificate_floor (by omega : 0 < d) hu hcert) hua
  refine ⟨hf, ?_⟩
  have h := (hf.trans_le hat).trans (ht.trans_le (mode_bias_upper (by omega) hk (by omega) hn))
  have hlog := Real.strictMonoOn_log (show 0 < 1/Real.sqrt (d : ℝ) by positivity)
    (Real.exp_pos _) h
  rw [one_div,Real.log_inv,Real.log_sqrt hd.le,Real.log_exp] at hlog
  have hcross := (lt_div_iff₀ hs).mp hlog
  push_cast at hcross
  nlinarith

#print axioms accuracy_certificate_query_ceiling
end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumTargetEvent
