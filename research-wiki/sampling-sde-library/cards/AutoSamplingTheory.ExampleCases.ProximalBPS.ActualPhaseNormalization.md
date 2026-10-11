# AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhaseNormalization

- File: `AutoSamplingTheory\ExampleCases\ProximalBPS\ActualPhaseNormalization.lean`
- Layer: uncategorized
- Purpose:
- Mathlib-quality status:

## Imports

- `AutoSamplingTheory.TechnicalLemmas.Analysis.HessianStrongConvexity`
- `AutoSamplingTheory.TechnicalLemmas.Analysis.StrongConvexGibbsIntegrability`
- `AutoSamplingTheory.TechnicalLemmas.Measure.IsotropicGaussianDensity`
- `AutoSamplingTheory.TechnicalLemmas.Measure.Gibbs`
- `Mathlib.MeasureTheory.Measure.Tilted`
- `Mathlib.MeasureTheory.Integral.Prod`

## Representative Declarations And Exports

- `actual_phase_normalization_statement`
- `actual_phase_gibbs_normalization`

## Curated Formalized Memory Entries

- `pbps.actualPhaseNormalization` -> `actual_phase_gibbs_normalization` (arXiv2609.06905v1 conditional energy and Eq3.1)

## Agent Usage

Search this card before inventing a nearby technical lemma.  If the needed fact
is generic and missing, create a Mathlib-ready leaf packet rather than hiding
the requirement inside a paper-specific theorem.
