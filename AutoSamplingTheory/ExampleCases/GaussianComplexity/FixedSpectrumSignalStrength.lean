import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumBias
import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumModeGap

/-!
Actual diagonal-Gaussian norm and normalized-bias signal strength from the
unnumbered target-side estimates of Section4.3 and the signal branch of Eq24.
One output threshold precedes all varying dimensions, condition parameters
and natural query caps in the original scalar regime. Moment/gap/positivity
certificates are internal proofs. The radius-tail estimate uses a sufficient
elementary exponential route, not a separate emitted copy of C.3 log bounds.
Concrete tau, shifted/rotated detector events, algorithmic laws, oracle/TV/cost
adapters, both main lower bounds and global reader acceptance remain open.
-/

noncomputable section
open MeasureTheory ProbabilityTheory
open scoped BigOperators
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumModeGap
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumBias
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumExactMeans

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSignalStrength

private theorem spectral_tail_le_third {κ : ℝ} (hκ : 2 ≤ κ)
    (d : ℕ) (hd : Real.sqrt κ ≤ (d : ℝ)) :
    let r : ℝ := (Real.sqrt κ - 1) / (Real.sqrt κ + 1)
    0 ≤ r ∧ r ^ (2 * d) ≤ (1 : ℝ) / 3 := by
  let s : ℝ := Real.sqrt κ
  let r : ℝ := (s - 1) / (s + 1)
  change 0 ≤ r ∧ r ^ (2 * d) ≤ (1 : ℝ) / 3
  have hs : 0 < s := Real.sqrt_pos.2 (by linarith)
  have hs1 : 1 ≤ s := Real.le_sqrt_of_sq_le (by nlinarith)
  have hr0 : 0 ≤ r := div_nonneg (by linarith) (by linarith)
  have hrlin : r ≤ 1 - 1 / s := by
    calc
      _ ≤ (s - 1) / s := div_le_div_of_nonneg_left (by linarith) hs (by linarith)
      _ = _ := by field_simp
  have hrexp : r ≤ Real.exp (-(1 / s)) := by
    have h := Real.add_one_le_exp (-(1 / s))
    linarith
  have hp := pow_le_pow_left₀ hr0 hrexp (2 * d)
  have hexponent : ((2 * d : ℕ) : ℝ) * (-(1 / s)) ≤ (-2 : ℝ) := by
    have hds : s ≤ (d : ℝ) := hd
    have hcast : ((2 * d : ℕ) : ℝ) = 2 * (d : ℝ) := by push_cast; rfl
    rw [hcast]
    have hdiv : (2 : ℝ) ≤ 2 * (d : ℝ) / s := by
      apply (le_div_iff₀ hs).2
      nlinarith
    calc
      _ = -(2 * (d : ℝ) / s) := by ring
      _ ≤ -2 := neg_le_neg hdiv
  have hexp3 : (3 : ℝ) ≤ Real.exp 2 := by
    have h := Real.add_one_le_exp (2 : ℝ)
    norm_num at h
    exact h
  have hexp : Real.exp (-2) ≤ (1 : ℝ) / 3 := by
    rw [Real.exp_neg]
    simpa only [one_div] using
      (inv_le_inv₀ (Real.exp_pos (2 : ℝ)) (by norm_num : (0 : ℝ) < 3)).2 hexp3
  refine ⟨hr0, ?_⟩
  calc
    _ ≤ (Real.exp (-(1 / s))) ^ (2 * d) := hp
    _ = Real.exp (((2 * d : ℕ) : ℝ) * (-(1 / s))) :=
      (Real.exp_nat_mul _ _).symm
    _ ≤ Real.exp (-2) := Real.exp_le_exp.mpr hexponent
    _ ≤ _ := hexp

