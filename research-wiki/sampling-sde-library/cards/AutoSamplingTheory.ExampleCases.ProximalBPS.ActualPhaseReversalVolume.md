# AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhaseReversalVolume

- File: `AutoSamplingTheory\ExampleCases\ProximalBPS\ActualPhaseReversalVolume.lean`
- Layer: uncategorized
- Purpose:
- Mathlib-quality status:

## Imports

- `AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHarmonicFlow`
- `AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBounceRate`
- `Mathlib.MeasureTheory.Measure.Haar.InnerProductSpace`
- `Mathlib.MeasureTheory.Group.Prod`
- `Mathlib.MeasureTheory.Integral.Bochner.Basic`
- `Mathlib.Tactic.Module`
- `Mathlib.Tactic.FieldSimp`
- `Mathlib.Tactic.Ring`

## Representative Declarations And Exports

- `actual_phase_reversal_volume_statement`
- `lower_shear`
- `upper_shear`
- `negate_phase`
- `reflect_fiber`
- `area_matrix`
- `harmonic_linear`
- `translate_position`
- `harmonic_affine`
- `actual_phase_reversal_volume_laws`

## Curated Formalized Memory Entries

- `pbps.actualPhaseReversalVolume` -> `actual_phase_reversal_volume_laws` (arXiv2609.06905v1 Appendix A1 flow A5 A6 and elementary A8 mechanics)

## Agent Usage

Search this card before inventing a nearby technical lemma.  If the needed fact
is generic and missing, create a Mathlib-ready leaf packet rather than hiding
the requirement inside a paper-specific theorem.
