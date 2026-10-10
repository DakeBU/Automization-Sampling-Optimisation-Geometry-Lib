# AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHarmonicFlow

- File: `AutoSamplingTheory\ExampleCases\ProximalBPS\ActualHarmonicFlow.lean`
- Layer: uncategorized
- Purpose:
- Mathlib-quality status:

## Imports

- `Mathlib.Tactic.Module`
- `Mathlib.Tactic.FieldSimp`
- `Mathlib.Tactic.FunProp`
- `Mathlib.Tactic.LinearCombination`
- `AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient`
- `Mathlib.Analysis.SpecialFunctions.Trigonometric.Deriv`
- `Mathlib.MeasureTheory.Constructions.BorelSpace.Basic`

## Representative Declarations And Exports

- `actual_harmonic_flow_statement`
- `actual_harmonic_flow_laws`

## Curated Formalized Memory Entries

- `pbps.actualHarmonicFlow` -> `actual_harmonic_flow_laws` (arXiv2609.06905v1 Section2 Algorithm1 and AppendixA1 Proposition3.1 construction)

## Agent Usage

Search this card before inventing a nearby technical lemma.  If the needed fact
is generic and missing, create a Mathlib-ready leaf packet rather than hiding
the requirement inside a paper-specific theorem.
