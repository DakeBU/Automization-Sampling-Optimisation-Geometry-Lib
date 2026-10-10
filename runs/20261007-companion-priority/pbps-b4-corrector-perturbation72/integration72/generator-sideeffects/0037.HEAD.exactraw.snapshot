# AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence

- File: `AutoSamplingTheory/TechnicalLemmas/Analysis/Calculus/Divergence.lean`
- Layer: Mathlib-ready technical lemma
- Purpose: finite-dimensional pointwise coordinate-divergence convention, fderiv trace bridges, radial-cutoff PiLp derivative producer, smulRight basis-trace identity, the generic L1 cutoff-gradient limit and generic cutoff main-term dominated convergence for Integrable fields, a.e. trace transfer, finite-box signed face-term wrappers, and the inner-closed-Pi-box/outer-open-Pi-box plateau specialization
- Mathlib-quality status: preferred ANALYSIS/SDE bridge for finite-box cancellation and the compiled generic cutoff cross-term/main-term/tail limits; concrete compact-test generator-display integrability and Gibbs-tail convergence are compiled in Langevin, while whole-space IBP, no-boundary passage, and invariant law remain separate

## Imports

- `AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff`
- `AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.LineDeriv`
- `Mathlib.Analysis.Calculus.BumpFunction.FiniteDimension`
- `Mathlib.Analysis.Calculus.FDeriv.WithLp`
- `Mathlib.Analysis.Normed.Operator.BoundedLinearMaps`
- `Mathlib.MeasureTheory.Integral.DivergenceTheorem`

## Representative Declarations And Exports

- `coordinateDivergence`
- `coordinateDivergence_eq_sum_lineDeriv`
- `coordinateDivergence_eq_sum_fderiv_apply_of_hasFDerivAt`
- `coordinateDivergence_eq_sum_fderiv_apply_of_differentiableAt`
- `continuousLinearEquiv_apply_euclideanSpace_single`
- `hasFDerivAt_radialSmoothCutoff_comp_toLp`
- `tendsto_integral_norm_fderiv_radialSmoothCutoff_comp_toLp_apply`
- `tendsto_integral_radialSmoothCutoff_comp_toLp_smul`
- `tendsto_setIntegral_norm_norm_ge_comp_toLp`
- `sum_smulRight_apply_pi_single_eq_apply`
- `coordinateDivergence_wrapped_toPi_trace_of_hasFDerivAt`
- `eventuallyEq_restrict_Icc_of_eqOn_univ_pi_Ioo_diff_countable`
- `coordinateDivergence_wrapped_toPi_trace_ae_of_ae_hasFDerivAt`
- `coordinateDivergence_wrapped_toPi_trace_ae_of_hasFDerivAt_off_countable`
- `integrableOn_coordinateDivergence_wrapped_of_integrableOn_trace_of_hasFDerivAt_off_countable`
- `integral_coordinateDivergence_toPi_box_of_hasFDerivAt_off_countable`
- `integral_coordinateDivergence_toPi_box_of_integrableOn_trace_of_hasFDerivAt_off_countable`
- `signedFaceTermSum_eq_zero_of_boundary_component_eq_zero`
- `signedFaceTermSum_eq_zero_of_update_boundary_component_eq_zero`
- `update_boundary_component_eq_zero_of_eq_zero_off_univ_pi_Ioo`
- `signedFaceTermSum_eq_zero_of_eq_zero_off_univ_pi_Ioo`
- `eq_zero_off_univ_pi_Ioo_of_support_subset_univ_pi_Ioo`
- `exists_contDiff_cutoff_tsupport_subset_univ_pi_Ioo`
- `support_subset_univ_pi_Ioo_of_tsupport_subset_univ_pi_Ioo`
- `exists_contDiff_cutoff_support_subset_univ_pi_Ioo`
- `exists_contDiff_support_eq_univ_pi_Ioo`
- `positive_on_univ_pi_Ioo_of_support_eq_univ_pi_Ioo`
- `Icc_subset_univ_pi_Ioo_of_strict_bounds`
- `exists_contDiff_cutoff_eq_one_on_Icc_tsupport_subset_outer_univ_pi_Ioo`
- `exists_contDiff_cutoff_support_subset_outer_univ_pi_Ioo_of_mem_Icc`
- `signedFaceTermSum_eq_zero_of_support_subset_univ_pi_Ioo`
- `support_smul_subset_univ_pi_Ioo_of_eq_zero_off_univ_pi_Ioo`
- `support_smul_subset_univ_pi_Ioo_of_scalar_support_subset_univ_pi_Ioo`
- `support_smul_subset_univ_pi_Ioo_of_scalar_tsupport_subset_univ_pi_Ioo`
- `continuousOn_smul_vectorField_of_continuousOn`
- `hasFDerivAt_smul_vectorField_of_hasFDerivAt`
- `hasFDerivAt_smul_vectorField_off_countable`
- `continuousOn_smul_vectorField_trace_of_component_continuousOn`
- `continuousOn_smul_vectorField_trace_of_components`
- `integrableOn_smul_vectorField_trace_of_continuousOn`

