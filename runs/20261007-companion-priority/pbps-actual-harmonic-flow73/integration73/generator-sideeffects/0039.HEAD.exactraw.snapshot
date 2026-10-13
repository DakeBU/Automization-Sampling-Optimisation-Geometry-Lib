# AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient

- File: `AutoSamplingTheory/TechnicalLemmas/Analysis/Calculus/Gradient.lean`
- Layer: Mathlib-ready technical lemma
- Purpose: Mathlib gradient bridges for Langevin calculus: Gibbs-weight chain rule `∇ exp(-V) = -exp(-V) • ∇V` from `HasGradientAt` or `DifferentiableAt`, coordinate displays, finite-dimensional coordinate-unit line derivatives, and pointwise `fderiv`-to-`gradient` inner-product/coordinate bridges
- Mathlib-quality status: preferred ANALYSIS/SDE bridge from Mathlib gradient API to finite-coordinate Langevin algebra; pointwise only, with no divergence, IBP, or invariant-law claims

## Imports

- `AutoSamplingTheory.TechnicalLemmas.Geometry.EuclideanSpaceCoordinates`
- `Mathlib.Analysis.Calculus.Gradient.Basic`
- `Mathlib.Analysis.Calculus.LineDeriv.Basic`
- `Mathlib.Analysis.SpecialFunctions.ExpDeriv`

## Representative Declarations And Exports

- `hasGradientAt_expNegPotential_of_hasGradientAt`
- `gradient_expNegPotential_eq_of_hasGradientAt`
- `gradient_expNegPotential_coordinate_eq_of_hasGradientAt`
- `gradient_expNegPotential_eq_of_differentiableAt`
- `gradient_expNegPotential_coordinate_eq_of_differentiableAt`
- `continuous_gradient_of_contDiff_one`
- `fderiv_apply_eq_inner_of_hasGradientAt`
- `fderiv_apply_eq_inner_gradient_of_differentiableAt`
- `fderiv_apply_coordinate_eq_gradient_coordinate_of_differentiableAt`
- `hasGradientAt_coordinateUnit_hasLineDerivAt`

## Curated Formalized Memory Entries

- `analysis.calculus.gradient-exp-neg-potential-chain-rule` -> `hasGradientAt_expNegPotential_of_hasGradientAt` (Mathlib.Analysis.Calculus.Gradient.Basic; Mathlib.Analysis.SpecialFunctions.ExpDeriv)
- `analysis.calculus.gradient-exp-neg-potential-mathlib-gradient-from-hasGradientAt` -> `gradient_expNegPotential_eq_of_hasGradientAt` (Mathlib.Analysis.Calculus.Gradient.Basic; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient)
- `analysis.calculus.gradient-exp-neg-potential-coordinate-from-hasGradientAt` -> `gradient_expNegPotential_coordinate_eq_of_hasGradientAt` (AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient)
- `analysis.calculus.gradient-exp-neg-potential-mathlib-gradient` -> `gradient_expNegPotential_eq_of_differentiableAt` (Mathlib.Analysis.Calculus.Gradient.Basic; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient)
- `analysis.calculus.gradient-exp-neg-potential-coordinate` -> `gradient_expNegPotential_coordinate_eq_of_differentiableAt` (AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient)
- `analysis.calculus.continuous-gradient-of-contDiff-one` -> `continuous_gradient_of_contDiff_one` (Mathlib.Analysis.Calculus.ContDiff.Basic; Mathlib.Analysis.Calculus.Gradient.Basic)
- `analysis.calculus.gradient-coordinate-unit-line-derivative` -> `hasGradientAt_coordinateUnit_hasLineDerivAt` (Mathlib.Analysis.Calculus.Gradient.Basic; Mathlib.Analysis.Calculus.LineDeriv.Basic; AutoSamplingTheory.TechnicalLemmas.Geometry.EuclideanSpaceCoordinates)
- `analysis.calculus.fderiv-apply-eq-inner-of-hasGradientAt` -> `fderiv_apply_eq_inner_of_hasGradientAt` (Mathlib.Analysis.Calculus.Gradient.Basic; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient)
- `analysis.calculus.fderiv-apply-eq-inner-gradient` -> `fderiv_apply_eq_inner_gradient_of_differentiableAt` (Mathlib.Analysis.Calculus.Gradient.Basic; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient)
- `analysis.calculus.fderiv-coordinate-eq-gradient-coordinate` -> `fderiv_apply_coordinate_eq_gradient_coordinate_of_differentiableAt` (Mathlib.Analysis.Calculus.Gradient.Basic; Mathlib.Analysis.InnerProductSpace.PiL2; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient)

## Agent Usage

Search this card before inventing a nearby technical lemma.  If the needed fact
is generic and missing, create a Mathlib-ready leaf packet rather than hiding
the requirement inside a paper-specific theorem.
