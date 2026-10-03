import AutoSamplingTheory.TechnicalLemmas.Measure.DisplacementInterpolation
import Mathlib.MeasureTheory.Integral.Lebesgue.Basic
import Mathlib.Tactic

/-!
# Midpoints of quadratic-optimal couplings remain optimal

Kantorovich feasibility is affine in the joint measure and the quadratic
transport objective is a lower Lebesgue integral, hence linear in the measure.
Therefore the midpoint of two optimal couplings with the same marginals is
again optimal.

This is the optimization-theoretic input for Brenier uniqueness. No convex
potential, differentiability, or graph theorem is used here.
-/

namespace AutoSamplingTheory
namespace TechnicalLemmas
namespace Measure
namespace QuadraticOptimalMidpoint

open MeasureTheory
open DisplacementInterpolation Transport WassersteinSpace
open scoped ENNReal

noncomputable section

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]

/-- Arithmetic midpoint of two measures. -/
noncomputable def midpointMeasure (gamma₀ gamma₁ : Measure (E × E)) : Measure (E × E) :=
  (2 : ℝ≥0∞)⁻¹ • gamma₀ + (2 : ℝ≥0∞)⁻¹ • gamma₁

private theorem inv_two_add_inv_two :
    (2 : ℝ≥0∞)⁻¹ + (2 : ℝ≥0∞)⁻¹ = 1 := by
  rw [← two_mul]
  exact ENNReal.mul_inv_cancel (by norm_num) (by norm_num)

/-- Couplings with common marginals are closed under the arithmetic midpoint. -/
theorem isCoupling_midpoint
    {gamma₀ gamma₁ : Measure (E × E)} {mu₀ mu₁ : Measure E}
    (h₀ : IsCoupling gamma₀ mu₀ mu₁)
    (h₁ : IsCoupling gamma₁ mu₀ mu₁) :
    IsCoupling (midpointMeasure gamma₀ gamma₁) mu₀ mu₁ := by
  constructor
  · rw [Measure.fst, midpointMeasure,
      Measure.map_add _ _ measurable_fst]
    simp only [Measure.map_smul, h₀.1, h₁.1]
    rw [← add_smul, inv_two_add_inv_two, one_smul]
  · rw [Measure.snd, midpointMeasure,
      Measure.map_add _ _ measurable_snd]
    simp only [Measure.map_smul, h₀.2, h₁.2]
    rw [← add_smul, inv_two_add_inv_two, one_smul]

/-- The lower integral of any nonnegative function over a midpoint measure is
the midpoint of the two lower integrals. -/
theorem lintegral_midpoint (f : E × E → ℝ≥0∞)
    (gamma₀ gamma₁ : Measure (E × E)) :
    (∫⁻ z, f z ∂midpointMeasure gamma₀ gamma₁) =
      (2 : ℝ≥0∞)⁻¹ * (∫⁻ z, f z ∂gamma₀) +
        (2 : ℝ≥0∞)⁻¹ * (∫⁻ z, f z ∂gamma₁) := by
  simp [midpointMeasure, MeasureTheory.lintegral_add_measure,
    MeasureTheory.lintegral_smul_measure, smul_eq_mul]

/-- The midpoint of two quadratic-optimal couplings with identical marginals
is again a quadratic-optimal coupling. -/
theorem isQuadraticOptimalCoupling_midpoint
    {gamma₀ gamma₁ : Measure (E × E)} {mu₀ mu₁ : Measure E}
    (h₀ : IsQuadraticOptimalCoupling gamma₀ mu₀ mu₁)
    (h₁ : IsQuadraticOptimalCoupling gamma₁ mu₀ mu₁) :
    IsQuadraticOptimalCoupling (midpointMeasure gamma₀ gamma₁) mu₀ mu₁ := by
  refine ⟨isCoupling_midpoint h₀.1 h₁.1, ?_⟩
  rw [lintegral_midpoint]
  rw [h₀.2, h₁.2]
  rw [← add_mul, inv_two_add_inv_two, one_mul]

end

end QuadraticOptimalMidpoint
end Measure
end TechnicalLemmas
end AutoSamplingTheory
