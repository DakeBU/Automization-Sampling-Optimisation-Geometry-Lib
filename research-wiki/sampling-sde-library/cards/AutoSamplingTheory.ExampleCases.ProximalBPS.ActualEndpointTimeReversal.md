# AutoSamplingTheory.ExampleCases.ProximalBPS.ActualEndpointTimeReversal

- File: `AutoSamplingTheory\ExampleCases\ProximalBPS\ActualEndpointTimeReversal.lean`
- Layer: uncategorized
- Purpose:
- Mathlib-quality status:

## Imports

- `AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteCountPath`
- `AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhaseReversalVolume`
- `Mathlib.Data.Fin.Rev`
- `Mathlib.Order.Fin.Tuple`

## Representative Declarations And Exports

- `delta`
- `reverseTime`
- `reverseTime_involutive`
- `reverseTime_mem`
- `reverseTime_measurable`
- `reverseTime_volume`
- `rho`
- `rho_measurable`
- `rho_involutive`
- `rho_volume`
- `reverse_fold_cancel`
- `fold_of_sequence`
- `gaps`
- `gaps_reversed`
- `post`
- `endpoint`
- `endpoint_as_word`
- `endpoint_reversed`
- `preserving_fold`
- `endpoint_volume`
- `endpoint_data_statement`
- `endpoint_data`
- `actual_endpoint_time_reversal_statement`
- `actual_endpoint_time_reversal_laws`

## Curated Formalized Memory Entries

- `pbps.actualEndpointTimeReversal` -> `actual_endpoint_time_reversal_laws` (arXiv2609.06905v1 Appendix A1 endpoint/time substitution surrounding A8)

## Agent Usage

Search this card before inventing a nearby technical lemma.  If the needed fact
is generic and missing, create a Mathlib-ready leaf packet rather than hiding
the requirement inside a paper-specific theorem.
