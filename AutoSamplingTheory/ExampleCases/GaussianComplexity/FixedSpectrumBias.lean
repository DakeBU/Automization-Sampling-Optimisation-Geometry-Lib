import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumExactMeans
import Mathlib.Analysis.SpecialFunctions.Log.Deriv
import Mathlib.Analysis.SpecialFunctions.Integrals.Basic

/-!
# Actual Gaussian exponential normalized bias

Zhou--Suzuki arXiv:2610.20492v1, Lemma4.5 Ex17 and Appendix C.3
Ex150--159. The exact logarithmic integral and remainder estimates are
proved using the canonical Mathlib derivative and the fundamental theorem
of calculus. The source gap is explicit; positivity and actual mean
normalization are proved internally.
The private Test is a separate zero-threshold numerical probability use.
-/
noncomputable section
open MeasureTheory ProbabilityTheory Set
open scoped BigOperators Interval
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumExactMeans

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumBias

private theorem log_remainder_integral {a : ℝ} (ha0 : 0 ≤ a) (ha1 : a < 1) (n : ℕ) :
    (∫ t : ℝ in 0..a, (t ^ 2) ^ n / (1 - t ^ 2)) =
      1 / 2 * Real.log ((1 + a) / (1 - a)) -
        (∑ i ∈ Finset.range n, a ^ (2 * i + 1) / (2 * i + 1)) := by
  have hden (t : ℝ) (ht : t ∈ Set.uIcc 0 a) : 1 - t ^ 2 ≠ 0 := by
    rw [Set.uIcc_of_le ha0] at ht
    have ht0 : 0 ≤ t := ht.1
    have ht1 : t < 1 := ht.2.trans_lt ha1
    nlinarith
  have hi : IntervalIntegrable (fun t : ℝ => (t ^ 2) ^ n / (1 - t ^ 2)) volume 0 a := by
    apply ContinuousOn.intervalIntegrable
    exact ContinuousOn.div (by fun_prop) (by fun_prop) hden
  have hd (t : ℝ) (ht : t ∈ Set.uIcc 0 a) : HasDerivAt
      (fun x : ℝ => 1 / 2 * Real.log ((1 + x) / (1 - x)) -
        (∑ i ∈ Finset.range n, x ^ (2 * i + 1) / (2 * i + 1)))
      ((t ^ 2) ^ n / (1 - t ^ 2)) t := by
    rw [Set.uIcc_of_le ha0] at ht
    exact Real.hasDerivAt_half_log_one_add_div_one_sub_sub_sum_range n
      (by linarith [ht.1]) (ht.2.trans_lt ha1)
  have h := intervalIntegral.integral_eq_sub_of_hasDerivAt hd hi
  simpa using h

private theorem log_integral_identities {a : ℝ} (ha0 : 0 ≤ a) (ha1 : a < 1) :
    Real.log ((1 + a) / (1 - a)) = 2 * (∫ t : ℝ in 0..a, 1 / (1 - t ^ 2)) ∧
    Real.log ((1 + a) / (1 - a)) =
      2 * a + 2 * (∫ t : ℝ in 0..a, t ^ 2 / (1 - t ^ 2)) := by
  have h0 := log_remainder_integral ha0 ha1 0
  have h1 := log_remainder_integral ha0 ha1 1
  simp only [pow_zero, Finset.range_zero, Finset.sum_empty, sub_zero] at h0
  simp only [pow_one, Finset.range_one, Finset.sum_singleton] at h1
  constructor <;> linarith

