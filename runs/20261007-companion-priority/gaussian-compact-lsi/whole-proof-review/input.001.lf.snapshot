import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianCompactLogSobolev
import AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff

noncomputable section
open MeasureTheory ProbabilityTheory Filter
open scoped ENNReal BigOperators Topology
open AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianCompactLogSobolev
open AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff
namespace Tests.GaussianCompactLogSobolev

/-- Actual zero observer, without a positive mass or logarithm-domain premise. -/
theorem zero_observer_entropy_bound :
    (∫ _x : ℝ, (0 : ℝ)^2 * Real.log ((0 : ℝ)^2) ∂gaussianReal 0 1) -
      (∫ _x : ℝ, (0 : ℝ)^2 ∂gaussianReal 0 1) *
        Real.log (∫ _x : ℝ, (0 : ℝ)^2 ∂gaussianReal 0 1) ≤
    2 * ∫ x : ℝ, (deriv (fun _ : ℝ => 0) x)^2 ∂gaussianReal 0 1 :=
  compact_gaussian_logSobolev (fun _ : ℝ => 0) contDiff_const (by simp [HasCompactSupport])

/-- A concrete signed, nonzero smooth compact observer. The C2/support facts
are constructed here; this consumer does not take domain/limit certificates. -/
private def signedProbe (x : ℝ) : ℝ := x * smoothUnitCutoff x

theorem actual_signed_compact_entropy_bound :
    (∫ x, (signedProbe x)^2 * Real.log ((signedProbe x)^2) ∂gaussianReal 0 1) -
      (∫ x, (signedProbe x)^2 ∂gaussianReal 0 1) *
        Real.log (∫ x, (signedProbe x)^2 ∂gaussianReal 0 1) ≤
    2 * ∫ x, (deriv signedProbe x)^2 ∂gaussianReal 0 1 := by
  have hc : ContDiff ℝ 2 signedProbe :=
    contDiff_id.mul (smoothUnitCutoff_contDiff.of_le
      (WithTop.coe_le_coe.mpr (le_top : (2 : ℕ∞) ≤ ⊤)))
  exact compact_gaussian_logSobolev signedProbe hc smoothUnitCutoff_hasCompactSupport.mul_left

#print axioms compact_gaussian_logSobolev
#print axioms zero_observer_entropy_bound
#print axioms actual_signed_compact_entropy_bound

end Tests.GaussianCompactLogSobolev
