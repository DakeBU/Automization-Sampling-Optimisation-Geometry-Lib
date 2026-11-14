import Mathlib.Analysis.SpecialFunctions.Pow.Asymptotics
import Mathlib.Tactic

/-!
# Uniform source-query mode and spectral gap

Zhou--Suzuki arXiv:2610.20492v1, Section4.3: Px1.p1.1--p1.2
and Px2.p2.1. One natural threshold works uniformly over the original
condition-number and integer query-cap ranges. The canonical logarithmic
little-o estimate supplies the threshold; all dimension/mode/gap facts
are conclusions. This is a numerical prerequisite, not an oracle theorem.
-/
open Filter Asymptotics
noncomputable section

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumModeGap

theorem eventual_source_query_mode_gap {δ : ℝ} (hδ0 : 0 < δ) (hδ1 : δ < 1) :
  ∃ d₀ : ℕ, ∀ (d : ℕ), d₀ ≤ d → ∀ (κ : ℝ), 2 ≤ κ →
    κ ≤ (d : ℝ) ^ (1 - δ) → ∀ (q : ℕ),
    (q : ℝ) ≤ (δ / 256) * Real.sqrt κ * Real.log (d : ℝ) →
    let n : ℕ := 2 * q + 1
    2 ≤ d ∧ 1 ≤ n ∧ n < d ∧ Real.sqrt κ ≤ (d : ℝ) - (n : ℝ) := by

  have hlo : (fun d : ℕ => Real.log (d : ℝ)) =o[Filter.atTop]
      (fun d : ℕ => (d : ℝ) ^ (1 / 2 : ℝ)) :=
    (isLittleO_log_rpow_atTop (by norm_num : (0 : ℝ) < 1 / 2)).comp_tendsto
      tendsto_natCast_atTop_atTop
  have hlogevent : ∀ᶠ d : ℕ in Filter.atTop, Real.log (d : ℝ) ≤ Real.sqrt (d : ℝ) := by
    filter_upwards [hlo.def (by norm_num : (0 : ℝ) < 1)] with d hd
    have hd' : |Real.log (d : ℝ)| ≤ (d : ℝ) ^ (1 / 2 : ℝ) := by
      simpa only [Real.norm_eq_abs, one_mul,
        abs_of_nonneg (Real.rpow_nonneg (Nat.cast_nonneg d) _)] using hd
    exact (le_abs_self _).trans (hd'.trans_eq (Real.sqrt_eq_rpow _).symm)
  rcases Filter.eventually_atTop.1 hlogevent with ⟨D, hD⟩
  refine ⟨max D 4, ?_⟩
  intro d hd κ hκ hκcap q hq
  change 2 ≤ d ∧ 1 ≤ 2 * q + 1 ∧ 2 * q + 1 < d ∧
    Real.sqrt κ ≤ (d : ℝ) - ((2 * q + 1 : ℕ) : ℝ)
  have hd4nat : 4 ≤ d := (le_max_right D 4).trans hd
  have hd4 : (4 : ℝ) ≤ (d : ℝ) := by exact_mod_cast hd4nat
  have hd0 : (0 : ℝ) ≤ (d : ℝ) := Nat.cast_nonneg d
  have hd1 : (1 : ℝ) ≤ (d : ℝ) := by linarith
  have hlog : Real.log (d : ℝ) ≤ Real.sqrt (d : ℝ) :=
    hD d ((le_max_left D 4).trans hd)
  have hlog0 : 0 ≤ Real.log (d : ℝ) := Real.log_nonneg hd1
  have hκd : κ ≤ (d : ℝ) := hκcap.trans (by
    simpa only [Real.rpow_one] using
      Real.rpow_le_rpow_of_exponent_le hd1 (by linarith : 1 - δ ≤ (1 : ℝ)))
  have hsκ : Real.sqrt κ ≤ Real.sqrt (d : ℝ) := Real.sqrt_le_sqrt hκd
  have hδscale : δ / 256 ≤ (1 / 256 : ℝ) := by linarith
  have hcoeff : (δ / 256) * Real.sqrt κ ≤ (1 / 256 : ℝ) * Real.sqrt (d : ℝ) :=
    (mul_le_mul_of_nonneg_right hδscale (Real.sqrt_nonneg κ)).trans
      (mul_le_mul_of_nonneg_left hsκ (by norm_num))
  have hq' : (q : ℝ) ≤ (1 / 256 : ℝ) * Real.sqrt (d : ℝ) * Real.log (d : ℝ) :=
    hq.trans (mul_le_mul_of_nonneg_right hcoeff hlog0)
  have hqsmall : (q : ℝ) ≤ (d : ℝ) / 256 := by
    calc
      _ ≤ (1 / 256 : ℝ) * Real.sqrt (d : ℝ) * Real.log (d : ℝ) := hq'
      _ ≤ (1 / 256 : ℝ) * Real.sqrt (d : ℝ) * Real.sqrt (d : ℝ) :=
        mul_le_mul_of_nonneg_left hlog (by positivity)
      _ = _ := by nlinarith [Real.sq_sqrt hd0]
  have hs2 : (2 : ℝ) ≤ Real.sqrt (d : ℝ) := by
    nlinarith [Real.sq_sqrt hd0, Real.sqrt_nonneg (d : ℝ)]
  have hsD : Real.sqrt (d : ℝ) ≤ (d : ℝ) / 2 := by
    nlinarith [Real.sq_sqrt hd0,
      mul_nonneg (Real.sqrt_nonneg (d : ℝ)) (sub_nonneg.mpr hs2)]
  have hncast : ((2 * q + 1 : ℕ) : ℝ) = 2 * (q : ℝ) + 1 := by norm_num
  have hgap : Real.sqrt κ ≤ (d : ℝ) - ((2 * q + 1 : ℕ) : ℝ) := by
    rw [hncast]
    linarith
  have hsκpos : 0 < Real.sqrt κ := Real.sqrt_pos.2 (by linarith)
  have hndreal : ((2 * q + 1 : ℕ) : ℝ) < (d : ℝ) := by linarith
  have hnd : 2 * q + 1 < d := by exact_mod_cast hndreal
  exact ⟨by omega, by omega, hnd, hgap⟩

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumModeGap
