import GC41Power
import GC41Reversal

/-! At the lower condition-number endpoint, one strict test decides between
two orientations with conditional error at most 1/10 under either target.
Any fixed nonnegative query index is available once the dimension is large. -/

open MeasureTheory ProbabilityTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumTargetEvent (queryThreshold)
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumRotation

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumWitness

theorem eventually_one_test_classifies (C : ℝ) (hC : 0 < C) (q : ℕ) :
    ∃ d₀ : ℕ, ∀ d ≥ d₀,
      let A := hiddenPrecision 2 (1 : Matrix.orthogonalGroup (Fin d) ℝ)
      let B := hiddenPrecision 2 (reversal d)
      let U := detectorEvent 2 (2*q+1) (queryThreshold C d q) A
      let P := multivariateGaussian (0 : EuclideanSpace ℝ (Fin d)) A⁻¹
      let Q := multivariateGaussian (0 : EuclideanSpace ℝ (Fin d)) B⁻¹
      P.real Uᶜ ≤ (1/10 : ℝ) ∧ Q.real U ≤ 1/10 := by
  obtain ⟨D, hD⟩ := eventual_rotated_target_power C hC (δ := 1/2) (by norm_num) (by norm_num)
  obtain ⟨N, hN⟩ := exists_nat_ge (Real.exp (512*(q:ℝ)))
  refine ⟨max 4 (max D N), ?_⟩
  intro d hd
  have hd4 : 4 ≤ d := (le_max_left ..).trans hd
  have hd2 : 2 ≤ d := by omega
  have hdD : D ≤ d := (le_max_left ..).trans ((le_max_right ..).trans hd)
  have hdN : N ≤ d := (le_max_right ..).trans ((le_max_right ..).trans hd)
  have hpos : 0 < (d : ℝ) := by exact_mod_cast (show 0 < d by omega)
  have hdim : (2 : ℝ) ≤ (d : ℝ)^(1-(1/2 : ℝ)) := by
    rw [show 1 - (1/2 : ℝ) = 1/2 by norm_num, ← Real.sqrt_eq_rpow]
    apply Real.le_sqrt_of_sq_le
    norm_num
    exact_mod_cast hd4
  have hlog : 512*(q:ℝ) ≤ Real.log (d : ℝ) :=
    (Real.le_log_iff_exp_le hpos).mpr (hN.trans (by exact_mod_cast hdN))
  have hnonneg : 0 ≤ Real.log (d : ℝ) := by linarith [Nat.cast_nonneg (α := ℝ) q]
  have hq : (q : ℝ) ≤ (1/2)/256 * Real.sqrt 2 * Real.log (d : ℝ) := by
    have hs : 1 ≤ Real.sqrt 2 := Real.le_sqrt_of_sq_le (by norm_num)
    nlinarith [mul_nonneg (sub_nonneg.mpr hs) hnonneg]
  let A := hiddenPrecision 2 (1 : Matrix.orthogonalGroup (Fin d) ℝ)
  let B := hiddenPrecision 2 (reversal d)
  let U := detectorEvent 2 (2*q+1) (queryThreshold C d q) A
  let V := detectorEvent 2 (2*q+1) (queryThreshold C d q) B
  let P := multivariateGaussian (0 : EuclideanSpace ℝ (Fin d)) A⁻¹
  let Q := multivariateGaussian (0 : EuclideanSpace ℝ (Fin d)) B⁻¹
  have hp : 9/10 ≤ P.real U := hD d hdD 2 le_rfl hdim q hq 1
  have hq' : 9/10 ≤ Q.real V := hD d hdD 2 le_rfl hdim q hq (reversal d)
  have hτ : 0 ≤ queryThreshold C d q := by unfold queryThreshold; positivity
  have hdis : Disjoint U V :=
    disjoint_reversed_odd_detector_events hd2 le_rfl ⟨q,rfl⟩ hτ
  have hsum : Q.real U + Q.real V ≤ 1 := by
    rw [← measureReal_union hdis (measurableSet_detectorEvent _ _ _ _)]
    exact measureReal_le_one
  change P.real Uᶜ ≤ 1/10 ∧ Q.real U ≤ 1/10
  rw [probReal_compl_eq_one_sub (measurableSet_detectorEvent _ _ _ _)]
  constructor <;> linarith

#print axioms eventually_one_test_classifies

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumWitness
