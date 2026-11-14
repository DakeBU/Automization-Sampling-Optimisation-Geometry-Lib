import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumModeGap
import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumBias

/-!
Private actual diagonal-Gaussian source-mode application of Section4.3 Ex23.
The new uniform dimension/mode/gap conclusions supply the actual Bias inputs;
the original q-cap gives the polynomial rate with exact constant
(1-exp(-4))*exp(-3). This numerical component is NON-ANCHOR. Concrete tau,
shifted events, rotated algorithmic laws, TV/oracle/cost and main bounds
remain separate obligations.
-/
noncomputable section
open MeasureTheory ProbabilityTheory
open scoped BigOperators
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumModeGap
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumBias

private theorem actual_gaussian_source_query_bias_power_lower {δ : ℝ} (hδ0 : 0 < δ) (hδ1 : δ < 1) :
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
    0 < M ∧ 0 < (-1 : ℝ) ^ n * b ∧
      ((1 - Real.exp (-4)) * Real.exp (-3)) * (d : ℝ) ^ (-δ / 4) ≤ |b| / M := by

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
  let C : ℝ := 1 - Real.exp (-4)
  change 0 < M ∧ 0 < (-1 : ℝ) ^ n * b ∧
    (C * Real.exp (-3)) * (d : ℝ) ^ (-δ / 4) ≤ |b| / M
  have hadm := hD d hd κ hκ hκcap q hq
  change 2 ≤ d ∧ 1 ≤ n ∧ n < d ∧ Real.sqrt κ ≤ (d : ℝ) - (n : ℝ) at hadm
  rcases hadm with ⟨hd2, hn1, hnd, hgap⟩
  rcases actual_diagonal_gaussian_exponential_bias hd2 hκ n hn1 hnd hgap with
    ⟨hMpos, hBpos, hlow, _hupp⟩
  refine ⟨hMpos, hBpos, ?_⟩
  have hdpos : 0 < (d : ℝ) := by exact_mod_cast (by omega : 0 < d)
  have hd1 : (1 : ℝ) ≤ (d : ℝ) := by exact_mod_cast (by omega : 1 ≤ d)
  have hlog0 : 0 ≤ Real.log (d : ℝ) := Real.log_nonneg hd1
  have hspos : 0 < Real.sqrt κ := Real.sqrt_pos.2 (by linarith)
  have hsone : (1 : ℝ) ≤ Real.sqrt κ := Real.le_sqrt_of_sq_le (by nlinarith)
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
  have hC0 : 0 ≤ C := by dsimp [C]; linarith
  calc
    _ = C * (Real.exp (-3) * Real.exp (Real.log (d : ℝ) * (-δ / 4))) := by
      rw [Real.rpow_def_of_pos hdpos]
      ring
    _ = C * Real.exp (-3 + Real.log (d : ℝ) * (-δ / 4)) := by rw [Real.exp_add]
    _ ≤ C * Real.exp (-3 * (n : ℝ) / Real.sqrt κ) :=
      mul_le_mul_of_nonneg_left (Real.exp_le_exp.mpr hexponent) hC0
    _ ≤ |b| / M := hlow
