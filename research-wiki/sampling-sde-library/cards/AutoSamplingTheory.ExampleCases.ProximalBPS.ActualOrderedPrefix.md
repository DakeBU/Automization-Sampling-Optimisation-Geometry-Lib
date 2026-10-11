# AutoSamplingTheory.ExampleCases.ProximalBPS.ActualOrderedPrefix

- File: `AutoSamplingTheory\ExampleCases\ProximalBPS\ActualOrderedPrefix.lean`
- Layer: uncategorized
- Purpose:
- Mathlib-quality status:

## Imports

- `AutoSamplingTheory.ExampleCases.ProximalBPS.ActualAbsoluteNextEventTime`
- `Mathlib.MeasureTheory.Constructions.Pi`
- `Mathlib.Order.Fin.Tuple`

## Representative Declarations And Exports

- `measurable_cons_zero`
- `simplex_measurable`
- `readTime`
- `readTime_measurable`
- `live_measurable`
- `history_guard_measurable`
- `ordered_prefix_borel_data`
- `actual_prefix_identification`
- `actual_prefix_base_integral`
- `guard`
- `guard_snoc`
- `record_history_snoc`
- `record_guard_step`
- `record_event_step`
- `actual_prefix_step_integral`
- `strictMono_snoc`
- `simplex_snoc`
- `snoc_volume_preserving`
- `orderedSimplex`
- `simplex_lintegral_snoc`
- `snocPrefix`
- `subtype_simplex_lintegral_snoc`
- `state`
- `state_snoc_prefix`
- `state_snoc_last`
- `weight`
- `weight_snoc`
- `timedHistory`
- `timedHistory_snoc`
- `ordered_last_nonneg`
- `weight_snoc_ofReal`
- `actual_prefix_all_integrals`
- `law_and_mass_of_all_tests`
- `actual_ordered_prefix_statement`
- `actual_ordered_prefix_law`

## Curated Formalized Memory Entries

- `pbps.actualOrderedPrefix` -> `actual_ordered_prefix_law` (arXiv2609.06905v1 Appendix A1 A1 A2 A7 finite iteration ingredient and Appendix A2)

## Agent Usage

Search this card before inventing a nearby technical lemma.  If the needed fact
is generic and missing, create a Mathlib-ready leaf packet rather than hiding
the requirement inside a paper-specific theorem.
