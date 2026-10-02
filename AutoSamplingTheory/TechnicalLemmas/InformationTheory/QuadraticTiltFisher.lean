import AutoSamplingTheory.TechnicalLemmas.InformationTheory.RelativeFisher
import AutoSamplingTheory.TechnicalLemmas.InformationTheory.TiltedLogRatio

/-!
# Relative Fisher energy of quadratic tilt representatives

Lee--Shen--Tian, arXiv:2010.03106v4, Lemma 2, first computes the
relative score between two restricted-Gaussian fibers in equation (11), then
integrates its squared norm under the left fiber.  This file isolates that
second step for the explicit smooth representative.

It does not differentiate Mathlib's canonical measurable `llr`, and it does
not prove a log-Sobolev, Talagrand, or Wasserstein inequality.
-/

namespace AutoSamplingTheory
namespace TechnicalLemmas
namespace InformationTheory
namespace QuadraticTiltFisher

open MeasureTheory
open scoped RealInnerProductSpace

noncomputable section

variable {ι : Type*} [Fintype ι]

private abbrev State := EuclideanSpace ℝ ι

/-- The relative Fisher energy of the explicit normalized quadratic log-ratio
representative is exactly the squared center displacement divided by `eta²`.

The common base `nu` appears only through the two spatially constant
normalizers, while the separate probability law `mu` is the measure under
which the score energy is integrated.  Keeping these roles separate is needed
for the paper specialization, where `mu` is the left normalized tilt of `nu`.
The probability assumption is the genuine step that turns the integral of the
constant squared score into that constant.  The paper consumer has `eta > 0`;
the algebraic statement only requires `eta ≠ 0`. -/
theorem information_quadratic_representative
    (nu mu : Measure (State (ι := ι))) [IsProbabilityMeasure mu]
    {eta : ℝ} (heta : eta ≠ 0) (y y' : State (ι := ι)) :
    RelativeFisher.information mu (fun _ => 1)
        (fun t =>
          -(‖t - y‖ ^ 2 / (2 * eta)) -
            Real.log (∫ z, Real.exp (-(‖z - y‖ ^ 2 / (2 * eta))) ∂nu) -
          (-(‖t - y'‖ ^ 2 / (2 * eta))) +
            Real.log (∫ z, Real.exp (-(‖z - y'‖ ^ 2 / (2 * eta))) ∂nu)) =
      eta⁻¹ ^ 2 * ‖y - y'‖ ^ 2 := by
  rw [RelativeFisher.information]
  simp_rw [RelativeFisher.densityEnergy, one_mul,
    TiltedLogRatio.gradient_quadratic_representative nu heta y y']
  simp [norm_smul, Real.norm_eq_abs, mul_pow]

end

end QuadraticTiltFisher
end InformationTheory
end TechnicalLemmas
end AutoSamplingTheory
