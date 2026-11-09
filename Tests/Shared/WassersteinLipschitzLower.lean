import AutoSamplingTheory.TechnicalLemmas.Measure.GaussianMixtureWasserstein

open MeasureTheory ProbabilityTheory
open AutoSamplingTheory.TechnicalLemmas.Measure
open scoped ENNReal

-- Pin both literal measures and the source's only hypothesis. This example
-- consumes the named assembly, whose proof now owns the moment/mean work.
example (m : ℝ) (hm : 0 < m) :
    let μ := (1 / 2 : ℝ≥0∞) • gaussianReal (-m) 1 + (1 / 2 : ℝ≥0∞) • gaussianReal m 1
    let ν := (1 / 4 : ℝ≥0∞) • gaussianReal (-m) 1 + (3 / 4 : ℝ≥0∞) • gaussianReal m 1
    ENNReal.ofReal (m / 2) ≤ WassersteinSpace.wassersteinDistance μ ν ∧
      WassersteinSpace.wassersteinDistance μ ν ≤ ENNReal.ofReal m :=
  GaussianMixtureWasserstein.wassersteinDistance_gaussianMixtures_bounds m hm

#print axioms AutoSamplingTheory.TechnicalLemmas.Measure.GaussianMixtureWasserstein.wassersteinDistance_gaussianMixtures_bounds
