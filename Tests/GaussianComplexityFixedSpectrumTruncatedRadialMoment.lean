import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumTruncatedRadialMoment

/-!
# The scalar bias of the retained Gaussian row moment

The exact norm-square mean and the complementary truncations identify the
bias. The proved strict tail moment supplies its quantitative bound.
-/

open MeasureTheory ProbabilityTheory

namespace AutoSamplingTheory.Tests.GaussianComplexityFixedSpectrumTruncatedRadialMoment

open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumTruncatedRadialMoment
open AutoSamplingTheory.TechnicalLemmas.Probability.StdGaussianMoment

/-- Apply the source tail first-moment estimate to the scalar in Appendix C.2. -/
private theorem actual_truncated_radial_bias
    {d q : ℕ} (hq : 2 * q + 1 < d) :
  let E := EuclideanSpace ℝ (Fin (q + 1))
  let μ : Measure E := stdGaussian E
  let r : ℝ := ((q + 1 : ℕ) : ℝ)
  let R : E → ℝ := fun x => ‖x‖ ^ 2
  let L : ℝ := 2 * r + 3 * Real.log (1000 * (d : ℝ))
  let a : ℝ := (∫ x, Set.indicator {y : E | R y ≤ L} R x ∂μ) / r
  0 ≤ a ∧ a ≤ 1 ∧
    1 - a = (∫ x, Set.indicator {y : E | L < R y} R x ∂μ) / r ∧
    1 - a ≤ (L + 3) / (1000 * r * (d : ℝ)) := by
  let E := EuclideanSpace ℝ (Fin (q + 1))
  let μ : Measure E := stdGaussian E
  let r : ℝ := (q + 1 : ℕ)
  let R : E → ℝ := fun x => ‖x‖ ^ 2
  let L : ℝ := 2 * r + 3 * Real.log (1000 * (d : ℝ))
  let good : Set E := {x | R x ≤ L}
  let bad : Set E := {x | L < R x}
  let goodMoment : E → ℝ := good.indicator R
  let badMoment : E → ℝ := bad.indicator R
  let a : ℝ := (∫ x, goodMoment x ∂μ) / r
  change 0 ≤ a ∧ a ≤ 1 ∧ 1 - a = (∫ x, badMoment x ∂μ) / r ∧
    1 - a ≤ (L + 3) / (1000 * r * (d : ℝ))
  have r_pos : 0 < r := by unfold r; positivity
  have radius_nonneg (x : E) : 0 ≤ R x := sq_nonneg _
  have radius_measurable : Measurable R := by unfold R; fun_prop
  obtain ⟨radius_integrable, radius_mean⟩ :=
    integrable_norm_sq_and_integral_stdGaussian (E := E)
  change Integrable R μ at radius_integrable
  rw [show Module.finrank ℝ E = q + 1 from finrank_euclideanSpace_fin] at radius_mean
  change (∫ x, R x ∂μ) = r at radius_mean
  have good_integrable : Integrable goodMoment μ :=
    radius_integrable.indicator (measurableSet_le radius_measurable measurable_const)
  have bad_integrable : Integrable badMoment μ :=
    radius_integrable.indicator (measurableSet_lt measurable_const radius_measurable)
  have good_nonneg (x : E) : 0 ≤ goodMoment x := by
    by_cases hx : R x ≤ L <;> simp [goodMoment, good, hx, radius_nonneg x]
  have good_le (x : E) : goodMoment x ≤ R x := by
    by_cases hx : R x ≤ L <;> simp [goodMoment, good, hx, radius_nonneg x]
  have good_integral_le : (∫ x, goodMoment x ∂μ) ≤ r := by
    rw [← radius_mean]
    exact integral_mono good_integrable radius_integrable good_le
  have split : (fun x => goodMoment x + badMoment x) = R := by
    funext x
    by_cases hx : R x ≤ L
    · simp [goodMoment, badMoment, good, bad, hx, not_lt_of_ge hx]
    · simp [goodMoment, badMoment, good, bad, hx, lt_of_not_ge hx]
  have moment_sum : (∫ x, goodMoment x ∂μ) + (∫ x, badMoment x ∂μ) = r := by
    rw [← integral_add good_integrable bad_integrable, split, radius_mean]
  have bias_identity : 1 - a = (∫ x, badMoment x ∂μ) / r := by
    unfold a
    rw [← div_self r_pos.ne', ← sub_div]
    congr 1
    linarith
  have a_nonneg : 0 ≤ a := div_nonneg (integral_nonneg good_nonneg) r_pos.le
  have a_le_one : a ≤ 1 := by
    calc
      a ≤ r / r := div_le_div_of_nonneg_right good_integral_le r_pos.le
      _ = 1 := div_self r_pos.ne'
  have tail_moment_bound : (∫ x, badMoment x ∂μ) ≤ (L + 3) / (1000 * (d : ℝ)) :=
    (actual_standard_row_tail_first_moment (d := d) (q := q) hq).2.2.2
  refine ⟨a_nonneg, a_le_one, bias_identity, ?_⟩
  calc
    1 - a = (∫ x, badMoment x ∂μ) / r := bias_identity
    _ ≤ ((L + 3) / (1000 * (d : ℝ))) / r :=
      div_le_div_of_nonneg_right tail_moment_bound r_pos.le
    _ = (L + 3) / (1000 * r * (d : ℝ)) := by
      rw [div_div]
      congr 1
      ring

end AutoSamplingTheory.Tests.GaussianComplexityFixedSpectrumTruncatedRadialMoment
