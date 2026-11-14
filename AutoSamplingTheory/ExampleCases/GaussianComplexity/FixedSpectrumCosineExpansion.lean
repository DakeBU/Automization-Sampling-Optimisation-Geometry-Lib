import Mathlib.Analysis.Complex.Trigonometric
import Mathlib.Analysis.Complex.Basic
import Mathlib.Analysis.SpecificLimits.Normed
import Mathlib.Analysis.Normed.Group.FunctionSeries
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

open scoped BigOperators
open Filter

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCosineExpansion

private theorem radius_bounds {κ : ℝ} (hκ : 2 ≤ κ) :
    1 < Real.sqrt κ ∧
    0 < (Real.sqrt κ - 1) / (Real.sqrt κ + 1) ∧
    (Real.sqrt κ - 1) / (Real.sqrt κ + 1) < 1 := by
  have hsq : (Real.sqrt κ) ^ 2 = κ := Real.sq_sqrt (by linarith)
  have hs : 1 < Real.sqrt κ := by nlinarith [Real.sqrt_nonneg κ]
  have hp : 0 < Real.sqrt κ + 1 := by linarith
  exact ⟨hs, div_pos (by linarith) hp, (div_lt_one hp).2 (by linarith)⟩

private theorem cosine_series_value {r : ℝ} (hr0 : 0 ≤ r) (hr1 : r < 1) (θ : ℝ) :
    1 + 2 * (∑' j : ℕ, (-r) ^ (j + 1) * Real.cos (((j + 1 : ℕ) : ℝ) * θ)) =
      (1 - r ^ 2) / (1 + 2 * r * Real.cos θ + r ^ 2) := by
  let z : ℂ := (-r : ℂ) * Complex.exp ((θ : ℂ) * Complex.I)
  have hz : ‖z‖ < 1 := by
    simpa [z, norm_mul, Real.norm_eq_abs, abs_of_nonneg hr0] using hr1
  have hterm (j : ℕ) : (z ^ j).re = (-r) ^ j * Real.cos ((j : ℝ) * θ) := by
    dsimp [z]
    have hp : (-r : ℂ) ^ j = (((-r) ^ j : ℝ) : ℂ) := by push_cast; rfl
    have he : Complex.exp ((θ : ℂ) * Complex.I) ^ j =
        Complex.exp ((((j : ℝ) * θ : ℝ) : ℂ) * Complex.I) := by
      rw [← Complex.exp_nat_mul]
      congr 1
      push_cast
      ring
    rw [mul_pow, hp, he]
    simp only [Complex.mul_re, Complex.ofReal_re, Complex.ofReal_im, zero_mul,
      sub_zero, Complex.exp_ofReal_mul_I_re]
  have hreal : HasSum (fun j : ℕ => (-r) ^ j * Real.cos ((j : ℝ) * θ))
      ((1 - z)⁻¹).re := by
    simpa only [hterm] using Complex.hasSum_re (hasSum_geometric_of_norm_lt_one hz)
  have hre : z.re = -r * Real.cos θ := by simp [z, Complex.mul_re]
  have him : z.im = -r * Real.sin θ := by simp [z, Complex.mul_im]
  have hnorm : Complex.normSq (1 - z) = 1 + 2 * r * Real.cos θ + r ^ 2 := by
    rw [Complex.normSq_apply]
    simp only [Complex.sub_re, Complex.one_re, Complex.sub_im, Complex.one_im, hre, him]
    have ht := congrArg (fun x : ℝ => r ^ 2 * x) (Real.sin_sq_add_cos_sq θ)
    nlinarith
  have hD : 0 < 1 + 2 * r * Real.cos θ + r ^ 2 := by
    have hm : 0 ≤ r * (1 + Real.cos θ) :=
      mul_nonneg hr0 (by linarith [Real.neg_one_le_cos θ])
    have hp : 0 < (1 - r) ^ 2 := sq_pos_of_pos (by linarith)
    nlinarith
  have hinv : ((1 - z)⁻¹).re =
      (1 + r * Real.cos θ) / (1 + 2 * r * Real.cos θ + r ^ 2) := by
    rw [Complex.inv_re, hnorm]
    simp [hre]
  have hsplit :
      1 + (∑' j : ℕ, (-r) ^ (j + 1) * Real.cos (((j + 1 : ℕ) : ℝ) * θ)) =
        (1 + r * Real.cos θ) / (1 + 2 * r * Real.cos θ + r ^ 2) := by
    rw [← hinv, ← hreal.tsum_eq]
    simpa using hreal.summable.tsum_eq_zero_add.symm
  apply (eq_div_iff (ne_of_gt hD)).2
  have hmul := (eq_div_iff (ne_of_gt hD)).1 hsplit
  calc
    _ = 2 * ((1 + (∑' j : ℕ, (-r) ^ (j + 1) *
        Real.cos (((j + 1 : ℕ) : ℝ) * θ))) *
        (1 + 2 * r * Real.cos θ + r ^ 2)) -
        (1 + 2 * r * Real.cos θ + r ^ 2) := by ring
    _ = 1 - r ^ 2 := by rw [hmul]; ring

theorem actual_inverse_spectrum_cosine_expansion {κ : ℝ} (hκ : 2 ≤ κ) :
  let r : ℝ := (Real.sqrt κ - 1) / (Real.sqrt κ + 1)
  (∀ θ : ℝ,
    2 / (κ + 1 + (κ - 1) * Real.cos θ) =
      (1 / Real.sqrt κ) *
        (1 + 2 * ∑' j : ℕ, (-r) ^ (j + 1) * Real.cos (((j + 1 : ℕ) : ℝ) * θ))) ∧
  (∀ θ : ℝ,
    Summable (fun j : ℕ => ‖(-r) ^ (j + 1) * Real.cos (((j + 1 : ℕ) : ℝ) * θ)‖)) ∧
  TendstoUniformly
    (fun N : ℕ => fun θ : ℝ =>
      ∑ j ∈ Finset.range N, (-r) ^ (j + 1) * Real.cos (((j + 1 : ℕ) : ℝ) * θ))
    (fun θ : ℝ => ∑' j : ℕ, (-r) ^ (j + 1) * Real.cos (((j + 1 : ℕ) : ℝ) * θ))
    atTop := by
  dsimp only
  set r : ℝ := (Real.sqrt κ - 1) / (Real.sqrt κ + 1) with hrdef
  obtain ⟨hs1, hr0, hr1⟩ := radius_bounds hκ
  change 0 < r at hr0
  change r < 1 at hr1
  have hgeom : Summable (fun j : ℕ => r ^ (j + 1)) :=
    (summable_nat_add_iff 1).2 (summable_geometric_of_lt_one hr0.le hr1)
  have hmajor (j : ℕ) (θ : ℝ) :
      ‖(-r) ^ (j + 1) * Real.cos (((j + 1 : ℕ) : ℝ) * θ)‖ ≤ r ^ (j + 1) := by
    have hc : |Real.cos (((j + 1 : ℕ) : ℝ) * θ)| ≤ 1 :=
      abs_le.mpr ⟨Real.neg_one_le_cos _, Real.cos_le_one _⟩
    simpa [norm_mul, norm_pow, Real.norm_eq_abs, abs_of_nonneg hr0.le] using
      mul_le_mul_of_nonneg_left hc (pow_nonneg hr0.le (j + 1))
  refine ⟨?_, ?_, tendstoUniformly_tsum_nat hgeom hmajor⟩
  · intro θ
    rw [cosine_series_value hr0.le hr1 θ]
    let s : ℝ := Real.sqrt κ
    have hs0 : s ≠ 0 := by dsimp [s]; linarith
    have hsden : s + 1 ≠ 0 := by dsimp [s]; linarith
    have hs2 : s ^ 2 = κ := Real.sq_sqrt (by linarith)
    have hrdef' : r = (s - 1) / (s + 1) := hrdef
    have hspec : 0 < κ + 1 + (κ - 1) * Real.cos θ := by
      have hm : 0 ≤ (κ - 1) * (1 + Real.cos θ) :=
        mul_nonneg (by linarith) (by linarith [Real.neg_one_le_cos θ])
      linarith
    have hparam : 1 + 2 * r * Real.cos θ + r ^ 2 =
        (1 - r) ^ 2 * (κ + 1 + (κ - 1) * Real.cos θ) / 2 := by
      rw [hrdef', ← hs2]
      field_simp [hsden]
      ring
    have hnorm : 1 - r ^ 2 = s * (1 - r) ^ 2 := by
      rw [hrdef']
      field_simp [hsden]
      ring
    have h1r : 1 - r ≠ 0 := by linarith
    change 2 / (κ + 1 + (κ - 1) * Real.cos θ) =
      (1 / s) * ((1 - r ^ 2) / (1 + 2 * r * Real.cos θ + r ^ 2))
    rw [hnorm, hparam]
    field_simp [hs0, hsden, ne_of_gt hspec, h1r]
  · intro θ
    exact hgeom.of_norm_bounded (fun j => by simpa only [norm_norm] using hmajor j θ)

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCosineExpansion
