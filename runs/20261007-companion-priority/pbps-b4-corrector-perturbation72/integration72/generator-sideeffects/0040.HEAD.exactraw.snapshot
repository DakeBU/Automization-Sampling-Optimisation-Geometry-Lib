# AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.LineDeriv

- File: `AutoSamplingTheory/TechnicalLemmas/Analysis/Calculus/LineDeriv.lean`
- Layer: Mathlib-ready technical lemma
- Purpose: line-derivative product-rule and second-derivative wiring bridges for finite-coordinate weighted-product calculations, including equality-form `lineDeriv`, explicit `exp(-V) * g` coordinate leaves, and `fderiv`-to-`iteratedFDeriv` coordinate leaves
- Mathlib-quality status: preferred ANALYSIS/SDE bridge for the product-rule and Hessian-coordinate components before divergence, IBP, or invariant-law contracts

## Imports

- `AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient`
- `Mathlib.Analysis.Calculus.ContDiff.FTaylorSeries`
- `Mathlib.Analysis.Calculus.FDeriv.CompCLM`
- `Mathlib.Analysis.Calculus.LineDeriv.Basic`

## Representative Declarations And Exports

- `hasLineDerivAt_mul`
- `hasLineDerivAt_rho_mul`
- `lineDeriv_rho_mul_eq_of_hasLineDerivAt`
- `lineDeriv_expNegPotential_mul_eq_of_differentiableAt`
- `hasLineDerivAt_fderiv_apply_const_of_hasFDerivAt_fderiv`
- `lineDeriv_fderiv_apply_const_eq_of_hasFDerivAt_fderiv`
- `lineDeriv_fderiv_apply_const_eq_iteratedFDeriv_two`
- `lineDeriv_fderiv_apply_coordinate_eq_iteratedFDeriv_two`
- `lineDeriv_expNegPotential_mul_fderiv_coordinate_eq`

## Curated Formalized Memory Entries

- `analysis.calculus.line-derivative-product-rule` -> `hasLineDerivAt_mul` (Mathlib.Analysis.Calculus.LineDeriv.Basic; Mathlib.Analysis.Calculus.Deriv.Mul)
- `analysis.calculus.line-derivative-rho-product-rule` -> `hasLineDerivAt_rho_mul` (AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.LineDeriv)
- `analysis.calculus.line-derivative-rho-product-rule-lineDeriv` -> `lineDeriv_rho_mul_eq_of_hasLineDerivAt` (Mathlib.Analysis.Calculus.LineDeriv.Basic; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.LineDeriv)
- `analysis.calculus.line-derivative-exp-neg-potential-product-coordinate` -> `lineDeriv_expNegPotential_mul_eq_of_differentiableAt` (Mathlib.Analysis.Calculus.LineDeriv.Basic; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.LineDeriv)
- `analysis.calculus.line-derivative-fderiv-apply-const-from-hasFDerivAt` -> `hasLineDerivAt_fderiv_apply_const_of_hasFDerivAt_fderiv` (Mathlib.Analysis.Calculus.FDeriv.CompCLM; Mathlib.Analysis.Calculus.LineDeriv.Basic)
- `analysis.calculus.line-derivative-fderiv-apply-const-lineDeriv` -> `lineDeriv_fderiv_apply_const_eq_of_hasFDerivAt_fderiv` (AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.LineDeriv)
- `analysis.calculus.line-derivative-fderiv-apply-iteratedFDeriv-two` -> `lineDeriv_fderiv_apply_const_eq_iteratedFDeriv_two` (Mathlib.Analysis.Calculus.ContDiff.FTaylorSeries; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.LineDeriv)
- `analysis.calculus.line-derivative-fderiv-coordinate-iteratedFDeriv-two` -> `lineDeriv_fderiv_apply_coordinate_eq_iteratedFDeriv_two` (AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.LineDeriv)
- `analysis.calculus.line-derivative-exp-neg-potential-fderiv-coordinate` -> `lineDeriv_expNegPotential_mul_fderiv_coordinate_eq` (AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.LineDeriv)

## Agent Usage

Search this card before inventing a nearby technical lemma.  If the needed fact
is generic and missing, create a Mathlib-ready leaf packet rather than hiding
the requirement inside a paper-specific theorem.
