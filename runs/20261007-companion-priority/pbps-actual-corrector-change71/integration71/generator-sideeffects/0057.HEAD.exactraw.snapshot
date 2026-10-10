# AutoSamplingTheory.TechnicalLemmas.Measure.Gibbs

- File: `AutoSamplingTheory/TechnicalLemmas/Measure/Gibbs.lean`
- Layer: Mathlib-ready technical lemma
- Purpose: ENNReal Gibbs density, positivity/finite-value, measurability, nonzero/finite-by-envelope, potential-envelope, and finite-measure lower-bound integral contracts, plus normalized withDensity probability bridges
- Mathlib-quality status: preferred Mathlib-style location for Gibbs target-measure wrappers

## Imports

- `AutoSamplingTheory.TechnicalLemmas.Measure.RadonNikodym`
- `Mathlib.MeasureTheory.Function.SpecialFunctions.Basic`

## Representative Declarations And Exports

- `gibbsDensityENNReal`
- `gibbsDensityENNReal_pos`
- `gibbsDensityENNReal_lt_top`
- `measurable_gibbsDensityENNReal`
- `aemeasurable_gibbsDensityENNReal`
- `lintegral_gibbsDensityENNReal_ne_zero`
- `lintegral_gibbsDensityENNReal_ne_top_of_ae_le`
- `gibbsDensityENNReal_le_of_potential_ge`
- `gibbsDensityENNReal_ae_le_of_ae_potential_ge`
- `lintegral_gibbsDensityENNReal_ne_top_of_ae_potential_ge`
- `lintegral_gibbsDensityENNReal_ne_top_of_ae_ge_const`
- `isProbabilityMeasure_withDensity_normalized_gibbs`
- `isProbabilityMeasure_withDensity_normalized_gibbs_of_ae_le`
- `isProbabilityMeasure_withDensity_normalized_gibbs_of_ae_potential_ge`
- `isProbabilityMeasure_withDensity_normalized_gibbs_of_ae_ge_const`

## Curated Formalized Memory Entries

- `measure.gibbs-density.pointwise-positive-finite` -> `gibbsDensityENNReal_pos` (Mathlib.Data.ENNReal.Real; Mathlib.Analysis.SpecialFunctions.Exp)
- `measure.gibbs-density.aemeasurable` -> `aemeasurable_gibbsDensityENNReal` (Mathlib.MeasureTheory.Function.SpecialFunctions.Basic; Mathlib.MeasureTheory.Constructions.BorelSpace.Real)
- `measure.gibbs-density.normalized-probability` -> `isProbabilityMeasure_withDensity_normalized_gibbs` (AutoSamplingTheory.TechnicalLemmas.Measure.RadonNikodym; Mathlib.MeasureTheory.Measure.WithDensity)
- `measure.gibbs-density.integral-nonzero` -> `lintegral_gibbsDensityENNReal_ne_zero` (Mathlib.MeasureTheory.Integral.Lebesgue.Basic; Mathlib.Order.Filter.Basic)
- `measure.gibbs-density.integral-finite-envelope` -> `lintegral_gibbsDensityENNReal_ne_top_of_ae_le` (Mathlib.MeasureTheory.Integral.Lebesgue.Basic)
- `measure.gibbs-density.potential-envelope-pointwise` -> `gibbsDensityENNReal_le_of_potential_ge` (Mathlib.MeasureTheory.Function.SpecialFunctions.Basic; Mathlib.Data.ENNReal.Real)
- `measure.gibbs-density.integral-finite-potential-envelope` -> `lintegral_gibbsDensityENNReal_ne_top_of_ae_potential_ge` (AutoSamplingTheory.TechnicalLemmas.Measure.Gibbs; Mathlib.MeasureTheory.Integral.Lebesgue.Basic)
- `measure.gibbs-density.finite-measure-lower-bound` -> `isProbabilityMeasure_withDensity_normalized_gibbs_of_ae_ge_const` (AutoSamplingTheory.TechnicalLemmas.Measure.Gibbs; Mathlib.MeasureTheory.Integral.Lebesgue.Basic)
- `measure.gibbs-density.normalized-probability-envelope` -> `isProbabilityMeasure_withDensity_normalized_gibbs_of_ae_le` (AutoSamplingTheory.TechnicalLemmas.Measure.Gibbs; Mathlib.MeasureTheory.Measure.WithDensity)
- `measure.gibbs-density.normalized-probability-potential-envelope` -> `isProbabilityMeasure_withDensity_normalized_gibbs_of_ae_potential_ge` (AutoSamplingTheory.TechnicalLemmas.Measure.Gibbs; Mathlib.MeasureTheory.Measure.WithDensity)

## Agent Usage

Search this card before inventing a nearby technical lemma.  If the needed fact
is generic and missing, create a Mathlib-ready leaf packet rather than hiding
the requirement inside a paper-specific theorem.
