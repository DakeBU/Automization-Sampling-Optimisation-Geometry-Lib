# AutoSamplingTheory.TechnicalLemmas.Measure.RadonNikodym

- File: `AutoSamplingTheory/TechnicalLemmas/Measure/RadonNikodym.lean`
- Layer: Mathlib-ready technical lemma
- Purpose: withDensity mass, reciprocal-lintegral normalization, finite-pi product density decomposition, measurable-equivalence density transport, absolute-continuity, and RN reconstruction wrappers
- Mathlib-quality status: preferred Mathlib-style location for density normalization and RN derivative leaves

## Imports

- `Mathlib.MeasureTheory.Measure.Decomposition.RadonNikodym`
- `Mathlib.MeasureTheory.Constructions.Pi`
- `Mathlib.MeasureTheory.Integral.Lebesgue.Map`
- `Mathlib.MeasureTheory.Function.SpecialFunctions.Basic`
- `Mathlib.MeasureTheory.Measure.WithDensity`

## Representative Declarations And Exports

- `lintegral_fin_nat_prod_eq_prod`
- `lintegral_fintype_prod_eq_prod`
- `pi_withDensity_prod`
- `withDensity_univ_eq_lintegral`
- `isProbabilityMeasure_withDensity_of_lintegral_eq_one`
- `isProbabilityMeasure_withDensity_ofReal_exp_of_integral_eq_one`
- `isFiniteMeasure_withDensity_of_lintegral_ne_top`
- `lintegral_inv_lintegral_mul_eq_one`
- `isProbabilityMeasure_withDensity_normalized_lintegral`
- `withDensity_absolutelyContinuous_base`
- `measurableEquiv_map_withDensity`
- `withDensity_rnDeriv_eq_of_absolutelyContinuous`

## Curated Formalized Memory Entries

- `measure.with-density.probability-normalization` -> `isProbabilityMeasure_withDensity_of_lintegral_eq_one` (Mathlib.MeasureTheory.Measure.WithDensity; Mathlib.MeasureTheory.Measure.Typeclasses.Probability)
- `measure.with-density.ofReal-exp-probability-normalization` -> `isProbabilityMeasure_withDensity_ofReal_exp_of_integral_eq_one` (Mathlib.MeasureTheory.Integral.Bochner.Basic; AutoSamplingTheory.TechnicalLemmas.Measure.RadonNikodym; SLT/GaussianLSI/DualityEntropy.lean as proof-pattern provenance)
- `measure.density.normalized-lintegral-one` -> `lintegral_inv_lintegral_mul_eq_one` (Mathlib.MeasureTheory.Integral.Lebesgue.Add; Mathlib.Data.ENNReal.Inv)
- `measure.with-density.normalized-probability` -> `isProbabilityMeasure_withDensity_normalized_lintegral` (Mathlib.MeasureTheory.Measure.WithDensity; Mathlib.MeasureTheory.Integral.Lebesgue.Add)
- `measure.pi.lintegral-product-factorization` -> `lintegral_fintype_prod_eq_prod` (Mathlib.MeasureTheory.Integral.Pi; external AST PiWithDensity.lean)
- `measure.pi.with-density-product` -> `pi_withDensity_prod` (Mathlib.MeasureTheory.Measure.WithDensity; external AST PiWithDensity.lean)
- `measure.with-density.absolute-continuity` -> `withDensity_absolutelyContinuous_base` (Mathlib.MeasureTheory.Measure.WithDensity)
- `measure.with-density.map-measurable-equiv` -> `measurableEquiv_map_withDensity` (Mathlib.MeasureTheory.Integral.Lebesgue.Map; Mathlib.MeasureTheory.Measure.WithDensity)
- `measure.rn-deriv.reconstruction` -> `withDensity_rnDeriv_eq_of_absolutelyContinuous` (Mathlib.MeasureTheory.Measure.Decomposition.RadonNikodym)

## Agent Usage

Search this card before inventing a nearby technical lemma.  If the needed fact
is generic and missing, create a Mathlib-ready leaf packet rather than hiding
the requirement inside a paper-specific theorem.