private theorem source_norm_scale_lower {d : ℕ} (hd : 0 < (d : ℝ))
    {δ κ : ℝ} (hκ0 : 0 < κ) (hκcap : κ ≤ (d : ℝ) ^ (1 - δ)) :
    (d : ℝ) ^ ((1 + δ) / 2) / 2 ≤ (d : ℝ) / (2 * Real.sqrt κ) := by
  have hs : 0 < Real.sqrt κ := Real.sqrt_pos.2 hκ0
  have hroot : Real.sqrt κ ≤ (d : ℝ) ^ ((1 - δ) / 2) := by
    calc
      _ ≤ Real.sqrt ((d : ℝ) ^ (1 - δ)) := Real.sqrt_le_sqrt hκcap
      _ = _ := by
        rw [Real.sqrt_eq_rpow, ← Real.rpow_mul hd.le]
        congr 1
        ring
  apply (le_div_iff₀ (by positivity : 0 < 2 * Real.sqrt κ)).2
  have hmul := mul_le_mul_of_nonneg_left hroot
    (Real.rpow_nonneg hd.le ((1 + δ) / 2))
  have heq : (d : ℝ) ^ ((1 + δ) / 2) * (d : ℝ) ^ ((1 - δ) / 2) = (d : ℝ) := by
    rw [← Real.rpow_add hd, show ((1 + δ) / 2 + (1 - δ) / 2 : ℝ) = 1 by ring,
      Real.rpow_one]
  rw [heq] at hmul
  nlinarith

