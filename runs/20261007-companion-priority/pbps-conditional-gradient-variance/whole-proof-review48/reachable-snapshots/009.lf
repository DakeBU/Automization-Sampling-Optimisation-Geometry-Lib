import AutoSamplingTheory.TechnicalLemmas.Measure.IsotropicGaussianDensity
import Mathlib.MeasureTheory.Group.Prod

/-!
# Density of the Gaussian augmentation

The joint-law density component of equations (2.6)-(2.7) in
arXiv:2609.06905v1, Section 2.2. The reference measure here is `μ.prod volume`.
Inserting the source's Gibbs density for `μ` to obtain a density relative to
`volume.prod volume` is a separate obligation. No reflection or PBPS-process
invariance, conditional representative, convergence, or query cost is claimed.
-/

open MeasureTheory ProbabilityTheory
open scoped ENNReal

namespace AutoSamplingTheory.ExampleCases.ProximalBPS.GaussianAugmentation

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]

/-- The law of independent `X ~ μ`, `Z ~ stdGaussian E` and
`Y = X + sqrt η • Z` has the displayed joint density relative to
`μ.prod volume`. The input law may be singular with respect to volume. -/
theorem augmentation_eq_withDensity (μ : Measure E) [IsProbabilityMeasure μ]
    (η : ℝ) (hη : 0 < η) :
    Measure.map (fun p : E × E => (p.1, p.1 + Real.sqrt η • p.2))
        (μ.prod (stdGaussian E)) =
      (μ.prod (volume : Measure E)).withDensity (fun p =>
        ENNReal.ofReal
          (((Real.sqrt (2 * Real.pi * η))⁻¹) ^ Module.finrank ℝ E *
            Real.exp (-‖p.2 - p.1‖ ^ 2 / (2 * η)))) := by
  let σ : E → E := fun z => Real.sqrt η • z
  let q : E → ℝ≥0∞ := fun z => ENNReal.ofReal
    (((Real.sqrt (2 * Real.pi * η))⁻¹) ^ Module.finrank ℝ E *
      Real.exp (-‖z‖ ^ 2 / (2 * η)))
  let S : E × E ≃ᵐ E × E := MeasurableEquiv.shearAddRight E
  have hq : Measurable q := by fun_prop
  have hnoise : (stdGaussian E).map σ = (volume : Measure E).withDensity q :=
    TechnicalLemmas.Measure.IsotropicGaussianDensity.map_sqrt_smul_stdGaussian_eq_withDensity
      η hη
  have hprod : Measure.map (Prod.map id σ) (μ.prod (stdGaussian E)) =
      μ.prod ((volume : Measure E).withDensity q) := by
    rw [← Measure.map_prod_map μ (stdGaussian E) measurable_id (by fun_prop),
      hnoise, Measure.map_id]
  have hΦ : (fun p : E × E => (p.1, p.1 + Real.sqrt η • p.2)) =
      S ∘ Prod.map id σ := rfl
  have hvol : (μ.prod (volume : Measure E)).map S = μ.prod volume :=
    (measurePreserving_prod_add μ volume).map_eq
  rw [hΦ, ← Measure.map_map S.measurable (by fun_prop), hprod,
    prod_withDensity_right hq,
    TechnicalLemmas.Measure.RadonNikodym.measurableEquiv_map_withDensity
      S _ (f := fun p : E × E => q p.2) (by fun_prop), hvol]
  congr 1
  funext p
  change q (-p.1 + p.2) = q (p.2 - p.1)
  rw [neg_add_eq_sub]

end AutoSamplingTheory.ExampleCases.ProximalBPS.GaussianAugmentation
