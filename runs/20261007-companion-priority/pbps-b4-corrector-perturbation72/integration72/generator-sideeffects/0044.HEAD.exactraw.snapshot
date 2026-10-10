# AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability

- File: `AutoSamplingTheory/TechnicalLemmas/Analysis/Integrability.lean`
- Layer: Mathlib-ready technical lemma
- Purpose: ofReal lintegral/Integrable bridge, finite-dimensional Gaussian quadratic-tail integrability, exact quadratic normalizers, exact one-dimensional Laplace normalizers, and quadratic/Laplace lower-bound Gibbs normalization leaves
- Mathlib-quality status: preferred Mathlib-style location for Lebesgue tail and coercive-envelope leaves; general coercive envelopes remain red

## Imports

- `AutoSamplingTheory.TechnicalLemmas.Geometry.StrongConvexity`
- `AutoSamplingTheory.TechnicalLemmas.Measure.Gibbs`
- `Mathlib.Analysis.SpecialFunctions.ImproperIntegrals`
- `Mathlib.Analysis.SpecialFunctions.Gaussian.FourierTransform`

## Representative Declarations And Exports

- `lintegral_ofReal_ne_top_of_integrable_nonneg`
- `integrable_exp_neg_mul_norm_sq`
- `integrable_exp_neg_add_mul_norm_sq`
- `lintegral_exp_neg_add_mul_norm_sq_ne_top`
- `integrable_exp_neg_add_mul_norm_sub_sq`
- `lintegral_exp_neg_add_mul_norm_sub_sq_ne_top`
- `integrable_exp_neg_add_mul_abs`
- `lintegral_exp_neg_add_mul_abs_ne_top`
- `integral_exp_neg_add_mul_abs_eq`
- `lintegral_exp_neg_add_mul_abs_eq`
- `lintegral_exp_neg_mul_norm_sq_eq`
- `lintegral_exp_neg_add_mul_norm_sq_eq`
- `lintegral_exp_neg_add_mul_norm_sub_sq_eq`
- `isProbabilityMeasure_withDensity_exp_neg_add_mul_norm_sq`
- `isProbabilityMeasure_withDensity_exp_neg_add_mul_norm_sub_sq`
- `isProbabilityMeasure_withDensity_exp_neg_add_mul_abs`
- `lintegral_gibbsDensityENNReal_ne_top_of_ae_quadratic_lower_bound`
- `lintegral_gibbsDensityENNReal_ne_top_of_ae_centered_quadratic_lower_bound`
- `lintegral_gibbsDensityENNReal_ne_top_of_ae_abs_linear_lower_bound`
- `lintegral_gibbsDensityENNReal_ne_top_of_strongConvexOn_minimizer`
- `isProbabilityMeasure_withDensity_normalized_gibbs_of_ae_quadratic_lower_bound`
- `isProbabilityMeasure_withDensity_normalized_gibbs_of_ae_centered_quadratic_lower_bound`
- `isProbabilityMeasure_withDensity_normalized_gibbs_of_ae_abs_linear_lower_bound`
- `isProbabilityMeasure_withDensity_normalized_gibbs_of_strongConvexOn_minimizer`

## Curated Formalized Memory Entries

