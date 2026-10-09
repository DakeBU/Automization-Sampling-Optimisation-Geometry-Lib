# AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin

- File: `AutoSamplingTheory/TechnicalLemmas/StochasticProcesses/Langevin.lean`
- Layer: Mathlib-ready technical lemma
- Purpose: finite-dimensional pointwise display for the formal differential expression `Δ f - <∇V, ∇f>`, supplied coordinate-to-Mathlib weighted-divergence handoffs, `exp(-V)` handoffs, coordinate-sum and coordinateDivergence displays, finite-box trace regularity, whole-space Gibbs-weighted source-field and compact-test generator-display integrability, and Gibbs-tail convergence
- Mathlib-quality status: preferred Mathlib-style location for Langevin expression algebra and the compiled source-field, compact-test generator-display, and Gibbs-tail leaves before IBP, invariant-law, Ito-generator, and semigroup-domain contracts

## Imports

- `AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence`
- `AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient`
- `AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Laplacian`
- `AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.LineDeriv`
- `AutoSamplingTheory.TechnicalLemmas.Geometry.EuclideanSpaceCoordinates`
- `Mathlib.Analysis.InnerProductSpace.Basic`
- `Mathlib.Analysis.SpecialFunctions.ExpDeriv`
- `Mathlib.Analysis.Calculus.Deriv.Mul`
- `Mathlib.Algebra.BigOperators.Fin`
- `Mathlib.Tactic.Ring`

## Representative Declarations And Exports

- `hasDerivAt_gibbsWeight_mul_testDeriv_eq_langevinGenerator_1d`
- `deriv_gibbsWeight_mul_testDeriv_eq_langevinGenerator_1d`
- `weightedDivergence_gibbsWeight_langevinGenerator_algebra`
- `expNeg_weightedDivergence_langevinGenerator_algebra`
- `finiteCoord_weightedDivergence_langevinGenerator_algebra`
- `finiteCoord_named_weightedDivergence_langevinGenerator_algebra`
- `finiteCoord_toLpInner_weightedDivergence_langevinGenerator_algebra`
- `finiteCoord_euclideanInner_weightedDivergence_langevinGenerator_algebra`
- `finiteEuclidean_langevinGenerator_basisDisplay`
- `finiteEuclidean_langevinGenerator_coordinateDisplay`
- `finiteEuclidean_weightedDivergence_langevinGenerator_basisHandoff`
- `finiteEuclidean_weightedDivergence_langevinGenerator_coordinateHandoff`
- `finiteEuclidean_expNeg_weightedDivergence_langevinGenerator_basisHandoff`
- `finiteEuclidean_expNeg_weightedDivergence_langevinGenerator_coordinateHandoff`
- `finiteEuclidean_expNeg_lineDeriv_fderiv_coordinateSum_langevinGenerator_display`
- `finiteEuclidean_expNeg_lineDeriv_fderiv_coordinateSum_langevinGenerator_display_of_differentiableAt`
- `coordinateDivergence_expNeg_fderivCoordinateField_langevinGenerator_display_of_differentiableAt`
- `trace_expNeg_fderivCoordinateField_langevinGenerator_display_of_hasFDerivAt`
- `continuousOn_expNeg_langevinGenerator_rhs_of_components`
- `continuousOn_expNeg_langevinGenerator_rhs_of_contDiff`
- `hasFDerivAt_expNeg_fderivCoordinateField_of_differentiableAt`
- `hasFDerivAt_expNeg_fderivCoordinateField_of_contDiff`
- `integrableOn_trace_expNeg_fderivCoordinateField_of_continuousOn`
- `integrableOn_trace_expNeg_fderivCoordinateField_of_component_continuousOn`
- `integrableOn_trace_expNeg_fderivCoordinateField_of_contDiff`
- `integrableOn_trace_expNeg_fderivCoordinateField_of_contDiff_fderiv`
- `integrable_expNeg_langevinGenerator_rhs_of_contDiff_of_hasCompactSupport`
- `integrable_expNeg_langevinGenerator_rhs_comp_toLp_of_contDiff_of_hasCompactSupport`
- `integrable_expNeg_comp_toLp_of_lintegral_expNeg_ne_top`
- `tendsto_setIntegral_expNeg_norm_ge_comp_toLp_of_lintegral_expNeg_ne_top`
- `integral_expNeg_langevinGenerator_rhs_eq_zero_of_contDiff_of_hasCompactSupport`
- `integrable_expNeg_fderivCoordinateField_of_lintegral_expNeg_ne_top_of_fderiv_norm_le`

