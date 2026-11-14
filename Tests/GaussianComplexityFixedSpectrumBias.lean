import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumBias
import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumVariances

/-!
Private NON-ANCHOR actual-law numerical consumer. The event has zero
threshold; it does not assert that the source concrete tau_dq is zero,
identify a rotated algorithmic event, or prove the full source Ex26.
The constant2 and exponent6 are local Chebyshev algebra with the actual
Q variance bound2M and the new lower exponential actual bias.
-/
noncomputable section
open MeasureTheory ProbabilityTheory
open scoped BigOperators
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumBias
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumVariances

private theorem actual_gaussian_zero_threshold_probability_le {d : ℕ} (hd : 2 ≤ d) {κ : ℝ} (hκ : 2 ≤ κ)
    (n : ℕ) (hn : 1 ≤ n) (hnd : n < d) (hgap : Real.sqrt κ ≤ (d : ℝ) - (n : ℝ)) :
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let eigenvalue : Fin d → ℝ := fun i => (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i)
  let Λ : Matrix (Fin d) (Fin d) ℝ := Matrix.diagonal eigenvalue
  let μ : Measure (EuclideanSpace ℝ (Fin d)) :=
    multivariateGaussian (0 : EuclideanSpace ℝ (Fin d)) Λ⁻¹
  let Q : EuclideanSpace ℝ (Fin d) → ℝ := fun x =>
    ∑ i : Fin d, Real.cos ((n : ℝ) * θ i) * (WithLp.ofLp x i) ^ 2
  let M : ℝ := ∫ x : EuclideanSpace ℝ (Fin d), ‖x‖ ^ 2 ∂μ
  (μ {x : EuclideanSpace ℝ (Fin d) | (-1 : ℝ) ^ n * Q x ≤ 0}).toReal ≤
    2 * Real.exp (6 * (n : ℝ) / Real.sqrt κ) / ((1 - Real.exp (-4)) ^ 2 * M) := by
  classical
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let eigenvalue : Fin d → ℝ := fun i => (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i)
  let Λ : Matrix (Fin d) (Fin d) ℝ := Matrix.diagonal eigenvalue
  let μ : Measure (EuclideanSpace ℝ (Fin d)) := multivariateGaussian 0 Λ⁻¹
  let Q : EuclideanSpace ℝ (Fin d) → ℝ := fun x =>
    ∑ i : Fin d, Real.cos ((n : ℝ) * θ i) * (WithLp.ofLp x i) ^ 2
  let M : ℝ := ∫ x : EuclideanSpace ℝ (Fin d), ‖x‖ ^ 2 ∂μ
  let b : ℝ := ∫ x : EuclideanSpace ℝ (Fin d), Q x ∂μ
  let X : EuclideanSpace ℝ (Fin d) → ℝ := fun x => (-1 : ℝ) ^ n * Q x
  let B : ℝ := (-1 : ℝ) ^ n * b
  let C : ℝ := 1 - Real.exp (-4)
  let L : ℝ := C * Real.exp (-3 * (n : ℝ) / Real.sqrt κ) * M
  change (μ {x | X x ≤ 0}).toReal ≤
    2 * Real.exp (6 * (n : ℝ) / Real.sqrt κ) / (C ^ 2 * M)
  rcases actual_diagonal_gaussian_exponential_bias hd hκ n hn hnd hgap with
    ⟨hMpos, hBpos, hlow, _hupp⟩
  rcases actual_diagonal_gaussian_quadratic_variances hd hκ n hn hnd with
    ⟨_hN, hQ, _hNexact, _hQexact, _hNbound, hQbound, _hMupper⟩
  change 0 < M at hMpos
  change 0 < B at hBpos
  have hX : MemLp X 2 μ := hQ.const_mul _
  have hmean : (∫ x, X x ∂μ) = B := by exact integral_const_mul _ _
  have habs : |b| = B := by
    calc
      |b| = |(-1 : ℝ) ^ n * b| := by rw [abs_mul, abs_neg_one_pow, one_mul]
      _ = _ := abs_of_pos hBpos
  have he4 : Real.exp (-4) < 1 := by
    simpa only [Real.exp_zero] using Real.exp_lt_exp.mpr (by norm_num : (-4 : ℝ) < 0)
  have hCpos : 0 < C := by dsimp [C]; linarith
  have hLpos : 0 < L := mul_pos (mul_pos hCpos (Real.exp_pos _)) hMpos
  have hLB : L ≤ B := by
    have h := (le_div_iff₀ hMpos).mp hlow
    rw [habs] at h
    exact h
  have hsign : ((-1 : ℝ) ^ n) ^ 2 = 1 := by
    rw [← pow_mul, Nat.mul_comm, pow_mul]
    norm_num
  have hV : Var[X; μ] ≤ 2 * M := by
    change Var[fun x => (-1 : ℝ) ^ n * Q x; μ] ≤ _
    rw [variance_const_mul, hsign, one_mul]
    exact hQbound
  have hsub : {x | X x ≤ 0} ⊆ {x | B ≤ |X x - (∫ y, X y ∂μ)|} := by
    intro x hx
    change X x ≤ 0 at hx
    change B ≤ |X x - (∫ y, X y ∂μ)|
    rw [hmean, abs_of_nonpos (by linarith : X x - B ≤ 0)]
    linarith
  have hc := meas_ge_le_variance_div_sq hX hBpos
  have hm : μ {x | X x ≤ 0} ≤ ENNReal.ofReal (Var[X; μ] / B ^ 2) :=
    (measure_mono hsub).trans (by simpa only [hmean] using hc)
  have hprob : (μ {x | X x ≤ 0}).toReal ≤ Var[X; μ] / B ^ 2 := by
    calc
      _ ≤ (ENNReal.ofReal (Var[X; μ] / B ^ 2)).toReal :=
        ENNReal.toReal_mono ENNReal.ofReal_ne_top hm
      _ = _ := ENNReal.toReal_ofReal (div_nonneg (variance_nonneg _ _) (sq_nonneg _))
  have hbsq : L ^ 2 ≤ B ^ 2 := pow_le_pow_left₀ hLpos.le hLB 2
  have hExpSq : (Real.exp (-3 * (n : ℝ) / Real.sqrt κ)) ^ 2 =
      (Real.exp (6 * (n : ℝ) / Real.sqrt κ))⁻¹ := by
    rw [← Real.exp_nat_mul]
    norm_num only [Nat.cast_ofNat]
    rw [show (2 : ℝ) * (-3 * (n : ℝ) / Real.sqrt κ) = -(6 * (n : ℝ) / Real.sqrt κ) by ring,
      Real.exp_neg]
  calc
    _ ≤ Var[X; μ] / B ^ 2 := hprob
    _ ≤ 2 * M / B ^ 2 := div_le_div_of_nonneg_right hV (sq_nonneg B)
    _ ≤ 2 * M / L ^ 2 :=
      div_le_div_of_nonneg_left (by positivity) (sq_pos_of_pos hLpos) hbsq
    _ = _ := by
      dsimp [L]
      rw [mul_pow, mul_pow, hExpSq]
      field_simp [ne_of_gt hCpos, ne_of_gt hMpos, Real.exp_ne_zero]
