# AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHazardClock

- File: `AutoSamplingTheory\ExampleCases\ProximalBPS\ActualHazardClock.lean`
- Layer: uncategorized
- Purpose:
- Mathlib-quality status:

## Imports

- `AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHarmonicFlow`
- `AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBounceRate`
- `Mathlib.MeasureTheory.Integral.DominatedConvergence`
- `Mathlib.Probability.Process.HittingTime`
- `Mathlib.Probability.Distributions.Exponential`
- `Mathlib.MeasureTheory.Constructions.BorelSpace.Order`

## Representative Declarations And Exports

- `actual_integrated_hazard_clock_statement`
- `actual_hazard_primitive_laws`
- `actual_integrated_hazard_clock_laws`

## Curated Formalized Memory Entries

- `pbps.actualHazardClock` -> `actual_integrated_hazard_clock_laws` (arXiv2609.06905v1 Algorithm1 and AppendixA1 equation(A1))

## Agent Usage

Search this card before inventing a nearby technical lemma.  If the needed fact
is generic and missing, create a Mathlib-ready leaf packet rather than hiding
the requirement inside a paper-specific theorem.
