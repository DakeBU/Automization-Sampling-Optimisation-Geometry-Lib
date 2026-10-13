# AutoSamplingTheory.TechnicalLemmas.Measure.GibbsIntegral

- File: `AutoSamplingTheory/TechnicalLemmas/Measure/GibbsIntegral.lean`
- Layer: Mathlib-ready technical lemma
- Purpose: Bochner integral rewrites for Gibbs withDensity measures, turning `Z⁻¹ * gibbsDensityENNReal V` integrals into real `Z.toReal⁻¹ * exp(-V)` weighted base-measure integrals
- Mathlib-quality status: preferred bridge from Gibbs target-measure wrappers to weak-generator, invariant-law, and KL/FI test-function algebra; does not prove normalization

## Imports

- `AutoSamplingTheory.TechnicalLemmas.Measure.Gibbs`
- `Mathlib.MeasureTheory.Integral.Bochner.ContinuousLinearMap`

## Representative Declarations And Exports

- `integral_withDensity_inv_mul_gibbsDensityENNReal_eq_integral_inv_mul_exp_smul`
- `integral_withDensity_lintegral_inv_mul_gibbsDensityENNReal_eq_integral_lintegral_inv_mul_exp_smul`
- `integral_withDensity_lintegral_inv_mul_gibbsDensityENNReal_eq_integral_lintegral_inv_mul_exp_smul_of_neZero`

## Curated Formalized Memory Entries

- `measure.gibbs-density.withDensity-integral-rewrite` -> `integral_withDensity_inv_mul_gibbsDensityENNReal_eq_integral_inv_mul_exp_smul` (AutoSamplingTheory.TechnicalLemmas.Measure.GibbsIntegral; Mathlib.MeasureTheory.Integral.Bochner.ContinuousLinearMap)
- `measure.gibbs-density.lintegral-withDensity-integral-rewrite` -> `integral_withDensity_lintegral_inv_mul_gibbsDensityENNReal_eq_integral_lintegral_inv_mul_exp_smul` (AutoSamplingTheory.TechnicalLemmas.Measure.GibbsIntegral)
- `measure.gibbs-density.lintegral-withDensity-integral-rewrite-nonzero-base` -> `integral_withDensity_lintegral_inv_mul_gibbsDensityENNReal_eq_integral_lintegral_inv_mul_exp_smul_of_neZero` (AutoSamplingTheory.TechnicalLemmas.Measure.GibbsIntegral; AutoSamplingTheory.TechnicalLemmas.Measure.Gibbs)

## Agent Usage

Search this card before inventing a nearby technical lemma.  If the needed fact
is generic and missing, create a Mathlib-ready leaf packet rather than hiding
the requirement inside a paper-specific theorem.
