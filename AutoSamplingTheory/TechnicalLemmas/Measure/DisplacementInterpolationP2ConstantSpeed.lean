import AutoSamplingTheory.TechnicalLemmas.Measure.DisplacementInterpolationConstantSpeed

/-!
# Constant speed of displacement interpolation for arbitrary P2 endpoints

This module generalizes the ordered metric identity from absolutely continuous
endpoints to arbitrary probability measures with finite second moments.  The
supplied coupling is assumed to attain the quadratic transport infimum.
-/

namespace AutoSamplingTheory
namespace TechnicalLemmas
namespace Measure
namespace DisplacementInterpolationConstantSpeed

open MeasureTheory Set
open scoped ENNReal

noncomputable section

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
  [SecondCountableTopology E] [StandardBorelSpace E] [Nonempty E]

open DisplacementInterpolation

/-- The ordered constant-speed identity for arbitrary probability endpoints
with finite second moments.

This is the metric-identity component of Statistical Optimal Transport,
Theorem 7.6. Optimal-coupling existence is an input. Finite second moments make
the endpoint distance finite, which permits cancellation in `ℝ≥0∞`; absolute
continuity is not required. -/
theorem wassersteinDistance_interpolation_eq_of_le_of_integrable_norm_sq
    {γ : Measure (E × E)} {μ₀ μ₁ : Measure E}
    [IsProbabilityMeasure μ₀] [IsProbabilityMeasure μ₁]
    (hμ₀ : Integrable (fun x : E => ‖x‖ ^ 2) μ₀)
    (hμ₁ : Integrable (fun x : E => ‖x‖ ^ 2) μ₁)
    (hγ : IsQuadraticOptimalCoupling γ μ₀ μ₁)
    {s t : ℝ} (hs0 : 0 ≤ s) (hst : s ≤ t) (ht1 : t ≤ 1) :
    WassersteinSpace.wassersteinDistance
        (displacementInterpolation γ s)
        (displacementInterpolation γ t) =
      ENNReal.ofReal (t - s) *
        WassersteinSpace.wassersteinDistance μ₀ μ₁ := by
  let μs : Measure E := displacementInterpolation γ s
  let μt : Measure E := displacementInterpolation γ t
  letI : IsProbabilityMeasure μs := by
    dsimp [μs]
    exact isProbabilityMeasure_displacementInterpolation hγ.1 s
  letI : IsProbabilityMeasure μt := by
    dsimp [μt]
    exact isProbabilityMeasure_displacementInterpolation hγ.1 t

  have hupper :
      WassersteinSpace.wassersteinDistance μs μt ≤
        ENNReal.ofReal (t - s) * WassersteinSpace.wassersteinDistance μ₀ μ₁ := by
    simpa [μs, μt] using wassersteinDistance_interpolation_le (E := E) hγ hst

  have h0s :
      WassersteinSpace.wassersteinDistance μ₀ μs ≤
        ENNReal.ofReal s * WassersteinSpace.wassersteinDistance μ₀ μ₁ := by
    have h := wassersteinDistance_interpolation_le (E := E) hγ hs0
    rw [displacementInterpolation_zero hγ.1] at h
    simpa [μs] using h

  have ht1' :
      WassersteinSpace.wassersteinDistance μt μ₁ ≤
        ENNReal.ofReal (1 - t) * WassersteinSpace.wassersteinDistance μ₀ μ₁ := by
    have h := wassersteinDistance_interpolation_le (E := E) hγ ht1
    rw [displacementInterpolation_one hγ.1] at h
    simpa [μt] using h

  have htri_left :=
    WassersteinTriangleExact.wassersteinDistance_triangle μ₀ μs μ₁
  have htri_right :=
    WassersteinTriangleExact.wassersteinDistance_triangle μs μt μ₁
  have hchain :
      WassersteinSpace.wassersteinDistance μ₀ μ₁ ≤
        WassersteinSpace.wassersteinDistance μ₀ μs +
          WassersteinSpace.wassersteinDistance μs μt +
            WassersteinSpace.wassersteinDistance μt μ₁ := by
    calc
      WassersteinSpace.wassersteinDistance μ₀ μ₁ ≤
          WassersteinSpace.wassersteinDistance μ₀ μs +
            WassersteinSpace.wassersteinDistance μs μ₁ := htri_left
      _ ≤ WassersteinSpace.wassersteinDistance μ₀ μs +
            (WassersteinSpace.wassersteinDistance μs μt +
              WassersteinSpace.wassersteinDistance μt μ₁) := by
        exact add_le_add le_rfl htri_right
      _ = WassersteinSpace.wassersteinDistance μ₀ μs +
            WassersteinSpace.wassersteinDistance μs μt +
              WassersteinSpace.wassersteinDistance μt μ₁ := by
        simp [add_assoc]

  have hchain' :
      WassersteinSpace.wassersteinDistance μ₀ μ₁ ≤
        ENNReal.ofReal s * WassersteinSpace.wassersteinDistance μ₀ μ₁ +
          WassersteinSpace.wassersteinDistance μs μt +
            ENNReal.ofReal (1 - t) * WassersteinSpace.wassersteinDistance μ₀ μ₁ := by
    exact hchain.trans (add_le_add (add_le_add h0s le_rfl) ht1')

  have hcoeff := interpolation_coefficients_sum_one hs0 hst ht1
  have hpartition :
      WassersteinSpace.wassersteinDistance μ₀ μ₁ =
        ENNReal.ofReal s * WassersteinSpace.wassersteinDistance μ₀ μ₁ +
          ENNReal.ofReal (t - s) * WassersteinSpace.wassersteinDistance μ₀ μ₁ +
            ENNReal.ofReal (1 - t) * WassersteinSpace.wassersteinDistance μ₀ μ₁ := by
    calc
      WassersteinSpace.wassersteinDistance μ₀ μ₁ =
          1 * WassersteinSpace.wassersteinDistance μ₀ μ₁ := by simp
      _ = (ENNReal.ofReal s + ENNReal.ofReal (t - s) + ENNReal.ofReal (1 - t)) *
            WassersteinSpace.wassersteinDistance μ₀ μ₁ := by rw [hcoeff]
      _ = ENNReal.ofReal s * WassersteinSpace.wassersteinDistance μ₀ μ₁ +
            ENNReal.ofReal (t - s) * WassersteinSpace.wassersteinDistance μ₀ μ₁ +
              ENNReal.ofReal (1 - t) * WassersteinSpace.wassersteinDistance μ₀ μ₁ := by
        simp [add_mul, add_assoc]

  have hcancelInput :
      ENNReal.ofReal s * WassersteinSpace.wassersteinDistance μ₀ μ₁ +
          ENNReal.ofReal (t - s) * WassersteinSpace.wassersteinDistance μ₀ μ₁ +
            ENNReal.ofReal (1 - t) * WassersteinSpace.wassersteinDistance μ₀ μ₁ ≤
        ENNReal.ofReal s * WassersteinSpace.wassersteinDistance μ₀ μ₁ +
          WassersteinSpace.wassersteinDistance μs μt +
            ENNReal.ofReal (1 - t) * WassersteinSpace.wassersteinDistance μ₀ μ₁ := by
    rw [← hpartition]
    exact hchain'

  have hd : WassersteinSpace.wassersteinDistance μ₀ μ₁ < ∞ :=
    WassersteinFiniteSecondMoment.wassersteinDistance_lt_top_of_integrable_norm_sq
      μ₀ μ₁ hμ₀ hμ₁
  have hprefix :
      ENNReal.ofReal s * WassersteinSpace.wassersteinDistance μ₀ μ₁ < ∞ :=
    ENNReal.mul_lt_top ENNReal.ofReal_lt_top hd
  have hsuffix :
      ENNReal.ofReal (1 - t) * WassersteinSpace.wassersteinDistance μ₀ μ₁ < ∞ :=
    ENNReal.mul_lt_top ENNReal.ofReal_lt_top hd

  have hcancelSuffix :
      ENNReal.ofReal s * WassersteinSpace.wassersteinDistance μ₀ μ₁ +
          ENNReal.ofReal (t - s) * WassersteinSpace.wassersteinDistance μ₀ μ₁ ≤
        ENNReal.ofReal s * WassersteinSpace.wassersteinDistance μ₀ μ₁ +
          WassersteinSpace.wassersteinDistance μs μt := by
    exact (ENNReal.add_le_add_iff_right hsuffix.ne).mp
      (by simpa [add_assoc] using hcancelInput)
  have hlower :
      ENNReal.ofReal (t - s) * WassersteinSpace.wassersteinDistance μ₀ μ₁ ≤
        WassersteinSpace.wassersteinDistance μs μt :=
    (ENNReal.add_le_add_iff_left hprefix.ne).mp hcancelSuffix

  change WassersteinSpace.wassersteinDistance μs μt =
    ENNReal.ofReal (t - s) * WassersteinSpace.wassersteinDistance μ₀ μ₁
  exact le_antisymm hupper hlower

end

end DisplacementInterpolationConstantSpeed
end Measure
end TechnicalLemmas
end AutoSamplingTheory
