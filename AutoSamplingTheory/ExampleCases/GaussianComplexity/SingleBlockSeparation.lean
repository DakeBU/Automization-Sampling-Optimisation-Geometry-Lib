import AutoSamplingTheory.ExampleCases.GaussianComplexity.ActualTotalVariation
import AutoSamplingTheory.ExampleCases.GaussianComplexity.EvaluatedGaussian
import AutoSamplingTheory.ExampleCases.GaussianComplexity.NumericSeparation
import Mathlib.Analysis.Convex.SpecificFunctions.Basic

/-!
# Actual single-block separation

Proposition B.7, Eq19 of Zhou--Suzuki, arXiv:2610.20492v1.
The source's actual determinant-conditioned Gaussian mixtures have normalized
event TV at least the explicit ratio, and hence the stated exponential.
Eq20, Eq24 and the scalar exponential comparison are reused canonical nodes.
The remaining Bernoulli and denominator estimates are discharged internally.
This single-block result does not assert amplification, transcript/oracle,
query-cap, precision, expected-cost, hidden-eigenbasis or main lower bounds.
-/

open Matrix MeasureTheory
open scoped ENNReal
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
open AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.SingleBlockSeparation
set_option autoImplicit false

theorem single_block_separation {n : ℕ} (hn : 3 ≤ n) {κ : ℝ} (hκ : 4 ≤ κ) :
    let s : ℝ := Real.sqrt κ
    let μ := orthogonalHaar n
    let νpos := (2 : ℝ≥0∞) • μ.restrict
      {O : Matrix.orthogonalGroup (Fin n) ℝ | (O : Matrix (Fin n) (Fin n) ℝ).det = 1}
    let νneg := (2 : ℝ≥0∞) • μ.restrict
      {O : Matrix.orthogonalGroup (Fin n) ℝ | (O : Matrix (Fin n) (Fin n) ℝ).det = -1}
    let γ : Matrix.orthogonalGroup (Fin n) ℝ → Measure (EuclideanSpace ℝ (Fin n)) :=
      fun O => ProbabilityTheory.multivariateGaussian (0 : EuclideanSpace ℝ (Fin n))
        (singleBlockPrecision κ O)⁻¹
    let Ppos := νpos.bind γ
    let Pneg := νneg.bind γ
    let δ : ℝ := sSup {z : ℝ | ∃ B : Set (EuclideanSpace ℝ (Fin n)),
      MeasurableSet B ∧ z = |Ppos.real B - Pneg.real B|}
    (1 / 2 : ℝ) * Real.exp (-(5 * (n : ℝ)) / s) ≤
      (((s - 1) / (s + 1)) ^ n) /
        (2 + 4 * (n : ℝ) * s / (s + 1) ^ 2) ∧
    (((s - 1) / (s + 1)) ^ n) /
        (2 + 4 * (n : ℝ) * s / (s + 1) ^ 2) ≤ δ := by
  dsimp only
  constructor
  · exact NumericSeparation.explicit_ratio_ge_exponential hn hκ
  · let s : ℝ := Real.sqrt κ
    let q : ℝ := (s - 1) / (s + 1)
    let a : ℝ := 1 - 1 / (n : ℝ)
    let r : ℝ := a * q
    let ℓ : ℝ := (4 * (n : ℝ) * s + (s - 1) ^ 2) /
      (8 * (n : ℝ) * ((n : ℝ) - 1))
    let v : ℝ := ((-1 : ℝ) ^ n / (n : ℝ)) * q ^ n *
      a ^ ((n : ℝ) / 2) / (1 - r ^ 2)
    have hn3 : (3 : ℝ) ≤ n := by exact_mod_cast hn
    have hn0 : (0 : ℝ) < n := by linarith
    have hs : (2 : ℝ) ≤ s := Real.le_sqrt_of_sq_le (by linarith)
    have hsp : 0 < s + 1 := by linarith
    have hq : 0 < q := div_pos (by linarith) hsp
    have hq1 : q < 1 := (div_lt_one hsp).2 (by linarith)
    have hqn : 0 ≤ q ^ n := (pow_pos hq n).le
    have hinv0 : 0 < 1 / (n : ℝ) := one_div_pos.mpr hn0
    have hinv1 : 1 / (n : ℝ) < 1 := (div_lt_one hn0).2 (by linarith)
    have ha : 0 < a := by dsimp [a]; linarith
    have hpow : 0 < a ^ ((n : ℝ) / 2) := Real.rpow_pos_of_pos ha _
    have ht := SelectedTilt.selected_tilt hn hκ
    have hr : 0 < r := ht.1
    have hr1 : r < 1 := ht.2.1
    have hden : 0 < 1 - r ^ 2 := by nlinarith
    have hprod : 0 < (n : ℝ) * (1 - r ^ 2) := mul_pos hn0 hden
    -- Bernoulli uses a real exponent, including odd dimensions.
    have hhalf : (1 / 2 : ℝ) ≤ a ^ ((n : ℝ) / 2) := by
      have hb := one_add_mul_self_le_rpow_one_add
        (s := -(1 / (n : ℝ))) (by linarith : -1 ≤ -(1 / (n : ℝ)))
        (p := (n : ℝ) / 2) (by linarith : 1 ≤ (n : ℝ) / 2)
      have hlin : (1 : ℝ) + (n : ℝ) / 2 * (-(1 / (n : ℝ))) = 1 / 2 := by
        field_simp
        ring
      rw [hlin] at hb
      simpa only [a, sub_eq_add_neg] using hb
    -- The literal denominator identity is the source's unnumbered display.
    have hdenid : (n : ℝ) * (1 - r ^ 2) =
        4 * (n : ℝ) * s / (s + 1) ^ 2 + q ^ 2 * (2 - 1 / (n : ℝ)) := by
      dsimp only [r, a, q]
      field_simp
      ring
    have hq2 : q ^ 2 ≤ 1 := by nlinarith
    have hterm : q ^ 2 * (2 - 1 / (n : ℝ)) ≤ 2 := by
      have hm : 0 ≤ 2 - 1 / (n : ℝ) := by linarith
      have hu := mul_le_mul_of_nonneg_right hq2 hm
      nlinarith
    have hdenle : (n : ℝ) * (1 - r ^ 2) ≤
        2 + 4 * (n : ℝ) * s / (s + 1) ^ 2 := by linarith [hdenid]
    have hD : 0 < 2 + 4 * (n : ℝ) * s / (s + 1) ^ 2 := by positivity
    -- Absolute value removes (-1)^n without a parity restriction.
    have hvabs : |v| = q ^ n * a ^ ((n : ℝ) / 2) /
        ((n : ℝ) * (1 - r ^ 2)) := by
      simp only [v, abs_div, abs_mul, abs_pow, abs_neg, abs_one, one_pow,
        abs_of_pos hn0, abs_of_nonneg hq.le, abs_of_pos hpow, abs_of_pos hden]
      field_simp
    have hratio : q ^ n / (2 + 4 * (n : ℝ) * s / (s + 1) ^ 2) ≤
        q ^ n / ((n : ℝ) * (1 - r ^ 2)) :=
      (div_le_div_iff₀ hD hprod).2 (mul_le_mul_of_nonneg_left hdenle hqn)
    have htest : q ^ n / ((n : ℝ) * (1 - r ^ 2)) ≤ 2 * |v| := by
      rw [hvabs]
      have hm := mul_le_mul_of_nonneg_left hhalf hqn
      have hnum : q ^ n ≤ 2 * (q ^ n * a ^ ((n : ℝ) / 2)) := by nlinarith
      calc
        _ ≤ (2 * (q ^ n * a ^ ((n : ℝ) / 2))) /
            ((n : ℝ) * (1 - r ^ 2)) := div_le_div_of_nonneg_right hnum hprod.le
        _ = _ := by ring
    have he := EvaluatedGaussian.selected_gaussian_value hn hκ
    have htv := ActualTotalVariation.actual_radial_test_tv hn hκ (ℓ := ℓ) ht.2.2.1.le
    dsimp only at he htv
    rw [he.2.2.2] at htv
    change 2 * |v| ≤ _ at htv
    exact hratio.trans (htest.trans htv)

end AutoSamplingTheory.ExampleCases.GaussianComplexity.SingleBlockSeparation