theorem eventual_actual_gaussian_signal_strength {δ : ℝ} (hδ0 : 0 < δ) (hδ1 : δ < 1) :
  ∃ d₀ : ℕ, ∀ (d : ℕ), d₀ ≤ d → ∀ (κ : ℝ), 2 ≤ κ →
    κ ≤ (d : ℝ) ^ (1 - δ) → ∀ (q : ℕ),
    (q : ℝ) ≤ (δ / 256) * Real.sqrt κ * Real.log (d : ℝ) →
    let n : ℕ := 2 * q + 1
    let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
    let eigenvalue : Fin d → ℝ := fun i => (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i)
    let Λ : Matrix (Fin d) (Fin d) ℝ := Matrix.diagonal eigenvalue
    let μ : Measure (EuclideanSpace ℝ (Fin d)) :=
      multivariateGaussian (0 : EuclideanSpace ℝ (Fin d)) Λ⁻¹
    let Q : EuclideanSpace ℝ (Fin d) → ℝ := fun x =>
      ∑ i : Fin d, Real.cos ((n : ℝ) * θ i) * (WithLp.ofLp x i) ^ 2
    let M : ℝ := ∫ x : EuclideanSpace ℝ (Fin d), ‖x‖ ^ 2 ∂μ
    let b : ℝ := ∫ x : EuclideanSpace ℝ (Fin d), Q x ∂μ
    let β : ℝ := |b| / M
    let B : ℝ := (1 - Real.exp (-4)) * Real.exp (-3)
    0 < M ∧ 0 < β ∧ (d : ℝ) / (2 * Real.sqrt κ) ≤ M ∧
      (d : ℝ) ^ ((1 + δ) / 2) / 2 ≤ M ∧
      (B ^ 2 / 2) * Real.sqrt (d : ℝ) ≤ M * β ^ 2
 := by
  rcases eventual_source_query_mode_gap hδ0 hδ1 with ⟨D, hD⟩
  refine ⟨D, ?_⟩
  intro d hd κ hκ hκcap q hq
  let n : ℕ := 2 * q + 1
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let eigenvalue : Fin d → ℝ := fun i => (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i)
  let Λ : Matrix (Fin d) (Fin d) ℝ := Matrix.diagonal eigenvalue
  let μ : Measure (EuclideanSpace ℝ (Fin d)) := multivariateGaussian 0 Λ⁻¹
  let Q : EuclideanSpace ℝ (Fin d) → ℝ := fun x =>
    ∑ i : Fin d, Real.cos ((n : ℝ) * θ i) * (WithLp.ofLp x i) ^ 2
  let M : ℝ := ∫ x : EuclideanSpace ℝ (Fin d), ‖x‖ ^ 2 ∂μ
  let b : ℝ := ∫ x : EuclideanSpace ℝ (Fin d), Q x ∂μ
  let β : ℝ := |b| / M
  let C : ℝ := 1 - Real.exp (-4)
  let B : ℝ := C * Real.exp (-3)
  change 0 < M ∧ 0 < β ∧ (d : ℝ) / (2 * Real.sqrt κ) ≤ M ∧
    (d : ℝ) ^ ((1 + δ) / 2) / 2 ≤ M ∧
    (B ^ 2 / 2) * Real.sqrt (d : ℝ) ≤ M * β ^ 2
  have hadm := hD d hd κ hκ hκcap q hq
  change 2 ≤ d ∧ 1 ≤ n ∧ n < d ∧ Real.sqrt κ ≤ (d : ℝ) - (n : ℝ) at hadm
  rcases hadm with ⟨hd2, hn1, hnd, hgap⟩
  rcases actual_diagonal_gaussian_exponential_bias hd2 hκ n hn1 hnd hgap with
    ⟨hMpos, hsignpos, hlow, _hupp⟩
  change 0 < M at hMpos
  change 0 < (-1 : ℝ) ^ n * b at hsignpos
  change C * Real.exp (-3 * (n : ℝ) / Real.sqrt κ) ≤ β at hlow
  have hdpos : 0 < (d : ℝ) := by exact_mod_cast (by omega : 0 < d)
  have hd1 : (1 : ℝ) ≤ (d : ℝ) := by exact_mod_cast (by omega : 1 ≤ d)
  have hlog0 : 0 ≤ Real.log (d : ℝ) := Real.log_nonneg hd1
  have hspos : 0 < Real.sqrt κ := Real.sqrt_pos.2 (by linarith)
  have hsone : (1 : ℝ) ≤ Real.sqrt κ := Real.le_sqrt_of_sq_le (by nlinarith)
  have hds : Real.sqrt κ ≤ (d : ℝ) := by
    have hn0 : (0 : ℝ) ≤ (n : ℝ) := Nat.cast_nonneg _
    linarith
  let r : ℝ := (Real.sqrt κ - 1) / (Real.sqrt κ + 1)
  rcases spectral_tail_le_third hκ d hds with ⟨hr0, htail⟩
  change 0 ≤ r at hr0
  change r ^ (2 * d) ≤ (1 : ℝ) / 3 at htail
  have hclosed := actual_diagonal_gaussian_exact_means hd2 hκ n hn1 hnd
  have hMformula : M = ((d : ℝ) / Real.sqrt κ) *
      ((1 - r ^ (2 * d)) / (1 + r ^ (2 * d))) := hclosed.2.2.1
  have hu0 : 0 ≤ r ^ (2 * d) := pow_nonneg hr0 _
  have hden : 0 < 1 + r ^ (2 * d) := by positivity
  have hcorrection : (1 : ℝ) / 2 ≤ (1 - r ^ (2 * d)) / (1 + r ^ (2 * d)) := by
    apply (le_div_iff₀ hden).2
    nlinarith
  have hMlower : (d : ℝ) / (2 * Real.sqrt κ) ≤ M := by
    rw [hMformula]
    calc
      _ = ((d : ℝ) / Real.sqrt κ) * (1 / 2) := by ring
      _ ≤ _ := mul_le_mul_of_nonneg_left hcorrection (by positivity)
  have hMpower : (d : ℝ) ^ ((1 + δ) / 2) / 2 ≤ M :=
    (source_norm_scale_lower hdpos (by linarith : 0 < κ) hκcap).trans hMlower
  have hbne : b ≠ 0 := by
    intro h
    rw [h, mul_zero] at hsignpos
    exact (lt_irrefl 0) hsignpos
  have hβpos : 0 < β := div_pos (abs_pos.mpr hbne) hMpos
  have hqr : (q : ℝ) / Real.sqrt κ ≤ (δ / 256) * Real.log (d : ℝ) := by
    apply (div_le_iff₀ hspos).2
    calc
      _ ≤ (δ / 256) * Real.sqrt κ * Real.log (d : ℝ) := hq
      _ = _ := by ring
  have h3s : 3 / Real.sqrt κ ≤ (3 : ℝ) := by
    apply (div_le_iff₀ hspos).2
    nlinarith
  have hncalc : 3 * (n : ℝ) / Real.sqrt κ =
      6 * ((q : ℝ) / Real.sqrt κ) + 3 / Real.sqrt κ := by
    simp only [n, Nat.cast_add, Nat.cast_mul, Nat.cast_ofNat]
    ring
  have hns : 3 * (n : ℝ) / Real.sqrt κ ≤
      3 + (3 * δ / 128) * Real.log (d : ℝ) := by
    calc
      _ = 6 * ((q : ℝ) / Real.sqrt κ) + 3 / Real.sqrt κ := hncalc
      _ ≤ 6 * ((δ / 256) * Real.log (d : ℝ)) + 3 :=
        add_le_add (mul_le_mul_of_nonneg_left hqr (by norm_num)) h3s
      _ = _ := by ring
  have hrelax : 3 + (3 * δ / 128) * Real.log (d : ℝ) ≤
      3 + (δ / 4) * Real.log (d : ℝ) := by
    have hc : 3 * δ / 128 ≤ δ / 4 := by nlinarith
    exact add_le_add le_rfl (mul_le_mul_of_nonneg_right hc hlog0)
  have hexponent : -3 + Real.log (d : ℝ) * (-δ / 4) ≤
      -3 * (n : ℝ) / Real.sqrt κ := by
    calc
      _ = -(3 + (δ / 4) * Real.log (d : ℝ)) := by ring
      _ ≤ -(3 * (n : ℝ) / Real.sqrt κ) := neg_le_neg (hns.trans hrelax)
      _ = _ := by ring
  have he4 : Real.exp (-4) < 1 := by
    simpa only [Real.exp_zero] using Real.exp_lt_exp.mpr (by norm_num : (-4 : ℝ) < 0)
  have hCpos : 0 < C := by dsimp [C]; linarith
  have hBpos : 0 < B := mul_pos hCpos (Real.exp_pos _)
  have hpoly : B * (d : ℝ) ^ (-δ / 4) ≤ β := by
    calc
      _ = C * (Real.exp (-3) * Real.exp (Real.log (d : ℝ) * (-δ / 4))) := by
        rw [Real.rpow_def_of_pos hdpos]
        ring
      _ = C * Real.exp (-3 + Real.log (d : ℝ) * (-δ / 4)) := by rw [Real.exp_add]
      _ ≤ C * Real.exp (-3 * (n : ℝ) / Real.sqrt κ) :=
        mul_le_mul_of_nonneg_left (Real.exp_le_exp.mpr hexponent) hCpos.le
      _ ≤ β := hlow
  have hpoly0 : 0 ≤ B * (d : ℝ) ^ (-δ / 4) := by positivity
  have hsquare : (B * (d : ℝ) ^ (-δ / 4)) ^ 2 ≤ β ^ 2 :=
    pow_le_pow_left₀ hpoly0 hpoly 2
  have hsignal := mul_le_mul hMpower hsquare
    (sq_nonneg (B * (d : ℝ) ^ (-δ / 4))) hMpos.le
  have hpowerproduct : (d : ℝ) ^ ((1 + δ) / 2) * ((d : ℝ) ^ (-δ / 4)) ^ 2 =
      Real.sqrt (d : ℝ) := by
    rw [← Real.rpow_mul_natCast hdpos.le, ← Real.rpow_add hdpos]
    rw [show ((1 + δ) / 2 + (-δ / 4) * (2 : ℕ) : ℝ) = 1 / 2 by push_cast; ring]
    exact (Real.sqrt_eq_rpow (d : ℝ)).symm
  have hsignalidentity : (d : ℝ) ^ ((1 + δ) / 2) / 2 *
      (B * (d : ℝ) ^ (-δ / 4)) ^ 2 = (B ^ 2 / 2) * Real.sqrt (d : ℝ) := by
    rw [mul_pow]
    calc
      _ = (B ^ 2 / 2) * ((d : ℝ) ^ ((1 + δ) / 2) * ((d : ℝ) ^ (-δ / 4)) ^ 2) := by ring
      _ = _ := by rw [hpowerproduct]
  refine ⟨hMpos, hβpos, hMlower, hMpower, ?_⟩
  calc
    _ = (d : ℝ) ^ ((1 + δ) / 2) / 2 * (B * (d : ℝ) ^ (-δ / 4)) ^ 2 := hsignalidentity.symm
    _ ≤ M * β ^ 2 := hsignal

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSignalStrength
