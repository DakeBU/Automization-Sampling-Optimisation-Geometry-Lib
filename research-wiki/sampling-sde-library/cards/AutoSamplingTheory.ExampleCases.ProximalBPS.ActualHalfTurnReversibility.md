# AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHalfTurnReversibility

- File: `AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHalfTurnReversibility.lean`
- Layer: route-local theorem edge
- Purpose: Every-y detailed balance for the SAME actual PBPS returned-position kernel after independent-reference averaging.
- Mathlib-quality status: Independently source/compiler VERIFIED; canonical integration and purification are separate gates. Private signed-Fubini/indicator adapters are not separate Registry leaves.
- Verification: [exact source, tests, seven-slot audit and integration](../../paper-contributions/PBPS/actual-half-turn-reversibility-verification.json).

## Imports

- `AutoSamplingTheory.ExampleCases.ProximalBPS.IdealHalfTurnKernel`
- `AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBoundedGibbsDuality`
- `Mathlib.Probability.Kernel.Invariance`

## Representative Declarations And Exports

- `actual_half_turn_reversible`
- Private implementation: `flux_ofReal`, `reversible_of_bounded_pairing`, `pairing_eq_reference_average`, `reversible_of_reference_average`, and the complete sealed proposition. They introduce no extra public hypotheses or mathematical leaves.

## Curated Formalized Memory Entries

- `pbps.actualHalfTurnReversibility` -> `actual_half_turn_reversible` (arXiv2609.06905v1 Proposition3.2 and Appendix A.2)

## Dependencies and Boundaries

Reuse the actual ideal-kernel and bounded signed phase-duality producers plus
the unit exponential product laws. The actual kernel/L2 realization is not a
proof parent merely because its integration preceded this result. Probability,
same-witness identification, measurability and finite signed Fubini are derived.
Mathlib `Kernel.IsReversible` means all measurable rectangles, not a singleton
criterion restricted to countable states. Rank-zero Hilbert spaces are retained.

The real planned paper consumer is Proposition3.4's actual augmented one-step
kernel; no existing downstream Lean consumer is invented. This is not temporal
restart or a semigroup, augmented L2 realization, hypocoercivity, implementation
error/cost, initialization, composition, or a full-paper result.
