# AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff

- File: `AutoSamplingTheory/TechnicalLemmas/Analysis/Calculus/Cutoff.lean`
- Layer: Mathlib-ready technical lemma
- Purpose: smooth unit and radial cutoffs, range bounds, support control, compact support, pointwise exhaustion, compact-in-open plateaus, scale-uniform radial first-derivative control, and closed outer-region totalized-fderiv vanishing
- Mathlib-quality status: compiled ANALYSIS/REG/SDE base through O(R^-1) fderiv and O(R^-2) second iterated derivative; the finite-dimensional Laplacian trace consumer is compiled in Laplacian

## Imports

- `Mathlib.Analysis.Calculus.BumpFunction.FiniteDimension`
- `Mathlib.Analysis.Calculus.LocalExtr.Basic`

## Representative Declarations And Exports

- `smoothUnitCutoff`
- `smoothUnitCutoff_eq_smoothTransition`
- `smoothUnitCutoff_contDiff`
- `smoothUnitCutoff_eq_one_of_abs_le_one`
- `smoothUnitCutoff_eq_zero_of_two_le_abs`
- `smoothUnitCutoff_mem_Icc`
- `smoothUnitCutoff_deriv_bounded`
- `radialSmoothCutoff`
- `radialSmoothCutoff_eq_one_of_norm_le`
- `radialSmoothCutoff_eq_zero_of_two_mul_le_norm`
- `radialSmoothCutoff_mem_Icc`
- `fderiv_norm_div_bound`
- `radialSmoothCutoff_contDiff`
- `radialSmoothCutoff_fderiv_bound`
- `radialSmoothCutoff_fderiv_eq_zero_of_two_mul_le_norm`
- `radialSmoothCutoff_support_subset_closedBall`
- `radialSmoothCutoff_tsupport_subset_closedBall`
- `radialSmoothCutoff_hasCompactSupport`
- `radialSmoothCutoff_tendsto_one`
- `exists_contDiff_eq_one_tsupport_subset`

## Curated Formalized Memory Entries

- `analysis.calculus.smooth-unit-cutoff-eq-smoothTransition` -> `smoothUnitCutoff_eq_smoothTransition` (SLT/GaussianSobolevDense/Defs.lean@d0f506f; Mathlib.Analysis.Calculus.BumpFunction.InnerProduct)
- `analysis.calculus.smooth-unit-cutoff-contDiff` -> `smoothUnitCutoff_contDiff` (SLT/GaussianSobolevDense/Defs.lean@d0f506f; Mathlib.Analysis.Calculus.BumpFunction.InnerProduct)
- `analysis.calculus.smooth-unit-cutoff-one-of-abs-le-one` -> `smoothUnitCutoff_eq_one_of_abs_le_one` (SLT/GaussianSobolevDense/Defs.lean@d0f506f; Mathlib.Analysis.SpecialFunctions.SmoothTransition)
- `analysis.calculus.smooth-unit-cutoff-zero-of-two-le-abs` -> `smoothUnitCutoff_eq_zero_of_two_le_abs` (SLT/GaussianSobolevDense/Defs.lean@d0f506f; Mathlib.Analysis.SpecialFunctions.SmoothTransition)
- `analysis.calculus.smooth-unit-cutoff-mem-Icc` -> `smoothUnitCutoff_mem_Icc` (Mathlib.Analysis.Calculus.BumpFunction.InnerProduct)
- `analysis.calculus.smooth-unit-cutoff-deriv-bounded` -> `smoothUnitCutoff_deriv_bounded` (SLT/GaussianSobolevDense/Cutoff.lean@d0f506f; Mathlib.Analysis.Calculus.ContDiff.Deriv)
- `analysis.calculus.radial-smooth-cutoff-one-of-norm-le` -> `radialSmoothCutoff_eq_one_of_norm_le` (SLT/GaussianSobolevDense/Defs.lean@d0f506f)
- `analysis.calculus.radial-smooth-cutoff-zero-of-two-mul-le-norm` -> `radialSmoothCutoff_eq_zero_of_two_mul_le_norm` (SLT/GaussianSobolevDense/Defs.lean@d0f506f)
- `analysis.calculus.radial-smooth-cutoff-mem-Icc` -> `radialSmoothCutoff_mem_Icc` (SLT/GaussianSobolevDense/Defs.lean@d0f506f)
- `analysis.calculus.fderiv-norm-div-bound` -> `fderiv_norm_div_bound` (SLT/GaussianSobolevDense/Cutoff.lean@d0f506f; Mathlib.Analysis.Calculus.Deriv.Basic)
- `analysis.calculus.radial-smooth-cutoff-contDiff` -> `radialSmoothCutoff_contDiff` (SLT/GaussianSobolevDense/Defs.lean@d0f506f; Mathlib.Analysis.Calculus.BumpFunction.InnerProduct)
- `analysis.calculus.radial-smooth-cutoff-fderiv-bound` -> `radialSmoothCutoff_fderiv_bound` (SLT/GaussianSobolevDense/Cutoff.lean@d0f506f; Mathlib.Analysis.Calculus.FDeriv.Comp)
- `analysis.calculus.radial-smooth-cutoff-fderiv-zero-of-two-mul-le-norm` -> `radialSmoothCutoff_fderiv_eq_zero_of_two_mul_le_norm` (Mathlib.Analysis.Calculus.LocalExtr.Basic; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff)
- `analysis.calculus.radial-smooth-cutoff-support-subset-closedBall` -> `radialSmoothCutoff_support_subset_closedBall` (SLT/GaussianSobolevDense/Defs.lean@d0f506f)
- `analysis.calculus.radial-smooth-cutoff-tsupport-subset-closedBall` -> `radialSmoothCutoff_tsupport_subset_closedBall` (AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff)
- `analysis.calculus.radial-smooth-cutoff-hasCompactSupport` -> `radialSmoothCutoff_hasCompactSupport` (SLT/GaussianSobolevDense/Defs.lean@d0f506f)
- `analysis.calculus.radial-smooth-cutoff-tendsto-one` -> `radialSmoothCutoff_tendsto_one` (SLT/GaussianSobolevDense/Defs.lean@d0f506f)
- `analysis.calculus.exists-contDiff-eq-one-tsupport-subset` -> `exists_contDiff_eq_one_tsupport_subset` (Mathlib.Topology.Compactness.LocallyCompact; Mathlib.Analysis.Calculus.BumpFunction.FiniteDimension; Mathlib.Topology.Order.Compact; Mathlib.Analysis.SpecialFunctions.SmoothTransition)

## Agent Usage

Search this card before inventing a nearby technical lemma.  If the needed fact
is generic and missing, create a Mathlib-ready leaf packet rather than hiding
the requirement inside a paper-specific theorem.