- `analysis.integrability.of-real-lintegral-finite` -> `lintegral_ofReal_ne_top_of_integrable_nonneg` (Mathlib.MeasureTheory.Function.L1Space.Integrable)
- `analysis.integrability.gaussian-quadratic-tail` -> `integrable_exp_neg_mul_norm_sq` (Mathlib.Analysis.SpecialFunctions.Gaussian.FourierTransform)
- `analysis.integrability.shifted-gaussian-quadratic-tail` -> `integrable_exp_neg_add_mul_norm_sq` (AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability)
- `analysis.integrability.centered-gaussian-quadratic-tail` -> `integrable_exp_neg_add_mul_norm_sub_sq` (AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability; Mathlib.MeasureTheory.Group.Integral)
- `analysis.integrability.laplace-absolute-linear-tail` -> `integrable_exp_neg_add_mul_abs` (Mathlib.Analysis.SpecialFunctions.ImproperIntegrals; Mathlib.MeasureTheory.Integral.IntegrableOn)
- `analysis.integrability.gaussian-quadratic-tail-normalizer` -> `lintegral_exp_neg_mul_norm_sq_eq` (Mathlib.Analysis.SpecialFunctions.Gaussian.FourierTransform; Mathlib.MeasureTheory.Integral.Bochner.Basic)
- `analysis.integrability.shifted-gaussian-quadratic-tail-normalizer` -> `lintegral_exp_neg_add_mul_norm_sq_eq` (AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability)
- `analysis.integrability.centered-gaussian-quadratic-tail-normalizer` -> `lintegral_exp_neg_add_mul_norm_sub_sq_eq` (AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability; Mathlib.MeasureTheory.Group.Integral)
- `analysis.integrability.laplace-absolute-linear-tail-finite-lintegral` -> `lintegral_exp_neg_add_mul_abs_ne_top` (AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability)
- `analysis.integrability.laplace-absolute-linear-tail-real-normalizer` -> `integral_exp_neg_add_mul_abs_eq` (Mathlib.Analysis.SpecialFunctions.ImproperIntegrals; Mathlib.MeasureTheory.Integral.Bochner.Set)
- `analysis.integrability.laplace-absolute-linear-tail-ennreal-normalizer` -> `lintegral_exp_neg_add_mul_abs_eq` (AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability; Mathlib.MeasureTheory.Integral.Bochner.Basic)
- `measure.gibbs-density.explicit-laplace-normalized-probability` -> `isProbabilityMeasure_withDensity_exp_neg_add_mul_abs` (AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability; AutoSamplingTheory.TechnicalLemmas.Measure.Gibbs)
- `measure.gibbs-density.explicit-quadratic-normalized-probability` -> `isProbabilityMeasure_withDensity_exp_neg_add_mul_norm_sq` (AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability; AutoSamplingTheory.TechnicalLemmas.Measure.Gibbs)
- `measure.gibbs-density.explicit-centered-quadratic-normalized-probability` -> `isProbabilityMeasure_withDensity_exp_neg_add_mul_norm_sub_sq` (AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability; AutoSamplingTheory.TechnicalLemmas.Measure.Gibbs)
- `measure.gibbs-density.integral-finite-quadratic-lower-bound` -> `lintegral_gibbsDensityENNReal_ne_top_of_ae_quadratic_lower_bound` (AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability; AutoSamplingTheory.TechnicalLemmas.Measure.Gibbs)
- `measure.gibbs-density.integral-finite-centered-quadratic-lower-bound` -> `lintegral_gibbsDensityENNReal_ne_top_of_ae_centered_quadratic_lower_bound` (AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability; AutoSamplingTheory.TechnicalLemmas.Measure.Gibbs)
- `measure.gibbs-density.normalized-probability-quadratic-lower-bound` -> `isProbabilityMeasure_withDensity_normalized_gibbs_of_ae_quadratic_lower_bound` (AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability; AutoSamplingTheory.TechnicalLemmas.Measure.Gibbs)
- `measure.gibbs-density.normalized-probability-centered-quadratic-lower-bound` -> `isProbabilityMeasure_withDensity_normalized_gibbs_of_ae_centered_quadratic_lower_bound` (AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability; AutoSamplingTheory.TechnicalLemmas.Measure.Gibbs)
- `measure.gibbs-density.integral-finite-strong-convex-minimizer` -> `lintegral_gibbsDensityENNReal_ne_top_of_strongConvexOn_minimizer` (AutoSamplingTheory.TechnicalLemmas.Geometry.StrongConvexity; AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability)
- `measure.gibbs-density.normalized-probability-strong-convex-minimizer` -> `isProbabilityMeasure_withDensity_normalized_gibbs_of_strongConvexOn_minimizer` (AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability; AutoSamplingTheory.TechnicalLemmas.Measure.Gibbs)
- `measure.gibbs-density.integral-finite-absolute-linear-lower-bound` -> `lintegral_gibbsDensityENNReal_ne_top_of_ae_abs_linear_lower_bound` (AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability; AutoSamplingTheory.TechnicalLemmas.Measure.Gibbs)
- `measure.gibbs-density.normalized-probability-absolute-linear-lower-bound` -> `isProbabilityMeasure_withDensity_normalized_gibbs_of_ae_abs_linear_lower_bound` (AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability; AutoSamplingTheory.TechnicalLemmas.Measure.Gibbs)

## Agent Usage

Search this card before inventing a nearby technical lemma.  If the needed fact
is generic and missing, create a Mathlib-ready leaf packet rather than hiding
the requirement inside a paper-specific theorem.
