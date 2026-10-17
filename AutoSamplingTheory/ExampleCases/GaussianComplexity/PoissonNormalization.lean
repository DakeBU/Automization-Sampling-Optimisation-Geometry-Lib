import AutoSamplingTheory.ExampleCases.GaussianComplexity.SelectedTilt
import AutoSamplingTheory.ExampleCases.GaussianComplexity.GaussianExpectation

open Matrix MeasureTheory
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
open AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily
/-!
The source-implicit real-power normalization between Eq23 and Eq24 in
Zhou--Suzuki arXiv:2610.20492v1. The actual full-Haar kernel is absolutely L1.
Sphere pushforward and the two Poisson integrals remain separate obligations.
-/
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.PoissonNormalization
set_option autoImplicit false
theorem selected_gaussian_normalization {n : ℕ} (hn : 3 ≤ n) {κ : ℝ}
    (hκ : 4 ≤ κ) :
    let s : ℝ := Real.sqrt κ
    let r : ℝ := (1 - 1 / (n : ℝ)) * ((s - 1) / (s + 1))
    let ℓ : ℝ := (4 * (n : ℝ) * s + (s - 1) ^ 2) /
      (8 * (n : ℝ) * ((n : ℝ) - 1))
    let j0 : Fin n := ⟨0, lt_of_lt_of_le (by decide : 0 < 3) hn⟩
    let U : Matrix.orthogonalGroup (Fin n) ℝ → ℝ :=
      fun O => (O : Matrix (Fin n) (Fin n) ℝ) j0 j0
    let q : Matrix.orthogonalGroup (Fin n) ℝ → ℝ := fun O =>
      ((s + 1) * U O - (s - 1)) /
        (1 + r ^ 2 - 2 * r * U O) ^ ((n : ℝ) / 2)
    let γ : Matrix.orthogonalGroup (Fin n) ℝ → Measure (EuclideanSpace ℝ (Fin n)) :=
      fun O => ProbabilityTheory.multivariateGaussian (0 : EuclideanSpace ℝ (Fin n))
        (singleBlockPrecision κ O)⁻¹
    Integrable q (orthogonalHaar n) ∧
      (∫ O : Matrix.orthogonalGroup (Fin n) ℝ,
        (O : Matrix (Fin n) (Fin n) ℝ).det *
          (∫ x : EuclideanSpace ℝ (Fin n), Real.exp (-ℓ * ‖x‖ ^ 2) ∂γ O)
        ∂orthogonalHaar n) =
        (((-1 : ℝ) ^ (n - 1) * (s - 1) ^ (n - 1)) / (s + 1) ^ n) *
          (1 - 1 / (n : ℝ)) ^ ((n : ℝ) / 2) * (∫ O, q O ∂orthogonalHaar n) := by
  classical
  let s : ℝ := Real.sqrt κ
  let r : ℝ := (1 - 1 / (n : ℝ)) * ((s - 1) / (s + 1))
  let ℓ : ℝ := (4 * (n : ℝ) * s + (s - 1) ^ 2) /
    (8 * (n : ℝ) * ((n : ℝ) - 1))
  let j0 : Fin n := ⟨0, lt_of_lt_of_le (by decide : 0 < 3) hn⟩
  let U : Matrix.orthogonalGroup (Fin n) ℝ → ℝ :=
    fun O => (O : Matrix (Fin n) (Fin n) ℝ) j0 j0
  let q : Matrix.orthogonalGroup (Fin n) ℝ → ℝ := fun O =>
    ((s + 1) * U O - (s - 1)) /
      (1 + r ^ 2 - 2 * r * U O) ^ ((n : ℝ) / 2)
  let γ : Matrix.orthogonalGroup (Fin n) ℝ → Measure (EuclideanSpace ℝ (Fin n)) :=
    fun O => ProbabilityTheory.multivariateGaussian (0 : EuclideanSpace ℝ (Fin n))
      (singleBlockPrecision κ O)⁻¹
  change Integrable q (orthogonalHaar n) ∧ _
  have hsel := SelectedTilt.selected_tilt hn hκ
  change 0 < r ∧ r < 1 ∧ 0 < ℓ ∧ _ at hsel
  obtain ⟨hr, hr1, hℓ, _hell, _hcoeff, hmatch⟩ := hsel
  have hn3 : (3 : ℝ) ≤ n := by exact_mod_cast hn
  have hn0 : (0 : ℝ) < n := by linarith
  have hn1 : (0 : ℝ) < (n : ℝ) - 1 := by linarith
  have hs : 0 ≤ s := Real.sqrt_nonneg κ
  have hp : 0 < s + 1 := by linarith
  let a : ℝ := 1 - 1 / (n : ℝ)
  let p : ℝ := (n : ℝ) / 2
  let C : ℝ := (n : ℝ) * (s + 1) ^ 2 / (2 * ((n : ℝ) - 1))
  let b : Matrix.orthogonalGroup (Fin n) ℝ → ℝ := fun O =>
    1 + r ^ 2 - 2 * r * U O
  have ha : 0 < a := by
    have hdiv : (1 : ℝ) / n < 1 := (div_lt_one hn0).2 (by linarith)
    dsimp [a]
    linarith
  have hC : 0 < C := by dsimp [C]; positivity
  have htwoC : 2 * C = (s + 1) ^ 2 / a := by
    dsimp [C, a]
    field_simp [hn0.ne', hn1.ne']
  have hbpos (O : Matrix.orthogonalGroup (Fin n) ℝ) : 0 < b O := by
    have huabs : |U O| ≤ 1 := by
      simpa only [U, Real.norm_eq_abs] using
        entry_norm_bound_of_unitary O.property j0 j0
    have hu : U O ≤ 1 := (abs_le.mp huabs).2
    have hsq : 0 < (1 - r) ^ 2 := sq_pos_of_pos (sub_pos.mpr hr1)
    have hprod : 0 ≤ r * (1 - U O) := mul_nonneg hr.le (sub_nonneg.mpr hu)
    dsimp [b]
    nlinarith
  have hU : Continuous U := continuous_subtype_val.matrix_elem j0 j0
  have hbcont : Continuous b := by dsimp [b]; fun_prop
  have hqcont : Continuous q := by
    change Continuous (fun O => ((s + 1) * U O - (s - 1)) / (b O) ^ p)
    exact ((continuous_const.mul hU).sub continuous_const).div
      (hbcont.rpow_const (fun O => Or.inl (hbpos O).ne'))
      (fun O => (Real.rpow_pos_of_pos (hbpos O) p).ne')
  let := (orthogonalHaar_spec n).1
  have hqL : Integrable q (orthogonalHaar n) :=
    hqcont.integrable_of_hasCompactSupport (isClosed_tsupport q).isCompact
  have hpow2 : ((s + 1) ^ 2) ^ p = (s + 1) ^ n := by
    calc
      ((s + 1) ^ 2) ^ p = (s + 1) ^ ((2 : ℝ) * p) :=
        (Real.rpow_natCast_mul hp.le 2 p).symm
      _ = (s + 1) ^ (n : ℝ) := by congr 1; dsimp [p]; ring
      _ = (s + 1) ^ n := Real.rpow_natCast _ _
  have hscale : (2 : ℝ) ^ p * C ^ p = (s + 1) ^ n / a ^ p := by
    rw [← Real.mul_rpow (by norm_num : (0 : ℝ) ≤ 2) hC.le, htwoC,
      Real.div_rpow (sq_nonneg _) ha.le, hpow2]
  have hpref :
      (((-1 : ℝ) ^ (n - 1) * (s - 1) ^ (n - 1)) / (2 : ℝ) ^ p) * (C ^ p)⁻¹ =
        (((-1 : ℝ) ^ (n - 1) * (s - 1) ^ (n - 1)) / (s + 1) ^ n) * a ^ p := by
    calc
      _ = ((-1 : ℝ) ^ (n - 1) * (s - 1) ^ (n - 1)) /
          ((2 : ℝ) ^ p * C ^ p) := by
        simp only [div_eq_mul_inv, _root_.mul_inv_rev]
        ring
      _ = ((-1 : ℝ) ^ (n - 1) * (s - 1) ^ (n - 1)) /
          ((s + 1) ^ n / a ^ p) := by rw [hscale]
      _ = _ := by
        field_simp [(Real.rpow_pos_of_pos ha p).ne', pow_ne_zero n hp.ne']
  have hden (O : Matrix.orthogonalGroup (Fin n) ℝ) :
      κ + 1 + 4 * ℓ - (κ - 1) * U O = C * b O :=
    (hmatch (U O)).1.trans (hmatch (U O)).2
  have hg := GaussianExpectation.actual_gaussian_transform hn hκ hℓ.le
  refine ⟨hqL, ?_⟩
  calc
    _ = (((-1 : ℝ) ^ (n - 1) * (s - 1) ^ (n - 1)) / (2 : ℝ) ^ p) *
        (∫ O : Matrix.orthogonalGroup (Fin n) ℝ,
          ((s + 1) * U O - (s - 1)) /
            (κ + 1 + 4 * ℓ - (κ - 1) * U O) ^ p ∂orthogonalHaar n) := hg.2.2
    _ = (((-1 : ℝ) ^ (n - 1) * (s - 1) ^ (n - 1)) / (2 : ℝ) ^ p) *
        ((C ^ p)⁻¹ * (∫ O, q O ∂orthogonalHaar n)) := by
      congr 1
      rw [← integral_const_mul]
      apply integral_congr_ae
      exact Filter.Eventually.of_forall fun O => by
        change ((s + 1) * U O - (s - 1)) /
          (κ + 1 + 4 * ℓ - (κ - 1) * U O) ^ p = (C ^ p)⁻¹ * q O
        rw [hden O, Real.mul_rpow hC.le (hbpos O).le]
        change ((s + 1) * U O - (s - 1)) / (C ^ p * (b O) ^ p) =
          (C ^ p)⁻¹ * (((s + 1) * U O - (s - 1)) / (b O) ^ p)
        simp only [div_eq_mul_inv, _root_.mul_inv_rev]
        ring
    _ = _ := by rw [← mul_assoc, hpref]

end AutoSamplingTheory.ExampleCases.GaussianComplexity.PoissonNormalization
