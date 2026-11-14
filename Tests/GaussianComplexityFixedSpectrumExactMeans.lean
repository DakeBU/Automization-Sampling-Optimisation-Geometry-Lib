import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumExactMeans

/-!
An actual consumer of both C.8 means: the normalized bias identity at
Appendix C.3 p9/Ex150 and the mean upper bound at p8.2. The variables m,b
are literal Gaussian integrals, with all signs and denominators derived.
No variance, concentration or full Lemma 4.5 claim is made here.
-/

noncomputable section
open MeasureTheory ProbabilityTheory
open scoped BigOperators
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumExactMeans

private theorem actual_gaussian_closed_means_bias_ratio {d : ℕ} (hd : 2 ≤ d) {κ : ℝ} (hκ : 2 ≤ κ)
    (n : ℕ) (hn : 1 ≤ n) (hnd : n < d) :
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let eigenvalue : Fin d → ℝ := fun i => (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i)
  let Λ : Matrix (Fin d) (Fin d) ℝ := Matrix.diagonal eigenvalue
  let μ : Measure (EuclideanSpace ℝ (Fin d)) :=
    multivariateGaussian (0 : EuclideanSpace ℝ (Fin d)) Λ⁻¹
  let Q : EuclideanSpace ℝ (Fin d) → ℝ := fun x =>
    ∑ i : Fin d, Real.cos ((n : ℝ) * θ i) * (WithLp.ofLp x i) ^ 2
  let r : ℝ := (Real.sqrt κ - 1) / (Real.sqrt κ + 1)
  let m : ℝ := ∫ x : EuclideanSpace ℝ (Fin d), ‖x‖ ^ 2 ∂μ
  let b : ℝ := ∫ x : EuclideanSpace ℝ (Fin d), Q x ∂μ
  0 < m ∧ m ≤ (d : ℝ) / Real.sqrt κ ∧ 0 < (-1 : ℝ) ^ n * b ∧
  |b| / m = r ^ n * ((1 - r ^ (2 * (d - n))) / (1 - r ^ (2 * d))) := by
  classical
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let eigenvalue : Fin d → ℝ := fun i => (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i)
  let Λ : Matrix (Fin d) (Fin d) ℝ := Matrix.diagonal eigenvalue
  let μ : Measure (EuclideanSpace ℝ (Fin d)) := multivariateGaussian 0 Λ⁻¹
  let Q : EuclideanSpace ℝ (Fin d) → ℝ := fun x =>
    ∑ i : Fin d, Real.cos ((n : ℝ) * θ i) * (WithLp.ofLp x i) ^ 2
  let r : ℝ := (Real.sqrt κ - 1) / (Real.sqrt κ + 1)
  let m : ℝ := ∫ x : EuclideanSpace ℝ (Fin d), ‖x‖ ^ 2 ∂μ
  let b : ℝ := ∫ x : EuclideanSpace ℝ (Fin d), Q x ∂μ
  change 0 < m ∧ m ≤ (d : ℝ) / Real.sqrt κ ∧ 0 < (-1 : ℝ) ^ n * b ∧
    |b| / m = r ^ n * ((1 - r ^ (2 * (d - n))) / (1 - r ^ (2 * d)))
  have hclosed := actual_diagonal_gaussian_exact_means hd hκ n hn hnd
  have hm : m = ((d : ℝ) / Real.sqrt κ) *
      ((1 - r ^ (2 * d)) / (1 + r ^ (2 * d))) := hclosed.2.2.1
  have hb : (-1 : ℝ) ^ n * b = ((d : ℝ) / Real.sqrt κ) *
      ((r ^ n - r ^ (2 * d - n)) / (1 + r ^ (2 * d))) := hclosed.2.2.2
  have hsqrt : 1 < Real.sqrt κ := by
    nlinarith [Real.sqrt_nonneg κ, Real.sq_sqrt (by linarith : 0 ≤ κ)]
  have hr0 : 0 < r := div_pos (by linarith) (by linarith)
  have hr1 : r < 1 := by
    dsimp [r]
    apply (div_lt_one (by linarith : 0 < Real.sqrt κ + 1)).2
    linarith
  have hscale : 0 < (d : ℝ) / Real.sqrt κ :=
    div_pos (by exact_mod_cast (by omega : 0 < d)) (by linarith)
  have hτ0 : 0 ≤ r ^ (2 * d) := pow_nonneg hr0.le _
  have hτ1 : r ^ (2 * d) < 1 := pow_lt_one₀ hr0.le hr1 (by omega)
  have hden : 0 < 1 + r ^ (2 * d) := by positivity
  have hmpos : 0 < m := by rw [hm]; exact mul_pos hscale (div_pos (by linarith) hden)
  have hmupper : m ≤ (d : ℝ) / Real.sqrt κ := by
    rw [hm]
    exact mul_le_of_le_one_right hscale.le ((div_le_one hden).2 (by linarith))
  have hgap : n + 2 * (d - n) = 2 * d - n := by omega
  have hfactor : r ^ n - r ^ (2 * d - n) = r ^ n * (1 - r ^ (2 * (d - n))) := by
    rw [← hgap, pow_add]
    ring
  have hsmall : r ^ (2 * (d - n)) < 1 := pow_lt_one₀ hr0.le hr1 (by omega)
  have hbpos : 0 < (-1 : ℝ) ^ n * b := by
    rw [hb, hfactor]
    exact mul_pos hscale (div_pos (mul_pos (pow_pos hr0 _) (by linarith)) hden)
  have habs : |b| = (-1 : ℝ) ^ n * b := by
    calc
      |b| = |(-1 : ℝ) ^ n * b| := by rw [abs_mul, abs_neg_one_pow, one_mul]
      _ = _ := abs_of_pos hbpos
  refine ⟨hmpos, hmupper, hbpos, ?_⟩
  rw [habs, hb, hm, hfactor]
  field_simp [ne_of_gt hscale, ne_of_gt hden, ne_of_gt (by linarith : 0 < 1 - r ^ (2 * d))]