private theorem log_integral_bounds {a : ℝ} (ha0 : 0 ≤ a) (ha1 : a < 1) :
    2 * a ≤ Real.log ((1 + a) / (1 - a)) ∧
    Real.log ((1 + a) / (1 - a)) ≤ 2 * a + 2 * a ^ 3 / (3 * (1 - a ^ 2)) := by
  have hpos (t : ℝ) (ht : t ∈ Set.Icc 0 a) : 0 < 1 - t ^ 2 := by
    have h0 := ht.1
    have h1 := ht.2.trans_lt ha1
    nlinarith
  have hcont (n : ℕ) : ContinuousOn (fun t : ℝ => (t ^ 2) ^ n / (1 - t ^ 2))
      (Set.uIcc 0 a) := by
    apply ContinuousOn.div (by fun_prop) (by fun_prop)
    intro t ht
    exact ne_of_gt (hpos t (by simpa only [Set.uIcc_of_le ha0] using ht))
  have hint0 : IntervalIntegrable (fun t : ℝ => 1 / (1 - t ^ 2)) volume 0 a := by
    simpa using (hcont 0).intervalIntegrable
  have hint1 : IntervalIntegrable (fun t : ℝ => t ^ 2 / (1 - t ^ 2)) volume 0 a := by
    simpa using (hcont 1).intervalIntegrable
  have hm0 : a ≤ (∫ t : ℝ in 0..a, 1 / (1 - t ^ 2)) := by
    calc
      a = (∫ _t : ℝ in 0..a, (1 : ℝ)) := by simp
      _ ≤ _ := intervalIntegral.integral_mono_on ha0
        ((by fun_prop : Continuous (fun _t : ℝ => (1 : ℝ))).intervalIntegrable 0 a) hint0 (by
        intro t ht
        apply (le_div_iff₀ (hpos t ht)).2
        nlinarith [sq_nonneg t])
  have hapos : 0 < 1 - a ^ 2 := hpos a ⟨ha0, le_rfl⟩
  have hm1 : (∫ t : ℝ in 0..a, t ^ 2 / (1 - t ^ 2)) ≤ a ^ 3 / (3 * (1 - a ^ 2)) := by
    calc
      _ ≤ (∫ t : ℝ in 0..a, t ^ 2 / (1 - a ^ 2)) :=
        intervalIntegral.integral_mono_on ha0 hint1
          ((by fun_prop : Continuous (fun t : ℝ => t ^ 2 / (1 - a ^ 2))).intervalIntegrable 0 a) (by
          intro t ht
          have hs : t ^ 2 ≤ a ^ 2 := pow_le_pow_left₀ ht.1 ht.2 2
          apply div_le_div_of_nonneg_left (sq_nonneg t) hapos
          linarith)
      _ = _ := by
        rw [intervalIntegral.integral_div, integral_pow]
        simp only [zero_pow (by norm_num : (3 : ℕ) ≠ 0), sub_zero]
        rw [div_div]
        norm_num
  rcases log_integral_identities ha0 ha1 with ⟨h0, h1⟩
  constructor
  · rw [h0]
    linarith
  · rw [h1]
    calc
      _ ≤ 2 * a + 2 * (a ^ 3 / (3 * (1 - a ^ 2))) :=
        add_le_add le_rfl (mul_le_mul_of_nonneg_left hm1 (show (0 : ℝ) ≤ 2 by norm_num))
      _ = _ := by ring

