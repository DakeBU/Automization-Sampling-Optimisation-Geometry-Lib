import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSignalStrength
import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumVariances

/-!
Private NON-ANCHOR actual-law numerical consumer of the new signal strength.
One enlarged delta-only output threshold gives signed-Q<=0 probability<=1/10
for every original admitted condition/query cap. Actual moments, variance,
sign and finite-measure conversion are proved internally. This is a ZERO
threshold, diagonal-law event; concrete tau, the shifted rotated detector,
full Ex26, algorithms/oracle/TV/cost and main lower bounds remain open.
-/

noncomputable section
open MeasureTheory ProbabilityTheory
open scoped BigOperators
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSignalStrength
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumModeGap
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumBias
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumVariances

private theorem actual_gaussian_source_query_zero_event_le_tenth {δ : ℝ}
    (hδ0 : 0 < δ) (hδ1 : δ < 1) :
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
    (μ {x | (-1 : ℝ) ^ n * Q x ≤ 0}).toReal ≤ (1 : ℝ) / 10
 := by
  let B : ℝ := (1 - Real.exp (-4)) * Real.exp (-3)
  have he4 : Real.exp (-4) < 1 := by
    simpa only [Real.exp_zero] using Real.exp_lt_exp.mpr (by norm_num : (-4 : ℝ) < 0)
  have hBpos : 0 < B := mul_pos (by linarith) (Real.exp_pos _)
  obtain ⟨N, hN⟩ := exists_nat_ge (40 / B ^ 2)
  rcases eventual_actual_gaussian_signal_strength hδ0 hδ1 with ⟨D, hD⟩
  rcases eventual_source_query_mode_gap hδ0 hδ1 with ⟨K, hK⟩
  refine ⟨max D (max K (N ^ 2)), ?_⟩
  intro d hd κ hκ hκcap q hq
  have hdD : D ≤ d := (le_max_left D (max K (N ^ 2))).trans hd
  have hdKN : max K (N ^ 2) ≤ d := (le_max_right D (max K (N ^ 2))).trans hd
  have hdK : K ≤ d := (le_max_left K (N ^ 2)).trans hdKN
  have hdN : N ^ 2 ≤ d := (le_max_right K (N ^ 2)).trans hdKN
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
  let X : EuclideanSpace ℝ (Fin d) → ℝ := fun x => (-1 : ℝ) ^ n * Q x
  let m : ℝ := (-1 : ℝ) ^ n * b
  change (μ {x | X x ≤ 0}).toReal ≤ (1 : ℝ) / 10
  have hadm := hK d hdK κ hκ hκcap q hq
  change 2 ≤ d ∧ 1 ≤ n ∧ n < d ∧ Real.sqrt κ ≤ (d : ℝ) - (n : ℝ) at hadm
  rcases hadm with ⟨hd2, hn1, hnd, hgap⟩
  have hs := hD d hdD κ hκ hκcap q hq
  change 0 < M ∧ 0 < β ∧ (d : ℝ) / (2 * Real.sqrt κ) ≤ M ∧
    (d : ℝ) ^ ((1 + δ) / 2) / 2 ≤ M ∧
    (B ^ 2 / 2) * Real.sqrt (d : ℝ) ≤ M * β ^ 2 at hs
  rcases hs with ⟨hMpos, _hβpos, _hMlower, _hMpower, hproduct⟩
  have hNsq : (N : ℝ) ^ 2 ≤ (d : ℝ) := by exact_mod_cast hdN
  have hNsqrt : (N : ℝ) ≤ Real.sqrt (d : ℝ) := Real.le_sqrt_of_sq_le hNsq
  have hthreshold : (20 : ℝ) ≤ (B ^ 2 / 2) * Real.sqrt (d : ℝ) := by
    have ht := mul_le_mul_of_nonneg_left (hN.trans hNsqrt)
      (by positivity : 0 ≤ B ^ 2 / 2)
    have heq : (B ^ 2 / 2) * (40 / B ^ 2) = (20 : ℝ) := by
      field_simp [ne_of_gt hBpos]; ring
    rw [heq] at ht
    exact ht
  have hsignal : (20 : ℝ) ≤ M * β ^ 2 := hthreshold.trans hproduct
  rcases actual_diagonal_gaussian_exponential_bias hd2 hκ n hn1 hnd hgap with
    ⟨_hMposBias, hmpos, _hlow, _hupp⟩
  change 0 < m at hmpos
  rcases actual_diagonal_gaussian_quadratic_variances hd2 hκ n hn1 hnd with
    ⟨_hNmem, hQmem, _hNexact, _hQexact, _hNbound, hQbound, _hMupper⟩
  have hX : MemLp X 2 μ := hQmem.const_mul _
  have hmean : (∫ x, X x ∂μ) = m := by exact integral_const_mul _ _
  have habs : |b| = m := by
    calc
      |b| = |(-1 : ℝ) ^ n * b| := by rw [abs_mul, abs_neg_one_pow, one_mul]
      _ = _ := abs_of_pos hmpos
  have hmeanRatio : m = β * M := by
    dsimp [β]
    rw [habs]
    exact (div_mul_cancel₀ m (ne_of_gt hMpos)).symm
  have hmeansq : m ^ 2 = (M * β ^ 2) * M := by rw [hmeanRatio]; ring
  have hlarge : 20 * M ≤ m ^ 2 := by
    have h := mul_le_mul_of_nonneg_right hsignal hMpos.le
    rw [← hmeansq] at h
    exact h
  have hsign : ((-1 : ℝ) ^ n) ^ 2 = 1 := by
    rw [← pow_mul, Nat.mul_comm, pow_mul]
    norm_num
  have hV : Var[X; μ] ≤ 2 * M := by
    change Var[fun x => (-1 : ℝ) ^ n * Q x; μ] ≤ _
    rw [variance_const_mul, hsign, one_mul]
    exact hQbound
  have hsub : {x | X x ≤ 0} ⊆ {x | m ≤ |X x - (∫ y, X y ∂μ)|} := by
    intro x hx
    change X x ≤ 0 at hx
    change m ≤ |X x - (∫ y, X y ∂μ)|
    rw [hmean, abs_of_nonpos (by linarith : X x - m ≤ 0)]
    linarith
  have hc := meas_ge_le_variance_div_sq hX hmpos
  have hm : μ {x | X x ≤ 0} ≤ ENNReal.ofReal (Var[X; μ] / m ^ 2) :=
    (measure_mono hsub).trans (by simpa only [hmean] using hc)
  have hprob : (μ {x | X x ≤ 0}).toReal ≤ Var[X; μ] / m ^ 2 := by
    calc
      _ ≤ (ENNReal.ofReal (Var[X; μ] / m ^ 2)).toReal :=
        ENNReal.toReal_mono ENNReal.ofReal_ne_top hm
      _ = _ := ENNReal.toReal_ofReal (div_nonneg (variance_nonneg _ _) (sq_nonneg _))
  calc
    _ ≤ Var[X; μ] / m ^ 2 := hprob
    _ ≤ 2 * M / m ^ 2 := div_le_div_of_nonneg_right hV (sq_nonneg m)
    _ ≤ (1 : ℝ) / 10 := by
      apply (div_le_iff₀ (sq_pos_of_pos hmpos)).2
      nlinarith