## Curated Formalized Memory Entries

- `analysis.calculus.exists-contDiff-cutoff-eq-one-on-Icc-tsupport-subset-outer-univ-pi-Ioo` -> `exists_contDiff_cutoff_eq_one_on_Icc_tsupport_subset_outer_univ_pi_Ioo` (AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence)
- `analysis.calculus.coordinate-divergence-sum-lineDeriv` -> `coordinateDivergence_eq_sum_lineDeriv` (AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence; Mathlib.Analysis.BoxIntegral.DivergenceTheorem pointwise summand shape)
- `analysis.calculus.coordinate-divergence-fderiv-trace-sum` -> `coordinateDivergence_eq_sum_fderiv_apply_of_hasFDerivAt` (Mathlib.Analysis.Calculus.LineDeriv.Basic; Mathlib.Analysis.Normed.Lp.PiLp; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence)
- `analysis.calculus.coordinate-divergence-fderiv-default-summand` -> `coordinateDivergence_eq_sum_fderiv_apply_of_differentiableAt` (AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence; Mathlib.MeasureTheory.Integral.DivergenceTheorem summand shape)
- `analysis.calculus.withlp-continuousLinearEquiv-euclidean-single` -> `continuousLinearEquiv_apply_euclideanSpace_single` (Mathlib.Analysis.Calculus.FDeriv.WithLp; Mathlib.Analysis.Normed.Lp.PiLp)
- `analysis.calculus.radial-smooth-cutoff-comp-toLp-hasFDerivAt` -> `hasFDerivAt_radialSmoothCutoff_comp_toLp` (Mathlib.Analysis.Calculus.FDeriv.WithLp; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff)
- `analysis.calculus.pilp-radial-cutoff-gradient-L1-tendsto-zero` -> `tendsto_integral_norm_fderiv_radialSmoothCutoff_comp_toLp_apply` (AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.{Cutoff,Divergence}; Mathlib.MeasureTheory.Integral.DominatedConvergence)
- `analysis.calculus.pilp-radial-cutoff-main-integral-tendsto` -> `tendsto_integral_radialSmoothCutoff_comp_toLp_smul` (AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.{Cutoff,Divergence}; Mathlib.MeasureTheory.Integral.DominatedConvergence)
- `analysis.calculus.pilp-integrable-field-norm-tail-tendsto-zero` -> `tendsto_setIntegral_norm_norm_ge_comp_toLp` (Mathlib.MeasureTheory.Integral.Bochner.Set; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence)
- `analysis.calculus.compact-support-whole-space-coordinate-divergence-zero` -> `integral_coordinateDivergence_wrapped_eq_zero_of_contDiff_of_hasCompactSupport` (Mathlib.MeasureTheory.Integral.DivergenceTheorem; Mathlib.Topology.MetricSpace.Bounded; Mathlib.MeasureTheory.Integral.Bochner.Set; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence)
- `analysis.calculus.sum-smulRight-apply-pi-single-eq-apply` -> `sum_smulRight_apply_pi_single_eq_apply` (Mathlib.Algebra.BigOperators.Pi; Mathlib.Topology.Algebra.Module.FiniteDimension)
- `analysis.calculus.coordinate-divergence-wrapped-toPi-trace` -> `coordinateDivergence_wrapped_toPi_trace_of_hasFDerivAt` (Mathlib.Analysis.Calculus.FDeriv.WithLp; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence)
- `analysis.calculus.eventuallyEq-restrict-Icc-open-box-diff-countable` -> `eventuallyEq_restrict_Icc_of_eqOn_univ_pi_Ioo_diff_countable` (Mathlib.MeasureTheory.Integral.DivergenceTheorem; Mathlib.MeasureTheory.Constructions.Polish.Basic)
- `analysis.calculus.coordinate-divergence-wrapped-toPi-trace-ae` -> `coordinateDivergence_wrapped_toPi_trace_ae_of_ae_hasFDerivAt` (AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence)
- `analysis.calculus.coordinate-divergence-wrapped-toPi-trace-ae-off-countable` -> `coordinateDivergence_wrapped_toPi_trace_ae_of_hasFDerivAt_off_countable` (AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence; Mathlib.MeasureTheory.Integral.DivergenceTheorem)
- `analysis.calculus.integrableOn-coordinate-divergence-wrapped-of-trace` -> `integrableOn_coordinateDivergence_wrapped_of_integrableOn_trace_of_hasFDerivAt_off_countable` (Mathlib.MeasureTheory.Integral.IntegrableOn; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence)
- `analysis.calculus.integral-coordinate-divergence-toPi-box-trace-integrable` -> `integral_coordinateDivergence_toPi_box_of_integrableOn_trace_of_hasFDerivAt_off_countable` (Mathlib.MeasureTheory.Integral.DivergenceTheorem; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence)
- `analysis.calculus.integral-coordinate-divergence-toPi-box-zero-face` -> `integral_coordinateDivergence_toPi_box_eq_zero_of_integrableOn_trace_of_hasFDerivAt_off_countable` (AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence)
- `analysis.calculus.signed-face-term-sum-zero-of-boundary-component-zero` -> `signedFaceTermSum_eq_zero_of_boundary_component_eq_zero` (AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence)
- `analysis.calculus.integral-coordinate-divergence-toPi-box-zero-boundary-component` -> `integral_coordinateDivergence_toPi_box_eq_zero_of_boundary_component_eq_zero` (AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence)
- `analysis.calculus.signed-face-term-sum-zero-of-update-boundary-component-zero` -> `signedFaceTermSum_eq_zero_of_update_boundary_component_eq_zero` (AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence)
- `analysis.calculus.integral-coordinate-divergence-toPi-box-zero-update-boundary-component` -> `integral_coordinateDivergence_toPi_box_eq_zero_of_update_boundary_component_eq_zero` (AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence)
- `analysis.calculus.update-boundary-component-zero-of-eq-zero-off-univ-pi-Ioo` -> `update_boundary_component_eq_zero_of_eq_zero_off_univ_pi_Ioo` (AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence)
- `analysis.calculus.signed-face-term-sum-zero-of-eq-zero-off-univ-pi-Ioo` -> `signedFaceTermSum_eq_zero_of_eq_zero_off_univ_pi_Ioo` (AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence)
- `analysis.calculus.integral-coordinate-divergence-toPi-box-zero-off-univ-pi-Ioo` -> `integral_coordinateDivergence_toPi_box_eq_zero_of_eq_zero_off_univ_pi_Ioo` (AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence)
- `analysis.calculus.eq-zero-off-univ-pi-Ioo-of-support-subset-univ-pi-Ioo` -> `eq_zero_off_univ_pi_Ioo_of_support_subset_univ_pi_Ioo` (AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence)
- `analysis.calculus.exists-contDiff-cutoff-tsupport-subset-univ-pi-Ioo` -> `exists_contDiff_cutoff_tsupport_subset_univ_pi_Ioo` (Mathlib.Analysis.Calculus.BumpFunction.FiniteDimension; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence)
- `analysis.calculus.support-subset-univ-pi-Ioo-of-tsupport-subset-univ-pi-Ioo` -> `support_subset_univ_pi_Ioo_of_tsupport_subset_univ_pi_Ioo` (Mathlib.Topology.Support; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence)
- `analysis.calculus.exists-contDiff-cutoff-support-subset-univ-pi-Ioo` -> `exists_contDiff_cutoff_support_subset_univ_pi_Ioo` (Mathlib.Analysis.Calculus.BumpFunction.FiniteDimension; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence)
- `analysis.calculus.exists-contDiff-support-eq-univ-pi-Ioo` -> `exists_contDiff_support_eq_univ_pi_Ioo` (Mathlib.Analysis.Calculus.BumpFunction.FiniteDimension; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence)
- `analysis.calculus.positive-on-univ-pi-Ioo-of-support-eq-univ-pi-Ioo` -> `positive_on_univ_pi_Ioo_of_support_eq_univ_pi_Ioo` (Mathlib.Topology.Support; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence)
- `analysis.calculus.Icc-subset-univ-pi-Ioo-of-forall-lt` -> `Icc_subset_univ_pi_Ioo_of_strict_bounds` (AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence)
- `analysis.calculus.exists-contDiff-cutoff-support-subset-outer-univ-pi-Ioo-of-mem-Icc` -> `exists_contDiff_cutoff_support_subset_outer_univ_pi_Ioo_of_mem_Icc` (Mathlib.Analysis.Calculus.BumpFunction.FiniteDimension; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence)
- `analysis.calculus.signed-face-term-sum-zero-of-support-subset-univ-pi-Ioo` -> `signedFaceTermSum_eq_zero_of_support_subset_univ_pi_Ioo` (AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence)
- `analysis.calculus.integral-coordinate-divergence-toPi-box-zero-support-subset-univ-pi-Ioo` -> `integral_coordinateDivergence_toPi_box_eq_zero_of_support_subset_univ_pi_Ioo` (AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence)
- `analysis.calculus.support-smul-subset-univ-pi-Ioo-of-cutoff-eq-zero-off-univ-pi-Ioo` -> `support_smul_subset_univ_pi_Ioo_of_eq_zero_off_univ_pi_Ioo` (AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence)
- `analysis.calculus.support-smul-subset-univ-pi-Ioo-of-scalar-support-subset-univ-pi-Ioo` -> `support_smul_subset_univ_pi_Ioo_of_scalar_support_subset_univ_pi_Ioo` (AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence)
- `analysis.calculus.support-smul-subset-univ-pi-Ioo-of-scalar-tsupport-subset-univ-pi-Ioo` -> `support_smul_subset_univ_pi_Ioo_of_scalar_tsupport_subset_univ_pi_Ioo` (Mathlib.Topology.Support; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence)
- `analysis.calculus.continuousOn-smul-vectorField-of-continuousOn` -> `continuousOn_smul_vectorField_of_continuousOn` (Mathlib.Topology.Algebra.Module.Basic; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence)
- `analysis.calculus.hasFDerivAt-smul-vectorField-of-hasFDerivAt` -> `hasFDerivAt_smul_vectorField_of_hasFDerivAt` (Mathlib.Analysis.Calculus.FDeriv.Basic; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence)
- `analysis.calculus.hasFDerivAt-smul-vectorField-off-countable` -> `hasFDerivAt_smul_vectorField_off_countable` (AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence)
- `analysis.calculus.signed-face-term-sum-smul-zero-of-cutoff-eq-zero-off-univ-pi-Ioo` -> `signedFaceTermSum_smul_eq_zero_of_cutoff_eq_zero_off_univ_pi_Ioo` (AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence)
- `analysis.calculus.signed-face-term-sum-smul-zero-of-scalar-support-subset-univ-pi-Ioo` -> `signedFaceTermSum_smul_eq_zero_of_scalar_support_subset_univ_pi_Ioo` (AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence)
- `analysis.calculus.signed-face-term-sum-smul-zero-of-scalar-tsupport-subset-univ-pi-Ioo` -> `signedFaceTermSum_smul_eq_zero_of_scalar_tsupport_subset_univ_pi_Ioo` (Mathlib.Topology.Support; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence)
- `analysis.calculus.integral-coordinate-divergence-toPi-box-zero-cutoff-eq-zero-off-univ-pi-Ioo` -> `integral_coordinateDivergence_toPi_box_eq_zero_of_cutoff_eq_zero_off_univ_pi_Ioo` (AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence)
- `analysis.calculus.integral-coordinate-divergence-toPi-box-zero-scalar-support-subset-univ-pi-Ioo` -> `integral_coordinateDivergence_toPi_box_eq_zero_of_scalar_support_subset_univ_pi_Ioo` (AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence)
- `analysis.calculus.integral-coordinate-divergence-toPi-box-zero-scalar-tsupport-subset-univ-pi-Ioo` -> `integral_coordinateDivergence_toPi_box_eq_zero_of_scalar_tsupport_subset_univ_pi_Ioo` (Mathlib.Topology.Support; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence)
- `analysis.calculus.integral-coordinate-divergence-toPi-box-zero-cutoff-eq-zero-off-univ-pi-Ioo-regularity` -> `integral_coordinateDivergence_toPi_box_eq_zero_of_cutoff_eq_zero_off_univ_pi_Ioo_of_regularity` (AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence)
- `analysis.calculus.integral-coordinate-divergence-toPi-box-zero-scalar-support-subset-univ-pi-Ioo-regularity` -> `integral_coordinateDivergence_toPi_box_eq_zero_of_scalar_support_subset_univ_pi_Ioo_of_regularity` (AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence)
- `analysis.calculus.integral-coordinate-divergence-toPi-box-zero-scalar-support-subset-univ-pi-Ioo-fderiv` -> `integral_coordinateDivergence_toPi_box_eq_zero_of_scalar_support_subset_univ_pi_Ioo_of_fderiv` (AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence)
- `analysis.calculus.integrableOn-smul-vectorField-trace-of-continuousOn` -> `integrableOn_smul_vectorField_trace_of_continuousOn` (Mathlib.MeasureTheory.Integral.Bochner.Basic; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence)
- `analysis.calculus.integral-coordinate-divergence-toPi-box-zero-cutoff-eq-zero-off-univ-pi-Ioo-trace-continuous` -> `integral_coordinateDivergence_toPi_box_eq_zero_of_cutoff_eq_zero_off_univ_pi_Ioo_of_trace_continuous` (AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence)
- `analysis.calculus.integral-coordinate-divergence-toPi-box-zero-scalar-support-subset-univ-pi-Ioo-trace-continuous` -> `integral_coordinateDivergence_toPi_box_eq_zero_of_scalar_support_subset_univ_pi_Ioo_of_trace_continuous` (AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence)
- `analysis.calculus.continuousOn-smul-vectorField-trace-of-component-continuousOn` -> `continuousOn_smul_vectorField_trace_of_component_continuousOn` (Mathlib.Topology.Algebra.Group.Basic; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence)
- `analysis.calculus.continuousOn-smul-vectorField-trace-of-components` -> `continuousOn_smul_vectorField_trace_of_components` (Mathlib.Analysis.Normed.Operator.BoundedLinearMaps; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence)
- `analysis.calculus.integral-coordinate-divergence-toPi-box-zero-cutoff-eq-zero-off-univ-pi-Ioo-component-continuous` -> `integral_coordinateDivergence_toPi_box_eq_zero_of_cutoff_eq_zero_off_univ_pi_Ioo_of_component_continuous` (AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence)
- `analysis.calculus.integral-coordinate-divergence-toPi-box-zero-scalar-support-subset-univ-pi-Ioo-component-continuous` -> `integral_coordinateDivergence_toPi_box_eq_zero_of_scalar_support_subset_univ_pi_Ioo_of_component_continuous` (AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence)
- `analysis.calculus.integral-coordinate-divergence-toPi-box` -> `integral_coordinateDivergence_toPi_box_of_hasFDerivAt_off_countable` (Mathlib.MeasureTheory.Integral.DivergenceTheorem; AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Divergence)

## Agent Usage

Search this card before inventing a nearby technical lemma.  If the needed fact
is generic and missing, create a Mathlib-ready leaf packet rather than hiding
the requirement inside a paper-specific theorem.