private theorem spectral_ratio_log_bounds {κ : ℝ} (hκ : 2 ≤ κ) :
    let r : ℝ := (Real.sqrt κ - 1) / (Real.sqrt κ + 1)
    0 < r ∧ r < 1 ∧ 2 / Real.sqrt κ ≤ Real.log (1 / r) ∧
      Real.log (1 / r) ≤ 8 / (3 * Real.sqrt κ) := by
  let s : ℝ := Real.sqrt κ
  let a : ℝ := 1 / s
  let r : ℝ := (Real.sqrt κ - 1) / (Real.sqrt κ + 1)
  change 0 < r ∧ r < 1 ∧ 2 / s ≤ Real.log (1 / r) ∧
    Real.log (1 / r) ≤ 8 / (3 * s)
  have hs1 : 1 < s := by
    dsimp [s]
    nlinarith [Real.sqrt_nonneg κ, Real.sq_sqrt (by linarith : 0 ≤ κ)]
  have hs0 : 0 < s := by linarith
  have hsne : s ≠ 0 := ne_of_gt hs0
  have hsq : s ^ 2 = κ := Real.sq_sqrt (by linarith)
  have ha0 : 0 ≤ a := by dsimp [a]; positivity
  have ha1 : a < 1 := by dsimp [a]; exact (div_lt_one hs0).2 hs1
  have ha2 : a ^ 2 ≤ 1 / 2 := by
    have hid : a ^ 2 * κ = 1 := by
      calc
        _ = (1 / s) ^ 2 * s ^ 2 := by dsimp [a]; rw [hsq]
        _ = 1 := by field_simp
    nlinarith [sq_nonneg a]
  have hapos : 0 < 1 - a ^ 2 := by linarith
  have hrem : a ^ 3 / (3 * (1 - a ^ 2)) ≤ a / 3 := by
    apply (div_le_iff₀ (by positivity : 0 < 3 * (1 - a ^ 2))).2
    have hm := mul_le_mul_of_nonneg_left ha2 ha0
    nlinarith
  have harg : 1 / r = (1 + a) / (1 - a) := by
    change 1 / ((s - 1) / (s + 1)) = (1 + a) / (1 - a)
    dsimp [a]
    field_simp [hsne, ne_of_gt (by linarith : 0 < s - 1),
      ne_of_gt (by linarith : 0 < s + 1)]
  have hl := log_integral_bounds ha0 ha1
  have hlower : 2 / s ≤ Real.log (1 / r) := by
    rw [harg]
    convert hl.1 using 1
    dsimp [a]
    ring
  have hupper : Real.log (1 / r) ≤ 8 / (3 * s) := by
    rw [harg]
    calc
      _ ≤ 2 * a + 2 * a ^ 3 / (3 * (1 - a ^ 2)) := hl.2
      _ = 2 * a + 2 * (a ^ 3 / (3 * (1 - a ^ 2))) := by ring
      _ ≤ 2 * a + 2 * (a / 3) :=
        add_le_add le_rfl (mul_le_mul_of_nonneg_left hrem (by norm_num : (0 : ℝ) ≤ 2))
      _ = _ := by dsimp [a]; field_simp; ring
  have hr0 : 0 < r := by
    change 0 < (s - 1) / (s + 1)
    exact div_pos (by linarith) (by linarith)
  have hr1 : r < 1 := by
    change (s - 1) / (s + 1) < 1
    apply (div_lt_one (by linarith : 0 < s + 1)).2
    linarith
  exact ⟨hr0, hr1, hlower, hupper⟩

private theorem spectral_ratio_power_bounds {κ : ℝ} (hκ : 2 ≤ κ) (k : ℕ) :
    let r : ℝ := (Real.sqrt κ - 1) / (Real.sqrt κ + 1)
    Real.exp (-3 * (k : ℝ) / Real.sqrt κ) ≤ r ^ k ∧
      r ^ k ≤ Real.exp (-2 * (k : ℝ) / Real.sqrt κ) := by
  let r : ℝ := (Real.sqrt κ - 1) / (Real.sqrt κ + 1)
  change Real.exp (-3 * (k : ℝ) / Real.sqrt κ) ≤ r ^ k ∧
    r ^ k ≤ Real.exp (-2 * (k : ℝ) / Real.sqrt κ)
  rcases spectral_ratio_log_bounds hκ with ⟨hr0, _hr1, hlo, hhi⟩
  have hs : 0 < Real.sqrt κ := Real.sqrt_pos.2 (by linarith)
  have h3 : Real.log (1 / r) ≤ 3 / Real.sqrt κ := by
    apply hhi.trans
    calc
      8 / (3 * Real.sqrt κ) = (8 / 3 : ℝ) / Real.sqrt κ := by rw [div_div]
      _ ≤ _ := div_le_div_of_nonneg_right (by norm_num) hs.le
  have hk : (0 : ℝ) ≤ (k : ℝ) := Nat.cast_nonneg _
  have hmhi := mul_le_mul_of_nonneg_left h3 hk
  have hmlo := mul_le_mul_of_nonneg_left hlo hk
  have hrepr : r ^ k = Real.exp (-(k : ℝ) * Real.log (1 / r)) := by
    rw [one_div, Real.log_inv, neg_mul_neg, Real.exp_nat_mul, Real.exp_log hr0]
  rw [hrepr]
  constructor
  · apply Real.exp_le_exp.mpr
    calc
      -3 * (k : ℝ) / Real.sqrt κ = -((k : ℝ) * (3 / Real.sqrt κ)) := by ring
      _ ≤ -((k : ℝ) * Real.log (1 / r)) := neg_le_neg hmhi
      _ = _ := by ring
  · apply Real.exp_le_exp.mpr
    calc
      -(k : ℝ) * Real.log (1 / r) = -((k : ℝ) * Real.log (1 / r)) := by ring
      _ ≤ -((k : ℝ) * (2 / Real.sqrt κ)) := neg_le_neg hmlo
      _ = _ := by ring

