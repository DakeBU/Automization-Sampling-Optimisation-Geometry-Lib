import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumGaussianMoments
import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumGridAlias
import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCosineExpansion

open MeasureTheory ProbabilityTheory
open scoped BigOperators
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumGaussianMoments
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumGridAlias
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCosineExpansion

private theorem actual_gaussian_cosine_alias_series {d : ℕ} (hd : 2 ≤ d) {κ : ℝ} (hκ : 2 ≤ κ)
    (n : ℕ) (hn : 1 ≤ n) (hnd : n < d) :
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let eigenvalue : Fin d → ℝ := fun i => (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i)
  let Λ : Matrix (Fin d) (Fin d) ℝ := Matrix.diagonal eigenvalue
  let μ : Measure (EuclideanSpace ℝ (Fin d)) :=
    multivariateGaussian (0 : EuclideanSpace ℝ (Fin d)) Λ⁻¹
  let Q : EuclideanSpace ℝ (Fin d) → ℝ := fun x =>
    ∑ i : Fin d, Real.cos ((n : ℝ) * θ i) * (WithLp.ofLp x i) ^ 2
  let r : ℝ := (Real.sqrt κ - 1) / (Real.sqrt κ + 1)
  let a : ℤ → ℝ := fun k =>
    if (2 * (d : ℤ)) ∣ k then (-1 : ℝ) ^ (k / (2 * (d : ℤ))) else 0
  Summable (fun j : ℕ => (-r) ^ (j + 1) *
    (a (((j + 1 : ℕ) : ℤ) - (n : ℤ)) + a (((j + 1 : ℕ) : ℤ) + (n : ℤ)))) ∧
  Integrable Q μ ∧
  (∫ x : EuclideanSpace ℝ (Fin d), Q x ∂μ) =
    ((d : ℝ) / Real.sqrt κ) * ∑' j : ℕ, (-r) ^ (j + 1) *
      (a (((j + 1 : ℕ) : ℤ) - (n : ℤ)) + a (((j + 1 : ℕ) : ℤ) + (n : ℤ))) := by
  classical
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let eigenvalue : Fin d → ℝ := fun i => (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i)
  let Λ : Matrix (Fin d) (Fin d) ℝ := Matrix.diagonal eigenvalue
  let μ : Measure (EuclideanSpace ℝ (Fin d)) := multivariateGaussian 0 Λ⁻¹
  let Q : EuclideanSpace ℝ (Fin d) → ℝ := fun x =>
    ∑ i : Fin d, Real.cos ((n : ℝ) * θ i) * (WithLp.ofLp x i) ^ 2
  let r : ℝ := (Real.sqrt κ - 1) / (Real.sqrt κ + 1)
  let a : ℤ → ℝ := fun k =>
    if (2 * (d : ℤ)) ∣ k then (-1 : ℝ) ^ (k / (2 * (d : ℤ))) else 0
  let w : Fin d → ℝ := fun i => Real.cos ((n : ℝ) * θ i)
  let f : Fin d → ℕ → ℝ := fun i j =>
    (-r) ^ (j + 1) * Real.cos (((j + 1 : ℕ) : ℝ) * θ i)
  let g : Fin d → ℕ → ℝ := fun i j =>
    (-r) ^ (j + 1) * (w i * Real.cos (((j + 1 : ℕ) : ℝ) * θ i))
  let G : ℕ → ℝ := fun j => ∑ i : Fin d, g i j
  let F : ℕ → ℝ := fun j => (-r) ^ (j + 1) *
    (a (((j + 1 : ℕ) : ℤ) - (n : ℤ)) + a (((j + 1 : ℕ) : ℤ) + (n : ℤ)))
  change Summable F ∧ Integrable Q μ ∧
    (∫ x : EuclideanSpace ℝ (Fin d), Q x ∂μ) =
      ((d : ℝ) / Real.sqrt κ) * ∑' j : ℕ, F j
  have hactual :
      Integrable (fun x : EuclideanSpace ℝ (Fin d) => ‖x‖ ^ 2) μ ∧
      Integrable Q μ ∧
      (∫ x : EuclideanSpace ℝ (Fin d), ‖x‖ ^ 2 ∂μ) = (∑ i : Fin d, (eigenvalue i)⁻¹) ∧
      (∫ x : EuclideanSpace ℝ (Fin d), Q x ∂μ) =
        ∑ i : Fin d, w i / eigenvalue i :=
    actual_diagonal_gaussian_quadratic_means hd hκ n hn hnd
  have hsqrt : 0 < Real.sqrt κ := Real.sqrt_pos.2 (by linarith)
  have heigenlower (i : Fin d) : 1 ≤ eigenvalue i := by
    dsimp [eigenvalue]
    have h := mul_nonneg (by linarith : 0 ≤ κ - 1)
      (by linarith [Real.neg_one_le_cos (θ i)] : 0 ≤ 1 + Real.cos (θ i))
    nlinarith
  have hcos (k : ℤ) : (∑ i : Fin d, Real.cos ((k : ℝ) * θ i)) = (d : ℝ) * a k :=
    actual_midpoint_grid_cosine_alias hd k
  have hnnon : ¬ (2 * (d : ℤ)) ∣ (n : ℤ) := by
    intro h
    have hle := Int.le_of_dvd (by omega : (0 : ℤ) < n) h
    omega
  have hzero : (∑ i : Fin d, w i) = 0 := by
    simpa [w, a, hnnon] using hcos (n : ℤ)
  obtain ⟨heq, habs, _⟩ := actual_inverse_spectrum_cosine_expansion hκ
  have hs (i : Fin d) : Summable (f i) := (habs (θ i)).of_norm
  have hmajor (i : Fin d) (j : ℕ) : ‖g i j‖ ≤ ‖f i j‖ := by
    have hw : ‖w i‖ ≤ 1 := by
      simpa only [w, Real.norm_eq_abs] using Real.abs_cos_le_one ((n : ℝ) * θ i)
    calc
      ‖g i j‖ = ‖w i‖ * ‖f i j‖ := by
        rw [← norm_mul]
        congr 1
        dsimp [g, f]
        ring
      _ ≤ 1 * ‖f i j‖ := mul_le_mul_of_nonneg_right hw (norm_nonneg _)
      _ = _ := one_mul _
  have hsgnorm (i : Fin d) : Summable (fun j : ℕ => ‖g i j‖) :=
    Summable.of_nonneg_of_le (fun j => norm_nonneg _) (hmajor i) (habs (θ i))
  have hsg (i : Fin d) : Summable (g i) := (hsgnorm i).of_norm
  have hsumG : Summable G := summable_sum (fun i _ => hsg i)
  have hprod (j : ℕ) :
      2 * (∑ i : Fin d, w i * Real.cos (((j + 1 : ℕ) : ℝ) * θ i)) =
      (d : ℝ) * (a (((j + 1 : ℕ) : ℤ) - (n : ℤ)) +
        a (((j + 1 : ℕ) : ℤ) + (n : ℤ))) := by
    have hp (i : Fin d) :
        2 * (w i * Real.cos (((j + 1 : ℕ) : ℝ) * θ i)) =
        Real.cos (((((j + 1 : ℕ) : ℤ) - (n : ℤ) : ℤ) : ℝ) * θ i) +
          Real.cos (((((j + 1 : ℕ) : ℤ) + (n : ℤ) : ℤ) : ℝ) * θ i) := by
      dsimp [w]
      push_cast
      simp only [sub_mul, add_mul, one_mul]
      have h := Real.two_mul_cos_mul_cos (((j : ℝ) + 1) * θ i) ((n : ℝ) * θ i)
      simp only [add_mul, one_mul] at h
      nlinarith [h]
    calc
      _ = ∑ i : Fin d,
          (Real.cos (((((j + 1 : ℕ) : ℤ) - (n : ℤ) : ℤ) : ℝ) * θ i) +
            Real.cos (((((j + 1 : ℕ) : ℤ) + (n : ℤ) : ℤ) : ℝ) * θ i)) := by
        rw [Finset.mul_sum]
        exact Finset.sum_congr rfl (fun i _ => hp i)
      _ = _ := by rw [Finset.sum_add_distrib, hcos, hcos]; ring
  have hterm (j : ℕ) : 2 * G j = (d : ℝ) * F j := by
    dsimp [G, g, F]
    rw [← Finset.mul_sum]
    calc
      _ = (-r) ^ (j + 1) *
          (2 * ∑ i : Fin d, w i * Real.cos (((j + 1 : ℕ) : ℝ) * θ i)) := by ring
      _ = _ := by rw [hprod]; push_cast; ring
  have hrnonneg : 0 ≤ r := by
    dsimp [r]
    apply div_nonneg _ (by linarith : 0 ≤ Real.sqrt κ + 1)
    nlinarith [Real.sq_sqrt (by linarith : 0 ≤ κ)]
  have ha_bound (k : ℤ) : ‖a k‖ ≤ 1 := by
    dsimp [a]
    split_ifs <;> simp
  have hpownorm (j : ℕ) : ‖(-r) ^ (j + 1)‖ = r ^ (j + 1) := by
    rw [norm_pow, norm_neg, Real.norm_eq_abs, abs_of_nonneg hrnonneg]
  have hFmajor (j : ℕ) : ‖F j‖ ≤ 2 * r ^ (j + 1) := by
    calc
      ‖F j‖ = r ^ (j + 1) *
          ‖a (((j + 1 : ℕ) : ℤ) - (n : ℤ)) + a (((j + 1 : ℕ) : ℤ) + (n : ℤ))‖ := by
        change ‖(-r) ^ (j + 1) *
          (a (((j + 1 : ℕ) : ℤ) - (n : ℤ)) + a (((j + 1 : ℕ) : ℤ) + (n : ℤ)))‖ = _
        rw [norm_mul, hpownorm]
      _ ≤ r ^ (j + 1) * (1 + 1) :=
        mul_le_mul_of_nonneg_left
          ((norm_add_le _ _).trans (add_le_add (ha_bound _) (ha_bound _)))
          (pow_nonneg hrnonneg _)
      _ = 2 * r ^ (j + 1) := by ring
  have hbase : Summable (fun j : ℕ => r ^ (j + 1)) := by
    have h0 := habs 0
    change Summable (fun j : ℕ => ‖(-r) ^ (j + 1) *
      Real.cos (((j + 1 : ℕ) : ℝ) * 0)‖) at h0
    simpa only [mul_zero, Real.cos_zero, mul_one, hpownorm] using h0
  have hFnorm : Summable (fun j : ℕ => ‖F j‖) :=
    Summable.of_nonneg_of_le (fun j => norm_nonneg _) hFmajor (hbase.mul_left 2)
  have hF : Summable F := hFnorm.of_norm
  have hseries : 2 * (∑' j : ℕ, G j) = (d : ℝ) * ∑' j : ℕ, F j := by
    rw [← hsumG.tsum_mul_left 2, ← hF.tsum_mul_left (d : ℝ)]
    exact tsum_congr hterm
  refine ⟨hF, hactual.2.1, hactual.2.2.2.trans ?_⟩
  have hlin (i : Fin d) : (∑' j : ℕ, g i j) = w i * (∑' j : ℕ, f i j) := by
    calc
      _ = ∑' j : ℕ, w i * f i j := tsum_congr (fun j => by dsimp [g, f]; ring)
      _ = _ := (hs i).tsum_mul_left (w i)
  have heigen (i : Fin d) : (eigenvalue i)⁻¹ =
      (1 / Real.sqrt κ) * (1 + 2 * ∑' j : ℕ, f i j) := by
    have htwice : 2 * eigenvalue i = κ + 1 + (κ - 1) * Real.cos (θ i) := by
      dsimp [eigenvalue]
      ring
    have hrecip : (eigenvalue i)⁻¹ = 2 / (κ + 1 + (κ - 1) * Real.cos (θ i)) := by
      have hi0 : eigenvalue i ≠ 0 := ne_of_gt (lt_of_lt_of_le (by norm_num) (heigenlower i))
      rw [← htwice]
      field_simp [hi0]
    exact hrecip.trans (heq (θ i))
  have hscalar (i : Fin d) : w i / eigenvalue i =
      (1 / Real.sqrt κ) * (w i + 2 * ∑' j : ℕ, g i j) := by
    rw [div_eq_mul_inv, heigen, hlin]
    ring
  have hexchange : (∑' j : ℕ, G j) = ∑ i : Fin d, ∑' j : ℕ, g i j :=
    Summable.tsum_finsetSum (fun i _ => hsg i)
  calc
    _ = ∑ i : Fin d, (1 / Real.sqrt κ) * (w i + 2 * ∑' j : ℕ, g i j) :=
      Finset.sum_congr rfl (fun i _ => hscalar i)
    _ = (1 / Real.sqrt κ) * ((∑ i : Fin d, w i) +
        2 * (∑ i : Fin d, ∑' j : ℕ, g i j)) := by
      rw [← Finset.mul_sum, Finset.sum_add_distrib, ← Finset.mul_sum]
    _ = (1 / Real.sqrt κ) * ((∑ i : Fin d, w i) + 2 * (∑' j : ℕ, G j)) := by
      rw [hexchange]
    _ = _ := by
      rw [hzero, zero_add, hseries]
      field_simp [ne_of_gt hsqrt]
