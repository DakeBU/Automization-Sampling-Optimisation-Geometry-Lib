# AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteCountPath

- File: `AutoSamplingTheory\ExampleCases\ProximalBPS\ActualFiniteCountPath.lean`
- Layer: uncategorized
- Purpose:
- Mathlib-quality status:

## Imports

- `AutoSamplingTheory.ExampleCases.ProximalBPS.ActualOrderedPrefix`
- `AutoSamplingTheory.ExampleCases.ProximalBPS.ActualConditionalNextWaitSurvival`
- `AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhysicalTimeMeasurability`
- `Mathlib.Data.Set.Card`
- `Mathlib.Order.Interval.Set.Nat`
- `Mathlib.MeasureTheory.Constructions.Pi`

## Representative Declarations And Exports

- `measurable_finite_fold`
- `measurable_record_step`
- `measurable_history_interpolation`
- `finite_fold_last_eligible`
- `terminal_elim_identity`
- `measurable_terminal_record_weight`
- `real_time_history_fold`
- `actual_history_interpolation_measurable`
- `localized_survival_history_measure`
- `actual_terminal_survival_history_tests`
- `actual_terminal_weighted_prefix_tests`
- `finite_history_fold_eq_process`
- `terminal_event_after`
- `actual_history_path_identification`
- `find_decidable_eq`
- `measurable_first_available`
- `monotone_intervals_unique`
- `interval_count_cardinality`
- `actual_count_selector_measurable`
- `actual_prescribed_path_interpolation`
- `subtype_coordinate_null`
- `weighted_map_coordinate_null`
- `live_prefix_strict_guard`
- `actual_fixed_horizon_endpoint_nullity`
- `actual_count_event_identification`
- `actual_finite_count_path_statement`
- `actual_finite_count_path_law`

## Curated Formalized Memory Entries

- `pbps.actualFiniteCountPath` -> `actual_finite_count_path_law` (arXiv2609.06905v1 Appendix A1 A7 finite-count ingredient and Appendix A2)

## Agent Usage

Search this card before inventing a nearby technical lemma.  If the needed fact
is generic and missing, create a Mathlib-ready leaf packet rather than hiding
the requirement inside a paper-specific theorem.