## Curated Formalized Memory Entries

- `langevin.gibbs-weighted-generator-hasDerivAt-1d` -> `hasDerivAt_gibbsWeight_mul_testDeriv_eq_langevinGenerator_1d` (Mathlib.Analysis.SpecialFunctions.ExpDeriv; Mathlib.Analysis.Calculus.Deriv.Mul)
- `langevin.gibbs-weighted-generator-deriv-1d` -> `deriv_gibbsWeight_mul_testDeriv_eq_langevinGenerator_1d` (AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin)
- `langevin.gibbs-weighted-divergence-generator-algebra` -> `weightedDivergence_gibbsWeight_langevinGenerator_algebra` (AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin; Mathlib.Analysis.InnerProductSpace.Basic)
- `langevin.exp-neg-weighted-divergence-generator-algebra` -> `expNeg_weightedDivergence_langevinGenerator_algebra` (AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin)
- `langevin.finite-coordinate-weighted-divergence-generator-algebra` -> `finiteCoord_weightedDivergence_langevinGenerator_algebra` (AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin; Mathlib.Algebra.BigOperators.Fin)
- `langevin.finite-coordinate-named-weighted-divergence-generator-algebra` -> `finiteCoord_named_weightedDivergence_langevinGenerator_algebra` (AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin)
- `langevin.finite-coordinate-toLp-inner-weighted-divergence-generator-algebra` -> `finiteCoord_toLpInner_weightedDivergence_langevinGenerator_algebra` (AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin; AutoSamplingTheory.TechnicalLemmas.Geometry.EuclideanSpaceCoordinates)
- `langevin.finite-coordinate-euclidean-inner-weighted-divergence-generator-algebra` -> `finiteCoord_euclideanInner_weightedDivergence_langevinGenerator_algebra` (AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin; AutoSamplingTheory.TechnicalLemmas.Geometry.EuclideanSpaceCoordinates)
- `langevin.finite-euclidean-generator-basis-display` -> `finiteEuclidean_langevinGenerator_basisDisplay` (Mathlib.Analysis.InnerProductSpace.Laplacian; AutoSamplingTheory.TechnicalLemmas.Geometry.EuclideanSpaceCoordinates)
- `langevin.finite-euclidean-generator-coordinate-display` -> `finiteEuclidean_langevinGenerator_coordinateDisplay` (AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin; Mathlib.Analysis.InnerProductSpace.PiL2)
- `langevin.finite-euclidean-weighted-divergence-basis-handoff` -> `finiteEuclidean_weightedDivergence_langevinGenerator_basisHandoff` (AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin)
- `langevin.finite-euclidean-weighted-divergence-coordinate-handoff` -> `finiteEuclidean_weightedDivergence_langevinGenerator_coordinateHandoff` (AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin)
- `langevin.finite-euclidean-exp-neg-weighted-divergence-basis-handoff` -> `finiteEuclidean_expNeg_weightedDivergence_langevinGenerator_basisHandoff` (AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient)
- `langevin.finite-euclidean-exp-neg-weighted-divergence-coordinate-handoff` -> `finiteEuclidean_expNeg_weightedDivergence_langevinGenerator_coordinateHandoff` (AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient)
- `langevin.finite-euclidean-exp-neg-lineDeriv-fderiv-coordinate-sum-display` -> `finiteEuclidean_expNeg_lineDeriv_fderiv_coordinateSum_langevinGenerator_display` (AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.LineDeriv; AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin)
- `langevin.finite-euclidean-exp-neg-lineDeriv-fderiv-coordinate-sum-display-differentiable` -> `finiteEuclidean_expNeg_lineDeriv_fderiv_coordinateSum_langevinGenerator_display_of_differentiableAt` (AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient; AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin)
- `langevin.coordinate-divergence-exp-neg-fderiv-display` -> `coordinateDivergence_expNeg_fderivCoordinateField_langevinGenerator_display_of_differentiableAt` (AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence; AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin)
- `langevin.trace-exp-neg-fderiv-coordinate-field-display` -> `trace_expNeg_fderivCoordinateField_langevinGenerator_display_of_hasFDerivAt` (AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence; AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin)
- `langevin.integrableOn-trace-exp-neg-fderiv-coordinate-field-continuous` -> `integrableOn_trace_expNeg_fderivCoordinateField_of_continuousOn` (Mathlib.MeasureTheory.Function.LocallyIntegrable; Mathlib.MeasureTheory.Integral.IntegrableOn; AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin)
- `langevin.continuousOn-exp-neg-generator-rhs-components` -> `continuousOn_expNeg_langevinGenerator_rhs_of_components` (Mathlib.Analysis.SpecialFunctions.Exp; Mathlib.Analysis.InnerProductSpace.Continuous; AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin)
- `langevin.integrableOn-trace-exp-neg-fderiv-coordinate-field-components` -> `integrableOn_trace_expNeg_fderivCoordinateField_of_component_continuousOn` (AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin)
- `langevin.continuousOn-exp-neg-generator-rhs-contDiff` -> `continuousOn_expNeg_langevinGenerator_rhs_of_contDiff` (AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Laplacian)
- `langevin.integrableOn-trace-exp-neg-fderiv-coordinate-field-contDiff` -> `integrableOn_trace_expNeg_fderivCoordinateField_of_contDiff` (AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin)
- `langevin.hasFDerivAt-exp-neg-fderiv-coordinate-field-contDiff` -> `hasFDerivAt_expNeg_fderivCoordinateField_of_contDiff` (Mathlib.Analysis.Calculus.FDeriv.Prod; Mathlib.Analysis.Calculus.FDeriv.WithLp; Mathlib.Analysis.SpecialFunctions.ExpDeriv; AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin)
- `langevin.integrableOn-trace-exp-neg-fderiv-coordinate-field-contDiff-fderiv` -> `integrableOn_trace_expNeg_fderivCoordinateField_of_contDiff_fderiv` (AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin)
- `langevin.integrable-exp-neg-fderiv-coordinate-source-field` -> `integrable_expNeg_fderivCoordinateField_of_lintegral_expNeg_ne_top_of_fderiv_norm_le` (Mathlib.MeasureTheory.Function.L1Space.Integrable; Mathlib.MeasureTheory.Measure.Haar.InnerProductSpace; AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin)
- `langevin.integrable-exp-neg-generator-rhs-compact-test` -> `integrable_expNeg_langevinGenerator_rhs_of_contDiff_of_hasCompactSupport` (Mathlib.MeasureTheory.Function.LocallyIntegrable; Mathlib.Analysis.Calculus.FDeriv.Const; Mathlib.Analysis.InnerProductSpace.Laplacian; AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin)
- `langevin.integrable-exp-neg-generator-rhs-compact-test-raw-pi` -> `integrable_expNeg_langevinGenerator_rhs_comp_toLp_of_contDiff_of_hasCompactSupport` (Mathlib.MeasureTheory.Measure.Haar.InnerProductSpace; AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin)
- `langevin.integrable-exp-neg-weight-raw-pi` -> `integrable_expNeg_comp_toLp_of_lintegral_expNeg_ne_top` (Mathlib.MeasureTheory.Function.L1Space.Integrable; Mathlib.MeasureTheory.Measure.Haar.InnerProductSpace; AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin)
- `langevin.gibbs-weight-tail-tendsto-zero-raw-pi` -> `tendsto_setIntegral_expNeg_norm_ge_comp_toLp_of_lintegral_expNeg_ne_top` (AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence)
- `langevin.whole-space-gibbs-weighted-generator-ibp-compact-test` -> `integral_expNeg_langevinGenerator_rhs_eq_zero_of_contDiff_of_hasCompactSupport` (AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence; AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.Langevin; Mathlib.MeasureTheory.Measure.Haar.InnerProductSpace)

## Agent Usage

Search this card before inventing a nearby technical lemma.  If the needed fact
is generic and missing, create a Mathlib-ready leaf packet rather than hiding
the requirement inside a paper-specific theorem.
