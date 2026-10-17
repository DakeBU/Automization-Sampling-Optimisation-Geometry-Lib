import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

/-! Literal selected parameters and denominator matching of Zhou--Suzuki
arXiv:2610.20492v1 Eq22--23. Universal scalar identities do not assert
positivity for arbitrary u or a spherical distribution. Eq24 stays separate. -/
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.SelectedTilt
set_option autoImplicit false

theorem selected_tilt {n : ℕ} (hn : 3 ≤ n) {κ : ℝ} (hκ : 4 ≤ κ) :
    let r : ℝ := (1 - 1 / (n : ℝ)) * ((Real.sqrt κ - 1) / (Real.sqrt κ + 1))
    let ℓ : ℝ := (4 * (n : ℝ) * Real.sqrt κ + (Real.sqrt κ - 1) ^ 2) /
      (8 * (n : ℝ) * ((n : ℝ) - 1))
    0 < r ∧ r < 1 ∧ 0 < ℓ ∧
      ℓ = (κ - 1) / (8 * r) * (1 + r ^ 2) - (κ + 1) / 4 ∧
      (κ - 1) / (2 * r) = (n : ℝ) * (Real.sqrt κ + 1) ^ 2 /
        (2 * ((n : ℝ) - 1)) ∧
      (∀ u : ℝ,
        κ + 1 + 4 * ℓ - (κ - 1) * u =
          (κ - 1) / (2 * r) * (1 + r ^ 2 - 2 * r * u) ∧
        (κ - 1) / (2 * r) * (1 + r ^ 2 - 2 * r * u) =
          ((n : ℝ) * (Real.sqrt κ + 1) ^ 2 / (2 * ((n : ℝ) - 1))) *
            (1 + r ^ 2 - 2 * r * u)) := by
  let s := Real.sqrt κ
  have hs : (2 : ℝ) ≤ s := Real.le_sqrt_of_sq_le (by nlinarith)
  have hs0 : 0 < s := by linarith
  have hm : 0 < s - 1 := by linarith
  have hp : 0 < s + 1 := by linarith
  have hs2 : s ^ 2 = κ := Real.sq_sqrt (by linarith)
  have hn3 : (3 : ℝ) ≤ n := by exact_mod_cast hn
  have hn0 : (0 : ℝ) < n := by linarith
  have hn1 : (0 : ℝ) < (n : ℝ) - 1 := by linarith
  let r : ℝ := (1 - 1 / (n : ℝ)) * ((s - 1) / (s + 1))
  let ℓ : ℝ := (4 * (n : ℝ) * s + (s - 1) ^ 2) /
    (8 * (n : ℝ) * ((n : ℝ) - 1))
  change 0 < r ∧ r < 1 ∧ 0 < ℓ ∧ _
  have hfactor : 0 < (1 : ℝ) - 1 / (n : ℝ) := by
    have hdiv : (1 : ℝ) / n < 1 := (div_lt_one hn0).2 (by linarith)
    linarith
  have hfactor1 : (1 : ℝ) - 1 / (n : ℝ) < 1 := by
    have : (0 : ℝ) < 1 / (n : ℝ) := one_div_pos.mpr hn0
    linarith
  have hratio : 0 < (s - 1) / (s + 1) := div_pos hm hp
  have hratio1 : (s - 1) / (s + 1) < 1 := (div_lt_one hp).2 (by linarith)
  have hr : 0 < r := mul_pos hfactor hratio
  have hr1 : r < 1 := by
    dsimp [r]
    nlinarith
  have hℓ : 0 < ℓ := by dsimp [ℓ]; positivity
  have hreq : r = ((n : ℝ) - 1) * (s - 1) / ((n : ℝ) * (s + 1)) := by
    dsimp [r]
    field_simp
  have hcoeff : (κ - 1) / (2 * r) =
      (n : ℝ) * (s + 1) ^ 2 / (2 * ((n : ℝ) - 1)) := by
    rw [← hs2, hreq]
    field_simp
    ring
  have hell : ℓ = (κ - 1) / (8 * r) * (1 + r ^ 2) - (κ + 1) / 4 := by
    rw [← hs2, hreq]
    dsimp [ℓ]
    field_simp
    ring
  refine ⟨hr, hr1, hℓ, hell, hcoeff, ?_⟩
  intro u
  change κ + 1 + 4 * ℓ - (κ - 1) * u =
      (κ - 1) / (2 * r) * (1 + r ^ 2 - 2 * r * u) ∧
    (κ - 1) / (2 * r) * (1 + r ^ 2 - 2 * r * u) =
      ((n : ℝ) * (s + 1) ^ 2 / (2 * ((n : ℝ) - 1))) *
        (1 + r ^ 2 - 2 * r * u)
  constructor
  · rw [hell]
    field_simp
    ring
  · rw [hcoeff]

end AutoSamplingTheory.ExampleCases.GaussianComplexity.SelectedTilt