theorem actual_diagonal_gaussian_exponential_bias {d : ℕ} (hd : 2 ≤ d) {κ : ℝ} (hκ : 2 ≤ κ)
    (n : ℕ) (hn : 1 ≤ n) (hnd : n < d) (hgap : Real.sqrt κ ≤ (d : ℝ) - (n : ℝ)) :
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let eigenvalue : Fin d → ℝ := fun i => (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i)
  let Λ : Matrix (Fin d) (Fin d) ℝ := Matrix.diagonal eigenvalue
  let μ : Measure (EuclideanSpace ℝ (Fin d)) :=
    multivariateGaussian (0 : EuclideanSpace ℝ (Fin d)) Λ⁻¹
  let Q : EuclideanSpace ℝ (Fin d) → ℝ := fun x =>
    ∑ i : Fin d, Real.cos ((n : ℝ) * θ i) * (WithLp.ofLp x i) ^ 2
  let M : ℝ := ∫ x : EuclideanSpace ℝ (Fin d), ‖x‖ ^ 2 ∂μ
  let b : ℝ := ∫ x : EuclideanSpace ℝ (Fin d), Q x ∂μ
  0 < M ∧ 0 < (-1 : ℝ) ^ n * b ∧
  (1 - Real.exp (-4)) * Real.exp (-3 * (n : ℝ) / Real.sqrt κ) ≤ |b| / M ∧
  |b| / M ≤ Real.exp (-2 * (n : ℝ) / Real.sqrt κ) := by
  classical
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let eigenvalue : Fin d → ℝ := fun i => (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i)
  let Λ : Matrix (Fin d) (Fin d) ℝ := Matrix.diagonal eigenvalue
  let μ : Measure (EuclideanSpace ℝ (Fin d)) := multivariateGaussian 0 Λ⁻¹
  let Q : EuclideanSpace ℝ (Fin d) → ℝ := fun x =>
    ∑ i : Fin d, Real.cos ((n : ℝ) * θ i) * (WithLp.ofLp x i) ^ 2
  let M : ℝ := ∫ x : EuclideanSpace ℝ (Fin d), ‖x‖ ^ 2 ∂μ
  let b : ℝ := ∫ x : EuclideanSpace ℝ (Fin d), Q x ∂μ
  let r : ℝ := (Real.sqrt κ - 1) / (Real.sqrt κ + 1)
  change 0 < M ∧ 0 < (-1 : ℝ) ^ n * b ∧
    (1 - Real.exp (-4)) * Real.exp (-3 * (n : ℝ) / Real.sqrt κ) ≤ |b| / M ∧
    |b| / M ≤ Real.exp (-2 * (n : ℝ) / Real.sqrt κ)
  have hclosed := actual_diagonal_gaussian_exact_means hd hκ n hn hnd
  have hm : M = ((d : ℝ) / Real.sqrt κ) *
      ((1 - r ^ (2 * d)) / (1 + r ^ (2 * d))) := hclosed.2.2.1
  have hb : (-1 : ℝ) ^ n * b = ((d : ℝ) / Real.sqrt κ) *
      ((r ^ n - r ^ (2 * d - n)) / (1 + r ^ (2 * d))) := hclosed.2.2.2
  rcases spectral_ratio_log_bounds hκ with ⟨hr0, hr1, _hloglo, _hloghi⟩
  have hs : 0 < Real.sqrt κ := Real.sqrt_pos.2 (by linarith)
  have hscale : 0 < (d : ℝ) / Real.sqrt κ :=
    div_pos (by exact_mod_cast (by omega : 0 < d)) hs
  have hu0 : 0 ≤ r ^ (2 * d) := pow_nonneg hr0.le _
  have hu1 : r ^ (2 * d) < 1 := pow_lt_one₀ hr0.le hr1 (by omega)
  have ht0 : 0 ≤ r ^ (2 * (d - n)) := pow_nonneg hr0.le _
  have ht1 : r ^ (2 * (d - n)) < 1 := pow_lt_one₀ hr0.le hr1 (by omega)
  have hden : 0 < 1 + r ^ (2 * d) := by positivity
  have hMpos : 0 < M := by
    rw [hm]
    exact mul_pos hscale (div_pos (by linarith) hden)
  have hindex : n + 2 * (d - n) = 2 * d - n := by omega
  have hfactor : r ^ n - r ^ (2 * d - n) = r ^ n * (1 - r ^ (2 * (d - n))) := by
    rw [← hindex, pow_add]
    ring
  have hbpos : 0 < (-1 : ℝ) ^ n * b := by
    rw [hb, hfactor]
    exact mul_pos hscale (div_pos (mul_pos (pow_pos hr0 _) (by linarith)) hden)
  have habs : |b| = (-1 : ℝ) ^ n * b := by
    calc
      |b| = |(-1 : ℝ) ^ n * b| := by rw [abs_mul, abs_neg_one_pow, one_mul]
      _ = _ := abs_of_pos hbpos
  have hratio : |b| / M = r ^ n *
      ((1 - r ^ (2 * (d - n))) / (1 - r ^ (2 * d))) := by
    rw [habs, hb, hm, hfactor]
    field_simp [ne_of_gt hscale, ne_of_gt hden, ne_of_gt (by linarith : 0 < 1 - r ^ (2 * d))]
  have hpoworder : r ^ (2 * d) ≤ r ^ (2 * (d - n)) :=
    pow_le_pow_of_le_one hr0.le hr1.le (by omega)
  have hfraclower : 1 - r ^ (2 * (d - n)) ≤
      (1 - r ^ (2 * (d - n))) / (1 - r ^ (2 * d)) := by
    apply (le_div_iff₀ (by linarith : 0 < 1 - r ^ (2 * d))).2
    nlinarith [mul_nonneg (by linarith : 0 ≤ 1 - r ^ (2 * (d - n))) hu0]
  have hfracupper : (1 - r ^ (2 * (d - n))) / (1 - r ^ (2 * d)) ≤ 1 := by
    apply (div_le_one (by linarith : 0 < 1 - r ^ (2 * d))).2
    linarith
  have htail : r ^ (2 * (d - n)) ≤ Real.exp (-4) := by
    apply (spectral_ratio_power_bounds hκ (2 * (d - n))).2.trans
    apply Real.exp_le_exp.mpr
    apply (div_le_iff₀ hs).2
    rw [Nat.cast_mul, Nat.cast_sub hnd.le]
    norm_num only [Nat.cast_ofNat]
    nlinarith [hgap]
  have he4 : Real.exp (-4) < 1 := by
    simpa only [Real.exp_zero] using Real.exp_lt_exp.mpr (by norm_num : (-4 : ℝ) < 0)
  have hC : 0 ≤ 1 - Real.exp (-4) := by linarith
  have hp := spectral_ratio_power_bounds hκ n
  refine ⟨hMpos, hbpos, ?_, ?_⟩
  · rw [hratio]
    calc
      _ ≤ (1 - Real.exp (-4)) * r ^ n := mul_le_mul_of_nonneg_left hp.1 hC
      _ ≤ (1 - r ^ (2 * (d - n))) * r ^ n :=
        mul_le_mul_of_nonneg_right (by linarith [htail]) (pow_nonneg hr0.le _)
      _ ≤ ((1 - r ^ (2 * (d - n))) / (1 - r ^ (2 * d))) * r ^ n :=
        mul_le_mul_of_nonneg_right hfraclower (pow_nonneg hr0.le _)
      _ = _ := mul_comm _ _
  · rw [hratio]
    calc
      _ ≤ r ^ n * 1 := mul_le_mul_of_nonneg_left hfracupper (pow_nonneg hr0.le _)
      _ = r ^ n := mul_one _
      _ ≤ _ := hp.2

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumBias
